r"""Software verification of ``BoundaryTwistMeshEnumerator``.

Evidence profile: routine

Bounded artifact scope: exact tensor-product boundary-twist mesh enumeration.

Facet and represented meaning

The ActionObject enumerates canonical representatives with the last axis fastest.

Intrinsic and cross-object scope

Two-dimensional ordering is included.

VVUQ and scientific exclusions

This verifies enumeration, not reciprocal integration or k-point weighting.
"""

import pytest

from ksdft2effmass.solid_state import (
    BoundaryTwistMesh,
    BoundaryTwistMeshEnumerator,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = BoundaryTwistMeshEnumerator


class TestBoundaryTwistMeshEnumerator:
    """Own software evidence for ``BoundaryTwistMeshEnumerator``."""

    def test_method__execute__varies_last_axis_fastest(self) -> None:
        """Evidence ID: SV-SOLID-STATE-CORE-014

        Requirement: Tensor-product enumeration varies the last axis fastest.

        Acceptance: A ``2 by 3`` mesh begins with three second-axis points followed by
        ``(1/2,0)``.
        """
        points = BoundaryTwistMeshEnumerator().execute(
            BoundaryTwistMesh(LatticeDimension.TWO, (2, 3))
        )

        assert tuple(point.turns for point in points[:4]) == (
            (0.0, 0.0),
            (0.0, 1.0 / 3.0),
            (0.0, 2.0 / 3.0),
            (0.5, 0.0),
        )
