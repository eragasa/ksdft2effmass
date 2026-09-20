r"""Software verification of ``BoundaryTwistReducer``.

Evidence profile: routine

Bounded artifact scope: boundary-twist lift reduction.

Facet and represented meaning

The ActionObject separates unreduced lifts, unit-cell representatives, and quotients.

Intrinsic and cross-object scope

Negative turns and retained quotient components are included.

VVUQ and scientific exclusions

This verifies represented quotient reduction, not finite-domain observables.
"""

import pytest

from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    BoundaryTwistReducer,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = BoundaryTwistReducer


class TestBoundaryTwistReducer:
    """Own software evidence for ``BoundaryTwistReducer``."""

    def test_method__execute__separates_representative_and_quotient(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-004

        Requirement: Reduction retains a representative and integer quotient.

        Acceptance: ``(0.25,-0.25)`` becomes ``(0.25,0.75)`` with ``(0,-1)``.
        """
        result = BoundaryTwistReducer().execute(
            BoundaryTwistLift(LatticeDimension.TWO, (0.25, -0.25))
        )

        assert result.representative.turns == (0.25, 0.75)
        assert result.quotient.components == (0, -1)
