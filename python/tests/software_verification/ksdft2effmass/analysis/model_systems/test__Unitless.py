r"""Software verification of ``Unitless``.

Evidence profile: routine

Bounded artifact scope: public Unitless represented software contract.

Facet and represented meaning

The class under test owns the declared public Unitless contract.

Intrinsic and cross-object scope

Intrinsic representation and directly documented compatibility behavior are included.

VVUQ and scientific exclusions

This is software verification of unit representation or conversion behavior. It
establishes no numerical convergence, scientific validation, uncertainty
quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.analysis import model_systems
from ksdft2effmass.analysis.model_systems import Unitless

pytestmark = pytest.mark.software_verification
SUT = Unitless


class TestUnitless:
    """Own software evidence for ``Unitless``."""

    def test_property__expression__is_first_class_dimensionless_unit(self) -> None:
        """Evidence ID: SV-MODEL-SYSTEM-UNIT-002

        Requirement: Unitless is a public unit type rather than absent metadata.

        Acceptance: The public export is exact and a Unitless instance identifies
        Pint's canonical dimensionless expression.
        """
        assert model_systems.Unitless is Unitless
        assert Unitless().expression == "dimensionless"
