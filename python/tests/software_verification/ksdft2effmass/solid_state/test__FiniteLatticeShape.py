r"""Software verification of ``FiniteLatticeShape``.

Evidence profile: routine

Bounded artifact scope: closed finite-lattice shape construction.

Facet and represented meaning

The DataObject retains positive exact integer extents in 1D, 2D, or 3D.

Intrinsic and cross-object scope

Boolean rejection at the numeric boundary is included.

VVUQ and scientific exclusions

This verifies software typing and invariants, not physical domain adequacy.
"""

import pytest
from physkit.periodic.lattice.finite_domain import (
    FinitePeriodicDomain as PhysKitFinitePeriodicDomain,
)

from ksdft2effmass.solid_state import (
    FiniteLatticeShape,
    FinitePeriodicDomain,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = FiniteLatticeShape


class TestFiniteLatticeShape:
    """Own software evidence for ``FiniteLatticeShape``."""

    def test_constructor__extent__rejects_boolean_integer(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-007

        Requirement: The supported finite-domain route uses PhysKit's nominal type,
        while extents reject Boolean values despite ``bool`` subclassing ``int``.

        Acceptance: The current and compatibility names are the exact PhysKit type,
        and a Boolean 1D extent raises ``TypeError``.
        """
        assert FinitePeriodicDomain is PhysKitFinitePeriodicDomain
        assert FiniteLatticeShape is FinitePeriodicDomain
        with pytest.raises(TypeError, match="built-in integers"):
            FinitePeriodicDomain(LatticeDimension.ONE, (True,))
