r"""Software verification of ``TaskExecutionContext``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskExecutionContext`` DataObject.

Facet and represented meaning

The class records exact Workflow, run, Task, activation, operation, and attempt
correlation supplied to a Task.

Intrinsic and cross-object scope

Tests cover the complete nominal field map and rejection of equal-looking wrong
identity classes.

VVUQ and scientific exclusions

This is software verification. Context does not establish authority, execution,
scientific validity, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.workflows import (
    AttemptIdentity,
    OperationIdentity,
    TaskActivationIdentity,
    TaskExecutionContext,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = TaskExecutionContext


def test_constructor__fields__retains_complete_correlation_context() -> None:
    """Test the complete valid ``TaskExecutionContext`` field mapping.

    Evidence ID: SV-WFM-CONTEXT-001

    Requirement: Context stores six distinct nominal correlation identities.

    Acceptance: Every public field retains the exact supplied identity object.
    """
    workflow = WorkflowIdentity("workflow.one")
    run = WorkflowRunIdentity("run.one")
    instance = TaskInstanceIdentity("instance.one")
    activation = TaskActivationIdentity("activation.one")
    operation = OperationIdentity("operation.one")
    attempt = AttemptIdentity("attempt.one")
    value = SUT(workflow, run, instance, activation, operation, attempt)
    assert value.workflow_identity is workflow
    assert value.workflow_run_identity is run
    assert value.task_instance_identity is instance
    assert value.task_activation_identity is activation
    assert value.operation_identity is operation
    assert value.attempt_identity is attempt


def test_constructor__workflow_identity__rejects_equal_looking_wrong_nominal_type() -> (
    None
):
    """Test nominal separation at the Workflow identity field.

    Evidence ID: SV-WFM-CONTEXT-002

    Requirement: Equal lexical values do not make Workflow and WorkflowRun
    identities interchangeable.

    Acceptance: Supplying ``WorkflowRunIdentity`` as ``workflow_identity`` raises
    ``TypeError``.
    """
    with pytest.raises(TypeError):
        SUT(
            WorkflowRunIdentity("workflow.one"),  # type: ignore[arg-type]
            WorkflowRunIdentity("run.one"),
            TaskInstanceIdentity("instance.one"),
            TaskActivationIdentity("activation.one"),
            OperationIdentity("operation.one"),
            AttemptIdentity("attempt.one"),
        )
