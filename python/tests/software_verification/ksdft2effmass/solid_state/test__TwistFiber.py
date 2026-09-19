r"""Software verification of ``TwistFiber``.

Evidence profile: routine

Bounded artifact scope: gauge-qualified boundary-twist fiber identity.

Facet and represented meaning

The DataObject retains the unreduced lift, quotient representative, integer quotient,
and exact represented gauge without collapsing integer-shifted lifts.

Intrinsic and cross-object scope

A nontrivial negative lift and uniform-link gauge are included.

VVUQ and scientific exclusions

This verifies represented identity, not gauge equivalence, operator construction,
scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    BoundaryTwistReducer,
    LatticeDimension,
    TwistFiber,
    TwistGaugeRepresentation,
)

pytestmark = pytest.mark.software_verification
SUT = TwistFiber


class TestTwistFiber:
    """Own software evidence for ``TwistFiber``."""

    def test_constructor__reduction__retains_lift_representative_and_gauge(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-TWIST-FIBER-001

        Requirement: A fiber retains both lift and quotient representative roles.

        Acceptance: Lift ``(1.25,-0.25)`` retains its original values, representative
        ``(0.25,0.75)``, quotient ``(1,-1)``, and uniform-link gauge.
        """
        reduction = BoundaryTwistReducer().execute(
            BoundaryTwistLift(LatticeDimension.TWO, (1.25, -0.25))
        )

        fiber = TwistFiber(reduction, TwistGaugeRepresentation.CENTERED_UNIFORM_LINK)

        assert fiber.dimension is LatticeDimension.TWO
        assert fiber.lift.turns == (1.25, -0.25)
        assert fiber.representative.turns == (0.25, 0.75)
        assert fiber.reduction.quotient.components == (1, -1)
        assert fiber.gauge is TwistGaugeRepresentation.CENTERED_UNIFORM_LINK
