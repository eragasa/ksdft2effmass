"""Compatibility imports for the former periodic model module.

New code imports crystal geometry from :mod:`ksdft2effmass.structures.periodic` and
k-point sampling from :mod:`ksdft2effmass.electronic_structure.sampling`. This module
contains no independent definitions and will be removed after current consumers and
schema-version-1 compatibility surfaces migrate.
"""

from ksdft2effmass.electronic_structure.sampling import (
    KPointSampling,
    KPointWeightNormalization,
)
from ksdft2effmass.structures.periodic import (
    AtomicSpecies,
    CoordinateConvention,
    DirectLattice,
    InverseLengthUnit,
    LengthUnit,
    PeriodicSite,
    PeriodicStructure,
    PhysicalDimension,
    ReciprocalLattice,
    ReciprocalLatticeCompatibilityValidator,
    ReciprocalScaleConvention,
    UnitSystem,
)

__all__ = [
    "AtomicSpecies",
    "CoordinateConvention",
    "DirectLattice",
    "InverseLengthUnit",
    "KPointSampling",
    "KPointWeightNormalization",
    "LengthUnit",
    "PeriodicSite",
    "PeriodicStructure",
    "PhysicalDimension",
    "ReciprocalLattice",
    "ReciprocalLatticeCompatibilityValidator",
    "ReciprocalScaleConvention",
    "UnitSystem",
]
