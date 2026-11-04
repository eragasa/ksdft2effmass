"""Public periodic scientific-model API.

The package owns the nominal one- through three-dimensional scientific-model
hierarchy and explicit control-model catalogs. Crystal geometry remains owned by
:mod:`ksdft2effmass.structures.periodic`, and k-point sampling remains owned by
:mod:`ksdft2effmass.electronic_structure.sampling`. This package owns no calculator,
integration, Kohn--Sham spectrum, serializer, or scientific-acceptance policy.
"""

from .catalog import PeriodicControlModelCatalog
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

__all__ = [
    "Periodic1DDefectModel",
    "Periodic1DModel",
    "Periodic2DDefectModel",
    "Periodic2DModel",
    "Periodic3DDefectModel",
    "Periodic3DModel",
    "PeriodicModel",
    "PeriodicModelRole",
    "PeriodicControlModelCatalog",
    "SpatialDimension",
]
