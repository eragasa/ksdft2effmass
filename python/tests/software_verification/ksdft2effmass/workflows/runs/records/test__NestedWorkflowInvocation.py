r"""Software verification of ``NestedWorkflowInvocation``.

Evidence profile: routine

Bounded artifact scope: the public ``NestedWorkflowInvocation`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by
``NestedWorkflowInvocation``.

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
    AttemptIdentity,
    OperationIdentity,
    TaskActivationIdentity,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    ChildWorkflowCreationIdempotencyIdentity,
    NestedWorkflowInvocation,
    NestedWorkflowInvocationIdentity,
    NestedWorkflowInvocationKind,
    NestedWorkflowObservationIdentity,
    ResultDependencyIdentity,
    ResultObjectReferenceIdentity,
    TaskAttemptRecordIdentity,
    WorkflowRunReplayResultIdentity,
    WorkflowRunRevisionIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = NestedWorkflowInvocation


class TestNestedWorkflowInvocation:
    """Own software evidence for ``NestedWorkflowInvocation``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-NESTED-WORKFLOW-INVOCATION-001

        Requirement: ``NestedWorkflowInvocation`` declares exactly its
        documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "parent_workflow_run_identity",
            "parent_revision_identity",
            "parent_task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "attempt_record_identity",
            "child_workflow_identity",
            "child_workflow_run_identity",
            "input_result_reference_identities",
            "child_creation_idempotency_identity",
            "kind",
            "terminal_observation_identity",
            "terminal_child_revision_identity",
            "replay_equal_child_result_identity",
            "exported_result_reference_identities",
            "export_admission_dependency_identities",
            "failure_record_identity",
            "reconciliation_identity_values",
        )

    def test_constructor__nested_invocation__enforces_closed_observations(self) -> None:
        """Admit only variant-appropriate nested terminal observation fields.

        Evidence ID: SV-WFR-RECORDS-005

        Requirement: Confirmed alone carries a replay-equal terminal child revision
        and paired exports/admissions; indeterminate carries reconciliation identities
        and exports nothing.

        Acceptance: Valid confirmed and indeterminate records construct, while a
        pending record containing a terminal observation raises ``ValueError``.
        """
        confirmed = self.make_nested_invocation(
            identity="invocation.one",
            kind=NestedWorkflowInvocationKind.CONFIRMED,
            terminal_observation_identity=NestedWorkflowObservationIdentity(
                "observation.one"
            ),
            terminal_child_revision_identity=WorkflowRunRevisionIdentity(
                "revision.child.terminal"
            ),
            replay_equal_child_result_identity=(self.make_replay_result_identity()),
            exported_result_reference_identities=(
                ResultObjectReferenceIdentity("reference.child"),
            ),
            export_admission_dependency_identities=(
                ResultDependencyIdentity("dependency.admission"),
            ),
        )
        indeterminate = self.make_nested_invocation(
            identity="invocation.two",
            kind=NestedWorkflowInvocationKind.INDETERMINATE,
            terminal_observation_identity=NestedWorkflowObservationIdentity(
                "observation.two"
            ),
            reconciliation_identity_values=("child-read.one",),
        )

        assert confirmed.child_workflow_run_identity == WorkflowRunIdentity("run.child")
        assert indeterminate.exported_result_reference_identities == ()
        with pytest.raises(ValueError):
            self.make_nested_invocation(
                identity="invocation.invalid",
                kind=NestedWorkflowInvocationKind.PENDING,
                terminal_observation_identity=NestedWorkflowObservationIdentity(
                    "observation.invalid"
                ),
            )

    @staticmethod
    def make_nested_invocation(
        *,
        identity: str,
        kind: NestedWorkflowInvocationKind,
        terminal_observation_identity: NestedWorkflowObservationIdentity | None = None,
        terminal_child_revision_identity: WorkflowRunRevisionIdentity | None = None,
        replay_equal_child_result_identity: WorkflowRunReplayResultIdentity
        | None = None,
        exported_result_reference_identities: tuple[
            ResultObjectReferenceIdentity, ...
        ] = (),
        export_admission_dependency_identities: tuple[
            ResultDependencyIdentity, ...
        ] = (),
        reconciliation_identity_values: tuple[str, ...] = (),
    ) -> NestedWorkflowInvocation:
        """Construct one nested invocation for closed-variant evidence."""
        return NestedWorkflowInvocation(
            identity=NestedWorkflowInvocationIdentity(identity),
            parent_workflow_run_identity=WorkflowRunIdentity("run.one"),
            parent_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            parent_task_instance_identity=TaskInstanceIdentity("instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            attempt_record_identity=TaskAttemptRecordIdentity("attempt.one.confirmed"),
            child_workflow_identity=WorkflowIdentity("workflow.child"),
            child_workflow_run_identity=WorkflowRunIdentity("run.child"),
            input_result_reference_identities=(),
            child_creation_idempotency_identity=(
                ChildWorkflowCreationIdempotencyIdentity("child-create.one")
            ),
            kind=kind,
            terminal_observation_identity=terminal_observation_identity,
            terminal_child_revision_identity=terminal_child_revision_identity,
            replay_equal_child_result_identity=replay_equal_child_result_identity,
            exported_result_reference_identities=(exported_result_reference_identities),
            export_admission_dependency_identities=(
                export_admission_dependency_identities
            ),
            reconciliation_identity_values=reconciliation_identity_values,
        )

    @staticmethod
    def make_replay_result_identity() -> WorkflowRunReplayResultIdentity:
        """Construct one syntactically exact child replay-result identity."""
        return WorkflowRunReplayResultIdentity("a" * 64)
