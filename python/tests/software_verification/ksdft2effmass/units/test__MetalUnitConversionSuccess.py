r"""Software verification of ``MetalUnitConversionSuccess``.

Evidence profile: routine

Bounded artifact scope: intrinsic request-definition-output pair correlation.

Facet and represented meaning

The module verifies that a represented conversion success cannot cite a conversion
definition or output unit that contradicts its exact request.

Intrinsic and cross-object scope

``MetalUnitConversionSuccess`` is the sole system under test. The converter supplies
one valid setup result; conversion arithmetic and external authorities are excluded.

VVUQ and scientific exclusions

This is structural software verification. It establishes no numerical-verification,
scientific-validation, or uncertainty-quantification claim.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.units import (
    MetalQuantityConverter,
    MetalUnitConversionOutcome,
    MetalUnitConversionRequest,
    MetalUnitConversionSuccess,
    PhysicalDimension,
    UnitIdentity,
    UnitScalar,
)

pytestmark = pytest.mark.software_verification
SUT = MetalUnitConversionSuccess


class TestMetalUnitConversionSuccess:
    """Own software evidence for successful-result pair correlation."""

    @staticmethod
    def success() -> MetalUnitConversionSuccess:
        """Return one valid Rydberg-to-electron-volt success."""
        result = MetalQuantityConverter().convert(
            MetalUnitConversionRequest(
                UnitScalar(1.0, UnitIdentity.RYDBERG),
                UnitIdentity.ELECTRON_VOLT,
            )
        )
        assert type(result) is MetalUnitConversionSuccess
        return result

    def test_constructor__pair_correlation__rejects_contradictory_provenance(
        self,
    ) -> None:
        """Evidence ID: SV-UNITS-CONVERSION-SUCCESS-001

        Requirement: Request source, requested target, selected definition pair, and
        represented output unit must form one exact correlated conversion.

        Acceptance: Source-definition, target-definition, and output-definition unit
        contradictions each raise ``ValueError``.
        """
        result = self.success()
        wrong_source = replace(
            result.definition,
            source_unit=UnitIdentity.HARTREE,
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
        with pytest.raises(ValueError, match="output unit"):
            replace(
                result, output=UnitScalar(result.output.value, UnitIdentity.ANGSTROM)
            )

    def test_constructor__outcome__distinguishes_type_from_closed_value(self) -> None:
        """Evidence ID: SV-UNITS-CONVERSION-SUCCESS-002

        Requirement: Outcome type errors remain distinct from a valid enum member that
        represents the wrong result kind.

        Acceptance: Text raises ``TypeError`` and a non-success enum member raises
        ``ValueError``.
        """
        result = self.success()

        with pytest.raises(TypeError, match="MetalUnitConversionOutcome"):
            replace(result, outcome="converted")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="CONVERTED"):
            replace(result, outcome=MetalUnitConversionOutcome.OVERFLOW)
