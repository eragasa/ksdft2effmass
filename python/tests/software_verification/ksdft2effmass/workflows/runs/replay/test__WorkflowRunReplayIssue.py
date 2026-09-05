r"""Software verification of ``WorkflowRunReplayIssue``.

Evidence profile: routine

Bounded artifact scope: the public ``WorkflowRunReplayIssue`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by ``WorkflowRunReplayIssue``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import WorkflowRunReplayIssue

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunReplayIssue


class TestWorkflowRunReplayIssue:
    """Own software evidence for ``WorkflowRunReplayIssue``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-WORKFLOW-RUN-REPLAY-ISSUE-001

        Requirement: ``WorkflowRunReplayIssue`` declares exactly its documented
        public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "code",
            "operation_phase",
            "diagnostic",
        )
