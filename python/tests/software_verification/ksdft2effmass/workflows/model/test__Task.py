r"""Software verification of ``Task``.

Evidence profile: routine

Bounded artifact scope: the public ``Task`` structural ActionObject protocol.

Facet and represented meaning

The protocol defines one reusable operation over named bound results and explicit
execution context.

Intrinsic and cross-object scope

Tests cover structural identity and the approved ``execute(inputs, context)`` call
boundary using an independent in-process implementation.

VVUQ and scientific exclusions

This is software verification. The synthetic operation performs no calculator effect,
scientific calculation, validation, uncertainty quantification, or acceptance.
"""

from dataclasses import dataclass

import pytest

from ksdft2effmass.workflows import (
    AttemptIdentity,
    OperationIdentity,
    ResultObject,
    ResultObjectIdentity,
    Task,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskExecutionContext,
    TaskInputBinding,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = Task


def test_protocol__execute__accepts_approved_structural_call_boundary() -> None:
    """Test ``Task.execute`` with named results and explicit correlation context.

    Evidence ID: SV-WFM-TASK-PROTOCOL-001

    Requirement: A Task structurally exposes ``TaskDefinitionIdentity`` and accepts
    exactly the approved input tuple plus ``TaskExecutionContext``.

    Acceptance: An independent implementation conforms and returns the exact bound
    result without requiring nominal inheritance.
    """

    @dataclass(frozen=True, slots=True)
    class ConcreteResult:
        identity: ResultObjectIdentity

    @dataclass(frozen=True, slots=True)
    class ConcreteTask:
        identity: TaskDefinitionIdentity

        def execute(
            self,
            inputs: tuple[TaskInputBinding, ...],
            context: TaskExecutionContext,
        ) -> tuple[ResultObject, ...]:
            assert context.operation_identity == OperationIdentity("operation.one")
            return tuple(item.result for item in inputs)

    result = ConcreteResult(ResultObjectIdentity("result.one"))
    task = ConcreteTask(TaskDefinitionIdentity("task.one"))
    context = TaskExecutionContext(
        WorkflowIdentity("workflow.one"),
        WorkflowRunIdentity("run.one"),
        TaskInstanceIdentity("instance.one"),
        TaskActivationIdentity("activation.one"),
        OperationIdentity("operation.one"),
        AttemptIdentity("attempt.one"),
    )
    assert isinstance(task, SUT)
    assert task.execute((TaskInputBinding("input.one", result),), context) == (result,)
