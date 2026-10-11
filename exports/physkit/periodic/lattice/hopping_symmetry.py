"""Scalar-hopping symmetry defects and exact-real orbit projection.

The actions measure represented defects and construct the orthogonal coefficient-space
projection onto real orbit-constant hopping families.  They choose no tolerance,
scientific target, energy zero, or campaign disposition.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from projectkoios.physkit.core.results import ResultsObject
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDisplacement,
    LatticeIntegerComponents,
)
from projectkoios.physkit.periodic.lattice.hopping import (
    ScalarHoppingModel,
    ScalarHoppingTerm,
)
from projectkoios.physkit.periodic.lattice.symmetry_orbits import (
    LatticeDisplacementOrbitPartition,
)
from projectkoios.physkit.units import ScalarQuantity


@dataclass(frozen=True, slots=True)
class ScalarHoppingSymmetryDefects(ResultsObject):
    """Retain maximum absolute Hermiticity, imaginary, and orbit defects."""

    source: ScalarHoppingModel
    partition: LatticeDisplacementOrbitPartition
    maximum_hermiticity_defect: ScalarQuantity
    maximum_imaginary_part: ScalarQuantity
    maximum_orbit_defect: ScalarQuantity

    def __post_init__(self) -> None:
        """Require exact source correlation and one shared energy unit."""
        _validate_model_partition(self.source, self.partition)
        for value, name in (
            (self.maximum_hermiticity_defect, "maximum_hermiticity_defect"),
            (self.maximum_imaginary_part, "maximum_imaginary_part"),
            (self.maximum_orbit_defect, "maximum_orbit_defect"),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.unit != self.source.energy_unit:
                raise ValueError(f"{name} must use the source energy unit")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        expected = _defect_magnitudes(self.source, self.partition)
        actual = (
            self.maximum_hermiticity_defect.magnitude,
            self.maximum_imaginary_part.magnitude,
            self.maximum_orbit_defect.magnitude,
        )
        if actual != expected:
            raise ValueError("defect magnitudes must reconstruct from the source")


class ScalarHoppingSymmetryDefectAnalyzer:
    """Measure defects without modifying the supplied hopping model."""

    __slots__ = ()

    def execute(
        self,
        source: ScalarHoppingModel,
        partition: LatticeDisplacementOrbitPartition,
    ) -> ScalarHoppingSymmetryDefects:
        """Return maximum absolute defects in the source energy unit."""
        _validate_model_partition(source, partition)
        hermiticity, imaginary, orbit_defect = _defect_magnitudes(source, partition)
        unit = source.energy_unit
        return ScalarHoppingSymmetryDefects(
            source,
            partition,
            ScalarQuantity(float(hermiticity), unit),
            ScalarQuantity(float(imaginary), unit),
            ScalarQuantity(float(orbit_defect), unit),
        )


@dataclass(frozen=True, slots=True)
class ScalarHoppingSymmetryProjection(ResultsObject):
    """Correlate one source with its exact-real orbit-constant projection."""

    source: ScalarHoppingModel
    partition: LatticeDisplacementOrbitPartition
    defects: ScalarHoppingSymmetryDefects
    projected: ScalarHoppingModel
    maximum_absolute_change: ScalarQuantity

    def __post_init__(self) -> None:
        """Reconstruct support, metadata, exact reality, and orbit constancy."""
        _validate_model_partition(self.source, self.partition)
        if type(self.defects) is not ScalarHoppingSymmetryDefects:
            raise TypeError("defects must be ScalarHoppingSymmetryDefects")
        if self.defects.source is not self.source:
            raise ValueError("defects must correlate the exact source")
        if self.defects.partition is not self.partition:
            raise ValueError("defects must correlate the exact partition")
        _validate_model_partition(self.projected, self.partition)
        if self.projected.dimension is not self.source.dimension:
            raise ValueError("projected dimension must match source")
        if self.projected.energy_unit != self.source.energy_unit:
            raise ValueError("projected energy unit must match source")
        if self.projected.energy_reference != self.source.energy_reference:
            raise ValueError("projected energy reference must match source")
        if self.projected.basis_identifier != self.source.basis_identifier:
            raise ValueError("projected basis identifier must match source")
        source_values = {
            term.displacement.components: term for term in self.source.terms
        }
        projected_values = {
            term.displacement.components: term for term in self.projected.terms
        }
        expected_maximum_change = 0.0
        for orbit in self.partition.orbits:
            values = tuple(
                projected_values[member.components] for member in orbit.members
            )
            if any(value.imaginary != 0.0 for value in values):
                raise ValueError("projected coefficients must be exactly real")
            expected = _orbit_real_mean(source_values, orbit.members)
            if any(value.real != expected for value in values):
                raise ValueError(
                    "projected coefficients must equal the canonical orbit mean"
                )
            expected_maximum_change = max(
                expected_maximum_change,
                max(
                    abs(source_values[member.components].value - expected)
                    for member in orbit.members
                ),
            )
        if type(self.maximum_absolute_change) is not ScalarQuantity:
            raise TypeError("maximum_absolute_change must be ScalarQuantity")
        if self.maximum_absolute_change.unit != self.source.energy_unit:
            raise ValueError("maximum_absolute_change must use the source energy unit")
        if self.maximum_absolute_change.magnitude < 0.0:
            raise ValueError("maximum_absolute_change must be nonnegative")
        if self.maximum_absolute_change.magnitude != expected_maximum_change:
            raise ValueError("maximum_absolute_change must reconstruct from operands")


class ScalarHoppingRealOrbitProjector:
    """Project finite scalar hopping coefficients onto exact real orbit values."""

    __slots__ = ()

    def execute(
        self,
        identifier: str,
        source: ScalarHoppingModel,
        partition: LatticeDisplacementOrbitPartition,
    ) -> ScalarHoppingSymmetryProjection:
        """Average real parts canonically and set imaginary parts to zero."""
        if type(identifier) is not str:
            raise TypeError("identifier must be a string")
        if not identifier:
            raise ValueError("identifier must be nonempty")
        _validate_model_partition(source, partition)
        defects = ScalarHoppingSymmetryDefectAnalyzer().execute(source, partition)
        source_terms = {term.displacement.components: term for term in source.terms}
        projected_by_components: dict[tuple[int, ...], ScalarHoppingTerm] = {}
        maximum_change = 0.0
        for orbit in partition.orbits:
            coefficient = _orbit_real_mean(source_terms, orbit.members)
            if not math.isfinite(coefficient):
                raise ValueError("projected orbit coefficient is nonfinite")
            for member in orbit.members:
                projected_by_components[member.components] = ScalarHoppingTerm(
                    member,
                    float(coefficient),
                    0.0,
                )
                maximum_change = max(
                    maximum_change,
                    abs(source_terms[member.components].value - coefficient),
                )
        terms = tuple(
            projected_by_components[components]
            for components in sorted(projected_by_components)
        )
        projected = ScalarHoppingModel(
            identifier,
            source.dimension,
            terms,
            source.energy_unit,
            source.energy_reference,
            source.basis_identifier,
        )
        return ScalarHoppingSymmetryProjection(
            source,
            partition,
            defects,
            projected,
            ScalarQuantity(float(maximum_change), source.energy_unit),
        )


def _orbit_real_mean(
    terms: dict[LatticeIntegerComponents, ScalarHoppingTerm],
    members: tuple[LatticeDisplacement, ...],
) -> float:
    values = tuple(terms[member.components].real for member in members)
    scale = max(abs(value) for value in values)
    if scale == 0.0:
        return 0.0
    try:
        normalized_mean = math.fsum(value / scale for value in values) / float(
            len(values)
        )
    except OverflowError as error:
        raise ValueError("projected orbit coefficient is nonfinite") from error
    result = scale * normalized_mean
    if not math.isfinite(result):
        raise ValueError("projected orbit coefficient is nonfinite")
    return float(result)


def _defect_magnitudes(
    source: ScalarHoppingModel,
    partition: LatticeDisplacementOrbitPartition,
) -> tuple[float, float, float]:
    values = {term.displacement.components: term.value for term in source.terms}
    hermiticity = 0.0
    imaginary = 0.0
    orbit_defect = 0.0
    for term in source.terms:
        inverse = tuple(-component for component in term.displacement.components)
        if inverse not in values:
            raise ValueError("source support must be closed under inversion")
        hermiticity = max(
            hermiticity,
            abs(term.value - values[inverse].conjugate()),
        )
        imaginary = max(imaginary, abs(term.imaginary))
    for orbit in partition.orbits:
        orbit_values = tuple(values[member.components] for member in orbit.members)
        orbit_defect = max(
            orbit_defect,
            max(
                abs(first - second) for first in orbit_values for second in orbit_values
            ),
        )
    return float(hermiticity), float(imaginary), float(orbit_defect)


def _validate_model_partition(
    model: ScalarHoppingModel,
    partition: LatticeDisplacementOrbitPartition,
) -> None:
    if type(model) is not ScalarHoppingModel:
        raise TypeError("model must be ScalarHoppingModel")
    if type(partition) is not LatticeDisplacementOrbitPartition:
        raise TypeError("partition must be LatticeDisplacementOrbitPartition")
    if model.dimension is not partition.displacements[0].dimension:
        raise ValueError("model and partition dimensions must agree")
    model_support = tuple(term.displacement for term in model.terms)
    if model_support != partition.displacements:
        raise ValueError("model support must exactly equal the partition inventory")


__all__ = [
    "ScalarHoppingRealOrbitProjector",
    "ScalarHoppingSymmetryDefectAnalyzer",
    "ScalarHoppingSymmetryDefects",
    "ScalarHoppingSymmetryProjection",
]
