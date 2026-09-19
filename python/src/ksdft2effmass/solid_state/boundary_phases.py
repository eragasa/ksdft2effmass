"""Boundary-twist records and actions for finite periodic lattice models.

Twists are expressed in turns. An unreduced lift in real coordinate space and its
componentwise representative in the quotient by integer shifts are distinct public
values. These records are unweighted boundary conditions, not reciprocal-space
``KPointSampling`` records.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from enum import StrEnum

from .geometry import (
    LatticeDimension,
    LatticeDisplacement,
    LatticeIntegerComponents,
)

type LatticeFloatComponents = (
    tuple[float] | tuple[float, float] | tuple[float, float, float]
)
"""Closed floating coordinate representation for one to three dimensions."""


class TwistGaugeRepresentation(StrEnum):
    """Supported finite-lattice boundary-twist gauge representations."""

    CENTERED_UNIFORM_LINK = "centered_uniform_link"
    QUOTIENT_SEAM = "quotient_seam"


@dataclass(frozen=True, slots=True)
class BoundaryTwistLift:
    """Represent one unreduced boundary-twist lift in turns.

    Parameters
    ----------
    dimension
        Exact supported spatial dimension.
    turns
        Exactly one, two, or three finite built-in floats matching ``dimension``.
        Components are not reduced modulo one.
    """

    dimension: LatticeDimension
    turns: LatticeFloatComponents

    def __post_init__(self) -> None:
        """Validate finite closed-dimensional twist components."""
        if type(self.dimension) is not LatticeDimension:
            raise TypeError("dimension must be LatticeDimension")
        if type(self.turns) is not tuple:
            raise TypeError("turns must be a tuple")
        if len(self.turns) != self.dimension.value:
            raise ValueError("twist component count must match dimension")
        if any(type(value) is not float for value in self.turns):
            raise TypeError("twist components must be built-in floats")
        if any(not math.isfinite(value) for value in self.turns):
            raise ValueError("twist components must be finite")


@dataclass(frozen=True, slots=True)
class BoundaryTwistRepresentative:
    """Represent a quotient-seam twist in the half-open interval ``[0, 1)``.

    Parameters
    ----------
    dimension
        Exact supported spatial dimension.
    turns
        Finite built-in-float components in ``[0, 1)``, one per axis.
    """

    dimension: LatticeDimension
    turns: LatticeFloatComponents

    def __post_init__(self) -> None:
        """Validate the canonical quotient representative."""
        if type(self.dimension) is not LatticeDimension:
            raise TypeError("dimension must be LatticeDimension")
        if type(self.turns) is not tuple:
            raise TypeError("turns must be a tuple")
        if len(self.turns) != self.dimension.value:
            raise ValueError("twist component count must match dimension")
        if any(type(value) is not float for value in self.turns):
            raise TypeError("twist components must be built-in floats")
        if any(not math.isfinite(value) for value in self.turns):
            raise ValueError("twist components must be finite")
        if any(value < 0.0 or value >= 1.0 for value in self.turns):
            raise ValueError("twist representative components must lie in [0, 1)")


@dataclass(frozen=True, slots=True)
class BoundaryTwistReductionResult:
    """Record reduction of one twist lift modulo integer shifts.

    Parameters
    ----------
    lift
        Original unreduced twist.
    representative
        Componentwise representative in ``[0, 1)``.
    quotient
        Integer vector satisfying ``lift = representative + quotient`` up to the
        binary64 subtraction used by the reduction action.
    """

    lift: BoundaryTwistLift
    representative: BoundaryTwistRepresentative
    quotient: LatticeDisplacement

    def __post_init__(self) -> None:
        """Require all result components to share one dimension."""
        if type(self.lift) is not BoundaryTwistLift:
            raise TypeError("lift must be BoundaryTwistLift")
        if type(self.representative) is not BoundaryTwistRepresentative:
            raise TypeError("representative must be BoundaryTwistRepresentative")
        if type(self.quotient) is not LatticeDisplacement:
            raise TypeError("quotient must be LatticeDisplacement")
        dimensions = {
            self.lift.dimension,
            self.representative.dimension,
            self.quotient.dimension,
        }
        if len(dimensions) != 1:
            raise ValueError("twist reduction dimensions must agree")


@dataclass(frozen=True, slots=True)
class TwistFiber:
    """Bind one twist lift and quotient representative to an exact gauge.

    Parameters
    ----------
    reduction
        Correlated unreduced lift, representative, and integer quotient.
    gauge
        Gauge in which a represented operator stores this twist fiber.

    Notes
    -----
    Retaining the complete reduction prevents an integer-shifted lift from being
    silently identified with the same representative in a uniform-link gauge.
    """

    reduction: BoundaryTwistReductionResult
    gauge: TwistGaugeRepresentation

    def __post_init__(self) -> None:
        """Validate exact twist reduction and gauge types."""
        if type(self.reduction) is not BoundaryTwistReductionResult:
            raise TypeError("reduction must be BoundaryTwistReductionResult")
        if type(self.gauge) is not TwistGaugeRepresentation:
            raise TypeError("gauge must be TwistGaugeRepresentation")

    @property
    def dimension(self) -> LatticeDimension:
        """Return the exact spatial dimension of the twist fiber."""
        return self.reduction.lift.dimension

    @property
    def lift(self) -> BoundaryTwistLift:
        """Return the retained unreduced twist lift."""
        return self.reduction.lift

    @property
    def representative(self) -> BoundaryTwistRepresentative:
        """Return the retained canonical quotient representative."""
        return self.reduction.representative


class BoundaryTwistReducer:
    """Reduce an unreduced twist to a quotient-seam representative."""

    __slots__ = ()

    def execute(self, lift: BoundaryTwistLift) -> BoundaryTwistReductionResult:
        """Reduce every component modulo one while retaining integer quotients."""
        if type(lift) is not BoundaryTwistLift:
            raise TypeError("lift must be BoundaryTwistLift")
        quotients = tuple(math.floor(value) for value in lift.turns)
        representatives = tuple(
            value - float(quotient)
            for value, quotient in zip(lift.turns, quotients, strict=True)
        )
        normalized = tuple(0.0 if value == 1.0 else value for value in representatives)
        if lift.dimension is LatticeDimension.ONE:
            representative_values: LatticeFloatComponents = (normalized[0],)
            quotient_values: LatticeIntegerComponents = (quotients[0],)
        elif lift.dimension is LatticeDimension.TWO:
            representative_values = (normalized[0], normalized[1])
            quotient_values = (quotients[0], quotients[1])
        else:
            representative_values = (normalized[0], normalized[1], normalized[2])
            quotient_values = (quotients[0], quotients[1], quotients[2])
        return BoundaryTwistReductionResult(
            lift,
            BoundaryTwistRepresentative(lift.dimension, representative_values),
            LatticeDisplacement(lift.dimension, quotient_values),
        )


@dataclass(frozen=True, slots=True)
class BoundaryTwistMesh:
    """Represent one complete tensor-product mesh of quotient twists.

    Parameters
    ----------
    dimension
        Exact supported spatial dimension.
    counts
        Positive built-in integer sample counts, one per axis. Axis samples are
        ``m / count`` for ``m`` from zero through ``count - 1``.
    """

    dimension: LatticeDimension
    counts: LatticeIntegerComponents

    def __post_init__(self) -> None:
        """Validate exact dimensional sample counts."""
        if type(self.dimension) is not LatticeDimension:
            raise TypeError("dimension must be LatticeDimension")
        if type(self.counts) is not tuple:
            raise TypeError("counts must be a tuple")
        if len(self.counts) != self.dimension.value:
            raise ValueError("mesh count length must match dimension")
        if any(type(value) is not int for value in self.counts):
            raise TypeError("mesh counts must be built-in integers")
        if any(value <= 0 for value in self.counts):
            raise ValueError("mesh counts must be positive")

    @property
    def point_count(self) -> int:
        """Return the exact tensor-product point count."""
        result = 1
        for count in self.counts:
            result *= count
        return result


class BoundaryTwistMeshEnumerator:
    """Enumerate a boundary-twist mesh with the last axis varying fastest."""

    __slots__ = ()

    def execute(
        self, mesh: BoundaryTwistMesh
    ) -> tuple[BoundaryTwistRepresentative, ...]:
        """Return every quotient representative in deterministic tensor order."""
        if type(mesh) is not BoundaryTwistMesh:
            raise TypeError("mesh must be BoundaryTwistMesh")
        axes = tuple(
            tuple(float(index) / float(count) for index in range(count))
            for count in mesh.counts
        )
        result: list[BoundaryTwistRepresentative] = []
        for point in itertools.product(*axes):
            if mesh.dimension is LatticeDimension.ONE:
                closed: LatticeFloatComponents = (point[0],)
            elif mesh.dimension is LatticeDimension.TWO:
                closed = (point[0], point[1])
            else:
                closed = (point[0], point[1], point[2])
            result.append(BoundaryTwistRepresentative(mesh.dimension, closed))
        return tuple(result)
