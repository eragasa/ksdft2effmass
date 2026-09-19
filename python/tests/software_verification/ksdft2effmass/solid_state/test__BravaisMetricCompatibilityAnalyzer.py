r"""Software verification of ``BravaisMetricCompatibilityAnalyzer``.

Evidence profile: routine

Bounded artifact scope: caller-toleranced conventional-cell metric compatibility.

Facet and represented meaning

The ActionObject checks normalized required invariants without inferring unique type.

Intrinsic and cross-object scope

Constrained 2D and 3D lattice systems and explicit failures are included.

VVUQ and scientific exclusions

This verifies represented metric rules, not material classification or validation.
"""

import pytest

from ksdft2effmass.operators import PhysicalUnit
from ksdft2effmass.solid_state import (
    BravaisCentering,
    BravaisLattice2D,
    BravaisLattice3D,
    BravaisMetricCompatibilityAnalyzer,
    DirectLattice2D,
    DirectLattice3D,
    LatticeSystem2D,
    LatticeSystem3D,
)

pytestmark = pytest.mark.software_verification
SUT = BravaisMetricCompatibilityAnalyzer


class TestBravaisMetricCompatibilityAnalyzer:
    """Own software evidence for ``BravaisMetricCompatibilityAnalyzer``."""

    def test_method__execute__checks_2d_conventional_invariants(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-010

        Requirement: 2D analysis checks required conventional metric invariants.

        Acceptance: Square and hexagonal metrics pass; unequal rectangular axes fail
        square-P while passing rectangular-C.
        """
        length = PhysicalUnit("bohr")
        analyzer = BravaisMetricCompatibilityAnalyzer()
        square_type = BravaisLattice2D(LatticeSystem2D.SQUARE, BravaisCentering.P)
        rectangular_type = BravaisLattice2D(
            LatticeSystem2D.RECTANGULAR, BravaisCentering.C
        )
        hexagonal_type = BravaisLattice2D(LatticeSystem2D.HEXAGONAL, BravaisCentering.P)
        unequal = DirectLattice2D(((2.0, 0.0), (0.0, 1.0)), length)

        square = analyzer.execute(
            DirectLattice2D(((1.0, 0.0), (0.0, 1.0)), length),
            square_type,
            relative_tolerance=1.0e-14,
        )
        not_square = analyzer.execute(unequal, square_type, relative_tolerance=1.0e-14)
        rectangular = analyzer.execute(
            unequal, rectangular_type, relative_tolerance=1.0e-14
        )
        hexagonal = analyzer.execute(
            DirectLattice2D(((1.0, 0.0), (0.5, 0.8660254037844386)), length),
            hexagonal_type,
            relative_tolerance=1.0e-14,
        )

        assert square.compatible
        assert not_square.issue_codes == (
            "SOLID_STATE.BRAVAIS_METRIC.RESIDUAL_EXCEEDED",
        )
        assert rectangular.compatible
        assert hexagonal.compatible

    def test_method__execute__checks_3d_conventional_invariants(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-011

        Requirement: 3D analysis checks each constrained lattice-system metric.

        Acceptance: Monoclinic, orthorhombic, tetragonal, rhombohedral, hexagonal,
        and cubic examples pass; a nonorthogonal cubic metric fails.
        """
        length = PhysicalUnit("bohr")
        analyzer = BravaisMetricCompatibilityAnalyzer()
        tolerance = 1.0e-12
        monoclinic = analyzer.execute(
            DirectLattice3D(
                ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.25, 0.0, 1.0)), length
            ),
            BravaisLattice3D(LatticeSystem3D.MONOCLINIC, BravaisCentering.C),
            relative_tolerance=tolerance,
        )
        orthorhombic = analyzer.execute(
            DirectLattice3D(
                ((1.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 3.0)), length
            ),
            BravaisLattice3D(LatticeSystem3D.ORTHORHOMBIC, BravaisCentering.P),
            relative_tolerance=tolerance,
        )
        tetragonal = analyzer.execute(
            DirectLattice3D(
                ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 2.0)), length
            ),
            BravaisLattice3D(LatticeSystem3D.TETRAGONAL, BravaisCentering.I),
            relative_tolerance=tolerance,
        )
        rhombohedral = analyzer.execute(
            DirectLattice3D(
                (
                    (1.0, 0.0, 0.0),
                    (0.5, 0.8660254037844386, 0.0),
                    (0.5, 0.28867513459481287, 0.816496580927726),
                ),
                length,
            ),
            BravaisLattice3D(LatticeSystem3D.RHOMBOHEDRAL, BravaisCentering.R),
            relative_tolerance=tolerance,
        )
        hexagonal = analyzer.execute(
            DirectLattice3D(
                (
                    (1.0, 0.0, 0.0),
                    (0.5, 0.8660254037844386, 0.0),
                    (0.0, 0.0, 2.0),
                ),
                length,
            ),
            BravaisLattice3D(LatticeSystem3D.HEXAGONAL, BravaisCentering.P),
            relative_tolerance=tolerance,
        )
        cubic_type = BravaisLattice3D(LatticeSystem3D.CUBIC, BravaisCentering.F)
        cubic = analyzer.execute(
            DirectLattice3D(
                ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)), length
            ),
            cubic_type,
            relative_tolerance=tolerance,
        )
        not_cubic = analyzer.execute(
            DirectLattice3D(
                ((1.0, 0.0, 0.0), (0.1, 1.0, 0.0), (0.0, 0.0, 1.0)), length
            ),
            cubic_type,
            relative_tolerance=tolerance,
        )

        assert monoclinic.compatible
        assert orthorhombic.compatible
        assert tetragonal.compatible
        assert rhombohedral.compatible
        assert hexagonal.compatible
        assert cubic.compatible
        assert not_cubic.issue_codes == (
            "SOLID_STATE.BRAVAIS_METRIC.RESIDUAL_EXCEEDED",
        )
