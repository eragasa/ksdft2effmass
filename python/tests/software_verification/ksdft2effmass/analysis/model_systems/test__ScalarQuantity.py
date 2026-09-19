r"""Software verification of ``ScalarQuantity``.

Evidence profile: routine

Bounded artifact scope: public ScalarQuantity represented software contract.

Facet and represented meaning

The class under test owns the declared public ScalarQuantity contract.

Intrinsic and cross-object scope

Intrinsic representation and directly documented compatibility behavior are included.

VVUQ and scientific exclusions

This is software verification of unit representation or conversion behavior. It
establishes no numerical convergence, scientific validation, uncertainty
quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import ScalarQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = ScalarQuantity


class TestScalarQuantity:
    """Own software evidence for ``ScalarQuantity``."""

    def test_constructor__magnitude_and_unit__require_finite_float_and_unit(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-UNIT-003

        Requirement: ScalarQuantity binds one finite built-in float to one explicit
        supported unit.

        Acceptance: The public export is exact, one Unitless value is retained, and a
        nonfinite magnitude is rejected.
        """
        assert model_systems.ScalarQuantity is ScalarQuantity
        assert ScalarQuantity(1.0, Unitless()) == ScalarQuantity(1.0, Unitless())
        with pytest.raises(ValueError, match="finite"):
            ScalarQuantity(float("nan"), Unitless())
