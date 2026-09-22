"""Canonical metal-unit values and explicit native-to-metal conversion contracts.

The package exposes typed in-memory records only. It does not define a wire format,
rewrite native source records, or render backend-native configuration.
"""

from ._conversion import (
    METAL_UNIT_CONVERSION_CATALOG,
    METAL_UNIT_INVENTORY,
    MetalQuantityConverter,
)
from ._model import (
    AuthorityReference,
    ContentIdentity,
    MetalUnitConversionAuthority,
    MetalUnitConversionCatalog,
    MetalUnitConversionDefinition,
    MetalUnitConversionFailure,
    MetalUnitConversionFailureCode,
    MetalUnitConversionLimitation,
    MetalUnitConversionOutcome,
    MetalUnitConversionRequest,
    MetalUnitConversionResult,
    MetalUnitConversionSourceCorrelation,
    MetalUnitConversionSuccess,
    MetalUnitInventory,
    NumericalPolicy,
    PhysicalDimension,
    UnitIdentity,
    UnitScalar,
)

__all__ = [
    "METAL_UNIT_CONVERSION_CATALOG",
    "METAL_UNIT_INVENTORY",
    "AuthorityReference",
    "ContentIdentity",
    "MetalQuantityConverter",
    "MetalUnitConversionAuthority",
    "MetalUnitConversionCatalog",
    "MetalUnitConversionDefinition",
    "MetalUnitConversionFailure",
    "MetalUnitConversionFailureCode",
    "MetalUnitConversionLimitation",
    "MetalUnitConversionOutcome",
    "MetalUnitConversionRequest",
    "MetalUnitConversionResult",
    "MetalUnitConversionSourceCorrelation",
    "MetalUnitConversionSuccess",
    "MetalUnitInventory",
    "NumericalPolicy",
    "PhysicalDimension",
    "UnitIdentity",
    "UnitScalar",
]
