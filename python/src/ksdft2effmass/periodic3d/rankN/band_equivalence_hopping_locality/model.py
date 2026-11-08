"""Synthetic periodic-3D arbitrary-rank study-case composition."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import ClassVar

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.physkit.periodic.lattice.hopping import DenseBlockHoppingModel

from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.base import (
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue,
)
from ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.parent import (
    Periodic3DRankNBlockHoppingParentBuilder,
)
from ksdft2effmass.periodic3d.rankN.gauge_alignment.transformation import (
    Periodic3DRankNGaugeNormalizationEnum,
    Periodic3DRankNGivensGaugeTransformation,
)


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRankNAnalyticCase(
    Periodic3DRankNBandEquivalenceHoppingLocalityCaseValue,
):
    """Compose one block-hopping parent with a separate gauge transformation."""

    MODEL_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic3d-rankN-analytic-givens-family.v1"
    )
    RETAINED_RANKS: ClassVar[tuple[int, ...]] = (3, 4, 8)
    CIRCUIT_DEPTHS: ClassVar[tuple[int, ...]] = (1, 2, 4)
    PARENT_SCALES: ClassVar[tuple[float, ...]] = (0.0, 1.0)
    NORM_ENERGY_SCALE: ClassVar[float] = 1.0
    EXTERNAL_GAP_LOWER_BOUND: ClassVar[float] = 1.9

    case_identifier: str
    retained_rank: int
    circuit_depth: int
    positive_bonds: tuple[tuple[int, int, int], ...]
    gauge_normalization: Periodic3DRankNGaugeNormalizationEnum
    parent_scale: float
    transformation_coefficient: float

    @property
    def band_subspace_rank(self) -> int:
        """Return the represented finite-rank case size."""
        return self.retained_rank

    def __post_init__(self) -> None:
        if type(self.case_identifier) is not str or not self.case_identifier:
            raise TypeError("case_identifier must be a nonempty built-in string")
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in integer")
        if self.retained_rank not in self.RETAINED_RANKS:
            raise ValueError("retained_rank is not in the selected inventory")
        if type(self.circuit_depth) is not int:
            raise TypeError("circuit_depth must be a built-in integer")
        if self.circuit_depth not in self.CIRCUIT_DEPTHS:
            raise ValueError("circuit_depth is not in the selected inventory")
        if type(self.positive_bonds) is not tuple or not self.positive_bonds:
            raise TypeError("positive_bonds must be a nonempty tuple")
        if any(
            type(bond) is not tuple
            or len(bond) != 3
            or any(type(component) is not int for component in bond)
            or bond == (0, 0, 0)
            for bond in self.positive_bonds
        ):
            raise TypeError("positive_bonds must contain nonzero integer triples")
        if len(set(self.positive_bonds)) != len(self.positive_bonds):
            raise ValueError("positive_bonds must be unique")
        if type(self.gauge_normalization) is not Periodic3DRankNGaugeNormalizationEnum:
            raise TypeError("gauge_normalization must be the exact periodic-3D enum")
        if type(self.parent_scale) is not float:
            raise TypeError("parent_scale must be a built-in float")
        if self.parent_scale not in self.PARENT_SCALES:
            raise ValueError("parent_scale is not in the selected inventory")
        if type(self.transformation_coefficient) is not float:
            raise TypeError("transformation_coefficient must be a built-in float")
        if (
            not math.isfinite(self.transformation_coefficient)
            or self.transformation_coefficient < 0.0
        ):
            raise ValueError(
                "transformation_coefficient must be finite and nonnegative"
            )
        if self.transformation_angle_upper_bound > math.pi / 4.0 + 1.0e-15:
            raise ValueError(
                "transformation coefficient exceeds the selected pi/4 angle bound"
            )

    @property
    def ambient_dimension(self) -> int:
        """Return the ordered retained-plus-exterior parent dimension."""
        return 2 * self.retained_rank

    @property
    def model_identity(self) -> str:
        """Return the stable case, rank, depth, scale, and transformation identity."""
        return (
            f"{self.MODEL_FAMILY_IDENTITY}:{self.case_identifier}:"
            f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}:"
            f"lambda-{self.parent_scale.hex()}:transformation-{self.transformation_coefficient.hex()}"
        )

    @property
    def parent_model(self) -> DenseBlockHoppingModel:
        """Return the PhysKit block-hopping parent independent of the transformation."""
        return Periodic3DRankNBlockHoppingParentBuilder(
            retained_rank=self.retained_rank,
            positive_bonds=self.positive_bonds,
            hopping_scale=self.parent_scale,
        ).execute()

    @property
    def gauge_transformation(self) -> Periodic3DRankNGivensGaugeTransformation:
        """Return the independently applicable synthetic gauge transformation."""
        return Periodic3DRankNGivensGaugeTransformation(
            retained_rank=self.retained_rank,
            circuit_depth=self.circuit_depth,
            harmonic_bonds=self.positive_bonds,
            normalization=self.gauge_normalization,
            coefficient=self.transformation_coefficient,
        )

    @property
    def transformation_angle_upper_bound(self) -> float:
        """Return a conservative continuum bound for every Givens angle."""
        return self.gauge_transformation.angle_upper_bound

    def _coordinates(self, value: Float64Array) -> Float64Array:
        coordinates = NumpyImmutableArrayConstructor(
            value,
            "reduced_coordinates",
            np.dtype(np.float64),
        ).execute()
        if coordinates.ndim < 2 or coordinates.shape[-1] != 3:
            raise ValueError("reduced_coordinates must have shape (..., 3)")
        if any(size <= 0 for size in coordinates.shape[:-1]):
            raise ValueError("reduced-coordinate mesh axes must be nonempty")
        return coordinates

    @staticmethod
    def _immutable_float(value: Float64Array) -> Float64Array:
        return NumpyImmutableArrayConstructor(
            value,
            "analytic_float_result",
            np.dtype(np.float64),
        ).execute()

    @staticmethod
    def _immutable_complex(
        value: Complex128Array,
    ) -> Complex128Array:
        return NumpyImmutableArrayConstructor(
            value,
            "analytic_complex_result",
            np.dtype(np.complex128),
        ).execute()

    def structure_factor(self, reduced_coordinates: Float64Array) -> Float64Array:
        """Return the normalized first/second-harmonic parent structure factor."""
        coordinates = self._coordinates(reduced_coordinates)
        bonds = np.asarray(self.positive_bonds, dtype=np.float64)
        arguments = 2.0 * np.pi * np.einsum("...d,bd->...b", coordinates, bonds)
        values = np.mean(
            0.75 * np.cos(arguments) + 0.25 * np.cos(2.0 * arguments),
            axis=-1,
        )
        return self._immutable_float(np.asarray(values, dtype=np.float64))

    def _orbital_coordinates(self) -> Float64Array:
        orbital = np.arange(self.retained_rank, dtype=np.float64)
        return np.asarray(
            (2.0 * orbital - self.retained_rank + 1.0) / (self.retained_rank - 1.0),
            dtype=np.float64,
        )

    def retained_energies(self, reduced_coordinates: Float64Array) -> Float64Array:
        """Return the strictly ordered retained-sector energies."""
        structure = self.structure_factor(reduced_coordinates)
        orbital = self._orbital_coordinates()
        values = 0.4 * orbital + (
            0.25 * self.parent_scale * (1.0 + 0.2 * orbital) * structure[..., None]
        )
        return self._immutable_float(np.asarray(values, dtype=np.float64))

    def exterior_energies(self, reduced_coordinates: Float64Array) -> Float64Array:
        """Return the separated exterior-sector energies."""
        structure = self.structure_factor(reduced_coordinates)
        orbital = self._orbital_coordinates()
        values = 3.0 + 0.3 * orbital + 0.1 * self.parent_scale * structure[..., None]
        return self._immutable_float(np.asarray(values, dtype=np.float64))

    def parent_hamiltonians(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return diagonal parent operators in the ordered ambient basis."""
        retained = self.retained_energies(reduced_coordinates)
        exterior = self.exterior_energies(reduced_coordinates)
        diagonal = np.concatenate((retained, exterior), axis=-1)
        identity = np.eye(self.ambient_dimension, dtype=np.complex128)
        values = diagonal[..., :, None] * identity
        return self._immutable_complex(np.asarray(values, dtype=np.complex128))

    def reference_frames(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return the constant retained-coordinate embedding on one mesh."""
        coordinates = self._coordinates(reduced_coordinates)
        frame = np.zeros(
            (self.ambient_dimension, self.retained_rank), dtype=np.complex128
        )
        frame[: self.retained_rank] = np.eye(self.retained_rank, dtype=np.complex128)
        values = np.broadcast_to(frame, (*coordinates.shape[:-1], *frame.shape)).copy()
        return self._immutable_complex(values)

    def exact_reduced_hamiltonians(
        self, reduced_coordinates: Float64Array
    ) -> Complex128Array:
        """Return exact retained operators in the analytic reference frame."""
        energies = self.retained_energies(reduced_coordinates)
        identity = np.eye(self.retained_rank, dtype=np.complex128)
        values = energies[..., :, None] * identity
        return self._immutable_complex(np.asarray(values, dtype=np.complex128))

    def gauge_unitaries(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return the unitary field generated by the composed gauge transformation."""
        return self.gauge_transformation.unitaries(reduced_coordinates)

    def gauge_transformed_frames(
        self, reduced_coordinates: Float64Array
    ) -> Complex128Array:
        """Return reference frames after the right-acting gauge transformation."""
        return self.gauge_transformation.transform_frames(
            reduced_coordinates,
            self.reference_frames(reduced_coordinates),
        )

    def gauge_transformed_reduced_hamiltonians(
        self, reduced_coordinates: Float64Array
    ) -> Complex128Array:
        """Return retained operators represented in the gauge-transformed frame."""
        return self.gauge_transformation.transform_operators(
            reduced_coordinates,
            self.exact_reduced_hamiltonians(reduced_coordinates),
        )

    def known_inverse_right_actions(
        self, reduced_coordinates: Float64Array
    ) -> Complex128Array:
        """Return the exact construction-oracle inverse right actions."""
        return self.gauge_transformation.inverse_right_actions(reduced_coordinates)


__all__ = [
    "Periodic3DRankNAnalyticCase",
    "Periodic3DRankNGaugeNormalizationEnum",
]
