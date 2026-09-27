r"""Software verification of ``FiniteLatticeCoordinateResolver``.

Evidence profile: routine

Bounded artifact scope: finite-lattice index-to-coordinate conversion.

Facet and represented meaning

The ActionObject inverts last-axis-fastest indexing.

Intrinsic and cross-object scope

Three-dimensional terminal-coordinate recovery is included.

VVUQ and scientific exclusions

This verifies represented indexing, not physical geometry or scientific validation.
"""

import pytest
from physkit.periodic.lattice.finite_domain import (
    FinitePeriodicCoordinateResolver as PhysKitFinitePeriodicCoordinateResolver,
)

from ksdft2effmass.solid_state import (
    FiniteLatticeCoordinateResolver,
    FinitePeriodicCoordinateResolver,
    FinitePeriodicDomain,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteLatticeCoordinateResolver


class TestFiniteLatticeCoordinateResolver:
    """Own software evidence for ``FiniteLatticeCoordinateResolver``."""

    def test_method__execute__recovers_terminal_3d_coordinate(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-013

        Requirement: The supported resolver route uses PhysKit's nominal type and
        follows last-axis-fastest ordering.

        Acceptance: Current and compatibility names are the exact PhysKit type, and
        index 23 in domain ``(2,3,4)`` resolves to ``(1,2,3)``.
        """
        assert (
            FinitePeriodicCoordinateResolver is PhysKitFinitePeriodicCoordinateResolver
        )
        assert FiniteLatticeCoordinateResolver is FinitePeriodicCoordinateResolver
        result = FinitePeriodicCoordinateResolver().execute(
            FinitePeriodicDomain(LatticeDimension.THREE, (2, 3, 4)), 23
        )

        assert result.components == (1, 2, 3)
