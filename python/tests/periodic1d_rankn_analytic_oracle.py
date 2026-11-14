"""Independent analytic oracle for periodic-1D finite-rank approximation tests."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray, RealArray

from ksdft2effmass.gauge_transformation import (
    FiniteRankGivensCircuit,
    FiniteRankGivensCircuitTransformationConstructor,
    FiniteRankGivensLayer,
    FiniteRankGivensRotation,
    SampledFiniteRankGaugeTransformation,
)
from ksdft2effmass.periodic1d.gauge_transformation import (
    Periodic1DFourierGivensGaugeTransformation,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNAnalyticOracleSample:
    """Retain exact parent and gauge-transformed fields on one supplied mesh."""

    reduced_coordinates: RealArray = field(repr=False)
    retained_energies: RealArray = field(repr=False)
    exterior_energies: RealArray = field(repr=False)
    parent_operators: ComplexArray = field(repr=False)
    reference_frames: ComplexArray = field(repr=False)
    reference_operators: ComplexArray = field(repr=False)
    transformation: SampledFiniteRankGaugeTransformation = field(repr=False)
    gauge_transformed_frames: ComplexArray = field(repr=False)
    gauge_transformed_operators: ComplexArray = field(repr=False)


class Periodic1DRankNAnalyticApproximationOracle:
    """Construct exact analytic fields independently of approximation code."""

    __slots__ = ()

    def sample(
        self,
        *,
        retained_rank: int,
        circuit_depth: int,
        reduced_coordinates: RealArray,
    ) -> Periodic1DRankNAnalyticOracleSample:
        """Return exact fields for one explicitly selected rank, depth, and mesh."""
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        if type(circuit_depth) is not int:
            raise TypeError("circuit_depth must be a built-in integer")
        if circuit_depth < 1:
            raise ValueError("circuit_depth must be positive")
        coordinates = NumpyImmutableArrayConstructor(
            reduced_coordinates,
            "reduced_coordinates",
            np.dtype(np.float64),
        ).execute()
        if coordinates.ndim != 1 or coordinates.size == 0:
            raise ValueError("reduced_coordinates must be a nonempty vector")

        retained = self._retained_energies(retained_rank, coordinates)
        exterior = self._exterior_energies(retained_rank, coordinates)
        reference_operators = self._diagonal_operators(retained)
        parent_operators = self._parent_operators(retained, exterior)
        reference_frames = self._reference_frames(coordinates.size, retained_rank)
        circuit = self._circuit(retained_rank, circuit_depth)
        angle_samples = self._angle_samples(
            retained_rank,
            circuit_depth,
            coordinates,
        )
        transformation = FiniteRankGivensCircuitTransformationConstructor(
            circuit=circuit,
            angle_samples=angle_samples,
        ).execute()
        return Periodic1DRankNAnalyticOracleSample(
            reduced_coordinates=coordinates,
            retained_energies=retained,
            exterior_energies=exterior,
            parent_operators=parent_operators,
            reference_frames=reference_frames,
            reference_operators=reference_operators,
            transformation=transformation,
            gauge_transformed_frames=transformation.transform_frames(reference_frames),
            gauge_transformed_operators=transformation.transform_operators(
                reference_operators
            ),
        )

    @staticmethod
    def exact_transformation_angle_maximum(retained_rank: int) -> float:
        """Return the analytic continuum maximum for the oracle schedule."""
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        q = (np.sqrt(41.0) - 3.0) / 8.0
        harmonic_maximum = np.sqrt(1.0 - q**2) * (0.75 + 0.5 * q)
        return float(
            0.35
            * (1.0 + 0.15 * (retained_rank - 2.0) / (retained_rank - 1.0))
            * harmonic_maximum
        )

    @staticmethod
    def _retained_energies(rank: int, coordinates: RealArray) -> RealArray:
        phase = 2.0 * np.pi * coordinates
        harmonic = 0.75 * np.cos(phase) + 0.25 * np.cos(2.0 * phase)
        orbital = np.arange(rank, dtype=np.float64)
        normalized = (2.0 * orbital - rank + 1.0) / (rank - 1.0)
        values = (
            0.4 * normalized[None, :]
            + 0.25 * (1.0 + 0.2 * normalized[None, :]) * harmonic[:, None]
        )
        return NumpyImmutableArrayConstructor(
            np.asarray(values, dtype=np.float64),
            "retained_energies",
            np.dtype(np.float64),
        ).execute()

    @staticmethod
    def _exterior_energies(rank: int, coordinates: RealArray) -> RealArray:
        phase = 2.0 * np.pi * coordinates
        harmonic = 0.75 * np.cos(phase) + 0.25 * np.cos(2.0 * phase)
        orbital = np.arange(rank, dtype=np.float64)
        normalized = (2.0 * orbital - rank + 1.0) / (rank - 1.0)
        values = 3.0 + 0.3 * normalized[None, :] + 0.1 * harmonic[:, None]
        return NumpyImmutableArrayConstructor(
            np.asarray(values, dtype=np.float64),
            "exterior_energies",
            np.dtype(np.float64),
        ).execute()

    @staticmethod
    def _diagonal_operators(energies: RealArray) -> ComplexArray:
        identity = np.eye(energies.shape[1], dtype=np.complex128)
        return NumpyImmutableArrayConstructor(
            np.asarray(
                energies[:, :, None] * identity[None, :, :],
                dtype=np.complex128,
            ),
            "reference_operators",
            np.dtype(np.complex128),
        ).execute()

    @staticmethod
    def _parent_operators(
        retained: RealArray,
        exterior: RealArray,
    ) -> ComplexArray:
        diagonal = np.concatenate((retained, exterior), axis=1)
        identity = np.eye(diagonal.shape[1], dtype=np.complex128)
        return NumpyImmutableArrayConstructor(
            np.asarray(
                diagonal[:, :, None] * identity[None, :, :],
                dtype=np.complex128,
            ),
            "parent_operators",
            np.dtype(np.complex128),
        ).execute()

    @staticmethod
    def _reference_frames(sample_count: int, rank: int) -> ComplexArray:
        frame = np.zeros((2 * rank, rank), dtype=np.complex128)
        frame[:rank] = np.eye(rank, dtype=np.complex128)
        return NumpyImmutableArrayConstructor(
            np.broadcast_to(frame, (sample_count, 2 * rank, rank)).copy(),
            "reference_frames",
            np.dtype(np.complex128),
        ).execute()

    @staticmethod
    def _circuit(rank: int, depth: int) -> FiniteRankGivensCircuit:
        return FiniteRankGivensCircuit(
            represented_rank=rank,
            layers=tuple(
                FiniteRankGivensLayer(
                    rotations=tuple(
                        FiniteRankGivensRotation(left, left + 1)
                        for left in range(
                            0 if layer_index % 2 == 1 else 1,
                            rank - 1,
                            2,
                        )
                    )
                )
                for layer_index in range(1, depth + 1)
            ),
        )

    @staticmethod
    def _angle_samples(
        rank: int,
        depth: int,
        coordinates: RealArray,
    ) -> RealArray:
        phase = 2.0 * np.pi * coordinates
        columns: list[np.ndarray] = []
        for layer_index in range(1, depth + 1):
            harmonic = 0.75 * np.sin(phase) + 0.25 * ((-1.0) ** layer_index) * np.sin(
                2.0 * phase
            )
            first_index = 0 if layer_index % 2 == 1 else 1
            for left in range(first_index, rank - 1, 2):
                pair_index = left + 1
                normalized_pair = (2.0 * pair_index - rank) / (rank - 1.0)
                columns.append(
                    0.35
                    * (-1.0) ** (layer_index + pair_index)
                    * (1.0 + 0.15 * normalized_pair)
                    * harmonic
                )
        return NumpyImmutableArrayConstructor(
            np.column_stack(columns).astype(np.float64, copy=False),
            "angle_samples",
            np.dtype(np.float64),
        ).execute()


def analytic_fourier_givens_transformation(
    *,
    retained_rank: int,
    circuit_depth: int,
) -> Periodic1DFourierGivensGaugeTransformation:
    """Return the explicit analytic transformation used by bounded tests."""
    circuit = Periodic1DRankNAnalyticApproximationOracle._circuit(
        retained_rank,
        circuit_depth,
    )
    sine_rows: list[tuple[float, float]] = []
    for layer_index in range(1, circuit_depth + 1):
        first_index = 0 if layer_index % 2 == 1 else 1
        for left in range(first_index, retained_rank - 1, 2):
            pair_index = left + 1
            normalized_pair = (2.0 * pair_index - retained_rank) / (retained_rank - 1.0)
            amplitude = (
                0.35
                * (-1.0) ** (layer_index + pair_index)
                * (1.0 + 0.15 * normalized_pair)
            )
            sine_rows.append(
                (
                    0.75 * amplitude,
                    0.25 * ((-1.0) ** layer_index) * amplitude,
                )
            )
    rotation_count = circuit.rotation_count
    return Periodic1DFourierGivensGaugeTransformation(
        transformation_identifier=(
            "periodic1d-rankN-test-analytic-fourier-givens:"
            f"r{retained_rank:02d}-L{circuit_depth:02d}"
        ),
        circuit=circuit,
        continuum_angle_maximum_bound=(
            Periodic1DRankNAnalyticApproximationOracle.exact_transformation_angle_maximum(
                retained_rank
            )
        ),
        constant_angles=np.zeros(rotation_count, dtype=np.float64),
        cosine_coefficients=np.zeros((rotation_count, 2), dtype=np.float64),
        sine_coefficients=np.asarray(sine_rows, dtype=np.float64),
    )


__all__ = [
    "Periodic1DRankNAnalyticApproximationOracle",
    "Periodic1DRankNAnalyticOracleSample",
    "analytic_fourier_givens_transformation",
]
