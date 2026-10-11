"""Dimensionful finite scalar-hopping Frobenius geometry.

The comparison sums over one explicitly declared complete displacement inventory.  It
preserves physical units and does not choose a scientific normalization or threshold.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from projectkoios.physkit.core.results import ResultsObject
from projectkoios.physkit.periodic.lattice.hopping import ScalarHoppingModel
from projectkoios.physkit.periodic.lattice.symmetry_orbits import (
    LatticeDisplacementOrbitPartition,
)
from projectkoios.physkit.units import PhysicalUnit, ScalarQuantity, Unitless


@dataclass(frozen=True, slots=True)
class ScalarHoppingFrobeniusDistance(ResultsObject):
    """Retain full-inventory squared and root Frobenius distances."""

    left: ScalarHoppingModel
    right: ScalarHoppingModel
    partition: LatticeDisplacementOrbitPartition
    squared_distance: ScalarQuantity
    distance: ScalarQuantity
    maximum_absolute_difference: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate operand compatibility, support correlation, and result units."""
        _validate_operands(self.left, self.right, self.partition)
        for value, name in (
            (self.squared_distance, "squared_distance"),
            (self.distance, "distance"),
            (self.maximum_absolute_difference, "maximum_absolute_difference"),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if self.squared_distance.unit != _squared_unit(self.left.energy_unit):
            raise ValueError("squared_distance must use the squared energy unit")
        if self.distance.unit != self.left.energy_unit:
            raise ValueError("distance must use the hopping energy unit")
        if self.maximum_absolute_difference.unit != self.left.energy_unit:
            raise ValueError(
                "maximum_absolute_difference must use the hopping energy unit"
            )
        expected = _distance_magnitudes(self.left, self.right)
        actual = (
            self.squared_distance.magnitude,
            self.distance.magnitude,
            self.maximum_absolute_difference.magnitude,
        )
        if actual != expected:
            raise ValueError("distance values must reconstruct from the operands")


class ScalarHoppingFrobeniusDistanceAnalyzer:
    """Compare two compatible complete scalar hopping families."""

    __slots__ = ()

    def execute(
        self,
        left: ScalarHoppingModel,
        right: ScalarHoppingModel,
        partition: LatticeDisplacementOrbitPartition,
    ) -> ScalarHoppingFrobeniusDistance:
        """Return the full represented-block distance without normalization."""
        _validate_operands(left, right, partition)
        squared, distance, maximum = _distance_magnitudes(left, right)
        unit = left.energy_unit
        return ScalarHoppingFrobeniusDistance(
            left,
            right,
            partition,
            ScalarQuantity(float(squared), _squared_unit(unit)),
            ScalarQuantity(float(distance), unit),
            ScalarQuantity(float(maximum), unit),
        )


def _distance_magnitudes(
    left: ScalarHoppingModel,
    right: ScalarHoppingModel,
) -> tuple[float, float, float]:
    contributions: list[float] = []
    components: list[float] = []
    has_underflowed_square = False
    maximum = 0.0
    for left_term, right_term in zip(left.terms, right.terms, strict=True):
        real = left_term.real - right_term.real
        imaginary = left_term.imaginary - right_term.imaginary
        if not math.isfinite(real) or not math.isfinite(imaginary):
            raise ValueError("hopping coefficient difference is nonfinite")
        components.extend((real, imaginary))
        real_square = real * real
        imaginary_square = imaginary * imaginary
        if not math.isfinite(real_square) or not math.isfinite(imaginary_square):
            raise ValueError("squared hopping difference is nonfinite")
        has_underflowed_square = has_underflowed_square or (
            (real != 0.0 and real_square == 0.0)
            or (imaginary != 0.0 and imaginary_square == 0.0)
        )
        contributions.append(real_square + imaginary_square)
        maximum = max(maximum, math.hypot(real, imaginary))
    distance = math.hypot(*components)
    if not math.isfinite(distance):
        raise ValueError("Frobenius distance is nonfinite")
    try:
        squared = (
            distance * distance if has_underflowed_square else math.fsum(contributions)
        )
    except OverflowError as error:
        raise ValueError("Frobenius squared distance is nonfinite") from error
    if not math.isfinite(squared):
        raise ValueError("Frobenius squared distance is nonfinite")
    return float(squared), float(distance), float(maximum)


def _validate_operands(
    left: ScalarHoppingModel,
    right: ScalarHoppingModel,
    partition: LatticeDisplacementOrbitPartition,
) -> None:
    if type(left) is not ScalarHoppingModel:
        raise TypeError("left must be ScalarHoppingModel")
    if type(right) is not ScalarHoppingModel:
        raise TypeError("right must be ScalarHoppingModel")
    if type(partition) is not LatticeDisplacementOrbitPartition:
        raise TypeError("partition must be LatticeDisplacementOrbitPartition")
    expected_support = partition.displacements
    if tuple(term.displacement for term in left.terms) != expected_support:
        raise ValueError("left support must exactly equal the partition inventory")
    if tuple(term.displacement for term in right.terms) != expected_support:
        raise ValueError("right support must exactly equal the partition inventory")
    if left.dimension is not right.dimension:
        raise ValueError("hopping dimensions must agree")
    if left.dimension is not expected_support[0].dimension:
        raise ValueError("hopping and partition dimensions must agree")
    if left.energy_unit != right.energy_unit:
        raise ValueError("hopping energy units must agree")
    if left.energy_reference != right.energy_reference:
        raise ValueError("hopping energy references must agree")
    if left.basis_identifier != right.basis_identifier:
        raise ValueError("hopping basis identifiers must agree")


def _squared_unit(unit: PhysicalUnit | Unitless) -> PhysicalUnit | Unitless:
    if type(unit) is Unitless:
        return Unitless()
    return PhysicalUnit(f"({unit.expression}) ** 2")


__all__ = [
    "ScalarHoppingFrobeniusDistance",
    "ScalarHoppingFrobeniusDistanceAnalyzer",
]
