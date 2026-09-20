r"""Software verification of ``BravaisLattice2D``.

Evidence profile: routine

Bounded artifact scope: two-dimensional Bravais classifications.

Facet and represented meaning

The DataObject factors lattice system from conventional-cell centering.

Intrinsic and cross-object scope

All five standard combinations and a prohibited square-C combination are included.

VVUQ and scientific exclusions

This verifies allowed labels, not basis-metric compatibility.
"""

import pytest

from ksdft2effmass.solid_state import (
    BravaisCentering,
    BravaisLattice2D,
    LatticeSystem2D,
)

pytestmark = pytest.mark.software_verification
SUT = BravaisLattice2D


class TestBravaisLattice2D:
    """Own software evidence for ``BravaisLattice2D``."""

    def test_constructor__system_centering__covers_five_combinations(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-019

        Requirement: Factored records represent exactly the five standard 2D types.

        Acceptance: All five construct and square-C fails.
        """
        values = (
            BravaisLattice2D(LatticeSystem2D.OBLIQUE, BravaisCentering.P),
            BravaisLattice2D(LatticeSystem2D.RECTANGULAR, BravaisCentering.P),
            BravaisLattice2D(LatticeSystem2D.RECTANGULAR, BravaisCentering.C),
            BravaisLattice2D(LatticeSystem2D.SQUARE, BravaisCentering.P),
            BravaisLattice2D(LatticeSystem2D.HEXAGONAL, BravaisCentering.P),
        )

        assert len(values) == 5
        with pytest.raises(ValueError, match="two-dimensional"):
            BravaisLattice2D(LatticeSystem2D.SQUARE, BravaisCentering.C)
