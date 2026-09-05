r"""Software verification of ``TaskInvocationOutcome``.

Evidence profile: routine

Bounded artifact scope: the public ``TaskInvocationOutcome`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by ``TaskInvocationOutcome``.

Intrinsic and cross-object scope

Constructor and field invariants belong to this class. Complete cross-record replay
and package-export agreement remain with their separate owners.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import dataclass, fields

import pytest

from ksdft2effmass.workflows import (
    AttemptIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    RepresentedTaskResultProducer,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectReference,
    ResultObjectReferenceIdentity,
    ResultObjectTypeIdentity,
    ResultProducerProvenanceIdentity,
    ResultProductionRecordIdentity,
    TaskAttemptRecordIdentity,
    TaskFailureRecordIdentity,
    TaskInvocationOutcome,
    TaskInvocationOutcomeIdentity,
    TaskInvocationOutcomeKind,
)

pytestmark = pytest.mark.software_verification
SUT = TaskInvocationOutcome


@dataclass(frozen=True, slots=True)
class _SyntheticResult:
    """Provide one exact immutable ResultObject for software verification."""

    identity: ResultObjectIdentity


class TestTaskInvocationOutcome:
    """Own software evidence for ``TaskInvocationOutcome``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-TASK-INVOCATION-OUTCOME-001

        Requirement: ``TaskInvocationOutcome`` declares exactly its documented
        public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "workflow_run_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "terminal_attempt_record_identity",
            "kind",
            "results",
            "production_record_identities",
            "failure_record_identity",
            "reconciliation_identity_values",
        )

    def test_constructor__invocation_outcome__enforces_closed_variants(self) -> None:
        """Reject fields that do not match the represented invocation outcome.

        Evidence ID: SV-WFR-RECORDS-001

        Requirement: Confirmed contains results only, rejected contains one failure
        only, and indeterminate contains reconciliation identities only.

        Acceptance: Each valid variant constructs and a confirmed outcome without a
        result raises ``ValueError``.
        """
        activation_identity = self.make_activation_identity()
        operation_identity = OperationIdentity("operation.one")
        attempt_identity = AttemptIdentity("attempt.one")
        terminal_record_identity = TaskAttemptRecordIdentity("attempt.one.confirmed")
        production_identity = ResultProductionRecordIdentity("production.one")
        producer = RepresentedTaskResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.one"),
            workflow_identity=WorkflowIdentity("workflow.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            task_instance_identity=TaskInstanceIdentity("instance.one"),
            activation_identity=activation_identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_record_identity,
            outcome_identity=TaskInvocationOutcomeIdentity("outcome.confirmed"),
            production_identity=production_identity,
        )
        result = ResultObjectReference(
            identity=ResultObjectReferenceIdentity("reference.one"),
            result=_SyntheticResult(ResultObjectIdentity("result.one")),
            concrete_type_identity=ResultObjectTypeIdentity("synthetic-result.v1"),
            owning_domain_identity=ResultObjectDomainIdentity("test.synthetic"),
            content_identity=ResultObjectContentIdentity("content.one"),
            producer_provenance=producer,
        )
        confirmed = TaskInvocationOutcome(
            identity=TaskInvocationOutcomeIdentity("outcome.confirmed"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            activation_identity=activation_identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_record_identity,
            kind=TaskInvocationOutcomeKind.CONFIRMED,
            results=(result,),
            production_record_identities=(production_identity,),
        )
        rejected = TaskInvocationOutcome(
            identity=TaskInvocationOutcomeIdentity("outcome.rejected"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            activation_identity=activation_identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_record_identity,
            kind=TaskInvocationOutcomeKind.REJECTED,
            failure_record_identity=TaskFailureRecordIdentity("failure-record.one"),
        )
        indeterminate = TaskInvocationOutcome(
            identity=TaskInvocationOutcomeIdentity("outcome.indeterminate"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            activation_identity=activation_identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_record_identity,
            kind=TaskInvocationOutcomeKind.INDETERMINATE,
            reconciliation_identity_values=("reconciliation.one",),
        )

        assert confirmed.results == (result,)
        assert rejected.failure_record_identity == TaskFailureRecordIdentity(
            "failure-record.one"
        )
        assert indeterminate.reconciliation_identity_values == ("reconciliation.one",)
        with pytest.raises(ValueError):
            TaskInvocationOutcome(
                identity=TaskInvocationOutcomeIdentity("outcome.invalid"),
                workflow_run_identity=WorkflowRunIdentity("run.one"),
                activation_identity=activation_identity,
                operation_identity=operation_identity,
                attempt_identity=attempt_identity,
                terminal_attempt_record_identity=terminal_record_identity,
                kind=TaskInvocationOutcomeKind.CONFIRMED,
            )

    @staticmethod
    def make_activation_identity() -> TaskActivationIdentity:
        """Construct the exact activation identity used by record tests."""
        return TaskActivationIdentity("activation.one")
