r"""Software verification of ``BravaisLattice1D``.

Evidence profile: routine

Bounded artifact scope: one-dimensional Bravais classification.

Facet and represented meaning

The DataObject accepts only the standard line-P classification.

Intrinsic and cross-object scope

The unique valid combination and one prohibited centering are included.

VVUQ and scientific exclusions

This verifies classification labels, not metric inference or physical validity.
"""

import pytest

from ksdft2effmass.solid_state import (
    BravaisCentering,
    BravaisLattice1D,
    LatticeSystem1D,
)

pytestmark = pytest.mark.software_verification
SUT = BravaisLattice1D


class TestBravaisLattice1D:
    """Own software evidence for ``BravaisLattice1D``."""

    def test_constructor__system_centering__accepts_only_line_primitive(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-008

        Requirement: The sole 1D Bravais classification is line-P.

        Acceptance: Line-P constructs and line-C fails.
        """
        result = BravaisLattice1D(LatticeSystem1D.LINE, BravaisCentering.P)

        assert result.centering is BravaisCentering.P
        with pytest.raises(ValueError, match="line P"):
            BravaisLattice1D(LatticeSystem1D.LINE, BravaisCentering.C)
