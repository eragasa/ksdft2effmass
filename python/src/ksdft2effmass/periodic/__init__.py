"""Temporary compatibility API for former periodic imports.

New code imports crystal geometry from :mod:`ksdft2effmass.structures.periodic` and
k-point sampling from :mod:`ksdft2effmass.electronic_structure.sampling`. The
compatibility package defines no independent public records and intentionally exports
no calculator, integration, Kohn--Sham spectrum, or serializer classes.
"""

from .models import (
    AtomicSpecies,
    CoordinateConvention,
    DirectLattice,
    InverseLengthUnit,
    KPointSampling,
    KPointWeightNormalization,
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
