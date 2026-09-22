#!/usr/bin/env python3
"""Extract portable evidence for the authorized non-DFT Wannier90 study."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from extract_wannier90 import CorrectedWannier90Extractor, JsonValue


class Wannier90StudyExtractor:
    """Extract each native case and summarize one-axis sensitivity."""

    __slots__ = ()

    def execute(
        self,
        study_path: Path,
        execution_path: Path,
        reference_result_path: Path,
        base_extractor_path: Path,
        output_directory: Path,
        output_path: Path,
    ) -> dict[str, JsonValue]:
        study = self._load(study_path)
        execution = self._load(execution_path)
        reference = self._load(reference_result_path)
        execution_cases = {
            self._string(self._mapping(value)["case_id"]): self._mapping(value)
            for value in self._array(execution["cases"])
        }
        declared_cases = [
            self._mapping(value) for value in self._array(study["new_cases"])
        ]
        if set(execution_cases) != {
            self._string(case["case_id"]) for case in declared_cases
        }:
            raise AssertionError("executed and declared case identities disagree")
        output_directory.mkdir(parents=True, exist_ok=True)
        extractor = CorrectedWannier90Extractor()
        case_records: list[JsonValue] = []
        for case in declared_cases:
            case_id = self._string(case["case_id"])
            execution_case = execution_cases[case_id]
            if execution_case["completed"] is not True:
                case_records.append(
                    {
                        "case_id": case_id,
                        "study_axis": self._string(case["study_axis"]),
                        "completed": False,
                    }
                )
                continue
            run_root = execution_path.parent / case_id
            input_path = run_root / "composite-input.json"
            result = extractor.execute(
                input_path,
                run_root,
                base_extractor_path,
                execution_record=execution_case,
            )
            case_result_path = output_directory / f"{case_id}.json"
            case_result_path.write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            case_records.append(
                {
                    "case_id": case_id,
                    "study_axis": self._string(case["study_axis"]),
                    "completed": True,
                    "plane_wave_cutoff": self._integer(case["plane_wave_cutoff"]),
                    "reciprocal_mesh_size": self._integer(case["reciprocal_mesh_size"]),
                    "transverse_lattice_length": self._real(
                        case["transverse_lattice_length"]
                    ),
                    "portable_result_path": case_result_path.relative_to(
                        output_path.parents[3]
                    ).as_posix(),
                    "portable_result_sha256": self._sha256(case_result_path),
                    "summary": self._summary(result),
                    "difference_from_reference": self._difference(result, reference),
                }
            )
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": self._string(study["experiment_id"]),
            "evidence_status": "calculated synthetic numerical verification",
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "authorization_checkpoint": "RM-PERIODIC-2D-NONDFT-STUDY-HC06",
            "provenance": {
                "study_input_path": study_path.relative_to(
                    output_path.parents[3]
                ).as_posix(),
                "study_input_sha256": self._sha256(study_path),
                "execution_result_path": str(execution_path),
                "execution_result_sha256": self._sha256(execution_path),
                "reference_result_path": reference_result_path.relative_to(
                    output_path.parents[3]
                ).as_posix(),
                "reference_result_sha256": self._sha256(reference_result_path),
                "extractor_sha256": self._sha256(Path(__file__).resolve()),
                "base_extractor_sha256": self._sha256(base_extractor_path),
            },
            "reference_case": {
                "case_id": "reference_p3_n15_c15",
                "plane_wave_cutoff": 3,
                "reciprocal_mesh_size": 15,
                "transverse_lattice_length": 15.0,
                "summary": self._summary(reference),
            },
            "cases": case_records,
            "all_declared_cases_completed": all(
                self._mapping(value)["completed"] is True for value in case_records
            ),
            "claim_boundary": (
                "This one-axis-at-a-time study is synthetic numerical verification, "
                "not DFT, material validation, a convergence theorem, or uncertainty "
                "quantification."
            ),
        }
        output_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return payload

    def _summary(self, result: dict[str, JsonValue]) -> dict[str, JsonValue]:
        localization = self._mapping(result["localization"])
        native = self._mapping(localization["native_wannier90"])
        represented = self._mapping(result["represented_comparison"])
        shell = {
            self._integer(self._mapping(value)["maximum_squared_radius"]): self._real(
                self._mapping(value)["omitted_block_frobenius_l2_norm"]
            )
            for value in self._array(represented["shell_study"])
        }
        execution = self._mapping(result["execution"])
        return {
            "iterations": self._integer(execution["iterations"]),
            "interface_neighbor_count": self._integer(
                execution["interface_neighbor_count"]
            ),
            "native_total_spread_cell_squared": self._real(
                native["total_spread_cell_squared"]
            ),
            "common_wannier90_total_spread_cell_squared": self._common_total(
                localization["common_finite_supercell_estimator"]
            ),
            "common_direct_total_spread_cell_squared": self._real(
                localization["direct_projected_total_spread_cell_squared"]
            ),
            "common_wannier90_to_direct_ratio": self._real(
                localization["common_estimator_wannier90_to_direct_spread_ratio"]
            ),
            "common_centers_modulo_cell": [
                self._mapping(value)["center_modulo_cell"]
                for value in self._array(
                    localization["common_finite_supercell_estimator"]
                )
            ],
            "radius_50_hopping_tail_energy_units": shell[50],
            "projector_maximum_frobenius_defect": self._real(
                represented["direct_w90_projector_maximum_frobenius_defect"]
            ),
            "hr_mesh_operator_maximum_frobenius_defect": self._real(
                represented["hr_mesh_operator_maximum_frobenius_defect"]
            ),
        }

    def _difference(
        self, result: dict[str, JsonValue], reference: dict[str, JsonValue]
    ) -> dict[str, JsonValue]:
        current = self._summary(result)
        baseline = self._summary(reference)
        current_centers = [
            self._reals(value)
            for value in self._array(current["common_centers_modulo_cell"])
        ]
        baseline_centers = [
            self._reals(value)
            for value in self._array(baseline["common_centers_modulo_cell"])
        ]
        center_defect = min(
            max(
                self._periodic_distance(
                    current_centers[index], baseline_centers[target]
                )
                for index, target in enumerate(permutation)
            )
            for permutation in itertools.permutations(range(3))
        )
        return {
            "native_total_spread_absolute_difference": abs(
                self._real(current["native_total_spread_cell_squared"])
                - self._real(baseline["native_total_spread_cell_squared"])
            ),
            "common_total_spread_absolute_difference": abs(
                self._real(current["common_wannier90_total_spread_cell_squared"])
                - self._real(baseline["common_wannier90_total_spread_cell_squared"])
            ),
            "common_center_set_maximum_periodic_distance": center_defect,
            "radius_50_hopping_tail_absolute_difference": abs(
                self._real(current["radius_50_hopping_tail_energy_units"])
                - self._real(baseline["radius_50_hopping_tail_energy_units"])
            ),
        }

    def _periodic_distance(
        self, first: tuple[float, ...], second: tuple[float, ...]
    ) -> float:
        differences = [
            abs(left - right) for left, right in zip(first, second, strict=True)
        ]
        wrapped = [min(value, 1.0 - value) for value in differences]
        return float(sum(value * value for value in wrapped) ** 0.5)

    def _common_total(self, value: JsonValue) -> float:
        return sum(
            self._real(self._mapping(record)["spread_cell_squared"])
            for record in self._array(value)
        )

    def _load(self, path: Path) -> dict[str, JsonValue]:
        return self._mapping(
            cast(JsonValue, json.loads(path.read_text(encoding="utf-8")))
        )

    def _sha256(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

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

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        return tuple(self._real(item) for item in self._array(value))


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--study", type=Path, required=True)
    parser.add_argument("--execution", type=Path, required=True)
    parser.add_argument("--reference-result", type=Path, required=True)
    parser.add_argument("--base-extractor", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = Wannier90StudyExtractor().execute(
        cast(Path, arguments.study).resolve(),
        cast(Path, arguments.execution).resolve(),
        cast(Path, arguments.reference_result).resolve(),
        cast(Path, arguments.base_extractor).resolve(),
        cast(Path, arguments.output_directory).resolve(),
        cast(Path, arguments.output).resolve(),
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
