"""Public periodic scientific-model, retention, and compatibility API.

The package owns the nominal one- through three-dimensional scientific-model
hierarchy, scientific retained-space and operator records, their explicit
construction Actions, and toy-model catalogs. Crystal geometry remains owned by
:mod:`ksdft2effmass.structures.periodic`, and k-point sampling remains owned by
:mod:`ksdft2effmass.electronic_structure.sampling`. Their former periodic imports are
retained temporarily while consumers migrate; this package owns no calculator,
integration, Kohn--Sham spectrum, serializer, or scientific-acceptance policy.
"""

from .catalog import PeriodicToyModelCatalog
from .model import (
    Periodic1DDefectModel,
    Periodic1DModel,
    Periodic2DDefectModel,
    Periodic2DModel,
    Periodic3DDefectModel,
    Periodic3DModel,
    PeriodicModel,
    PeriodicModelRole,
    SpatialDimension,
)
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
from .retention import (
    PeriodicHermiticityStatus,
    PeriodicOperatorReference,
    PeriodicRepresentedRetainedOperator,
    PeriodicRepresentedRetainedOperatorConstructor,
    PeriodicRetainedOperator,
    PeriodicRetainedOperatorConstructionKind,
    PeriodicRetainedOperatorConstructor,
    PeriodicRetainedSubspace,
    PeriodicRetainedSubspaceConstructor,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)

__all__ = [
    "AtomicSpecies",
    "CoordinateConvention",
    "DirectLattice",
    "InverseLengthUnit",
    "KPointSampling",
    "KPointWeightNormalization",
    "LengthUnit",
    "Periodic1DDefectModel",
    "Periodic1DModel",
    "Periodic2DDefectModel",
    "Periodic2DModel",
    "Periodic3DDefectModel",
    "Periodic3DModel",
    "PeriodicHermiticityStatus",
    "PeriodicModel",
    "PeriodicModelRole",
    "PeriodicOperatorReference",
    "PeriodicRepresentedRetainedOperator",
    "PeriodicRepresentedRetainedOperatorConstructor",
    "PeriodicRetainedOperator",
    "PeriodicRetainedOperatorConstructionKind",
    "PeriodicRetainedOperatorConstructor",
    "PeriodicRetainedSubspace",
    "PeriodicRetainedSubspaceConstructor",
    "PeriodicRetentionDefinition",
    "PeriodicRetentionKind",
    "PeriodicSite",
    "PeriodicStructure",
    "PeriodicToyModelCatalog",
    "PhysicalDimension",
    "ReciprocalLattice",
    "ReciprocalLatticeCompatibilityValidator",
    "ReciprocalScaleConvention",
    "SpatialDimension",
    "UnitSystem",
]
