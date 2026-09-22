#!/usr/bin/env python3
"""Independently verify the extracted standalone-study results."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from execute_study import JsonValue

type ComplexArray = npt.NDArray[np.complex128]
type RealArray = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class IndependentReconstruction:
    """Independent common-grid records and ephemeral densities."""

    records: list[JsonValue]
    densities: tuple[RealArray, ...]


class IndependentCommonEstimator:
    """Reconstruct selected common-grid endpoints without the primary extractor."""

    __slots__ = ()

    def execute(
        self, controls: dict[str, JsonValue], seed_root: Path, fft_size: int
    ) -> IndependentReconstruction:
        kpoints, unitaries = self._u_matrices(seed_root / "low_triple_u.mat")
        raw_frames = self._raw_frames(controls, kpoints)
        frames = raw_frames @ unitaries
        cutoff = self._integer(controls["plane_wave_cutoff"])
        mesh_size = self._integer(controls["reciprocal_mesh_size"])
        plane = range(-cutoff, cutoff + 1)
        coordinate = np.arange(fft_size, dtype=float) * mesh_size / fft_size
        records: list[JsonValue] = []
        densities: list[RealArray] = []
        for orbital in range(3):
            coefficients = np.zeros((fft_size, fft_size), dtype=np.complex128)
            for point, (kx, ky, _) in enumerate(kpoints):
                ix = int(round(float(kx) * mesh_size)) % mesh_size
                iy = int(round(float(ky) * mesh_size)) % mesh_size
                cursor = 0
                for p in plane:
                    for q in plane:
                        coefficients[
                            (p * mesh_size + ix) % fft_size,
                            (q * mesh_size + iy) % fft_size,
                        ] = frames[point, cursor, orbital] / mesh_size
                        cursor += 1
            wave = np.fft.ifft2(coefficients) * fft_size**2
            density = np.abs(wave) ** 2
            density /= np.sum(density)
            center_x = self._center(np.sum(density, axis=1), coordinate, mesh_size)
            center_y = self._center(np.sum(density, axis=0), coordinate, mesh_size)
            dx = (coordinate - center_x + mesh_size / 2.0) % mesh_size
            dx -= mesh_size / 2.0
            dy = (coordinate - center_y + mesh_size / 2.0) % mesh_size
            dy -= mesh_size / 2.0
            spread = float(np.sum(density * (dx[:, None] ** 2 + dy[None, :] ** 2)))
            digest = hashlib.sha256(
                np.round(density, 12).astype("<f8", copy=False).tobytes(order="C")
            ).hexdigest()
            records.append(
                {
                    "orbital": orbital,
                    "center_supercell_cells": [center_x, center_y],
                    "center_modulo_cell": [center_x % 1.0, center_y % 1.0],
                    "spread_cell_squared": spread,
                    "density_content_sha256": digest,
                }
            )
            density = np.asarray(density, dtype=np.float64)
            density.setflags(write=False)
            densities.append(density)
        return IndependentReconstruction(records, tuple(densities))

    def _raw_frames(
        self, controls: dict[str, JsonValue], kpoints: RealArray
    ) -> ComplexArray:
        potential = self._mapping(controls["potential"])
        cutoff = self._integer(controls["plane_wave_cutoff"])
        indices = np.arange(-cutoff, cutoff + 1)
        p_grid, q_grid = np.meshgrid(indices, indices, indexing="ij")
        p = p_grid.ravel()
        q = q_grid.ravel()
        dp = p[:, None] - p[None, :]
        dq = q[:, None] - q[None, :]
        frames = np.empty((len(kpoints), len(p), 3), dtype=np.complex128)
        for index, (kx, ky, _) in enumerate(kpoints):
            matrix = np.diag((kx + p) ** 2 + (ky + q) ** 2).astype(complex)
            matrix += (self._real(potential["lambda_x"]) / 2.0) * (
                (np.abs(dp) == 1) & (dq == 0)
            )
            matrix += (self._real(potential["lambda_y"]) / 2.0) * (
                (dp == 0) & (np.abs(dq) == 1)
            )
            matrix += (self._real(potential["lambda_xy"]) / 4.0) * (
                (np.abs(dp) == 1) & (np.abs(dq) == 1)
            )
            _, vectors = np.linalg.eigh(matrix)
            frames[index] = vectors[:, :3]
        return frames

    def _u_matrices(self, path: Path) -> tuple[RealArray, ComplexArray]:
        lines = path.read_text(encoding="utf-8").splitlines()
        count, rows, columns = (int(value) for value in lines[1].split())
        kpoints = np.empty((count, 3), dtype=float)
        matrices = np.empty((count, rows, columns), dtype=complex)
        cursor = 2
        for index in range(count):
            while not lines[cursor].strip():
                cursor += 1
            kpoints[index] = [float(value) for value in lines[cursor].split()]
            cursor += 1
            values: list[complex] = []
            for _ in range(rows * columns):
                real, imaginary = (float(value) for value in lines[cursor].split())
                values.append(complex(real, imaginary))
                cursor += 1
            matrices[index] = np.asarray(values).reshape((rows, columns), order="F")
        return kpoints, matrices

    @staticmethod
    def _center(marginal: RealArray, coordinate: RealArray, period: int) -> float:
        moment = np.sum(marginal * np.exp(2j * np.pi * coordinate / period))
        return float((np.angle(moment) % (2.0 * np.pi)) * period / (2.0 * np.pi))

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected an object")
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


class IndependentBasinControl:
    """Check exact symmetry and translation round trips independently."""

    __slots__ = ()

    _operations = (
        ((1, 0), (0, 1)),
        ((0, -1), (1, 0)),
        ((-1, 0), (0, -1)),
        ((0, 1), (-1, 0)),
        ((1, 0), (0, -1)),
        ((-1, 0), (0, 1)),
        ((0, 1), (1, 0)),
        ((0, -1), (-1, 0)),
    )
    _inverses = (0, 3, 2, 1, 4, 5, 6, 7)

    def execute(
        self, densities: tuple[RealArray, ...], mesh_size: int
    ) -> dict[str, float]:
        mismatches: list[float] = []
        for operation, inverse in enumerate(self._inverses):
            for density in densities:
                transformed = self._transform(density, operation)
                round_trip = self._transform(transformed, inverse)
                mismatches.append(self._mismatch(round_trip, density, mesh_size))
        permutation = (2, 0, 1)
        inverse_permutation = tuple(permutation.index(index) for index in range(3))
        permuted = tuple(densities[index] for index in permutation)
        restored = tuple(permuted[index] for index in inverse_permutation)
        mismatches.extend(
            self._mismatch(left, right, mesh_size)
            for left, right in zip(restored, densities, strict=True)
        )
        leakages: list[float] = []
        for translation in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            for density in densities:
                shifted, leakage = self._translate(density, translation, mesh_size)
                restored_density, inverse_leakage = self._translate(
                    shifted, (-translation[0], -translation[1]), mesh_size
                )
                leakages.extend((leakage, inverse_leakage))
                mismatches.append(self._mismatch(restored_density, density, mesh_size))
        return {
            "maximum_density_l2_round_trip_mismatch": max(mismatches),
            "maximum_fractional_translation_imaginary_leakage": max(leakages),
        }

    def _transform(self, density: RealArray, operation: int) -> RealArray:
        size = density.shape[0]
        rows, columns = np.indices((size, size))
        matrix = self._operations[operation]
        transformed_rows = (matrix[0][0] * rows + matrix[0][1] * columns) % size
        transformed_columns = (matrix[1][0] * rows + matrix[1][1] * columns) % size
        transformed = np.empty_like(density)
        transformed[transformed_rows, transformed_columns] = density
        return transformed

    @staticmethod
    def _translate(
        density: RealArray,
        translation: tuple[int, int],
        mesh_size: int,
    ) -> tuple[RealArray, float]:
        size = density.shape[0]
        frequency = np.fft.fftfreq(size)
        phase = np.exp(
            -2j
            * np.pi
            * (
                frequency[:, None] * translation[0] * size / mesh_size
                + frequency[None, :] * translation[1] * size / mesh_size
            )
        )
        translated = np.fft.ifft2(np.fft.fft2(density) * phase)
        return (
            np.asarray(np.real(translated), dtype=np.float64),
            float(np.max(np.abs(np.imag(translated)))),
        )

    @staticmethod
    def _mismatch(source: RealArray, target: RealArray, mesh_size: int) -> float:
        return float(
            np.linalg.norm(np.fft.fft2(source) - np.fft.fft2(target)) / mesh_size
        )


class StandaloneResultVerifier:
    """Verify native records, endpoint selection, summaries, and sampled grids."""

    __slots__ = ()

    _component_patterns = {
        "omega_i_cell_squared": r"Omega I\s+=\s+([^\s]+)",
        "omega_d_cell_squared": r"Omega D\s+=\s+([^\s]+)",
        "omega_od_cell_squared": r"Omega OD\s+=\s+([^\s]+)",
        "omega_total_cell_squared": r"Omega Total\s+=\s+([^\s]+)",
    }

    def execute(
        self, proposal_path: Path, execution_path: Path, result_path: Path
    ) -> None:
        proposal = self._load(proposal_path)
        execution = self._load(execution_path)
        result = self._load(result_path)
        provenance = self._mapping(result["provenance"])
        self._identity(
            proposal_path, self._string(provenance["proposal_sha256"]), "proposal"
        )
        self._identity(
            execution_path,
            self._string(provenance["execution_result_sha256"]),
            "execution result",
        )
        extractor = Path(self._string(provenance["extractor_path"]))
        self._identity(
            extractor, self._string(provenance["extractor_sha256"]), "extractor"
        )
        endpoints = [self._mapping(value) for value in self._array(result["endpoints"])]
        self._equal(len(endpoints), 256, "endpoint count")
        keys = {
            (
                self._string(value["configuration_id"]),
                self._string(value["arm"]),
                self._string(value["start_id"]),
            )
            for value in endpoints
        }
        self._equal(len(keys), 256, "unique endpoint count")
        initial = [
            self._mapping(value) for value in self._array(execution["localizations"])
        ]
        continuations = {
            (
                self._string(value["configuration_id"]),
                self._string(value["source_arm"]),
                self._string(value["start_id"]),
            ): value
            for value in (
                self._mapping(item) for item in self._array(execution["continuations"])
            )
        }
        initial_by_key = {
            (
                self._string(value["configuration_id"]),
                self._string(value["arm"]),
                self._string(value["start_id"]),
            ): value
            for value in initial
        }
        for endpoint in endpoints:
            key = (
                self._string(endpoint["configuration_id"]),
                self._string(endpoint["arm"]),
                self._string(endpoint["start_id"]),
            )
            initial_record = initial_by_key[key]
            continuation = continuations.get(key)
            expected_root = Path(
                self._string(
                    continuation["run_root"]
                    if continuation is not None
                    else initial_record["run_root"]
                )
            )
            if Path(self._string(endpoint["effective_run_root"])) != expected_root:
                raise AssertionError("effective endpoint selection disagrees")
            expected_convergence = (
                continuation["native_convergence_criterion_satisfied"]
                if continuation is not None
                else initial_record["native_convergence_criterion_satisfied"]
            )
            if endpoint["effective_native_converged"] is not expected_convergence:
                raise AssertionError("effective convergence status disagrees")
            self._verify_native(endpoint, expected_root)
            self._verify_tails(endpoint, expected_root)
        self._verify_summary(result, endpoints)
        self._verify_groups(result, endpoints)
        self._verify_basin_rejections(result, proposal)
        self._verify_common_samples(result, endpoints, execution_path.parent)

    def _verify_native(
        self, endpoint: dict[str, JsonValue], effective_root: Path
    ) -> None:
        text = (effective_root / "low_triple" / "low_triple.wout").read_text(
            encoding="utf-8"
        )
        final = text.rsplit("Final State", maxsplit=1)[1]
        native = self._mapping(endpoint["effective_native_endpoint"])
        for key, pattern in self._component_patterns.items():
            match = re.search(pattern, final)
            if match is None:
                raise ValueError(f"missing native component {key}")
            self._close(self._real(native[key]), float(match.group(1)), 0.0, key)
        self._close(
            self._real(native["omega_tilde_cell_squared"]),
            self._real(native["omega_d_cell_squared"])
            + self._real(native["omega_od_cell_squared"]),
            1.0e-15,
            "Omega tilde",
        )
        statement = "Wannierisation convergence criteria satisfied" in text
        if endpoint["effective_native_converged"] is not statement:
            raise AssertionError("native convergence statement disagrees")

    def _verify_tails(
        self, endpoint: dict[str, JsonValue], effective_root: Path
    ) -> None:
        blocks = self._hopping_blocks(
            effective_root / "low_triple" / "low_triple_hr.dat"
        )
        represented = self._mapping(endpoint["represented_endpoint"])
        for value in self._array(represented["hopping_tails"]):
            record = self._mapping(value)
            radius = self._integer(record["maximum_squared_radius"])
            expected = math.sqrt(
                sum(
                    float(np.linalg.norm(matrix) ** 2)
                    for (rx, ry), matrix in blocks.items()
                    if rx * rx + ry * ry > radius
                )
            )
            self._close(
                self._real(record["omitted_block_frobenius_l2_norm_energy_units"]),
                expected,
                1.0e-15,
                "hopping tail",
            )

    def _verify_summary(
        self, result: dict[str, JsonValue], endpoints: list[dict[str, JsonValue]]
    ) -> None:
        summary = self._mapping(result["execution_summary"])
        self._equal(
            self._integer(summary["initial_native_converged_count"]),
            sum(value["initial_native_converged"] is True for value in endpoints),
            "initial convergence count",
        )
        self._equal(
            self._integer(summary["effective_native_converged_count"]),
            sum(value["effective_native_converged"] is True for value in endpoints),
            "effective convergence count",
        )
        self._equal(
            self._integer(summary["effective_native_nonconverged_count"]),
            sum(value["effective_native_converged"] is False for value in endpoints),
            "effective nonconvergence count",
        )

    def _verify_groups(
        self, result: dict[str, JsonValue], endpoints: list[dict[str, JsonValue]]
    ) -> None:
        for value in self._array(result["groups"]):
            group = self._mapping(value)
            selected = [
                endpoint
                for endpoint in endpoints
                if endpoint["configuration_id"] == group["configuration_id"]
                and endpoint["arm"] == group["arm"]
            ]
            self._equal(len(selected), 16, "group start count")
            converged = [
                endpoint
                for endpoint in selected
                if endpoint["effective_native_converged"] is True
            ]
            self._equal(
                self._integer(group["effective_native_converged_count"]),
                len(converged),
                "group convergence count",
            )
            expected_best = min(
                converged,
                key=lambda endpoint: (
                    self._omega_tilde(endpoint),
                    self._string(endpoint["start_id"]),
                ),
            )
            best = self._mapping(group["best_observed_converged"])
            if best["start_id"] != expected_best["start_id"]:
                raise AssertionError("group best endpoint disagrees")
            basins = [
                self._mapping(item)
                for item in self._array(group["observed_density_d4_basins"])
            ]
            self._equal(
                sum(self._integer(basin["occupancy"]) for basin in basins),
                len(converged),
                "basin occupancy sum",
            )

    def _verify_basin_rejections(
        self, result: dict[str, JsonValue], proposal: dict[str, JsonValue]
    ) -> None:
        method = self._mapping(proposal["basin_method"])
        center_tolerance = self._real(method["center_set_periodic_tolerance_cell"])
        density_tolerance = self._real(method["maximum_matched_density_l2_mismatch"])
        for value in self._array(result["groups"]):
            group = self._mapping(value)
            basins = [
                self._mapping(basin)
                for basin in self._array(group["observed_density_d4_basins"])
            ]
            best_start = self._string(basins[0]["representative_start_id"])
            candidates: list[tuple[str, float, float]] = []
            for basin in basins:
                candidate_start = self._string(basin["representative_start_id"])
                for rejected_value in self._array(
                    basin["rejected_equivalence_candidates"]
                ):
                    rejected = self._mapping(rejected_value)
                    center = self._real(rejected["center_set_periodic_distance"])
                    density = self._real(rejected["maximum_density_l2_mismatch"])
                    if center <= center_tolerance and density <= density_tolerance:
                        raise AssertionError("basin classifier rejected a passing pair")
                    candidates.append(
                        (
                            candidate_start
                            if self._string(rejected["representative_start_id"])
                            == best_start
                            else "",
                            center,
                            density,
                        )
                    )
            sensitivity = [
                self._mapping(record)
                for record in self._array(group["density_tolerance_sensitivity"])
            ]
            for record in sensitivity:
                tolerance = self._real(record["density_l2_tolerance"])
                matching = [
                    candidate
                    for candidate in candidates
                    if candidate[1] <= center_tolerance and candidate[2] <= tolerance
                ]
                best_matches = [candidate for candidate in matching if candidate[0]]
                self._equal(
                    self._integer(record["direct_matching_pair_count"]),
                    len(matching),
                    "density sensitivity pair count",
                )
                self._equal(
                    self._integer(record["best_endpoint_direct_occupancy"]),
                    1 + len(best_matches),
                    "density sensitivity best occupancy",
                )

    def _verify_common_samples(
        self,
        result: dict[str, JsonValue],
        endpoints: list[dict[str, JsonValue]],
        external_root: Path,
    ) -> None:
        endpoint_by_key = {
            (
                self._string(value["configuration_id"]),
                self._string(value["arm"]),
                self._string(value["start_id"]),
            ): value
            for value in endpoints
        }
        estimator = IndependentCommonEstimator()
        control = IndependentBasinControl()
        sample_keys: set[tuple[str, str, str]] = set()
        group_by_best_key: dict[tuple[str, str, str], dict[str, JsonValue]] = {}
        for value in self._array(result["groups"]):
            group = self._mapping(value)
            best_key = (
                self._string(group["configuration_id"]),
                self._string(group["arm"]),
                self._string(
                    self._mapping(group["best_observed_converged"])["start_id"]
                ),
            )
            group_by_best_key[best_key] = group
            sample_keys.add(
                (
                    self._string(group["configuration_id"]),
                    self._string(group["arm"]),
                    self._string(
                        self._mapping(group["best_observed_converged"])["start_id"]
                    ),
                )
            )
            sample_keys.add(
                (
                    self._string(group["configuration_id"]),
                    self._string(group["arm"]),
                    self._string(
                        self._mapping(group["median_across_converged"])[
                            "center_medoid_start_id"
                        ]
                    ),
                )
            )
        for index, key in enumerate(sorted(sample_keys), start=1):
            endpoint = endpoint_by_key[key]
            controls = self._load(external_root / key[0] / "composite-input.json")
            seed_root = (
                Path(self._string(endpoint["effective_run_root"])) / "low_triple"
            )
            reconstructed = estimator.execute(controls, seed_root, 1024)
            represented = self._mapping(endpoint["represented_endpoint"])
            retained = [
                self._mapping(value)
                for value in self._array(represented["common_localization"])
            ]
            for actual_value, expected in zip(
                reconstructed.records, retained, strict=True
            ):
                actual = self._mapping(actual_value)
                if (
                    actual["density_content_sha256"]
                    != expected["density_content_sha256"]
                ):
                    raise AssertionError("sampled density identity disagrees")
                self._close(
                    self._real(actual["spread_cell_squared"]),
                    self._real(expected["spread_cell_squared"]),
                    1.0e-12,
                    "sampled common spread",
                )
                for left, right in zip(
                    self._reals(actual["center_supercell_cells"]),
                    self._reals(expected["center_supercell_cells"]),
                    strict=True,
                ):
                    self._close(left, right, 1.0e-12, "sampled common center")
            group = group_by_best_key.get(key)
            if group is not None:
                independent = control.execute(
                    reconstructed.densities,
                    self._integer(controls["reciprocal_mesh_size"]),
                )
                recorded = self._mapping(group["basin_post_hoc_numerical_controls"])
                density_tolerance = 1.0e-8
                if (
                    independent["maximum_density_l2_round_trip_mismatch"]
                    > density_tolerance
                    or self._real(recorded["maximum_density_l2_mismatch"])
                    > density_tolerance
                ):
                    raise AssertionError("exact basin controls exceed roundoff bound")
                if (
                    independent["maximum_fractional_translation_imaginary_leakage"]
                    > density_tolerance
                ):
                    raise AssertionError("fractional translation leakage is too large")
                if recorded["passes_frozen_center_tolerance"] is not True:
                    raise AssertionError("center control fails frozen tolerance")
                if recorded["passes_frozen_density_tolerance"] is not True:
                    raise AssertionError("density control fails frozen tolerance")
            print(
                f"common_estimator_sample={index}/{len(sample_keys)} "
                f"configuration={key[0]} arm={key[1]} start={key[2]}",
                flush=True,
            )

    def _hopping_blocks(self, path: Path) -> dict[tuple[int, int], ComplexArray]:
        lines = path.read_text(encoding="utf-8").splitlines()
        rank = int(lines[1])
        count = int(lines[2])
        degeneracies: list[int] = []
        cursor = 3
        while len(degeneracies) < count:
            degeneracies.extend(int(value) for value in lines[cursor].split())
            cursor += 1
        blocks: dict[tuple[int, int], ComplexArray] = {}
        for line in lines[cursor:]:
            rx, ry, rz, row, column, real, imaginary = line.split()
            if int(rz) != 0:
                raise AssertionError("inactive hopping is nonzero")
            matrix = blocks.setdefault(
                (int(rx), int(ry)), np.zeros((rank, rank), dtype=complex)
            )
            matrix[int(row) - 1, int(column) - 1] = complex(
                float(real), float(imaginary)
            )
        self._equal(len(blocks), count, "hopping block count")
        return blocks

    def _omega_tilde(self, endpoint: dict[str, JsonValue]) -> float:
        return self._real(
            self._mapping(endpoint["effective_native_endpoint"])[
                "omega_tilde_cell_squared"
            ]
        )

    @staticmethod
    def _identity(path: Path, expected: str, label: str) -> None:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={expected}"
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
    """Adapt exact retained paths to independent verification."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--proposal", type=Path, required=True)
        parser.add_argument("--execution-result", type=Path, required=True)
        parser.add_argument("--result", type=Path, required=True)
        arguments = parser.parse_args(argv)
        StandaloneResultVerifier().execute(
            cast(Path, arguments.proposal).resolve(),
            cast(Path, arguments.execution_result).resolve(),
            cast(Path, arguments.result).resolve(),
        )
        print("periodic_2d_standalone_result_verification=PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
