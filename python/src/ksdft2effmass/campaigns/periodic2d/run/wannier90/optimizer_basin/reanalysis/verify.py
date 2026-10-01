"""Repository-portable verification of optimizer-basin reanalysis."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np

from .....model.retained.optimizer_reanalysis import (
    Periodic2DOptimizerReanalysisCampaignModel,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerReanalysisCampaignVerificationRequest:
    """Request portable verification of retained reanalysis."""

    model: Periodic2DOptimizerReanalysisCampaignModel
    repository_root: Path


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerReanalysisCampaignVerificationResult:
    """Report reconstructed spread, basin, trace, and refinement evidence."""

    source_authentication_passed: bool
    structural_reconstruction_passed: bool
    endpoint_count: int
    refinement_case_count: int
    retained_result_sha256: str

    @property
    def passes(self) -> bool:
        """Return the aggregate bounded verification disposition."""
        return (
            self.source_authentication_passed and self.structural_reconstruction_passed
        )


class Periodic2DOptimizerReanalysisCampaignVerifier:
    """Reconstruct retained offline diagnostics without native execution files."""

    __slots__ = ()

    def execute(
        self, request: Periodic2DOptimizerReanalysisCampaignVerificationRequest
    ) -> Periodic2DOptimizerReanalysisCampaignVerificationResult:
        """Authenticate repository sources and reconstruct retained diagnostics."""
        source = self._mapping(
            cast(JsonValue, json.loads(request.model.source_result_payload))
        )
        result = self._mapping(
            cast(JsonValue, json.loads(request.model.result_payload))
        )
        self._equal(self._integer(result["schema_version"]), 1, "result schema")
        provenance = self._mapping(result["provenance"])
        self._identity(
            request.model.source_result_payload,
            self._string(provenance["source_result_sha256"]),
            "source result",
        )
        for path_key, digest_key in (
            ("reanalyzer_path", "reanalyzer_sha256"),
            ("base_extractor_path", "base_extractor_sha256"),
        ):
            path = request.repository_root / self._string(provenance[path_key])
            self._identity(
                path.read_bytes(), self._string(provenance[digest_key]), path_key
            )
        source_configs = {
            self._string(item["configuration_id"]): item
            for item in self._records(source["configurations"])
        }
        method = self._mapping(result["method"])
        configurations = self._records(result["configurations"])
        if set(source_configs) != {
            self._string(item["configuration_id"]) for item in configurations
        }:
            raise AssertionError("configuration identities disagree")
        observed_counts: dict[str, int] = {}
        endpoint_count = 0
        for configuration in configurations:
            identifier = self._string(configuration["configuration_id"])
            source_starts = {
                self._string(item["gauge_id"]): item
                for item in self._records(source_configs[identifier]["starts"])
            }
            starts = self._records(configuration["starts"])
            endpoint_count += len(starts)
            if set(source_starts) != {
                self._string(item["gauge_id"]) for item in starts
            }:
                raise AssertionError(f"{identifier}: endpoint identities disagree")
            for start in starts:
                gauge = self._string(start["gauge_id"])
                source_start = source_starts[gauge]
                if self._boolean(
                    start["convergence_criterion_satisfied"]
                ) != self._boolean(source_start["convergence_criterion_satisfied"]):
                    raise AssertionError(f"{identifier}/{gauge}: convergence changed")
                components = self._mapping(start["spread_components"])
                omega_i = self._real(components["omega_i_cell_squared"])
                omega_d = self._real(components["omega_d_cell_squared"])
                omega_od = self._real(components["omega_od_cell_squared"])
                self._close(
                    self._real(components["omega_tilde_cell_squared"]),
                    omega_d + omega_od,
                    2.0e-8,
                    "omega tilde",
                )
                self._close(
                    self._real(components["omega_total_cell_squared"]),
                    omega_i + omega_d + omega_od,
                    2.0e-8,
                    "omega total",
                )
                self._close(
                    self._real(source_start["native_total_spread_cell_squared"]),
                    self._real(components["omega_total_cell_squared"]),
                    2.0e-8,
                    "source total",
                )
                metrics = {
                    key: self._real(components[key])
                    for key in (
                        "terminal_spread_slope_per_iteration",
                        "terminal_detrended_spread_rms",
                        "terminal_median_absolute_delta_spread",
                        "terminal_median_rms_gradient",
                    )
                }
                classification = self._classification(
                    self._boolean(start["convergence_criterion_satisfied"]), metrics
                )
                if classification != self._string(
                    components["diagnostic_classification"]
                ):
                    raise AssertionError(
                        f"{identifier}/{gauge}: diagnostic class changed"
                    )
                observed_counts[classification] = (
                    observed_counts.get(classification, 0) + 1
                )
            converged = [
                item
                for item in starts
                if self._boolean(item["convergence_criterion_satisfied"])
            ]
            expected = self._clusters(
                converged,
                self._real(method["basin_spread_absolute_tolerance"]),
                self._real(method["basin_center_set_periodic_tolerance"]),
            )
            observed = [
                sorted(self._string(value) for value in self._array(item["gauge_ids"]))
                for item in self._records(
                    configuration["symmetry_aware_observed_basins"]
                )
            ]
            if sorted(expected) != sorted(observed):
                raise AssertionError(f"{identifier}: D4 basin membership changed")
        retained_counts = self._mapping(result["diagnostic_classification_counts"])
        if observed_counts != {
            key: self._integer(value) for key, value in retained_counts.items()
        }:
            raise AssertionError("diagnostic counts disagree")
        refinements = self._records(result["common_estimator_refinement"])
        for refinement in refinements:
            self._verify_refinement(refinement, request.repository_root)
        return Periodic2DOptimizerReanalysisCampaignVerificationResult(
            True,
            True,
            endpoint_count,
            len(refinements),
            hashlib.sha256(request.model.result_payload).hexdigest(),
        )

    def _classification(self, converged: bool, metrics: dict[str, float]) -> str:
        if converged:
            return "native_converged"
        if (
            metrics["terminal_median_absolute_delta_spread"] <= 1.0e-8
            and metrics["terminal_median_rms_gradient"] <= 1.0e-3
        ):
            return "near_stationary_without_window_convergence"
        if metrics["terminal_spread_slope_per_iteration"] < -1.0e-8:
            return "continuing_descent_at_iteration_limit"
        if metrics["terminal_detrended_spread_rms"] > 1.0e-5:
            return "oscillatory_or_stalled"
        return "stalled_or_nondescent"

    def _clusters(
        self,
        starts: list[dict[str, JsonValue]],
        spread_tolerance: float,
        center_tolerance: float,
    ) -> list[list[str]]:
        clusters: list[list[dict[str, JsonValue]]] = []
        for start in sorted(
            starts,
            key=lambda item: (self._omega_tilde(item), self._string(item["gauge_id"])),
        ):
            match = next(
                (
                    cluster
                    for cluster in clusters
                    if abs(self._omega_tilde(start) - self._omega_tilde(cluster[0]))
                    <= spread_tolerance
                    and self._center_distance(
                        start["native_centers_modulo_cell"],
                        cluster[0]["native_centers_modulo_cell"],
                        d4=True,
                    )
                    <= center_tolerance
                ),
                None,
            )
            if match is None:
                clusters.append([start])
            else:
                match.append(start)
        return [
            sorted(self._string(item["gauge_id"]) for item in cluster)
            for cluster in clusters
        ]

    def _omega_tilde(self, start: dict[str, JsonValue]) -> float:
        return self._real(
            self._mapping(start["spread_components"])["omega_tilde_cell_squared"]
        )

    def _center_distance(
        self, first: JsonValue, second: JsonValue, *, d4: bool
    ) -> float:
        left = [self._reals(value) for value in self._array(first)]
        right = [self._reals(value) for value in self._array(second)]
        return min(
            self._ordinary_distance(self._transform(left, operation), right)
            for operation in (range(8) if d4 else range(1))
        )

    @staticmethod
    def _transform(
        centers: list[tuple[float, ...]], operation: int
    ) -> list[tuple[float, float]]:
        transformed: list[tuple[float, float]] = []
        for x, y in centers:
            a, b = (
                (x, y),
                (-y, x),
                (-x, -y),
                (y, -x),
                (x, -y),
                (-x, y),
                (y, x),
                (-y, -x),
            )[operation]
            transformed.append((a % 1.0, b % 1.0))
        return transformed

    @staticmethod
    def _ordinary_distance(
        first: Sequence[tuple[float, ...]], second: Sequence[tuple[float, ...]]
    ) -> float:
        return min(
            max(
                math.sqrt(
                    sum(
                        min(abs(a - b), 1.0 - abs(a - b)) ** 2
                        for a, b in zip(first[index], second[target], strict=True)
                    )
                )
                for index, target in enumerate(permutation)
            )
            for permutation in itertools.permutations(range(len(second)))
        )

    def _verify_refinement(
        self, refinement: dict[str, JsonValue], repository_root: Path
    ) -> None:
        sizes = self._records(refinement["sizes"])
        if tuple(self._integer(item["fft_size"]) for item in sizes) != (256, 512, 1024):
            raise AssertionError("unexpected FFT refinement sizes")
        for item in sizes:
            retained_path = Path(self._string(item["input_path"]))
            path = (
                repository_root
                / "calculations"
                / "research-monograph"
                / "periodic-2d-optimizer-basin"
                / "estimator-inputs"
                / retained_path.name
            )
            self._identity(
                path.read_bytes(),
                self._string(item["input_sha256"]),
                retained_path.name,
            )
        lower, upper = sizes[1], sizes[2]
        observed = self._mapping(refinement["refinement_512_to_1024"])
        lower_spread = self._real(lower["common_total_spread_cell_squared"])
        upper_spread = self._real(upper["common_total_spread_cell_squared"])
        relative = abs(lower_spread - upper_spread) / max(abs(upper_spread), 1.0e-15)
        self._close(
            relative,
            self._real(observed["relative_total_spread_difference"]),
            1.0e-15,
            "refinement spread",
        )
        distance = self._center_distance(
            lower["common_centers_modulo_cell"],
            upper["common_centers_modulo_cell"],
            d4=False,
        )
        self._close(
            distance,
            self._real(observed["center_set_periodic_distance"]),
            1.0e-15,
            "refinement centers",
        )

    @staticmethod
    def _identity(payload: bytes, expected: str, label: str) -> None:
        if hashlib.sha256(payload).hexdigest() != expected:
            raise AssertionError(f"{label} identity mismatch")

    def _records(self, value: JsonValue) -> list[dict[str, JsonValue]]:
        return [self._mapping(item) for item in self._array(value)]

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        return tuple(self._real(item) for item in self._array(value))

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
