r"""Software verification of ``AuthorityReservationOutcomeKind``.

Evidence profile: routine

Bounded artifact scope: the public ``AuthorityReservationOutcomeKind`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by
``AuthorityReservationOutcomeKind``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import AuthorityReservationOutcomeKind

pytestmark = pytest.mark.software_verification
SUT = AuthorityReservationOutcomeKind


class TestAuthorityReservationOutcomeKind:
    """Own software evidence for ``AuthorityReservationOutcomeKind``."""

    def test_fields__members__match_closed_contract(self) -> None:
        """Retain the exact closed member inventory.

        Evidence ID: SV-WFR-AUTHORITY-RESERVATION-OUTCOME-KIND-001

        Requirement: ``AuthorityReservationOutcomeKind`` exposes exactly its
        documented string-valued
        members in declaration order.

        Acceptance: Iteration returns the exact member-name and value tuple.
        """
        assert tuple((member.name, member.value) for member in SUT) == (
            ("RESERVED", "reserved"),
            ("CLAIMED", "claimed"),
        )
