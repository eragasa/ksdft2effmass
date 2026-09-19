r"""Software verification of public units package surface.

Evidence profile: routine

Bounded artifact scope: documented public package exports for typed unit conversion.

Facet and represented meaning

The module verifies import availability and does not duplicate behavioral evidence.

Intrinsic and cross-object scope

The public package surface is the sole artifact under test. Conversion behavior,
serialization, and domain adapters are excluded.

VVUQ and scientific exclusions

This structural test establishes no numerical or scientific claim.
"""

import pytest

import ksdft2effmass.units as units

pytestmark = pytest.mark.software_verification


class TestUnitsPublicApi:
    """Own structural evidence for documented package exports."""

    def test_public_api__package__exports_documented_contract(self) -> None:
        """Evidence ID: SV-UNITS-PUBLIC-API-001

        Requirement: The package exposes every documented class and catalog through
        the supported package import path.

        Acceptance: ``__all__`` equals the closed expected export-name set.
        """
        assert set(units.__all__) == {
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
        }
