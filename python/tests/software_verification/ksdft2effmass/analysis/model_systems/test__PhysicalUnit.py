r"""Software verification of ``PhysicalUnit``.

Evidence profile: routine

Bounded artifact scope: public PhysicalUnit represented software contract.

Facet and represented meaning

The class under test owns the declared public PhysicalUnit contract.

Intrinsic and cross-object scope

Intrinsic representation and directly documented compatibility behavior are included.

VVUQ and scientific exclusions

This is software verification of unit representation or conversion behavior. It
establishes no numerical convergence, scientific validation, uncertainty
quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import PhysicalUnit

pytestmark = pytest.mark.software_verification
SUT = PhysicalUnit


class TestPhysicalUnit:
    """Own software evidence for ``PhysicalUnit``."""

    def test_constructor__expression__excludes_absent_and_dimensionless_units(
        self,
    ) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-UNIT-001

        Requirement: PhysicalUnit stores a nonempty physical-unit expression and
        leaves dimensionless values to the distinct Unitless type.

        Acceptance: The public export is exact, meter is retained, and empty or
        dimensionless expressions are rejected.
        """
        assert model_systems.PhysicalUnit is PhysicalUnit
        assert PhysicalUnit("meter").expression == "meter"
        with pytest.raises(ValueError, match="nonempty"):
            PhysicalUnit("")
        with pytest.raises(ValueError, match="require Unitless"):
            PhysicalUnit("dimensionless")
        with pytest.raises(ValueError, match="valid Pint unit"):
            PhysicalUnit("not_a_unit")
