#!/usr/bin/env python3
"""Extract and compare bounded Wannier90 outputs for periodic-1D pairs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt
from scipy.linalg import schur  # type: ignore[import-untyped]

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type RealVector = npt.NDArray[np.float64]
type RealMatrix = npt.NDArray[np.float64]
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexArray3 = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class ExtractionInput:
    """Represent the frozen parent and retained groups needed for comparison."""

    strength: float
    cutoff: int
    mesh_size: int
    groups: tuple[tuple[str, int, int], ...]
    ranges: tuple[int, ...]


class ExtractionInputDeserializer:
    """Deserialize the owned comparison subset of the composite input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> ExtractionInput:
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        root = self._mapping(value)
        groups: list[tuple[str, int, int]] = []
        for entry in self._array(root["retained_band_groups"]):
            group = self._mapping(entry)
            indices = self._array(group["band_indices"])
            groups.append(
                (
                    self._string(group["id"]),
                    self._integer(indices[0]),
                    self._integer(indices[1]),
                )
            )
        return ExtractionInput(
            strength=self._real(root["potential_strength_over_recoil"]),
            cutoff=self._integer(root["plane_wave_cutoff"]),
            mesh_size=self._integer(root["reciprocal_mesh_size"]),
            groups=tuple(groups),
            ranges=tuple(
                self._integer(item)
                for item in self._array(root["hopping_ranges_cells"])
            ),
        )

    @staticmethod
    def _mapping(value: JsonValue) -> dict[str, JsonValue]:
        if not isinstance(value, dict):
            raise TypeError("value must be a JSON object")
        return value

    @staticmethod
    def _array(value: JsonValue) -> list[JsonValue]:
        if not isinstance(value, list):
            raise TypeError("value must be a JSON array")
        return value

    @staticmethod
    def _string(value: JsonValue) -> str:
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        return value

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("value must be an integer")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be a number")
        return float(value)


class Wannier90ResultExtractor:
    """Compare Wannier90 frames with the direct polar construction."""

    __slots__ = ()

    def execute(
        self,
        specification: ExtractionInput,
        input_path: Path,
        workdir: Path,
        output_path: Path,
    ) -> None:
        group_results: list[JsonValue] = []
        convergence: list[bool] = []
        for seed, lower, upper in specification.groups:
            group_results.append(
                self._group_result(specification, workdir, seed, lower, upper)
            )
            wout = (workdir / seed / f"{seed}.wout").read_text(encoding="utf-8")
            convergence.append(
                "Wannierisation convergence criteria satisfied" in wout
            )
        all_converged = all(convergence)
        first_seed = specification.groups[0][0]
        win_text = (workdir / first_seed / f"{first_seed}.win").read_text(
            encoding="utf-8"
        )
        preconditioned = "precond = true" in win_text
        checkpoint_ids: list[JsonValue] = [
            "RM-PERIODIC-1D-W90-RUN-HC01",
            "RM-PERIODIC-1D-W90-RETRY-HC02",
        ]
        if preconditioned:
            checkpoint_ids.extend(
                [
                    "RM-PERIODIC-1D-W90-NONCONVERGENCE-HC03",
                    "RM-PERIODIC-1D-W90-CONVERGENCE-HC04",
                    "RM-PERIODIC-1D-W90-CONVERGENCE-FAILURE-HC05",
                    "RM-PERIODIC-1D-W90-PRECONDITIONED-HC06",
                ]
            )
        repository_root = output_path.parents[3]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": "research-monograph.periodic-1d.wannier90.v1",
            "evidence_status": (
                "calculated illustrative converged comparison"
                if all_converged
                else "calculated illustrative comparison"
            ),
            "checkpoint_ids": checkpoint_ids,
            "executable": {
                "name": "wannier90.x",
                "version": "3.1.0",
                "documented_sha256": (
                    "c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd"
                ),
            },
            "interface_conventions": {
                "energy_mapping": "one numerical E_G written as one eV",
                "active_lattice_mapping": "one numerical a written as one Angstrom",
                "inactive_embedding": (
                    "unit transverse form factor for y/z reciprocal shifts"
                ),
                "trial_projections": "identity in each retained eigenbasis",
                "search_shells": 130,
                "num_iter": 5000 if "num_iter = 5000" in win_text else 500,
                "preconditioned": preconditioned,
            },
            "groups": group_results,
            "provenance": {
                "composite_input_path": input_path.relative_to(
                    repository_root
                ).as_posix(),
                "composite_input_sha256": self._sha256(input_path),
                "extractor_path": Path(__file__).resolve().relative_to(
                    repository_root
                ).as_posix(),
                "extractor_sha256": self._sha256(Path(__file__).resolve()),
                "external_run_identity": workdir.name,
            },
            "claim_boundary": (
                "Both preconditioned Wannier90 runs satisfied the frozen spread "
                "convergence criterion. The result is a converged localization "
                "comparison for the identified synthetic parent and interface, "
                "not material validation, transferability to silicon, or UQ."
                if all_converged
                else "The two bounded Wannier90 runs completed but did not "
                "satisfy the frozen spread convergence criterion. The result is "
                "an independent-route diagnostic, not a converged localization "
                "reference, material validation, or UQ."
            ),
        }
        output_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )

    def _group_result(
        self,
        specification: ExtractionInput,
        workdir: Path,
        seed: str,
        lower: int,
        upper: int,
    ) -> dict[str, JsonValue]:
        seed_dir = workdir / seed
        momenta, unitaries = self._read_u_matrix(seed_dir / f"{seed}_u.mat")
        energies, raw_frames, parent_matrices = self._parent_states(
            specification, momenta, lower, upper
        )
        direct_frames, wilson_phases = self._direct_frames(raw_frames)
        wannier_frames = np.einsum(
            "kdi,kij->kdj", raw_frames, unitaries, optimize=True
        )
        aligned_frames, rotations = self._align_frames(
            direct_frames, wannier_frames
        )
        direct_hamiltonians = self._represented_hamiltonians(
            direct_frames, parent_matrices
        )
        wannier_hamiltonians = self._represented_hamiltonians(
            wannier_frames, parent_matrices
        )
        aligned_hamiltonians = np.einsum(
            "kji,kjl,klm->kim",
            rotations.conj(),
            wannier_hamiltonians,
            rotations,
            optimize=True,
        )
        representatives = np.arange(
            -specification.mesh_size // 2,
            specification.mesh_size // 2,
        )
        transform = np.exp(
            -2j * np.pi * np.outer(representatives, momenta)
        ) / specification.mesh_size
        direct_hoppings = np.einsum(
            "rk,kij->rij", transform, direct_hamiltonians, optimize=True
        )
        wannier_hoppings = np.einsum(
            "rk,kij->rij", transform, wannier_hamiltonians, optimize=True
        )
        aligned_hoppings = np.einsum(
            "rk,kij->rij", transform, aligned_hamiltonians, optimize=True
        )
        range_records: list[JsonValue] = []
        for hopping_range in specification.ranges:
            retained = np.abs(representatives) <= hopping_range
            model = np.einsum(
                "kr,rij->kij",
                np.exp(
                    2j * np.pi * np.outer(momenta, representatives[retained])
                ),
                wannier_hoppings[retained],
                optimize=True,
            )
            range_records.append(
                {
                    "hopping_range_cells": hopping_range,
                    "wannier90_training_eigenvalue_maximum_error": float(
                        np.max(np.abs(np.linalg.eigvalsh(model) - energies))
                    ),
                    "wannier90_omitted_block_l2_norm": float(
                        np.sqrt(np.sum(np.abs(wannier_hoppings[~retained]) ** 2))
                    ),
                }
            )
        wout = (seed_dir / f"{seed}.wout").read_text(encoding="utf-8")
        converged = "Wannierisation convergence criteria satisfied" in wout
        centers, spreads, omega = self._final_localization(wout)
        direct_centers = np.sort(wilson_phases / (2.0 * np.pi))
        center_defect = self._center_set_defect(direct_centers, centers[:, 0])
        hr_momenta, hr_hamiltonians = self._read_hr(
            seed_dir / f"{seed}_hr.dat", momenta
        )
        if np.max(np.abs(hr_momenta - momenta)) > 1.0e-14:
            raise ValueError("hr interpolation momenta disagree with u-matrix mesh")
        source_paths = (
            seed_dir / f"{seed}.win",
            seed_dir / f"{seed}.eig",
            seed_dir / f"{seed}.amn",
            seed_dir / f"{seed}.mmn",
            seed_dir / f"{seed}.nnkp",
            seed_dir / f"{seed}.wout",
            seed_dir / f"{seed}.chk",
            seed_dir / f"{seed}_u.mat",
            seed_dir / f"{seed}_hr.dat",
            seed_dir / f"{seed}.run.stdout",
            seed_dir / f"{seed}.run.stderr",
        )
        return {
            "id": seed,
            "band_indices": [lower, upper],
            "preprocessing_status": "completed",
            "localization_status": (
                "completed_converged"
                if converged
                else "completed_iteration_limit_not_converged"
            ),
            "iterations": self._maximum_iteration(wout),
            "convergence_criterion_satisfied": converged,
            "centers_cell_coordinates": self._real_array(centers),
            "spreads_cell_squared": [float(value) for value in spreads],
            "omega_components_cell_squared": omega,
            "direct_wilson_eigenphases": [float(value) for value in wilson_phases],
            "direct_wilson_centers_by_phase_convention": [
                float(value) for value in direct_centers
            ],
            "center_set_circular_maximum_defect": center_defect,
            "u_matrix_unitarity_maximum_frobenius_defect": float(
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
            ),
            "pointwise_alignment_frame_maximum_frobenius_defect": float(
                np.max(np.linalg.norm(aligned_frames - direct_frames, axis=(1, 2)))
            ),
            "pointwise_alignment_operator_maximum_frobenius_defect": float(
                np.max(
                    np.linalg.norm(
                        aligned_hamiltonians - direct_hamiltonians,
                        axis=(1, 2),
                    )
                )
            ),
            "wannier90_represented_eigenvalue_maximum_defect": float(
                np.max(np.abs(np.linalg.eigvalsh(wannier_hamiltonians) - energies))
            ),
            "unaligned_direct_vs_wannier90_hopping_l2_defect": float(
                np.linalg.norm(direct_hoppings - wannier_hoppings)
            ),
            "aligned_direct_vs_wannier90_hopping_l2_defect": float(
                np.linalg.norm(direct_hoppings - aligned_hoppings)
            ),
            "hr_matrix_maximum_defect_from_u_matrix_transform": float(
                np.max(np.abs(hr_hamiltonians - wannier_hamiltonians))
            ),
            "hr_training_eigenvalue_maximum_error": float(
                np.max(np.abs(np.linalg.eigvalsh(hr_hamiltonians) - energies))
            ),
            "range_study": range_records,
            "u_matrices": self._complex_array(unitaries),
            "artifact_identities": [
                {
                    "name": path.name,
                    "bytes": path.stat().st_size,
                    "sha256": self._sha256(path),
                }
                for path in source_paths
            ],
        }

    @staticmethod
    def _read_u_matrix(path: Path) -> tuple[RealVector, ComplexArray3]:
        lines = path.read_text(encoding="utf-8").splitlines()
        mesh_size, row_count, column_count = map(int, lines[1].split())
        if row_count != 2 or column_count != 2:
            raise ValueError("u-matrix must contain 2x2 matrices")
        momenta = np.empty(mesh_size, dtype=np.float64)
        matrices = np.empty((mesh_size, 2, 2), dtype=np.complex128)
        line_index = 2
        for k_index in range(mesh_size):
            while not lines[line_index].strip():
                line_index += 1
            momentum_fields = lines[line_index].split()
            momenta[k_index] = float(momentum_fields[0])
            line_index += 1
            for column in range(2):
                for row in range(2):
                    fields = lines[line_index].split()
                    matrices[k_index, row, column] = complex(
                        float(fields[0]), float(fields[1])
                    )
                    line_index += 1
        return momenta, matrices

    @staticmethod
    def _parent_states(
        specification: ExtractionInput,
        momenta: RealVector,
        lower: int,
        upper: int,
    ) -> tuple[RealMatrix, ComplexArray3, ComplexArray3]:
        dimension = 2 * specification.cutoff + 1
        indices = np.arange(-specification.cutoff, specification.cutoff + 1)
        energies = np.empty((momenta.size, 2), dtype=np.float64)
        frames = np.empty((momenta.size, dimension, 2), dtype=np.complex128)
        matrices = np.empty(
            (momenta.size, dimension, dimension), dtype=np.complex128
        )
        for k_index, momentum in enumerate(momenta):
            matrix = np.diag(np.square(momentum + indices)).astype(np.complex128)
            coupling = 0.5 * specification.strength
            matrix += np.diag(np.full(dimension - 1, coupling), 1)
            matrix += np.diag(np.full(dimension - 1, coupling), -1)
            values, vectors = np.linalg.eigh(matrix)
            energies[k_index] = values[lower : upper + 1]
            frames[k_index] = vectors[:, lower : upper + 1]
            matrices[k_index] = matrix
        return energies, frames, matrices

    def _direct_frames(
        self, raw_frames: ComplexArray3
    ) -> tuple[ComplexArray3, RealVector]:
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
            fraction = index / frames.shape[0]
            root = (
                eigenvectors
                @ np.diag(np.exp(1j * phases * fraction))
                @ eigenvectors.conj().T
            )
            frames[index] = frames[index] @ root
        return frames, phases

    @staticmethod
    def _sew(frame: ComplexMatrix) -> ComplexMatrix:
        result = np.zeros_like(frame)
        result[:-1] = frame[1:]
        return result

    @staticmethod
    def _align_frames(
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
    def _represented_hamiltonians(
        frames: ComplexArray3, parent_matrices: ComplexArray3
    ) -> ComplexArray3:
        return np.einsum(
            "kdi,kde,kej->kij",
            frames.conj(),
            parent_matrices,
            frames,
            optimize=True,
        )

    @staticmethod
    def _final_localization(
        wout: str,
    ) -> tuple[npt.NDArray[np.float64], RealVector, dict[str, JsonValue]]:
        final_index = wout.rfind("Final State")
        if final_index < 0:
            raise ValueError("wout lacks a Final State")
        final_text = wout[final_index:]
        pattern = re.compile(
            r"WF centre and spread\s+\d+\s+\(\s*"
            r"([-+0-9.Ee]+),\s*([-+0-9.Ee]+),\s*([-+0-9.Ee]+)\s*\)\s*"
            r"([-+0-9.Ee]+)"
        )
        matches = pattern.findall(final_text)
        if len(matches) < 2:
            raise ValueError("wout lacks two final centers and spreads")
        centers = np.asarray(
            [[float(value) for value in match[:3]] for match in matches[:2]],
            dtype=np.float64,
        )
        spreads = np.asarray(
            [float(match[3]) for match in matches[:2]], dtype=np.float64
        )
        omega: dict[str, JsonValue] = {}
        for key, label in (
            ("omega_i", "Omega I"),
            ("omega_d", "Omega D"),
            ("omega_od", "Omega OD"),
            ("omega_total", "Omega Total"),
        ):
            match = re.search(rf"{label}\s+=\s+([-+0-9.Ee]+)", final_text)
            if match is None:
                raise ValueError(f"wout lacks {label}")
            omega[key] = float(match.group(1))
        return centers, spreads, omega

    @staticmethod
    def _maximum_iteration(wout: str) -> int:
        values = [
            int(match.group(1))
            for match in re.finditer(r"^\s*(\d+)\s+[-+0-9.E]+.*<-- CONV$", wout, re.M)
        ]
        if not values:
            raise ValueError("wout lacks iteration records")
        return max(values)

    @staticmethod
    def _center_set_defect(direct: RealVector, wannier: RealVector) -> float:
        direct_sorted = np.sort(((direct + 0.5) % 1.0) - 0.5)
        wannier_sorted = np.sort(((wannier + 0.5) % 1.0) - 0.5)
        differences = ((direct_sorted - wannier_sorted + 0.5) % 1.0) - 0.5
        return float(np.max(np.abs(differences)))

    @staticmethod
    def _read_hr(path: Path, momenta: RealVector) -> tuple[RealVector, ComplexArray3]:
        lines = path.read_text(encoding="utf-8").splitlines()
        num_wann = int(lines[1])
        representative_count = int(lines[2])
        if num_wann != 2:
            raise ValueError("hr file must contain two Wannier functions")
        line_index = 3
        degeneracies: list[int] = []
        while len(degeneracies) < representative_count:
            degeneracies.extend(int(value) for value in lines[line_index].split())
            line_index += 1
        representatives = np.empty((representative_count, 3), dtype=np.int64)
        blocks = np.empty((representative_count, 2, 2), dtype=np.complex128)
        for representative_index in range(representative_count):
            block = np.empty((2, 2), dtype=np.complex128)
            for _ in range(4):
                fields = lines[line_index].split()
                line_index += 1
                representatives[representative_index] = [
                    int(fields[0]),
                    int(fields[1]),
                    int(fields[2]),
                ]
                row = int(fields[3]) - 1
                column = int(fields[4]) - 1
                block[row, column] = complex(float(fields[5]), float(fields[6]))
            blocks[representative_index] = block
        phases = np.exp(
            2j * np.pi * np.outer(momenta, representatives[:, 0])
        )
        hamiltonians = np.einsum("kr,rij->kij", phases, blocks, optimize=True)
        return momenta.copy(), hamiltonians

    @staticmethod
    def _complex_array(values: ComplexArray3) -> list[JsonValue]:
        return [
            [
                [[float(value.real), float(value.imag)] for value in row]
                for row in matrix
            ]
            for matrix in values
        ]

    @staticmethod
    def _real_array(values: npt.NDArray[np.float64]) -> list[JsonValue]:
        return [[float(value) for value in row] for row in values]

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


class CommandAdapter:
    """Adapt composite input, external run, and retained output paths."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=Path, required=True)
        parser.add_argument("--workdir", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(argv)
        input_path = cast(Path, args.input).resolve()
        specification = ExtractionInputDeserializer().execute(input_path.read_bytes())
        Wannier90ResultExtractor().execute(
            specification,
            input_path,
            cast(Path, args.workdir).resolve(),
            cast(Path, args.output).resolve(),
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
