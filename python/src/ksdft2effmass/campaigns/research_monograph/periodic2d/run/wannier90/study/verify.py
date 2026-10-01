#!/usr/bin/env python3
"""Independently verify the bounded non-DFT Wannier90 study."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from ....model.retained.wannier90_study import Periodic2DWannier90StudyCampaignModel
from ..balanced.verify import JsonValue, Periodic2DWannier90BalancedReconstructor


class Periodic2DWannier90StudyReconstructor:
    """Verify study identities and portable case evidence."""

    __slots__ = ()

    def execute_portable(
        self,
        input_payload: bytes,
        result_payload: bytes,
        *,
        repository_root: Path,
        study_extractor_path: Path,
        base_extractor_path: Path,
    ) -> None:
        """Authenticate and reconstruct every repository-portable study case."""
        result = self._loads(result_payload)
        if self._integer(result["schema_version"]) != 1:
            raise ValueError("unsupported study result schema")
        if result["evidence_status"] != "calculated synthetic numerical verification":
            raise ValueError("unexpected evidence status")
        if result["all_declared_cases_completed"] is not True:
            raise AssertionError("not every declared case completed")
        provenance = self._mapping(result["provenance"])
        reference_path = repository_root / self._string(
            provenance["reference_result_path"]
        )
        self._identity(
            study_extractor_path,
            self._string(provenance["extractor_sha256"]),
            "study extractor",
        )
        self._content_identity(
            input_payload,
            self._string(provenance["study_input_sha256"]),
            "study input",
        )
        self._identity(
            reference_path,
            self._string(provenance["reference_result_sha256"]),
            "reference result",
        )
        self._identity(
            base_extractor_path,
            self._string(provenance["base_extractor_sha256"]),
            "base extractor",
        )
        study = self._loads(input_payload)
        declared = {
            self._string(self._mapping(value)["case_id"]): self._mapping(value)
            for value in self._array(study["new_cases"])
        }
        records = [self._mapping(value) for value in self._array(result["cases"])]
        if set(declared) != {self._string(record["case_id"]) for record in records}:
            raise AssertionError("declared and retained case identities disagree")
        verifier = Periodic2DWannier90BalancedReconstructor()
        for record in records:
            case_id = self._string(record["case_id"])
            expected = declared[case_id]
            self._equal(
                self._integer(record["plane_wave_cutoff"]),
                self._integer(expected["plane_wave_cutoff"]),
                f"{case_id} cutoff",
            )
            self._equal(
                self._integer(record["reciprocal_mesh_size"]),
                self._integer(expected["reciprocal_mesh_size"]),
                f"{case_id} mesh",
            )
            self._close(
                self._real(record["transverse_lattice_length"]),
                self._real(expected["transverse_lattice_length"]),
                0.0,
                f"{case_id} transverse length",
            )
            case_path = repository_root / self._string(record["portable_result_path"])
            self._identity(
                case_path,
                self._string(record["portable_result_sha256"]),
                f"{case_id} portable result",
            )
            verifier.execute_portable(
                case_path.read_bytes(),
                repository_root=repository_root,
                extractor_path=base_extractor_path,
            )
            self._verify_summary(record, self._load(case_path), case_id)

    def _verify_summary(
        self,
        record: dict[str, JsonValue],
        case_result: dict[str, JsonValue],
        case_id: str,
    ) -> None:
        summary = self._mapping(record["summary"])
        execution = self._mapping(case_result["execution"])
        localization = self._mapping(case_result["localization"])
        native = self._mapping(localization["native_wannier90"])
        represented = self._mapping(case_result["represented_comparison"])
        self._equal(
            self._integer(summary["iterations"]),
            self._integer(execution["iterations"]),
            f"{case_id} iterations",
        )
        self._close(
            self._real(summary["native_total_spread_cell_squared"]),
            self._real(native["total_spread_cell_squared"]),
            0.0,
            f"{case_id} native spread",
        )
        common_total = sum(
            self._real(self._mapping(value)["spread_cell_squared"])
            for value in self._array(localization["common_finite_supercell_estimator"])
        )
        self._close(
            self._real(summary["common_wannier90_total_spread_cell_squared"]),
            common_total,
            1.0e-13,
            f"{case_id} common spread",
        )
        shell_50 = next(
            self._mapping(value)
            for value in self._array(represented["shell_study"])
            if self._integer(self._mapping(value)["maximum_squared_radius"]) == 50
        )
        self._close(
            self._real(summary["radius_50_hopping_tail_energy_units"]),
            self._real(shell_50["omitted_block_frobenius_l2_norm"]),
            0.0,
            f"{case_id} radius-50 tail",
        )

    def _loads(self, payload: bytes) -> dict[str, JsonValue]:
        return self._mapping(cast(JsonValue, json.loads(payload.decode("utf-8"))))

    def _content_identity(self, payload: bytes, expected: str, label: str) -> None:
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={expected}"
            )

    def _load(self, path: Path) -> dict[str, JsonValue]:
        return self._mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        )

    def _identity(self, path: Path, expected: str, label: str) -> None:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={expected}"
            )

    def _mapping(self, value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected a mapping")
        return value

    def _array(self, value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
        return value

    def _string(self, value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected a string")
        return value

    def _integer(self, value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected an integer")
        return value

    def _real(self, value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected a real number")
        return float(value)

    def _equal(self, actual: int, expected: int, label: str) -> None:
        if actual != expected:
            raise AssertionError(f"{label}: actual={actual}, expected={expected}")

    def _close(
        self, actual: float, expected: float, tolerance: float, label: str
    ) -> None:
        if abs(actual - expected) > tolerance:
            raise AssertionError(
                f"{label}: actual={actual:.16e}, expected={expected:.16e}"
            )


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90StudyCampaignVerificationRequest:
    """Request repository-portable study verification."""

    model: Periodic2DWannier90StudyCampaignModel
    repository_root: Path


@dataclass(frozen=True, slots=True)
class Periodic2DWannier90StudyCampaignVerificationResult:
    """Report authenticated portable study reconstruction."""

    source_authentication_passed: bool
    numerical_reconstruction_passed: bool
    case_count: int
    retained_result_sha256: str

    @property
    def passes(self) -> bool:
        """Return the aggregate bounded verification disposition."""
        return (
            self.source_authentication_passed and self.numerical_reconstruction_passed
        )


class Periodic2DWannier90StudyCampaignVerifier:
    """Verify every retained study fixture without native external files."""

    __slots__ = ()

    def execute(
        self, request: Periodic2DWannier90StudyCampaignVerificationRequest
    ) -> Periodic2DWannier90StudyCampaignVerificationResult:
        """Authenticate sources and reconstruct all six portable cases."""
        calculation_root = (
            request.repository_root / "calculations/research-monograph/periodic-2d"
        )
        Periodic2DWannier90StudyReconstructor().execute_portable(
            request.model.input_payload,
            request.model.result_payload,
            repository_root=request.repository_root,
            study_extractor_path=calculation_root / "extract_wannier90_study.py",
            base_extractor_path=calculation_root / "extract_wannier90.py",
        )
        return Periodic2DWannier90StudyCampaignVerificationResult(
            source_authentication_passed=True,
            numerical_reconstruction_passed=True,
            case_count=6,
            retained_result_sha256=hashlib.sha256(
                request.model.result_payload
            ).hexdigest(),
        )
