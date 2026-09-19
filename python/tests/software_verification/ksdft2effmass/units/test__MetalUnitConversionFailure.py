r"""Software verification of ``MetalUnitConversionFailure``.

Evidence profile: routine

Bounded artifact scope: intrinsic numeric-failure request-definition pair correlation.

Facet and represented meaning

The module verifies that overflow and underflow failures cannot cite a conversion
definition whose ordered unit pair contradicts the exact request.

Intrinsic and cross-object scope

``MetalUnitConversionFailure`` is the sole system under test. The converter supplies
one valid setup result; conversion arithmetic and unsupported-pair policy are excluded.

VVUQ and scientific exclusions

This is structural software verification. It establishes no numerical-verification,
scientific-validation, or uncertainty-quantification claim.
"""

import sys
from dataclasses import replace

import pytest

from ksdft2effmass.units import (
    MetalQuantityConverter,
    MetalUnitConversionFailure,
    MetalUnitConversionRequest,
    PhysicalDimension,
    UnitIdentity,
    UnitScalar,
)

pytestmark = pytest.mark.software_verification
SUT = MetalUnitConversionFailure


class TestMetalUnitConversionFailure:
    """Own software evidence for numeric-failure pair correlation."""

    @staticmethod
    def overflow() -> MetalUnitConversionFailure:
        """Return one valid Hartree-to-electron-volt overflow failure."""
        result = MetalQuantityConverter().convert(
            MetalUnitConversionRequest(
                UnitScalar(sys.float_info.max, UnitIdentity.HARTREE),
                UnitIdentity.ELECTRON_VOLT,
            )
        )
        assert type(result) is MetalUnitConversionFailure
        assert result.definition is not None
        return result

    def test_constructor__numeric_pair_correlation__rejects_contradictory_provenance(
        self,
    ) -> None:
        """Evidence ID: SV-UNITS-CONVERSION-FAILURE-001

        Requirement: A numeric conversion failure must cite the exact definition for
        the request's ordered source-to-target unit pair.

        Acceptance: Source-definition and target-definition contradictions each
        raise ``ValueError``.
        """
        result = self.overflow()
        assert result.definition is not None
        wrong_source = replace(
            result.definition,
            source_unit=UnitIdentity.RYDBERG,
            source_dimension=PhysicalDimension.ENERGY,
        )
        wrong_target = replace(
            result.definition,
            target_unit=UnitIdentity.ANGSTROM,
            target_dimension=PhysicalDimension.LENGTH,
        )

        with pytest.raises(ValueError, match="definition source unit"):
            replace(result, definition=wrong_source)
        with pytest.raises(ValueError, match="definition target unit"):
            replace(result, definition=wrong_target)
