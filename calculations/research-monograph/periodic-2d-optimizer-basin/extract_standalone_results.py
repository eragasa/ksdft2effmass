#!/usr/bin/env python3
"""Extract the completed standalone optimizer-convergence study."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from execute_study import JsonValue

type ComplexArray = npt.NDArray[np.complex128]
type RealArray = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class RepresentedEndpoint:
    """Compact endpoint summary with ephemeral common-grid densities."""

    summary: dict[str, JsonValue]
    densities: tuple[RealArray, ...]


class NativeEndpointAction:
    """Extract spread components, centers, and terminal trace diagnostics."""

    __slots__ = ()

    _trace_pattern = re.compile(
        r"^\s*(\d+)\s+([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+"
        r"([-+0-9.Ee]+)\s+([-+0-9.Ee]+)\s+<-- CONV$",
        re.MULTILINE,
    )
    _center_pattern = re.compile(
        r"WF centre and spread\s+(\d+)\s+\(\s*([^,]+),\s*([^,]+),"
        r"\s*([^\)]+)\s*\)\s+([^\s]+)"
    )

    def execute(self, path: Path, converged: bool) -> dict[str, JsonValue]:
        text = path.read_text(encoding="utf-8")
        final = text.rsplit("Final State", maxsplit=1)[1]
        components = {
            name: self._component(final, pattern)
            for name, pattern in (
                ("omega_i_cell_squared", r"Omega I\s+=\s+([^\s]+)"),
                ("omega_d_cell_squared", r"Omega D\s+=\s+([^\s]+)"),
                ("omega_od_cell_squared", r"Omega OD\s+=\s+([^\s]+)"),
                ("omega_total_cell_squared", r"Omega Total\s+=\s+([^\s]+)"),
            )
        }
        components["omega_tilde_cell_squared"] = (
            components["omega_d_cell_squared"] + components["omega_od_cell_squared"]
        )
        centers: list[JsonValue] = []
        orbital_spreads: list[JsonValue] = []
        matches = self._center_pattern.findall(final)
        if len(matches) < 3:
            raise ValueError(f"final centers are absent from {path}")
        for orbital, x, y, z, spread in matches[:3]:
            if abs(float(z)) > 5.0e-7:
                raise ValueError("inactive center is nonzero")
            centers.append(
                {
                    "orbital": int(orbital) - 1,
                    "active_fractional": [float(x), float(y)],
                    "active_fractional_modulo_cell": [
                        float(x) % 1.0,
                        float(y) % 1.0,
                    ],
                }
            )
            orbital_spreads.append(float(spread))
        trace = [
            (
                int(match.group(1)),
                float(match.group(2)),
                float(match.group(3)),
                float(match.group(4)),
            )
            for match in self._trace_pattern.finditer(text)
        ]
        if not trace:
            raise ValueError(f"iteration trace is absent from {path}")
        tail = trace[-min(200, len(trace)) :]
        iterations = np.asarray([value[0] for value in tail], dtype=float)
        deltas = np.asarray([value[1] for value in tail], dtype=float)
        gradients = np.asarray([value[2] for value in tail], dtype=float)
        spreads = np.asarray([value[3] for value in tail], dtype=float)
        slope = float(np.polyfit(iterations, spreads, deg=1)[0])
        trend = slope * (iterations - np.mean(iterations)) + np.mean(spreads)
        detrended_rms = float(np.sqrt(np.mean((spreads - trend) ** 2)))
        median_delta = float(np.median(np.abs(deltas)))
        median_gradient = float(np.median(gradients))
        if converged:
            classification = "native_converged"
        elif median_delta <= 1.0e-8 and median_gradient <= 1.0e-3:
            classification = "near_stationary_without_window_convergence"
        elif slope < -1.0e-8:
            classification = "continuing_descent_at_iteration_limit"
        elif detrended_rms > 1.0e-5:
            classification = "oscillatory_or_stalled"
        else:
            classification = "stalled_or_nondescent"
        return {
            **components,
            "centers": centers,
            "orbital_spreads_cell_squared": orbital_spreads,
            "iterations": trace[-1][0],
            "trace_point_count": len(trace),
            "terminal_window_point_count": len(tail),
            "terminal_spread_slope_per_iteration": slope,
            "terminal_detrended_spread_rms": detrended_rms,
            "terminal_median_absolute_delta_spread": median_delta,
            "terminal_median_rms_gradient": median_gradient,
            "terminal_minimum_spread_cell_squared": float(np.min(spreads)),
            "terminal_maximum_spread_cell_squared": float(np.max(spreads)),
            "diagnostic_classification": classification,
            "classification_status": "exploratory descriptive diagnostic",
        }

    @staticmethod
    def _component(text: str, pattern: str) -> float:
        match = re.search(pattern, text)
        if match is None:
            raise ValueError(f"final spread component is absent: {pattern}")
        return float(match.group(1))


class CommonRepresentationAction:
    """Reconstruct common-grid densities, spreads, centers, and hopping tails."""

    __slots__ = ("_controls", "_fft_size", "_kpoints", "_raw_frames", "_indices")

    def __init__(
        self, controls: dict[str, JsonValue], reference_u_path: Path, fft_size: int
    ) -> None:
        self._controls = controls
        self._fft_size = fft_size
        self._kpoints, _ = self._u_matrices(reference_u_path)
        self._raw_frames = self._raw_frames_action(controls, self._kpoints)
        self._indices = self._coefficient_indices(controls, self._kpoints, fft_size)

    def execute(self, seed_root: Path) -> RepresentedEndpoint:
        kpoints, unitaries = self._u_matrices(seed_root / "low_triple_u.mat")
        if not np.array_equal(kpoints, self._kpoints):
            raise AssertionError(
                "endpoint k-points differ from configuration reference"
            )
        frames = self._raw_frames @ unitaries
        mesh_size = self._integer(self._controls["reciprocal_mesh_size"])
        coordinate = np.arange(self._fft_size, dtype=float) * (
            mesh_size / self._fft_size
        )
        localization: list[JsonValue] = []
        densities: list[RealArray] = []
        for orbital in range(3):
            coefficients = np.zeros(
                (self._fft_size, self._fft_size), dtype=np.complex128
            )
            coefficients.ravel()[self._indices] = (
                frames[:, :, orbital].ravel() / mesh_size
            )
            coefficient_norm = float(np.sum(np.abs(coefficients) ** 2))
            wave = np.fft.ifft2(coefficients) * self._fft_size**2
            probability = np.abs(wave) ** 2
            probability /= np.sum(probability)
            probability = np.asarray(probability, dtype=np.float64)
            probability.setflags(write=False)
            center_x = self._circular_center(
                np.sum(probability, axis=1), coordinate, mesh_size
            )
            center_y = self._circular_center(
                np.sum(probability, axis=0), coordinate, mesh_size
            )
            dx = (coordinate - center_x + mesh_size / 2.0) % mesh_size
            dx -= mesh_size / 2.0
            dy = (coordinate - center_y + mesh_size / 2.0) % mesh_size
            dy -= mesh_size / 2.0
            spread = float(np.sum(probability * (dx[:, None] ** 2 + dy[None, :] ** 2)))
            digest = hashlib.sha256(
                np.round(probability, 12).astype("<f8", copy=False).tobytes(order="C")
            ).hexdigest()
            localization.append(
                {
                    "orbital": orbital,
                    "coefficient_norm": coefficient_norm,
                    "center_supercell_cells": [center_x, center_y],
                    "center_modulo_cell": [center_x % 1.0, center_y % 1.0],
                    "spread_cell_squared": spread,
                    "density_content_sha256": digest,
                }
            )
            densities.append(probability)
        blocks = self._hopping_blocks(seed_root / "low_triple_hr.dat")
        tails: list[JsonValue] = []
        for radius in (8, 18):
            tail = math.sqrt(
                sum(
                    float(np.linalg.norm(matrix) ** 2)
                    for (rx, ry), matrix in blocks.items()
                    if rx * rx + ry * ry > radius
                )
            )
            tails.append(
                {
                    "maximum_squared_radius": radius,
                    "omitted_block_frobenius_l2_norm_energy_units": tail,
                }
            )
        return RepresentedEndpoint(
            summary={
                "common_finite_supercell_fft_size": self._fft_size,
                "common_localization": localization,
                "common_total_spread_cell_squared": sum(
                    self._real(self._mapping(value)["spread_cell_squared"])
                    for value in localization
                ),
                "hopping_tails": tails,
                "u_matrix_sha256": self._sha256(seed_root / "low_triple_u.mat"),
                "hr_sha256": self._sha256(seed_root / "low_triple_hr.dat"),
            },
            densities=tuple(densities),
        )

    def _raw_frames_action(
        self, controls: dict[str, JsonValue], kpoints: RealArray
    ) -> ComplexArray:
        potential = self._mapping(controls["potential"])
        cutoff = self._integer(controls["plane_wave_cutoff"])
        lambda_x = self._real(potential["lambda_x"])
        lambda_y = self._real(potential["lambda_y"])
        lambda_xy = self._real(potential["lambda_xy"])
        side = 2 * cutoff + 1
        dimension = side * side
        frames = np.empty((kpoints.shape[0], dimension, 3), dtype=np.complex128)
        indices = np.arange(-cutoff, cutoff + 1)
        p_grid, q_grid = np.meshgrid(indices, indices, indexing="ij")
        p_values = p_grid.ravel()
        q_values = q_grid.ravel()
        dp = p_values[:, None] - p_values[None, :]
        dq = q_values[:, None] - q_values[None, :]
        for index, (kx, ky, _) in enumerate(kpoints):
            operator = np.diag((kx + p_values) ** 2 + (ky + q_values) ** 2).astype(
                np.complex128
            )
            operator += (lambda_x / 2.0) * ((np.abs(dp) == 1) & (dq == 0))
            operator += (lambda_y / 2.0) * ((dp == 0) & (np.abs(dq) == 1))
            operator += (lambda_xy / 4.0) * ((np.abs(dp) == 1) & (np.abs(dq) == 1))
            _, vectors = np.linalg.eigh(operator)
            frames[index] = vectors[:, :3]
        return frames

    def _coefficient_indices(
        self, controls: dict[str, JsonValue], kpoints: RealArray, fft_size: int
    ) -> npt.NDArray[np.int64]:
        cutoff = self._integer(controls["plane_wave_cutoff"])
        mesh_size = self._integer(controls["reciprocal_mesh_size"])
        plane = np.arange(-cutoff, cutoff + 1)
        p_grid, q_grid = np.meshgrid(plane, plane, indexing="ij")
        p_values = p_grid.ravel()
        q_values = q_grid.ravel()
        records: list[npt.NDArray[np.int64]] = []
        for kx, ky, _ in kpoints:
            ix = int(round(float(kx) * mesh_size)) % mesh_size
            iy = int(round(float(ky) * mesh_size)) % mesh_size
            x = (p_values * mesh_size + ix) % fft_size
            y = (q_values * mesh_size + iy) % fft_size
            records.append((x * fft_size + y).astype(np.int64))
        flattened = np.concatenate(records)
        if len(set(int(value) for value in flattened)) != flattened.size:
            raise AssertionError("common-grid coefficient indices collide")
        return flattened

    @staticmethod
    def _circular_center(
        marginal: RealArray, coordinate: RealArray, period: int
    ) -> float:
        moment = np.sum(marginal * np.exp(2j * np.pi * coordinate / period))
        return float((np.angle(moment) % (2.0 * np.pi)) * period / (2.0 * np.pi))

    def _u_matrices(self, path: Path) -> tuple[RealArray, ComplexArray]:
        lines = path.read_text(encoding="utf-8").splitlines()
        count, rows, columns = (int(value) for value in lines[1].split())
        if rows != 3 or columns != 3:
            raise ValueError("expected rank-three U matrices")
        kpoints = np.empty((count, 3), dtype=np.float64)
        matrices = np.empty((count, rows, columns), dtype=np.complex128)
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

    def _hopping_blocks(self, path: Path) -> dict[tuple[int, int], ComplexArray]:
        lines = path.read_text(encoding="utf-8").splitlines()
        rank = int(lines[1])
        count = int(lines[2])
        degeneracies: list[int] = []
        cursor = 3
        while len(degeneracies) < count:
            degeneracies.extend(int(value) for value in lines[cursor].split())
            cursor += 1
        if any(value != 1 for value in degeneracies):
            raise ValueError("expected unit Wigner-Seitz degeneracies")
        blocks: dict[tuple[int, int], ComplexArray] = {}
        for line in lines[cursor:]:
            rx, ry, rz, row, column, real, imaginary = line.split()
            if int(rz) != 0:
                raise ValueError("inactive-direction hopping must vanish")
            key = (int(rx), int(ry))
            matrix = blocks.setdefault(key, np.zeros((rank, rank), dtype=np.complex128))
            matrix[int(row) - 1, int(column) - 1] = complex(
                float(real), float(imaginary)
            )
        if len(blocks) != count:
            raise ValueError("hopping block count mismatch")
        return blocks

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

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


class DensityAwareBasinAction:
    """Classify converged endpoints under permutation, wrapping, and D4."""

    __slots__ = ("_spread_tolerance", "_center_tolerance", "_density_tolerance")

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

    def __init__(self, proposal: dict[str, JsonValue]) -> None:
        method = self._mapping(proposal["basin_method"])
        self._spread_tolerance = self._real(
            method["spread_absolute_tolerance_cell_squared"]
        )
        self._center_tolerance = self._real(
            method["center_set_periodic_tolerance_cell"]
        )
        self._density_tolerance = self._real(
            method["maximum_matched_density_l2_mismatch"]
        )

    def execute(
        self, endpoints: list[RepresentedEndpoint], mesh_size: int
    ) -> list[JsonValue]:
        basins: list[dict[str, JsonValue]] = []
        representatives: list[RepresentedEndpoint] = []
        ordered = sorted(
            endpoints,
            key=lambda value: (
                self._omega_tilde(value.summary),
                self._string(value.summary["start_id"]),
            ),
        )
        for endpoint in ordered:
            match_index: int | None = None
            match_diagnostics: dict[str, JsonValue] | None = None
            rejected_candidates: list[JsonValue] = []
            for index, representative in enumerate(representatives):
                if (
                    abs(
                        self._omega_tilde(endpoint.summary)
                        - self._omega_tilde(representative.summary)
                    )
                    > self._spread_tolerance
                ):
                    continue
                diagnostics = self._equivalence(endpoint, representative, mesh_size)
                if (
                    self._real(diagnostics["center_set_periodic_distance"])
                    <= self._center_tolerance
                    and self._real(diagnostics["maximum_density_l2_mismatch"])
                    <= self._density_tolerance
                ):
                    match_index = index
                    match_diagnostics = diagnostics
                    break
                rejected_candidates.append(
                    {
                        "representative_start_id": representative.summary["start_id"],
                        **diagnostics,
                    }
                )
            if match_index is None:
                representatives.append(endpoint)
                start_id = self._string(endpoint.summary["start_id"])
                basins.append(
                    {
                        "basin_id": f"density_d4_basin_{len(basins) + 1:02d}",
                        "representative_start_id": start_id,
                        "representative_omega_tilde_cell_squared": (
                            self._omega_tilde(endpoint.summary)
                        ),
                        "start_ids": [start_id],
                        "occupancy": 1,
                        "start_blocks_present": [self._start_block(start_id)],
                        "member_equivalence_diagnostics": [],
                        "rejected_equivalence_candidates": rejected_candidates,
                    }
                )
            else:
                basin = basins[match_index]
                start_id = self._string(endpoint.summary["start_id"])
                self._array(basin["start_ids"]).append(start_id)
                basin["occupancy"] = self._integer(basin["occupancy"]) + 1
                block = self._start_block(start_id)
                blocks = self._array(basin["start_blocks_present"])
                if block not in blocks:
                    blocks.append(block)
                if match_diagnostics is None:
                    raise AssertionError("matched basin lacks diagnostics")
                self._array(basin["member_equivalence_diagnostics"]).append(
                    {"start_id": start_id, **match_diagnostics}
                )
        for basin in basins:
            blocks = sorted(self._integers(basin["start_blocks_present"]))
            basin["start_blocks_present"] = blocks
            basin["appears_in_both_start_blocks"] = blocks == [0, 1]
        return cast(list[JsonValue], basins)

    def post_hoc_numerical_controls(
        self, endpoint: RepresentedEndpoint, mesh_size: int
    ) -> dict[str, JsonValue]:
        """Measure roundoff on exact equivalence controls after execution."""
        records: list[dict[str, JsonValue]] = []
        identity = self._equivalence(endpoint, endpoint, mesh_size)
        records.append({"control": "identity", **identity})
        for operation in range(8):
            transformed = self._transformed_endpoint(endpoint, operation)
            records.append(
                {
                    "control": f"d4_operation_{operation}",
                    **self._equivalence(transformed, endpoint, mesh_size),
                }
            )
        permutation = (2, 0, 1)
        permuted = self._permuted_endpoint(endpoint, permutation)
        records.append(
            {
                "control": "orbital_permutation_2_0_1",
                **self._equivalence(permuted, endpoint, mesh_size),
            }
        )
        imaginary_leakage: list[float] = []
        for translation in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            translated, leakage = self._translated_endpoint(
                endpoint, translation, mesh_size
            )
            imaginary_leakage.append(leakage)
            records.append(
                {
                    "control": (
                        f"integer_translation_{translation[0]}_{translation[1]}"
                    ),
                    **self._equivalence(translated, endpoint, mesh_size),
                }
            )
        maximum_center = max(
            self._real(record["center_set_periodic_distance"]) for record in records
        )
        maximum_density = max(
            self._real(record["maximum_density_l2_mismatch"]) for record in records
        )
        return {
            "status": (
                "post-hoc protocol-deviation control; this does not retroactively "
                "satisfy the planned pre-execution check"
            ),
            "control_count": len(records),
            "records": cast(list[JsonValue], records),
            "maximum_center_set_periodic_distance_cell": maximum_center,
            "maximum_density_l2_mismatch": maximum_density,
            "maximum_fractional_translation_imaginary_leakage": max(imaginary_leakage),
            "passes_frozen_center_tolerance": maximum_center <= self._center_tolerance,
            "passes_frozen_density_tolerance": maximum_density
            <= self._density_tolerance,
        }

    def density_tolerance_sensitivity(self, basins: list[JsonValue]) -> list[JsonValue]:
        """Count direct pair matches under several density tolerances."""
        if any(
            self._integer(self._mapping(value)["occupancy"]) != 1 for value in basins
        ):
            raise AssertionError("sensitivity requires singleton frozen basins")
        best_start = self._string(self._mapping(basins[0])["representative_start_id"])
        candidates: list[tuple[str, float, float]] = []
        for basin_value in basins:
            basin = self._mapping(basin_value)
            candidate_start = self._string(basin["representative_start_id"])
            for rejected_value in self._array(basin["rejected_equivalence_candidates"]):
                rejected = self._mapping(rejected_value)
                candidates.append(
                    (
                        candidate_start,
                        self._real(rejected["center_set_periodic_distance"]),
                        self._real(rejected["maximum_density_l2_mismatch"]),
                    )
                    if self._string(rejected["representative_start_id"]) == best_start
                    else (
                        "",
                        self._real(rejected["center_set_periodic_distance"]),
                        self._real(rejected["maximum_density_l2_mismatch"]),
                    )
                )
        records: list[JsonValue] = []
        for tolerance in (1.0e-6, 5.0e-6, 1.0e-5, 2.0e-5, 2.5e-5, 5.0e-5, 1.0e-4):
            matching = [
                value
                for value in candidates
                if value[1] <= self._center_tolerance and value[2] <= tolerance
            ]
            best_matches = [value for value in matching if value[0]]
            records.append(
                {
                    "density_l2_tolerance": tolerance,
                    "direct_matching_pair_count": len(matching),
                    "best_endpoint_direct_occupancy": 1 + len(best_matches),
                    "best_endpoint_direct_match_start_ids": [
                        value[0] for value in best_matches
                    ],
                }
            )
        return records

    def center_distance(self, first: JsonValue, second: JsonValue) -> float:
        left = self._center_values(first)
        right = self._center_values(second)
        return min(
            self._center_assignment_distance(
                self._transform_centers(left, operation, modulo_cell=True), right
            )[0]
            for operation in range(8)
        )

    def _equivalence(
        self,
        first: RepresentedEndpoint,
        second: RepresentedEndpoint,
        mesh_size: int,
    ) -> dict[str, JsonValue]:
        left_native = self._center_values(first.summary["native_centers_modulo_cell"])
        right_native = self._center_values(second.summary["native_centers_modulo_cell"])
        left_common = self._common_centers(first.summary)
        right_common = self._common_centers(second.summary)
        best: tuple[float, float, int, tuple[int, ...]] | None = None
        for operation in range(8):
            transformed_native = self._transform_centers(
                left_native, operation, modulo_cell=True
            )
            center_distance, permutation = self._center_assignment_distance(
                transformed_native, right_native
            )
            if center_distance > self._center_tolerance:
                continue
            transformed_common = self._transform_centers(
                left_common, operation, modulo_cell=False
            )
            mismatches: list[float] = []
            for source_index, target_index in enumerate(permutation):
                transformed_density = self._transform_density(
                    first.densities[source_index], operation
                )
                source_center = transformed_common[source_index]
                target_center = right_common[target_index]
                translation = (
                    round(target_center[0] - source_center[0]),
                    round(target_center[1] - source_center[1]),
                )
                mismatches.append(
                    self._density_l2(
                        transformed_density,
                        second.densities[target_index],
                        translation,
                        mesh_size,
                    )
                )
            maximum = max(mismatches)
            candidate = (center_distance, maximum, operation, permutation)
            if best is None or (candidate[1], candidate[0]) < (best[1], best[0]):
                best = candidate
        if best is None:
            return {
                "center_set_periodic_distance": math.inf,
                "maximum_density_l2_mismatch": math.inf,
                "d4_operation": None,
                "orbital_permutation": None,
            }
        return {
            "center_set_periodic_distance": best[0],
            "maximum_density_l2_mismatch": best[1],
            "d4_operation": best[2],
            "orbital_permutation": list(best[3]),
        }

    def _transformed_endpoint(
        self, endpoint: RepresentedEndpoint, operation: int
    ) -> RepresentedEndpoint:
        native = self._transform_centers(
            self._center_values(endpoint.summary["native_centers_modulo_cell"]),
            operation,
            modulo_cell=True,
        )
        common = self._transform_centers(
            self._common_centers(endpoint.summary), operation, modulo_cell=False
        )
        return self._control_endpoint(
            native,
            common,
            tuple(
                self._transform_density(density, operation)
                for density in endpoint.densities
            ),
        )

    def _permuted_endpoint(
        self, endpoint: RepresentedEndpoint, permutation: tuple[int, ...]
    ) -> RepresentedEndpoint:
        native = self._center_values(endpoint.summary["native_centers_modulo_cell"])
        common = self._common_centers(endpoint.summary)
        return self._control_endpoint(
            [native[index] for index in permutation],
            [common[index] for index in permutation],
            tuple(endpoint.densities[index] for index in permutation),
        )

    def _translated_endpoint(
        self,
        endpoint: RepresentedEndpoint,
        translation: tuple[int, int],
        mesh_size: int,
    ) -> tuple[RepresentedEndpoint, float]:
        native = self._center_values(endpoint.summary["native_centers_modulo_cell"])
        common = [
            (x + translation[0], y + translation[1])
            for x, y in self._common_centers(endpoint.summary)
        ]
        densities: list[RealArray] = []
        leakage: list[float] = []
        for density in endpoint.densities:
            shifted, imaginary = self._fractional_translate_density(
                density, translation, mesh_size
            )
            densities.append(shifted)
            leakage.append(imaginary)
        return self._control_endpoint(native, common, tuple(densities)), max(leakage)

    def _fractional_translate_density(
        self,
        density: RealArray,
        translation_cells: tuple[int, int],
        mesh_size: int,
    ) -> tuple[RealArray, float]:
        size = density.shape[0]
        frequency = np.fft.fftfreq(size)
        shift_x = translation_cells[0] * size / mesh_size
        shift_y = translation_cells[1] * size / mesh_size
        phase = np.exp(
            -2j * np.pi * (frequency[:, None] * shift_x + frequency[None, :] * shift_y)
        )
        shifted_complex = np.fft.ifft2(np.fft.fft2(density) * phase)
        leakage = float(np.max(np.abs(np.imag(shifted_complex))))
        shifted = np.asarray(np.real(shifted_complex), dtype=np.float64)
        shifted.setflags(write=False)
        return shifted, leakage

    @staticmethod
    def _control_endpoint(
        native_centers: list[tuple[float, float]],
        common_centers: list[tuple[float, float]],
        densities: tuple[RealArray, ...],
    ) -> RepresentedEndpoint:
        return RepresentedEndpoint(
            summary={
                "native_centers_modulo_cell": [[x, y] for x, y in native_centers],
                "represented_endpoint": {
                    "common_localization": [
                        {"center_supercell_cells": [x, y]} for x, y in common_centers
                    ]
                },
            },
            densities=densities,
        )

    def _density_l2(
        self,
        source: RealArray,
        target: RealArray,
        translation_cells: tuple[int, int],
        mesh_size: int,
    ) -> float:
        size = source.shape[0]
        source_fourier = np.fft.fft2(source)
        target_fourier = np.fft.fft2(target)
        frequency = np.fft.fftfreq(size)
        shift_x = translation_cells[0] * size / mesh_size
        shift_y = translation_cells[1] * size / mesh_size
        phase = np.exp(
            -2j * np.pi * (frequency[:, None] * shift_x + frequency[None, :] * shift_y)
        )
        return float(
            np.linalg.norm(source_fourier * phase - target_fourier) / mesh_size
        )

    def _transform_density(self, density: RealArray, operation: int) -> RealArray:
        size = density.shape[0]
        ii, jj = np.indices((size, size))
        matrix = self._operations[operation]
        ip = (matrix[0][0] * ii + matrix[0][1] * jj) % size
        jp = (matrix[1][0] * ii + matrix[1][1] * jj) % size
        transformed = np.empty_like(density)
        transformed[ip, jp] = density
        return transformed

    def _transform_centers(
        self,
        centers: list[tuple[float, float]],
        operation: int,
        *,
        modulo_cell: bool,
    ) -> list[tuple[float, float]]:
        matrix = self._operations[operation]
        transformed = [
            (
                matrix[0][0] * x + matrix[0][1] * y,
                matrix[1][0] * x + matrix[1][1] * y,
            )
            for x, y in centers
        ]
        if modulo_cell:
            return [(x % 1.0, y % 1.0) for x, y in transformed]
        return transformed

    def _center_assignment_distance(
        self, first: list[tuple[float, float]], second: list[tuple[float, float]]
    ) -> tuple[float, tuple[int, ...]]:
        return min(
            (
                max(
                    self._periodic_distance(first[index], second[target])
                    for index, target in enumerate(permutation)
                ),
                permutation,
            )
            for permutation in itertools.permutations(range(len(second)))
        )

    @staticmethod
    def _periodic_distance(
        first: tuple[float, float], second: tuple[float, float]
    ) -> float:
        differences = [
            min(abs(left - right), 1.0 - abs(left - right))
            for left, right in zip(first, second, strict=True)
        ]
        return math.sqrt(sum(value * value for value in differences))

    def _common_centers(
        self, summary: dict[str, JsonValue]
    ) -> list[tuple[float, float]]:
        represented = self._mapping(summary["represented_endpoint"])
        return [
            self._reals(self._mapping(value)["center_supercell_cells"])
            for value in self._array(represented["common_localization"])
        ]

    def _center_values(self, value: JsonValue) -> list[tuple[float, float]]:
        return [self._reals(item) for item in self._array(value)]

    def _omega_tilde(self, summary: dict[str, JsonValue]) -> float:
        native = self._mapping(summary["effective_native_endpoint"])
        return self._real(native["omega_tilde_cell_squared"])

    @staticmethod
    def _start_block(start_id: str) -> int:
        index = 0 if start_id == "identity" else int(start_id.rsplit("_", 1)[1])
        return 0 if index <= 7 else 1

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

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        return tuple(self._integer(item) for item in self._array(value))

    def _reals(self, value: JsonValue) -> tuple[float, float]:
        values = self._array(value)
        if len(values) != 2:
            raise ValueError("expected an active-plane pair")
        return self._real(values[0]), self._real(values[1])


class StandaloneResultExtractor:
    """Extract endpoints and evaluate the frozen standalone-study criteria."""

    __slots__ = ()

    def execute(
        self,
        proposal_path: Path,
        execution_path: Path,
        output_path: Path,
    ) -> dict[str, JsonValue]:
        proposal = self._load(proposal_path)
        execution = self._load(execution_path)
        if execution["stopped_early"] is not False:
            raise AssertionError("standalone execution is incomplete")
        initial = [
            self._mapping(value) for value in self._array(execution["localizations"])
        ]
        continuations = {
            self._continuation_key(self._mapping(value)): self._mapping(value)
            for value in self._array(execution["continuations"])
        }
        configuration_by_id = {
            self._string(self._mapping(value)["configuration_id"]): self._mapping(value)
            for value in self._array(proposal["baseline_configurations"])
        }
        grouped: dict[tuple[str, str], list[dict[str, JsonValue]]] = {}
        for record in initial:
            key = (
                self._string(record["configuration_id"]),
                self._string(record["arm"]),
            )
            grouped.setdefault(key, []).append(record)
        native_action = NativeEndpointAction()
        basin_action = DensityAwareBasinAction(proposal)
        group_results: list[JsonValue] = []
        all_endpoint_results: list[JsonValue] = []
        representation_cache: dict[str, CommonRepresentationAction] = {}
        for group_index, ((configuration_id, arm), records) in enumerate(
            sorted(grouped.items()), start=1
        ):
            print(
                f"[{group_index}/{len(grouped)}] extracting "
                f"configuration={configuration_id} arm={arm}",
                flush=True,
            )
            configuration = configuration_by_id[configuration_id]
            external_root = execution_path.parent / configuration_id
            controls = self._load(external_root / "composite-input.json")
            reference_root = Path(self._string(records[0]["run_root"])) / "low_triple"
            representation = representation_cache.get(configuration_id)
            if representation is None:
                representation = CommonRepresentationAction(
                    controls,
                    reference_root / "low_triple_u.mat",
                    self._integer(
                        self._mapping(proposal["represented_diagnostics"])[
                            "common_finite_supercell_fft_size"
                        ]
                    ),
                )
                representation_cache[configuration_id] = representation
            endpoints: list[RepresentedEndpoint] = []
            for start_index, initial_record in enumerate(
                sorted(records, key=lambda value: self._start_index(value)), start=1
            ):
                start_id = self._string(initial_record["start_id"])
                key = (configuration_id, arm, start_id)
                continuation = continuations.get(key)
                initial_root = Path(self._string(initial_record["run_root"]))
                initial_native = native_action.execute(
                    initial_root / "low_triple" / "low_triple.wout",
                    initial_record["native_convergence_criterion_satisfied"] is True,
                )
                continuation_native: dict[str, JsonValue] | None = None
                if continuation is not None:
                    continuation_root = Path(self._string(continuation["run_root"]))
                    continuation_native = native_action.execute(
                        continuation_root / "low_triple" / "low_triple.wout",
                        continuation["native_convergence_criterion_satisfied"] is True,
                    )
                    effective_root = continuation_root
                    effective_converged = (
                        continuation["native_convergence_criterion_satisfied"] is True
                    )
                else:
                    effective_root = initial_root
                    effective_converged = (
                        initial_record["native_convergence_criterion_satisfied"] is True
                    )
                represented = representation.execute(effective_root / "low_triple")
                effective_native = (
                    continuation_native
                    if continuation_native is not None
                    else initial_native
                )
                summary: dict[str, JsonValue] = {
                    "configuration_id": configuration_id,
                    "arm": arm,
                    "start_id": start_id,
                    "start_index": self._start_index(initial_record),
                    "initial_process_completed": initial_record["process_completed"],
                    "initial_native_converged": initial_record[
                        "native_convergence_criterion_satisfied"
                    ],
                    "continuation_applied": continuation is not None,
                    "continuation_native_converged": (
                        continuation["native_convergence_criterion_satisfied"]
                        if continuation is not None
                        else None
                    ),
                    "effective_native_converged": effective_converged,
                    "initial_native_endpoint": initial_native,
                    "continuation_native_endpoint": continuation_native,
                    "effective_native_endpoint": effective_native,
                    "effective_total_iterations": self._integer(
                        initial_native["iterations"]
                    )
                    + (
                        self._integer(continuation_native["iterations"])
                        if continuation_native is not None
                        else 0
                    ),
                    "effective_run_root": str(effective_root),
                    "represented_endpoint": represented.summary,
                }
                summary["native_centers_modulo_cell"] = [
                    self._mapping(value)["active_fractional_modulo_cell"]
                    for value in self._array(effective_native["centers"])
                ]
                if continuation_native is not None:
                    summary["continuation_change"] = {
                        "omega_tilde_change_cell_squared": self._real(
                            continuation_native["omega_tilde_cell_squared"]
                        )
                        - self._real(initial_native["omega_tilde_cell_squared"]),
                        "omega_total_change_cell_squared": self._real(
                            continuation_native["omega_total_cell_squared"]
                        )
                        - self._real(initial_native["omega_total_cell_squared"]),
                        "native_center_set_d4_periodic_distance": (
                            basin_action.center_distance(
                                summary["native_centers_modulo_cell"],
                                [
                                    self._mapping(value)[
                                        "active_fractional_modulo_cell"
                                    ]
                                    for value in self._array(initial_native["centers"])
                                ],
                            )
                        ),
                    }
                endpoint = RepresentedEndpoint(summary, represented.densities)
                endpoints.append(endpoint)
                all_endpoint_results.append(summary)
                print(
                    f"  [{start_index}/{len(records)}] start={start_id} "
                    f"initial_converged={summary['initial_native_converged']} "
                    f"continued={summary['continuation_applied']} "
                    f"final_converged={effective_converged}",
                    flush=True,
                )
            converged = [
                endpoint
                for endpoint in endpoints
                if endpoint.summary["effective_native_converged"] is True
            ]
            basins = basin_action.execute(
                converged, self._integer(configuration["reciprocal_mesh_size"])
            )
            group_results.append(
                self._group_summary(configuration, arm, endpoints, basins, basin_action)
            )
        groups_by_key = {
            (
                self._string(self._mapping(value)["configuration_id"]),
                self._string(self._mapping(value)["arm"]),
            ): self._mapping(value)
            for value in group_results
        }
        assessment = self._assessment(proposal, groups_by_key, basin_action)
        diagnostic_counts = Counter(
            self._string(
                self._mapping(self._mapping(value)["effective_native_endpoint"])[
                    "diagnostic_classification"
                ]
            )
            for value in all_endpoint_results
            if self._mapping(value)["effective_native_converged"] is False
        )
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": self._string(proposal["proposal_id"]),
            "evidence_status": "calculated synthetic non-DFT numerical verification",
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "authorization_checkpoints": [
                "RM-PERIODIC-2D-STANDALONE-EXECUTION-HC09",
                "RM-PERIODIC-2D-STANDALONE-CONTINUATION-RESUME-HC10",
            ],
            "provenance": {
                "proposal_path": str(proposal_path),
                "proposal_sha256": self._sha256(proposal_path),
                "execution_result_path": str(execution_path),
                "execution_result_sha256": self._sha256(execution_path),
                "extractor_path": str(Path(__file__).resolve()),
                "extractor_sha256": self._sha256(Path(__file__).resolve()),
            },
            "execution_summary": {
                "initial_localization_count": len(initial),
                "initial_process_completion_count": sum(
                    value["process_completed"] is True for value in initial
                ),
                "initial_native_converged_count": sum(
                    value["native_convergence_criterion_satisfied"] is True
                    for value in initial
                ),
                "continuation_count": len(continuations),
                "continuation_native_converged_count": sum(
                    value["native_convergence_criterion_satisfied"] is True
                    for value in continuations.values()
                ),
                "effective_native_converged_count": sum(
                    self._mapping(value)["effective_native_converged"] is True
                    for value in all_endpoint_results
                ),
                "effective_native_nonconverged_count": sum(
                    self._mapping(value)["effective_native_converged"] is False
                    for value in all_endpoint_results
                ),
                "effective_nonconvergence_diagnostic_counts": dict(
                    sorted(diagnostic_counts.items())
                ),
                "cumulative_execution_seconds": execution["elapsed_seconds"],
                "external_output_bytes": execution["external_output_bytes"],
            },
            "groups": group_results,
            "endpoints": all_endpoint_results,
            "convergence_assessment": assessment,
            "analysis_contract": {
                "effective_endpoint": (
                    "initial endpoint when natively converged; otherwise the exact "
                    "retained continuation endpoint, whether converged or not"
                ),
                "common_finite_supercell_fft_size": 1024,
                "hopping_shell_squared_radii": [8, 18],
                "basin_objective": "Omega_D+Omega_OD",
                "basin_equivalence": (
                    "spread, orbital permutation, periodic lattice translation, "
                    "eight D4 operations, and matched active-plane density"
                ),
                "density_l2_definition": (
                    "continuous-grid L2 norm reconstructed by Parseval after the "
                    "matched D4 operation and integer-cell Fourier translation"
                ),
                "basin_tolerance_control_status": (
                    "planned pre-execution control lacks a retained record; post-hoc "
                    "exact-equivalence and threshold-sensitivity controls are "
                    "reported without retroactive compliance"
                ),
                "density_tolerance_sensitivity_values": [
                    1.0e-6,
                    5.0e-6,
                    1.0e-5,
                    2.0e-5,
                    2.5e-5,
                    5.0e-5,
                    1.0e-4,
                ],
                "nonconvergence_trace_classes_are_exploratory": True,
            },
            "claim_boundary": proposal["claim_boundary"],
        }
        output_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return payload

    def _group_summary(
        self,
        configuration: dict[str, JsonValue],
        arm: str,
        endpoints: list[RepresentedEndpoint],
        basins: list[JsonValue],
        basin_action: DensityAwareBasinAction,
    ) -> dict[str, JsonValue]:
        converged = [
            endpoint
            for endpoint in endpoints
            if endpoint.summary["effective_native_converged"] is True
        ]
        if not converged:
            raise AssertionError("group has no converged endpoint")
        best = min(
            converged,
            key=lambda value: (
                self._omega_tilde(value.summary),
                self._string(value.summary["start_id"]),
            ),
        )
        medoid = min(
            converged,
            key=lambda candidate: sum(
                basin_action.center_distance(
                    candidate.summary["native_centers_modulo_cell"],
                    other.summary["native_centers_modulo_cell"],
                )
                for other in converged
            ),
        )
        values = [endpoint.summary for endpoint in converged]
        best_basin = self._mapping(basins[0])
        method_pass = (
            self._integer(best_basin["occupancy"]) >= 4
            and best_basin["appears_in_both_start_blocks"] is True
        )
        return {
            "configuration_id": configuration["configuration_id"],
            "arm": arm,
            "axes": configuration["axes"],
            "plane_wave_cutoff": configuration["plane_wave_cutoff"],
            "reciprocal_mesh_size": configuration["reciprocal_mesh_size"],
            "transverse_lattice_length": configuration["transverse_lattice_length"],
            "start_count": len(endpoints),
            "initial_native_converged_count": sum(
                endpoint.summary["initial_native_converged"] is True
                for endpoint in endpoints
            ),
            "effective_native_converged_count": len(converged),
            "effective_native_converged_fraction": len(converged) / len(endpoints),
            "effective_nonconverged_start_ids": [
                endpoint.summary["start_id"]
                for endpoint in endpoints
                if endpoint.summary["effective_native_converged"] is False
            ],
            "observed_density_d4_basins": basins,
            "observed_density_d4_basin_count": len(basins),
            "best_basin_criterion_pass": method_pass,
            "basin_post_hoc_numerical_controls": (
                basin_action.post_hoc_numerical_controls(
                    best, self._integer(configuration["reciprocal_mesh_size"])
                )
            ),
            "density_tolerance_sensitivity": (
                basin_action.density_tolerance_sensitivity(basins)
            ),
            "best_observed_converged": self._compact(best.summary),
            "median_across_converged": {
                "omega_i_cell_squared": self._median_native(
                    values, "omega_i_cell_squared"
                ),
                "omega_tilde_cell_squared": self._median_native(
                    values, "omega_tilde_cell_squared"
                ),
                "omega_total_cell_squared": self._median_native(
                    values, "omega_total_cell_squared"
                ),
                "radius_18_hopping_tail_energy_units": self._median_tail(values, 18),
                "center_medoid_start_id": medoid.summary["start_id"],
                "native_centers_modulo_cell_medoid": medoid.summary[
                    "native_centers_modulo_cell"
                ],
            },
        }

    def _assessment(
        self,
        proposal: dict[str, JsonValue],
        groups: dict[tuple[str, str], dict[str, JsonValue]],
        basin_action: DensityAwareBasinAction,
    ) -> dict[str, JsonValue]:
        method = self._mapping(proposal["convergence_method"])
        baseline = {
            identifier: groups[(identifier, "baseline_preconditioned")]
            for identifier in {
                self._string(self._mapping(value)["configuration_id"])
                for value in self._array(proposal["baseline_configurations"])
            }
        }
        fixed_ids = [f"fixed_c31_p4_n{size}" for size in (11, 15, 19, 23, 27, 31)]
        balanced_ids = [
            "balanced_p4_n11_c11",
            "balanced_p4_n15_c15",
            "balanced_p4_n19_c19",
            "balanced_p4_n23_c23",
            "balanced_p4_n27_c27",
            "fixed_c31_p4_n31",
        ]
        cutoff_ids = [
            "fixed_c31_p3_n23",
            "fixed_c31_p4_n23",
            "fixed_c31_p5_n23",
            "fixed_c31_p6_n23",
        ]
        fixed_pair = self._pair_assessment(
            baseline["fixed_c31_p4_n27"],
            baseline["fixed_c31_p4_n31"],
            method,
            basin_action,
        )
        cutoff_pair = self._pair_assessment(
            baseline["fixed_c31_p5_n23"],
            baseline["fixed_c31_p6_n23"],
            method,
            basin_action,
        )
        holdout = self._holdout(
            [baseline[identifier] for identifier in fixed_ids], method
        )
        embedding = [
            self._embedding_pair(
                baseline[fixed_id], baseline[balanced_id], basin_action
            )
            for fixed_id, balanced_id in zip(fixed_ids, balanced_ids, strict=True)
        ]
        controls = [
            self._optimizer_control(
                groups[(identifier, "baseline_preconditioned")],
                groups[(identifier, "control_preconditioner_off")],
            )
            for identifier in (
                "fixed_c31_p4_n23",
                "balanced_p4_n23_c23",
            )
        ]
        supports = (
            fixed_pair["supporting"] is True
            and cutoff_pair["supporting"] is True
            and holdout["supporting"] is True
        )
        return {
            "fixed_embedding_mesh_sequence": [
                self._axis_record(baseline[identifier]) for identifier in fixed_ids
            ],
            "balanced_embedding_mesh_sequence": [
                self._axis_record(baseline[identifier]) for identifier in balanced_ids
            ],
            "cutoff_sequence": [
                self._axis_record(baseline[identifier]) for identifier in cutoff_ids
            ],
            "fixed_embedding_finest_pair": fixed_pair,
            "cutoff_finest_pair": cutoff_pair,
            "fixed_embedding_holdout": holdout,
            "embedding_comparisons": embedding,
            "preconditioner_controls": controls,
            "supports_declared_convergence": supports,
            "disposition": (
                "supports the frozen standalone finite-sequence criteria"
                if supports
                else "does not support the frozen standalone finite-sequence criteria"
            ),
            "not_global_optimizer_convergence": True,
            "not_general_wannier_convergence": True,
        }

    def _pair_assessment(
        self,
        lower: dict[str, JsonValue],
        upper: dict[str, JsonValue],
        method: dict[str, JsonValue],
        basin_action: DensityAwareBasinAction,
    ) -> dict[str, JsonValue]:
        best = self._differences(
            self._mapping(lower["best_observed_converged"]),
            self._mapping(upper["best_observed_converged"]),
            basin_action,
        )
        median = self._differences(
            self._mapping(lower["median_across_converged"]),
            self._mapping(upper["median_across_converged"]),
            basin_action,
        )
        metric_pass = all(
            self._real(self._mapping(value)["relative_omega_i_change"])
            <= self._real(method["relative_omega_i_tolerance"])
            and self._real(self._mapping(value)["relative_omega_tilde_change"])
            <= self._real(method["relative_omega_tilde_tolerance"])
            and self._real(self._mapping(value)["center_set_periodic_distance"])
            <= self._real(method["center_set_periodic_tolerance_cell"])
            and self._real(self._mapping(value)["relative_radius_18_tail_change"])
            <= self._real(method["relative_radius_18_hopping_tail_tolerance"])
            for value in (best, median)
        )
        fraction_pass = all(
            self._real(value["effective_native_converged_fraction"])
            >= self._real(method["minimum_converged_start_fraction"])
            for value in (lower, upper)
        )
        basin_pass = all(
            value["best_basin_criterion_pass"] is True for value in (lower, upper)
        )
        return {
            "lower_configuration_id": lower["configuration_id"],
            "upper_configuration_id": upper["configuration_id"],
            "best_observed_differences": best,
            "median_differences": median,
            "metric_pass": metric_pass,
            "converged_fraction_pass": fraction_pass,
            "repeated_best_basin_pass": basin_pass,
            "supporting": metric_pass and fraction_pass and basin_pass,
        }

    def _differences(
        self,
        lower: dict[str, JsonValue],
        upper: dict[str, JsonValue],
        basin_action: DensityAwareBasinAction,
    ) -> dict[str, JsonValue]:
        lower_centers = (
            lower["native_centers_modulo_cell"]
            if "native_centers_modulo_cell" in lower
            else lower["native_centers_modulo_cell_medoid"]
        )
        upper_centers = (
            upper["native_centers_modulo_cell"]
            if "native_centers_modulo_cell" in upper
            else upper["native_centers_modulo_cell_medoid"]
        )
        return {
            "relative_omega_i_change": self._relative(
                self._real(lower["omega_i_cell_squared"]),
                self._real(upper["omega_i_cell_squared"]),
            ),
            "relative_omega_tilde_change": self._relative(
                self._real(lower["omega_tilde_cell_squared"]),
                self._real(upper["omega_tilde_cell_squared"]),
            ),
            "center_set_periodic_distance": basin_action.center_distance(
                lower_centers, upper_centers
            ),
            "relative_radius_18_tail_change": self._relative(
                self._real(lower["radius_18_hopping_tail_energy_units"]),
                self._real(upper["radius_18_hopping_tail_energy_units"]),
            ),
        }

    def _holdout(
        self,
        sequence: list[dict[str, JsonValue]],
        method: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        training = sequence[1:5]
        holdout = sequence[5]
        records: list[JsonValue] = []
        for summary_name, source_key in (
            ("best", "best_observed_converged"),
            ("median", "median_across_converged"),
        ):
            for metric in (
                "omega_i_cell_squared",
                "omega_tilde_cell_squared",
                "radius_18_hopping_tail_energy_units",
            ):
                x = np.asarray(
                    [
                        1.0 / self._integer(value["reciprocal_mesh_size"]) ** 2
                        for value in training
                    ],
                    dtype=float,
                )
                y = np.asarray(
                    [
                        self._real(self._mapping(value[source_key])[metric])
                        for value in training
                    ],
                    dtype=float,
                )
                design = np.column_stack((np.ones_like(x), x))
                coefficients, _, _, _ = np.linalg.lstsq(design, y, rcond=None)
                holdout_x = 1.0 / self._integer(holdout["reciprocal_mesh_size"]) ** 2
                predicted = float(coefficients[0] + coefficients[1] * holdout_x)
                observed = self._real(self._mapping(holdout[source_key])[metric])
                residual = self._relative(predicted, observed)
                records.append(
                    {
                        "summary": summary_name,
                        "metric": metric,
                        "intercept": float(coefficients[0]),
                        "inverse_square_coefficient": float(coefficients[1]),
                        "predicted_n31": predicted,
                        "observed_n31": observed,
                        "relative_residual": residual,
                        "pass": residual
                        <= self._real(method["maximum_holdout_relative_residual"]),
                    }
                )
        return {
            "training_meshes": [15, 19, 23, 27],
            "holdout_mesh": 31,
            "records": records,
            "supporting": all(
                self._mapping(value)["pass"] is True for value in records
            ),
        }

    def _embedding_pair(
        self,
        fixed: dict[str, JsonValue],
        balanced: dict[str, JsonValue],
        basin_action: DensityAwareBasinAction,
    ) -> dict[str, JsonValue]:
        return {
            "reciprocal_mesh_size": fixed["reciprocal_mesh_size"],
            "fixed_configuration_id": fixed["configuration_id"],
            "balanced_configuration_id": balanced["configuration_id"],
            "best_observed_differences": self._differences(
                self._mapping(fixed["best_observed_converged"]),
                self._mapping(balanced["best_observed_converged"]),
                basin_action,
            ),
        }

    def _optimizer_control(
        self,
        baseline: dict[str, JsonValue],
        control: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        return {
            "configuration_id": baseline["configuration_id"],
            "baseline_final_converged_count": baseline[
                "effective_native_converged_count"
            ],
            "control_final_converged_count": control[
                "effective_native_converged_count"
            ],
            "baseline_best_omega_tilde_cell_squared": self._mapping(
                baseline["best_observed_converged"]
            )["omega_tilde_cell_squared"],
            "control_best_omega_tilde_cell_squared": self._mapping(
                control["best_observed_converged"]
            )["omega_tilde_cell_squared"],
            "descriptive_only": True,
        }

    def _axis_record(self, group: dict[str, JsonValue]) -> dict[str, JsonValue]:
        return {
            "configuration_id": group["configuration_id"],
            "reciprocal_mesh_size": group["reciprocal_mesh_size"],
            "plane_wave_cutoff": group["plane_wave_cutoff"],
            "transverse_lattice_length": group["transverse_lattice_length"],
            "effective_native_converged_count": group[
                "effective_native_converged_count"
            ],
            "effective_native_converged_fraction": group[
                "effective_native_converged_fraction"
            ],
            "best_observed_converged": group["best_observed_converged"],
            "median_across_converged": group["median_across_converged"],
            "best_basin_criterion_pass": group["best_basin_criterion_pass"],
        }

    def _compact(self, summary: dict[str, JsonValue]) -> dict[str, JsonValue]:
        native = self._mapping(summary["effective_native_endpoint"])
        represented = self._mapping(summary["represented_endpoint"])
        return {
            "start_id": summary["start_id"],
            "omega_i_cell_squared": native["omega_i_cell_squared"],
            "omega_tilde_cell_squared": native["omega_tilde_cell_squared"],
            "omega_total_cell_squared": native["omega_total_cell_squared"],
            "native_centers_modulo_cell": summary["native_centers_modulo_cell"],
            "common_total_spread_cell_squared": represented[
                "common_total_spread_cell_squared"
            ],
            "radius_8_hopping_tail_energy_units": self._tail(summary, 8),
            "radius_18_hopping_tail_energy_units": self._tail(summary, 18),
        }

    def _median_native(self, values: list[dict[str, JsonValue]], key: str) -> float:
        return float(
            np.median(
                [
                    self._real(self._mapping(value["effective_native_endpoint"])[key])
                    for value in values
                ]
            )
        )

    def _median_tail(self, values: list[dict[str, JsonValue]], radius: int) -> float:
        return float(np.median([self._tail(value, radius) for value in values]))

    def _tail(self, summary: dict[str, JsonValue], radius: int) -> float:
        represented = self._mapping(summary["represented_endpoint"])
        return self._real(
            next(
                self._mapping(value)["omitted_block_frobenius_l2_norm_energy_units"]
                for value in self._array(represented["hopping_tails"])
                if self._integer(self._mapping(value)["maximum_squared_radius"])
                == radius
            )
        )

    def _omega_tilde(self, summary: dict[str, JsonValue]) -> float:
        return self._real(
            self._mapping(summary["effective_native_endpoint"])[
                "omega_tilde_cell_squared"
            ]
        )

    @staticmethod
    def _relative(first: float, second: float) -> float:
        return abs(first - second) / max(abs(second), 1.0e-15)

    def _continuation_key(self, value: dict[str, JsonValue]) -> tuple[str, str, str]:
        return (
            self._string(value["configuration_id"]),
            self._string(value["source_arm"]),
            self._string(value["start_id"]),
        )

    def _start_index(self, value: dict[str, JsonValue]) -> int:
        start_id = self._string(value["start_id"])
        return 0 if start_id == "identity" else int(start_id.rsplit("_", 1)[1])

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


class CommandAdapter:
    """Adapt proposal and retained execution paths to offline extraction."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--proposal", type=Path, required=True)
        parser.add_argument("--execution-result", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        arguments = parser.parse_args(argv)
        result = StandaloneResultExtractor().execute(
            cast(Path, arguments.proposal).resolve(),
            cast(Path, arguments.execution_result).resolve(),
            cast(Path, arguments.output).resolve(),
        )
        summary = result["execution_summary"]
        assessment = result["convergence_assessment"]
        if not isinstance(summary, dict) or not isinstance(assessment, dict):
            raise TypeError("result summaries must be objects")
        print(
            json.dumps(
                {
                    "effective_native_converged_count": summary[
                        "effective_native_converged_count"
                    ],
                    "effective_native_nonconverged_count": summary[
                        "effective_native_nonconverged_count"
                    ],
                    "supports_declared_convergence": assessment[
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
