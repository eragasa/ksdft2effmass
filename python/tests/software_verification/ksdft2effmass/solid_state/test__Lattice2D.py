r"""Software verification of ``Lattice2D``.

Evidence profile: routine

Bounded artifact scope: verified two-dimensional lattice composition.

Facet and represented meaning

The DataObject composes correlated direct, reciprocal, and square-P records.

Intrinsic and cross-object scope

Passing duality and metric analysis retention is included.

VVUQ and scientific exclusions

This verifies software composition, not unique Bravais inference or validation.
"""

import pytest

from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import (
    BravaisCentering,
    BravaisLattice2D,
    BravaisMetricCompatibilityAnalyzer,
    DirectLattice2D,
    Lattice2D,
    LatticeDualityAnalyzer,
    LatticeSystem2D,
    ReciprocalLattice2D,
)

pytestmark = pytest.mark.software_verification
SUT = Lattice2D


class TestLattice2D:
    """Own software evidence for ``Lattice2D``."""

    def test_constructor__results__retains_verified_square_composition(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-021

        Requirement: Composition retains correlated passing duality and metric results.

        Acceptance: An orthogonal square-P representation constructs exactly.
        """
        length = PhysicalUnit("bohr")
        inverse_length = PhysicalUnit("1 / bohr")
        two_pi = 6.283185307179586
        direct = DirectLattice2D(((1.0, 0.0), (0.0, 1.0)), length)
        reciprocal = ReciprocalLattice2D(((two_pi, 0.0), (0.0, two_pi)), inverse_length)
        bravais = BravaisLattice2D(LatticeSystem2D.SQUARE, BravaisCentering.P)

        lattice = Lattice2D(
            direct,
            reciprocal,
            bravais,
            LatticeDualityAnalyzer().execute(
                direct, reciprocal, absolute_tolerance=1.0e-14
            ),
            BravaisMetricCompatibilityAnalyzer().execute(
                direct, bravais, relative_tolerance=1.0e-14
            ),
        )

        assert lattice.bravais.system is LatticeSystem2D.SQUARE
        assert lattice.duality.compatible and lattice.metric.compatible
