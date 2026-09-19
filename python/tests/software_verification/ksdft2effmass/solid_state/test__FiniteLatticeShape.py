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

from ksdft2effmass.solid_state import FiniteLatticeShape, LatticeDimension

pytestmark = pytest.mark.software_verification
SUT = FiniteLatticeShape


class TestFiniteLatticeShape:
    """Own software evidence for ``FiniteLatticeShape``."""

    def test_constructor__extent__rejects_boolean_integer(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-007

        Requirement: Shape extents reject Boolean values despite ``bool`` subclassing
        ``int``.

        Acceptance: A Boolean 1D extent raises ``TypeError``.
        """
        with pytest.raises(TypeError, match="built-in integers"):
            FiniteLatticeShape(LatticeDimension.ONE, (True,))
