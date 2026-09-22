#!/usr/bin/env python3
"""Fit a post-hoc censored regression to standalone convergence iterations."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from execute_study import JsonValue
from scipy.optimize import OptimizeResult, minimize
from scipy.special import log_ndtr, ndtr

type BoolArray = npt.NDArray[np.bool_]
type RealArray = npt.NDArray[np.float64]


class CensoredConvergenceRegressionAction:
    """Fit a log-normal accelerated-failure-time model with right censoring."""

    __slots__ = ()

    _reference_group = ("fixed_c31_p4_n23", "baseline_preconditioned")
    _reference_start = "identity"

    def execute(self, result_path: Path, output_path: Path) -> dict[str, JsonValue]:
        result = self._load(result_path)
        endpoints = [self._mapping(value) for value in self._array(result["endpoints"])]
        groups = [self._mapping(value) for value in self._array(result["groups"])]
        group_keys = self._ordered_group_keys(groups)
        start_ids = ["identity", *[f"halton_{index:02d}" for index in range(1, 16)]]
        design, times, converged, cluster_ids = self._design(
            endpoints, group_keys, start_ids
        )
        log_times = np.log(times)
        initial = np.zeros(design.shape[1] + 1, dtype=np.float64)
        initial[:-1], _, _, _ = np.linalg.lstsq(design, log_times, rcond=None)
        initial[-1] = math.log(max(float(np.std(log_times)), 0.2))
        optimized = cast(
            OptimizeResult,
            minimize(
                self._objective_with_gradient,
                initial,
                args=(design, log_times, converged),
                method="L-BFGS-B",
                jac=True,
                bounds=[(None, None)] * design.shape[1] + [(-5.0, 5.0)],
                options={"maxiter": 5000, "ftol": 1.0e-12, "gtol": 1.0e-8},
            ),
        )
        if not bool(optimized.success):
            raise RuntimeError(f"censored regression failed: {optimized.message}")
        parameters = np.asarray(optimized.x, dtype=np.float64)
        covariance, hessian_condition = self._cluster_covariance(
            parameters, design, log_times, converged, cluster_ids
        )
        estimates = self._category_estimates(
            endpoints,
            group_keys,
            start_ids,
            parameters,
            covariance,
        )
        _, gradient = self._objective_with_gradient(
            parameters, design, log_times, converged
        )
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "evidence_status": (
                "post-hoc exploratory censored regression of calculated synthetic "
                "non-DFT trajectories"
            ),
            "source_result_path": str(result_path),
            "source_result_sha256": hashlib.sha256(
                result_path.read_bytes()
            ).hexdigest(),
            "model": {
                "family": "log-normal accelerated-failure-time",
                "response": "total optimizer iterations to native convergence",
                "censoring": (
                    "right-censored at the retained final iteration for trajectories "
                    "without the native convergence statement"
                ),
                "category_effects": "configuration-by-optimizer group",
                "start_adjustment": "fixed effect for each deterministic start",
                "reference_group": self._group_key(*self._reference_group),
                "reference_start": self._reference_start,
                "intervals": (
                    "exploratory model-based 95% sandwich intervals clustered by "
                    "the 16 deterministic starts; they have no population-sampling "
                    "or physical-uncertainty interpretation"
                ),
                "interpretation": (
                    "time ratios above one indicate more iterations to native "
                    "convergence; estimates are descriptive and not causal"
                ),
            },
            "observation_count": len(endpoints),
            "converged_count": int(np.sum(converged)),
            "right_censored_count": int(np.sum(~converged)),
            "parameter_count": len(parameters),
            "parameters": [
                {"name": name, "value": float(value)}
                for name, value in zip(
                    self._parameter_names(group_keys, start_ids),
                    parameters,
                    strict=True,
                )
            ],
            "negative_log_likelihood": float(optimized.fun),
            "gradient_infinity_norm": float(np.max(np.abs(gradient))),
            "hessian_condition_number": hessian_condition,
            "log_time_scale": float(parameters[-1]),
            "time_scale": math.exp(float(parameters[-1])),
            "category_estimates": estimates,
            "claim_boundary": (
                "This post-hoc model summarizes the retained finite trajectories. "
                "It does not alter native convergence, establish causality, prove "
                "optimizer convergence, or predict DFT behavior."
            ),
        }
        output_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return payload

    def _design(
        self,
        endpoints: list[dict[str, JsonValue]],
        group_keys: list[tuple[str, str]],
        start_ids: list[str],
    ) -> tuple[RealArray, RealArray, BoolArray, npt.NDArray[np.int64]]:
        group_columns = {
            key: index + 1
            for index, key in enumerate(
                key for key in group_keys if key != self._reference_group
            )
        }
        start_offset = 1 + len(group_columns)
        start_columns = {
            start_id: start_offset + index
            for index, start_id in enumerate(
                value for value in start_ids if value != self._reference_start
            )
        }
        design = np.zeros(
            (len(endpoints), 1 + len(group_columns) + len(start_columns)),
            dtype=np.float64,
        )
        design[:, 0] = 1.0
        times = np.empty(len(endpoints), dtype=np.float64)
        converged = np.empty(len(endpoints), dtype=np.bool_)
        cluster_ids = np.empty(len(endpoints), dtype=np.int64)
        start_index = {value: index for index, value in enumerate(start_ids)}
        for row, endpoint in enumerate(endpoints):
            key = (
                self._string(endpoint["configuration_id"]),
                self._string(endpoint["arm"]),
            )
            group_column = group_columns.get(key)
            if group_column is not None:
                design[row, group_column] = 1.0
            start_id = self._string(endpoint["start_id"])
            start_column = start_columns.get(start_id)
            if start_column is not None:
                design[row, start_column] = 1.0
            times[row] = self._real(endpoint["effective_total_iterations"])
            converged[row] = endpoint["effective_native_converged"] is True
            cluster_ids[row] = start_index[start_id]
        return design, times, converged, cluster_ids

    def _objective_with_gradient(
        self,
        parameters: RealArray,
        design: RealArray,
        log_times: RealArray,
        converged: BoolArray,
    ) -> tuple[float, RealArray]:
        coefficients = parameters[:-1]
        log_scale = float(parameters[-1])
        scale = math.exp(log_scale)
        residual = (log_times - design @ coefficients) / scale
        event_loss = (
            log_scale + 0.5 * residual[converged] ** 2 + 0.5 * math.log(2.0 * math.pi)
        )
        censored_loss = -log_ndtr(-residual[~converged])
        loss = float(np.sum(event_loss) + np.sum(censored_loss))
        gradients = self._observation_gradients(
            parameters, design, log_times, converged
        )
        return loss, np.sum(gradients, axis=0)

    def _observation_gradients(
        self,
        parameters: RealArray,
        design: RealArray,
        log_times: RealArray,
        converged: BoolArray,
    ) -> RealArray:
        coefficients = parameters[:-1]
        scale = math.exp(float(parameters[-1]))
        residual = (log_times - design @ coefficients) / scale
        gradients = np.zeros((len(log_times), len(parameters)), dtype=np.float64)
        gradients[converged, :-1] = (
            -residual[converged, None] * design[converged] / scale
        )
        gradients[converged, -1] = 1.0 - residual[converged] ** 2
        censored_residual = residual[~converged]
        log_density = -0.5 * censored_residual**2 - 0.5 * math.log(2.0 * math.pi)
        inverse_mills = np.exp(log_density - log_ndtr(-censored_residual))
        gradients[~converged, :-1] = (
            -inverse_mills[:, None] * design[~converged] / scale
        )
        gradients[~converged, -1] = -inverse_mills * censored_residual
        return gradients

    def _cluster_covariance(
        self,
        parameters: RealArray,
        design: RealArray,
        log_times: RealArray,
        converged: BoolArray,
        cluster_ids: npt.NDArray[np.int64],
    ) -> tuple[RealArray, float]:
        dimension = len(parameters)
        hessian = np.empty((dimension, dimension), dtype=np.float64)
        for column in range(dimension):
            step = 1.0e-5 * max(1.0, abs(float(parameters[column])))
            plus = parameters.copy()
            minus = parameters.copy()
            plus[column] += step
            minus[column] -= step
            _, plus_gradient = self._objective_with_gradient(
                plus, design, log_times, converged
            )
            _, minus_gradient = self._objective_with_gradient(
                minus, design, log_times, converged
            )
            hessian[:, column] = (plus_gradient - minus_gradient) / (2.0 * step)
        hessian = 0.5 * (hessian + hessian.T)
        bread = np.linalg.pinv(hessian, rcond=1.0e-12)
        observation_scores = self._observation_gradients(
            parameters, design, log_times, converged
        )
        cluster_scores = np.stack(
            [
                np.sum(observation_scores[cluster_ids == cluster], axis=0)
                for cluster in np.unique(cluster_ids)
            ]
        )
        meat = cluster_scores.T @ cluster_scores
        cluster_count = cluster_scores.shape[0]
        observation_count = len(log_times)
        correction = (cluster_count / (cluster_count - 1.0)) * (
            (observation_count - 1.0) / (observation_count - dimension)
        )
        covariance = correction * bread @ meat @ bread
        return covariance, float(np.linalg.cond(hessian))

    def _category_estimates(
        self,
        endpoints: list[dict[str, JsonValue]],
        group_keys: list[tuple[str, str]],
        start_ids: list[str],
        parameters: RealArray,
        covariance: RealArray,
    ) -> list[JsonValue]:
        group_parameter = {
            key: index + 1
            for index, key in enumerate(
                key for key in group_keys if key != self._reference_group
            )
        }
        start_offset = 1 + len(group_parameter)
        mean_start_effect = sum(
            float(parameters[start_offset + index])
            for index, _ in enumerate(
                value for value in start_ids if value != self._reference_start
            )
        ) / len(start_ids)
        estimates: list[JsonValue] = []
        scale = math.exp(float(parameters[-1]))
        checkpoints = (500, 1000, 2500, 5000, 10000, 20000)
        for key in group_keys:
            selected = [
                endpoint
                for endpoint in endpoints
                if endpoint["configuration_id"] == key[0] and endpoint["arm"] == key[1]
            ]
            parameter_index = group_parameter.get(key)
            log_ratio = (
                0.0 if parameter_index is None else float(parameters[parameter_index])
            )
            standard_error = (
                0.0
                if parameter_index is None
                else math.sqrt(
                    max(float(covariance[parameter_index, parameter_index]), 0.0)
                )
            )
            lower = math.exp(log_ratio - 1.96 * standard_error)
            upper = math.exp(log_ratio + 1.96 * standard_error)
            adjusted_log_median = float(parameters[0]) + log_ratio + mean_start_effect
            estimates.append(
                {
                    "group_key": self._group_key(*key),
                    "label": self._label(*key),
                    "converged_count": sum(
                        value["effective_native_converged"] is True
                        for value in selected
                    ),
                    "right_censored_count": sum(
                        value["effective_native_converged"] is False
                        for value in selected
                    ),
                    "log_time_ratio": log_ratio,
                    "clustered_standard_error": standard_error,
                    "time_ratio": math.exp(log_ratio),
                    "time_ratio_95_percent_interval": [lower, upper],
                    "adjusted_median_iterations": math.exp(adjusted_log_median),
                    "predicted_convergence_probability": [
                        {
                            "iterations": checkpoint,
                            "probability": float(
                                ndtr(
                                    (math.log(checkpoint) - adjusted_log_median) / scale
                                )
                            ),
                        }
                        for checkpoint in checkpoints
                    ],
                }
            )
        return estimates

    def _ordered_group_keys(
        self, groups: list[dict[str, JsonValue]]
    ) -> list[tuple[str, str]]:
        available = {
            (self._string(value["configuration_id"]), self._string(value["arm"]))
            for value in groups
        }
        ordered = [
            *(
                (f"fixed_c31_p4_n{size}", "baseline_preconditioned")
                for size in (11, 15, 19, 23, 27, 31)
            ),
            *(
                (f"balanced_p4_n{size}_c{size}", "baseline_preconditioned")
                for size in (11, 15, 19, 23, 27)
            ),
            *(
                (f"fixed_c31_p{cutoff}_n23", "baseline_preconditioned")
                for cutoff in (3, 5, 6)
            ),
            ("fixed_c31_p4_n23", "control_preconditioner_off"),
            ("balanced_p4_n23_c23", "control_preconditioner_off"),
        ]
        if set(ordered) != available:
            raise AssertionError(
                "regression group ordering does not cover result groups"
            )
        return ordered

    def _parameter_names(
        self, group_keys: list[tuple[str, str]], start_ids: list[str]
    ) -> list[str]:
        return [
            "intercept",
            *[
                f"group:{self._group_key(*key)}"
                for key in group_keys
                if key != self._reference_group
            ],
            *[
                f"start:{start_id}"
                for start_id in start_ids
                if start_id != self._reference_start
            ],
            "log_scale",
        ]

    @staticmethod
    def _group_key(configuration_id: str, arm: str) -> str:
        return f"{configuration_id}:{arm}"

    @staticmethod
    def _label(configuration_id: str, arm: str) -> str:
        if arm == "control_preconditioner_off":
            if configuration_id.startswith("fixed"):
                return r"fixed $N=23$, preconditioner off"
            return r"balanced $N=23$, preconditioner off"
        if configuration_id.startswith("balanced"):
            size = configuration_id.split("_n", maxsplit=1)[1].split("_", maxsplit=1)[0]
            return rf"balanced $N={size}$"
        pieces = configuration_id.split("_")
        cutoff = next(value[1:] for value in pieces if value.startswith("p"))
        size = next(value[1:] for value in pieces if value.startswith("n"))
        if cutoff == "4":
            return rf"fixed $N={size}$"
        return rf"cutoff $P={cutoff}$"

    def _load(self, path: Path) -> dict[str, JsonValue]:
        return self._mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        )

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected an object")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)


class CommandAdapter:
    """Adapt command-line paths to the regression action."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--result", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        arguments = parser.parse_args(argv)
        payload = CensoredConvergenceRegressionAction().execute(
            cast(Path, arguments.result).resolve(),
            cast(Path, arguments.output).resolve(),
        )
        print(
            json.dumps(
                {
                    "converged_count": payload["converged_count"],
                    "right_censored_count": payload["right_censored_count"],
                    "gradient_infinity_norm": payload["gradient_infinity_norm"],
                },
                indent=2,
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
