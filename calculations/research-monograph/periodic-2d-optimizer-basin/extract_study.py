#!/usr/bin/env python3
"""Extract basin and convergence evidence from the authorized native runs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import statistics
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

BASE_DIRECTORY = Path(__file__).resolve().parents[1] / "periodic-2d"
if str(BASE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BASE_DIRECTORY))

from extract_wannier90 import CorrectedWannier90Extractor, JsonValue  # noqa: E402


class OptimizerBasinExtractor:
    """Extract all starts, classify observed basins, and apply frozen gates."""

    __slots__ = ()

    def execute(
        self,
        study_path: Path,
        execution_path: Path,
        base_extractor_path: Path,
        output_path: Path,
    ) -> dict[str, JsonValue]:
        study = self._load(study_path)
        execution = self._load(execution_path)
        if execution["all_declared_localizations_attempted"] is not True:
            raise AssertionError("execution did not attempt all declared localizations")
        if execution["stopped_early"] is not False:
            raise AssertionError("execution stopped before the declared boundary")
        execution_by_id = {
            self._string(self._mapping(value)["configuration_id"]): self._mapping(value)
            for value in self._array(execution["configurations"])
        }
        method = self._mapping(study["convergence_method"])
        common_grid = self._integer(method["common_finite_supercell_grid_size"])
        extractor = CorrectedWannier90Extractor()
        configuration_records: list[JsonValue] = []
        for declared_value in self._array(study["configurations"]):
            declared = self._mapping(declared_value)
            identifier = self._string(declared["configuration_id"])
            native = execution_by_id[identifier]
            configuration_records.append(
                self._configuration(
                    declared,
                    native,
                    execution_path.parent,
                    extractor,
                    base_extractor_path,
                    common_grid,
                    method,
                )
            )
        records_by_id = {
            self._string(self._mapping(value)["configuration_id"]): self._mapping(value)
            for value in configuration_records
        }
        convergence = self._convergence(records_by_id, method)
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": self._string(study["experiment_id"]),
            "evidence_status": "calculated synthetic non-DFT numerical verification",
            "authorization_checkpoint": self._string(study["authorization_checkpoint"]),
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "provenance": {
                "study_input_path": study_path.relative_to(
                    output_path.parents[3]
                ).as_posix(),
                "study_input_sha256": self._sha256(study_path),
                "execution_result_path": str(execution_path),
                "execution_result_sha256": self._sha256(execution_path),
                "extractor_path": Path(__file__)
                .relative_to(output_path.parents[3])
                .as_posix(),
                "extractor_sha256": self._sha256(Path(__file__).resolve()),
                "base_extractor_path": base_extractor_path.relative_to(
                    output_path.parents[3]
                ).as_posix(),
                "base_extractor_sha256": self._sha256(base_extractor_path),
            },
            "execution_summary": {
                "configuration_count": len(configuration_records),
                "localization_count": sum(
                    len(self._array(self._mapping(value)["starts"]))
                    for value in configuration_records
                ),
                "all_localization_processes_completed": all(
                    self._mapping(start)["completed"] is True
                    for configuration in configuration_records
                    for start in self._array(self._mapping(configuration)["starts"])
                ),
                "converged_localization_count": sum(
                    self._mapping(start)["convergence_criterion_satisfied"] is True
                    for configuration in configuration_records
                    for start in self._array(self._mapping(configuration)["starts"])
                ),
                "nonconverged_localization_count": sum(
                    self._mapping(start)["convergence_criterion_satisfied"] is False
                    for configuration in configuration_records
                    for start in self._array(self._mapping(configuration)["starts"])
                ),
                "elapsed_seconds": execution["elapsed_seconds"],
                "external_output_bytes_at_execution_end": execution[
                    "external_output_bytes"
                ],
                "maximum_localization_seconds": max(
                    self._real(self._mapping(start)["elapsed_seconds"])
                    for configuration in configuration_records
                    for start in self._array(self._mapping(configuration)["starts"])
                ),
                "maximum_localization_resident_bytes": max(
                    self._integer(self._mapping(start)["maximum_resident_bytes"])
                    for configuration in configuration_records
                    for start in self._array(self._mapping(configuration)["starts"])
                ),
            },
            "configurations": configuration_records,
            "convergence_assessment": convergence,
            "claim_boundary": study["claim_boundary"],
        }
        output_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return payload

    def _configuration(
        self,
        declared: dict[str, JsonValue],
        native: dict[str, JsonValue],
        execution_root: Path,
        extractor: CorrectedWannier90Extractor,
        base_extractor_path: Path,
        common_grid: int,
        method: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        identifier = self._string(declared["configuration_id"])
        configuration_root = execution_root / identifier
        input_path = configuration_root / "composite-input.json"
        controls = self._load(input_path)
        controls["localization_fft_size"] = common_grid
        analysis_input = configuration_root / "analysis-input-512.json"
        analysis_input.write_text(
            json.dumps(controls, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        preprocessing = next(
            self._mapping(value)
            for value in self._array(native["interface_stages"])
            if self._mapping(value)["stage"] == "preprocessing"
        )
        localization_by_id = {
            self._string(self._mapping(value)["gauge_id"]): self._mapping(value)
            for value in self._array(native["localizations"])
        }
        starts: list[JsonValue] = []
        for gauge_id in sorted(localization_by_id):
            localization_record = localization_by_id[gauge_id]
            stage = self._mapping(localization_record["stage"])
            gauge_root = configuration_root / gauge_id
            seed_root = gauge_root / "low_triple"
            self._compatibility_records(seed_root, preprocessing, stage)
            extraction_execution: dict[str, JsonValue] = {
                "stages": [preprocessing, stage]
            }
            extracted = extractor.execute(
                analysis_input,
                gauge_root,
                base_extractor_path,
                execution_record=extraction_execution,
            )
            extracted["experiment_id"] = (
                "research-monograph.periodic-2d.optimizer-basin.start.v1"
            )
            extracted["authorization_checkpoint"] = (
                "RM-PERIODIC-2D-OPTIMIZER-BASIN-EXECUTION-HC07"
            )
            extracted["analysis_context"] = {
                "configuration_id": identifier,
                "gauge_id": gauge_id,
                "common_finite_supercell_grid_size": common_grid,
            }
            analysis_path = gauge_root / "analysis-result.json"
            analysis_path.write_text(
                json.dumps(extracted, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            starts.append(
                self._start_summary(
                    gauge_id,
                    localization_record,
                    extracted,
                    analysis_path,
                )
            )
        converged_starts = [
            value
            for value in starts
            if self._mapping(value)["convergence_criterion_satisfied"] is True
        ]
        if not converged_starts:
            raise AssertionError(f"{identifier} has no converged localization")
        basin_records = self._basins(converged_starts, method)
        best = min(
            (self._mapping(value) for value in converged_starts),
            key=lambda value: (
                self._real(value["native_total_spread_cell_squared"]),
                self._string(value["gauge_id"]),
            ),
        )
        median = self._median_summary(converged_starts)
        return {
            "configuration_id": identifier,
            "study_axes": declared["study_axes"],
            "plane_wave_cutoff": declared["plane_wave_cutoff"],
            "reciprocal_mesh_size": declared["reciprocal_mesh_size"],
            "transverse_lattice_length": declared["transverse_lattice_length"],
            "analysis_input_path": str(analysis_input),
            "analysis_input_sha256": self._sha256(analysis_input),
            "starts": starts,
            "converged_start_count": len(converged_starts),
            "nonconverged_gauge_ids": [
                self._mapping(value)["gauge_id"]
                for value in starts
                if self._mapping(value)["convergence_criterion_satisfied"] is False
            ],
            "observed_converged_basins": basin_records,
            "observed_converged_basin_count": len(basin_records),
            "best_observed_converged": best,
            "median_across_converged_starts": median,
            "best_is_observed_not_proven_global": True,
        }

    def _start_summary(
        self,
        gauge_id: str,
        execution: dict[str, JsonValue],
        result: dict[str, JsonValue],
        analysis_path: Path,
    ) -> dict[str, JsonValue]:
        localization = self._mapping(result["localization"])
        native = self._mapping(localization["native_wannier90"])
        common = [
            self._mapping(value)
            for value in self._array(localization["common_finite_supercell_estimator"])
        ]
        represented = self._mapping(result["represented_comparison"])
        shell_50 = next(
            self._mapping(value)
            for value in self._array(represented["shell_study"])
            if self._integer(self._mapping(value)["maximum_squared_radius"]) == 50
        )
        stage = self._mapping(execution["stage"])
        memory = stage["maximum_resident_bytes"]
        if memory is None:
            raise ValueError("localization record lacks resident memory")
        return {
            "gauge_id": gauge_id,
            "completed": execution["completed"],
            "convergence_criterion_satisfied": self._mapping(result["execution"])[
                "convergence_criterion_satisfied"
            ],
            "iterations": self._mapping(result["execution"])["iterations"],
            "elapsed_seconds": stage["elapsed_seconds"],
            "maximum_resident_bytes": memory,
            "native_total_spread_cell_squared": native["total_spread_cell_squared"],
            "native_centers_modulo_cell": [
                self._mapping(value)["active_fractional_modulo_cell"]
                for value in self._array(native["centers_cell_fractional"])
            ],
            "common_total_spread_cell_squared": sum(
                self._real(value["spread_cell_squared"]) for value in common
            ),
            "common_centers_modulo_cell": [
                value["center_modulo_cell"] for value in common
            ],
            "common_direct_total_spread_cell_squared": localization[
                "direct_projected_total_spread_cell_squared"
            ],
            "radius_50_hopping_tail_energy_units": shell_50[
                "omitted_block_frobenius_l2_norm"
            ],
            "projector_maximum_frobenius_defect": represented[
                "direct_w90_projector_maximum_frobenius_defect"
            ],
            "hr_mesh_operator_maximum_frobenius_defect": represented[
                "hr_mesh_operator_maximum_frobenius_defect"
            ],
            "analysis_result_path": str(analysis_path),
            "analysis_result_sha256": self._sha256(analysis_path),
        }

    def _basins(
        self, starts: list[JsonValue], method: dict[str, JsonValue]
    ) -> list[JsonValue]:
        spread_tolerance = self._real(method["basin_spread_absolute_tolerance"])
        center_tolerance = self._real(method["basin_center_set_periodic_tolerance"])
        basins: list[dict[str, JsonValue]] = []
        ordered = sorted(
            (self._mapping(value) for value in starts),
            key=lambda value: (
                self._real(value["native_total_spread_cell_squared"]),
                self._string(value["gauge_id"]),
            ),
        )
        for start in ordered:
            match: dict[str, JsonValue] | None = None
            for basin in basins:
                if (
                    abs(
                        self._real(start["native_total_spread_cell_squared"])
                        - self._real(
                            basin["representative_native_total_spread_cell_squared"]
                        )
                    )
                    <= spread_tolerance
                    and self._center_set_distance(
                        start["native_centers_modulo_cell"],
                        basin["representative_native_centers_modulo_cell"],
                    )
                    <= center_tolerance
                ):
                    match = basin
                    break
            if match is None:
                match = {
                    "basin_id": f"basin_{len(basins) + 1:02d}",
                    "representative_gauge_id": start["gauge_id"],
                    "representative_native_total_spread_cell_squared": start[
                        "native_total_spread_cell_squared"
                    ],
                    "representative_native_centers_modulo_cell": start[
                        "native_centers_modulo_cell"
                    ],
                    "gauge_ids": [],
                    "occupancy": 0,
                }
                basins.append(match)
            self._array(match["gauge_ids"]).append(start["gauge_id"])
            match["occupancy"] = self._integer(match["occupancy"]) + 1
        return cast(list[JsonValue], basins)

    def _median_summary(self, starts: list[JsonValue]) -> dict[str, JsonValue]:
        records = [self._mapping(value) for value in starts]
        medoid = min(
            records,
            key=lambda candidate: sum(
                self._center_set_distance(
                    candidate["native_centers_modulo_cell"],
                    other["native_centers_modulo_cell"],
                )
                for other in records
            ),
        )
        return {
            "native_total_spread_cell_squared": statistics.median(
                self._real(value["native_total_spread_cell_squared"])
                for value in records
            ),
            "common_total_spread_cell_squared": statistics.median(
                self._real(value["common_total_spread_cell_squared"])
                for value in records
            ),
            "radius_50_hopping_tail_energy_units": statistics.median(
                self._real(value["radius_50_hopping_tail_energy_units"])
                for value in records
            ),
            "native_centers_modulo_cell_medoid": medoid["native_centers_modulo_cell"],
            "common_centers_modulo_cell_medoid": medoid["common_centers_modulo_cell"],
            "center_medoid_gauge_id": medoid["gauge_id"],
        }

    def _convergence(
        self,
        records: dict[str, dict[str, JsonValue]],
        method: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        mesh = self._pair(
            records["mesh_n19_p4_c19"], records["mesh_n23_p4_c23"], method
        )
        cutoff = self._pair(
            records["mesh_n19_p4_c19"], records["cutoff_p5_n19_c19"], method
        )
        supporting = mesh["supporting"] is True and cutoff["supporting"] is True
        embedding = [
            self._axis_summary(records[identifier])
            for identifier in (
                "embedding_c15_p4_n19",
                "mesh_n19_p4_c19",
                "embedding_c23_p4_n19",
            )
        ]
        return {
            "mesh_finest_pair": mesh,
            "cutoff_finest_pair": cutoff,
            "embedding_sensitivity": embedding,
            "supports_declared_convergence": supporting,
            "disposition": (
                "supports the frozen finite-parameter convergence criteria"
                if supporting
                else "does not support the frozen finite-parameter convergence criteria"
            ),
            "not_a_global_or_general_claim": True,
        }

    def _pair(
        self,
        lower: dict[str, JsonValue],
        upper: dict[str, JsonValue],
        method: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        best_lower = self._mapping(lower["best_observed_converged"])
        best_upper = self._mapping(upper["best_observed_converged"])
        median_lower = self._mapping(lower["median_across_converged_starts"])
        median_upper = self._mapping(upper["median_across_converged_starts"])
        best = self._differences(best_lower, best_upper, False)
        median = self._differences(median_lower, median_upper, True)
        spread_tolerance = self._real(method["finest_pair_relative_spread_tolerance"])
        center_tolerance = self._real(
            method["finest_pair_center_set_periodic_tolerance"]
        )
        tail_tolerance = self._real(
            method["finest_pair_relative_hopping_tail_tolerance"]
        )
        metrics_pass = all(
            self._real(self._mapping(value)["relative_spread_difference"])
            <= spread_tolerance
            and self._real(self._mapping(value)["center_set_periodic_distance"])
            <= center_tolerance
            and self._real(self._mapping(value)["relative_hopping_tail_difference"])
            <= tail_tolerance
            for value in (best, median)
        )
        minimum_occupancy = self._integer(
            method["minimum_repeated_best_basin_occupancy"]
        )
        occupancy = min(
            self._integer(
                self._mapping(self._array(lower["observed_converged_basins"])[0])[
                    "occupancy"
                ]
            ),
            self._integer(
                self._mapping(self._array(upper["observed_converged_basins"])[0])[
                    "occupancy"
                ]
            ),
        )
        return {
            "lower_configuration_id": lower["configuration_id"],
            "upper_configuration_id": upper["configuration_id"],
            "best_observed_differences": best,
            "median_across_converged_starts_differences": median,
            "minimum_endpoint_best_basin_occupancy": occupancy,
            "metrics_pass": metrics_pass,
            "occupancy_pass": occupancy >= minimum_occupancy,
            "supporting": metrics_pass and occupancy >= minimum_occupancy,
        }

    def _differences(
        self,
        lower: dict[str, JsonValue],
        upper: dict[str, JsonValue],
        median: bool,
    ) -> dict[str, JsonValue]:
        center_key = (
            "native_centers_modulo_cell_medoid"
            if median
            else "native_centers_modulo_cell"
        )
        return {
            "relative_spread_difference": self._relative(
                self._real(lower["native_total_spread_cell_squared"]),
                self._real(upper["native_total_spread_cell_squared"]),
            ),
            "center_set_periodic_distance": self._center_set_distance(
                lower[center_key], upper[center_key]
            ),
            "relative_hopping_tail_difference": self._relative(
                self._real(lower["radius_50_hopping_tail_energy_units"]),
                self._real(upper["radius_50_hopping_tail_energy_units"]),
            ),
        }

    def _axis_summary(
        self, configuration: dict[str, JsonValue]
    ) -> dict[str, JsonValue]:
        return {
            "configuration_id": configuration["configuration_id"],
            "transverse_lattice_length": configuration["transverse_lattice_length"],
            "observed_converged_basin_count": configuration[
                "observed_converged_basin_count"
            ],
            "best_observed_converged": configuration["best_observed_converged"],
            "median_across_converged_starts": configuration[
                "median_across_converged_starts"
            ],
        }

    def _center_set_distance(self, first: JsonValue, second: JsonValue) -> float:
        left = [self._reals(value) for value in self._array(first)]
        right = [self._reals(value) for value in self._array(second)]
        if len(left) != len(right):
            raise ValueError("center sets must have equal cardinality")
        return min(
            max(
                self._periodic_distance(left[index], right[target])
                for index, target in enumerate(permutation)
            )
            for permutation in itertools.permutations(range(len(right)))
        )

    @staticmethod
    def _periodic_distance(
        first: tuple[float, ...], second: tuple[float, ...]
    ) -> float:
        differences = [
            min(abs(left - right), 1.0 - abs(left - right))
            for left, right in zip(first, second, strict=True)
        ]
        return float(sum(value * value for value in differences) ** 0.5)

    @staticmethod
    def _relative(first: float, second: float) -> float:
        return abs(first - second) / max(abs(second), 1.0e-15)

    def _compatibility_records(
        self,
        seed_root: Path,
        preprocessing: dict[str, JsonValue],
        localization: dict[str, JsonValue],
    ) -> None:
        (seed_root / "low_triple.pp.exitcode").write_text(
            f"{self._integer(preprocessing['exit_code'])}\n", encoding="utf-8"
        )
        (seed_root / "low_triple.run.exitcode").write_text(
            f"{self._integer(localization['exit_code'])}\n", encoding="utf-8"
        )
        for suffix, record in (("pp", preprocessing), ("run", localization)):
            (seed_root / f"low_triple.{suffix}.time").write_text(
                f"{self._real(record['elapsed_seconds']):.6f} real\n"
                f"{self._integer(record['maximum_resident_bytes'])} "
                "maximum resident set size\n",
                encoding="utf-8",
            )

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

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

    def _reals(self, value: JsonValue) -> tuple[float, ...]:
        return tuple(self._real(item) for item in self._array(value))


class CommandAdapter:
    """Adapt CLI paths to the extraction action."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--study", type=Path, required=True)
        parser.add_argument("--execution", type=Path, required=True)
        parser.add_argument("--base-extractor", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        arguments = parser.parse_args(argv)
        result = OptimizerBasinExtractor().execute(
            cast(Path, arguments.study).resolve(),
            cast(Path, arguments.execution).resolve(),
            cast(Path, arguments.base_extractor).resolve(),
            cast(Path, arguments.output).resolve(),
        )
        execution = result["execution_summary"]
        convergence = result["convergence_assessment"]
        if not isinstance(execution, dict) or not isinstance(convergence, dict):
            raise TypeError("result summaries must be objects")
        print(
            json.dumps(
                {
                    "localization_count": execution["localization_count"],
                    "supports_declared_convergence": convergence[
                        "supports_declared_convergence"
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
