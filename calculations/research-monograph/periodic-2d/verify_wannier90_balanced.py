#!/usr/bin/env python3
"""Independently verify the corrected periodic-2D Wannier90 comparison."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
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


class CorrectedWannier90Verifier:
    """Reconstruct parent, gauge, hopping, localization, and execution facts."""

    __slots__ = ()

    def execute(
        self,
        result_path: Path,
        *,
        portable: bool = False,
        repository_root: Path | None = None,
        extractor_path: Path | None = None,
    ) -> None:
        result = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        if self._integer(result["schema_version"]) != 1:
            raise ValueError("unexpected result schema")
        if result["evidence_status"] != "calculated illustrative converged comparison":
            raise ValueError("unexpected evidence status")
        provenance = self._mapping(result["provenance"])
        resolved_repository_root = (
            result_path.parents[3]
            if repository_root is None
            else repository_root.resolve()
        )
        input_reference = Path(self._string(provenance["input_path"]))
        input_path = (
            input_reference
            if input_reference.is_absolute()
            else resolved_repository_root / input_reference
        )
        resolved_extractor_path = (
            result_path.with_name("extract_wannier90.py")
            if extractor_path is None
            else extractor_path.resolve()
        )
        self._identity(
            resolved_extractor_path,
            self._string(provenance["extractor_sha256"]),
            "extractor",
        )
        if portable:
            fixture = self._mapping(result["portable_evidence"])
            input_payload = self._string(fixture["input_payload_utf8"]).encode()
            self._content_identity(
                input_payload, self._string(provenance["input_sha256"]), "input"
            )
            controls = self._mapping(
                cast(JsonValue, json.loads(input_payload.decode("utf-8")))
            )
        else:
            self._identity(
                input_path, self._string(provenance["input_sha256"]), "input"
            )
            controls = self._mapping(
                cast(JsonValue, json.loads(input_path.read_text(encoding="utf-8")))
            )
        run_root = Path(self._string(provenance["external_run_root"]))
        seed_dir = run_root / "low_triple"
        files = self._array(provenance["files"])
        execution = self._mapping(result["execution"])
        if not self._boolean(execution["convergence_criterion_satisfied"]):
            raise AssertionError("localization is not marked converged")
        if self._integer(execution["interface_neighbor_count"]) <= 0:
            raise AssertionError("interface must have at least one neighbor")
        if self._real(execution["transverse_lattice_length"]) <= 0.0:
            raise AssertionError("transverse lattice length must be positive")

        if portable:
            kpoints = self._real_matrix(fixture["kpoints_fractional"])
            w90_unitaries = self._complex_matrix(
                fixture["w90_unitaries_real_imaginary"]
            )
            energies = self._real_matrix(fixture["energies_energy_units"])
            blocks = self._portable_hopping_blocks(fixture["hopping_blocks"])
            native_total_observed = self._real(
                fixture["native_total_spread_cell_squared"]
            )
            self._equal(
                self._integer(fixture["native_convergence_iterations"]),
                self._integer(execution["iterations"]),
                "portable convergence iterations",
            )
        else:
            for file_value in files:
                record = self._mapping(file_value)
                path = seed_dir / self._string(record["name"])
                self._identity(path, self._string(record["sha256"]), path.name)
                self._equal(
                    path.stat().st_size, self._integer(record["bytes"]), path.name
                )
            self._equal(
                int((seed_dir / "low_triple.pp.exitcode").read_text().strip()),
                self._integer(execution["preprocessing_exit_code"]),
                "preprocessing exit",
            )
            self._equal(
                int((seed_dir / "low_triple.run.exitcode").read_text().strip()),
                self._integer(execution["localization_exit_code"]),
                "localization exit",
            )
            wout = (seed_dir / "low_triple.wout").read_text(encoding="utf-8")
            if "Wannierisation convergence criteria satisfied" not in wout:
                raise AssertionError("native convergence statement is absent")
            iterations = re.findall(r"^\s+(\d+)\s+.*<-- CONV$", wout, re.MULTILINE)
            if not iterations:
                raise AssertionError("native convergence iterations are absent")
            self._equal(
                int(iterations[-1]),
                self._integer(execution["iterations"]),
                "iterations",
            )
            total_match = re.search(
                r"Final Spread \(Ang\^2\)\s+Omega Total\s+=\s+([^\s]+)",
                wout.rsplit("Final State", maxsplit=1)[1],
            )
            if total_match is None:
                raise AssertionError("native final spread is absent")
            native_total_observed = float(total_match.group(1))
            kpoints, w90_unitaries = self._u_matrices(seed_dir / "low_triple_u.mat")
            energies = self._energies(seed_dir / "low_triple.eig", kpoints.shape[0])
            blocks = self._hopping_blocks(seed_dir / "low_triple_hr.dat")
            self._equal(
                self._neighbor_count(seed_dir / "low_triple.nnkp"),
                self._integer(execution["interface_neighbor_count"]),
                "interface neighbor count",
            )
            self._close(
                self._transverse_lattice_length(seed_dir / "low_triple.win"),
                self._real(execution["transverse_lattice_length"]),
                1.0e-14,
                "transverse lattice length",
            )
        direct_unitaries, raw_frames = self._direct_polar_frames(controls, kpoints)
        direct_hamiltonians = np.einsum(
            "kji,kj,kjl->kil", direct_unitaries.conj(), energies, direct_unitaries
        )
        w90_hamiltonians = np.einsum(
            "kji,kj,kjl->kil", w90_unitaries.conj(), energies, w90_unitaries
        )
        represented = self._mapping(result["represented_comparison"])
        unitarity = float(
            np.max(
                np.linalg.norm(
                    w90_unitaries.conj().transpose(0, 2, 1) @ w90_unitaries - np.eye(3),
                    axis=(-2, -1),
                )
            )
        )
        self._close(
            unitarity,
            self._real(represented["w90_unitarity_maximum_frobenius_defect"]),
            2.0e-14,
            "U-matrix unitarity",
        )
        projector_defect = 0.0
        exact_defect = 0.0
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
            transform = w90_unitaries[index].conj().T @ direct_unitaries[index]
            exact_defect = max(
                exact_defect,
                float(
                    np.linalg.norm(
                        transform.conj().T @ w90_hamiltonians[index] @ transform
                        - direct_hamiltonians[index]
                    )
                ),
            )
        self._close(
            projector_defect,
            self._real(represented["direct_w90_projector_maximum_frobenius_defect"]),
            3.0e-10,
            "projector defect",
        )
        self._close(
            exact_defect,
            self._real(
                represented[
                    "k_dependent_exact_alignment_operator_maximum_frobenius_defect"
                ]
            ),
            3.0e-10,
            "exact aligned operator defect",
        )
        raw_defect = float(
            np.max(
                np.linalg.norm(direct_hamiltonians - w90_hamiltonians, axis=(-2, -1))
            )
        )
        self._close(
            raw_defect,
            self._real(represented["raw_gauge_operator_maximum_frobenius_defect"]),
            3.0e-10,
            "raw operator defect",
        )
        self._verify_bounded_alignment(
            self._mapping(represented["translation_constant_alignment"]),
            kpoints,
            direct_unitaries,
            w90_unitaries,
            direct_hamiltonians,
            w90_hamiltonians,
        )

        reconstructed = np.empty_like(w90_hamiltonians)
        for index, (kx, ky, _) in enumerate(kpoints):
            reconstructed[index] = sum(
                np.exp(2j * np.pi * (kx * rx + ky * ry)) * matrix
                for (rx, ry), matrix in blocks.items()
            )
        operator_defect = float(
            np.max(np.linalg.norm(reconstructed - w90_hamiltonians, axis=(-2, -1)))
        )
        spectrum_defect = float(
            np.max(
                np.abs(
                    np.linalg.eigvalsh(reconstructed)
                    - np.linalg.eigvalsh(w90_hamiltonians)
                )
            )
        )
        self._close(
            operator_defect,
            self._real(represented["hr_mesh_operator_maximum_frobenius_defect"]),
            2.0e-12,
            "hr operator reconstruction",
        )
        self._close(
            spectrum_defect,
            self._real(represented["hr_mesh_spectrum_maximum_absolute_defect"]),
            2.0e-12,
            "hr spectrum reconstruction",
        )
        shell_records = self._array(represented["shell_study"])
        for shell_value in shell_records:
            shell = self._mapping(shell_value)
            radius = self._integer(shell["maximum_squared_radius"])
            omitted = float(
                np.sqrt(
                    sum(
                        np.linalg.norm(matrix) ** 2
                        for (rx, ry), matrix in blocks.items()
                        if rx * rx + ry * ry > radius
                    )
                )
            )
            self._close(
                omitted,
                self._real(shell["omitted_block_frobenius_l2_norm"]),
                2.0e-14,
                f"shell {radius}",
            )
        localization = self._mapping(result["localization"])
        native = self._mapping(localization["native_wannier90"])
        native_total = native_total_observed
        self._close(
            native_total,
            self._real(native["total_spread_cell_squared"]),
            1.0e-12,
            "native total spread",
        )
        common_records = self._finite_supercell_localization(
            controls, kpoints, raw_frames @ w90_unitaries
        )
        recorded_common = self._array(localization["common_finite_supercell_estimator"])
        self._equal(len(common_records), len(recorded_common), "common spread count")
        for rebuilt, recorded_value in zip(
            common_records, recorded_common, strict=True
        ):
            recorded = self._mapping(recorded_value)
            self._close(
                self._real(rebuilt["coefficient_norm"]),
                self._real(recorded["coefficient_norm"]),
                2.0e-13,
                "common coefficient norm",
            )
            self._close(
                self._real(rebuilt["spread_cell_squared"]),
                self._real(recorded["spread_cell_squared"]),
                2.0e-12,
                "common finite-supercell spread",
            )
            if rebuilt["density_content_sha256"] != recorded["density_content_sha256"]:
                raise AssertionError("common density identity mismatch")
        common_total = sum(
            self._real(record["spread_cell_squared"]) for record in common_records
        )
        direct_common_records = self._finite_supercell_localization(
            controls, kpoints, raw_frames @ direct_unitaries
        )
        recorded_direct_common = self._array(
            localization["direct_projected_common_finite_supercell_estimator"]
        )
        self._equal(
            len(direct_common_records),
            len(recorded_direct_common),
            "direct common spread count",
        )
        for rebuilt, recorded_value in zip(
            direct_common_records, recorded_direct_common, strict=True
        ):
            recorded = self._mapping(recorded_value)
            self._close(
                self._real(rebuilt["spread_cell_squared"]),
                self._real(recorded["spread_cell_squared"]),
                2.0e-12,
                "direct common finite-supercell spread",
            )
            if rebuilt["density_content_sha256"] != recorded["density_content_sha256"]:
                raise AssertionError("direct common density identity mismatch")
        direct_total = sum(
            self._real(record["spread_cell_squared"])
            for record in direct_common_records
        )
        self._close(
            direct_total,
            self._real(localization["direct_projected_total_spread_cell_squared"]),
            1.0e-12,
            "direct projected common-estimator spread",
        )
        recorded_centered_total = localization[
            "centered_mesh_direct_projected_total_spread_cell_squared"
        ]
        if recorded_centered_total is not None:
            composite_result = self._mapping(
                cast(
                    JsonValue,
                    json.loads(
                        result_path.with_name("composite-result.json").read_text(
                            encoding="utf-8"
                        )
                    ),
                )
            )
            smooth = self._mapping(composite_result["smooth_projected_gauge"])
            centered_direct_total = sum(
                self._real(self._mapping(value)["spread_cell_squared"])
                for value in self._array(smooth["localization"])
            )
            self._close(
                centered_direct_total,
                self._real(recorded_centered_total),
                1.0e-12,
                "centered-mesh direct projected spread",
            )
        self._close(
            common_total / direct_total,
            self._real(
                localization["common_estimator_wannier90_to_direct_spread_ratio"]
            ),
            1.0e-14,
            "common-estimator spread ratio",
        )
        self._close(
            native_total / common_total,
            self._real(localization["native_to_common_wannier90_spread_ratio"]),
            1.0e-14,
            "native-to-common spread ratio",
        )

    def _finite_supercell_localization(
        self,
        controls: dict[str, JsonValue],
        kpoints: RealMatrix,
        frames: ComplexFrames,
    ) -> list[dict[str, JsonValue]]:
        cutoff = self._integer(controls["plane_wave_cutoff"])
        mesh_size = self._integer(controls["reciprocal_mesh_size"])
        fft_size = self._integer(controls["localization_fft_size"])
        side = 2 * cutoff + 1
        coordinate = np.linspace(0.0, mesh_size, fft_size, endpoint=False)
        records: list[dict[str, JsonValue]] = []
        for orbital in range(3):
            coefficients = np.zeros((fft_size, fft_size), dtype=np.complex128)
            for point in range(kpoints.shape[0]):
                ix = int(np.rint(kpoints[point, 0] * mesh_size)) % mesh_size
                iy = int(np.rint(kpoints[point, 1] * mesh_size)) % mesh_size
                values = frames[point, :, orbital].reshape(side, side)
                for ip in range(side):
                    for iq in range(side):
                        p = ip - cutoff
                        q = iq - cutoff
                        coefficients[
                            (p * mesh_size + ix) % fft_size,
                            (q * mesh_size + iy) % fft_size,
                        ] += values[ip, iq] / mesh_size
            coefficient_norm = float(np.vdot(coefficients, coefficients).real)
            probability = np.abs(np.fft.ifftn(coefficients) * fft_size**2) ** 2
            probability /= probability.sum()
            marginal_x = probability.sum(axis=1)
            marginal_y = probability.sum(axis=0)
            center_x = self._circular_center(marginal_x, coordinate, mesh_size)
            center_y = self._circular_center(marginal_y, coordinate, mesh_size)
            displacement_x = (
                np.remainder(coordinate - center_x + mesh_size / 2.0, mesh_size)
                - mesh_size / 2.0
            )
            displacement_y = (
                np.remainder(coordinate - center_y + mesh_size / 2.0, mesh_size)
                - mesh_size / 2.0
            )
            spread = float(
                np.einsum(
                    "ij,ij->",
                    probability,
                    displacement_x[:, None] ** 2 + displacement_y[None, :] ** 2,
                )
            )
            digest = hashlib.sha256(
                np.around(probability, decimals=12)
                .astype("<f8", copy=False)
                .tobytes(order="C")
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

    def _circular_center(
        self,
        marginal: npt.NDArray[np.float64],
        coordinate: npt.NDArray[np.float64],
        period: int,
    ) -> float:
        phase = np.exp(2j * np.pi * coordinate / period)
        angle = np.angle(np.dot(marginal, phase)) % (2.0 * np.pi)
        return float(angle * period / (2.0 * np.pi))

    def _verify_bounded_alignment(
        self,
        recorded: dict[str, JsonValue],
        kpoints: RealMatrix,
        direct: ComplexFrames,
        w90: ComplexFrames,
        direct_hamiltonians: ComplexFrames,
        w90_hamiltonians: ComplexFrames,
    ) -> None:
        translations = tuple(itertools.product((-1, 0, 1), repeat=2))
        best = (np.inf, np.inf, np.inf)
        best_assignment: tuple[tuple[int, int], ...] | None = None
        for assignment in itertools.product(translations, repeat=3):
            phases = np.column_stack(
                [
                    np.exp(-2j * np.pi * (kpoints[:, 0] * rx + kpoints[:, 1] * ry))
                    for rx, ry in assignment
                ]
            )
            translated = w90 * phases[:, None, :]
            cross = np.einsum("kji,kjl->il", translated.conj(), direct)
            left, _, right_h = np.linalg.svd(cross)
            constant = left @ right_h
            aligned = translated @ constant
            defects = np.linalg.norm(aligned - direct, axis=(-2, -1))
            rms = float(np.sqrt(np.mean(np.square(defects)) / 3.0))
            if rms < best[0]:
                operator_defect = 0.0
                for index in range(kpoints.shape[0]):
                    diagonal = np.diag(phases[index])
                    value = (
                        constant.conj().T
                        @ diagonal.conj().T
                        @ w90_hamiltonians[index]
                        @ diagonal
                        @ constant
                    )
                    operator_defect = max(
                        operator_defect,
                        float(np.linalg.norm(value - direct_hamiltonians[index])),
                    )
                best = (rms, float(np.max(defects)), operator_defect)
                best_assignment = assignment
        if best_assignment is None:
            raise RuntimeError("alignment search had no candidates")
        recorded_assignment = tuple(
            tuple(self._integers(value))
            for value in self._array(recorded["best_orbital_translations"])
        )
        if recorded_assignment != best_assignment:
            raise AssertionError("best bounded translations disagree")
        for actual, key in zip(
            best,
            (
                "frame_root_mean_square_defect_per_orbital",
                "frame_maximum_frobenius_defect",
                "operator_maximum_frobenius_defect",
            ),
            strict=True,
        ):
            self._close(actual, self._real(recorded[key]), 3.0e-10, key)

    def _direct_polar_frames(
        self, controls: dict[str, JsonValue], kpoints: RealMatrix
    ) -> tuple[ComplexFrames, ComplexFrames]:
        potential = self._mapping(controls["potential"])
        trial_input = self._mapping(controls["trial_orbitals"])
        cutoff = self._integer(controls["plane_wave_cutoff"])
        width = self._real(trial_input["momentum_width"])
        center = self._reals(trial_input["center_fractional"])
        lambdas = (
            self._real(potential["lambda_x"]),
            self._real(potential["lambda_y"]),
            self._real(potential["lambda_xy"]),
        )
        reciprocal = tuple(
            (p, q)
            for p in range(-cutoff, cutoff + 1)
            for q in range(-cutoff, cutoff + 1)
        )
        dimension = len(reciprocal)
        unitaries = np.empty((kpoints.shape[0], 3, 3), dtype=np.complex128)
        raw_frames = np.empty((kpoints.shape[0], dimension, 3), dtype=np.complex128)
        for point, (kx, ky, _) in enumerate(kpoints):
            matrix = np.zeros((dimension, dimension), dtype=np.complex128)
            for first, (p, q) in enumerate(reciprocal):
                matrix[first, first] = (kx + p) ** 2 + (ky + q) ** 2
                for second, (r, s) in enumerate(reciprocal):
                    dp = p - r
                    dq = q - s
                    if abs(dp) == 1 and dq == 0:
                        matrix[first, second] += lambdas[0] / 2.0
                    if dp == 0 and abs(dq) == 1:
                        matrix[first, second] += lambdas[1] / 2.0
                    if abs(dp) == 1 and abs(dq) == 1:
                        matrix[first, second] += lambdas[2] / 4.0
            _, vectors = np.linalg.eigh(matrix)
            raw = vectors[:, :3]
            trial_values = np.empty((dimension, 3), dtype=np.complex128)
            for index, (p, q) in enumerate(reciprocal):
                x = kx + p
                y = ky + q
                base = np.exp(-0.5 * width**2 * (x * x + y * y))
                phase = np.exp(-2j * np.pi * (center[0] * x + center[1] * y))
                trial_values[index] = (
                    base * phase,
                    1j * x * base * phase,
                    1j * y * base * phase,
                )
            for column in range(3):
                trial_values[:, column] /= np.linalg.norm(trial_values[:, column])
            trial_frame, _ = np.linalg.qr(trial_values)
            overlap = raw.conj().T @ trial_frame
            gram = overlap.conj().T @ overlap
            eigenvalues, eigenvectors = np.linalg.eigh(gram)
            inverse_root = (
                eigenvectors
                @ np.diag(1.0 / np.sqrt(eigenvalues))
                @ eigenvectors.conj().T
            )
            unitaries[point] = overlap @ inverse_root
            raw_frames[point] = raw
        return unitaries, raw_frames

    def _u_matrices(self, path: Path) -> tuple[RealMatrix, ComplexFrames]:
        lines = path.read_text(encoding="utf-8").splitlines()
        count, rows, columns = (int(value) for value in lines[1].split())
        kpoints = np.empty((count, 3), dtype=np.float64)
        matrices = np.empty((count, rows, columns), dtype=np.complex128)
        cursor = 2
        for point in range(count):
            while not lines[cursor].strip():
                cursor += 1
            kpoints[point] = [float(value) for value in lines[cursor].split()]
            cursor += 1
            values: list[complex] = []
            for _ in range(rows * columns):
                real, imaginary = (float(value) for value in lines[cursor].split())
                values.append(complex(real, imaginary))
                cursor += 1
            matrices[point] = np.asarray(values).reshape((rows, columns), order="F")
        return kpoints, matrices

    def _energies(self, path: Path, count: int) -> RealMatrix:
        result = np.empty((count, 3), dtype=np.float64)
        for line in path.read_text(encoding="utf-8").splitlines():
            band, point, energy = line.split()
            result[int(point) - 1, int(band) - 1] = float(energy)
        return result

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
            raise AssertionError("nonunit hopping degeneracy")
        blocks: dict[tuple[int, int], ComplexMatrix] = {}
        for line in lines[cursor:]:
            rx, ry, rz, row, column, real, imaginary = line.split()
            if int(rz) != 0:
                raise AssertionError("inactive hopping is nonzero")
            matrix = blocks.setdefault(
                (int(rx), int(ry)),
                np.zeros((rank, rank), dtype=np.complex128),
            )
            matrix[int(row) - 1, int(column) - 1] = complex(
                float(real), float(imaginary)
            )
        return blocks

    def _real_matrix(self, value: JsonValue) -> RealMatrix:
        return np.array(
            [self._reals(row) for row in self._array(value)], dtype=np.float64
        )

    def _complex_matrix(self, value: JsonValue) -> ComplexFrames:
        return np.array(
            [
                [
                    [complex(*self._reals(pair)) for pair in self._array(row)]
                    for row in self._array(matrix)
                ]
                for matrix in self._array(value)
            ],
            dtype=np.complex128,
        )

    def _portable_hopping_blocks(
        self, value: JsonValue
    ) -> dict[tuple[int, int], ComplexMatrix]:
        blocks: dict[tuple[int, int], ComplexMatrix] = {}
        for block_value in self._array(value):
            block = self._mapping(block_value)
            translation = self._integers(block["translation"])
            if len(translation) != 2:
                raise ValueError("portable hopping translation must have length two")
            matrix_values = self._array(block["matrix_real_imaginary"])
            matrix = np.array(
                [
                    [complex(*self._reals(pair)) for pair in self._array(row)]
                    for row in matrix_values
                ],
                dtype=np.complex128,
            )
            blocks[(translation[0], translation[1])] = matrix
        return blocks

    def _neighbor_count(self, path: Path) -> int:
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
        return int(lines[lines.index("begin nnkpts") + 1])

    def _transverse_lattice_length(self, path: Path) -> float:
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
        fields = lines[lines.index("begin unit_cell_cart") + 4].split()
        if len(fields) != 3:
            raise ValueError("unexpected transverse lattice vector")
        return float(fields[2])

    def _content_identity(self, payload: bytes, expected: str, label: str) -> None:
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected:
            raise AssertionError(
                f"{label} identity mismatch: actual={actual}, expected={expected}"
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

    def _boolean(self, value: JsonValue) -> bool:
        if not isinstance(value, bool):
            raise TypeError("expected a boolean")
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
    parser.add_argument(
        "--portable",
        action="store_true",
        help="verify the compact extracted fixture without native external files",
    )
    parser.add_argument("--repository-root", type=Path)
    parser.add_argument("--extractor", type=Path)
    arguments = parser.parse_args()
    repository_root = cast(Path | None, arguments.repository_root)
    extractor_path = cast(Path | None, arguments.extractor)
    CorrectedWannier90Verifier().execute(
        arguments.result.resolve(),
        portable=arguments.portable,
        repository_root=(
            None if repository_root is None else repository_root.resolve()
        ),
        extractor_path=None if extractor_path is None else extractor_path.resolve(),
    )
    source = "portable_fixture" if arguments.portable else "native_external_run"
    print(f"periodic_2d_wannier90_balanced_verification=PASS source={source}")


if __name__ == "__main__":
    main()
