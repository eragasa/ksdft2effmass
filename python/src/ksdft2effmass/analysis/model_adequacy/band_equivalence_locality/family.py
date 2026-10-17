"""Axis-symmetric scientific family shared by the 1-D, 2-D, and 3-D studies."""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass

from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension
from scipy.special import j0  # type: ignore[import-untyped]

type ReducedCoordinate = tuple[float, ...]
type ComplexMatrix = tuple[tuple[complex, ...], ...]
type RealMatrix2 = tuple[tuple[float, float], tuple[float, float]]

_ONSITE: ComplexMatrix = (
    (-1.20 + 0.0j, 0.06 + 0.0j, 0.0j, 0.0j),
    (0.06 + 0.0j, -0.35 + 0.0j, 0.0j, 0.0j),
    (0.0j, 0.0j, 1.00 + 0.0j, 0.04 + 0.0j),
    (0.0j, 0.0j, 0.04 + 0.0j, 1.75 + 0.0j),
)
_DIRECTED_HOPPING: ComplexMatrix = (
    (0.15 + 0.0j, 0.0j, 0.12 + 0.0j, 0.0j),
    (0.0j, -0.10 + 0.0j, 0.0j, 0.10 + 0.0j),
    (0.0j, 0.0j, 0.05 + 0.0j, 0.0j),
    (0.0j, 0.0j, 0.0j, -0.04 + 0.0j),
)


def _finite_builtin_float(name: str, value: float) -> None:
    if type(value) is not float:
        raise TypeError(f"{name} must be a built-in float")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _validate_coordinate(
    dimension: LatticeDimension, coordinate: ReducedCoordinate
) -> None:
    if type(coordinate) is not tuple:
        raise TypeError("reduced_coordinate must be a tuple")
    if len(coordinate) != dimension.value:
        raise ValueError("reduced_coordinate length must match dimension")
    for index, value in enumerate(coordinate):
        _finite_builtin_float(f"reduced_coordinate[{index}]", value)
        if not -0.5 <= value < 0.5:
            raise ValueError("reduced coordinates must lie in [-1/2, 1/2)")


@dataclass(frozen=True, slots=True)
class AxisSymmetricFourStateParent:
    """Evaluate the normalized dimension-general directed-hopping parent.

    ``parent_hopping_scale`` is the unit-free homotopy parameter ``rho`` and
    must lie in ``[0, 1]``. Returned matrix entries are normalized by the positive
    energy scale :math:`E_ref`; this object does not attach a physical energy unit.
    The axis average makes the diagonal specialization ``(q, ..., q)`` identical in
    one, two, and three dimensions.
    """

    dimension: LatticeDimension
    parent_hopping_scale: float

    def __post_init__(self) -> None:
        """Validate the closed dimension and homotopy controls."""
        if type(self.dimension) is not LatticeDimension:
            raise TypeError("dimension must be LatticeDimension")
        _finite_builtin_float("parent_hopping_scale", self.parent_hopping_scale)
        if not 0.0 <= self.parent_hopping_scale <= 1.0:
            raise ValueError("parent_hopping_scale must lie in [0, 1]")

    def evaluate(self, reduced_coordinate: ReducedCoordinate) -> ComplexMatrix:
        """Return the immutable normalized four-state Bloch matrix.

        The coordinate components are built-in binary64 floats in the reduced
        half-open cell ``[-1/2, 1/2)``. Bounded phases and fixed matrix entries cannot
        overflow binary64 under this contract.
        """
        _validate_coordinate(self.dimension, reduced_coordinate)
        phase_average = sum(
            cmath.exp(2.0j * math.pi * value) for value in reduced_coordinate
        ) / float(self.dimension.value)
        scaled_phase = self.parent_hopping_scale * phase_average
        return tuple(
            tuple(
                _ONSITE[row][column]
                + scaled_phase * _DIRECTED_HOPPING[row][column]
                + scaled_phase.conjugate() * _DIRECTED_HOPPING[column][row].conjugate()
                for column in range(4)
            )
            for row in range(4)
        )


@dataclass(frozen=True, slots=True)
class SeparableSineRotation:
    """Evaluate the dimension-general retained-space real rotation.

    ``amplitude`` is a built-in binary64 angle in radians in ``[0, pi/4]``. The
    rotation angle is ``amplitude / d`` times the sum of the axis sine fields. The
    flat-parent continuous correlation is evaluated directly as
    ``J_0(2*amplitude/d)**d`` and is not inferred from an amplitude interpolant.
    """

    dimension: LatticeDimension
    amplitude: float

    def __post_init__(self) -> None:
        """Validate dimension and bounded amplitude."""
        if type(self.dimension) is not LatticeDimension:
            raise TypeError("dimension must be LatticeDimension")
        _finite_builtin_float("amplitude", self.amplitude)
        if not 0.0 <= self.amplitude <= math.pi / 4.0:
            raise ValueError("amplitude must lie in [0, pi/4]")

    def angle(self, reduced_coordinate: ReducedCoordinate) -> float:
        """Return the real rotation angle in radians at one reduced coordinate."""
        _validate_coordinate(self.dimension, reduced_coordinate)
        return (
            self.amplitude
            * math.fsum(math.sin(math.tau * value) for value in reduced_coordinate)
            / float(self.dimension.value)
        )

    def matrix(self, reduced_coordinate: ReducedCoordinate) -> RealMatrix2:
        """Return the immutable ``SO(2)`` rotation matrix at one coordinate."""
        angle = self.angle(reduced_coordinate)
        cosine = math.cos(angle)
        sine = math.sin(angle)
        return ((cosine, -sine), (sine, cosine))

    @property
    def flat_parent_correlation(self) -> float:
        """Return the direct analytic flat-parent correlation."""
        argument = 2.0 * self.amplitude / float(self.dimension.value)
        value = float(j0(argument)) ** self.dimension.value
        if not math.isfinite(value):
            raise FloatingPointError("flat-parent correlation became nonfinite")
        return value
