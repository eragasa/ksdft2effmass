r"""Software verification of ``NestedWorkflowMembership``.

Evidence profile: routine

Bounded artifact scope: the public ``NestedWorkflowMembership`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by
``NestedWorkflowMembership``.

Intrinsic and cross-object scope

Constructor and field invariants belong to this class. Complete cross-record replay
and package-export agreement remain with their separate owners.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows import (
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    NestedWorkflowMembership,
    NestedWorkflowMembershipIdentity,
    WorkflowRunRevisionIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = NestedWorkflowMembership


class TestNestedWorkflowMembership:
    """Own software evidence for ``NestedWorkflowMembership``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-NESTED-WORKFLOW-MEMBERSHIP-001

        Requirement: ``NestedWorkflowMembership`` declares exactly its
        documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "parent_workflow_run_identity",
            "parent_revision_identity",
            "parent_task_instance_identity",
            "child_workflow_identity",
            "child_workflow_run_identity",
        )

    def test_constructor__nested_membership__requires_distinct_child_run(self) -> None:
        """Reject parent/child membership that reuses the parent run identity.

        Evidence ID: SV-WFR-RECORDS-004

        Requirement: A nested Workflow always owns a distinct child WorkflowRun.

        Acceptance: Equal parent and child run identities raise ``ValueError``.
        """
        with pytest.raises(ValueError):
            NestedWorkflowMembership(
                identity=NestedWorkflowMembershipIdentity("membership.nested.one"),
                parent_workflow_run_identity=WorkflowRunIdentity("run.one"),
                parent_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
                parent_task_instance_identity=TaskInstanceIdentity("instance.one"),
                child_workflow_identity=WorkflowIdentity("workflow.child"),
                child_workflow_run_identity=WorkflowRunIdentity("run.one"),
            )
