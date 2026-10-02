"""Repository-portable verification of the standalone optimizer study."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np

from .....model.retained.optimizer_standalone import (
    Periodic2DOptimizerStandaloneCampaignModel,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerStandaloneCampaignVerificationRequest:
    """Request portable verification of the standalone study."""

    model: Periodic2DOptimizerStandaloneCampaignModel
    repository_root: Path


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerStandaloneCampaignVerificationResult:
    """Report reconstructed initial, continuation, and basin evidence."""

    source_authentication_passed: bool
    structural_reconstruction_passed: bool
    endpoint_count: int
    continuation_count: int
    effective_converged_count: int
    final_nonconverged_count: int
    retained_result_sha256: str

    @property
    def passes(self) -> bool:
        """Return the aggregate bounded verification disposition."""
        return (
            self.source_authentication_passed and self.structural_reconstruction_passed
        )


class Periodic2DOptimizerStandaloneCampaignVerifier:
    """Reconstruct all retained endpoints without opening native run paths."""

    __slots__ = ()

    def execute(
        self, request: Periodic2DOptimizerStandaloneCampaignVerificationRequest
    ) -> Periodic2DOptimizerStandaloneCampaignVerificationResult:
        """Authenticate repository sources and reconstruct retained outcomes."""
        proposal = self._mapping(
            cast(JsonValue, json.loads(request.model.proposal_payload))
        )
        gauges = self._mapping(
            cast(JsonValue, json.loads(request.model.initial_gauges_payload))
        )
        result = self._mapping(
            cast(JsonValue, json.loads(request.model.result_payload))
        )
        self._equal(self._integer(proposal["schema_version"]), 1, "proposal schema")
        self._equal(self._integer(gauges["schema_version"]), 1, "gauge schema")
        self._equal(self._integer(result["schema_version"]), 1, "result schema")
        provenance = self._mapping(result["provenance"])
        self._identity(
            request.model.proposal_payload,
            self._string(provenance["proposal_sha256"]),
            "proposal",
        )
        self._identity(
            request.model.proposal_payload,
            self._string(gauges["proposal_sha256"]),
            "gauge proposal",
        )
        extractor = (
            request.repository_root
            / "calculations"
            / "research-monograph"
            / "periodic-2d-optimizer-basin"
            / Path(self._string(provenance["extractor_path"])).name
        )
        self._identity(
            extractor.read_bytes(),
            self._string(provenance["extractor_sha256"]),
            "extractor",
        )
        starts = self._records(gauges["starts"])
        start_ids = tuple(self._string(item["start_id"]) for item in starts)
        self._equal(self._integer(gauges["start_count"]), len(starts), "gauge count")
        if len(starts) != 16 or len(set(start_ids)) != 16:
            raise AssertionError("expected 16 unique starts")
        endpoints = self._records(result["endpoints"])
        keys = {
            (
                self._string(item["configuration_id"]),
                self._string(item["arm"]),
                self._string(item["start_id"]),
            )
            for item in endpoints
        }
        if len(endpoints) != 256 or len(keys) != 256:
            raise AssertionError("expected 256 unique endpoints")
        continuation_count = 0
        effective_converged_count = 0
        diagnostic_counts: dict[str, int] = {}
        for endpoint in endpoints:
            if not self._boolean(endpoint["initial_process_completed"]):
                raise AssertionError("incomplete initial process")
            start_id = self._string(endpoint["start_id"])
            if start_id not in start_ids:
                raise AssertionError("undeclared start identity")
            self._equal(
                self._integer(endpoint["start_index"]),
                start_ids.index(start_id),
                "start index",
            )
            initial = self._mapping(endpoint["initial_native_endpoint"])
            self._verify_native_endpoint(initial)
            initial_converged = self._boolean(endpoint["initial_native_converged"])
            continuation_applied = self._boolean(endpoint["continuation_applied"])
            if continuation_applied == initial_converged:
                raise AssertionError("continuation selection disagrees")
            effective = self._mapping(endpoint["effective_native_endpoint"])
            self._verify_native_endpoint(effective)
            if continuation_applied:
                continuation_count += 1
                continuation = self._mapping(endpoint["continuation_native_endpoint"])
                self._verify_native_endpoint(continuation)
                if continuation != effective:
                    raise AssertionError("effective endpoint is not continuation")
                if self._boolean(
                    endpoint["continuation_native_converged"]
                ) != self._boolean(endpoint["effective_native_converged"]):
                    raise AssertionError("continuation status changed")
                self._equal(
                    self._integer(endpoint["effective_total_iterations"]),
                    self._integer(initial["iterations"])
                    + self._integer(continuation["iterations"]),
                    "continued iterations",
                )
            else:
                if (
                    endpoint["continuation_native_endpoint"] is not None
                    or endpoint["continuation_native_converged"] is not None
                ):
                    raise AssertionError("unexpected continuation record")
                if initial != effective:
                    raise AssertionError("effective endpoint is not initial")
                self._equal(
                    self._integer(endpoint["effective_total_iterations"]),
                    self._integer(initial["iterations"]),
                    "initial iterations",
                )
            effective_converged = self._boolean(endpoint["effective_native_converged"])
            effective_converged_count += int(effective_converged)
            classification = self._classification(effective_converged, effective)
            if classification != self._string(effective["diagnostic_classification"]):
                raise AssertionError("diagnostic classification disagrees")
            if not effective_converged:
                diagnostic_counts[classification] = (
                    diagnostic_counts.get(classification, 0) + 1
                )
        self._verify_summary(
            result,
            endpoints,
            continuation_count,
            effective_converged_count,
            diagnostic_counts,
        )
        self._verify_groups(result, endpoints, proposal, start_ids)
        contract = self._mapping(result["analysis_contract"])
        status = self._string(contract["basin_tolerance_control_status"])
        if "lacks a retained record" not in status:
            raise AssertionError("protocol deviation was not preserved")
        assessment = self._mapping(result["convergence_assessment"])
        if self._boolean(assessment["supports_declared_convergence"]):
            raise AssertionError("negative disposition changed")
        if not self._boolean(
            assessment["not_global_optimizer_convergence"]
        ) or not self._boolean(assessment["not_general_wannier_convergence"]):
            raise AssertionError("claim boundary changed")
        final_nonconverged = len(endpoints) - effective_converged_count
        return Periodic2DOptimizerStandaloneCampaignVerificationResult(
            True,
            True,
            len(endpoints),
            continuation_count,
            effective_converged_count,
            final_nonconverged,
            hashlib.sha256(request.model.result_payload).hexdigest(),
        )

    def _verify_native_endpoint(self, endpoint: dict[str, JsonValue]) -> None:
        omega_d = self._real(endpoint["omega_d_cell_squared"])
        omega_od = self._real(endpoint["omega_od_cell_squared"])
        omega_i = self._real(endpoint["omega_i_cell_squared"])
        self._close(
            self._real(endpoint["omega_tilde_cell_squared"]),
            omega_d + omega_od,
            2.0e-8,
            "omega tilde",
        )
        self._close(
            self._real(endpoint["omega_total_cell_squared"]),
            omega_i + omega_d + omega_od,
            2.0e-8,
            "omega total",
        )

    def _classification(self, converged: bool, endpoint: dict[str, JsonValue]) -> str:
        if converged:
            return "native_converged"
        delta = self._real(endpoint["terminal_median_absolute_delta_spread"])
        gradient = self._real(endpoint["terminal_median_rms_gradient"])
        slope = self._real(endpoint["terminal_spread_slope_per_iteration"])
        rms = self._real(endpoint["terminal_detrended_spread_rms"])
        if delta <= 1.0e-8 and gradient <= 1.0e-3:
            return "near_stationary_without_window_convergence"
        if slope < -1.0e-8:
            return "continuing_descent_at_iteration_limit"
        if rms > 1.0e-5:
            return "oscillatory_or_stalled"
        return "stalled_or_nondescent"

    def _verify_summary(
        self,
        result: dict[str, JsonValue],
        endpoints: list[dict[str, JsonValue]],
        continuation_count: int,
        effective_converged: int,
        diagnostics: dict[str, int],
    ) -> None:
        summary = self._mapping(result["execution_summary"])
        expected = {
            "initial_localization_count": len(endpoints),
            "initial_process_completion_count": sum(
                self._boolean(item["initial_process_completed"]) for item in endpoints
            ),
            "initial_native_converged_count": sum(
                self._boolean(item["initial_native_converged"]) for item in endpoints
            ),
            "continuation_count": continuation_count,
            "continuation_native_converged_count": sum(
                item["continuation_native_converged"] is True for item in endpoints
            ),
            "effective_native_converged_count": effective_converged,
            "effective_native_nonconverged_count": len(endpoints) - effective_converged,
        }
        for key, value in expected.items():
            self._equal(self._integer(summary[key]), value, key)
        represented = self._mapping(
            summary["effective_nonconvergence_diagnostic_counts"]
        )
        if {
            key: self._integer(value) for key, value in represented.items()
        } != diagnostics:
            raise AssertionError("nonconvergence diagnostic counts disagree")

    def _verify_groups(
        self,
        result: dict[str, JsonValue],
        endpoints: list[dict[str, JsonValue]],
        proposal: dict[str, JsonValue],
        start_ids: tuple[str, ...],
    ) -> None:
        method = self._mapping(proposal["basin_method"])
        center_tolerance = self._real(method["center_set_periodic_tolerance_cell"])
        density_tolerance = self._real(method["maximum_matched_density_l2_mismatch"])
        required = self._integer(method["best_basin_minimum_occupancy"])
        groups = self._records(result["groups"])
        self._equal(len(groups), 16, "group count")
        for group in groups:
            selected = [
                item
                for item in endpoints
                if item["configuration_id"] == group["configuration_id"]
                and item["arm"] == group["arm"]
            ]
            self._equal(len(selected), len(start_ids), "group endpoint count")
            if {self._string(item["start_id"]) for item in selected} != set(start_ids):
                raise AssertionError("group start identities disagree")
            converged = [
                item
                for item in selected
                if self._boolean(item["effective_native_converged"])
            ]
            self._equal(
                self._integer(group["initial_native_converged_count"]),
                sum(
                    self._boolean(item["initial_native_converged"]) for item in selected
                ),
                "group initial count",
            )
            self._equal(
                self._integer(group["effective_native_converged_count"]),
                len(converged),
                "group effective count",
            )
            self._close(
                self._real(group["effective_native_converged_fraction"]),
                len(converged) / len(selected),
                0.0,
                "group fraction",
            )
            expected_nonconverged = {
                self._string(item["start_id"])
                for item in selected
                if not self._boolean(item["effective_native_converged"])
            }
            if {
                self._string(value)
                for value in self._array(group["effective_nonconverged_start_ids"])
            } != expected_nonconverged:
                raise AssertionError("group nonconverged identities disagree")
            best = min(
                converged,
                key=lambda item: (
                    self._real(
                        self._mapping(item["effective_native_endpoint"])[
                            "omega_tilde_cell_squared"
                        ]
                    ),
                    self._string(item["start_id"]),
                ),
            )
            best_id = self._string(
                self._mapping(group["best_observed_converged"])["start_id"]
            )
            if best_id != self._string(best["start_id"]):
                raise AssertionError("group best endpoint disagrees")
            basins = self._records(group["observed_density_d4_basins"])
            self._equal(
                self._integer(group["observed_density_d4_basin_count"]),
                len(basins),
                "basin count",
            )
            members = [
                self._string(value)
                for basin in basins
                for value in self._array(basin["start_ids"])
            ]
            if sorted(members) != sorted(
                self._string(item["start_id"]) for item in converged
            ) or len(members) != len(set(members)):
                raise AssertionError("basins do not partition converged endpoints")
            for basin in basins:
                self._equal(
                    self._integer(basin["occupancy"]),
                    len(self._array(basin["start_ids"])),
                    "basin occupancy",
                )
            best_basin = next(
                basin
                for basin in basins
                if best_id
                in {self._string(value) for value in self._array(basin["start_ids"])}
            )
            expected_best_pass = self._integer(
                best_basin["occupancy"]
            ) >= required and self._boolean(best_basin["appears_in_both_start_blocks"])
            if self._boolean(group["best_basin_criterion_pass"]) != expected_best_pass:
                raise AssertionError("best-basin gate disagrees")
            self._verify_sensitivity(
                group, basins, center_tolerance, density_tolerance, best_id
            )
            self._verify_controls(group, center_tolerance, density_tolerance)

    def _verify_sensitivity(
        self,
        group: dict[str, JsonValue],
        basins: list[dict[str, JsonValue]],
        center_tolerance: float,
        density_tolerance: float,
        best_id: str,
    ) -> None:
        candidates: list[tuple[bool, float, float, str]] = []
        for basin in basins:
            for value in self._array(basin["rejected_equivalence_candidates"]):
                rejected = self._mapping(value)
                center = self._nonnegative_extended_real(
                    rejected["center_set_periodic_distance"]
                )
                density = self._nonnegative_extended_real(
                    rejected["maximum_density_l2_mismatch"]
                )
                if center <= center_tolerance and density <= density_tolerance:
                    raise AssertionError("passing pair was rejected")
                candidates.append(
                    (
                        self._string(basin["representative_start_id"]) == best_id,
                        center,
                        density,
                        self._string(rejected["representative_start_id"]),
                    )
                )
        for record in self._records(group["density_tolerance_sensitivity"]):
            tolerance = self._real(record["density_l2_tolerance"])
            matches = [
                item
                for item in candidates
                if item[1] <= center_tolerance and item[2] <= tolerance
            ]
            self._equal(
                self._integer(record["direct_matching_pair_count"]),
                len(matches),
                "sensitivity pair count",
            )
            expected_ids = {item[3] for item in matches if item[0]}
            if {
                self._string(value)
                for value in self._array(record["best_endpoint_direct_match_start_ids"])
            } != expected_ids:
                raise AssertionError("best sensitivity identities disagree")
            self._equal(
                self._integer(record["best_endpoint_direct_occupancy"]),
                1 + len(expected_ids),
                "best sensitivity occupancy",
            )

    def _verify_controls(
        self,
        group: dict[str, JsonValue],
        center_tolerance: float,
        density_tolerance: float,
    ) -> None:
        controls = self._mapping(group["basin_post_hoc_numerical_controls"])
        records = self._records(controls["records"])
        self._equal(
            self._integer(controls["control_count"]), len(records), "control count"
        )
        maximum_center = max(
            self._real(item["center_set_periodic_distance"]) for item in records
        )
        maximum_density = max(
            self._real(item["maximum_density_l2_mismatch"]) for item in records
        )
        self._close(
            self._real(controls["maximum_center_set_periodic_distance_cell"]),
            maximum_center,
            0.0,
            "control center maximum",
        )
        self._close(
            self._real(controls["maximum_density_l2_mismatch"]),
            maximum_density,
            0.0,
            "control density maximum",
        )
        if self._boolean(controls["passes_frozen_center_tolerance"]) != (
            maximum_center <= center_tolerance
        ):
            raise AssertionError("control center gate disagrees")
        if self._boolean(controls["passes_frozen_density_tolerance"]) != (
            maximum_density <= density_tolerance
        ):
            raise AssertionError("control density gate disagrees")

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
    def _nonnegative_extended_real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a nonnegative extended real")
        result = float(value)
        if np.isnan(result) or result < 0.0:
            raise ValueError("extended real must be nonnegative and not NaN")
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
