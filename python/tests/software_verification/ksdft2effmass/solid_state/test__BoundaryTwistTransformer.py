r"""Software verification of ``BoundaryTwistTransformer``.

Evidence profile: routine

Bounded artifact scope: signed-axis-permutation transformation of twist lifts.

Facet and represented meaning

The ActionObject accepts orthogonal signed permutations and rejects general shears.

Intrinsic and cross-object scope

A 3D axis cycle and a 2D unimodular shear are included.

VVUQ and scientific exclusions

This verifies the bounded transform contract, not gauge-equivalent observables.
"""

import pytest

from ksdft2effmass.solid_state import (
    BoundaryTwistLift,
    BoundaryTwistTransformer,
    IntegralLatticeOperation,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = BoundaryTwistTransformer


class TestBoundaryTwistTransformer:
    """Own software evidence for ``BoundaryTwistTransformer``."""

    def test_method__execute__accepts_signed_permutation_and_rejects_shear(
        self,
    ) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-016

        Requirement: Twist transformation is restricted to signed axis permutations.

        Acceptance: A 3D cycle maps the turns and a general unimodular shear fails.
        """
        cycle = IntegralLatticeOperation(
            "axis_cycle",
            LatticeDimension.THREE,
            ((0, 1, 0), (0, 0, 1), (1, 0, 0)),
        )
        shear = IntegralLatticeOperation(
            "shear", LatticeDimension.TWO, ((1, 1), (0, 1))
        )

        result = BoundaryTwistTransformer().execute(
            cycle, BoundaryTwistLift(LatticeDimension.THREE, (0.1, 0.2, 0.3))
        )

        assert result.turns == (0.2, 0.3, 0.1)
        assert not shear.is_signed_axis_permutation
        with pytest.raises(ValueError, match="signed axis permutation"):
            BoundaryTwistTransformer().execute(
                shear, BoundaryTwistLift(LatticeDimension.TWO, (0.1, 0.2))
            )
