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

from ksdft2effmass.solid_state import (
    FiniteLatticeCoordinateResolver,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteLatticeCoordinateResolver


class TestFiniteLatticeCoordinateResolver:
    """Own software evidence for ``FiniteLatticeCoordinateResolver``."""

    def test_method__execute__recovers_terminal_3d_coordinate(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-013

        Requirement: Inverse indexing follows last-axis-fastest ordering.

        Acceptance: Index 23 in shape ``(2,3,4)`` resolves to ``(1,2,3)``.
        """
        result = FiniteLatticeCoordinateResolver().execute(
            FiniteLatticeShape(LatticeDimension.THREE, (2, 3, 4)), 23
        )

        assert result.components == (1, 2, 3)
