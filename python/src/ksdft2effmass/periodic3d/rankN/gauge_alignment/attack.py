"""Synthetic right-acting gauge attacks for periodic-3D finite-rank fields."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import ClassVar

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor

from ksdft2effmass.serialization import StrWireEnum


class Periodic3DRankNGaugeNormalizationEnum(StrWireEnum):
    """Select the reviewed interpretation of one gauge-attack coefficient."""

    AXIS_MAXIMUM = "axis-maximum"
    BOND_RMS = "bond-rms"


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRankNGivensGaugeAttack:
    """Define and apply one bounded alternating Givens gauge attack.

    The attack acts only in retained coordinates.  It is independent of the
    parent Hamiltonian and can therefore be applied to analytic or authenticated
    DFT/Wannier frame and represented-operator fields with matching rank and
    reciprocal coordinates.
    """

    ATTACK_FAMILY_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic3d-rankN-alternating-givens-attack.v1"
    )

    retained_rank: int
    circuit_depth: int
    harmonic_bonds: tuple[tuple[int, int, int], ...]
    normalization: Periodic3DRankNGaugeNormalizationEnum
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
            or len(bond) != 3
            or any(type(component) is not int for component in bond)
            or bond == (0, 0, 0)
            for bond in self.harmonic_bonds
        ):
            raise TypeError("harmonic_bonds must contain nonzero integer triples")
        if len(set(self.harmonic_bonds)) != len(self.harmonic_bonds):
            raise ValueError("harmonic_bonds must be unique")
        if type(self.normalization) is not Periodic3DRankNGaugeNormalizationEnum:
            raise TypeError("normalization must be the exact periodic-3D enum")
        if type(self.coefficient) is not float:
            raise TypeError("coefficient must be a built-in float")
        if not math.isfinite(self.coefficient) or self.coefficient < 0.0:
            raise ValueError("coefficient must be finite and nonnegative")
        if self.angle_upper_bound > math.pi / 4.0 + 1.0e-15:
            raise ValueError("coefficient exceeds the selected pi/4 angle bound")

    @property
    def attack_identity(self) -> str:
        """Return a stable identity for the attack independently of any parent."""
        bonds = ";".join(
            ",".join(str(component) for component in bond)
            for bond in self.harmonic_bonds
        )
        return (
            f"{self.ATTACK_FAMILY_IDENTITY}:r{self.retained_rank:02d}:"
            f"L{self.circuit_depth:02d}:{self.normalization.to_wire()}:"
            f"bonds-{bonds}:coefficient-{self.coefficient.hex()}"
        )

    @property
    def angle_upper_bound(self) -> float:
        """Return a conservative continuum bound for every Givens angle."""
        bond_count = len(self.harmonic_bonds)
        normalization = (
            1.0 / 3.0
            if self.normalization is Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM
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
        if coordinates.ndim < 2 or coordinates.shape[-1] != 3:
            raise ValueError("reduced_coordinates must have shape (..., 3)")
        if any(size <= 0 for size in coordinates.shape[:-1]):
            raise ValueError("reduced-coordinate mesh axes must be nonempty")
        return coordinates

    def _gauge_scalar(
        self,
        reduced_coordinates: Float64Array,
        layer_index: int,
    ) -> Float64Array:
        bonds = np.asarray(self.harmonic_bonds, dtype=np.float64)
        arguments = 2.0 * np.pi * np.einsum("...d,bd->...b", reduced_coordinates, bonds)
        harmonic = 0.75 * np.sin(arguments) + 0.25 * ((-1.0) ** layer_index) * np.sin(
            2.0 * arguments
        )
        normalization = (
            1.0 / 3.0
            if self.normalization is Periodic3DRankNGaugeNormalizationEnum.AXIS_MAXIMUM
            else math.sqrt(2.0 / float(len(self.harmonic_bonds)))
        )
        return np.asarray(normalization * np.sum(harmonic, axis=-1), dtype=np.float64)

    def unitaries(self, reduced_coordinates: Float64Array) -> Complex128Array:
        """Return the alternating nearest-neighbor real Givens circuit."""
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
                    self.coefficient
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
        return self._immutable_complex(
            np.asarray(gauges, dtype=np.complex128),
            "gauge_unitaries",
        )

    def inverse_right_actions(
        self, reduced_coordinates: Float64Array
    ) -> Complex128Array:
        """Return the exact inverse right actions supplied by the construction."""
        gauge = self.unitaries(reduced_coordinates)
        values = np.swapaxes(gauge.conjugate(), -1, -2)
        return self._immutable_complex(
            np.asarray(values, dtype=np.complex128),
            "inverse_right_actions",
        )

    def apply_to_frames(
        self,
        reduced_coordinates: Float64Array,
        frames: Complex128Array,
    ) -> Complex128Array:
        """Apply the attack from the right to an admitted frame field."""
        coordinates = self._coordinates(reduced_coordinates)
        admitted = self._immutable_complex(frames, "reference_frames")
        if admitted.shape[:-2] != coordinates.shape[:-1]:
            raise ValueError("frame sample shape must match reduced coordinates")
        if admitted.shape[-2] < self.retained_rank:
            raise ValueError("frame ambient dimension must be at least retained rank")
        if admitted.shape[-1] != self.retained_rank:
            raise ValueError("frame column count must match retained rank")
        values = admitted @ self.unitaries(coordinates)
        return self._immutable_complex(
            np.asarray(values, dtype=np.complex128),
            "attacked_frames",
        )

    def apply_to_operators(
        self,
        reduced_coordinates: Float64Array,
        operators: Complex128Array,
    ) -> Complex128Array:
        """Represent an admitted retained operator field in the attacked basis."""
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
        gauge = self.unitaries(coordinates)
        values = np.swapaxes(gauge.conjugate(), -1, -2) @ admitted @ gauge
        return self._immutable_complex(
            np.asarray(values, dtype=np.complex128),
            "attacked_operators",
        )


__all__ = [
    "Periodic3DRankNGaugeNormalizationEnum",
    "Periodic3DRankNGivensGaugeAttack",
]
