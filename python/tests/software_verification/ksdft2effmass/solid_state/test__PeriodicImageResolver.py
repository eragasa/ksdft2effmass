r"""Software verification of ``PeriodicImageResolver``.

Evidence profile: routine

Bounded artifact scope: periodic representative and quotient resolution.

Facet and represented meaning

The ActionObject retains Euclidean wrapping quotients for every axis.

Intrinsic and cross-object scope

Negative and positive multi-axis boundary crossings are included.

VVUQ and scientific exclusions

This verifies integer quotient mechanics, not boundary-phase physics.
"""

import pytest

from ksdft2effmass.solid_state import (
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
    PeriodicImageResolver,
)

pytestmark = pytest.mark.software_verification
SUT = PeriodicImageResolver


class TestPeriodicImageResolver:
    """Own software evidence for ``PeriodicImageResolver``."""

    def test_method__execute__retains_negative_crossing_quotients(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-003

        Requirement: Periodic wrapping uses Euclidean division and retains quotients.

        Acceptance: ``(-1,7,-9)`` in ``(4,5,6)`` maps to ``(3,2,3)`` with quotient
        ``(-1,1,-2)``.
        """
        result = PeriodicImageResolver().execute(
            FiniteLatticeShape(LatticeDimension.THREE, (4, 5, 6)),
            LatticeCoordinate(LatticeDimension.THREE, (-1, 7, -9)),
        )

        assert result.coordinate.components == (3, 2, 3)
        assert result.quotient.components == (-1, 1, -2)
