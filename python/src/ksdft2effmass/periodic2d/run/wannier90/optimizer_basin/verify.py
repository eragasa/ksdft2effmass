"""Repository-portable verification of the optimizer-basin study."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np

from .encoded_documents import Periodic2DOptimizerBasinEncodedDocuments

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerBasinCampaignVerificationRequest:
    """Request portable verification of one retained optimizer study."""

    encoded_documents: Periodic2DOptimizerBasinEncodedDocuments
    repository_root: Path

    def __post_init__(self) -> None:
        """Validate exact document ownership and an absolute repository root."""
        if type(self.encoded_documents) is not Periodic2DOptimizerBasinEncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic2DOptimizerBasinEncodedDocuments"
            )
        if not isinstance(self.repository_root, Path):
            raise TypeError("repository_root must be pathlib.Path")
        if not self.repository_root.is_absolute():
            raise ValueError("repository_root must be absolute")


@dataclass(frozen=True, slots=True)
class Periodic2DOptimizerBasinCampaignVerificationResult:
    """Report authenticated retained-outcome reconstruction."""

    source_authentication_passed: bool
    structural_reconstruction_passed: bool
    configuration_count: int
    converged_count: int
    nonconverged_count: int
    retained_result_sha256: str

    @property
    def passes(self) -> bool:
        """Return the aggregate bounded verification disposition."""
        return (
            self.source_authentication_passed and self.structural_reconstruction_passed
        )


class Periodic2DOptimizerBasinCampaignVerifier:
    """Verify all endpoints, basin groups, counts, and frozen negative gates."""

    __slots__ = ()

    def execute(
        self, request: Periodic2DOptimizerBasinCampaignVerificationRequest
    ) -> Periodic2DOptimizerBasinCampaignVerificationResult:
        """Authenticate repository sources and reconstruct retained arithmetic."""
        study = self._mapping(
            cast(JsonValue, json.loads(request.encoded_documents.input_payload))
        )
        result = self._mapping(
            cast(JsonValue, json.loads(request.encoded_documents.result_payload))
        )
        self._equal(self._integer(study["schema_version"]), 1, "study schema")
        self._equal(self._integer(result["schema_version"]), 1, "result schema")
        provenance = self._mapping(result["provenance"])
        self._content_identity(
            request.encoded_documents.input_payload,
            self._string(provenance["study_input_sha256"]),
            "study input",
        )
        for path_key, digest_key in (
            ("extractor_path", "extractor_sha256"),
            ("base_extractor_path", "base_extractor_sha256"),
        ):
            path = request.repository_root / self._string(provenance[path_key])
            self._content_identity(
                path.read_bytes(), self._string(provenance[digest_key]), path_key
            )
        declared = {
            self._string(item["configuration_id"]): item
            for item in self._records(study["configurations"])
        }
        gauge_ids = tuple(
            self._string(item["gauge_id"])
            for item in self._records(study["initial_gauges"])
        )
        if len(gauge_ids) != 8 or len(set(gauge_ids)) != 8:
            raise AssertionError("expected eight unique deterministic gauges")
        configurations = self._records(result["configurations"])
        if len(configurations) != 9 or set(declared) != {
            self._string(item["configuration_id"]) for item in configurations
        }:
            raise AssertionError("configuration identities disagree")
        converged_total = 0
        nonconverged_total = 0
        by_id: dict[str, dict[str, JsonValue]] = {}
        for configuration in configurations:
            identifier = self._string(configuration["configuration_id"])
            by_id[identifier] = configuration
            expected = declared[identifier]
            for key in ("plane_wave_cutoff", "reciprocal_mesh_size"):
                self._equal(
                    self._integer(configuration[key]),
                    self._integer(expected[key]),
                    f"{identifier}:{key}",
                )
            self._close(
                self._real(configuration["transverse_lattice_length"]),
                self._real(expected["transverse_lattice_length"]),
                0.0,
                f"{identifier}:embedding",
            )
            starts = self._records(configuration["starts"])
            if {self._string(item["gauge_id"]) for item in starts} != set(gauge_ids):
                raise AssertionError(f"{identifier}: gauge identities disagree")
            if not all(self._boolean(item["completed"]) for item in starts):
                raise AssertionError(f"{identifier}: incomplete endpoint")
            converged = [
                item
                for item in starts
                if self._boolean(item["convergence_criterion_satisfied"])
            ]
            nonconverged = [
                item
                for item in starts
                if not self._boolean(item["convergence_criterion_satisfied"])
            ]
            converged_total += len(converged)
            nonconverged_total += len(nonconverged)
            self._equal(
                self._integer(configuration["converged_start_count"]),
                len(converged),
                f"{identifier}:converged count",
            )
            retained_nonconverged = tuple(
                self._string(value)
                for value in self._array(configuration["nonconverged_gauge_ids"])
            )
            if set(retained_nonconverged) != {
                self._string(item["gauge_id"]) for item in nonconverged
            }:
                raise AssertionError(f"{identifier}: nonconverged identities disagree")
            self._verify_basins(configuration, converged, identifier)
            best = min(
                converged,
                key=lambda item: self._real(item["native_total_spread_cell_squared"]),
            )
            if self._string(best["gauge_id"]) != self._string(
                self._mapping(configuration["best_observed_converged"])["gauge_id"]
            ):
                raise AssertionError(f"{identifier}: best observed endpoint disagrees")
        summary = self._mapping(result["execution_summary"])
        self._equal(
            self._integer(summary["configuration_count"]),
            len(configurations),
            "configuration count",
        )
        self._equal(
            self._integer(summary["localization_count"]),
            converged_total + nonconverged_total,
            "localization count",
        )
        self._equal(
            self._integer(summary["converged_localization_count"]),
            converged_total,
            "converged count",
        )
        self._equal(
            self._integer(summary["nonconverged_localization_count"]),
            nonconverged_total,
            "nonconverged count",
        )
        self._verify_negative_disposition(result, by_id, study)
        return Periodic2DOptimizerBasinCampaignVerificationResult(
            True,
            True,
            len(configurations),
            converged_total,
            nonconverged_total,
            hashlib.sha256(request.encoded_documents.result_payload).hexdigest(),
        )

    def _verify_basins(
        self,
        configuration: dict[str, JsonValue],
        converged: list[dict[str, JsonValue]],
        identifier: str,
    ) -> None:
        basins = self._records(configuration["observed_converged_basins"])
        members: list[str] = []
        for basin in basins:
            gauge_ids = [
                self._string(value) for value in self._array(basin["gauge_ids"])
            ]
            self._equal(
                self._integer(basin["occupancy"]),
                len(gauge_ids),
                f"{identifier}:basin occupancy",
            )
            if self._string(basin["representative_gauge_id"]) not in gauge_ids:
                raise AssertionError(f"{identifier}: basin representative absent")
            members.extend(gauge_ids)
        expected = sorted(self._string(item["gauge_id"]) for item in converged)
        if sorted(members) != expected or len(members) != len(set(members)):
            raise AssertionError(f"{identifier}: basin partition disagrees")
        self._equal(
            self._integer(configuration["observed_converged_basin_count"]),
            len(basins),
            f"{identifier}:basin count",
        )

    def _verify_negative_disposition(
        self,
        result: dict[str, JsonValue],
        by_id: dict[str, dict[str, JsonValue]],
        study: dict[str, JsonValue],
    ) -> None:
        assessment = self._mapping(result["convergence_assessment"])
        if self._boolean(assessment["supports_declared_convergence"]):
            raise AssertionError("retained negative convergence disposition changed")
        method = self._mapping(study["convergence_method"])
        required = self._integer(method["minimum_repeated_best_basin_occupancy"])
        for key in ("mesh_finest_pair", "cutoff_finest_pair"):
            pair = self._mapping(assessment[key])
            lower = by_id[self._string(pair["lower_configuration_id"])]
            upper = by_id[self._string(pair["upper_configuration_id"])]
            occupancy = min(
                self._best_basin_occupancy(lower), self._best_basin_occupancy(upper)
            )
            self._equal(
                self._integer(pair["minimum_endpoint_best_basin_occupancy"]),
                occupancy,
                f"{key}:occupancy",
            )
            if self._boolean(pair["occupancy_pass"]) != (occupancy >= required):
                raise AssertionError(f"{key}: occupancy disposition disagrees")
            if self._boolean(pair["supporting"]):
                raise AssertionError(f"{key}: unsupported convergence promotion")

    def _best_basin_occupancy(self, configuration: dict[str, JsonValue]) -> int:
        best_id = self._string(
            self._mapping(configuration["best_observed_converged"])["gauge_id"]
        )
        for basin in self._records(configuration["observed_converged_basins"]):
            ids = tuple(
                self._string(value) for value in self._array(basin["gauge_ids"])
            )
            if best_id in ids:
                return self._integer(basin["occupancy"])
        raise AssertionError("best endpoint has no basin")

    @staticmethod
    def _content_identity(payload: bytes, expected: str, label: str) -> None:
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected:
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
            raise ValueError("real values must be finite")
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
