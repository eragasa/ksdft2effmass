"""Bounded dispatch values in the WorkflowRun wire representation."""

from __future__ import annotations

from ksdft2effmass.workflows.artifacts import (
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
)
from ksdft2effmass.workflows.model import (
    AttemptIdentity,
    OperationIdentity,
    TaskActivationIdentity,
    TaskInstanceIdentity,
)
from ksdft2effmass.workflows.runs.identities import (
    DispatchCreationIdempotencyIdentity,
    DispatchDestinationIdentity,
    DispatchObservationRecordIdentity,
    DispatchOutcomeRecordIdentity,
    DispatchResourceScopeIdentity,
    ExecutionGrantIdentity,
    ObligationDispositionIdentity,
    ObligationIdentity,
    ResultObjectReferenceIdentity,
    ScientificExecutorIdentity,
    SimulationDispatchEntryIdentity,
    SimulationDispatchEntryReceiptIdentity,
    SimulationDispatchObservationIdentity,
    SimulationDispatchOutcomeIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestCorrelationIdentity,
    SimulationExecutionRequestIdentity,
    TaskAttemptRecordIdentity,
    TaskFailureRecordIdentity,
)
from ksdft2effmass.workflows.runs.records import (
    DispatchObservationKind,
    DispatchObservationRecord,
    DispatchOutcomeKind,
    DispatchOutcomeRecord,
    ObligationDisposition,
    ObligationDispositionKind,
    SimulationDispatchEntry,
    SimulationDispatchObligation,
    SimulationDispatchOutcome,
    SimulationExecutionRequestCorrelation,
    TaskInvocationFailure,
)

from ...model import (
    ResultObject,
    WorkflowRunIdentity,
)
from ...runs.identities import (
    AuthorityReservationOutcomeIdentity,
    WorkflowRunRevisionIdentity,
)
from ..records import (
    WorkflowEncodedResultValue,
)
from ._base import (
    _ResultJson,
    _RunValue,
    _WorkflowRunWireSerializer,
    _WorkflowRunWireUnsupported,
)


class _WorkflowRunDispatchWireSerializer(_WorkflowRunWireSerializer):
    """Encode and decode the closed dispatch value family."""

    def _encode_dispatch(
        self, value: _RunValue, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _ResultJson:
        if type(value) is DispatchObservationKind:
            return self._record("DispatchObservationKind", {"value": value.value})
        if type(value) is DispatchOutcomeKind:
            return self._record("DispatchOutcomeKind", {"value": value.value})
        if type(value) is ObligationDispositionKind:
            return self._record("ObligationDispositionKind", {"value": value.value})
        if type(value) is DispatchCreationIdempotencyIdentity:
            return self._record(
                "DispatchCreationIdempotencyIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is DispatchDestinationIdentity:
            return self._record(
                "DispatchDestinationIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is DispatchObservationRecord:
            return self._record(
                "DispatchObservationRecord",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "request_identity": self._encode(value.request_identity, seen),
                    "obligation_identity": self._encode(
                        value.obligation_identity, seen
                    ),
                    "dispatch_entry_identity": self._encode(
                        value.dispatch_entry_identity, seen
                    ),
                    "dispatch_entry_receipt_identity": self._encode(
                        value.dispatch_entry_receipt_identity, seen
                    ),
                    "outcome_identity": self._encode(value.outcome_identity, seen),
                    "kind": self._encode(value.kind, seen),
                    "observed_outcomes": self._encode(value.observed_outcomes, seen),
                    "reconciliation_identity_values": self._encode(
                        value.reconciliation_identity_values, seen
                    ),
                },
            )
        if type(value) is DispatchObservationRecordIdentity:
            return self._record(
                "DispatchObservationRecordIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is DispatchOutcomeRecord:
            return self._record(
                "DispatchOutcomeRecord",
                {
                    "identity": self._encode(value.identity, seen),
                    "envelope_identity": self._encode(value.envelope_identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "request_identity": self._encode(value.request_identity, seen),
                    "task_instance_identity": self._encode(
                        value.task_instance_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "executor_identity": self._encode(value.executor_identity, seen),
                    "obligation_identity": self._encode(
                        value.obligation_identity, seen
                    ),
                    "grant_identity": self._encode(value.grant_identity, seen),
                    "kind": self._encode(value.kind, seen),
                    "result_reference_identity": self._encode(
                        value.result_reference_identity, seen
                    ),
                    "failure_record_identity": self._encode(
                        value.failure_record_identity, seen
                    ),
                    "reconciliation_identity_values": self._encode(
                        value.reconciliation_identity_values, seen
                    ),
                },
            )
        if type(value) is DispatchOutcomeRecordIdentity:
            return self._record(
                "DispatchOutcomeRecordIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is DispatchResourceScopeIdentity:
            return self._record(
                "DispatchResourceScopeIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ObligationDisposition:
            return self._record(
                "ObligationDisposition",
                {
                    "identity": self._encode(value.identity, seen),
                    "obligation_identity": self._encode(
                        value.obligation_identity, seen
                    ),
                    "request_identity": self._encode(value.request_identity, seen),
                    "dispatch_outcome_record_identity": self._encode(
                        value.dispatch_outcome_record_identity, seen
                    ),
                    "attempt_record_identity": self._encode(
                        value.attempt_record_identity, seen
                    ),
                    "kind": self._encode(value.kind, seen),
                    "predecessor_disposition_identity": self._encode(
                        value.predecessor_disposition_identity, seen
                    ),
                    "reconciliation_identity_values": self._encode(
                        value.reconciliation_identity_values, seen
                    ),
                },
            )
        if type(value) is ObligationDispositionIdentity:
            return self._record(
                "ObligationDispositionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ObligationIdentity:
            return self._record(
                "ObligationIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is SimulationDispatchEntry:
            return self._record(
                "SimulationDispatchEntry",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "predecessor_revision_identity": self._encode(
                        value.predecessor_revision_identity, seen
                    ),
                    "committed_revision_identity": self._encode(
                        value.committed_revision_identity, seen
                    ),
                    "claimed_reservation_identity": self._encode(
                        value.claimed_reservation_identity, seen
                    ),
                    "request_identity": self._encode(value.request_identity, seen),
                    "obligation_identity": self._encode(
                        value.obligation_identity, seen
                    ),
                    "receipt_identity": self._encode(value.receipt_identity, seen),
                    "outcome_identity": self._encode(value.outcome_identity, seen),
                },
            )
        if type(value) is SimulationDispatchEntryIdentity:
            return self._record(
                "SimulationDispatchEntryIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is SimulationDispatchEntryReceiptIdentity:
            return self._record(
                "SimulationDispatchEntryReceiptIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is SimulationDispatchObligation:
            return self._record(
                "SimulationDispatchObligation",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "workflow_run_revision_identity": self._encode(
                        value.workflow_run_revision_identity, seen
                    ),
                    "request_identity": self._encode(value.request_identity, seen),
                    "task_instance_identity": self._encode(
                        value.task_instance_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "executor_identity": self._encode(value.executor_identity, seen),
                    "grant_identity": self._encode(value.grant_identity, seen),
                    "destination_identity": self._encode(
                        value.destination_identity, seen
                    ),
                    "resource_scope_identities": self._encode(
                        value.resource_scope_identities, seen
                    ),
                    "creation_idempotency_identity": self._encode(
                        value.creation_idempotency_identity, seen
                    ),
                },
            )
        if type(value) is SimulationDispatchObservationIdentity:
            return self._record(
                "SimulationDispatchObservationIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is SimulationDispatchOutcome:
            return self._record(
                "SimulationDispatchOutcome",
                {
                    "identity": self._encode(value.identity, seen),
                    "observation_identity": self._encode(
                        value.observation_identity, seen
                    ),
                    "request_identity": self._encode(value.request_identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "task_instance_identity": self._encode(
                        value.task_instance_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "executor_identity": self._encode(value.executor_identity, seen),
                    "obligation_identity": self._encode(
                        value.obligation_identity, seen
                    ),
                    "grant_identity": self._encode(value.grant_identity, seen),
                    "kind": self._encode(value.kind, seen),
                    "result": self._encode(value.result, seen),
                    "native_output_manifest_identity": self._encode(
                        value.native_output_manifest_identity, seen
                    ),
                    "native_output_manifest_entry_identities": self._encode(
                        value.native_output_manifest_entry_identities, seen
                    ),
                    "failure": self._encode(value.failure, seen),
                    "reconciliation_identity_values": self._encode(
                        value.reconciliation_identity_values, seen
                    ),
                },
            )
        if type(value) is SimulationDispatchOutcomeIdentity:
            return self._record(
                "SimulationDispatchOutcomeIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is SimulationExecutionRequestCorrelation:
            return self._record(
                "SimulationExecutionRequestCorrelation",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "task_instance_identity": self._encode(
                        value.task_instance_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "attempt_record_identity": self._encode(
                        value.attempt_record_identity, seen
                    ),
                    "request_identity": self._encode(value.request_identity, seen),
                    "executor_identity": self._encode(value.executor_identity, seen),
                    "obligation_identity": self._encode(
                        value.obligation_identity, seen
                    ),
                    "grant_identity": self._encode(value.grant_identity, seen),
                    "authorization_result_identity": self._encode(
                        value.authorization_result_identity, seen
                    ),
                    "input_result_reference_identities": self._encode(
                        value.input_result_reference_identities, seen
                    ),
                    "input_artifact_entry_identities": self._encode(
                        value.input_artifact_entry_identities, seen
                    ),
                },
            )
        if type(value) is SimulationExecutionRequestCorrelationIdentity:
            return self._record(
                "SimulationExecutionRequestCorrelationIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is SimulationExecutionRequestIdentity:
            return self._record(
                "SimulationExecutionRequestIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        raise _WorkflowRunWireUnsupported

    def _decode_dispatch(
        self, tag: str, wire: _ResultJson, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _RunValue:
        record: _RunValue
        if tag == "DispatchObservationKind":
            return DispatchObservationKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "DispatchOutcomeKind":
            return DispatchOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ObligationDispositionKind":
            return ObligationDispositionKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "DispatchCreationIdempotencyIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = DispatchCreationIdempotencyIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "DispatchDestinationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = DispatchDestinationIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "DispatchObservationRecord":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "request_identity",
                    "obligation_identity",
                    "dispatch_entry_identity",
                    "dispatch_entry_receipt_identity",
                    "outcome_identity",
                    "kind",
                    "observed_outcomes",
                    "reconciliation_identity_values",
                ),
            )
            record = DispatchObservationRecord(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    DispatchObservationRecordIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    SimulationExecutionRequestIdentity,
                ),
                obligation_identity=self._exact(
                    self._decode(fields["obligation_identity"], seen),
                    ObligationIdentity,
                ),
                dispatch_entry_identity=self._exact(
                    self._decode(fields["dispatch_entry_identity"], seen),
                    SimulationDispatchEntryIdentity,
                ),
                dispatch_entry_receipt_identity=self._exact(
                    self._decode(fields["dispatch_entry_receipt_identity"], seen),
                    SimulationDispatchEntryReceiptIdentity,
                ),
                outcome_identity=self._exact(
                    self._decode(fields["outcome_identity"], seen),
                    SimulationDispatchOutcomeIdentity,
                ),
                kind=self._exact(
                    self._decode(fields["kind"], seen), DispatchObservationKind
                ),
                observed_outcomes=tuple(
                    self._exact(item, SimulationDispatchOutcome)
                    for item in self._items(
                        self._decode(fields["observed_outcomes"], seen)
                    )
                ),
                reconciliation_identity_values=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["reconciliation_identity_values"], seen)
                    )
                ),
            )
            return record
        if tag == "DispatchObservationRecordIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = DispatchObservationRecordIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "DispatchOutcomeRecord":
            fields = self._fields(
                wire,
                tag,
                (
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
                ),
            )
            record = DispatchOutcomeRecord(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    DispatchOutcomeRecordIdentity,
                ),
                envelope_identity=self._exact(
                    self._decode(fields["envelope_identity"], seen),
                    SimulationDispatchObservationIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    SimulationExecutionRequestIdentity,
                ),
                task_instance_identity=self._exact(
                    self._decode(fields["task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
                activation_identity=self._exact(
                    self._decode(fields["activation_identity"], seen),
                    TaskActivationIdentity,
                ),
                operation_identity=self._exact(
                    self._decode(fields["operation_identity"], seen), OperationIdentity
                ),
                attempt_identity=self._exact(
                    self._decode(fields["attempt_identity"], seen), AttemptIdentity
                ),
                executor_identity=self._exact(
                    self._decode(fields["executor_identity"], seen),
                    ScientificExecutorIdentity,
                ),
                obligation_identity=self._exact(
                    self._decode(fields["obligation_identity"], seen),
                    ObligationIdentity,
                ),
                grant_identity=self._exact(
                    self._decode(fields["grant_identity"], seen), ExecutionGrantIdentity
                ),
                kind=self._exact(
                    self._decode(fields["kind"], seen), DispatchOutcomeKind
                ),
                result_reference_identity=self._parse_DispatchOutcomeRecord_result_reference_identity(
                    self._decode(fields["result_reference_identity"], seen)
                ),
                failure_record_identity=self._parse_DispatchOutcomeRecord_failure_record_identity(
                    self._decode(fields["failure_record_identity"], seen)
                ),
                reconciliation_identity_values=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["reconciliation_identity_values"], seen)
                    )
                ),
            )
            return record
        if tag == "DispatchOutcomeRecordIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = DispatchOutcomeRecordIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "DispatchResourceScopeIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = DispatchResourceScopeIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ObligationDisposition":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "obligation_identity",
                    "request_identity",
                    "dispatch_outcome_record_identity",
                    "attempt_record_identity",
                    "kind",
                    "predecessor_disposition_identity",
                    "reconciliation_identity_values",
                ),
            )
            record = ObligationDisposition(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ObligationDispositionIdentity,
                ),
                obligation_identity=self._exact(
                    self._decode(fields["obligation_identity"], seen),
                    ObligationIdentity,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    SimulationExecutionRequestIdentity,
                ),
                dispatch_outcome_record_identity=self._exact(
                    self._decode(fields["dispatch_outcome_record_identity"], seen),
                    DispatchOutcomeRecordIdentity,
                ),
                attempt_record_identity=self._exact(
                    self._decode(fields["attempt_record_identity"], seen),
                    TaskAttemptRecordIdentity,
                ),
                kind=self._exact(
                    self._decode(fields["kind"], seen), ObligationDispositionKind
                ),
                predecessor_disposition_identity=self._parse_ObligationDisposition_predecessor_disposition_identity(
                    self._decode(fields["predecessor_disposition_identity"], seen)
                ),
                reconciliation_identity_values=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["reconciliation_identity_values"], seen)
                    )
                ),
            )
            return record
        if tag == "ObligationDispositionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ObligationDispositionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ObligationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ObligationIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "SimulationDispatchEntry":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "predecessor_revision_identity",
                    "committed_revision_identity",
                    "claimed_reservation_identity",
                    "request_identity",
                    "obligation_identity",
                    "receipt_identity",
                    "outcome_identity",
                ),
            )
            record = SimulationDispatchEntry(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    SimulationDispatchEntryIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                predecessor_revision_identity=self._exact(
                    self._decode(fields["predecessor_revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                committed_revision_identity=self._exact(
                    self._decode(fields["committed_revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                claimed_reservation_identity=self._exact(
                    self._decode(fields["claimed_reservation_identity"], seen),
                    AuthorityReservationOutcomeIdentity,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    SimulationExecutionRequestIdentity,
                ),
                obligation_identity=self._exact(
                    self._decode(fields["obligation_identity"], seen),
                    ObligationIdentity,
                ),
                receipt_identity=self._exact(
                    self._decode(fields["receipt_identity"], seen),
                    SimulationDispatchEntryReceiptIdentity,
                ),
                outcome_identity=self._exact(
                    self._decode(fields["outcome_identity"], seen),
                    SimulationDispatchOutcomeIdentity,
                ),
            )
            return record
        if tag == "SimulationDispatchEntryIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = SimulationDispatchEntryIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "SimulationDispatchEntryReceiptIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = SimulationDispatchEntryReceiptIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "SimulationDispatchObligation":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "workflow_run_revision_identity",
                    "request_identity",
                    "task_instance_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "executor_identity",
                    "grant_identity",
                    "destination_identity",
                    "resource_scope_identities",
                    "creation_idempotency_identity",
                ),
            )
            record = SimulationDispatchObligation(
                identity=self._exact(
                    self._decode(fields["identity"], seen), ObligationIdentity
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                workflow_run_revision_identity=self._exact(
                    self._decode(fields["workflow_run_revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    SimulationExecutionRequestIdentity,
                ),
                task_instance_identity=self._exact(
                    self._decode(fields["task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
                activation_identity=self._exact(
                    self._decode(fields["activation_identity"], seen),
                    TaskActivationIdentity,
                ),
                operation_identity=self._exact(
                    self._decode(fields["operation_identity"], seen), OperationIdentity
                ),
                attempt_identity=self._exact(
                    self._decode(fields["attempt_identity"], seen), AttemptIdentity
                ),
                executor_identity=self._exact(
                    self._decode(fields["executor_identity"], seen),
                    ScientificExecutorIdentity,
                ),
                grant_identity=self._exact(
                    self._decode(fields["grant_identity"], seen), ExecutionGrantIdentity
                ),
                destination_identity=self._exact(
                    self._decode(fields["destination_identity"], seen),
                    DispatchDestinationIdentity,
                ),
                resource_scope_identities=tuple(
                    self._exact(item, DispatchResourceScopeIdentity)
                    for item in self._items(
                        self._decode(fields["resource_scope_identities"], seen)
                    )
                ),
                creation_idempotency_identity=self._exact(
                    self._decode(fields["creation_idempotency_identity"], seen),
                    DispatchCreationIdempotencyIdentity,
                ),
            )
            return record
        if tag == "SimulationDispatchObservationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = SimulationDispatchObservationIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "SimulationDispatchOutcome":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "observation_identity",
                    "request_identity",
                    "workflow_run_identity",
                    "task_instance_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "executor_identity",
                    "obligation_identity",
                    "grant_identity",
                    "kind",
                    "result",
                    "native_output_manifest_identity",
                    "native_output_manifest_entry_identities",
                    "failure",
                    "reconciliation_identity_values",
                ),
            )
            record = SimulationDispatchOutcome(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    SimulationDispatchOutcomeIdentity,
                ),
                observation_identity=self._exact(
                    self._decode(fields["observation_identity"], seen),
                    SimulationDispatchObservationIdentity,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    SimulationExecutionRequestIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                task_instance_identity=self._exact(
                    self._decode(fields["task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
                activation_identity=self._exact(
                    self._decode(fields["activation_identity"], seen),
                    TaskActivationIdentity,
                ),
                operation_identity=self._exact(
                    self._decode(fields["operation_identity"], seen), OperationIdentity
                ),
                attempt_identity=self._exact(
                    self._decode(fields["attempt_identity"], seen), AttemptIdentity
                ),
                executor_identity=self._exact(
                    self._decode(fields["executor_identity"], seen),
                    ScientificExecutorIdentity,
                ),
                obligation_identity=self._exact(
                    self._decode(fields["obligation_identity"], seen),
                    ObligationIdentity,
                ),
                grant_identity=self._exact(
                    self._decode(fields["grant_identity"], seen), ExecutionGrantIdentity
                ),
                kind=self._exact(
                    self._decode(fields["kind"], seen), DispatchOutcomeKind
                ),
                result=self._parse_SimulationDispatchOutcome_result(
                    self._decode(fields["result"], seen)
                ),
                native_output_manifest_identity=self._parse_SimulationDispatchOutcome_native_output_manifest_identity(
                    self._decode(fields["native_output_manifest_identity"], seen)
                ),
                native_output_manifest_entry_identities=tuple(
                    self._exact(item, ArtifactManifestEntryIdentity)
                    for item in self._items(
                        self._decode(
                            fields["native_output_manifest_entry_identities"], seen
                        )
                    )
                ),
                failure=self._parse_SimulationDispatchOutcome_failure(
                    self._decode(fields["failure"], seen)
                ),
                reconciliation_identity_values=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["reconciliation_identity_values"], seen)
                    )
                ),
            )
            return record
        if tag == "SimulationDispatchOutcomeIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = SimulationDispatchOutcomeIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "SimulationExecutionRequestCorrelation":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "task_instance_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "attempt_record_identity",
                    "request_identity",
                    "executor_identity",
                    "obligation_identity",
                    "grant_identity",
                    "authorization_result_identity",
                    "input_result_reference_identities",
                    "input_artifact_entry_identities",
                ),
            )
            record = SimulationExecutionRequestCorrelation(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    SimulationExecutionRequestCorrelationIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                task_instance_identity=self._exact(
                    self._decode(fields["task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
                activation_identity=self._exact(
                    self._decode(fields["activation_identity"], seen),
                    TaskActivationIdentity,
                ),
                operation_identity=self._exact(
                    self._decode(fields["operation_identity"], seen), OperationIdentity
                ),
                attempt_identity=self._exact(
                    self._decode(fields["attempt_identity"], seen), AttemptIdentity
                ),
                attempt_record_identity=self._exact(
                    self._decode(fields["attempt_record_identity"], seen),
                    TaskAttemptRecordIdentity,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    SimulationExecutionRequestIdentity,
                ),
                executor_identity=self._exact(
                    self._decode(fields["executor_identity"], seen),
                    ScientificExecutorIdentity,
                ),
                obligation_identity=self._exact(
                    self._decode(fields["obligation_identity"], seen),
                    ObligationIdentity,
                ),
                grant_identity=self._exact(
                    self._decode(fields["grant_identity"], seen), ExecutionGrantIdentity
                ),
                authorization_result_identity=self._exact(
                    self._decode(fields["authorization_result_identity"], seen),
                    SimulationExecutionAuthorizationResultIdentity,
                ),
                input_result_reference_identities=tuple(
                    self._exact(item, ResultObjectReferenceIdentity)
                    for item in self._items(
                        self._decode(fields["input_result_reference_identities"], seen)
                    )
                ),
                input_artifact_entry_identities=tuple(
                    self._exact(item, ArtifactManifestEntryIdentity)
                    for item in self._items(
                        self._decode(fields["input_artifact_entry_identities"], seen)
                    )
                ),
            )
            return record
        if tag == "SimulationExecutionRequestCorrelationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = SimulationExecutionRequestCorrelationIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "SimulationExecutionRequestIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = SimulationExecutionRequestIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        raise _WorkflowRunWireUnsupported

    def _parse_DispatchOutcomeRecord_result_reference_identity(
        self, value: _RunValue
    ) -> ResultObjectReferenceIdentity | None:
        if type(value) is ResultObjectReferenceIdentity:
            return self._exact(value, ResultObjectReferenceIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_DispatchOutcomeRecord_failure_record_identity(
        self, value: _RunValue
    ) -> TaskFailureRecordIdentity | None:
        if type(value) is TaskFailureRecordIdentity:
            return self._exact(value, TaskFailureRecordIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ObligationDisposition_predecessor_disposition_identity(
        self, value: _RunValue
    ) -> ObligationDispositionIdentity | None:
        if type(value) is ObligationDispositionIdentity:
            return self._exact(value, ObligationDispositionIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_SimulationDispatchOutcome_result(
        self, value: _RunValue
    ) -> ResultObject | None:
        if isinstance(value, ResultObject):
            return self._as_result(value)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_SimulationDispatchOutcome_native_output_manifest_identity(
        self, value: _RunValue
    ) -> ArtifactManifestIdentity | None:
        if type(value) is ArtifactManifestIdentity:
            return self._exact(value, ArtifactManifestIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_SimulationDispatchOutcome_failure(
        self, value: _RunValue
    ) -> TaskInvocationFailure | None:
        if type(value) is TaskInvocationFailure:
            return self._exact(value, TaskInvocationFailure)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")
