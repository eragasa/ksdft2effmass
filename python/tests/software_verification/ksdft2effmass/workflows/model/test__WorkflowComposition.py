r"""Software verification of ``WorkflowComposition``.

Evidence profile: routine

Bounded artifact scope: the public ``WorkflowComposition`` DataObject.

Facet and represented meaning

The class records Task-instance membership for one reusable Workflow definition.

Intrinsic and cross-object scope

Tests cover tuple-only membership and unique run-scoped Task-instance identities.

VVUQ and scientific exclusions

This is software verification. Membership establishes no prerequisite closure,
activation, execution, scientific validity, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import (
    TaskDefinitionIdentity,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowComposition,
    WorkflowIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowComposition


def test_constructor__task_instances__retains_unique_tuple_membership() -> None:
    """Test the complete valid ``WorkflowComposition`` field mapping.

    Evidence ID: SV-WFM-COMPOSITION-001

    Requirement: Composition binds one Workflow identity to an immutable tuple of
    uniquely identified run-scoped Task instances.

    Acceptance: Construction retains the exact Workflow and member objects.
    """
    workflow = WorkflowIdentity("workflow.one")
    member = TaskInstance(
        TaskInstanceIdentity("instance.one"), TaskDefinitionIdentity("task.one"), None
    )
    value = SUT(workflow, (member,))
    assert value.workflow_identity is workflow
    assert value.task_instances == (member,)


def test_constructor__task_instances__rejects_mutable_or_duplicate_membership() -> None:
    """Test collection and identity closure for Workflow membership.

    Evidence ID: SV-WFM-COMPOSITION-002

    Requirement: Membership is a tuple and each Task-instance identity occurs once.

    Acceptance: A list raises ``TypeError`` and repeated membership raises
    ``ValueError``.
    """
    workflow = WorkflowIdentity("workflow.one")
    member = TaskInstance(
        TaskInstanceIdentity("instance.one"), TaskDefinitionIdentity("task.one"), None
    )
    with pytest.raises(TypeError):
        SUT(workflow, [member])  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        SUT(workflow, (member, member))
