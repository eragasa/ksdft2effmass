r"""Software verification of ``OrientationFiniteDomainCase``.

Evidence profile: routine

Bounded artifact scope: one three-evaluation orientation comparison record.

Facet and represented meaning

The DataObject correlates swapped geometry and twist components while keeping source
and swapped parent identities distinct.

Intrinsic and cross-object scope

A valid swapped pair and unswapped-target attack are included.

VVUQ and scientific exclusions

This is software contract evidence only; it does not execute an operator evaluation or
establish validation, UQ, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    OrientationFiniteDomainCase,
)
from ksdft2effmass.solid_state import (
    BoundaryTwistRepresentative,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = OrientationFiniteDomainCase


class TestOrientationFiniteDomainCase:
    """Own software evidence for one orientation comparison record."""

    def test_constructor__swapped_geometry_and_twist__requires_covariant_pair(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-ORIENTATION-CASE-001

        Requirement: Target geometry and twist are exact axis swaps of the source.

        Acceptance: A valid pair represents three evaluations; retaining the unswapped
        target twist raises ``ValueError``.
        """
        source_twist = BoundaryTwistRepresentative(
            LatticeDimension.TWO, (1.0 / 9.0, 2.0 / 9.0)
        )
        case = OrientationFiniteDomainCase(
            "case",
            "anisotropic_source",
            "anisotropic_swapped",
            FiniteLatticeShape(LatticeDimension.TWO, (8, 18)),
            FiniteLatticeShape(LatticeDimension.TWO, (18, 8)),
            "defect",
            11,
            source_twist,
            BoundaryTwistRepresentative(LatticeDimension.TWO, (2.0 / 9.0, 1.0 / 9.0)),
        )

        assert case.operator_evaluation_count == 3
        with pytest.raises(ValueError, match="swap source components"):
            replace(case, target_twist=source_twist)
