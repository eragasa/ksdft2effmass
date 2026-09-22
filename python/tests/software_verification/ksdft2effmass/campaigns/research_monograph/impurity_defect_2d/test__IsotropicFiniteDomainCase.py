r"""Software verification of ``IsotropicFiniteDomainCase``.

Evidence profile: routine

Bounded artifact scope: one shared isotropic operator-evaluation case and its separate
analysis-channel memberships.

Facet and represented meaning

The DataObject requires boundary-phase membership plus area or shape membership and
cannot be relabeled as an orientation case.

Intrinsic and cross-object scope

A valid area/boundary membership and missing-boundary adverse case are included.

VVUQ and scientific exclusions

This is software contract evidence only; it does not execute an operator evaluation or
establish validation, UQ, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FiniteDomainChannel,
    IsotropicFiniteDomainCase,
)
from ksdft2effmass.solid_state import (
    BoundaryTwistRepresentative,
    FiniteLatticeShape,
    LatticeDimension,
)

pytestmark = pytest.mark.software_verification
SUT = IsotropicFiniteDomainCase


class TestIsotropicFiniteDomainCase:
    """Own software evidence for shared isotropic case membership."""

    def test_constructor__channel_memberships__requires_boundary_phase(self) -> None:
        """Evidence ID: SV-CAMPAIGN-DEFECT-2D-ISOTROPIC-CASE-001

        Requirement: Shared evaluation identity does not pool its analysis channels.

        Acceptance: Area and boundary-phase memberships are retained separately;
        removing boundary phase raises ``ValueError``.
        """
        case = IsotropicFiniteDomainCase(
            "case",
            "isotropic",
            FiniteLatticeShape(LatticeDimension.TWO, (6, 6)),
            "defect",
            0,
            BoundaryTwistRepresentative(LatticeDimension.TWO, (0.0, 0.0)),
            (FiniteDomainChannel.AREA, FiniteDomainChannel.BOUNDARY_PHASE),
        )

        assert case.channel_memberships == (
            FiniteDomainChannel.AREA,
            FiniteDomainChannel.BOUNDARY_PHASE,
        )
        with pytest.raises(ValueError, match="boundary-phase"):
            replace(case, channel_memberships=(FiniteDomainChannel.AREA,))
