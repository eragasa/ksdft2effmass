#!/usr/bin/env python3
"""Independently verify the post-hoc censored convergence regression record."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import cast

import numpy as np
from execute_study import JsonValue
from scipy.special import log_ndtr, ndtr


class CensoredConvergenceRegressionVerifier:
    """Reconstruct counts, likelihood, gradient, ratios, and probability curves."""

    __slots__ = ()

    def execute(self, source_path: Path, regression_path: Path) -> None:
        source = self._load(source_path)
        regression = self._load(regression_path)
        endpoints = [self._mapping(value) for value in self._array(source["endpoints"])]
        if hashlib.sha256(source_path.read_bytes()).hexdigest() != self._string(
            regression["source_result_sha256"]
        ):
            raise AssertionError("regression source identity disagrees")
        parameter_records = [
            self._mapping(value) for value in self._array(regression["parameters"])
        ]
        names = [self._string(value["name"]) for value in parameter_records]
        parameters = np.asarray(
            [self._real(value["value"]) for value in parameter_records], dtype=float
        )
        design = np.zeros((len(endpoints), len(parameters) - 1), dtype=float)
        design[:, 0] = 1.0
        times = np.empty(len(endpoints), dtype=float)
        converged = np.empty(len(endpoints), dtype=bool)
        cluster_ids = np.empty(len(endpoints), dtype=np.int64)
        name_to_column = {name: index for index, name in enumerate(names[:-1])}
        start_ids = ["identity", *[f"halton_{index:02d}" for index in range(1, 16)]]
        start_to_cluster = {start_id: index for index, start_id in enumerate(start_ids)}
        for row, endpoint in enumerate(endpoints):
            group_name = (
                "group:"
                f"{self._string(endpoint['configuration_id'])}:"
                f"{self._string(endpoint['arm'])}"
            )
            start_name = f"start:{self._string(endpoint['start_id'])}"
            group_column = name_to_column.get(group_name)
            start_column = name_to_column.get(start_name)
            if group_column is not None:
                design[row, group_column] = 1.0
            if start_column is not None:
                design[row, start_column] = 1.0
            times[row] = self._real(endpoint["effective_total_iterations"])
            converged[row] = endpoint["effective_native_converged"] is True
            cluster_ids[row] = start_to_cluster[self._string(endpoint["start_id"])]
        self._equal(
            self._integer(regression["observation_count"]),
            len(endpoints),
            "observation count",
        )
        self._equal(
            self._integer(regression["converged_count"]),
            int(np.sum(converged)),
            "converged count",
        )
        self._equal(
            self._integer(regression["right_censored_count"]),
            int(np.sum(~converged)),
            "right-censored count",
        )
        self._equal(
            self._integer(regression["parameter_count"]),
            len(parameters),
            "parameter count",
        )
        loss, gradient = self._objective(parameters, design, np.log(times), converged)
        self._close(
            self._real(regression["negative_log_likelihood"]),
            loss,
            1.0e-9,
            "negative log likelihood",
        )
        self._close(
            self._real(regression["gradient_infinity_norm"]),
            float(np.max(np.abs(gradient))),
            1.0e-9,
            "gradient infinity norm",
        )
        if float(np.max(np.abs(gradient))) > 2.0e-4:
            raise AssertionError("regression gradient is too large")
        covariance, hessian_condition = self._cluster_covariance(
            parameters,
            design,
            np.log(times),
            converged,
            cluster_ids,
        )
        self._close(
            self._real(regression["hessian_condition_number"]),
            hessian_condition,
            1.0e-7,
            "Hessian condition number",
        )
        self._close(
            self._real(regression["log_time_scale"]),
            float(parameters[-1]),
            1.0e-12,
            "log-time scale",
        )
        scale = math.exp(float(parameters[-1]))
        self._close(
            self._real(regression["time_scale"]),
            scale,
            1.0e-12,
            "time scale",
        )
        start_effects = [
            float(parameters[index])
            for name, index in name_to_column.items()
            if name.startswith("start:")
        ]
        mean_start_effect = sum(start_effects) / 16.0
        for value in self._array(regression["category_estimates"]):
            estimate = self._mapping(value)
            key = self._string(estimate["group_key"])
            coefficient_index = name_to_column.get(f"group:{key}")
            log_ratio = (
                0.0
                if coefficient_index is None
                else float(parameters[coefficient_index])
            )
            self._close(
                self._real(estimate["time_ratio"]),
                math.exp(log_ratio),
                1.0e-12,
                "time ratio",
            )
            standard_error = (
                0.0
                if coefficient_index is None
                else math.sqrt(
                    max(float(covariance[coefficient_index, coefficient_index]), 0.0)
                )
            )
            self._close(
                self._real(estimate["clustered_standard_error"]),
                standard_error,
                1.0e-9,
                "clustered standard error",
            )
            interval = self._array(estimate["time_ratio_95_percent_interval"])
            self._close(
                self._real(interval[0]),
                math.exp(log_ratio - 1.96 * standard_error),
                1.0e-9,
                "time-ratio lower interval",
            )
            self._close(
                self._real(interval[1]),
                math.exp(log_ratio + 1.96 * standard_error),
                1.0e-9,
                "time-ratio upper interval",
            )
            selected = [
                endpoint
                for endpoint in endpoints
                if (
                    f"{self._string(endpoint['configuration_id'])}:"
                    f"{self._string(endpoint['arm'])}"
                )
                == key
            ]
            self._equal(
                self._integer(estimate["converged_count"]),
                sum(value["effective_native_converged"] is True for value in selected),
                "category converged count",
            )
            self._equal(
                self._integer(estimate["right_censored_count"]),
                sum(value["effective_native_converged"] is False for value in selected),
                "category right-censored count",
            )
            adjusted_log_median = float(parameters[0]) + log_ratio + mean_start_effect
            self._close(
                self._real(estimate["adjusted_median_iterations"]),
                math.exp(adjusted_log_median),
                1.0e-9,
                "adjusted median iterations",
            )
            for probability_value in self._array(
                estimate["predicted_convergence_probability"]
            ):
                probability = self._mapping(probability_value)
                iterations = self._integer(probability["iterations"])
                expected = float(
                    ndtr((math.log(iterations) - adjusted_log_median) / scale)
                )
                self._close(
                    self._real(probability["probability"]),
                    expected,
                    1.0e-12,
                    "predicted convergence probability",
                )
        print("periodic_2d_standalone_convergence_regression_verification=PASS")

    def _objective(
        self,
        parameters: np.ndarray,
        design: np.ndarray,
        log_times: np.ndarray,
        converged: np.ndarray,
    ) -> tuple[float, np.ndarray]:
        coefficients = parameters[:-1]
        log_scale = float(parameters[-1])
        scale = math.exp(log_scale)
        residual = (log_times - design @ coefficients) / scale
        event_loss = (
            log_scale + 0.5 * residual[converged] ** 2 + 0.5 * math.log(2.0 * math.pi)
        )
        censored_loss = -log_ndtr(-residual[~converged])
        gradient_rows = self._observation_gradients(
            parameters, design, log_times, converged
        )
        return (
            float(np.sum(event_loss) + np.sum(censored_loss)),
            np.sum(gradient_rows, axis=0),
        )

    def _observation_gradients(
        self,
        parameters: np.ndarray,
        design: np.ndarray,
        log_times: np.ndarray,
        converged: np.ndarray,
    ) -> np.ndarray:
        coefficients = parameters[:-1]
        scale = math.exp(float(parameters[-1]))
        residual = (log_times - design @ coefficients) / scale
        gradient_rows = np.zeros((len(log_times), len(parameters)), dtype=float)
        gradient_rows[converged, :-1] = (
            -residual[converged, None] * design[converged] / scale
        )
        gradient_rows[converged, -1] = 1.0 - residual[converged] ** 2
        censored_residual = residual[~converged]
        inverse_mills = np.exp(
            -0.5 * censored_residual**2
            - 0.5 * math.log(2.0 * math.pi)
            - log_ndtr(-censored_residual)
        )
        gradient_rows[~converged, :-1] = (
            -inverse_mills[:, None] * design[~converged] / scale
        )
        gradient_rows[~converged, -1] = -inverse_mills * censored_residual
        return gradient_rows

    def _cluster_covariance(
        self,
        parameters: np.ndarray,
        design: np.ndarray,
        log_times: np.ndarray,
        converged: np.ndarray,
        cluster_ids: np.ndarray,
    ) -> tuple[np.ndarray, float]:
        dimension = len(parameters)
        hessian = np.empty((dimension, dimension), dtype=float)
        for column in range(dimension):
            step = 1.0e-5 * max(1.0, abs(float(parameters[column])))
            plus = parameters.copy()
            minus = parameters.copy()
            plus[column] += step
            minus[column] -= step
            _, plus_gradient = self._objective(plus, design, log_times, converged)
            _, minus_gradient = self._objective(minus, design, log_times, converged)
            hessian[:, column] = (plus_gradient - minus_gradient) / (2.0 * step)
        hessian = 0.5 * (hessian + hessian.T)
        inverse_hessian = np.linalg.pinv(hessian, rcond=1.0e-12)
        observation_scores = self._observation_gradients(
            parameters, design, log_times, converged
        )
        cluster_scores = np.stack(
            [
                np.sum(observation_scores[cluster_ids == cluster], axis=0)
                for cluster in np.unique(cluster_ids)
            ]
        )
        cluster_count = cluster_scores.shape[0]
        correction = (cluster_count / (cluster_count - 1.0)) * (
            (len(log_times) - 1.0) / (len(log_times) - dimension)
        )
        meat = cluster_scores.T @ cluster_scores
        covariance = correction * inverse_hessian @ meat @ inverse_hessian
        return covariance, float(np.linalg.cond(hessian))

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
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    @staticmethod
    def _equal(actual: int, expected: int, label: str) -> None:
        if actual != expected:
            raise AssertionError(f"{label}: actual={actual}, expected={expected}")

    @staticmethod
    def _close(actual: float, expected: float, tolerance: float, label: str) -> None:
        if abs(actual - expected) > tolerance:
            raise AssertionError(
                f"{label}: actual={actual:.16e}, expected={expected:.16e}"
            )


class CommandAdapter:
    """Adapt source and regression paths to the verifier."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--source-result", type=Path, required=True)
        parser.add_argument("--regression-result", type=Path, required=True)
        arguments = parser.parse_args(argv)
        CensoredConvergenceRegressionVerifier().execute(
            cast(Path, arguments.source_result).resolve(),
            cast(Path, arguments.regression_result).resolve(),
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
