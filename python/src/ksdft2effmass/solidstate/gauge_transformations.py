"""Gauge-rotation definitions and their action on represented operators."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array


@dataclass(frozen=True, slots=True)
class GaugeRotation(ABC):
    """Define a matrix-valued right-acting gauge rotation.

    A concrete rotation must bind every parameter needed to define its matrix field.
    The sample coordinates are supplied only when the field is evaluated by a
    :class:`GaugeAttack`.
    """

    rank: int

    def __post_init__(self) -> None:
        if type(self.rank) is not int:
            raise TypeError("rank must be a built-in int")
        if self.rank < 1:
            raise ValueError("rank must be positive")

    @abstractmethod
    def matrices(self, coordinates: Float64Array) -> Complex128Array:
        """Return rotation matrices for the ordered finite coordinates."""


@dataclass(frozen=True, slots=True)
class GaugeAttack:
    """Evaluate and apply a gauge rotation to represented operators."""

    rotation: GaugeRotation
    unitarity_absolute_tolerance: float

    def __post_init__(self) -> None:
        if not isinstance(self.rotation, GaugeRotation):
            raise TypeError("rotation must implement GaugeRotation")
        if type(self.unitarity_absolute_tolerance) is not float:
            raise TypeError(
                "unitarity_absolute_tolerance must be a built-in float"
            )
        if (
            not math.isfinite(self.unitarity_absolute_tolerance)
            or self.unitarity_absolute_tolerance <= 0.0
        ):
            raise ValueError(
                "unitarity_absolute_tolerance must be finite and positive"
            )

    def apply(
        self,
        *,
        coordinates: Float64Array,
        represented_matrices: Complex128Array,
    ) -> Complex128Array:
        """Return immutable ``U[s]^dagger H[s] U[s]`` matrices."""
        sample_count = self._validate_coordinates(coordinates)
        self._validate_represented_matrices(represented_matrices, sample_count)
        rotations = self.rotation.matrices(coordinates)
        self._validate_rotations(rotations, sample_count)
        result = np.asarray(
            np.swapaxes(rotations.conjugate(), -1, -2)
            @ represented_matrices
            @ rotations,
            dtype=np.complex128,
        )
        result.setflags(write=False)
        return result

    @staticmethod
    def _validate_coordinates(coordinates: Float64Array) -> int:
        if type(coordinates) is not np.ndarray:
            raise TypeError("coordinates must be a NumPy array")
        if coordinates.dtype != np.dtype(np.float64):
            raise TypeError("coordinates must have dtype float64")
        if coordinates.ndim not in (1, 2) or coordinates.shape[0] == 0:
            raise ValueError(
                "coordinates must be a nonempty vector or sample-by-dimension array"
            )
        if not bool(np.isfinite(coordinates).all()):
            raise ValueError("coordinates must be finite")
        return int(coordinates.shape[0])

    def _validate_represented_matrices(
        self,
        represented_matrices: Complex128Array,
        sample_count: int,
    ) -> None:
        if type(represented_matrices) is not np.ndarray:
            raise TypeError("represented_matrices must be a NumPy array")
        if represented_matrices.dtype != np.dtype(np.complex128):
            raise TypeError("represented_matrices must have dtype complex128")
        if represented_matrices.shape != (
            sample_count,
            self.rotation.rank,
            self.rotation.rank,
        ):
            raise ValueError(
                "represented_matrices must match the coordinate count and rotation rank"
            )
        if not bool(np.isfinite(represented_matrices).all()):
            raise ValueError("represented_matrices must be finite")

    def _validate_rotations(
        self,
        rotations: Complex128Array,
        sample_count: int,
    ) -> None:
        if type(rotations) is not np.ndarray:
            raise TypeError("rotation matrices must be a NumPy array")
        if rotations.dtype != np.dtype(np.complex128):
            raise TypeError("rotation matrices must have dtype complex128")
        if rotations.shape != (
            sample_count,
            self.rotation.rank,
            self.rotation.rank,
        ):
            raise ValueError(
                "rotation matrices must match the coordinate count and declared rank"
            )
        if not bool(np.isfinite(rotations).all()):
            raise ValueError("rotation matrices must be finite")
        identity = np.eye(self.rotation.rank, dtype=np.complex128)
        defect = float(
            np.max(
                np.abs(
                    np.swapaxes(rotations.conjugate(), -1, -2)
                    @ rotations
                    - identity
                )
            )
        )
        if defect > self.unitarity_absolute_tolerance:
            raise ValueError(
                "rotation matrices exceed the declared unitarity tolerance"
            )


__all__ = ["GaugeAttack", "GaugeRotation"]
