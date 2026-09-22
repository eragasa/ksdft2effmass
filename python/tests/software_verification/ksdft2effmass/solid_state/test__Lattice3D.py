r"""Software verification of ``Lattice3D``.

Evidence profile: routine

Bounded artifact scope: verified three-dimensional lattice composition.

Facet and represented meaning

The DataObject composes correlated direct, reciprocal, and cubic-P records.

Intrinsic and cross-object scope

Passing duality and metric analysis retention is included.

VVUQ and scientific exclusions

This verifies software composition, not unique Bravais inference or validation.
"""

import pytest

from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import (
    BravaisCentering,
    BravaisLattice3D,
    BravaisMetricCompatibilityAnalyzer,
    DirectLattice3D,
    Lattice3D,
    LatticeDualityAnalyzer,
    LatticeSystem3D,
    ReciprocalLattice3D,
)

pytestmark = pytest.mark.software_verification
SUT = Lattice3D


class TestLattice3D:
    """Own software evidence for ``Lattice3D``."""

    def test_constructor__results__retains_verified_cubic_composition(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-022

        Requirement: Composition retains correlated passing duality and metric results.

        Acceptance: An orthogonal cubic-P representation constructs exactly.
        """
        length = PhysicalUnit("bohr")
        inverse_length = PhysicalUnit("1 / bohr")
        two_pi = 6.283185307179586
        direct = DirectLattice3D(
            ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)), length
        )
        reciprocal = ReciprocalLattice3D(
            (
                (two_pi, 0.0, 0.0),
                (0.0, two_pi, 0.0),
                (0.0, 0.0, two_pi),
            ),
            inverse_length,
        )
        bravais = BravaisLattice3D(LatticeSystem3D.CUBIC, BravaisCentering.P)

        lattice = Lattice3D(
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

        assert lattice.bravais.system is LatticeSystem3D.CUBIC
        assert lattice.duality.compatible and lattice.metric.compatible
