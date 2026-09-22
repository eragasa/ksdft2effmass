r"""Software verification of ``MetalUnitConversionCatalog``.

Evidence profile: routine

Bounded artifact scope: the exact authorized native-to-metal definition catalog.

Facet and represented meaning

The module verifies closed pair lookup, factors, uncertainties, and pinned authority
content identities implemented from the owning architecture page.

Intrinsic and cross-object scope

``MetalUnitConversionCatalog`` is the sole system under test. Conversion execution,
aggregate-record normalization, serialization, and external calculation are excluded.

VVUQ and scientific exclusions

This is contract verification against retained authority values. It does not establish
scientific validation or propagate conversion-factor uncertainty.
"""

from decimal import Decimal

import pytest

from ksdft2effmass.units import (
    METAL_UNIT_CONVERSION_CATALOG,
    MetalUnitConversionCatalog,
    UnitIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = MetalUnitConversionCatalog


class TestMetalUnitConversionCatalog:
    """Own software evidence for the exact version-1 conversion definitions."""

    @pytest.mark.parametrize(
        ("source_unit", "target_unit", "scale", "uncertainty", "content_digest"),
        [
            pytest.param(
                UnitIdentity.HARTREE,
                UnitIdentity.ELECTRON_VOLT,
                Decimal("27.211386245981"),
                Decimal("0.000000000030"),
                "sha256:2fb00672d6de492db9619b4e532fbef55cc0029f4e7644f3def5eae5510d626b",
                id="hartree_energy_definition",
            ),
            pytest.param(
                UnitIdentity.RYDBERG,
                UnitIdentity.ELECTRON_VOLT,
                Decimal("13.6056931229905"),
                Decimal("0.000000000015"),
                "sha256:b2aaace372a88fba0d321664512c9fcd00e49094741903e28aa0cd43ee924154",
                id="rydberg_energy_definition",
            ),
            pytest.param(
                UnitIdentity.BOHR,
                UnitIdentity.ANGSTROM,
                Decimal("0.529177210544"),
                Decimal("0.000000000082"),
                "sha256:91adb62af983494f479467b143c4507b945af1e34f23d801fa3e9f172fac609c",
                id="bohr_length_definition",
            ),
            pytest.param(
                UnitIdentity.UNIFIED_ATOMIC_MASS_UNIT,
                UnitIdentity.GRAM_PER_MOLE,
                Decimal("1.00000000105"),
                Decimal("0.00000000031"),
                "sha256:12590b98302929d722bd5fa9f662c8da3534fdc576f86ceaea4c278727cea77b",
                id="atomic_to_molar_mass_definition",
            ),
        ],
    )
    def test_method__definition_for__returns_exact_versioned_definition(
        self,
        source_unit: UnitIdentity,
        target_unit: UnitIdentity,
        scale: Decimal,
        uncertainty: Decimal,
        content_digest: str,
    ) -> None:
        """Evidence ID: SV-UNITS-CONVERSION-CATALOG-001

        Requirement: Version 1 contains only exact demonstrated factors,
        uncertainties, and definition content identities.

        Acceptance: Each authorized ordered pair resolves to its retained values.
        """
        definition = METAL_UNIT_CONVERSION_CATALOG.definition_for(
            source_unit, target_unit
        )

        assert definition is not None
        assert definition.version == 1
        assert definition.decimal_scale == scale
        assert definition.standard_uncertainty == uncertainty
        assert definition.content_identity.value == content_digest

    def test_field__definitions__preserve_exact_authority_content(self) -> None:
        """Evidence ID: SV-UNITS-CONVERSION-CATALOG-002

        Requirement: Every definition binds exact LAMMPS, NIST, and BIPM source
        content identities plus numerical-policy and implementation identities.

        Acceptance: One resolved definition exposes all selected immutable identities;
        catalog construction guarantees the shared authority for the other entries.
        """
        definition = METAL_UNIT_CONVERSION_CATALOG.definition_for(
            UnitIdentity.HARTREE, UnitIdentity.ELECTRON_VOLT
        )

        assert definition is not None
        authority = definition.authority
        assert authority.lammps_units_document.content_identity.value == (
            "sha256:442a188db85bacf28bbbe47541382c09aa6ba6f2a8271bc2aadbf35d16987834"
        )
        assert authority.nist_codata_adjustment.content_identity.value == (
            "sha256:77fb90e66c40db3e6eb16630bc9c88e4c7c8beddbe5e71be406f2f26e3f67e67"
        )
        assert authority.bipm_si_brochure.content_identity.value == (
            "sha256:5442eea2c680caf77a9d96879205a97f57c7c270b98a0bd0126c18fefe47e02c"
        )
        assert authority.bipm_si_brochure.doi == "10.59161/AUEZ1291"
        assert definition.numerical_policy.identity == (
            "ksdft2effmass.units.decimal-scale-binary64.v1"
        )
        assert definition.implementation_identity == (
            "ksdft2effmass.units.MetalQuantityConverter.v1"
        )

    def test_method__definition_for__returns_none_for_unimplemented_pair(self) -> None:
        """Evidence ID: SV-UNITS-CONVERSION-CATALOG-003

        Requirement: The catalog does not infer inverse or identity conversions.

        Acceptance: Angstrom-to-bohr lookup returns ``None``.
        """
        definition = METAL_UNIT_CONVERSION_CATALOG.definition_for(
            UnitIdentity.ANGSTROM, UnitIdentity.BOHR
        )

        assert definition is None
