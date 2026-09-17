#!/usr/bin/env python3
"""Run the direct composite-band periodic-reduction experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
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
class BandGroup:
    """Identify one contiguous two-band retained subspace."""

    identifier: str
    lower: int
    upper: int


@dataclass(frozen=True, slots=True)
class CompositeInput:
    """Represent the frozen direct composite-band calculation."""

    experiment_id: str
    period: float
    potential_strength: float
    plane_wave_cutoff: int
    reciprocal_mesh_size: int
    withheld_mesh_size: int
    band_groups: tuple[BandGroup, ...]
    hopping_ranges: tuple[int, ...]
    external_gap_threshold: float
    direct_route_range: int
    controlled_gauge_amplitude: float
    rough_gauge_amplitude: float


class CompositeInputDeserializer:
    """Deserialize and validate the closed version-1 input."""

    __slots__ = ()

    def execute(self, payload: bytes) -> CompositeInput:
        value = cast(JsonValue, json.loads(payload.decode("utf-8")))
        root = self._mapping(value)
        if root["schema_version"] != 1:
            raise ValueError("unsupported composite input schema version")
        if root["evidence_status"] != "illustrative numerical verification":
            raise ValueError("unexpected evidence status")
        groups = self._groups(root["retained_band_groups"])
        result = CompositeInput(
            experiment_id=self._string(root["experiment_id"]),
            period=self._positive_real(root["period"]),
            potential_strength=self._real(root["potential_strength_over_recoil"]),
            plane_wave_cutoff=self._positive_integer(root["plane_wave_cutoff"]),
            reciprocal_mesh_size=self._positive_integer(
                root["reciprocal_mesh_size"]
            ),
            withheld_mesh_size=self._positive_integer(root["withheld_mesh_size"]),
            band_groups=groups,
            hopping_ranges=self._integers(root["hopping_ranges_cells"]),
            external_gap_threshold=self._positive_real(
                root["external_gap_threshold"]
            ),
            direct_route_range=self._integer(root["direct_route_range_cells"]),
            controlled_gauge_amplitude=self._real(
                root["controlled_gauge_amplitude"]
            ),
            rough_gauge_amplitude=self._real(root["rough_gauge_amplitude"]),
        )
        if result.reciprocal_mesh_size % 2 != 0:
            raise ValueError("reciprocal mesh size must be even")
        if result.withheld_mesh_size < result.reciprocal_mesh_size:
            raise ValueError("withheld mesh must be denser than the training mesh")
        if tuple(sorted(set(result.hopping_ranges))) != result.hopping_ranges:
            raise ValueError("hopping ranges must be strictly increasing")
        if result.direct_route_range not in result.hopping_ranges:
            raise ValueError("direct-route range must be in the hopping hierarchy")
        return result

    def _groups(self, value: JsonValue) -> tuple[BandGroup, ...]:
        entries = self._array(value)
        groups: list[BandGroup] = []
        for entry in entries:
            item = self._mapping(entry)
            bands = self._integers(item["band_indices"])
            if len(bands) != 2 or bands[1] != bands[0] + 1:
                raise ValueError(
                    "each retained group must contain two contiguous bands"
                )
            groups.append(
                BandGroup(
                    identifier=self._string(item["id"]),
                    lower=bands[0],
                    upper=bands[1],
                )
            )
        if len({group.identifier for group in groups}) != len(groups):
            raise ValueError("band-group identifiers must be unique")
        return tuple(groups)

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
        if not isinstance(value, str) or not value:
            raise TypeError("value must be a nonempty string")
        return value

    @staticmethod
    def _real(value: JsonValue) -> float:
        if isinstance(value, bool) or not isinstance(value, int | float):
            raise TypeError("value must be a number")
        result = float(value)
        if not np.isfinite(result):
            raise ValueError("value must be finite")
        return result

    def _positive_real(self, value: JsonValue) -> float:
        result = self._real(value)
        if result <= 0.0:
            raise ValueError("value must be positive")
        return result

    @staticmethod
    def _integer(value: JsonValue) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("value must be an integer")
        return value

    def _positive_integer(self, value: JsonValue) -> int:
        result = self._integer(value)
        if result <= 0:
            raise ValueError("value must be positive")
        return result

    def _integers(self, value: JsonValue) -> tuple[int, ...]:
        return tuple(self._integer(item) for item in self._array(value))


class CompositeBandExperiment:
    """Construct, attack, align, and truncate direct composite-band operators."""

    __slots__ = ()

    def execute(
        self, specification: CompositeInput, input_path: Path, script_path: Path
    ) -> bytes:
        momenta, parent_matrices, eigenvalues, eigenvectors = self._parent_mesh(
            specification
        )
        withheld_momenta, _, withheld_values, _ = self._parent_mesh(
            specification, mesh_size=specification.withheld_mesh_size, endpoint=True
        )
        groups: list[JsonValue] = []
        for group in specification.band_groups:
            groups.append(
                self._group_result(
                    specification,
                    group,
                    momenta,
                    parent_matrices,
                    eigenvalues,
                    eigenvectors,
                    withheld_momenta,
                    withheld_values,
                )
            )
        repository_root = script_path.parents[3]
        payload: dict[str, JsonValue] = {
            "schema_version": 1,
            "experiment_id": specification.experiment_id,
            "evidence_status": "illustrative numerical verification",
            "calculation_status": "calculated illustrative result",
            "conventions": {
                "basis_order": "plane waves n=-P,...,P",
                "reciprocal_mesh": "uniform half-open [-1/2,1/2)",
                "sewing": "coefficient shift under k -> k+1",
                "overlap_inner_product": (
                    "orthonormal plane-wave coefficient inner product"
                ),
                "hopping_transform": "T_R=N_k^-1 sum_k exp(-ikRa) H(k)",
                "matrix_norm": "Frobenius",
                "energy_unit": "E_G",
                "length_unit": "a",
            },
            "groups": groups,
            "provenance": {
                "input_path": input_path.relative_to(repository_root).as_posix(),
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                "script_path": script_path.relative_to(repository_root).as_posix(),
                "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
                "python_version": platform.python_version(),
                "numpy_version": np.__version__,
                "floating_point": "IEEE-754 binary64",
            },
            "claim_boundary": (
                "Direct two-band composite-space numerical verification in the "
                "frozen one-dimensional cosine model; no Wannier90 execution, "
                "material validation, or uncertainty quantification."
            ),
        }
        serialized = json.dumps(
            payload, indent=2, sort_keys=True, allow_nan=False
        )
        return (serialized + "\n").encode("utf-8")

    def _group_result(
        self,
        specification: CompositeInput,
        group: BandGroup,
        momenta: RealVector,
        parent_matrices: ComplexArray3,
        eigenvalues: RealMatrix,
        eigenvectors: ComplexArray3,
        withheld_momenta: RealVector,
        withheld_values: RealMatrix,
    ) -> dict[str, JsonValue]:
        raw_frames = eigenvectors[:, :, group.lower : group.upper + 1]
        minimum_singular_value = self._minimum_neighbor_singular_value(raw_frames)
        smooth_frames, wilson_phases = self._closed_polar_frames(raw_frames)
        controlled_raw = self._apply_controlled_gauge(
            raw_frames, specification.controlled_gauge_amplitude
        )
        attacked_frames, attacked_wilson_phases = self._closed_polar_frames(
            controlled_raw
        )
        projector_defect = self._projector_defect(raw_frames, controlled_raw)
        aligned_frames, alignment_defect = self._align_frames(
            smooth_frames, attacked_frames
        )

        smooth_hamiltonians = self._represented_hamiltonians(
            smooth_frames, parent_matrices
        )
        attacked_hamiltonians = self._represented_hamiltonians(
            attacked_frames, parent_matrices
        )
        aligned_hamiltonians = self._represented_hamiltonians(
            aligned_frames, parent_matrices
        )
        alignment_operator_defect = float(
            np.max(
                np.linalg.norm(
                    aligned_hamiltonians - smooth_hamiltonians,
                    axis=(1, 2),
                )
            )
        )
        eigenvalue_covariance_defect = self._eigenvalue_defect(
            attacked_hamiltonians,
            eigenvalues[:, group.lower : group.upper + 1],
        )
        wilson_phase_defect = self._phase_set_defect(
            wilson_phases, attacked_wilson_phases
        )

        rough_frames = self._apply_rough_gauge(
            smooth_frames, specification.rough_gauge_amplitude
        )
        rough_hamiltonians = self._represented_hamiltonians(
            rough_frames, parent_matrices
        )
        representatives = np.arange(
            -specification.reciprocal_mesh_size // 2,
            specification.reciprocal_mesh_size // 2,
        )
        smooth_hoppings = self._hoppings(
            momenta, smooth_hamiltonians, representatives, specification.period
        )
        rough_hoppings = self._hoppings(
            momenta, rough_hamiltonians, representatives, specification.period
        )
        smooth_reconstruction = self._reconstruct(
            momenta, smooth_hoppings, representatives, specification.period
        )
        rough_reconstruction = self._reconstruct(
            momenta, rough_hoppings, representatives, specification.period
        )
        smooth_reconstruction_error = float(
            np.max(
                np.linalg.norm(
                    smooth_reconstruction - smooth_hamiltonians,
                    axis=(1, 2),
                )
            )
        )
        rough_reconstruction_error = float(
            np.max(
                np.linalg.norm(
                    rough_reconstruction - rough_hamiltonians,
                    axis=(1, 2),
                )
            )
        )
        hermiticity_residual = self._hopping_hermiticity_residual(
            smooth_hoppings, representatives
        )
        target_withheld = withheld_values[:, group.lower : group.upper + 1]
        range_study: list[JsonValue] = []
        for hopping_range in specification.hopping_ranges:
            range_study.append(
                self._range_record(
                    hopping_range,
                    momenta,
                    withheld_momenta,
                    eigenvalues[:, group.lower : group.upper + 1],
                    target_withheld,
                    representatives,
                    smooth_hoppings,
                    rough_hoppings,
                    specification.period,
                )
            )

        direct_record = self._direct_route_record(
            specification.direct_route_range,
            momenta,
            smooth_hamiltonians,
            representatives,
            smooth_hoppings,
            specification.period,
        )
        unaligned_hopping_defect = float(
            np.sqrt(np.sum(np.abs(rough_hoppings - smooth_hoppings) ** 2))
        )
        external_gap, internal_gap = self._group_gaps(
            group, withheld_values
        )
        return {
            "id": group.identifier,
            "band_indices": [group.lower, group.upper],
            "internal_minimum_gap": internal_gap,
            "external_minimum_gap": external_gap,
            "external_isolation_status": (
                "pass"
                if external_gap > specification.external_gap_threshold
                else "failed"
            ),
            "neighbor_overlap_minimum_singular_value": minimum_singular_value,
            "wilson_loop_eigenphases": [float(value) for value in wilson_phases],
            "controlled_gauge_wilson_phase_set_defect": wilson_phase_defect,
            "controlled_gauge_projector_maximum_frobenius_defect": projector_defect,
            "pointwise_alignment_frame_maximum_frobenius_defect": alignment_defect,
            "pointwise_alignment_operator_maximum_frobenius_defect": (
                alignment_operator_defect
            ),
            "controlled_gauge_eigenvalue_maximum_defect": (
                eigenvalue_covariance_defect
            ),
            "smooth_full_reconstruction_maximum_frobenius_error": (
                smooth_reconstruction_error
            ),
            "rough_full_reconstruction_maximum_frobenius_error": (
                rough_reconstruction_error
            ),
            "smooth_hopping_hermiticity_maximum_frobenius_residual": (
                hermiticity_residual
            ),
            "rough_vs_smooth_unaligned_hopping_l2_defect": (
                unaligned_hopping_defect
            ),
            "range_study": range_study,
            "direct_route": direct_record,
            "represented_reciprocal_hamiltonians": self._complex_array(
                smooth_hamiltonians
            ),
            "smooth_hopping_blocks": self._hopping_records(
                representatives, smooth_hoppings
            ),
            "rough_hopping_blocks": self._hopping_records(
                representatives, rough_hoppings
            ),
            "identities": {
                "smooth_frame_sha256": self._array_sha256(smooth_frames),
                "smooth_projector_sha256": self._array_sha256(
                    self._projectors(smooth_frames)
                ),
                "smooth_reciprocal_hamiltonian_sha256": self._array_sha256(
                    smooth_hamiltonians
                ),
                "smooth_hopping_sha256": self._array_sha256(smooth_hoppings),
                "rough_hopping_sha256": self._array_sha256(rough_hoppings),
            },
        }

    def _parent_mesh(
        self,
        specification: CompositeInput,
        *,
        mesh_size: int | None = None,
        endpoint: bool = False,
    ) -> tuple[RealVector, ComplexArray3, RealMatrix, ComplexArray3]:
        count = specification.reciprocal_mesh_size if mesh_size is None else mesh_size
        momenta = (
            np.linspace(-0.5, 0.5, count)
            if endpoint
            else -0.5 + np.arange(count, dtype=np.float64) / count
        )
        dimension = 2 * specification.plane_wave_cutoff + 1
        required_bands = max(group.upper for group in specification.band_groups) + 2
        matrices = np.empty((count, dimension, dimension), dtype=np.complex128)
        values = np.empty((count, required_bands), dtype=np.float64)
        vectors = np.empty(
            (count, dimension, required_bands), dtype=np.complex128
        )
        for index, momentum in enumerate(momenta):
            matrix = self._parent_matrix(
                float(momentum),
                specification.potential_strength,
                specification.plane_wave_cutoff,
            )
            eigenvalue, eigenvector = np.linalg.eigh(matrix)
            matrices[index] = matrix
            values[index] = eigenvalue[:required_bands]
            vectors[index] = eigenvector[:, :required_bands]
        return momenta, matrices, values, vectors

    @staticmethod
    def _parent_matrix(
        momentum: float, strength: float, cutoff: int
    ) -> ComplexMatrix:
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.diag(np.square(momentum + indices)).astype(np.complex128)
        coupling = 0.5 * strength
        matrix += np.diag(np.full(2 * cutoff, coupling), 1)
        matrix += np.diag(np.full(2 * cutoff, coupling), -1)
        return matrix

    def _minimum_neighbor_singular_value(self, frames: ComplexArray3) -> float:
        singular_values: list[float] = []
        for index in range(frames.shape[0] - 1):
            overlap = frames[index].conj().T @ frames[index + 1]
            singular_values.extend(np.linalg.svd(overlap, compute_uv=False).tolist())
        closure = frames[-1].conj().T @ self._sew(frames[0])
        singular_values.extend(np.linalg.svd(closure, compute_uv=False).tolist())
        return min(singular_values)

    def _closed_polar_frames(
        self, raw_frames: ComplexArray3
    ) -> tuple[ComplexArray3, RealVector]:
        frames = raw_frames.copy()
        for index in range(frames.shape[0] - 1):
            overlap = frames[index].conj().T @ raw_frames[index + 1]
            left, _, right_h = np.linalg.svd(overlap)
            rotation = right_h.conj().T @ left.conj().T
            frames[index + 1] = raw_frames[index + 1] @ rotation
        closure = frames[-1].conj().T @ self._sew(frames[0])
        left, _, right_h = np.linalg.svd(closure)
        unitary_closure = left @ right_h
        triangular, eigenvectors = schur(unitary_closure, output="complex")
        phases = np.angle(np.diag(triangular)).astype(np.float64)
        order = np.argsort(phases)
        phases = phases[order]
        eigenvectors = eigenvectors[:, order]
        count = frames.shape[0]
        for index in range(count):
            fraction = index / count
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
    def _apply_controlled_gauge(
        frames: ComplexArray3, amplitude: float
    ) -> ComplexArray3:
        result = np.empty_like(frames)
        count = frames.shape[0]
        for index in range(count):
            coordinate = index / count
            angle = amplitude * np.sin(2.0 * np.pi * coordinate)
            first_phase = 0.31 * np.cos(2.0 * np.pi * coordinate)
            second_phase = -0.27 * np.sin(4.0 * np.pi * coordinate)
            rotation = np.asarray(
                [
                    [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)],
                ],
                dtype=np.complex128,
            )
            phases = np.diag(np.exp(1j * np.asarray([first_phase, second_phase])))
            result[index] = frames[index] @ rotation @ phases
        return result

    @staticmethod
    def _apply_rough_gauge(
        frames: ComplexArray3, amplitude: float
    ) -> ComplexArray3:
        result = np.empty_like(frames)
        for index in range(frames.shape[0]):
            sign = 1.0 if index % 2 == 0 else -1.0
            angle = amplitude * sign
            rotation = np.asarray(
                [
                    [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)],
                ],
                dtype=np.complex128,
            )
            phases = np.diag(
                np.exp(1j * np.asarray([0.43 * sign, -0.37 * sign]))
            )
            result[index] = frames[index] @ rotation @ phases
        return result

    @staticmethod
    def _projectors(frames: ComplexArray3) -> ComplexArray3:
        return np.einsum("kdi,kei->kde", frames, frames.conj(), optimize=True)

    def _projector_defect(
        self, first: ComplexArray3, second: ComplexArray3
    ) -> float:
        difference = self._projectors(first) - self._projectors(second)
        return float(np.max(np.linalg.norm(difference, axis=(1, 2))))

    @staticmethod
    def _align_frames(
        reference: ComplexArray3, candidate: ComplexArray3
    ) -> tuple[ComplexArray3, float]:
        aligned = np.empty_like(candidate)
        defects: list[float] = []
        for index in range(reference.shape[0]):
            overlap = candidate[index].conj().T @ reference[index]
            left, _, right_h = np.linalg.svd(overlap)
            rotation = left @ right_h
            aligned[index] = candidate[index] @ rotation
            defects.append(float(np.linalg.norm(aligned[index] - reference[index])))
        return aligned, max(defects)

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
    def _eigenvalue_defect(
        hamiltonians: ComplexArray3, target: RealMatrix
    ) -> float:
        represented = np.linalg.eigvalsh(hamiltonians)
        return float(np.max(np.abs(represented - target)))

    @staticmethod
    def _phase_set_defect(first: RealVector, second: RealVector) -> float:
        if first.shape != second.shape:
            raise ValueError("phase sets must have equal shape")
        differences = np.angle(np.exp(1j * (np.sort(first) - np.sort(second))))
        return float(np.max(np.abs(differences)))

    @staticmethod
    def _hoppings(
        momenta: RealVector,
        hamiltonians: ComplexArray3,
        representatives: npt.NDArray[np.int64],
        period: float,
    ) -> ComplexArray3:
        transform = np.exp(
            -1j * np.outer(representatives * period, momenta)
        ) / momenta.size
        return np.einsum("rk,kij->rij", transform, hamiltonians, optimize=True)

    @staticmethod
    def _reconstruct(
        momenta: RealVector,
        hoppings: ComplexArray3,
        representatives: npt.NDArray[np.int64],
        period: float,
    ) -> ComplexArray3:
        inverse = np.exp(1j * np.outer(momenta, representatives * period))
        return np.einsum("kr,rij->kij", inverse, hoppings, optimize=True)

    @staticmethod
    def _hopping_hermiticity_residual(
        hoppings: ComplexArray3, representatives: npt.NDArray[np.int64]
    ) -> float:
        lookup = {int(value): index for index, value in enumerate(representatives)}
        residuals: list[float] = []
        for index, representative in enumerate(representatives):
            opposite = lookup.get(-int(representative))
            if opposite is not None:
                residuals.append(
                    float(
                        np.linalg.norm(
                            hoppings[index] - hoppings[opposite].conj().T
                        )
                    )
                )
        return max(residuals)

    def _range_record(
        self,
        hopping_range: int,
        training_momenta: RealVector,
        withheld_momenta: RealVector,
        training_target: RealMatrix,
        withheld_target: RealMatrix,
        representatives: npt.NDArray[np.int64],
        smooth_hoppings: ComplexArray3,
        rough_hoppings: ComplexArray3,
        period: float,
    ) -> dict[str, JsonValue]:
        retained = np.abs(representatives) <= hopping_range
        smooth_training = self._reconstruct(
            training_momenta,
            smooth_hoppings[retained],
            representatives[retained],
            period,
        )
        rough_training = self._reconstruct(
            training_momenta,
            rough_hoppings[retained],
            representatives[retained],
            period,
        )
        smooth_withheld = self._reconstruct(
            withheld_momenta,
            smooth_hoppings[retained],
            representatives[retained],
            period,
        )
        rough_withheld = self._reconstruct(
            withheld_momenta,
            rough_hoppings[retained],
            representatives[retained],
            period,
        )
        return {
            "hopping_range_cells": hopping_range,
            "smooth_omitted_block_l2_norm": float(
                np.sqrt(np.sum(np.abs(smooth_hoppings[~retained]) ** 2))
            ),
            "rough_omitted_block_l2_norm": float(
                np.sqrt(np.sum(np.abs(rough_hoppings[~retained]) ** 2))
            ),
            "smooth_training_eigenvalue_maximum_error": self._band_error(
                smooth_training, training_target
            ),
            "rough_training_eigenvalue_maximum_error": self._band_error(
                rough_training, training_target
            ),
            "smooth_withheld_eigenvalue_maximum_error": self._band_error(
                smooth_withheld, withheld_target
            ),
            "rough_withheld_eigenvalue_maximum_error": self._band_error(
                rough_withheld, withheld_target
            ),
        }

    @staticmethod
    def _band_error(hamiltonians: ComplexArray3, target: RealMatrix) -> float:
        values = np.linalg.eigvalsh(hamiltonians)
        return float(np.max(np.abs(values - target)))

    def _direct_route_record(
        self,
        hopping_range: int,
        momenta: RealVector,
        hamiltonians: ComplexArray3,
        representatives: npt.NDArray[np.int64],
        mediated_hoppings: ComplexArray3,
        period: float,
    ) -> dict[str, JsonValue]:
        retained = np.abs(representatives) <= hopping_range
        retained_representatives = representatives[retained]
        design = np.exp(
            1j * np.outer(momenta, retained_representatives * period)
        )
        direct_flat = np.linalg.lstsq(
            design, hamiltonians.reshape(momenta.size, 4), rcond=None
        )[0]
        direct = direct_flat.reshape(retained_representatives.size, 2, 2)
        mediated = mediated_hoppings[retained]
        direct_model = self._reconstruct(
            momenta, direct, retained_representatives, period
        )
        mediated_model = self._reconstruct(
            momenta, mediated, retained_representatives, period
        )
        return {
            "hopping_range_cells": hopping_range,
            "coefficient_frobenius_defect": float(
                np.linalg.norm(direct - mediated)
            ),
            "training_operator_maximum_frobenius_defect": float(
                np.max(np.linalg.norm(direct_model - mediated_model, axis=(1, 2)))
            ),
        }

    @staticmethod
    def _group_gaps(group: BandGroup, values: RealMatrix) -> tuple[float, float]:
        internal = float(np.min(values[:, group.upper] - values[:, group.lower]))
        external_candidates: list[float] = []
        if group.lower > 0:
            external_candidates.append(
                float(np.min(values[:, group.lower] - values[:, group.lower - 1]))
            )
        if group.upper + 1 < values.shape[1]:
            external_candidates.append(
                float(np.min(values[:, group.upper + 1] - values[:, group.upper]))
            )
        return min(external_candidates), internal

    @staticmethod
    def _complex_array(values: ComplexArray3) -> list[JsonValue]:
        return [
            [
                [[float(entry.real), float(entry.imag)] for entry in row]
                for row in matrix
            ]
            for matrix in values
        ]

    def _hopping_records(
        self,
        representatives: npt.NDArray[np.int64],
        hoppings: ComplexArray3,
    ) -> list[JsonValue]:
        return [
            {
                "representative_cells": int(representative),
                "matrix": self._complex_array(hoppings[index : index + 1])[0],
                "frobenius_norm": float(np.linalg.norm(hoppings[index])),
            }
            for index, representative in enumerate(representatives)
        ]

    @staticmethod
    def _array_sha256(values: npt.NDArray[np.complex128]) -> str:
        canonical = np.ascontiguousarray(values, dtype="<c16")
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


class CommandAdapter:
    """Adapt command-line paths to the composite experiment."""

    __slots__ = ()

    def execute(self, argv: tuple[str, ...] | None = None) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--input", type=Path, required=True)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args(argv)
        input_path = cast(Path, args.input).resolve()
        output_path = cast(Path, args.output).resolve()
        script_path = Path(__file__).resolve()
        specification = CompositeInputDeserializer().execute(input_path.read_bytes())
        output_path.write_bytes(
            CompositeBandExperiment().execute(
                specification, input_path, script_path
            )
        )
        return 0


if __name__ == "__main__":
    raise SystemExit(CommandAdapter().execute())
