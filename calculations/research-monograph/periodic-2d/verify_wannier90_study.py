#!/usr/bin/env python3
"""Independently verify the bounded non-DFT Wannier90 study."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

from verify_wannier90_balanced import CorrectedWannier90Verifier, JsonValue


class Wannier90StudyVerifier:
    """Verify study identities, portable case evidence, and execution records."""

    __slots__ = ()

    def execute(self, result_path: Path, *, portable: bool) -> None:
        result = self._load(result_path)
        if self._integer(result["schema_version"]) != 1:
            raise ValueError("unsupported study result schema")
        if result["evidence_status"] != "calculated synthetic numerical verification":
            raise ValueError("unexpected evidence status")
        if result["all_declared_cases_completed"] is not True:
            raise AssertionError("not every declared case completed")
        repository_root = result_path.parents[3]
        provenance = self._mapping(result["provenance"])
        study_path = repository_root / self._string(provenance["study_input_path"])
        reference_path = repository_root / self._string(
            provenance["reference_result_path"]
        )
        base_extractor_path = result_path.with_name("extract_wannier90.py")
        study_extractor_path = result_path.with_name("extract_wannier90_study.py")
        self._identity(
            study_extractor_path,
            self._string(provenance["extractor_sha256"]),
            "study extractor",
        )
        self._identity(
            study_path, self._string(provenance["study_input_sha256"]), "study input"
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
        study = self._load(study_path)
        declared = {
            self._string(self._mapping(value)["case_id"]): self._mapping(value)
            for value in self._array(study["new_cases"])
        }
        records = [self._mapping(value) for value in self._array(result["cases"])]
        if set(declared) != {self._string(record["case_id"]) for record in records}:
            raise AssertionError("declared and retained case identities disagree")
        verifier = CorrectedWannier90Verifier()
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
            verifier.execute(
                case_path,
                portable=True,
                repository_root=repository_root,
                extractor_path=base_extractor_path,
            )
            self._verify_summary(record, self._load(case_path), case_id)
        if not portable:
            execution_path = Path(self._string(provenance["execution_result_path"]))
            self._identity(
                execution_path,
                self._string(provenance["execution_result_sha256"]),
                "execution result",
            )
            self._verify_execution(self._load(execution_path), execution_path.parent)

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

    def _verify_execution(
        self, execution: dict[str, JsonValue], execution_root: Path
    ) -> None:
        limits = self._mapping(execution["limits"])
        maximum_memory = self._integer(limits["maximum_resident_bytes_per_stage"])
        maximum_output = self._integer(limits["maximum_external_output_bytes_per_case"])
        for case_value in self._array(execution["cases"]):
            case = self._mapping(case_value)
            case_id = self._string(case["case_id"])
            if (
                case["completed"] is not True
                or case["resource_limit_exceeded"] is not False
            ):
                raise AssertionError(
                    f"{case_id} execution did not complete within limits"
                )
            if self._integer(case["external_output_bytes"]) > maximum_output:
                raise AssertionError(f"{case_id} output limit exceeded")
            for stage_value in self._array(case["stages"]):
                stage = self._mapping(stage_value)
                if self._integer(stage["exit_code"]) != 0:
                    raise AssertionError(f"{case_id} stage failed")
                memory = stage["maximum_resident_bytes"]
                if memory is not None and self._integer(memory) > maximum_memory:
                    raise AssertionError(f"{case_id} memory limit exceeded")
            case_root = execution_root / case_id
            for file_value in self._array(case["file_manifest"]):
                file_record = self._mapping(file_value)
                path = case_root / self._string(file_record["path"])
                self._identity(
                    path,
                    self._string(file_record["sha256"]),
                    f"{case_id}:{path.name}",
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


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--portable", action="store_true")
    arguments = parser.parse_args()
    Wannier90StudyVerifier().execute(
        cast(Path, arguments.result).resolve(), portable=arguments.portable
    )
    source = "portable_fixture" if arguments.portable else "native_external_run"
    print(f"periodic_2d_wannier90_study_verification=PASS source={source}")


if __name__ == "__main__":
    main()
