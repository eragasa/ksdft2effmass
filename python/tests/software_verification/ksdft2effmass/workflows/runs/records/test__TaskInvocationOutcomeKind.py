r"""Software verification of ``TaskInvocationOutcomeKind``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskInvocationOutcomeKind`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by ``TaskInvocationOutcomeKind``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import TaskInvocationOutcomeKind

pytestmark = pytest.mark.software_verification
SUT = TaskInvocationOutcomeKind


class TestTaskInvocationOutcomeKind:
    """Own software evidence for ``TaskInvocationOutcomeKind``."""

    def test_fields__members__match_closed_contract(self) -> None:
        """Retain the exact closed member inventory.

        Evidence ID: SV-WFR-TASK-INVOCATION-OUTCOME-KIND-001

        Requirement: ``TaskInvocationOutcomeKind`` exposes exactly its
        documented string-valued
        members in declaration order.

        Acceptance: Iteration returns the exact member-name and value tuple.
        """
        assert tuple((member.name, member.value) for member in SUT) == (
            ("CONFIRMED", "confirmed"),
            ("REJECTED", "rejected"),
            ("INDETERMINATE", "indeterminate"),
        )
