r"""Software verification of ``LatticeCoordinateTransformer``.

Evidence profile: routine

Bounded artifact scope: integral transformation of lattice-index coordinates.

Facet and represented meaning

The ActionObject applies the declared unimodular matrix to coordinate components.

Intrinsic and cross-object scope

A three-dimensional axis cycle is included.

VVUQ and scientific exclusions

This verifies integer transformation mechanics, not a material symmetry claim.
"""

import pytest

from ksdft2effmass.solid_state import (
    IntegralLatticeOperation,
    LatticeCoordinate,
    LatticeCoordinateTransformer,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = LatticeCoordinateTransformer


class TestLatticeCoordinateTransformer:
    """Own software evidence for ``LatticeCoordinateTransformer``."""

    def test_method__execute__applies_3d_axis_cycle(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-006

        Requirement: The action applies the operation matrix in the declared dimension.

        Acceptance: The axis cycle maps ``(1,2,3)`` to ``(2,3,1)``.
        """
        operation = IntegralLatticeOperation(
            "axis_cycle",
            LatticeDimension.THREE,
            ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
        )

        result = LatticeCoordinateTransformer().execute(
            operation, LatticeCoordinate(LatticeDimension.THREE, (1, 2, 3))
        )

        assert result.components == (2, 3, 1)
