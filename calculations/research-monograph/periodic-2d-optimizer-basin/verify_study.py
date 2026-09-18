#!/usr/bin/env python3
"""Independently verify the optimizer-basin and convergence study."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import sys
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

BASE_DIRECTORY = Path(__file__).resolve().parents[1] / "periodic-2d"
if str(BASE_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(BASE_DIRECTORY))

from verify_wannier90_balanced import (  # noqa: E402
    CorrectedWannier90Verifier,
    JsonValue,
)

type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexTensor = npt.NDArray[np.complex128]


class OptimizerBasinVerifier:
    """Verify identities, native outcomes, basin grouping, and frozen gates."""

    __slots__ = ()

    def execute(self, result_path: Path, *, verify_native: bool) -> None:
        result = self._load(result_path)
        if self._integer(result["schema_version"]) != 1:
            raise ValueError("unsupported result schema")
        if (
            result["evidence_status"]
            != "calculated synthetic non-DFT numerical verification"
        ):
            raise ValueError("unexpected evidence status")
        repository_root = result_path.parents[3]
        provenance = self._mapping(result["provenance"])
        study_path = repository_root / self._string(provenance["study_input_path"])
        extractor_path = repository_root / self._string(provenance["extractor_path"])
        base_extractor_path = repository_root / self._string(
            provenance["base_extractor_path"]
        )
        execution_path = Path(self._string(provenance["execution_result_path"]))
        self._identity(study_path, provenance["study_input_sha256"], "study input")
        self._identity(extractor_path, provenance["extractor_sha256"], "extractor")
        self._identity(
            base_extractor_path,
            provenance["base_extractor_sha256"],
            "base extractor",
        )
        self._identity(
            execution_path,
            provenance["execution_result_sha256"],
            "execution result",
        )
        study = self._load(study_path)
        execution = self._load(execution_path)
        self._verify_execution(study, execution, execution_path.parent)
        configurations = [
            self._mapping(value) for value in self._array(result["configurations"])
        ]
        declared = {
            self._string(self._mapping(value)["configuration_id"]): self._mapping(value)
            for value in self._array(study["configurations"])
        }
        if set(declared) != {
            self._string(value["configuration_id"]) for value in configurations
        }:
            raise AssertionError("declared and extracted configurations disagree")
        convergence_method = self._mapping(study["convergence_method"])
        converged_count = 0
        nonconverged_count = 0
        base_verifier = CorrectedWannier90Verifier()
        for configuration in configurations:
            identifier = self._string(configuration["configuration_id"])
            self._verify_configuration(
                configuration,
                declared[identifier],
                convergence_method,
                repository_root,
                base_extractor_path,
                base_verifier,
                verify_native,
            )
            starts = [
                self._mapping(value) for value in self._array(configuration["starts"])
            ]
            converged_count += sum(
                value["convergence_criterion_satisfied"] is True for value in starts
            )
            nonconverged_count += sum(
                value["convergence_criterion_satisfied"] is False for value in starts
            )
        summary = self._mapping(result["execution_summary"])
        self._equal(
            converged_count,
            self._integer(summary["converged_localization_count"]),
            "converged count",
        )
        self._equal(
            nonconverged_count,
            self._integer(summary["nonconverged_localization_count"]),
            "nonconverged count",
        )
        self._equal(converged_count + nonconverged_count, 72, "total outcomes")
        self._verify_convergence(result, convergence_method)

    def _verify_execution(
        self,
        study: dict[str, JsonValue],
        execution: dict[str, JsonValue],
        execution_root: Path,
    ) -> None:
        if execution["stopped_early"] is not False:
            raise AssertionError("execution stopped early")
        if execution["all_declared_localizations_attempted"] is not True:
            raise AssertionError("not all localizations were attempted")
        limits = self._mapping(study["execution_limits"])
        if self._real(execution["elapsed_seconds"]) > self._integer(
            limits["maximum_total_seconds"]
        ):
            raise AssertionError("total execution time exceeded")
        if self._integer(execution["external_output_bytes"]) > self._integer(
            limits["maximum_external_output_bytes_total"]
        ):
            raise AssertionError("execution output exceeded")
        localization_count = 0
        for configuration_value in self._array(execution["configurations"]):
            configuration = self._mapping(configuration_value)
            if configuration["interface_completed"] is not True:
                raise AssertionError("interface preparation did not complete")
            for stage_value in self._array(configuration["interface_stages"]):
                self._verify_stage(self._mapping(stage_value), limits)
            for localization_value in self._array(configuration["localizations"]):
                localization = self._mapping(localization_value)
                localization_count += 1
                if localization["completed"] is not True:
                    raise AssertionError("localization process failed")
                if localization["resource_limit_exceeded"] is not False:
                    raise AssertionError("localization exceeded a resource limit")
                self._verify_stage(self._mapping(localization["stage"]), limits)
                root = (
                    execution_root
                    / self._string(configuration["configuration_id"])
                    / self._string(localization["gauge_id"])
                )
                for file_value in self._array(localization["file_manifest"]):
                    file_record = self._mapping(file_value)
                    path = root / self._string(file_record["path"])
                    self._identity(path, file_record["sha256"], str(path))
                    self._equal(
                        path.stat().st_size,
                        self._integer(file_record["bytes"]),
                        f"{path} size",
                    )
        self._equal(
            localization_count,
            self._integer(limits["maximum_localizations"]),
            "localization attempts",
        )

    def _verify_stage(
        self, stage: dict[str, JsonValue], limits: dict[str, JsonValue]
    ) -> None:
        self._equal(self._integer(stage["exit_code"]), 0, "stage exit code")
        if stage["timed_out"] is not False:
            raise AssertionError("stage timed out")
        if self._real(stage["elapsed_seconds"]) > self._integer(
            limits["maximum_seconds_per_stage"]
        ):
            raise AssertionError("stage time exceeded")
        memory = stage["maximum_resident_bytes"]
        if memory is not None and self._integer(memory) > self._integer(
            limits["maximum_resident_bytes_per_stage"]
        ):
            raise AssertionError("stage memory exceeded")

    def _verify_configuration(
        self,
        configuration: dict[str, JsonValue],
        declared: dict[str, JsonValue],
        method: dict[str, JsonValue],
        repository_root: Path,
        base_extractor_path: Path,
        base_verifier: CorrectedWannier90Verifier,
        verify_native: bool,
    ) -> None:
        identifier = self._string(configuration["configuration_id"])
        for key in (
            "plane_wave_cutoff",
            "reciprocal_mesh_size",
            "transverse_lattice_length",
        ):
            if configuration[key] != declared[key]:
                raise AssertionError(f"{identifier} {key} disagrees with input")
        starts = [
            self._mapping(value) for value in self._array(configuration["starts"])
        ]
        if len(starts) != 8:
            raise AssertionError(f"{identifier} must contain eight starts")
        converged = [
            value
            for value in starts
            if value["convergence_criterion_satisfied"] is True
        ]
        nonconverged = [
            value
            for value in starts
            if value["convergence_criterion_satisfied"] is False
        ]
        self._equal(
            len(converged),
            self._integer(configuration["converged_start_count"]),
            f"{identifier} converged count",
        )
        if sorted(self._string(value["gauge_id"]) for value in nonconverged) != sorted(
            self._string(value)
            for value in self._array(configuration["nonconverged_gauge_ids"])
        ):
            raise AssertionError(f"{identifier} nonconverged identities disagree")
        for start in starts:
            self._verify_start(
                start,
                repository_root,
                base_extractor_path,
                base_verifier,
                verify_native,
            )
        best = min(
            converged,
            key=lambda value: (
                self._real(value["native_total_spread_cell_squared"]),
                self._string(value["gauge_id"]),
            ),
        )
        reported_best = self._mapping(configuration["best_observed_converged"])
        if best["gauge_id"] != reported_best["gauge_id"]:
            raise AssertionError(f"{identifier} best converged gauge disagrees")
        expected_basins = self._cluster(converged, method)
        reported_basins = [
            sorted(
                self._string(gauge)
                for gauge in self._array(self._mapping(value)["gauge_ids"])
            )
            for value in self._array(configuration["observed_converged_basins"])
        ]
        if sorted(expected_basins) != sorted(reported_basins):
            raise AssertionError(f"{identifier} basin classification disagrees")

    def _verify_start(
        self,
        start: dict[str, JsonValue],
        repository_root: Path,
        base_extractor_path: Path,
        base_verifier: CorrectedWannier90Verifier,
        verify_native: bool,
    ) -> None:
        analysis_path = Path(self._string(start["analysis_result_path"]))
        self._identity(analysis_path, start["analysis_result_sha256"], "analysis")
        analysis = self._load(analysis_path)
        execution = self._mapping(analysis["execution"])
        convergence = execution["convergence_criterion_satisfied"]
        if convergence is not start["convergence_criterion_satisfied"]:
            raise AssertionError("summary convergence status disagrees")
        run_root = Path(
            self._string(self._mapping(analysis["provenance"])["external_run_root"])
        )
        seed_root = run_root / "low_triple"
        wout = (seed_root / "low_triple.wout").read_text(encoding="utf-8")
        phrase_present = "Wannierisation convergence criteria satisfied" in wout
        if phrase_present is not convergence:
            raise AssertionError("native convergence statement disagrees")
        iterations = re.findall(r"^\s+(\d+)\s+.*<-- CONV$", wout, re.MULTILINE)
        if not iterations:
            raise AssertionError("native iteration records are absent")
        self._equal(
            int(iterations[-1]), self._integer(start["iterations"]), "iterations"
        )
        final = wout.rsplit("Final State", maxsplit=1)[1]
        spread_match = re.search(
            r"Final Spread \(Ang\^2\)\s+Omega Total\s+=\s+([^\s]+)", final
        )
        if spread_match is None:
            raise AssertionError("native final spread is absent")
        self._close(
            float(spread_match.group(1)),
            self._real(start["native_total_spread_cell_squared"]),
            5.0e-10,
            "native spread",
        )
        unitaries = self._u_matrices(seed_root / "low_triple_u.mat")
        defect = float(
            np.max(
                np.linalg.norm(
                    unitaries.conj().transpose(0, 2, 1) @ unitaries - np.eye(3),
                    axis=(-2, -1),
                )
            )
        )
        if defect > 1.0e-8:
            raise AssertionError("native U matrices are not unitary")
        tail = self._radius_50_tail(seed_root / "low_triple_hr.dat")
        self._close(
            tail,
            self._real(start["radius_50_hopping_tail_energy_units"]),
            1.0e-14,
            "hopping tail",
        )
        if verify_native and convergence is True:
            base_verifier.execute(
                analysis_path,
                portable=False,
                repository_root=repository_root,
                extractor_path=base_extractor_path,
            )

    def _verify_convergence(
        self, result: dict[str, JsonValue], method: dict[str, JsonValue]
    ) -> None:
        records = {
            self._string(self._mapping(value)["configuration_id"]): self._mapping(value)
            for value in self._array(result["configurations"])
        }
        convergence = self._mapping(result["convergence_assessment"])
        expected_mesh = self._pair(
            records["mesh_n19_p4_c19"], records["mesh_n23_p4_c23"], method
        )
        expected_cutoff = self._pair(
            records["mesh_n19_p4_c19"], records["cutoff_p5_n19_c19"], method
        )
        for label, expected in (
            ("mesh_finest_pair", expected_mesh),
            ("cutoff_finest_pair", expected_cutoff),
        ):
            observed = self._mapping(convergence[label])
            for key in ("metrics_pass", "occupancy_pass", "supporting"):
                if observed[key] is not expected[key]:
                    raise AssertionError(f"{label} {key} disagrees")
        expected_support = (
            expected_mesh["supporting"] is True
            and expected_cutoff["supporting"] is True
        )
        if convergence["supports_declared_convergence"] is not expected_support:
            raise AssertionError("overall convergence disposition disagrees")

    def _pair(
        self,
        lower: dict[str, JsonValue],
        upper: dict[str, JsonValue],
        method: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        best = self._difference(
            self._mapping(lower["best_observed_converged"]),
            self._mapping(upper["best_observed_converged"]),
            median=False,
        )
        median = self._difference(
            self._mapping(lower["median_across_converged_starts"]),
            self._mapping(upper["median_across_converged_starts"]),
            median=True,
        )
        metrics = all(
            value[0] <= self._real(method["finest_pair_relative_spread_tolerance"])
            and value[1]
            <= self._real(method["finest_pair_center_set_periodic_tolerance"])
            and value[2]
            <= self._real(method["finest_pair_relative_hopping_tail_tolerance"])
            for value in (best, median)
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
        occupancy_pass = occupancy >= self._integer(
            method["minimum_repeated_best_basin_occupancy"]
        )
        return {
            "metrics_pass": metrics,
            "occupancy_pass": occupancy_pass,
            "supporting": metrics and occupancy_pass,
        }

    def _difference(
        self,
        lower: dict[str, JsonValue],
        upper: dict[str, JsonValue],
        *,
        median: bool,
    ) -> tuple[float, float, float]:
        center_key = (
            "native_centers_modulo_cell_medoid"
            if median
            else "native_centers_modulo_cell"
        )
        return (
            self._relative(
                self._real(lower["native_total_spread_cell_squared"]),
                self._real(upper["native_total_spread_cell_squared"]),
            ),
            self._center_set_distance(lower[center_key], upper[center_key]),
            self._relative(
                self._real(lower["radius_50_hopping_tail_energy_units"]),
                self._real(upper["radius_50_hopping_tail_energy_units"]),
            ),
        )

    def _cluster(
        self,
        starts: list[dict[str, JsonValue]],
        method: dict[str, JsonValue],
    ) -> list[list[str]]:
        spread_tolerance = self._real(method["basin_spread_absolute_tolerance"])
        center_tolerance = self._real(method["basin_center_set_periodic_tolerance"])
        clusters: list[list[dict[str, JsonValue]]] = []
        for start in sorted(
            starts,
            key=lambda value: (
                self._real(value["native_total_spread_cell_squared"]),
                self._string(value["gauge_id"]),
            ),
        ):
            match = next(
                (
                    cluster
                    for cluster in clusters
                    if abs(
                        self._real(start["native_total_spread_cell_squared"])
                        - self._real(cluster[0]["native_total_spread_cell_squared"])
                    )
                    <= spread_tolerance
                    and self._center_set_distance(
                        start["native_centers_modulo_cell"],
                        cluster[0]["native_centers_modulo_cell"],
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
            sorted(self._string(value["gauge_id"]) for value in cluster)
            for cluster in clusters
        ]

    def _u_matrices(self, path: Path) -> ComplexTensor:
        lines = path.read_text(encoding="utf-8").splitlines()
        dimensions = [int(value) for value in lines[1].split()]
        if len(dimensions) != 3:
            raise ValueError("unexpected U-matrix dimensions")
        count, rows, columns = dimensions
        matrices = np.empty((count, rows, columns), dtype=complex)
        cursor = 2
        for point in range(count):
            while not lines[cursor].strip():
                cursor += 1
            cursor += 1
            values: list[complex] = []
            for _ in range(rows * columns):
                real, imaginary = (float(value) for value in lines[cursor].split())
                values.append(complex(real, imaginary))
                cursor += 1
            matrices[point] = np.asarray(values).reshape((rows, columns), order="F")
        return matrices

    def _radius_50_tail(self, path: Path) -> float:
        lines = path.read_text(encoding="utf-8").splitlines()
        rank = int(lines[1])
        count = int(lines[2])
        cursor = 3
        degeneracies: list[int] = []
        while len(degeneracies) < count:
            degeneracies.extend(int(value) for value in lines[cursor].split())
            cursor += 1
        if any(value != 1 for value in degeneracies):
            raise AssertionError("nonunit hopping degeneracy")
        blocks: dict[tuple[int, int], ComplexMatrix] = {}
        for line in lines[cursor:]:
            rx, ry, rz, row, column, real, imaginary = line.split()
            if int(rz) != 0:
                raise AssertionError("inactive hopping translation is nonzero")
            key = (int(rx), int(ry))
            matrix = blocks.setdefault(key, np.zeros((rank, rank), dtype=complex))
            matrix[int(row) - 1, int(column) - 1] = complex(
                float(real), float(imaginary)
            )
        return math.sqrt(
            sum(
                float(np.linalg.norm(matrix) ** 2)
                for (rx, ry), matrix in blocks.items()
                if rx * rx + ry * ry > 50
            )
        )

    def _center_set_distance(self, first: JsonValue, second: JsonValue) -> float:
        left = [self._reals(value) for value in self._array(first)]
        right = [self._reals(value) for value in self._array(second)]
        return min(
            max(
                math.dist(
                    (0.0, 0.0),
                    tuple(
                        min(abs(a - b), 1.0 - abs(a - b))
                        for a, b in zip(left[index], right[target], strict=True)
                    ),
                )
                for index, target in enumerate(permutation)
            )
            for permutation in itertools.permutations(range(len(right)))
        )

    @staticmethod
    def _relative(first: float, second: float) -> float:
        return abs(first - second) / max(abs(second), 1.0e-15)

    def _identity(self, path: Path, expected: JsonValue, label: str) -> None:
        digest = self._string(expected)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={digest}"
            )

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
    """Adapt CLI arguments to the independent verifier."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        parser.add_argument("--native", action="store_true")
        arguments = parser.parse_args(argv)
        OptimizerBasinVerifier().execute(
            cast(Path, arguments.result).resolve(),
            verify_native=bool(arguments.native),
        )
        source = "native_external_runs" if arguments.native else "summary_and_manifests"
        print(f"periodic_2d_optimizer_basin_verification=PASS source={source}")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
