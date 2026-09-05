r"""Software verification of ``DispatchOutcomeKind``.

Evidence profile: routine

Bounded artifact scope: the public ``DispatchOutcomeKind`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by ``DispatchOutcomeKind``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import DispatchOutcomeKind

pytestmark = pytest.mark.software_verification
SUT = DispatchOutcomeKind


class TestDispatchOutcomeKind:
    """Own software evidence for ``DispatchOutcomeKind``."""

    def test_fields__members__match_closed_contract(self) -> None:
        """Retain the exact closed member inventory.

        Evidence ID: SV-WFR-DISPATCH-OUTCOME-KIND-001

        Requirement: ``DispatchOutcomeKind`` exposes exactly its documented
        string-valued
        members in declaration order.

        Acceptance: Iteration returns the exact member-name and value tuple.
        """
        assert tuple((member.name, member.value) for member in SUT) == (
            ("CONFIRMED", "confirmed"),
            ("REJECTED", "rejected"),
            ("INDETERMINATE", "indeterminate"),
        )
