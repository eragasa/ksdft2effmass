"""Bounded authority values in the WorkflowRun wire representation."""

from __future__ import annotations

from datetime import datetime

from ksdft2effmass.workflows.artifacts import (
    ArtifactManifestEntryIdentity,
)
from ksdft2effmass.workflows.model import (
    AttemptIdentity,
    OperationIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
)
from ksdft2effmass.workflows.runs.authority import (
    ScientificExecutionAuthorityGrant,
    ScientificExecutionAuthoritySnapshot,
    ScientificExecutionAuthorityVerificationKind,
    ScientificExecutionGrantState,
    SimulationExecutionAuthorizationOutcomeKind,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizationRequest,
    SimulationExecutionAuthorizationResult,
)
from ksdft2effmass.workflows.runs.identities import (
    DispatchDestinationIdentity,
    DispatchResourceScopeIdentity,
    ExecutionGrantIdentity,
    ExecutionGrantRevisionIdentity,
    ObligationIdentity,
    ResultObjectReferenceIdentity,
    ScientificExecutionAuthoritySnapshotIdentity,
    ScientificExecutionAuthorityStateIdentity,
    ScientificExecutorIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestIdentity,
    TaskAttemptRecordIdentity,
)
from ksdft2effmass.workflows.runs.records import (
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeKind,
    ScientificExecutionAuthorityReference,
)

from ...model import (
    WorkflowRunIdentity,
)
from ...runs.identities import (
    AuthorityContextIdentity,
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


class _WorkflowRunAuthorityWireSerializer(_WorkflowRunWireSerializer):
    """Encode and decode the closed authority value family."""

    def _encode_authority(
        self, value: _RunValue, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _ResultJson:
        if type(value) is AuthorityReservationOutcomeKind:
            return self._record(
                "AuthorityReservationOutcomeKind", {"value": value.value}
            )
        if type(value) is ScientificExecutionAuthorityVerificationKind:
            return self._record(
                "ScientificExecutionAuthorityVerificationKind", {"value": value.value}
            )
        if type(value) is ScientificExecutionGrantState:
            return self._record("ScientificExecutionGrantState", {"value": value.value})
        if type(value) is SimulationExecutionAuthorizationOutcomeKind:
            return self._record(
                "SimulationExecutionAuthorizationOutcomeKind", {"value": value.value}
            )
        if type(value) is SimulationExecutionAuthorizationPhase:
            return self._record(
                "SimulationExecutionAuthorizationPhase", {"value": value.value}
            )
        if type(value) is AuthorityContextIdentity:
            return self._record(
                "AuthorityContextIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is AuthorityReservationOutcome:
            return self._record(
                "AuthorityReservationOutcome",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "workflow_run_revision_identity": self._encode(
                        value.workflow_run_revision_identity, seen
                    ),
                    "authority_reference": self._encode(
                        value.authority_reference, seen
                    ),
                    "authorization_result_identity": self._encode(
                        value.authorization_result_identity, seen
                    ),
                    "request_identity": self._encode(value.request_identity, seen),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "attempt_record_identity": self._encode(
                        value.attempt_record_identity, seen
                    ),
                    "obligation_identity": self._encode(
                        value.obligation_identity, seen
                    ),
                    "expected_revision_identity": self._encode(
                        value.expected_revision_identity, seen
                    ),
                    "kind": self._encode(value.kind, seen),
                    "predecessor_reservation_identity": self._encode(
                        value.predecessor_reservation_identity, seen
                    ),
                },
            )
        if type(value) is AuthorityReservationOutcomeIdentity:
            return self._record(
                "AuthorityReservationOutcomeIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ExecutionGrantIdentity:
            return self._record(
                "ExecutionGrantIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ExecutionGrantRevisionIdentity:
            return self._record(
                "ExecutionGrantRevisionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ScientificExecutionAuthorityGrant:
            return self._record(
                "ScientificExecutionAuthorityGrant",
                {
                    "authority_reference": self._encode(
                        value.authority_reference, seen
                    ),
                    "authority_source_identity": self._encode(
                        value.authority_source_identity, seen
                    ),
                    "issuer_identity": self._encode(value.issuer_identity, seen),
                    "request_identity": self._encode(value.request_identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "task_definition_identity": self._encode(
                        value.task_definition_identity, seen
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
                    "destination_identity": self._encode(
                        value.destination_identity, seen
                    ),
                    "resource_scope_identities": self._encode(
                        value.resource_scope_identities, seen
                    ),
                    "input_result_reference_identities": self._encode(
                        value.input_result_reference_identities, seen
                    ),
                    "input_artifact_entry_identities": self._encode(
                        value.input_artifact_entry_identities, seen
                    ),
                    "valid_from": self._encode(value.valid_from, seen),
                    "valid_until": self._encode(value.valid_until, seen),
                    "state": self._encode(value.state, seen),
                    "reserved_obligation_identity": self._encode(
                        value.reserved_obligation_identity, seen
                    ),
                },
            )
        if type(value) is ScientificExecutionAuthorityReference:
            return self._record(
                "ScientificExecutionAuthorityReference",
                {
                    "grant_identity": self._encode(value.grant_identity, seen),
                    "grant_revision_identity": self._encode(
                        value.grant_revision_identity, seen
                    ),
                    "snapshot_identity": self._encode(value.snapshot_identity, seen),
                    "state_identity": self._encode(value.state_identity, seen),
                },
            )
        if type(value) is ScientificExecutionAuthoritySnapshot:
            return self._record(
                "ScientificExecutionAuthoritySnapshot",
                {
                    "identity": self._encode(value.identity, seen),
                    "source_identity": self._encode(value.source_identity, seen),
                    "issuer_identity": self._encode(value.issuer_identity, seen),
                    "trust_configuration_identity": self._encode(
                        value.trust_configuration_identity, seen
                    ),
                    "content_verification_identity": self._encode(
                        value.content_verification_identity, seen
                    ),
                    "authentication_verification_identity": self._encode(
                        value.authentication_verification_identity, seen
                    ),
                    "predecessor_closure_identity": self._encode(
                        value.predecessor_closure_identity, seen
                    ),
                    "revocation_closure_identity": self._encode(
                        value.revocation_closure_identity, seen
                    ),
                    "content_verification": self._encode(
                        value.content_verification, seen
                    ),
                    "authentication_verification": self._encode(
                        value.authentication_verification, seen
                    ),
                    "predecessor_closure": self._encode(
                        value.predecessor_closure, seen
                    ),
                    "revocation_closure": self._encode(value.revocation_closure, seen),
                    "valid_from": self._encode(value.valid_from, seen),
                    "valid_until": self._encode(value.valid_until, seen),
                    "verified_at": self._encode(value.verified_at, seen),
                    "fresh_until": self._encode(value.fresh_until, seen),
                    "resolver_implementation_identity": self._encode(
                        value.resolver_implementation_identity, seen
                    ),
                },
            )
        if type(value) is ScientificExecutionAuthoritySnapshotIdentity:
            return self._record(
                "ScientificExecutionAuthoritySnapshotIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ScientificExecutionAuthorityStateIdentity:
            return self._record(
                "ScientificExecutionAuthorityStateIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ScientificExecutorIdentity:
            return self._record(
                "ScientificExecutorIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is SimulationExecutionAuthorizationRequest:
            return self._record(
                "SimulationExecutionAuthorizationRequest",
                {
                    "result_identity": self._encode(value.result_identity, seen),
                    "phase": self._encode(value.phase, seen),
                    "grant": self._encode(value.grant, seen),
                    "snapshot": self._encode(value.snapshot, seen),
                    "request_identity": self._encode(value.request_identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "task_definition_identity": self._encode(
                        value.task_definition_identity, seen
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
                    "destination_identity": self._encode(
                        value.destination_identity, seen
                    ),
                    "obligation_identity": self._encode(
                        value.obligation_identity, seen
                    ),
                    "resource_scope_identities": self._encode(
                        value.resource_scope_identities, seen
                    ),
                    "input_result_reference_identities": self._encode(
                        value.input_result_reference_identities, seen
                    ),
                    "input_artifact_entry_identities": self._encode(
                        value.input_artifact_entry_identities, seen
                    ),
                    "evaluated_at": self._encode(value.evaluated_at, seen),
                },
            )
        if type(value) is SimulationExecutionAuthorizationResult:
            return self._record(
                "SimulationExecutionAuthorizationResult",
                {
                    "identity": self._encode(value.identity, seen),
                    "request": self._encode(value.request, seen),
                    "kind": self._encode(value.kind, seen),
                    "authorized_grant_state": self._encode(
                        value.authorized_grant_state, seen
                    ),
                    "diagnostics": self._encode(value.diagnostics, seen),
                    "authorizer_implementation_identity": self._encode(
                        value.authorizer_implementation_identity, seen
                    ),
                },
            )
        if type(value) is SimulationExecutionAuthorizationResultIdentity:
            return self._record(
                "SimulationExecutionAuthorizationResultIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        raise _WorkflowRunWireUnsupported

    def _decode_authority(
        self, tag: str, wire: _ResultJson, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _RunValue:
        record: _RunValue
        if tag == "AuthorityReservationOutcomeKind":
            return AuthorityReservationOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ScientificExecutionAuthorityVerificationKind":
            return ScientificExecutionAuthorityVerificationKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ScientificExecutionGrantState":
            return ScientificExecutionGrantState(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "SimulationExecutionAuthorizationOutcomeKind":
            return SimulationExecutionAuthorizationOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "SimulationExecutionAuthorizationPhase":
            return SimulationExecutionAuthorizationPhase(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "AuthorityContextIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = AuthorityContextIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "AuthorityReservationOutcome":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "workflow_run_revision_identity",
                    "authority_reference",
                    "authorization_result_identity",
                    "request_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "attempt_record_identity",
                    "obligation_identity",
                    "expected_revision_identity",
                    "kind",
                    "predecessor_reservation_identity",
                ),
            )
            record = AuthorityReservationOutcome(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    AuthorityReservationOutcomeIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                workflow_run_revision_identity=self._exact(
                    self._decode(fields["workflow_run_revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                authority_reference=self._exact(
                    self._decode(fields["authority_reference"], seen),
                    ScientificExecutionAuthorityReference,
                ),
                authorization_result_identity=self._exact(
                    self._decode(fields["authorization_result_identity"], seen),
                    SimulationExecutionAuthorizationResultIdentity,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    SimulationExecutionRequestIdentity,
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
                obligation_identity=self._exact(
                    self._decode(fields["obligation_identity"], seen),
                    ObligationIdentity,
                ),
                expected_revision_identity=self._exact(
                    self._decode(fields["expected_revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                kind=self._exact(
                    self._decode(fields["kind"], seen), AuthorityReservationOutcomeKind
                ),
                predecessor_reservation_identity=self._parse_AuthorityReservationOutcome_predecessor_reservation_identity(
                    self._decode(fields["predecessor_reservation_identity"], seen)
                ),
            )
            return record
        if tag == "AuthorityReservationOutcomeIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = AuthorityReservationOutcomeIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ExecutionGrantIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ExecutionGrantIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ExecutionGrantRevisionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ExecutionGrantRevisionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ScientificExecutionAuthorityGrant":
            fields = self._fields(
                wire,
                tag,
                (
                    "authority_reference",
                    "authority_source_identity",
                    "issuer_identity",
                    "request_identity",
                    "workflow_run_identity",
                    "task_definition_identity",
                    "task_instance_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "executor_identity",
                    "destination_identity",
                    "resource_scope_identities",
                    "input_result_reference_identities",
                    "input_artifact_entry_identities",
                    "valid_from",
                    "valid_until",
                    "state",
                    "reserved_obligation_identity",
                ),
            )
            record = ScientificExecutionAuthorityGrant(
                authority_reference=self._exact(
                    self._decode(fields["authority_reference"], seen),
                    ScientificExecutionAuthorityReference,
                ),
                authority_source_identity=self._exact(
                    self._decode(fields["authority_source_identity"], seen), str
                ),
                issuer_identity=self._exact(
                    self._decode(fields["issuer_identity"], seen), str
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    SimulationExecutionRequestIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                task_definition_identity=self._exact(
                    self._decode(fields["task_definition_identity"], seen),
                    TaskDefinitionIdentity,
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
                valid_from=self._exact(
                    self._decode(fields["valid_from"], seen), datetime
                ),
                valid_until=self._exact(
                    self._decode(fields["valid_until"], seen), datetime
                ),
                state=self._exact(
                    self._decode(fields["state"], seen), ScientificExecutionGrantState
                ),
                reserved_obligation_identity=self._parse_ScientificExecutionAuthorityGrant_reserved_obligation_identity(
                    self._decode(fields["reserved_obligation_identity"], seen)
                ),
            )
            return record
        if tag == "ScientificExecutionAuthorityReference":
            fields = self._fields(
                wire,
                tag,
                (
                    "grant_identity",
                    "grant_revision_identity",
                    "snapshot_identity",
                    "state_identity",
                ),
            )
            record = ScientificExecutionAuthorityReference(
                grant_identity=self._exact(
                    self._decode(fields["grant_identity"], seen), ExecutionGrantIdentity
                ),
                grant_revision_identity=self._exact(
                    self._decode(fields["grant_revision_identity"], seen),
                    ExecutionGrantRevisionIdentity,
                ),
                snapshot_identity=self._exact(
                    self._decode(fields["snapshot_identity"], seen),
                    ScientificExecutionAuthoritySnapshotIdentity,
                ),
                state_identity=self._exact(
                    self._decode(fields["state_identity"], seen),
                    ScientificExecutionAuthorityStateIdentity,
                ),
            )
            return record
        if tag == "ScientificExecutionAuthoritySnapshot":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "source_identity",
                    "issuer_identity",
                    "trust_configuration_identity",
                    "content_verification_identity",
                    "authentication_verification_identity",
                    "predecessor_closure_identity",
                    "revocation_closure_identity",
                    "content_verification",
                    "authentication_verification",
                    "predecessor_closure",
                    "revocation_closure",
                    "valid_from",
                    "valid_until",
                    "verified_at",
                    "fresh_until",
                    "resolver_implementation_identity",
                ),
            )
            record = ScientificExecutionAuthoritySnapshot(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ScientificExecutionAuthoritySnapshotIdentity,
                ),
                source_identity=self._exact(
                    self._decode(fields["source_identity"], seen), str
                ),
                issuer_identity=self._exact(
                    self._decode(fields["issuer_identity"], seen), str
                ),
                trust_configuration_identity=self._exact(
                    self._decode(fields["trust_configuration_identity"], seen), str
                ),
                content_verification_identity=self._exact(
                    self._decode(fields["content_verification_identity"], seen), str
                ),
                authentication_verification_identity=self._exact(
                    self._decode(fields["authentication_verification_identity"], seen),
                    str,
                ),
                predecessor_closure_identity=self._exact(
                    self._decode(fields["predecessor_closure_identity"], seen), str
                ),
                revocation_closure_identity=self._exact(
                    self._decode(fields["revocation_closure_identity"], seen), str
                ),
                content_verification=self._exact(
                    self._decode(fields["content_verification"], seen),
                    ScientificExecutionAuthorityVerificationKind,
                ),
                authentication_verification=self._exact(
                    self._decode(fields["authentication_verification"], seen),
                    ScientificExecutionAuthorityVerificationKind,
                ),
                predecessor_closure=self._exact(
                    self._decode(fields["predecessor_closure"], seen),
                    ScientificExecutionAuthorityVerificationKind,
                ),
                revocation_closure=self._exact(
                    self._decode(fields["revocation_closure"], seen),
                    ScientificExecutionAuthorityVerificationKind,
                ),
                valid_from=self._exact(
                    self._decode(fields["valid_from"], seen), datetime
                ),
                valid_until=self._exact(
                    self._decode(fields["valid_until"], seen), datetime
                ),
                verified_at=self._exact(
                    self._decode(fields["verified_at"], seen), datetime
                ),
                fresh_until=self._exact(
                    self._decode(fields["fresh_until"], seen), datetime
                ),
                resolver_implementation_identity=self._exact(
                    self._decode(fields["resolver_implementation_identity"], seen), str
                ),
            )
            return record
        if tag == "ScientificExecutionAuthoritySnapshotIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ScientificExecutionAuthoritySnapshotIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ScientificExecutionAuthorityStateIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ScientificExecutionAuthorityStateIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ScientificExecutorIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ScientificExecutorIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "SimulationExecutionAuthorizationRequest":
            fields = self._fields(
                wire,
                tag,
                (
                    "result_identity",
                    "phase",
                    "grant",
                    "snapshot",
                    "request_identity",
                    "workflow_run_identity",
                    "task_definition_identity",
                    "task_instance_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "executor_identity",
                    "destination_identity",
                    "obligation_identity",
                    "resource_scope_identities",
                    "input_result_reference_identities",
                    "input_artifact_entry_identities",
                    "evaluated_at",
                ),
            )
            record = SimulationExecutionAuthorizationRequest(
                result_identity=self._exact(
                    self._decode(fields["result_identity"], seen),
                    SimulationExecutionAuthorizationResultIdentity,
                ),
                phase=self._exact(
                    self._decode(fields["phase"], seen),
                    SimulationExecutionAuthorizationPhase,
                ),
                grant=self._exact(
                    self._decode(fields["grant"], seen),
                    ScientificExecutionAuthorityGrant,
                ),
                snapshot=self._exact(
                    self._decode(fields["snapshot"], seen),
                    ScientificExecutionAuthoritySnapshot,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    SimulationExecutionRequestIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                task_definition_identity=self._exact(
                    self._decode(fields["task_definition_identity"], seen),
                    TaskDefinitionIdentity,
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
                destination_identity=self._exact(
                    self._decode(fields["destination_identity"], seen),
                    DispatchDestinationIdentity,
                ),
                obligation_identity=self._exact(
                    self._decode(fields["obligation_identity"], seen),
                    ObligationIdentity,
                ),
                resource_scope_identities=tuple(
                    self._exact(item, DispatchResourceScopeIdentity)
                    for item in self._items(
                        self._decode(fields["resource_scope_identities"], seen)
                    )
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
                evaluated_at=self._exact(
                    self._decode(fields["evaluated_at"], seen), datetime
                ),
            )
            return record
        if tag == "SimulationExecutionAuthorizationResult":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "request",
                    "kind",
                    "authorized_grant_state",
                    "diagnostics",
                    "authorizer_implementation_identity",
                ),
            )
            record = SimulationExecutionAuthorizationResult(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    SimulationExecutionAuthorizationResultIdentity,
                ),
                request=self._exact(
                    self._decode(fields["request"], seen),
                    SimulationExecutionAuthorizationRequest,
                ),
                kind=self._exact(
                    self._decode(fields["kind"], seen),
                    SimulationExecutionAuthorizationOutcomeKind,
                ),
                authorized_grant_state=self._parse_SimulationExecutionAuthorizationResult_authorized_grant_state(
                    self._decode(fields["authorized_grant_state"], seen)
                ),
                diagnostics=tuple(
                    self._exact(item, str)
                    for item in self._items(self._decode(fields["diagnostics"], seen))
                ),
                authorizer_implementation_identity=self._exact(
                    self._decode(fields["authorizer_implementation_identity"], seen),
                    str,
                ),
            )
            return record
        if tag == "SimulationExecutionAuthorizationResultIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = SimulationExecutionAuthorizationResultIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        raise _WorkflowRunWireUnsupported

    def _parse_AuthorityReservationOutcome_predecessor_reservation_identity(
        self, value: _RunValue
    ) -> AuthorityReservationOutcomeIdentity | None:
        if type(value) is AuthorityReservationOutcomeIdentity:
            return self._exact(value, AuthorityReservationOutcomeIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ScientificExecutionAuthorityGrant_reserved_obligation_identity(
        self, value: _RunValue
    ) -> ObligationIdentity | None:
        if type(value) is ObligationIdentity:
            return self._exact(value, ObligationIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_SimulationExecutionAuthorizationResult_authorized_grant_state(
        self, value: _RunValue
    ) -> ScientificExecutionGrantState | None:
        if type(value) is ScientificExecutionGrantState:
            return self._exact(value, ScientificExecutionGrantState)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")
