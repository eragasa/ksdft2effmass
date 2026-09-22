r"""Software verification of ``Lattice1D``.

Evidence profile: routine

Bounded artifact scope: verified one-dimensional lattice composition.

Facet and represented meaning

The DataObject requires correlated passing duality and Bravais-metric results.

Intrinsic and cross-object scope

Valid construction and mismatched-result rejection are included.

VVUQ and scientific exclusions

This verifies software composition, not scientific validation.
"""

import pytest

from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import (
    BravaisCentering,
    BravaisLattice1D,
    BravaisMetricCompatibilityAnalyzer,
    DirectLattice1D,
    Lattice1D,
    LatticeDualityAnalyzer,
    LatticeSystem1D,
    ReciprocalLattice1D,
)

pytestmark = pytest.mark.software_verification
SUT = Lattice1D


class TestLattice1D:
    """Own software evidence for ``Lattice1D``."""

    def test_constructor__results__requires_passing_correlation(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-012

        Requirement: Composition requires analyses of the exact retained records.

        Acceptance: A verified lattice constructs and a result for another basis fails.
        """
        length = PhysicalUnit("bohr")
        inverse_length = PhysicalUnit("1 / bohr")
        two_pi = 6.283185307179586
        direct = DirectLattice1D((1.0,), length)
        reciprocal = ReciprocalLattice1D((two_pi,), inverse_length)
        bravais = BravaisLattice1D(LatticeSystem1D.LINE, BravaisCentering.P)
        metric = BravaisMetricCompatibilityAnalyzer().execute(
            direct, bravais, relative_tolerance=1.0e-14
        )
        duality = LatticeDualityAnalyzer().execute(
            direct, reciprocal, absolute_tolerance=1.0e-14
        )

        lattice = Lattice1D(direct, reciprocal, bravais, duality, metric)

        assert lattice.duality.compatible and lattice.metric.compatible
        other_duality = LatticeDualityAnalyzer().execute(
            DirectLattice1D((2.0,), length),
            ReciprocalLattice1D((0.5 * two_pi,), inverse_length),
            absolute_tolerance=1.0e-14,
        )
        with pytest.raises(ValueError, match="correlated"):
            Lattice1D(direct, reciprocal, bravais, other_duality, metric)
