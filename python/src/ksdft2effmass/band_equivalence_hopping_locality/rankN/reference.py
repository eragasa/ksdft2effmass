"""Independent dimension-neutral parent and alignment reference arithmetic."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array


@dataclass(frozen=True, slots=True)
class _ExpectedFittedEvidence:
    sample_count: int
    minimum_numerical_rank: int
    minimum_cross_singular_value: float
    maximum_optimal_residual_frobenius_norm: float
    maximum_applied_rank_cutoff: float


@dataclass(frozen=True, slots=True)
class _ExpectedAlignment:
    maximum_aligned_frame_defect: float
    maximum_direct_matrix_difference: float
    fitted_evidence: _ExpectedFittedEvidence | None


@dataclass(frozen=True, slots=True)
class _ExpectedAlignmentInventory:
    identity: _ExpectedAlignment
    global_unitary: _ExpectedAlignment
    pointwise_unitary: _ExpectedAlignment
    known_inverse_oracle: _ExpectedAlignment


class _IndependentPeriodicRankNCase:
    """Reconstruct selected formulas without invoking maintained model owners."""

    __slots__ = (
        "_transformation_coefficient",
        "_axis_maximum_normalization",
        "_circuit_depth",
        "_parent_scale",
        "_positive_bonds",
        "_rank",
        "_spatial_dimension",
    )

    def __init__(
        self,
        *,
        spatial_dimension: int,
        positive_bonds: tuple[tuple[int, ...], ...],
        axis_maximum_normalization: bool,
        retained_rank: int,
        circuit_depth: int,
        parent_scale: float,
        transformation_coefficient: float,
    ) -> None:
        self._spatial_dimension = spatial_dimension
        self._positive_bonds = positive_bonds
        self._axis_maximum_normalization = axis_maximum_normalization
        self._rank = retained_rank
        self._circuit_depth = circuit_depth
        self._parent_scale = parent_scale
        self._transformation_coefficient = transformation_coefficient

    def coordinates(self, size: int, offset: float) -> Float64Array:
        axis = -0.5 + (np.arange(size, dtype=np.float64) + offset) / float(size)
        axes = tuple(axis for _ in range(self._spatial_dimension))
        return np.asarray(
            np.stack(np.meshgrid(*axes, indexing="ij"), axis=-1),
            dtype=np.float64,
        )

    def _orbital_coordinates(self) -> Float64Array:
        orbital = np.arange(self._rank, dtype=np.float64)
        return np.asarray(
            (2.0 * orbital - self._rank + 1.0) / (self._rank - 1.0),
            dtype=np.float64,
        )

    def _arguments(self, coordinates: Float64Array) -> Float64Array:
        bonds = np.asarray(self._positive_bonds, dtype=np.float64)
        return np.asarray(
            2.0 * np.pi * np.einsum("...d,bd->...b", coordinates, bonds),
            dtype=np.float64,
        )

    def structure_factor(self, coordinates: Float64Array) -> Float64Array:
        arguments = self._arguments(coordinates)
        return np.asarray(
            np.mean(
                0.75 * np.cos(arguments) + 0.25 * np.cos(2.0 * arguments),
                axis=-1,
            ),
            dtype=np.float64,
        )

    def retained_energies(self, coordinates: Float64Array) -> Float64Array:
        orbital = self._orbital_coordinates()
        structure = self.structure_factor(coordinates)
        return np.asarray(
            0.4 * orbital
            + 0.25 * self._parent_scale * (1.0 + 0.2 * orbital) * structure[..., None],
            dtype=np.float64,
        )

    def exterior_energies(self, coordinates: Float64Array) -> Float64Array:
        orbital = self._orbital_coordinates()
        structure = self.structure_factor(coordinates)
        return np.asarray(
            3.0 + 0.3 * orbital + 0.1 * self._parent_scale * structure[..., None],
            dtype=np.float64,
        )

    def exact_operators(self, coordinates: Float64Array) -> Complex128Array:
        energies = self.retained_energies(coordinates)
        return np.asarray(
            energies[..., :, None] * np.eye(self._rank, dtype=np.complex128),
            dtype=np.complex128,
        )

    def gauges(self, coordinates: Float64Array) -> Complex128Array:
        arguments = self._arguments(coordinates)
        identity = np.eye(self._rank, dtype=np.complex128)
        gauges = np.broadcast_to(
            identity,
            (*coordinates.shape[:-1], self._rank, self._rank),
        ).copy()
        normalization = (
            1.0 / float(self._spatial_dimension)
            if self._axis_maximum_normalization
            else math.sqrt(2.0 / float(len(self._positive_bonds)))
        )
        for layer_index in range(1, self._circuit_depth + 1):
            harmonic = 0.75 * np.sin(arguments) + 0.25 * (
                (-1.0) ** layer_index
            ) * np.sin(2.0 * arguments)
            scalar = normalization * np.sum(harmonic, axis=-1)
            layer = np.broadcast_to(
                identity,
                (*coordinates.shape[:-1], self._rank, self._rank),
            ).copy()
            first_left = 0 if layer_index % 2 == 1 else 1
            for left in range(first_left, self._rank - 1, 2):
                pair_index = left + 1
                pair_coordinate = (2.0 * pair_index - self._rank) / (self._rank - 1.0)
                weight = (1.0 + 0.15 * pair_coordinate) / 1.15
                angle = (
                    self._transformation_coefficient
                    * (-1.0) ** (layer_index + pair_index)
                    * weight
                    * scalar
                )
                cosine = np.cos(angle)
                sine = np.sin(angle)
                layer[..., left, left] = cosine
                layer[..., left, left + 1] = -sine
                layer[..., left + 1, left] = sine
                layer[..., left + 1, left + 1] = cosine
            gauges = gauges @ layer
        return np.asarray(gauges, dtype=np.complex128)

    def minimum_gap(self, construction_coordinates: Float64Array) -> float:
        retained = self.retained_energies(construction_coordinates)
        exterior = self.exterior_energies(construction_coordinates)
        return float(np.min(exterior[..., 0] - retained[..., -1]))

    @staticmethod
    def _right_polar_factor(cross: Complex128Array) -> Complex128Array:
        gram = cross.conjugate().T @ cross
        eigenvalues, eigenvectors = np.linalg.eigh(gram)
        if bool((eigenvalues <= 0.0).any()):
            raise ValueError("bounded reference requires a positive cross Gram matrix")
        inverse_square_root = (
            eigenvectors * (1.0 / np.sqrt(eigenvalues))[None, :]
        ) @ eigenvectors.conjugate().T
        return np.asarray(cross @ inverse_square_root, dtype=np.complex128)

    @staticmethod
    def _maximum_frobenius(
        left: Complex128Array,
        right: Complex128Array,
    ) -> float:
        return float(np.max(np.linalg.norm(left - right, axis=(-2, -1))))

    @staticmethod
    def _cutoff(largest_singular_value: float) -> float:
        return max(1.0e-12, 1.0e-10 * largest_singular_value)

    def alignments(
        self,
        construction_coordinates: Float64Array,
        evaluation_coordinates: Float64Array,
    ) -> _ExpectedAlignmentInventory:
        rank = self._rank
        identity = np.eye(rank, dtype=np.complex128)
        construction_gauge = self.gauges(construction_coordinates)
        evaluation_gauge = self.gauges(evaluation_coordinates)
        exact_evaluation = self.exact_operators(evaluation_coordinates)
        gauge_transformed_evaluation = np.asarray(
            np.swapaxes(evaluation_gauge.conjugate(), -1, -2)
            @ exact_evaluation
            @ evaluation_gauge,
            dtype=np.complex128,
        )

        global_cross = np.sum(
            np.swapaxes(construction_gauge.conjugate(), -1, -2),
            axis=tuple(range(construction_gauge.ndim - 2)),
        )
        global_right = self._right_polar_factor(global_cross)
        global_singular_values = np.sqrt(
            np.maximum(
                np.linalg.eigvalsh(global_cross.conjugate().T @ global_cross), 0.0
            )
        )[::-1]
        global_difference = construction_gauge @ global_right - identity
        global_residual = float(np.linalg.norm(global_difference.reshape(-1, rank)))
        global_cutoff = self._cutoff(float(global_singular_values[0]))
        global_evidence = _ExpectedFittedEvidence(
            sample_count=1,
            minimum_numerical_rank=int(
                np.count_nonzero(global_singular_values > global_cutoff)
            ),
            minimum_cross_singular_value=float(global_singular_values[-1]),
            maximum_optimal_residual_frobenius_norm=global_residual,
            maximum_applied_rank_cutoff=global_cutoff,
        )
        pointwise_cutoff = self._cutoff(1.0)
        pointwise_evidence = _ExpectedFittedEvidence(
            sample_count=(
                math.prod(construction_coordinates.shape[:-1])
                + math.prod(evaluation_coordinates.shape[:-1])
            ),
            minimum_numerical_rank=rank,
            minimum_cross_singular_value=1.0,
            maximum_optimal_residual_frobenius_norm=0.0,
            maximum_applied_rank_cutoff=pointwise_cutoff,
        )
        global_evaluation = np.asarray(
            global_right.conjugate().T @ gauge_transformed_evaluation @ global_right,
            dtype=np.complex128,
        )
        return _ExpectedAlignmentInventory(
            identity=_ExpectedAlignment(
                maximum_aligned_frame_defect=self._maximum_frobenius(
                    construction_gauge,
                    identity,
                ),
                maximum_direct_matrix_difference=self._maximum_frobenius(
                    gauge_transformed_evaluation,
                    exact_evaluation,
                ),
                fitted_evidence=None,
            ),
            global_unitary=_ExpectedAlignment(
                maximum_aligned_frame_defect=self._maximum_frobenius(
                    construction_gauge @ global_right,
                    identity,
                ),
                maximum_direct_matrix_difference=self._maximum_frobenius(
                    global_evaluation,
                    exact_evaluation,
                ),
                fitted_evidence=global_evidence,
            ),
            pointwise_unitary=_ExpectedAlignment(
                maximum_aligned_frame_defect=0.0,
                maximum_direct_matrix_difference=0.0,
                fitted_evidence=pointwise_evidence,
            ),
            known_inverse_oracle=_ExpectedAlignment(
                maximum_aligned_frame_defect=0.0,
                maximum_direct_matrix_difference=0.0,
                fitted_evidence=None,
            ),
        )
