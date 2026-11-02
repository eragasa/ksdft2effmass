"""Recommended analytic periodic-3D arbitrary-rank parent and gauge attack."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import ClassVar

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor

from ksdft2effmass.periodic3d.base import Periodic3DCapability
from ksdft2effmass.serialization import StringWireEnum


class Periodic3DRankNGaugeNormalizationEnum(StringWireEnum):
    """Select the reviewed interpretation of one gauge-attack coefficient."""

    AXIS_MAXIMUM = "axis-maximum"
    BOND_RMS = "bond-rms"


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRankNAnalyticCase(Periodic3DCapability):
    """Define one topologically trivial rank-N parent and right gauge circuit."""

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
    attack_coefficient: float

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
        if type(self.attack_coefficient) is not float:
            raise TypeError("attack_coefficient must be a built-in float")
        if not math.isfinite(self.attack_coefficient) or self.attack_coefficient < 0.0:
            raise ValueError("attack_coefficient must be finite and nonnegative")
        if self.attack_angle_upper_bound > math.pi / 4.0 + 1.0e-15:
            raise ValueError("attack coefficient exceeds the selected pi/4 angle bound")

    @property
    def ambient_dimension(self) -> int:
        """Return the ordered retained-plus-exterior parent dimension."""
        return 2 * self.retained_rank

    @property
    def model_identity(self) -> str:
        """Return the stable case, rank, depth, scale, and attack identity."""
        return (
            f"{self.MODEL_FAMILY_IDENTITY}:{self.case_identifier}:"
            f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}:"
            f"lambda-{self.parent_scale.hex()}:attack-{self.attack_coefficient.hex()}"
        )

    @property
    def attack_angle_upper_bound(self) -> float:
        """Return a conservative continuum bound for every Givens angle."""
        bond_count = len(self.positive_bonds)
        normalization = (
            1.0 / 3.0
            if self.gauge_normalization
            is Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM
            else math.sqrt(2.0 / float(bond_count))
        )
        return self.attack_coefficient * normalization * float(bond_count)

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

    def _gauge_scalar(
        self,
        reduced_coordinates: Float64Array,
        layer_index: int,
    ) -> Float64Array:
        coordinates = self._coordinates(reduced_coordinates)
        bonds = np.asarray(self.positive_bonds, dtype=np.float64)
        arguments = 2.0 * np.pi * np.einsum("...d,bd->...b", coordinates, bonds)
        harmonic = 0.75 * np.sin(arguments) + 0.25 * ((-1.0) ** layer_index) * np.sin(
            2.0 * arguments
        )
        normalization = (
            1.0 / 3.0
            if self.gauge_normalization
            is Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM
            else math.sqrt(2.0 / float(len(self.positive_bonds)))
        )
        return np.asarray(normalization * np.sum(harmonic, axis=-1), dtype=np.float64)

    def gauge_unitaries(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return the selected alternating nearest-neighbor real Givens circuit."""
        coordinates = self._coordinates(reduced_coordinates)
        rank = self.retained_rank
        identity = np.eye(rank, dtype=np.complex128)
        gauges = np.broadcast_to(identity, (*coordinates.shape[:-1], rank, rank)).copy()
        for layer_index in range(1, self.circuit_depth + 1):
            scalar = self._gauge_scalar(coordinates, layer_index)
            layer = np.broadcast_to(
                identity, (*coordinates.shape[:-1], rank, rank)
            ).copy()
            first_left = 0 if layer_index % 2 == 1 else 1
            for left in range(first_left, rank - 1, 2):
                pair_index = left + 1
                pair_coordinate = (2.0 * pair_index - rank) / (rank - 1.0)
                weight = (1.0 + 0.15 * pair_coordinate) / 1.15
                angle = (
                    self.attack_coefficient
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
        return self._immutable_complex(np.asarray(gauges, dtype=np.complex128))

    def attacked_frames(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return reference frames after the right-acting gauge attack."""
        values = self.reference_frames(reduced_coordinates) @ self.gauge_unitaries(
            reduced_coordinates
        )
        return self._immutable_complex(np.asarray(values, dtype=np.complex128))

    def attacked_reduced_hamiltonians(
        self, reduced_coordinates: Float64Array
    ) -> Complex128Array:
        """Return retained operators represented in the attacked frame."""
        gauge = self.gauge_unitaries(reduced_coordinates)
        exact = self.exact_reduced_hamiltonians(reduced_coordinates)
        values = np.swapaxes(gauge.conjugate(), -1, -2) @ exact @ gauge
        return self._immutable_complex(np.asarray(values, dtype=np.complex128))

    def known_inverse_right_actions(
        self, reduced_coordinates: Float64Array
    ) -> Complex128Array:
        """Return the exact construction-oracle inverse right actions."""
        gauge = self.gauge_unitaries(reduced_coordinates)
        values = np.swapaxes(gauge.conjugate(), -1, -2)
        return self._immutable_complex(np.asarray(values, dtype=np.complex128))


__all__ = [
    "Periodic3DRankNAnalyticCase",
    "Periodic3DRankNGaugeNormalizationEnum",
]
