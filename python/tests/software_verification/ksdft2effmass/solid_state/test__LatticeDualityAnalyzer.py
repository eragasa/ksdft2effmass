r"""Software verification of ``LatticeDualityAnalyzer``.

Evidence profile: routine

Bounded artifact scope: caller-toleranced direct--reciprocal duality analysis.

Facet and represented meaning

The ActionObject checks ``A B^T = 2*pi*I`` after explicit unit conversion.

Intrinsic and cross-object scope

Orthogonal 1D, 2D, and 3D bases and one residual failure are included.

VVUQ and scientific exclusions

This verifies represented duality, not physical basis alignment or validation.
"""

import pytest

from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import (
    DirectLattice1D,
    DirectLattice2D,
    DirectLattice3D,
    LatticeDualityAnalyzer,
    ReciprocalLattice1D,
    ReciprocalLattice2D,
    ReciprocalLattice3D,
)

pytestmark = pytest.mark.software_verification
SUT = LatticeDualityAnalyzer


class TestLatticeDualityAnalyzer:
    """Own software evidence for ``LatticeDualityAnalyzer``."""

    def test_method__execute__checks_two_pi_duality_in_all_dimensions(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-009

        Requirement: The analyzer checks direct--reciprocal duality with caller-owned
        tolerance in 1D, 2D, and 3D.

        Acceptance: Orthogonal unit bases pass at ``1e-14`` and value one fails in 1D.
        """
        length = PhysicalUnit("bohr")
        inverse_length = PhysicalUnit("1 / bohr")
        two_pi = 6.283185307179586
        analyzer = LatticeDualityAnalyzer()
        one = analyzer.execute(
            DirectLattice1D((1.0,), length),
            ReciprocalLattice1D((two_pi,), inverse_length),
            absolute_tolerance=1.0e-14,
        )
        two = analyzer.execute(
            DirectLattice2D(((1.0, 0.0), (0.0, 1.0)), length),
            ReciprocalLattice2D(((two_pi, 0.0), (0.0, two_pi)), inverse_length),
            absolute_tolerance=1.0e-14,
        )
        three = analyzer.execute(
            DirectLattice3D(
                ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)), length
            ),
            ReciprocalLattice3D(
                (
                    (two_pi, 0.0, 0.0),
                    (0.0, two_pi, 0.0),
                    (0.0, 0.0, two_pi),
                ),
                inverse_length,
            ),
            absolute_tolerance=1.0e-14,
        )
        mismatch = analyzer.execute(
            DirectLattice1D((1.0,), length),
            ReciprocalLattice1D((1.0,), inverse_length),
            absolute_tolerance=1.0e-14,
        )

        assert one.compatible and one.maximum_absolute_residual == 0.0
        assert two.compatible and two.maximum_absolute_residual == 0.0
        assert three.compatible and three.maximum_absolute_residual == 0.0
        assert mismatch.issue_codes == (
            "SOLID_STATE.LATTICE_DUALITY.RESIDUAL_EXCEEDED",
        )
