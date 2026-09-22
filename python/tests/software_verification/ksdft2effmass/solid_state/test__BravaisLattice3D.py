r"""Software verification of ``BravaisLattice3D``.

Evidence profile: routine

Bounded artifact scope: three-dimensional Bravais classifications.

Facet and represented meaning

The DataObject factors seven lattice systems from P/C/I/F/R centering.

Intrinsic and cross-object scope

All fourteen standard combinations and prohibited combinations are included.

VVUQ and scientific exclusions

This verifies allowed labels, not basis-metric compatibility.
"""

import pytest

from ksdft2effmass.solid_state import (
    BravaisCentering,
    BravaisLattice3D,
    LatticeSystem3D,
)

pytestmark = pytest.mark.software_verification
SUT = BravaisLattice3D


class TestBravaisLattice3D:
    """Own software evidence for ``BravaisLattice3D``."""

    def test_constructor__system_centering__covers_fourteen_combinations(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-020

        Requirement: Factored records represent exactly the fourteen standard 3D
        system-centering combinations.

        Acceptance: All fourteen construct; tetragonal-F and rhombohedral-P fail.
        """
        values = tuple(
            BravaisLattice3D(system, centering)
            for system, centering in (
                (LatticeSystem3D.TRICLINIC, BravaisCentering.P),
                (LatticeSystem3D.MONOCLINIC, BravaisCentering.P),
                (LatticeSystem3D.MONOCLINIC, BravaisCentering.C),
                (LatticeSystem3D.ORTHORHOMBIC, BravaisCentering.P),
                (LatticeSystem3D.ORTHORHOMBIC, BravaisCentering.C),
                (LatticeSystem3D.ORTHORHOMBIC, BravaisCentering.I),
                (LatticeSystem3D.ORTHORHOMBIC, BravaisCentering.F),
                (LatticeSystem3D.TETRAGONAL, BravaisCentering.P),
                (LatticeSystem3D.TETRAGONAL, BravaisCentering.I),
                (LatticeSystem3D.RHOMBOHEDRAL, BravaisCentering.R),
                (LatticeSystem3D.HEXAGONAL, BravaisCentering.P),
                (LatticeSystem3D.CUBIC, BravaisCentering.P),
                (LatticeSystem3D.CUBIC, BravaisCentering.I),
                (LatticeSystem3D.CUBIC, BravaisCentering.F),
            )
        )

        assert len(values) == 14
        with pytest.raises(ValueError, match="three-dimensional"):
            BravaisLattice3D(LatticeSystem3D.TETRAGONAL, BravaisCentering.F)
        with pytest.raises(ValueError, match="three-dimensional"):
            BravaisLattice3D(LatticeSystem3D.RHOMBOHEDRAL, BravaisCentering.P)
