"""Bounded history values in the WorkflowRun wire representation."""

from __future__ import annotations

from ksdft2effmass.petrinet.colored.firing import (
    ColoredPetriNetFiringResult,
)
from ksdft2effmass.petrinet.colored.markings import (
    ColoredPetriNetBinding,
    ColoredPetriNetTransitionIdentity,
)
from ksdft2effmass.workflows.artifacts import (
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    ResultArtifactRelationIdentity,
)
from ksdft2effmass.workflows.model import (
    AttemptIdentity,
    OperationIdentity,
    TaskActivationIdentity,
    TaskInstanceIdentity,
)
from ksdft2effmass.workflows.runs.identities import (
    ChildWorkflowCreationIdempotencyIdentity,
    DispatchOutcomeRecordIdentity,
    ExternalProducerAttemptIdentity,
    ExternalResultProducerIdentity,
    HumanResultAuthorIdentity,
    NativeOutputAdmissionIdentity,
    NestedWorkflowInvocationIdentity,
    NestedWorkflowInvocationIntentIdentity,
    NestedWorkflowMembershipIdentity,
    NestedWorkflowObservationIdentity,
    ResultDependencyIdentity,
    ResultObjectReferenceIdentity,
    ResultProducerEvidenceIdentity,
    ResultProductionRecordIdentity,
    RetainedResultSourceIdentity,
    SimulationDispatchObservationIdentity,
    TaskAttemptRecordIdentity,
    TaskInvocationOutcomeIdentity,
    WorkflowDefinitionReferenceIdentity,
    WorkflowRunReplayResultIdentity,
    WorkflowRuntimeBundleIdentity,
    WorkflowTransitionSequenceIdentity,
)
from ksdft2effmass.workflows.runs.records import (
    ExternalResultProducer,
    HumanAuthoredResultProducer,
    ImportedRetainedResultProducer,
    NativeOutputAdmission,
    NestedWorkflowInvocation,
    NestedWorkflowInvocationIntent,
    NestedWorkflowInvocationKind,
    NestedWorkflowMembership,
    NestedWorkflowTerminalObservation,
    NestedWorkflowTerminalObservationKind,
    RepresentedTaskResultProducer,
    ResultDependency,
    ResultObjectReference,
    ResultProductionRecord,
    ScientificDecisionOption,
    ScientificDecisionRequest,
    ScientificDecisionWorkflowTransitionRecord,
    UnknownLegacyResultProducer,
)

from ...model import (
    ResultObjectIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ...runs.identities import (
    AuthorityContextIdentity,
    ResponseSourceIdentity,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectTypeIdentity,
    ResultProducerProvenanceIdentity,
    ScientificDecisionOptionIdentity,
    ScientificDecisionRecorderIdentity,
    ScientificDecisionRequestIdentity,
    ScientificDecisionTransitionRecordIdentity,
    WorkflowRunRevisionIdentity,
)
from ...runs.records import (
    RepresentedScientificDecisionIngressProducer,
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


class _WorkflowRunHistoryWireSerializer(_WorkflowRunWireSerializer):
    """Encode and decode the closed history value family."""

    def _encode_history(
        self, value: _RunValue, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _ResultJson:
        if type(value) is NestedWorkflowInvocationKind:
            return self._record("NestedWorkflowInvocationKind", {"value": value.value})
        if type(value) is ArtifactManifestEntryIdentity:
            return self._record(
                "ArtifactManifestEntryIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ArtifactManifestIdentity:
            return self._record(
                "ArtifactManifestIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ChildWorkflowCreationIdempotencyIdentity:
            return self._record(
                "ChildWorkflowCreationIdempotencyIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ExternalProducerAttemptIdentity:
            return self._record(
                "ExternalProducerAttemptIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ExternalResultProducer:
            return self._record(
                "ExternalResultProducer",
                {
                    "identity": self._encode(value.identity, seen),
                    "external_producer_identity": self._encode(
                        value.external_producer_identity, seen
                    ),
                    "producer_attempt_identity": self._encode(
                        value.producer_attempt_identity, seen
                    ),
                    "evidence_identities": self._encode(
                        value.evidence_identities, seen
                    ),
                    "limitations": self._encode(value.limitations, seen),
                },
            )
        if type(value) is ExternalResultProducerIdentity:
            return self._record(
                "ExternalResultProducerIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is HumanAuthoredResultProducer:
            return self._record(
                "HumanAuthoredResultProducer",
                {
                    "identity": self._encode(value.identity, seen),
                    "author_identity": self._encode(value.author_identity, seen),
                    "source_identity": self._encode(value.source_identity, seen),
                    "evidence_identities": self._encode(
                        value.evidence_identities, seen
                    ),
                    "limitations": self._encode(value.limitations, seen),
                },
            )
        if type(value) is HumanResultAuthorIdentity:
            return self._record(
                "HumanResultAuthorIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ImportedRetainedResultProducer:
            return self._record(
                "ImportedRetainedResultProducer",
                {
                    "identity": self._encode(value.identity, seen),
                    "source_identity": self._encode(value.source_identity, seen),
                    "evidence_identities": self._encode(
                        value.evidence_identities, seen
                    ),
                    "limitations": self._encode(value.limitations, seen),
                },
            )
        if type(value) is NativeOutputAdmission:
            return self._record(
                "NativeOutputAdmission",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "dispatch_outcome_record_identity": self._encode(
                        value.dispatch_outcome_record_identity, seen
                    ),
                    "dispatch_envelope_identity": self._encode(
                        value.dispatch_envelope_identity, seen
                    ),
                    "production_record_identity": self._encode(
                        value.production_record_identity, seen
                    ),
                    "result_reference_identity": self._encode(
                        value.result_reference_identity, seen
                    ),
                    "manifest_identity": self._encode(value.manifest_identity, seen),
                    "manifest_entry_identities": self._encode(
                        value.manifest_entry_identities, seen
                    ),
                },
            )
        if type(value) is NativeOutputAdmissionIdentity:
            return self._record(
                "NativeOutputAdmissionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is NestedWorkflowInvocationIntentIdentity:
            return self._record(
                "NestedWorkflowInvocationIntentIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is NestedWorkflowTerminalObservationKind:
            return self._record(
                "NestedWorkflowTerminalObservationKind",
                {
                    "value": value.value,
                },
            )
        if type(value) is NestedWorkflowInvocationIntent:
            return self._record(
                "NestedWorkflowInvocationIntent",
                {
                    "identity": self._encode(value.identity, seen),
                    "parent_workflow_run_identity": self._encode(
                        value.parent_workflow_run_identity, seen
                    ),
                    "parent_revision_identity": self._encode(
                        value.parent_revision_identity, seen
                    ),
                    "parent_task_instance_identity": self._encode(
                        value.parent_task_instance_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "started_attempt_record_identity": self._encode(
                        value.started_attempt_record_identity, seen
                    ),
                    "child_workflow_identity": self._encode(
                        value.child_workflow_identity, seen
                    ),
                    "child_workflow_run_identity": self._encode(
                        value.child_workflow_run_identity, seen
                    ),
                    "input_result_reference_identities": self._encode(
                        value.input_result_reference_identities, seen
                    ),
                    "child_creation_idempotency_identity": self._encode(
                        value.child_creation_idempotency_identity, seen
                    ),
                },
            )
        if type(value) is NestedWorkflowTerminalObservation:
            return self._record(
                "NestedWorkflowTerminalObservation",
                {
                    "identity": self._encode(value.identity, seen),
                    "intent_identity": self._encode(value.intent_identity, seen),
                    "parent_workflow_run_identity": self._encode(
                        value.parent_workflow_run_identity, seen
                    ),
                    "parent_revision_identity": self._encode(
                        value.parent_revision_identity, seen
                    ),
                    "terminal_attempt_record_identity": self._encode(
                        value.terminal_attempt_record_identity, seen
                    ),
                    "outcome_identity": self._encode(value.outcome_identity, seen),
                    "kind": self._encode(value.kind, seen),
                    "terminal_child_revision_identity": self._encode(
                        value.terminal_child_revision_identity, seen
                    ),
                    "replay_equal_child_result_identity": self._encode(
                        value.replay_equal_child_result_identity, seen
                    ),
                    "exported_result_reference_identities": self._encode(
                        value.exported_result_reference_identities, seen
                    ),
                    "export_admission_dependency_identities": self._encode(
                        value.export_admission_dependency_identities, seen
                    ),
                    "failure_record_identity": self._encode(
                        value.failure_record_identity, seen
                    ),
                    "reconciliation_identity_values": self._encode(
                        value.reconciliation_identity_values, seen
                    ),
                },
            )
        if type(value) is NestedWorkflowInvocation:
            return self._record(
                "NestedWorkflowInvocation",
                {
                    "identity": self._encode(value.identity, seen),
                    "parent_workflow_run_identity": self._encode(
                        value.parent_workflow_run_identity, seen
                    ),
                    "parent_revision_identity": self._encode(
                        value.parent_revision_identity, seen
                    ),
                    "parent_task_instance_identity": self._encode(
                        value.parent_task_instance_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "attempt_record_identity": self._encode(
                        value.attempt_record_identity, seen
                    ),
                    "child_workflow_identity": self._encode(
                        value.child_workflow_identity, seen
                    ),
                    "child_workflow_run_identity": self._encode(
                        value.child_workflow_run_identity, seen
                    ),
                    "input_result_reference_identities": self._encode(
                        value.input_result_reference_identities, seen
                    ),
                    "child_creation_idempotency_identity": self._encode(
                        value.child_creation_idempotency_identity, seen
                    ),
                    "kind": self._encode(value.kind, seen),
                    "terminal_observation_identity": self._encode(
                        value.terminal_observation_identity, seen
                    ),
                    "terminal_child_revision_identity": self._encode(
                        value.terminal_child_revision_identity, seen
                    ),
                    "replay_equal_child_result_identity": self._encode(
                        value.replay_equal_child_result_identity, seen
                    ),
                    "exported_result_reference_identities": self._encode(
                        value.exported_result_reference_identities, seen
                    ),
                    "export_admission_dependency_identities": self._encode(
                        value.export_admission_dependency_identities, seen
                    ),
                    "failure_record_identity": self._encode(
                        value.failure_record_identity, seen
                    ),
                    "reconciliation_identity_values": self._encode(
                        value.reconciliation_identity_values, seen
                    ),
                },
            )
        if type(value) is NestedWorkflowInvocationIdentity:
            return self._record(
                "NestedWorkflowInvocationIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is NestedWorkflowMembership:
            return self._record(
                "NestedWorkflowMembership",
                {
                    "identity": self._encode(value.identity, seen),
                    "parent_workflow_run_identity": self._encode(
                        value.parent_workflow_run_identity, seen
                    ),
                    "parent_revision_identity": self._encode(
                        value.parent_revision_identity, seen
                    ),
                    "parent_task_instance_identity": self._encode(
                        value.parent_task_instance_identity, seen
                    ),
                    "child_workflow_identity": self._encode(
                        value.child_workflow_identity, seen
                    ),
                    "child_workflow_run_identity": self._encode(
                        value.child_workflow_run_identity, seen
                    ),
                },
            )
        if type(value) is NestedWorkflowMembershipIdentity:
            return self._record(
                "NestedWorkflowMembershipIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is NestedWorkflowObservationIdentity:
            return self._record(
                "NestedWorkflowObservationIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is RepresentedScientificDecisionIngressProducer:
            return self._record(
                "RepresentedScientificDecisionIngressProducer",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "request_identity": self._encode(value.request_identity, seen),
                    "transition_record_identity": self._encode(
                        value.transition_record_identity, seen
                    ),
                    "recorder_identity": self._encode(value.recorder_identity, seen),
                    "response_source_identity": self._encode(
                        value.response_source_identity, seen
                    ),
                    "authority_context_identity": self._encode(
                        value.authority_context_identity, seen
                    ),
                    "resolution_identity": self._encode(
                        value.resolution_identity, seen
                    ),
                },
            )
        if type(value) is RepresentedTaskResultProducer:
            return self._record(
                "RepresentedTaskResultProducer",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
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
                    "terminal_attempt_record_identity": self._encode(
                        value.terminal_attempt_record_identity, seen
                    ),
                    "outcome_identity": self._encode(value.outcome_identity, seen),
                    "production_identity": self._encode(
                        value.production_identity, seen
                    ),
                },
            )
        if type(value) is ResponseSourceIdentity:
            return self._record(
                "ResponseSourceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ResultArtifactRelationIdentity:
            return self._record(
                "ResultArtifactRelationIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ResultDependency:
            return self._record(
                "ResultDependency",
                {
                    "identity": self._encode(value.identity, seen),
                    "result_reference_identity": self._encode(
                        value.result_reference_identity, seen
                    ),
                    "producer_workflow_run_identity": self._encode(
                        value.producer_workflow_run_identity, seen
                    ),
                    "consumer_workflow_run_identity": self._encode(
                        value.consumer_workflow_run_identity, seen
                    ),
                    "consumer_task_instance_identity": self._encode(
                        value.consumer_task_instance_identity, seen
                    ),
                    "consumer_activation_identity": self._encode(
                        value.consumer_activation_identity, seen
                    ),
                    "input_name": self._encode(value.input_name, seen),
                },
            )
        if type(value) is ResultDependencyIdentity:
            return self._record(
                "ResultDependencyIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ResultObjectContentIdentity:
            return self._record(
                "ResultObjectContentIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ResultObjectDomainIdentity:
            return self._record(
                "ResultObjectDomainIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ResultObjectIdentity:
            return self._record(
                "ResultObjectIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ResultObjectReference:
            self._check_reference(value, seen)
            return self._record(
                "ResultObjectReference",
                {
                    "identity": self._encode(value.identity, seen),
                    "result": self._encode(value.result, seen),
                    "concrete_type_identity": self._encode(
                        value.concrete_type_identity, seen
                    ),
                    "owning_domain_identity": self._encode(
                        value.owning_domain_identity, seen
                    ),
                    "content_identity": self._encode(value.content_identity, seen),
                    "producer_provenance": self._encode(
                        value.producer_provenance, seen
                    ),
                },
            )
        if type(value) is ResultObjectReferenceIdentity:
            return self._record(
                "ResultObjectReferenceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ResultObjectTypeIdentity:
            return self._record(
                "ResultObjectTypeIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ResultProducerEvidenceIdentity:
            return self._record(
                "ResultProducerEvidenceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ResultProducerProvenanceIdentity:
            return self._record(
                "ResultProducerProvenanceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ResultProductionRecord:
            return self._record(
                "ResultProductionRecord",
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
                    "terminal_attempt_record_identity": self._encode(
                        value.terminal_attempt_record_identity, seen
                    ),
                    "outcome_identity": self._encode(value.outcome_identity, seen),
                    "result_reference_identity": self._encode(
                        value.result_reference_identity, seen
                    ),
                    "result_artifact_relation_identities": self._encode(
                        value.result_artifact_relation_identities, seen
                    ),
                    "external_output_binding": self._encode(
                        value.external_output_binding, seen
                    ),
                },
            )
        if type(value) is ResultProductionRecordIdentity:
            return self._record(
                "ResultProductionRecordIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is RetainedResultSourceIdentity:
            return self._record(
                "RetainedResultSourceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ScientificDecisionOption:
            return self._record(
                "ScientificDecisionOption",
                {
                    "identity": self._encode(value.identity, seen),
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ScientificDecisionOptionIdentity:
            return self._record(
                "ScientificDecisionOptionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ScientificDecisionRecorderIdentity:
            return self._record(
                "ScientificDecisionRecorderIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ScientificDecisionRequest:
            return self._record(
                "ScientificDecisionRequest",
                {
                    "identity": self._encode(value.identity, seen),
                    "question": self._encode(value.question, seen),
                    "options": self._encode(value.options, seen),
                    "declared_scope": self._encode(value.declared_scope, seen),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "affected_task_instance_identity": self._encode(
                        value.affected_task_instance_identity, seen
                    ),
                    "affected_transition_identity": self._encode(
                        value.affected_transition_identity, seen
                    ),
                    "required_response_source_identity": self._encode(
                        value.required_response_source_identity, seen
                    ),
                    "required_authority_context_identity": self._encode(
                        value.required_authority_context_identity, seen
                    ),
                    "definition_identity": self._encode(
                        value.definition_identity, seen
                    ),
                    "definition_version": self._encode(value.definition_version, seen),
                },
            )
        if type(value) is ScientificDecisionRequestIdentity:
            return self._record(
                "ScientificDecisionRequestIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ScientificDecisionTransitionRecordIdentity:
            return self._record(
                "ScientificDecisionTransitionRecordIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ScientificDecisionWorkflowTransitionRecord:
            return self._record(
                "ScientificDecisionWorkflowTransitionRecord",
                {
                    "identity": self._encode(value.identity, seen),
                    "sequence_identity": self._encode(value.sequence_identity, seen),
                    "sequence_index": self._encode(value.sequence_index, seen),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "definition_reference_identity": self._encode(
                        value.definition_reference_identity, seen
                    ),
                    "runtime_bundle_identity": self._encode(
                        value.runtime_bundle_identity, seen
                    ),
                    "request_identity": self._encode(value.request_identity, seen),
                    "resolution_identity": self._encode(
                        value.resolution_identity, seen
                    ),
                    "producer_provenance_identity": self._encode(
                        value.producer_provenance_identity, seen
                    ),
                    "firing_result": self._encode(value.firing_result, seen),
                },
            )
        if type(value) is UnknownLegacyResultProducer:
            return self._record(
                "UnknownLegacyResultProducer",
                {
                    "identity": self._encode(value.identity, seen),
                    "source_identity": self._encode(value.source_identity, seen),
                    "evidence_identities": self._encode(
                        value.evidence_identities, seen
                    ),
                    "limitations": self._encode(value.limitations, seen),
                },
            )
        raise _WorkflowRunWireUnsupported

    def _decode_history(
        self, tag: str, wire: _ResultJson, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _RunValue:
        record: _RunValue
        if tag == "NestedWorkflowInvocationKind":
            return NestedWorkflowInvocationKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ArtifactManifestEntryIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ArtifactManifestEntryIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ArtifactManifestIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ArtifactManifestIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ChildWorkflowCreationIdempotencyIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ChildWorkflowCreationIdempotencyIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ExternalProducerAttemptIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ExternalProducerAttemptIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ExternalResultProducer":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "external_producer_identity",
                    "producer_attempt_identity",
                    "evidence_identities",
                    "limitations",
                ),
            )
            record = ExternalResultProducer(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ResultProducerProvenanceIdentity,
                ),
                external_producer_identity=self._exact(
                    self._decode(fields["external_producer_identity"], seen),
                    ExternalResultProducerIdentity,
                ),
                producer_attempt_identity=self._exact(
                    self._decode(fields["producer_attempt_identity"], seen),
                    ExternalProducerAttemptIdentity,
                ),
                evidence_identities=tuple(
                    self._exact(item, ResultProducerEvidenceIdentity)
                    for item in self._items(
                        self._decode(fields["evidence_identities"], seen)
                    )
                ),
                limitations=tuple(
                    self._exact(item, str)
                    for item in self._items(self._decode(fields["limitations"], seen))
                ),
            )
            return record
        if tag == "ExternalResultProducerIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ExternalResultProducerIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "HumanAuthoredResultProducer":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "author_identity",
                    "source_identity",
                    "evidence_identities",
                    "limitations",
                ),
            )
            record = HumanAuthoredResultProducer(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ResultProducerProvenanceIdentity,
                ),
                author_identity=self._exact(
                    self._decode(fields["author_identity"], seen),
                    HumanResultAuthorIdentity,
                ),
                source_identity=self._exact(
                    self._decode(fields["source_identity"], seen),
                    RetainedResultSourceIdentity,
                ),
                evidence_identities=tuple(
                    self._exact(item, ResultProducerEvidenceIdentity)
                    for item in self._items(
                        self._decode(fields["evidence_identities"], seen)
                    )
                ),
                limitations=tuple(
                    self._exact(item, str)
                    for item in self._items(self._decode(fields["limitations"], seen))
                ),
            )
            return record
        if tag == "HumanResultAuthorIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = HumanResultAuthorIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ImportedRetainedResultProducer":
            fields = self._fields(
                wire,
                tag,
                ("identity", "source_identity", "evidence_identities", "limitations"),
            )
            record = ImportedRetainedResultProducer(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ResultProducerProvenanceIdentity,
                ),
                source_identity=self._exact(
                    self._decode(fields["source_identity"], seen),
                    RetainedResultSourceIdentity,
                ),
                evidence_identities=tuple(
                    self._exact(item, ResultProducerEvidenceIdentity)
                    for item in self._items(
                        self._decode(fields["evidence_identities"], seen)
                    )
                ),
                limitations=tuple(
                    self._exact(item, str)
                    for item in self._items(self._decode(fields["limitations"], seen))
                ),
            )
            return record
        if tag == "NativeOutputAdmission":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "dispatch_outcome_record_identity",
                    "dispatch_envelope_identity",
                    "production_record_identity",
                    "result_reference_identity",
                    "manifest_identity",
                    "manifest_entry_identities",
                ),
            )
            record = NativeOutputAdmission(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    NativeOutputAdmissionIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                dispatch_outcome_record_identity=self._exact(
                    self._decode(fields["dispatch_outcome_record_identity"], seen),
                    DispatchOutcomeRecordIdentity,
                ),
                dispatch_envelope_identity=self._exact(
                    self._decode(fields["dispatch_envelope_identity"], seen),
                    SimulationDispatchObservationIdentity,
                ),
                production_record_identity=self._exact(
                    self._decode(fields["production_record_identity"], seen),
                    ResultProductionRecordIdentity,
                ),
                result_reference_identity=self._exact(
                    self._decode(fields["result_reference_identity"], seen),
                    ResultObjectReferenceIdentity,
                ),
                manifest_identity=self._exact(
                    self._decode(fields["manifest_identity"], seen),
                    ArtifactManifestIdentity,
                ),
                manifest_entry_identities=tuple(
                    self._exact(item, ArtifactManifestEntryIdentity)
                    for item in self._items(
                        self._decode(fields["manifest_entry_identities"], seen)
                    )
                ),
            )
            return record
        if tag == "NativeOutputAdmissionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = NativeOutputAdmissionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "NestedWorkflowInvocationIntentIdentity":
            fields = self._fields(wire, tag, ("value",))
            return NestedWorkflowInvocationIntentIdentity(
                self._exact(self._decode(fields["value"], seen), str)
            )
        if tag == "NestedWorkflowTerminalObservationKind":
            fields = self._fields(wire, tag, ("value",))
            return NestedWorkflowTerminalObservationKind(self._string(fields["value"]))
        if tag == "NestedWorkflowInvocationIntent":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "parent_workflow_run_identity",
                    "parent_revision_identity",
                    "parent_task_instance_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "started_attempt_record_identity",
                    "child_workflow_identity",
                    "child_workflow_run_identity",
                    "input_result_reference_identities",
                    "child_creation_idempotency_identity",
                ),
            )
            return NestedWorkflowInvocationIntent(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    NestedWorkflowInvocationIntentIdentity,
                ),
                parent_workflow_run_identity=self._exact(
                    self._decode(fields["parent_workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                parent_revision_identity=self._exact(
                    self._decode(fields["parent_revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                parent_task_instance_identity=self._exact(
                    self._decode(fields["parent_task_instance_identity"], seen),
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
                started_attempt_record_identity=self._exact(
                    self._decode(fields["started_attempt_record_identity"], seen),
                    TaskAttemptRecordIdentity,
                ),
                child_workflow_identity=self._exact(
                    self._decode(fields["child_workflow_identity"], seen),
                    WorkflowIdentity,
                ),
                child_workflow_run_identity=self._exact(
                    self._decode(fields["child_workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                input_result_reference_identities=tuple(
                    self._exact(item, ResultObjectReferenceIdentity)
                    for item in self._items(
                        self._decode(fields["input_result_reference_identities"], seen)
                    )
                ),
                child_creation_idempotency_identity=self._exact(
                    self._decode(fields["child_creation_idempotency_identity"], seen),
                    ChildWorkflowCreationIdempotencyIdentity,
                ),
            )
        if tag == "NestedWorkflowTerminalObservation":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "intent_identity",
                    "parent_workflow_run_identity",
                    "parent_revision_identity",
                    "terminal_attempt_record_identity",
                    "outcome_identity",
                    "kind",
                    "terminal_child_revision_identity",
                    "replay_equal_child_result_identity",
                    "exported_result_reference_identities",
                    "export_admission_dependency_identities",
                    "failure_record_identity",
                    "reconciliation_identity_values",
                ),
            )
            intent_identity = self._decode(fields["intent_identity"], seen)
            if not isinstance(
                intent_identity,
                (
                    NestedWorkflowInvocationIntentIdentity,
                    NestedWorkflowInvocationIdentity,
                ),
            ):
                raise TypeError("wrong nominal intent reference")
            return NestedWorkflowTerminalObservation(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    NestedWorkflowObservationIdentity,
                ),
                intent_identity=intent_identity,
                parent_workflow_run_identity=self._exact(
                    self._decode(fields["parent_workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                parent_revision_identity=self._exact(
                    self._decode(fields["parent_revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                terminal_attempt_record_identity=self._exact(
                    self._decode(fields["terminal_attempt_record_identity"], seen),
                    TaskAttemptRecordIdentity,
                ),
                outcome_identity=self._exact(
                    self._decode(fields["outcome_identity"], seen),
                    TaskInvocationOutcomeIdentity,
                ),
                kind=self._exact(
                    self._decode(fields["kind"], seen),
                    NestedWorkflowTerminalObservationKind,
                ),
                terminal_child_revision_identity=self._parse_NestedWorkflowInvocation_terminal_child_revision_identity(
                    self._decode(fields["terminal_child_revision_identity"], seen)
                ),
                replay_equal_child_result_identity=self._parse_NestedWorkflowInvocation_replay_equal_child_result_identity(
                    self._decode(fields["replay_equal_child_result_identity"], seen)
                ),
                exported_result_reference_identities=tuple(
                    self._exact(item, ResultObjectReferenceIdentity)
                    for item in self._items(
                        self._decode(
                            fields["exported_result_reference_identities"], seen
                        )
                    )
                ),
                export_admission_dependency_identities=tuple(
                    self._exact(item, ResultDependencyIdentity)
                    for item in self._items(
                        self._decode(
                            fields["export_admission_dependency_identities"], seen
                        )
                    )
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
        if tag == "NestedWorkflowInvocation":
            fields = self._fields(
                wire,
                tag,
                (
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
                ),
            )
            record = NestedWorkflowInvocation(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    NestedWorkflowInvocationIdentity,
                ),
                parent_workflow_run_identity=self._exact(
                    self._decode(fields["parent_workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                parent_revision_identity=self._exact(
                    self._decode(fields["parent_revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                parent_task_instance_identity=self._exact(
                    self._decode(fields["parent_task_instance_identity"], seen),
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
                child_workflow_identity=self._exact(
                    self._decode(fields["child_workflow_identity"], seen),
                    WorkflowIdentity,
                ),
                child_workflow_run_identity=self._exact(
                    self._decode(fields["child_workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                input_result_reference_identities=tuple(
                    self._exact(item, ResultObjectReferenceIdentity)
                    for item in self._items(
                        self._decode(fields["input_result_reference_identities"], seen)
                    )
                ),
                child_creation_idempotency_identity=self._exact(
                    self._decode(fields["child_creation_idempotency_identity"], seen),
                    ChildWorkflowCreationIdempotencyIdentity,
                ),
                kind=self._exact(
                    self._decode(fields["kind"], seen), NestedWorkflowInvocationKind
                ),
                terminal_observation_identity=self._parse_NestedWorkflowInvocation_terminal_observation_identity(
                    self._decode(fields["terminal_observation_identity"], seen)
                ),
                terminal_child_revision_identity=self._parse_NestedWorkflowInvocation_terminal_child_revision_identity(
                    self._decode(fields["terminal_child_revision_identity"], seen)
                ),
                replay_equal_child_result_identity=self._parse_NestedWorkflowInvocation_replay_equal_child_result_identity(
                    self._decode(fields["replay_equal_child_result_identity"], seen)
                ),
                exported_result_reference_identities=tuple(
                    self._exact(item, ResultObjectReferenceIdentity)
                    for item in self._items(
                        self._decode(
                            fields["exported_result_reference_identities"], seen
                        )
                    )
                ),
                export_admission_dependency_identities=tuple(
                    self._exact(item, ResultDependencyIdentity)
                    for item in self._items(
                        self._decode(
                            fields["export_admission_dependency_identities"], seen
                        )
                    )
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
        if tag == "NestedWorkflowInvocationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = NestedWorkflowInvocationIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "NestedWorkflowMembership":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "parent_workflow_run_identity",
                    "parent_revision_identity",
                    "parent_task_instance_identity",
                    "child_workflow_identity",
                    "child_workflow_run_identity",
                ),
            )
            record = NestedWorkflowMembership(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    NestedWorkflowMembershipIdentity,
                ),
                parent_workflow_run_identity=self._exact(
                    self._decode(fields["parent_workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                parent_revision_identity=self._exact(
                    self._decode(fields["parent_revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                parent_task_instance_identity=self._exact(
                    self._decode(fields["parent_task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
                child_workflow_identity=self._exact(
                    self._decode(fields["child_workflow_identity"], seen),
                    WorkflowIdentity,
                ),
                child_workflow_run_identity=self._exact(
                    self._decode(fields["child_workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
            )
            return record
        if tag == "NestedWorkflowMembershipIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = NestedWorkflowMembershipIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "NestedWorkflowObservationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = NestedWorkflowObservationIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "RepresentedScientificDecisionIngressProducer":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_identity",
                    "workflow_run_identity",
                    "request_identity",
                    "transition_record_identity",
                    "recorder_identity",
                    "response_source_identity",
                    "authority_context_identity",
                    "resolution_identity",
                ),
            )
            record = RepresentedScientificDecisionIngressProducer(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ResultProducerProvenanceIdentity,
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    ScientificDecisionRequestIdentity,
                ),
                transition_record_identity=self._exact(
                    self._decode(fields["transition_record_identity"], seen),
                    ScientificDecisionTransitionRecordIdentity,
                ),
                recorder_identity=self._exact(
                    self._decode(fields["recorder_identity"], seen),
                    ScientificDecisionRecorderIdentity,
                ),
                response_source_identity=self._exact(
                    self._decode(fields["response_source_identity"], seen),
                    ResponseSourceIdentity,
                ),
                authority_context_identity=self._exact(
                    self._decode(fields["authority_context_identity"], seen),
                    AuthorityContextIdentity,
                ),
                resolution_identity=self._exact(
                    self._decode(fields["resolution_identity"], seen),
                    ResultObjectIdentity,
                ),
            )
            return record
        if tag == "RepresentedTaskResultProducer":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_identity",
                    "workflow_run_identity",
                    "task_instance_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "terminal_attempt_record_identity",
                    "outcome_identity",
                    "production_identity",
                ),
            )
            record = RepresentedTaskResultProducer(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ResultProducerProvenanceIdentity,
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
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
                terminal_attempt_record_identity=self._exact(
                    self._decode(fields["terminal_attempt_record_identity"], seen),
                    TaskAttemptRecordIdentity,
                ),
                outcome_identity=self._exact(
                    self._decode(fields["outcome_identity"], seen),
                    TaskInvocationOutcomeIdentity,
                ),
                production_identity=self._exact(
                    self._decode(fields["production_identity"], seen),
                    ResultProductionRecordIdentity,
                ),
            )
            return record
        if tag == "ResponseSourceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResponseSourceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ResultArtifactRelationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResultArtifactRelationIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ResultDependency":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "result_reference_identity",
                    "producer_workflow_run_identity",
                    "consumer_workflow_run_identity",
                    "consumer_task_instance_identity",
                    "consumer_activation_identity",
                    "input_name",
                ),
            )
            record = ResultDependency(
                identity=self._exact(
                    self._decode(fields["identity"], seen), ResultDependencyIdentity
                ),
                result_reference_identity=self._exact(
                    self._decode(fields["result_reference_identity"], seen),
                    ResultObjectReferenceIdentity,
                ),
                producer_workflow_run_identity=self._parse_ResultDependency_producer_workflow_run_identity(
                    self._decode(fields["producer_workflow_run_identity"], seen)
                ),
                consumer_workflow_run_identity=self._exact(
                    self._decode(fields["consumer_workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                consumer_task_instance_identity=self._exact(
                    self._decode(fields["consumer_task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
                consumer_activation_identity=self._parse_ResultDependency_consumer_activation_identity(
                    self._decode(fields["consumer_activation_identity"], seen)
                ),
                input_name=self._exact(self._decode(fields["input_name"], seen), str),
            )
            return record
        if tag == "ResultDependencyIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResultDependencyIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ResultObjectContentIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResultObjectContentIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ResultObjectDomainIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResultObjectDomainIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ResultObjectIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResultObjectIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ResultObjectReference":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "result",
                    "concrete_type_identity",
                    "owning_domain_identity",
                    "content_identity",
                    "producer_provenance",
                ),
            )
            record = ResultObjectReference(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ResultObjectReferenceIdentity,
                ),
                result=self._as_result(self._decode(fields["result"], seen)),
                concrete_type_identity=self._exact(
                    self._decode(fields["concrete_type_identity"], seen),
                    ResultObjectTypeIdentity,
                ),
                owning_domain_identity=self._exact(
                    self._decode(fields["owning_domain_identity"], seen),
                    ResultObjectDomainIdentity,
                ),
                content_identity=self._exact(
                    self._decode(fields["content_identity"], seen),
                    ResultObjectContentIdentity,
                ),
                producer_provenance=self._parse_ResultObjectReference_producer_provenance(
                    self._decode(fields["producer_provenance"], seen)
                ),
            )
            self._check_reference(record, seen)
            return record
        if tag == "ResultObjectReferenceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResultObjectReferenceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ResultObjectTypeIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResultObjectTypeIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ResultProducerEvidenceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResultProducerEvidenceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ResultProducerProvenanceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResultProducerProvenanceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ResultProductionRecord":
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
                    "terminal_attempt_record_identity",
                    "outcome_identity",
                    "result_reference_identity",
                    "result_artifact_relation_identities",
                    "external_output_binding",
                ),
            )
            record = ResultProductionRecord(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ResultProductionRecordIdentity,
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
                terminal_attempt_record_identity=self._exact(
                    self._decode(fields["terminal_attempt_record_identity"], seen),
                    TaskAttemptRecordIdentity,
                ),
                outcome_identity=self._exact(
                    self._decode(fields["outcome_identity"], seen),
                    TaskInvocationOutcomeIdentity,
                ),
                result_reference_identity=self._exact(
                    self._decode(fields["result_reference_identity"], seen),
                    ResultObjectReferenceIdentity,
                ),
                result_artifact_relation_identities=tuple(
                    self._exact(item, ResultArtifactRelationIdentity)
                    for item in self._items(
                        self._decode(
                            fields["result_artifact_relation_identities"], seen
                        )
                    )
                ),
                external_output_binding=self._exact(
                    self._decode(fields["external_output_binding"], seen),
                    ColoredPetriNetBinding,
                ),
            )
            return record
        if tag == "ResultProductionRecordIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ResultProductionRecordIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "RetainedResultSourceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = RetainedResultSourceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ScientificDecisionOption":
            fields = self._fields(wire, tag, ("identity", "value"))
            record = ScientificDecisionOption(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ScientificDecisionOptionIdentity,
                ),
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ScientificDecisionOptionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ScientificDecisionOptionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ScientificDecisionRecorderIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ScientificDecisionRecorderIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ScientificDecisionRequest":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "question",
                    "options",
                    "declared_scope",
                    "workflow_identity",
                    "workflow_run_identity",
                    "affected_task_instance_identity",
                    "affected_transition_identity",
                    "required_response_source_identity",
                    "required_authority_context_identity",
                    "definition_identity",
                    "definition_version",
                ),
            )
            record = ScientificDecisionRequest(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ScientificDecisionRequestIdentity,
                ),
                question=self._exact(self._decode(fields["question"], seen), str),
                options=tuple(
                    self._exact(item, ScientificDecisionOption)
                    for item in self._items(self._decode(fields["options"], seen))
                ),
                declared_scope=self._exact(
                    self._decode(fields["declared_scope"], seen), str
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                affected_task_instance_identity=self._exact(
                    self._decode(fields["affected_task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
                affected_transition_identity=self._exact(
                    self._decode(fields["affected_transition_identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
                required_response_source_identity=self._exact(
                    self._decode(fields["required_response_source_identity"], seen),
                    ResponseSourceIdentity,
                ),
                required_authority_context_identity=self._exact(
                    self._decode(fields["required_authority_context_identity"], seen),
                    AuthorityContextIdentity,
                ),
                definition_identity=self._exact(
                    self._decode(fields["definition_identity"], seen), str
                ),
                definition_version=self._exact(
                    self._decode(fields["definition_version"], seen), int
                ),
            )
            return record
        if tag == "ScientificDecisionRequestIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ScientificDecisionRequestIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ScientificDecisionTransitionRecordIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ScientificDecisionTransitionRecordIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ScientificDecisionWorkflowTransitionRecord":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "sequence_identity",
                    "sequence_index",
                    "workflow_identity",
                    "workflow_run_identity",
                    "definition_reference_identity",
                    "runtime_bundle_identity",
                    "request_identity",
                    "resolution_identity",
                    "producer_provenance_identity",
                    "firing_result",
                ),
            )
            record = ScientificDecisionWorkflowTransitionRecord(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ScientificDecisionTransitionRecordIdentity,
                ),
                sequence_identity=self._exact(
                    self._decode(fields["sequence_identity"], seen),
                    WorkflowTransitionSequenceIdentity,
                ),
                sequence_index=self._exact(
                    self._decode(fields["sequence_index"], seen), int
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                definition_reference_identity=self._exact(
                    self._decode(fields["definition_reference_identity"], seen),
                    WorkflowDefinitionReferenceIdentity,
                ),
                runtime_bundle_identity=self._exact(
                    self._decode(fields["runtime_bundle_identity"], seen),
                    WorkflowRuntimeBundleIdentity,
                ),
                request_identity=self._exact(
                    self._decode(fields["request_identity"], seen),
                    ScientificDecisionRequestIdentity,
                ),
                resolution_identity=self._exact(
                    self._decode(fields["resolution_identity"], seen),
                    ResultObjectIdentity,
                ),
                producer_provenance_identity=self._exact(
                    self._decode(fields["producer_provenance_identity"], seen),
                    ResultProducerProvenanceIdentity,
                ),
                firing_result=self._exact(
                    self._decode(fields["firing_result"], seen),
                    ColoredPetriNetFiringResult,
                ),
            )
            return record
        if tag == "UnknownLegacyResultProducer":
            fields = self._fields(
                wire,
                tag,
                ("identity", "source_identity", "evidence_identities", "limitations"),
            )
            record = UnknownLegacyResultProducer(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ResultProducerProvenanceIdentity,
                ),
                source_identity=self._exact(
                    self._decode(fields["source_identity"], seen),
                    RetainedResultSourceIdentity,
                ),
                evidence_identities=tuple(
                    self._exact(item, ResultProducerEvidenceIdentity)
                    for item in self._items(
                        self._decode(fields["evidence_identities"], seen)
                    )
                ),
                limitations=tuple(
                    self._exact(item, str)
                    for item in self._items(self._decode(fields["limitations"], seen))
                ),
            )
            return record
        raise _WorkflowRunWireUnsupported

    def _parse_NestedWorkflowInvocation_terminal_observation_identity(
        self, value: _RunValue
    ) -> NestedWorkflowObservationIdentity | None:
        if type(value) is NestedWorkflowObservationIdentity:
            return self._exact(value, NestedWorkflowObservationIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_NestedWorkflowInvocation_terminal_child_revision_identity(
        self, value: _RunValue
    ) -> WorkflowRunRevisionIdentity | None:
        if type(value) is WorkflowRunRevisionIdentity:
            return self._exact(value, WorkflowRunRevisionIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_NestedWorkflowInvocation_replay_equal_child_result_identity(
        self, value: _RunValue
    ) -> WorkflowRunReplayResultIdentity | None:
        if type(value) is WorkflowRunReplayResultIdentity:
            return self._exact(value, WorkflowRunReplayResultIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ResultDependency_producer_workflow_run_identity(
        self, value: _RunValue
    ) -> WorkflowRunIdentity | None:
        if type(value) is WorkflowRunIdentity:
            return self._exact(value, WorkflowRunIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ResultDependency_consumer_activation_identity(
        self, value: _RunValue
    ) -> TaskActivationIdentity | None:
        if type(value) is TaskActivationIdentity:
            return self._exact(value, TaskActivationIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ResultObjectReference_producer_provenance(
        self, value: _RunValue
    ) -> (
        RepresentedTaskResultProducer
        | RepresentedScientificDecisionIngressProducer
        | ExternalResultProducer
        | ImportedRetainedResultProducer
        | HumanAuthoredResultProducer
        | UnknownLegacyResultProducer
    ):
        if type(value) is RepresentedTaskResultProducer:
            return self._exact(value, RepresentedTaskResultProducer)
        if type(value) is RepresentedScientificDecisionIngressProducer:
            return self._exact(value, RepresentedScientificDecisionIngressProducer)
        if type(value) is ExternalResultProducer:
            return self._exact(value, ExternalResultProducer)
        if type(value) is ImportedRetainedResultProducer:
            return self._exact(value, ImportedRetainedResultProducer)
        if type(value) is HumanAuthoredResultProducer:
            return self._exact(value, HumanAuthoredResultProducer)
        if type(value) is UnknownLegacyResultProducer:
            return self._exact(value, UnknownLegacyResultProducer)
        raise TypeError("wrong closed field variant")
