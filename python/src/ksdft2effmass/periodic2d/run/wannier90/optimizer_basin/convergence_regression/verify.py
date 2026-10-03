"""Independent portable verification of censored optimizer regression."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from scipy.special import log_ndtr, ndtr  # type: ignore[import-untyped]

from .encoded_documents import Periodic2DOptimizerRegressionEncodedDocuments

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type FloatArray = npt.NDArray[np.float64]
type BoolArray = npt.NDArray[np.bool_]
type IntArray = npt.NDArray[np.int64]


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerRegressionCampaignVerificationRequest:
    """Request independent reconstruction of the retained censored regression."""

    encoded_documents: Periodic2DOptimizerRegressionEncodedDocuments
    repository_root: Path


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerRegressionCampaignVerificationResult:
    """Report source authentication and reconstructed model diagnostics."""

    source_authentication_passed: bool
    numerical_reconstruction_passed: bool
    observation_count: int
    converged_count: int
    right_censored_count: int
    parameter_count: int
    retained_result_sha256: str

    @property
    def passes(self) -> bool:
        """Return the aggregate bounded verification disposition."""
        return (
            self.source_authentication_passed and self.numerical_reconstruction_passed
        )


class Periodic2DOptimizerRegressionCampaignVerifier:
    """Reconstruct likelihood, scores, clustered intervals, ratios, and curves."""

    __slots__ = ()
    _analyzer_sha256 = (
        "e80c16ab7fd11d86e6c51a344e01790306982f1a628b962611dfd0291d16fe46"
    )

    def execute(
        self, request: Periodic2DOptimizerRegressionCampaignVerificationRequest
    ) -> Periodic2DOptimizerRegressionCampaignVerificationResult:
        """Verify one retained regression without importing its maintained analyzer."""
        source = self._mapping(
            cast(
                JsonValue,
                json.loads(request.encoded_documents.standalone_result_payload),
            )
        )
        regression = self._mapping(
            cast(JsonValue, json.loads(request.encoded_documents.regression_payload))
        )
        self._equal(self._integer(regression["schema_version"]), 1, "regression schema")
        self._identity(
            request.encoded_documents.standalone_result_payload,
            self._string(regression["source_result_sha256"]),
            "standalone result",
        )
        self._identity(
            request.encoded_documents.analyzer_payload,
            self._analyzer_sha256,
            "regression analyzer",
        )
        endpoints = self._records(source["endpoints"])
        parameter_records = self._records(regression["parameters"])
        names = [self._string(item["name"]) for item in parameter_records]
        parameters = np.asarray(
            [self._real(item["value"]) for item in parameter_records], dtype=np.float64
        )
        if (
            len(names) != len(set(names))
            or names[0] != "intercept"
            or names[-1] != "log_scale"
        ):
            raise AssertionError("parameter identities disagree")
        design = np.zeros((len(endpoints), len(parameters) - 1), dtype=np.float64)
        design[:, 0] = 1.0
        times = np.empty(len(endpoints), dtype=np.float64)
        converged = np.empty(len(endpoints), dtype=np.bool_)
        cluster_ids = np.empty(len(endpoints), dtype=np.int64)
        name_to_column = {name: index for index, name in enumerate(names[:-1])}
        starts = sorted(
            {
                (self._integer(item["start_index"]), self._string(item["start_id"]))
                for item in endpoints
            }
        )
        start_to_cluster = {
            start_id: index for index, (_, start_id) in enumerate(starts)
        }
        if [index for index, _ in starts] != list(range(16)):
            raise AssertionError("start clusters disagree")
        for row, endpoint in enumerate(endpoints):
            group = (
                f"group:{self._string(endpoint['configuration_id'])}:"
                f"{self._string(endpoint['arm'])}"
            )
            start = f"start:{self._string(endpoint['start_id'])}"
            group_column = name_to_column.get(group)
            start_column = name_to_column.get(start)
            if group_column is not None:
                design[row, group_column] = 1.0
            if start_column is not None:
                design[row, start_column] = 1.0
            times[row] = self._real(endpoint["effective_total_iterations"])
            converged[row] = self._boolean(endpoint["effective_native_converged"])
            cluster_ids[row] = start_to_cluster[self._string(endpoint["start_id"])]
        observed_count = len(endpoints)
        converged_count = int(np.sum(converged))
        censored_count = int(np.sum(~converged))
        for key, value in (
            ("observation_count", observed_count),
            ("converged_count", converged_count),
            ("right_censored_count", censored_count),
            ("parameter_count", len(parameters)),
        ):
            self._equal(self._integer(regression[key]), value, key)
        loss, gradient = self._objective(parameters, design, np.log(times), converged)
        self._close(
            self._real(regression["negative_log_likelihood"]),
            loss,
            1.0e-9,
            "negative log likelihood",
        )
        gradient_norm = float(np.max(np.abs(gradient)))
        self._close(
            self._real(regression["gradient_infinity_norm"]),
            gradient_norm,
            1.0e-9,
            "gradient infinity norm",
        )
        if gradient_norm > 2.0e-4:
            raise AssertionError("regression gradient is too large")
        covariance, condition = self._cluster_covariance(
            parameters, design, np.log(times), converged, cluster_ids
        )
        self._close(
            self._real(regression["hessian_condition_number"]),
            condition,
            1.0e-7,
            "Hessian condition number",
        )
        log_scale = float(parameters[-1])
        self._close(
            self._real(regression["log_time_scale"]),
            log_scale,
            1.0e-12,
            "log-time scale",
        )
        scale = math.exp(log_scale)
        self._close(self._real(regression["time_scale"]), scale, 1.0e-12, "time scale")
        start_effects = [
            float(parameters[index])
            for name, index in name_to_column.items()
            if name.startswith("start:")
        ]
        mean_start_effect = sum(start_effects) / 16.0
        estimates = self._records(regression["category_estimates"])
        if len(estimates) != 16:
            raise AssertionError("category count disagrees")
        for estimate in estimates:
            key = self._string(estimate["group_key"])
            coefficient_index = name_to_column.get(f"group:{key}")
            log_ratio = (
                0.0
                if coefficient_index is None
                else float(parameters[coefficient_index])
            )
            self._close(
                self._real(estimate["log_time_ratio"]),
                log_ratio,
                1.0e-12,
                "log time ratio",
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
                "ratio lower interval",
            )
            self._close(
                self._real(interval[1]),
                math.exp(log_ratio + 1.96 * standard_error),
                1.0e-9,
                "ratio upper interval",
            )
            selected = [
                item
                for item in endpoints
                if (
                    f"{self._string(item['configuration_id'])}:"
                    f"{self._string(item['arm'])}"
                )
                == key
            ]
            self._equal(
                self._integer(estimate["converged_count"]),
                sum(
                    self._boolean(item["effective_native_converged"])
                    for item in selected
                ),
                "category converged count",
            )
            self._equal(
                self._integer(estimate["right_censored_count"]),
                sum(
                    not self._boolean(item["effective_native_converged"])
                    for item in selected
                ),
                "category censored count",
            )
            adjusted = float(parameters[0]) + log_ratio + mean_start_effect
            self._close(
                self._real(estimate["adjusted_median_iterations"]),
                math.exp(adjusted),
                1.0e-9,
                "adjusted median",
            )
            for probability in self._records(
                estimate["predicted_convergence_probability"]
            ):
                iterations = self._integer(probability["iterations"])
                expected = float(ndtr((math.log(iterations) - adjusted) / scale))
                self._close(
                    self._real(probability["probability"]),
                    expected,
                    1.0e-12,
                    "predicted probability",
                )
        claim = self._string(regression["claim_boundary"])
        for phrase in (
            "does not alter native convergence",
            "establish causality",
            "predict DFT behavior",
        ):
            if phrase not in claim:
                raise AssertionError("regression claim boundary changed")
        return Periodic2DOptimizerRegressionCampaignVerificationResult(
            True,
            True,
            observed_count,
            converged_count,
            censored_count,
            len(parameters),
            hashlib.sha256(request.encoded_documents.regression_payload).hexdigest(),
        )

    def _objective(
        self,
        parameters: FloatArray,
        design: FloatArray,
        log_times: FloatArray,
        converged: BoolArray,
    ) -> tuple[float, FloatArray]:
        coefficients = parameters[:-1]
        log_scale = float(parameters[-1])
        scale = math.exp(log_scale)
        residual = (log_times - design @ coefficients) / scale
        event_loss = (
            log_scale + 0.5 * residual[converged] ** 2 + 0.5 * math.log(2.0 * math.pi)
        )
        censored_loss = -log_ndtr(-residual[~converged])
        gradient = self._observation_gradients(parameters, design, log_times, converged)
        return float(np.sum(event_loss) + np.sum(censored_loss)), np.asarray(
            np.sum(gradient, axis=0), dtype=np.float64
        )

    def _observation_gradients(
        self,
        parameters: FloatArray,
        design: FloatArray,
        log_times: FloatArray,
        converged: BoolArray,
    ) -> FloatArray:
        scale = math.exp(float(parameters[-1]))
        residual = (log_times - design @ parameters[:-1]) / scale
        rows = np.zeros((len(log_times), len(parameters)), dtype=np.float64)
        rows[converged, :-1] = -residual[converged, None] * design[converged] / scale
        rows[converged, -1] = 1.0 - residual[converged] ** 2
        censored = residual[~converged]
        mills = np.exp(
            -0.5 * censored**2 - 0.5 * math.log(2.0 * math.pi) - log_ndtr(-censored)
        )
        rows[~converged, :-1] = -mills[:, None] * design[~converged] / scale
        rows[~converged, -1] = -mills * censored
        return rows

    def _cluster_covariance(
        self,
        parameters: FloatArray,
        design: FloatArray,
        log_times: FloatArray,
        converged: BoolArray,
        cluster_ids: IntArray,
    ) -> tuple[FloatArray, float]:
        dimension = len(parameters)
        hessian = np.empty((dimension, dimension), dtype=np.float64)
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
        inverse = np.linalg.pinv(hessian, rcond=1.0e-12)
        scores = self._observation_gradients(parameters, design, log_times, converged)
        clusters = np.stack(
            [
                np.sum(scores[cluster_ids == cluster], axis=0)
                for cluster in np.unique(cluster_ids)
            ]
        )
        cluster_count = clusters.shape[0]
        correction = (cluster_count / (cluster_count - 1.0)) * (
            (len(log_times) - 1.0) / (len(log_times) - dimension)
        )
        meat = clusters.T @ clusters
        return np.asarray(
            correction * inverse @ meat @ inverse, dtype=np.float64
        ), float(np.linalg.cond(hessian))

    @staticmethod
    def _identity(payload: bytes, expected: str, label: str) -> None:
        if hashlib.sha256(payload).hexdigest() != expected:
            raise AssertionError(f"{label} identity mismatch")

    def _records(self, value: JsonValue) -> list[dict[str, JsonValue]]:
        return [self._mapping(item) for item in self._array(value)]

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected mapping")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected string")
        return value

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected integer")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected real")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError("real must be finite")
        return result

    @staticmethod
    def _boolean(value: JsonValue) -> bool:
        if not isinstance(value, bool):
            raise TypeError("expected boolean")
        return value

    @staticmethod
    def _equal(actual: int, expected: int, label: str) -> None:
        if actual != expected:
            raise AssertionError(f"{label}: {actual} != {expected}")

    @staticmethod
    def _close(actual: float, expected: float, tolerance: float, label: str) -> None:
        if abs(actual - expected) > tolerance:
            raise AssertionError(f"{label}: {actual} != {expected}")
