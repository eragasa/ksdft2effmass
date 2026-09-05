r"""Software verification of ``WorkflowRunReplayOutcomeKind``.

Evidence profile: routine

Bounded artifact scope: the public ``WorkflowRunReplayOutcomeKind`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by
``WorkflowRunReplayOutcomeKind``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows.runs import WorkflowRunReplayOutcomeKind

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunReplayOutcomeKind


class TestWorkflowRunReplayOutcomeKind:
    """Own software evidence for ``WorkflowRunReplayOutcomeKind``."""

    def test_fields__members__match_closed_contract(self) -> None:
        """Retain the exact closed member inventory.

        Evidence ID: SV-WFR-WORKFLOW-RUN-REPLAY-OUTCOME-KIND-001

        Requirement: ``WorkflowRunReplayOutcomeKind`` exposes exactly its
        documented string-valued
        members in declaration order.

        Acceptance: Iteration returns the exact member-name and value tuple.
        """
        assert tuple((member.name, member.value) for member in SUT) == (
            ("EQUAL", "equal"),
            ("UNEQUAL", "unequal"),
            ("UNSUPPORTED_VERSION", "unsupported_version"),
            ("ERROR", "error"),
        )
