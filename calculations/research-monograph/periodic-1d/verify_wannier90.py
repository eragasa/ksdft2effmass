#!/usr/bin/env python3
"""Independently verify the retained bounded Wannier90 comparison."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from scipy.linalg import schur  # type: ignore[import-untyped]

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealVector = npt.NDArray[np.float64]
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexArray3 = npt.NDArray[np.complex128]


class Wannier90ResultVerifier:
    """Recompute frame, operator, and finite-range diagnostics from retained U."""

    __slots__ = ()

    def execute(self, result_path: Path) -> None:
        root = self._mapping(
            cast(JsonValue, json.loads(result_path.read_text(encoding="utf-8")))
        )
        if root["schema_version"] != 1:
            raise ValueError("unexpected Wannier90 result schema version")
        if root["evidence_status"] not in (
            "calculated illustrative comparison",
            "calculated illustrative converged comparison",
        ):
            raise ValueError("unexpected Wannier90 evidence status")
        provenance = self._mapping(root["provenance"])
        repository_root = result_path.parents[3]
        input_path = repository_root / self._string(
            provenance["composite_input_path"]
        )
        extractor_path = repository_root / self._string(provenance["extractor_path"])
        if self._sha256(input_path) != self._string(
            provenance["composite_input_sha256"]
        ):
            raise ValueError("composite input identity mismatch")
        if self._sha256(extractor_path) != self._string(
            provenance["extractor_sha256"]
        ):
            raise ValueError("extractor identity mismatch")
        input_root = self._mapping(
            cast(JsonValue, json.loads(input_path.read_text(encoding="utf-8")))
        )
        strength = self._real(input_root["potential_strength_over_recoil"])
        cutoff = self._integer(input_root["plane_wave_cutoff"])
        mesh_size = self._integer(input_root["reciprocal_mesh_size"])
        conventions = self._mapping(root["interface_conventions"])
        iteration_limit = self._integer(conventions["num_iter"])
        groups = self._records(root["groups"])
        if {self._string(group["id"]) for group in groups} != {
            "low_pair",
            "higher_pair",
        }:
            raise ValueError("unexpected Wannier90 retained groups")
        for group in groups:
            self._verify_group(
                group, strength, cutoff, mesh_size, iteration_limit
            )

    def _verify_group(
        self,
        group: dict[str, JsonValue],
        strength: float,
        cutoff: int,
        mesh_size: int,
        iteration_limit: int,
    ) -> None:
        identifier = self._string(group["id"])
        if group["preprocessing_status"] != "completed":
            raise ValueError(f"{identifier}: preprocessing did not complete")
        converged = self._boolean(group["convergence_criterion_satisfied"])
        expected_status = (
            "completed_converged"
            if converged
            else "completed_iteration_limit_not_converged"
        )
        if group["localization_status"] != expected_status:
            raise ValueError(f"{identifier}: unexpected localization disposition")
        iterations = self._integer(group["iterations"])
        if iterations <= 0 or iterations > iteration_limit:
            raise ValueError(f"{identifier}: unexpected iteration count")
        if not converged and iterations != iteration_limit:
            raise ValueError(f"{identifier}: nonconverged run stopped early")
        band_indices = self._integers(group["band_indices"])
        if len(band_indices) != 2 or band_indices[1] != band_indices[0] + 1:
            raise ValueError(f"{identifier}: invalid retained bands")
        unitaries = self._complex_array(group["u_matrices"])
        if unitaries.shape != (mesh_size, 2, 2):
            raise ValueError(f"{identifier}: unexpected U-matrix shape")
        unitarity = float(
            np.max(
                np.linalg.norm(
                    np.einsum(
                        "kji,kjl->kil",
                        unitaries.conj(),
                        unitaries,
                        optimize=True,
                    )
                    - np.eye(2),
                    axis=(1, 2),
                )
            )
        )
        self._agree(
            unitarity,
            self._real(group["u_matrix_unitarity_maximum_frobenius_defect"]),
            1.0e-14,
            f"{identifier} U-matrix unitarity",
        )
        if unitarity > 1.0e-8:
            raise ValueError(f"{identifier}: U matrices are not unitary")

        momenta = np.arange(mesh_size, dtype=np.float64) / mesh_size
        energies, raw_frames, parent_matrices = self._parent(
            momenta, strength, cutoff, band_indices[0]
        )
        direct_frames = self._direct_frames(raw_frames)
        wannier_frames = np.einsum(
            "kdi,kij->kdj", raw_frames, unitaries, optimize=True
        )
        aligned_frames, rotations = self._align(direct_frames, wannier_frames)
        frame_defect = float(
            np.max(np.linalg.norm(aligned_frames - direct_frames, axis=(1, 2)))
        )
        self._agree(
            frame_defect,
            self._real(group["pointwise_alignment_frame_maximum_frobenius_defect"]),
            1.0e-13,
            f"{identifier} frame alignment",
        )
        direct_hamiltonians = self._represented(direct_frames, parent_matrices)
        wannier_hamiltonians = self._represented(wannier_frames, parent_matrices)
        aligned_hamiltonians = np.einsum(
            "kji,kjl,klm->kim",
            rotations.conj(),
            wannier_hamiltonians,
            rotations,
            optimize=True,
        )
        operator_defect = float(
            np.max(
                np.linalg.norm(
                    aligned_hamiltonians - direct_hamiltonians,
                    axis=(1, 2),
                )
            )
        )
        self._agree(
            operator_defect,
            self._real(
                group["pointwise_alignment_operator_maximum_frobenius_defect"]
            ),
            1.0e-12,
            f"{identifier} operator alignment",
        )
        eigenvalue_defect = float(
            np.max(np.abs(np.linalg.eigvalsh(wannier_hamiltonians) - energies))
        )
        self._agree(
            eigenvalue_defect,
            self._real(group["wannier90_represented_eigenvalue_maximum_defect"]),
            1.0e-12,
            f"{identifier} represented eigenvalues",
        )
        if max(frame_defect, operator_defect, eigenvalue_defect) > 1.0e-8:
            raise ValueError(f"{identifier}: aligned represented operator failed")

        representatives = np.arange(-mesh_size // 2, mesh_size // 2)
        transform = np.exp(
            -2j * np.pi * np.outer(representatives, momenta)
        ) / mesh_size
        hoppings = np.einsum(
            "rk,kij->rij", transform, wannier_hamiltonians, optimize=True
        )
        range_records = self._records(group["range_study"])
        errors: list[float] = []
        for record in range_records:
            hopping_range = self._integer(record["hopping_range_cells"])
            retained = np.abs(representatives) <= hopping_range
            model = np.einsum(
                "kr,rij->kij",
                np.exp(
                    2j * np.pi * np.outer(momenta, representatives[retained])
                ),
                hoppings[retained],
                optimize=True,
            )
            error = float(np.max(np.abs(np.linalg.eigvalsh(model) - energies)))
            self._agree(
                error,
                self._real(
                    record["wannier90_training_eigenvalue_maximum_error"]
                ),
                1.0e-12,
                f"{identifier} range {hopping_range}",
            )
            errors.append(error)
        if any(
            later >= earlier
            for earlier, later in zip(errors, errors[1:], strict=False)
        ):
            raise ValueError(f"{identifier}: range errors are not decreasing")
        center_defect = self._real(group["center_set_circular_maximum_defect"])
        if not converged and center_defect <= 0.1:
            raise ValueError(
                f"{identifier}: nonconverged center discrepancy was not retained"
            )

    @staticmethod
    def _parent(
        momenta: RealVector, strength: float, cutoff: int, lower: int
    ) -> tuple[npt.NDArray[np.float64], ComplexArray3, ComplexArray3]:
        dimension = 2 * cutoff + 1
        reciprocal = np.arange(-cutoff, cutoff + 1)
        energies = np.empty((momenta.size, 2), dtype=np.float64)
        frames = np.empty((momenta.size, dimension, 2), dtype=np.complex128)
        matrices = np.empty(
            (momenta.size, dimension, dimension), dtype=np.complex128
        )
        for index, momentum in enumerate(momenta):
            matrix = np.diag(np.square(momentum + reciprocal)).astype(np.complex128)
            coupling = 0.5 * strength
            matrix += np.diag(np.full(dimension - 1, coupling), 1)
            matrix += np.diag(np.full(dimension - 1, coupling), -1)
            values, vectors = np.linalg.eigh(matrix)
            energies[index] = values[lower : lower + 2]
            frames[index] = vectors[:, lower : lower + 2]
            matrices[index] = matrix
        return energies, frames, matrices

    def _direct_frames(self, raw_frames: ComplexArray3) -> ComplexArray3:
        frames = raw_frames.copy()
        for index in range(frames.shape[0] - 1):
            overlap = frames[index].conj().T @ raw_frames[index + 1]
            left, _, right_h = np.linalg.svd(overlap)
            frames[index + 1] = (
                raw_frames[index + 1] @ right_h.conj().T @ left.conj().T
            )
        closure = frames[-1].conj().T @ self._sew(frames[0])
        left, _, right_h = np.linalg.svd(closure)
        triangular, eigenvectors = schur(left @ right_h, output="complex")
        phases = np.angle(np.diag(triangular)).astype(np.float64)
        order = np.argsort(phases)
        phases = phases[order]
        eigenvectors = eigenvectors[:, order]
        for index in range(frames.shape[0]):
            root = (
                eigenvectors
                @ np.diag(np.exp(1j * phases * index / frames.shape[0]))
                @ eigenvectors.conj().T
            )
            frames[index] = frames[index] @ root
        return frames

    @staticmethod
    def _sew(frame: ComplexMatrix) -> ComplexMatrix:
        result = np.zeros_like(frame)
        result[:-1] = frame[1:]
        return result

    @staticmethod
    def _align(
        reference: ComplexArray3, candidate: ComplexArray3
    ) -> tuple[ComplexArray3, ComplexArray3]:
        aligned = np.empty_like(candidate)
        rotations = np.empty((candidate.shape[0], 2, 2), dtype=np.complex128)
        for index in range(reference.shape[0]):
            overlap = candidate[index].conj().T @ reference[index]
            left, _, right_h = np.linalg.svd(overlap)
            rotations[index] = left @ right_h
            aligned[index] = candidate[index] @ rotations[index]
        return aligned, rotations

    @staticmethod
    def _represented(
        frames: ComplexArray3, parent_matrices: ComplexArray3
    ) -> ComplexArray3:
        return np.einsum(
            "kdi,kde,kej->kij",
            frames.conj(),
            parent_matrices,
            frames,
            optimize=True,
        )

    def _complex_array(self, value: JsonValue) -> ComplexArray3:
        matrices: list[list[list[complex]]] = []
        for matrix_value in self._array(value):
            rows: list[list[complex]] = []
            for row_value in self._array(matrix_value):
                row: list[complex] = []
                for entry_value in self._array(row_value):
                    pair = self._array(entry_value)
                    if len(pair) != 2:
                        raise TypeError("complex entry must be a pair")
                    row.append(complex(self._real(pair[0]), self._real(pair[1])))
                rows.append(row)
            matrices.append(rows)
        return np.asarray(matrices, dtype=np.complex128)

    @staticmethod
    def _agree(observed: float, retained: float, tolerance: float, label: str) -> None:
        if abs(observed - retained) > tolerance:
            raise ValueError(f"{label} retained value mismatch")

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("expected JSON object")
        return value

    @staticmethod
    def _records(value: JsonValue) -> tuple[dict[str, JsonValue], ...]:
        if not isinstance(value, list):
            raise TypeError("expected JSON array")
        records: list[dict[str, JsonValue]] = []
        for item in value:
            if not isinstance(item, dict):
                raise TypeError("expected JSON object entry")
            records.append(item)
        return tuple(records)

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("expected JSON array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("expected string")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("expected number")
        return float(value)

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("expected integer")
        return value

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        return tuple(self._integer(item) for item in self._array(value))

    @staticmethod
    def _boolean(value: JsonValue) -> bool:
        if not isinstance(value, bool):
            raise TypeError("expected Boolean")
        return value


class CommandAdapter:
    """Adapt one retained result path to the independent verifier."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("result", type=Path)
        args = parser.parse_args(argv)
        Wannier90ResultVerifier().execute(cast(Path, args.result).resolve())
        print("periodic-1d bounded Wannier90 comparison: PASS")
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
