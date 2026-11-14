"""Synthetic right-acting gauge transformations for periodic-2D finite-rank fields."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import ClassVar

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor

from ksdft2effmass.gauge_transformation import (
    FiniteRankAlternatingNearestNeighborGivensCircuitConstructor,
    FiniteRankGivensCircuitTransformationConstructor,
    SampledFiniteRankGaugeTransformation,
)
from ksdft2effmass.serialization import StrWireEnum


class Periodic2DRankNGaugeNormalizationEnum(StrWireEnum):
    """Select the reviewed interpretation of one gauge-transformation coefficient."""

    AXIS_MAXIMUM = "axis-maximum"
    BOND_RMS = "bond-rms"


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNGivensGaugeTransformation:
    """Define and apply one bounded alternating Givens gauge transformation.

    The transformation acts only in retained coordinates. It owns no parent model,
    basis, geometry, mesh, or study identity.
    """

    TRANSFORMATION_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic2d-rankN-alternating-givens-transformation.v1"
    )

    retained_rank: int
    circuit_depth: int
    harmonic_bonds: tuple[tuple[int, int], ...]
    normalization: Periodic2DRankNGaugeNormalizationEnum
    coefficient: float

    def __post_init__(self) -> None:
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank < 2:
            raise ValueError("retained_rank must be at least two")
        if type(self.circuit_depth) is not int:
            raise TypeError("circuit_depth must be a built-in integer")
        if self.circuit_depth < 1:
            raise ValueError("circuit_depth must be positive")
        if type(self.harmonic_bonds) is not tuple or not self.harmonic_bonds:
            raise TypeError("harmonic_bonds must be a nonempty tuple")
        if any(
            type(bond) is not tuple
            or len(bond) != 2
            or any(type(component) is not int for component in bond)
            or bond == (0, 0)
            for bond in self.harmonic_bonds
        ):
            raise TypeError("harmonic_bonds must contain nonzero integer pairs")
        if len(set(self.harmonic_bonds)) != len(self.harmonic_bonds):
            raise ValueError("harmonic_bonds must be unique")
        if type(self.normalization) is not Periodic2DRankNGaugeNormalizationEnum:
            raise TypeError("normalization must be the exact periodic-2D enum")
        if type(self.coefficient) is not float:
            raise TypeError("coefficient must be a built-in float")
        if not math.isfinite(self.coefficient) or self.coefficient < 0.0:
            raise ValueError("coefficient must be finite and nonnegative")
        if self.angle_upper_bound > math.pi / 4.0 + 1.0e-15:
            raise ValueError("coefficient exceeds the selected pi/4 angle bound")

    @property
    def transformation_identity(self) -> str:
        """Return a stable transformation identity independently of any parent."""
        bonds = ";".join(
            ",".join(str(component) for component in bond)
            for bond in self.harmonic_bonds
        )
        return (
            f"{self.TRANSFORMATION_FAMILY_IDENTITY}:r{self.retained_rank:02d}:"
            f"L{self.circuit_depth:02d}:{self.normalization.to_wire()}:"
            f"bonds-{bonds}:coefficient-{self.coefficient.hex()}"
        )

    @property
    def angle_upper_bound(self) -> float:
        """Return a conservative continuum bound for every Givens angle."""
        bond_count = len(self.harmonic_bonds)
        normalization = (
            1.0 / 2.0
            if self.normalization is Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM
            else math.sqrt(2.0 / float(bond_count))
        )
        return self.coefficient * normalization * float(bond_count)

    @staticmethod
    def _immutable_float(value: Float64Array, name: str) -> Float64Array:
        return NumpyImmutableArrayConstructor(
            value,
            name,
            np.dtype(np.float64),
        ).execute()

    @staticmethod
    def _immutable_complex(value: Complex128Array, name: str) -> Complex128Array:
        return NumpyImmutableArrayConstructor(
            value,
            name,
            np.dtype(np.complex128),
        ).execute()

    def _coordinates(self, value: Float64Array) -> Float64Array:
        coordinates = self._immutable_float(value, "reduced_coordinates")
        if coordinates.ndim < 2 or coordinates.shape[-1] != 2:
            raise ValueError("reduced_coordinates must have shape (..., 2)")
        if any(size <= 0 for size in coordinates.shape[:-1]):
            raise ValueError("reduced-coordinate mesh axes must be nonempty")
        return coordinates

    def _gauge_scalar(
        self,
        reduced_coordinates: Float64Array,
        layer_index: int,
    ) -> Float64Array:
        bonds = np.asarray(self.harmonic_bonds, dtype=np.float64)
        arguments = (
            2.0
            * np.pi
            * np.einsum(
                "...d,bd->...b",
                reduced_coordinates,
                bonds,
            )
        )
        harmonic = 0.75 * np.sin(arguments) + 0.25 * ((-1.0) ** layer_index) * np.sin(
            2.0 * arguments
        )
        normalization = (
            1.0 / 2.0
            if self.normalization is Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM
            else math.sqrt(2.0 / float(len(self.harmonic_bonds)))
        )
        return np.asarray(
            normalization * np.sum(harmonic, axis=-1),
            dtype=np.float64,
        )

    def _sampled_transformation(
        self,
        coordinates: Float64Array,
    ) -> SampledFiniteRankGaugeTransformation:
        circuit = FiniteRankAlternatingNearestNeighborGivensCircuitConstructor(
            represented_rank=self.retained_rank,
            layer_count=self.circuit_depth,
        ).execute()
        columns: list[np.ndarray] = []
        rank = self.retained_rank
        for layer_index in range(1, self.circuit_depth + 1):
            scalar = self._gauge_scalar(coordinates, layer_index).reshape(-1)
            first_left = 0 if layer_index % 2 == 1 else 1
            for left in range(first_left, rank - 1, 2):
                pair_index = left + 1
                pair_coordinate = (2.0 * pair_index - rank) / (rank - 1.0)
                weight = (1.0 + 0.15 * pair_coordinate) / 1.15
                columns.append(
                    self.coefficient
                    * (-1.0) ** (layer_index + pair_index)
                    * weight
                    * scalar
                )
        return FiniteRankGivensCircuitTransformationConstructor(
            circuit=circuit,
            angle_samples=np.column_stack(columns).astype(
                np.float64,
                copy=False,
            ),
        ).execute()

    def unitaries(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return the alternating nearest-neighbor real Givens circuit."""
        coordinates = self._coordinates(reduced_coordinates)
        sampled = self._sampled_transformation(coordinates)
        values = sampled.unitaries.reshape(
            *coordinates.shape[:-1],
            self.retained_rank,
            self.retained_rank,
        )
        return self._immutable_complex(values, "gauge_unitaries")

    def inverse_right_actions(
        self,
        reduced_coordinates: Float64Array,
    ) -> Complex128Array:
        """Return the exact inverse right actions supplied by the construction."""
        coordinates = self._coordinates(reduced_coordinates)
        sampled = self._sampled_transformation(coordinates)
        values = sampled.inverse_right_actions.reshape(
            *coordinates.shape[:-1],
            self.retained_rank,
            self.retained_rank,
        )
        return self._immutable_complex(
            np.asarray(values, dtype=np.complex128),
            "inverse_right_actions",
        )

    def transform_frames(
        self,
        reduced_coordinates: Float64Array,
        frames: Complex128Array,
    ) -> Complex128Array:
        """Apply the transformation from the right to an admitted frame field."""
        coordinates = self._coordinates(reduced_coordinates)
        admitted = self._immutable_complex(frames, "reference_frames")
        if admitted.shape[:-2] != coordinates.shape[:-1]:
            raise ValueError("frame sample shape must match reduced coordinates")
        if admitted.shape[-2] < self.retained_rank:
            raise ValueError("frame ambient dimension must be at least retained rank")
        if admitted.shape[-1] != self.retained_rank:
            raise ValueError("frame column count must match retained rank")
        sample_shape = coordinates.shape[:-1]
        ambient_dimension = admitted.shape[-2]
        sampled = self._sampled_transformation(coordinates)
        values = sampled.transform_frames(
            admitted.reshape(-1, ambient_dimension, self.retained_rank)
        ).reshape(*sample_shape, ambient_dimension, self.retained_rank)
        return self._immutable_complex(values, "gauge_transformed_frames")

    def transform_operators(
        self,
        reduced_coordinates: Float64Array,
        operators: Complex128Array,
    ) -> Complex128Array:
        """Represent an admitted operator field in the transformed basis."""
        coordinates = self._coordinates(reduced_coordinates)
        admitted = self._immutable_complex(operators, "reference_operators")
        expected_shape = (
            *coordinates.shape[:-1],
            self.retained_rank,
            self.retained_rank,
        )
        if admitted.shape != expected_shape:
            raise ValueError(
                "operator shape must match reduced coordinates and retained rank"
            )
        sampled = self._sampled_transformation(coordinates)
        values = sampled.transform_operators(
            admitted.reshape(-1, self.retained_rank, self.retained_rank)
        ).reshape(expected_shape)
        return self._immutable_complex(values, "gauge_transformed_operators")


__all__ = [
    "Periodic2DRankNGaugeNormalizationEnum",
    "Periodic2DRankNGivensGaugeTransformation",
]
