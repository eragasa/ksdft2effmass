#!/usr/bin/env python3
"""Extract the corrected periodic-2D Wannier90 comparison."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexFrames = npt.NDArray[np.complex128]
type RealMatrix = npt.NDArray[np.float64]


class CorrectedWannier90Extractor:
    """Compare native Wannier90 outputs with the direct projected gauge."""

    __slots__ = ()

    def execute(
        self,
        input_path: Path,
        run_root: Path,
        script_path: Path,
        execution_record: dict[str, JsonValue] | None = None,
    ) -> dict[str, JsonValue]:
        controls = self._mapping(
            cast(JsonValue, json.loads(input_path.read_text(encoding="utf-8")))
        )
        seed_dir = run_root / "low_triple"
        kpoints, w90_unitaries = self._u_matrices(seed_dir / "low_triple_u.mat")
        energies = self._energies(seed_dir / "low_triple.eig", kpoints.shape[0], 3)
        direct_unitaries, raw_frames = self._direct_unitaries(controls, kpoints)
        w90_frames = raw_frames @ w90_unitaries
        direct_frames = raw_frames @ direct_unitaries
        common_localization = self._finite_supercell_localization(
            controls, kpoints, w90_frames
        )
        direct_common_localization = self._finite_supercell_localization(
            controls, kpoints, direct_frames
        )
        direct_hamiltonians = np.einsum(
            "kji,kj,kjl->kil", direct_unitaries.conj(), energies, direct_unitaries
        )
        w90_hamiltonians = np.einsum(
            "kji,kj,kjl->kil", w90_unitaries.conj(), energies, w90_unitaries
        )
        hopping_blocks = self._hopping_blocks(seed_dir / "low_triple_hr.dat")
        reconstructed = self._reconstruct(kpoints, hopping_blocks)
        wout_text = (seed_dir / "low_triple.wout").read_text(encoding="utf-8")
        centers, spreads, total_spread, iterations = self._localization(wout_text)
        composite_result_path = input_path.with_name("composite-result.json")
        direct_total_spread: float | None = None
        if composite_result_path.is_file():
            composite_result = self._mapping(
                cast(
                    JsonValue,
                    json.loads(composite_result_path.read_text(encoding="utf-8")),
                )
            )
            smooth = self._mapping(composite_result["smooth_projected_gauge"])
            smooth_localization = self._array(smooth["localization"])
            direct_total_spread = sum(
                self._real(self._mapping(record)["spread_cell_squared"])
                for record in smooth_localization
            )
        alignment = self._translation_constant_alignment(
            kpoints,
            energies,
            direct_unitaries,
            w90_unitaries,
            direct_hamiltonians,
            w90_hamiltonians,
        )
        exact_alignment_defect = 0.0
        for index in range(kpoints.shape[0]):
            transform = w90_unitaries[index].conj().T @ direct_unitaries[index]
            aligned = transform.conj().T @ w90_hamiltonians[index] @ transform
            exact_alignment_defect = max(
                exact_alignment_defect,
                float(np.linalg.norm(aligned - direct_hamiltonians[index])),
            )
        projector_defect = 0.0
        for index in range(kpoints.shape[0]):
            direct_frame = raw_frames[index] @ direct_unitaries[index]
            w90_frame = raw_frames[index] @ w90_unitaries[index]
            projector_defect = max(
                projector_defect,
                float(
                    np.linalg.norm(
                        direct_frame @ direct_frame.conj().T
                        - w90_frame @ w90_frame.conj().T
                    )
                ),
            )
        shell_radii = self._integers(controls["hopping_shell_squared_radii"])
        shell_records: list[JsonValue] = []
        for radius in shell_radii:
            omitted = float(
                np.sqrt(
                    sum(
                        np.linalg.norm(matrix) ** 2
                        for (rx, ry), matrix in hopping_blocks.items()
                        if rx * rx + ry * ry > radius
                    )
                )
            )
            shell_records.append(
                {
                    "maximum_squared_radius": radius,
                    "omitted_block_frobenius_l2_norm": omitted,
                }
            )
        execution_files = tuple(
            sorted(path for path in seed_dir.iterdir() if path.is_file())
        )
        return {
            "schema_version": 1,
            "experiment_id": "research-monograph.periodic-2d.wannier90-balanced.v1",
            "evidence_status": "calculated illustrative converged comparison",
            "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "authorization_checkpoint": (
                "RM-PERIODIC-2D-WANNIER90-EMBEDDING-RETRY-HC04"
            ),
            "provenance": {
                "input_path": self._portable_path(input_path, script_path.parents[3]),
                "input_sha256": self._sha256(input_path),
                "extractor_sha256": self._sha256(script_path),
                "external_run_root": str(run_root),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
                "files": [
                    {
                        "name": path.name,
                        "bytes": path.stat().st_size,
                        "sha256": self._sha256(path),
                    }
                    for path in execution_files
                ],
            },
            "portable_evidence": {
                "status": (
                    "compact extracted numerical fixture; native format and "
                    "execution-log verification require the external run"
                ),
                "input_payload_utf8": input_path.read_text(encoding="utf-8"),
                "kpoints_fractional": kpoints.tolist(),
                "w90_unitaries_real_imaginary": self._complex_values(w90_unitaries),
                "energies_energy_units": energies.tolist(),
                "hopping_blocks": [
                    {
                        "translation": [rx, ry],
                        "matrix_real_imaginary": self._complex_values(matrix),
                    }
                    for (rx, ry), matrix in sorted(hopping_blocks.items())
                ],
                "native_total_spread_cell_squared": total_spread,
                "native_convergence_iterations": iterations,
            },
            "execution": {
                "preprocessing_exit_code": self._execution_exit_code(
                    execution_record,
                    "preprocessing",
                    seed_dir / "low_triple.pp.exitcode",
                ),
                "localization_exit_code": self._execution_exit_code(
                    execution_record,
                    "localization",
                    seed_dir / "low_triple.run.exitcode",
                ),
                "preprocessing": self._execution_time_record(
                    execution_record,
                    "preprocessing",
                    seed_dir / "low_triple.pp.time",
                ),
                "localization": self._execution_time_record(
                    execution_record,
                    "localization",
                    seed_dir / "low_triple.run.time",
                ),
                "external_output_bytes": sum(
                    path.stat().st_size
                    for path in run_root.rglob("*")
                    if path.is_file()
                ),
                "convergence_criterion_satisfied": (
                    "Wannierisation convergence criteria satisfied" in wout_text
                ),
                "iterations": iterations,
                "interface_neighbor_count": self._neighbor_count(
                    seed_dir / "low_triple.nnkp"
                ),
                "transverse_lattice_length": self._transverse_lattice_length(
                    seed_dir / "low_triple.win"
                ),
            },
            "localization": {
                "native_wannier90": {
                    "centers_cell_fractional": centers,
                    "spreads_cell_squared": spreads,
                    "total_spread_cell_squared": total_spread,
                    "active_plane_only": True,
                },
                "common_finite_supercell_estimator": common_localization,
                "direct_projected_common_finite_supercell_estimator": (
                    direct_common_localization
                ),
                "direct_projected_total_spread_cell_squared": (
                    self._localization_total(direct_common_localization)
                ),
                "centered_mesh_direct_projected_total_spread_cell_squared": (
                    direct_total_spread
                ),
                "common_estimator_wannier90_to_direct_spread_ratio": (
                    self._localization_total(common_localization)
                    / self._localization_total(direct_common_localization)
                ),
                "native_to_common_wannier90_spread_ratio": (
                    total_spread / self._localization_total(common_localization)
                ),
            },
            "represented_comparison": {
                "w90_unitarity_maximum_frobenius_defect": float(
                    np.max(
                        np.linalg.norm(
                            w90_unitaries.conj().transpose(0, 2, 1) @ w90_unitaries
                            - np.eye(3),
                            axis=(-2, -1),
                        )
                    )
                ),
                "direct_w90_projector_maximum_frobenius_defect": projector_defect,
                "raw_gauge_operator_maximum_frobenius_defect": float(
                    np.max(
                        np.linalg.norm(
                            direct_hamiltonians - w90_hamiltonians, axis=(-2, -1)
                        )
                    )
                ),
                "translation_constant_alignment": alignment,
                "k_dependent_exact_alignment_operator_maximum_frobenius_defect": (
                    exact_alignment_defect
                ),
                "hr_mesh_operator_maximum_frobenius_defect": float(
                    np.max(
                        np.linalg.norm(reconstructed - w90_hamiltonians, axis=(-2, -1))
                    )
                ),
                "hr_mesh_spectrum_maximum_absolute_defect": float(
                    np.max(
                        np.abs(
                            np.linalg.eigvalsh(reconstructed)
                            - np.linalg.eigvalsh(w90_hamiltonians)
                        )
                    )
                ),
                "hopping_hermiticity_maximum_frobenius_defect": self._hermiticity(
                    hopping_blocks
                ),
                "shell_study": shell_records,
            },
            "interpretation": {
                "gauge_result": (
                    "The direct projected and optimized Wannier90 frames span the "
                    "same retained subspace but are not related by only bounded "
                    "integer translations and one constant orbital unitary."
                ),
                "localization_result": (
                    "On the common finite-supercell estimator, Wannier90 reduces "
                    "spread and improves the long-range hopping tail relative to the "
                    "direct projected gauge. Its native Berry-link spread is reported "
                    "separately and is not substituted for that common estimator."
                ),
                "claim_boundary": (
                    "This is an independently implemented localization comparison "
                    "for one synthetic represented parent, not material validation, "
                    "a general localization theorem, or uncertainty quantification."
                ),
            },
        }

    def _finite_supercell_localization(
        self,
        controls: dict[str, JsonValue],
        kpoints: RealMatrix,
        frames: ComplexFrames,
    ) -> list[JsonValue]:
        cutoff = self._integer(controls["plane_wave_cutoff"])
        mesh_size = self._integer(controls["reciprocal_mesh_size"])
        fft_size = self._integer(controls["localization_fft_size"])
        side = 2 * cutoff + 1
        coordinate = np.arange(fft_size, dtype=float) * mesh_size / fft_size
        records: list[JsonValue] = []
        for orbital in range(frames.shape[-1]):
            coefficients = np.zeros((fft_size, fft_size), dtype=np.complex128)
            for point, (kx, ky, _) in enumerate(kpoints):
                ix = int(round(float(kx) * mesh_size)) % mesh_size
                iy = int(round(float(ky) * mesh_size)) % mesh_size
                frame = frames[point, :, orbital].reshape(side, side)
                for ip, p in enumerate(range(-cutoff, cutoff + 1)):
                    for iq, q in enumerate(range(-cutoff, cutoff + 1)):
                        coefficients[
                            (p * mesh_size + ix) % fft_size,
                            (q * mesh_size + iy) % fft_size,
                        ] += frame[ip, iq] / mesh_size
            coefficient_norm = float(np.sum(np.square(np.abs(coefficients))))
            wave = np.fft.ifft2(coefficients) * fft_size**2
            probability = np.square(np.abs(wave))
            probability /= np.sum(probability)
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
            records.append(
                {
                    "orbital": orbital,
                    "coefficient_norm": coefficient_norm,
                    "center_supercell_cells": [center_x, center_y],
                    "center_modulo_cell": [center_x % 1.0, center_y % 1.0],
                    "spread_cell_squared": spread,
                    "density_content_sha256": digest,
                }
            )
        return records

    def _localization_total(self, records: list[JsonValue]) -> float:
        return sum(
            self._real(self._mapping(record)["spread_cell_squared"])
            for record in records
        )

    def _circular_center(
        self,
        marginal: npt.NDArray[np.float64],
        coordinate: npt.NDArray[np.float64],
        period: int,
    ) -> float:
        moment = np.sum(marginal * np.exp(2j * np.pi * coordinate / period))
        return float(np.angle(moment) % (2.0 * np.pi) * period / (2.0 * np.pi))

    def _neighbor_count(self, path: Path) -> int:
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
        begin = lines.index("begin nnkpts")
        return int(lines[begin + 1])

    def _transverse_lattice_length(self, path: Path) -> float:
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
        begin = lines.index("begin unit_cell_cart")
        transverse = lines[begin + 4].split()
        if len(transverse) != 3:
            raise ValueError("unexpected transverse lattice vector")
        return float(transverse[2])

    def _portable_path(self, path: Path, repository_root: Path) -> str:
        try:
            return path.relative_to(repository_root).as_posix()
        except ValueError:
            return str(path)

    def _complex_values(self, values: ComplexMatrix) -> JsonValue:
        stacked = np.stack((values.real, values.imag), axis=-1)
        return cast(JsonValue, stacked.tolist())

    def _direct_unitaries(
        self, controls: dict[str, JsonValue], kpoints: RealMatrix
    ) -> tuple[ComplexFrames, ComplexFrames]:
        potential = self._mapping(controls["potential"])
        trials = self._mapping(controls["trial_orbitals"])
        cutoff = self._integer(controls["plane_wave_cutoff"])
        width = self._real(trials["momentum_width"])
        center = self._reals(trials["center_fractional"])
        lambda_x = self._real(potential["lambda_x"])
        lambda_y = self._real(potential["lambda_y"])
        lambda_xy = self._real(potential["lambda_xy"])
        dimension = (2 * cutoff + 1) ** 2
        raw_frames = np.empty((kpoints.shape[0], dimension, 3), dtype=np.complex128)
        unitaries = np.empty((kpoints.shape[0], 3, 3), dtype=np.complex128)
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
            raw = vectors[:, :3]
            trial_columns: list[npt.NDArray[np.complex128]] = []
            for character in range(3):
                x = kx + p_values
                y = ky + q_values
                base = np.exp(-0.5 * width**2 * (x * x + y * y))
                phase = np.exp(-2j * np.pi * (center[0] * x + center[1] * y))
                factor = (
                    np.ones_like(x, dtype=np.complex128)
                    if character == 0
                    else 1j * (x if character == 1 else y)
                )
                column = factor * base * phase
                column /= np.linalg.norm(column)
                trial_columns.append(column)
            trial_frame, _ = np.linalg.qr(np.column_stack(trial_columns))
            overlap = raw.conj().T @ trial_frame
            left, _, right_h = np.linalg.svd(overlap, full_matrices=False)
            raw_frames[index] = raw
            unitaries[index] = left @ right_h
        return unitaries, raw_frames

    def _translation_constant_alignment(
        self,
        kpoints: RealMatrix,
        energies: RealMatrix,
        direct_unitaries: ComplexFrames,
        w90_unitaries: ComplexFrames,
        direct_hamiltonians: ComplexFrames,
        w90_hamiltonians: ComplexFrames,
    ) -> dict[str, JsonValue]:
        translations = tuple(itertools.product((-1, 0, 1), repeat=2))
        best_residual = np.inf
        best_maximum = np.inf
        best_operator = np.inf
        best_translations: tuple[tuple[int, int], ...] | None = None
        for assignment in itertools.product(translations, repeat=3):
            phases = np.empty((kpoints.shape[0], 3), dtype=np.complex128)
            for orbital, (rx, ry) in enumerate(assignment):
                phases[:, orbital] = np.exp(
                    -2j * np.pi * (kpoints[:, 0] * rx + kpoints[:, 1] * ry)
                )
            translated = w90_unitaries * phases[:, None, :]
            cross = np.sum(
                translated.conj().transpose(0, 2, 1) @ direct_unitaries, axis=0
            )
            left, _, right_h = np.linalg.svd(cross)
            constant = left @ right_h
            aligned = translated @ constant
            defects = np.linalg.norm(aligned - direct_unitaries, axis=(-2, -1))
            residual = float(np.sqrt(np.mean(np.square(defects)) / 3.0))
            if residual < best_residual:
                aligned_hamiltonians = np.empty_like(w90_hamiltonians)
                for index in range(kpoints.shape[0]):
                    diagonal = np.diag(phases[index])
                    aligned_hamiltonians[index] = (
                        constant.conj().T
                        @ diagonal.conj().T
                        @ w90_hamiltonians[index]
                        @ diagonal
                        @ constant
                    )
                best_residual = residual
                best_maximum = float(np.max(defects))
                best_operator = float(
                    np.max(
                        np.linalg.norm(
                            aligned_hamiltonians - direct_hamiltonians,
                            axis=(-2, -1),
                        )
                    )
                )
                best_translations = assignment
        if best_translations is None:
            raise RuntimeError("translation alignment had no candidates")
        _ = energies
        return {
            "translation_search_domain": [-1, 0, 1],
            "best_orbital_translations": [list(value) for value in best_translations],
            "frame_root_mean_square_defect_per_orbital": best_residual,
            "frame_maximum_frobenius_defect": best_maximum,
            "operator_maximum_frobenius_defect": best_operator,
        }

    def _u_matrices(self, path: Path) -> tuple[RealMatrix, ComplexFrames]:
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

    def _energies(self, path: Path, count: int, rank: int) -> RealMatrix:
        energies = np.empty((count, rank), dtype=np.float64)
        for line in path.read_text(encoding="utf-8").splitlines():
            band, point, value = line.split()
            energies[int(point) - 1, int(band) - 1] = float(value)
        return energies

    def _hopping_blocks(self, path: Path) -> dict[tuple[int, int], ComplexMatrix]:
        lines = path.read_text(encoding="utf-8").splitlines()
        rank = int(lines[1])
        count = int(lines[2])
        degeneracies: list[int] = []
        cursor = 3
        while len(degeneracies) < count:
            degeneracies.extend(int(value) for value in lines[cursor].split())
            cursor += 1
        if any(value != 1 for value in degeneracies):
            raise ValueError("version 1 expects unit Wigner-Seitz degeneracies")
        blocks: dict[tuple[int, int], ComplexMatrix] = {}
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

    def _reconstruct(
        self, kpoints: RealMatrix, blocks: dict[tuple[int, int], ComplexMatrix]
    ) -> ComplexFrames:
        result = np.empty((kpoints.shape[0], 3, 3), dtype=np.complex128)
        for index, (kx, ky, _) in enumerate(kpoints):
            result[index] = sum(
                np.exp(2j * np.pi * (kx * rx + ky * ry)) * matrix
                for (rx, ry), matrix in blocks.items()
            )
        return result

    def _localization(
        self, text: str
    ) -> tuple[list[JsonValue], list[JsonValue], float, int]:
        final = text.rsplit("Final State", maxsplit=1)[1]
        pattern = re.compile(
            r"WF centre and spread\s+(\d+)\s+\(\s*([^,]+),\s*([^,]+),"
            r"\s*([^\)]+)\s*\)\s+([^\s]+)"
        )
        matches = pattern.findall(final)
        if len(matches) < 3:
            raise ValueError("final centers and spreads were not found")
        centers: list[JsonValue] = []
        spreads: list[JsonValue] = []
        for orbital, x, y, z, spread in matches[:3]:
            if abs(float(z)) > 5.0e-7:
                raise ValueError("inactive center is nonzero")
            centers.append(
                {
                    "orbital": int(orbital) - 1,
                    "active_fractional": [float(x), float(y)],
                    "active_fractional_modulo_cell": [float(x) % 1.0, float(y) % 1.0],
                }
            )
            spreads.append(float(spread))
        total_match = re.search(
            r"Final Spread \(Ang\^2\)\s+Omega Total\s+=\s+([^\s]+)", final
        )
        if total_match is None:
            raise ValueError("final total spread was not found")
        iteration_matches = re.findall(r"^\s+(\d+)\s+.*<-- CONV$", text, re.MULTILINE)
        if not iteration_matches:
            raise ValueError("convergence iterations were not found")
        return centers, spreads, float(total_match.group(1)), int(iteration_matches[-1])

    def _time_record(self, path: Path) -> dict[str, JsonValue]:
        text = path.read_text(encoding="utf-8")
        elapsed_match = re.search(r"^\s*([0-9.]+) real", text, re.MULTILINE)
        memory_match = re.search(
            r"^\s*(\d+)\s+maximum resident set size", text, re.MULTILINE
        )
        if elapsed_match is None or memory_match is None:
            raise ValueError("time record is incomplete")
        return {
            "elapsed_seconds": float(elapsed_match.group(1)),
            "maximum_resident_bytes": int(memory_match.group(1)),
        }

    def _hermiticity(self, blocks: dict[tuple[int, int], ComplexMatrix]) -> float:
        return max(
            float(np.linalg.norm(matrix - blocks[(-rx, -ry)].conj().T))
            for (rx, ry), matrix in blocks.items()
        )

    def _mapping(self, value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected a mapping")
        return value

    def _array(self, value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected an array")
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

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        return tuple(self._integer(item) for item in self._array(value))

    def _execution_exit_code(
        self,
        execution_record: dict[str, JsonValue] | None,
        stage: str,
        fallback_path: Path,
    ) -> int:
        if execution_record is None:
            return int(fallback_path.read_text(encoding="utf-8").strip())
        record = self._execution_stage(execution_record, stage)
        return self._integer(record["exit_code"])

    def _execution_time_record(
        self,
        execution_record: dict[str, JsonValue] | None,
        stage: str,
        fallback_path: Path,
    ) -> dict[str, JsonValue]:
        if execution_record is None:
            return self._time_record(fallback_path)
        record = self._execution_stage(execution_record, stage)
        return {
            "elapsed_seconds": self._real(record["elapsed_seconds"]),
            "maximum_resident_bytes": self._integer(record["maximum_resident_bytes"]),
        }

    def _execution_stage(
        self, execution_record: dict[str, JsonValue], stage: str
    ) -> dict[str, JsonValue]:
        for value in self._array(execution_record["stages"]):
            record = self._mapping(value)
            if record["stage"] == stage:
                return record
        raise ValueError(f"execution record lacks stage {stage}")

    def _exit_code(self, path: Path) -> int:
        return int(path.read_text(encoding="utf-8").strip())

    def _sha256(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """CLI entry point required by the script boundary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    result = CorrectedWannier90Extractor().execute(
        arguments.input.resolve(),
        arguments.run_root.resolve(),
        Path(__file__).resolve(),
    )
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
