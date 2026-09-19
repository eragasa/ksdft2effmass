r"""Software verification of ``FiniteLatticeIndexer``.

Evidence profile: routine

Bounded artifact scope: finite-lattice coordinate-to-index conversion.

Facet and represented meaning

The ActionObject applies the declared last-axis-fastest ordering in 1D, 2D, and 3D.

Intrinsic and cross-object scope

Closed dimensional inputs and terminal indices are included.

VVUQ and scientific exclusions

This verifies represented indexing, not a physical lattice or calculation result.
"""

import pytest

from ksdft2effmass.solid_state import (
    FiniteLatticeIndexer,
    FiniteLatticeShape,
    LatticeCoordinate,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteLatticeIndexer


class TestFiniteLatticeIndexer:
    """Own software evidence for ``FiniteLatticeIndexer``."""

    def test_method__execute__uses_last_axis_fastest_in_all_dimensions(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-002

        Requirement: Indexing is closed over 1D, 2D, and 3D with the last axis fastest.

        Acceptance: Hand-derived terminal indices are 3, 5, and 23.
        """
        indexer = FiniteLatticeIndexer()

        assert (
            indexer.execute(
                FiniteLatticeShape(LatticeDimension.ONE, (4,)),
                LatticeCoordinate(LatticeDimension.ONE, (3,)),
            )
            == 3
        )
        assert (
            indexer.execute(
                FiniteLatticeShape(LatticeDimension.TWO, (2, 3)),
                LatticeCoordinate(LatticeDimension.TWO, (1, 2)),
            )
            == 5
        )
        assert (
            indexer.execute(
                FiniteLatticeShape(LatticeDimension.THREE, (2, 3, 4)),
                LatticeCoordinate(LatticeDimension.THREE, (1, 2, 3)),
            )
            == 23
        )
