r"""Software verification of ``DispatchOutcomeRecord``.

Evidence profile: routine

Bounded artifact scope: the public ``DispatchOutcomeRecord`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by ``DispatchOutcomeRecord``.

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
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    DispatchOutcomeKind,
    DispatchOutcomeRecord,
    DispatchOutcomeRecordIdentity,
    ExecutionGrantIdentity,
    ObligationIdentity,
    ResultObjectReferenceIdentity,
    ScientificExecutorIdentity,
    SimulationDispatchOutcomeIdentity,
    SimulationExecutionRequestIdentity,
    TaskFailureRecordIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = DispatchOutcomeRecord


class TestDispatchOutcomeRecord:
    """Own software evidence for ``DispatchOutcomeRecord``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-DISPATCH-OUTCOME-RECORD-001

        Requirement: ``DispatchOutcomeRecord`` declares exactly its documented
        public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "envelope_identity",
            "workflow_run_identity",
            "request_identity",
            "task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "executor_identity",
            "obligation_identity",
            "grant_identity",
            "kind",
            "result_reference_identity",
            "failure_record_identity",
            "reconciliation_identity_values",
        )

    def test_constructor__dispatch_outcome__enforces_closed_variants(self) -> None:
        """Prohibit fabricated results on rejected or indeterminate dispatch.

        Evidence ID: SV-WFR-CONTROL-002

        Requirement: Confirmed alone references a returned ResultObject; rejected
        references one failure; indeterminate retains reconciliation identities only.

        Acceptance: All valid variants construct and indeterminate with a result raises
        ``ValueError``.
        """
        confirmed = self.make_dispatch_outcome(
            identity="dispatch.confirmed",
            kind=DispatchOutcomeKind.CONFIRMED,
            result_reference_identity=ResultObjectReferenceIdentity("reference.one"),
        )
        rejected = self.make_dispatch_outcome(
            identity="dispatch.rejected",
            kind=DispatchOutcomeKind.REJECTED,
            failure_record_identity=TaskFailureRecordIdentity("failure.one"),
        )
        indeterminate = self.make_dispatch_outcome(
            identity="dispatch.indeterminate",
            kind=DispatchOutcomeKind.INDETERMINATE,
            reconciliation_identity_values=("dispatch-read.one",),
        )

        assert confirmed.result_reference_identity is not None
        assert rejected.failure_record_identity is not None
        assert indeterminate.reconciliation_identity_values == ("dispatch-read.one",)
        with pytest.raises(ValueError):
            self.make_dispatch_outcome(
                identity="dispatch.invalid",
                kind=DispatchOutcomeKind.INDETERMINATE,
                result_reference_identity=ResultObjectReferenceIdentity(
                    "reference.invalid"
                ),
                reconciliation_identity_values=("dispatch-read.one",),
            )

    @staticmethod
    def make_dispatch_outcome(
        *,
        identity: str,
        kind: DispatchOutcomeKind,
        result_reference_identity: ResultObjectReferenceIdentity | None = None,
        failure_record_identity: TaskFailureRecordIdentity | None = None,
        reconciliation_identity_values: tuple[str, ...] = (),
    ) -> DispatchOutcomeRecord:
        """Construct one specialized dispatch observation for variant evidence."""
        return DispatchOutcomeRecord(
            identity=DispatchOutcomeRecordIdentity(identity),
            envelope_identity=SimulationDispatchOutcomeIdentity(f"envelope.{identity}"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            task_instance_identity=TaskInstanceIdentity("instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            obligation_identity=ObligationIdentity("obligation.one"),
            grant_identity=ExecutionGrantIdentity("grant.one"),
            kind=kind,
            result_reference_identity=result_reference_identity,
            failure_record_identity=failure_record_identity,
            reconciliation_identity_values=reconciliation_identity_values,
        )
