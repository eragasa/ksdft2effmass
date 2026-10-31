"""Specified periodic-1D gauge rotations for band-locality controls."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array

from ksdft2effmass.solidstate import GaugeRotation


@dataclass(frozen=True, slots=True, init=False)
class Periodic1DRank2SinusoidalGaugeRotation(GaugeRotation):
    """Define the declared dimensionless rank-two ``SO(2)`` rotation field.

    For amplitude ``a`` and reduced reciprocal coordinate ``q``, the right-acting
    retained-space rotation angle is ``a sin(2 pi q)``.
    """

    amplitude: float

    def __init__(self, amplitude: float) -> None:
        if type(amplitude) is not float:
            raise TypeError("amplitude must be a built-in float")
        if not math.isfinite(amplitude):
            raise ValueError("amplitude must be finite")
        object.__setattr__(self, "amplitude", amplitude)
        GaugeRotation.__init__(self, rank=2)

    def matrices(self, coordinates: Float64Array) -> Complex128Array:
        """Return immutable rotations on ordered reduced coordinates."""
        if type(coordinates) is not np.ndarray:
            raise TypeError("coordinates must be a NumPy array")
        if coordinates.dtype != np.dtype(np.float64):
            raise TypeError("coordinates must have dtype float64")
        if coordinates.ndim != 1 or coordinates.size == 0:
            raise ValueError("coordinates must be a nonempty vector")
        if not bool(np.isfinite(coordinates).all()):
            raise ValueError("coordinates must be finite")
        theta = self.amplitude * np.sin(2.0 * np.pi * coordinates)
        rotations = np.empty((coordinates.size, 2, 2), dtype=np.complex128)
        rotations[:, 0, 0] = np.cos(theta)
        rotations[:, 0, 1] = -np.sin(theta)
        rotations[:, 1, 0] = np.sin(theta)
        rotations[:, 1, 1] = np.cos(theta)
        rotations.setflags(write=False)
        return rotations


__all__ = ["Periodic1DRank2SinusoidalGaugeRotation"]
