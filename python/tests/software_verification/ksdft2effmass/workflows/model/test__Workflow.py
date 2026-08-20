r"""Software verification of ``Workflow``.

Evidence profile: routine

Bounded artifact scope: the public ``Workflow`` structural composite protocol.

Facet and represented meaning

The protocol is a reusable composition that is also accepted wherever a Task is used.

Intrinsic and cross-object scope

Tests cover structural Task behavior plus exact Workflow identity and composition
members without a runtime engine or WorkflowRun aggregate.

VVUQ and scientific exclusions

This is software verification. The synthetic composition performs no Task effect,
scientific calculation, validation, uncertainty quantification, or acceptance.
"""

from dataclasses import dataclass

import pytest

from ksdft2effmass.workflows import (
    ResultObject,
    Task,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
    Workflow,
    WorkflowComposition,
    WorkflowIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = Workflow


def test_protocol__composition__is_structurally_both_workflow_and_task() -> None:
    """Test the approved structural nesting relation of ``Workflow``.

    Evidence ID: SV-WFM-WORKFLOW-PROTOCOL-001

    Requirement: A Workflow exposes Task identity and execution plus exact Workflow
    identity and immutable composition properties.

    Acceptance: An independent implementation satisfies both ``Workflow`` and ``Task``
    runtime protocols without inheriting either.
    """

    @dataclass(frozen=True, slots=True)
    class ConcreteWorkflow:
        identity: TaskDefinitionIdentity
        workflow_identity: WorkflowIdentity
        composition: WorkflowComposition

        def execute(
            self,
            inputs: tuple[TaskInputBinding, ...],
            context: TaskExecutionContext,
        ) -> tuple[ResultObject, ...]:
            return tuple(item.result for item in inputs)

    workflow_identity = WorkflowIdentity("workflow.one")
    workflow = ConcreteWorkflow(
        TaskDefinitionIdentity("workflow.task.one"),
        workflow_identity,
        WorkflowComposition(workflow_identity, ()),
    )
    assert isinstance(workflow, SUT)
    assert isinstance(workflow, Task)
    assert workflow.composition.workflow_identity is workflow_identity
