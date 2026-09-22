r"""Software verification of ``LatticeCoordinate``.

Evidence profile: routine

Bounded artifact scope: closed integer lattice-coordinate construction.

Facet and represented meaning

The DataObject binds exact integer components to one supported dimension.

Intrinsic and cross-object scope

Component-count agreement is included.

VVUQ and scientific exclusions

This verifies lattice-index representation, not atomic Cartesian coordinates.
"""

import pytest

from ksdft2effmass.solid_state import LatticeCoordinate, LatticeDimension

pytestmark = pytest.mark.software_verification
SUT = LatticeCoordinate


class TestLatticeCoordinate:
    """Own software evidence for ``LatticeCoordinate``."""

    def test_constructor__components__rejects_dimension_mismatch(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-018

        Requirement: Component count must equal the declared dimension.

        Acceptance: A one-component coordinate declared as 2D raises ``ValueError``.
        """
        with pytest.raises(ValueError, match="count must match dimension"):
            LatticeCoordinate(LatticeDimension.TWO, (1,))
