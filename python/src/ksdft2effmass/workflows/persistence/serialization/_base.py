"""Shared typed mechanics for the closed WorkflowRun wire serializers."""

from __future__ import annotations

import base64
from datetime import datetime
from typing import Literal

from ksdft2effmass.petrinet.colored.definitions import (
    ColoredPetriNetArcDefinition,
    ColoredPetriNetArcIdentity,
    ColoredPetriNetColorDefinition,
    ColoredPetriNetDefinition,
    ColoredPetriNetPlaceDefinition,
    ColoredPetriNetSelectionPolicy,
    ColoredPetriNetTransitionDefinition,
)
from ksdft2effmass.petrinet.colored.enablement import (
    ColoredPetriNetEnablementFailure,
    ColoredPetriNetEnablementFailureCode,
    ColoredPetriNetEnablementFailureIdentity,
    ColoredPetriNetEnablementResult,
    ColoredPetriNetEnablementResultIdentity,
    ColoredPetriNetExpressionEvaluatorIdentity,
    ColoredPetriNetOrderingPolicyIdentity,
    ColoredPetriNetTransitionEnablerIdentity,
)
from ksdft2effmass.petrinet.colored.expressions import (
    ColoredPetriNetGuardExpression,
    ColoredPetriNetGuardOperator,
    ColoredPetriNetInhibitorPattern,
    ColoredPetriNetInputInscription,
    ColoredPetriNetInputMode,
    ColoredPetriNetOutputInscription,
    ColoredPetriNetTokenPattern,
    ColoredPetriNetTokenTemplate,
    ColoredPetriNetValueExpression,
    ColoredPetriNetValueExpressionKind,
)
from ksdft2effmass.petrinet.colored.firing import (
    ColoredPetriNetFiringAudit,
    ColoredPetriNetFiringFailure,
    ColoredPetriNetFiringFailureCode,
    ColoredPetriNetFiringFailureIdentity,
    ColoredPetriNetFiringInput,
    ColoredPetriNetFiringOutcomeKind,
    ColoredPetriNetFiringResult,
    ColoredPetriNetFiringResultIdentity,
    ColoredPetriNetInhibitorEvaluation,
    ColoredPetriNetProducedToken,
    ColoredPetriNetTokenOccurrence,
    ColoredPetriNetTransitionFirerIdentity,
)
from ksdft2effmass.petrinet.colored.markings import (
    ColoredPetriNetBinding,
    ColoredPetriNetBindingAssignment,
    ColoredPetriNetBindingVariableIdentity,
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingIdentity,
    ColoredPetriNetPlaceIdentity,
    ColoredPetriNetPlaceMarking,
    ColoredPetriNetTransitionIdentity,
)
from ksdft2effmass.petrinet.colored.selection import (
    ColoredPetriNetBindingSelectorIdentity,
    ColoredPetriNetSelectionDirective,
    ColoredPetriNetSelectionDirectiveIdentity,
    ColoredPetriNetSelectionFailureCode,
    ColoredPetriNetSelectionOutcomeKind,
    ColoredPetriNetSelectionResult,
    ColoredPetriNetSelectionResultIdentity,
)
from ksdft2effmass.petrinet.colored.validation import (
    ColoredPetriNetValidationIssue,
    ColoredPetriNetValidationIssueCode,
)
from ksdft2effmass.petrinet.colored.values import (
    ColoredPetriNetColorIdentity,
    ColoredPetriNetToken,
    ColoredPetriNetTokenIdentity,
    ColoredPetriNetValue,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.workflows.artifacts import (
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    ResultArtifactRelationIdentity,
)
from ksdft2effmass.workflows.model import (
    AllOfTaskActivationSelection,
    AnyOfTaskActivationSelection,
    AttemptIdentity,
    DirectTaskActivationSelection,
    OperationIdentity,
    TaskActivation,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskGateSelection,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    TaskStartGate,
    TaskStartGateIdentity,
    TaskStartGateSet,
    TaskStartGateSetIdentity,
    TaskStartGateSetMode,
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
    ChildWorkflowCreationIdempotencyIdentity,
    DispatchCreationIdempotencyIdentity,
    DispatchDestinationIdentity,
    DispatchObservationRecordIdentity,
    DispatchOutcomeRecordIdentity,
    DispatchResourceScopeIdentity,
    ExecutionGrantIdentity,
    ExecutionGrantRevisionIdentity,
    ExternalProducerAttemptIdentity,
    ExternalResultProducerIdentity,
    HumanResultAuthorIdentity,
    NativeOutputAdmissionIdentity,
    NestedWorkflowInvocationIdentity,
    NestedWorkflowInvocationIntentIdentity,
    NestedWorkflowMembershipIdentity,
    NestedWorkflowObservationIdentity,
    ObligationDispositionIdentity,
    ObligationIdentity,
    ResultDependencyIdentity,
    ResultObjectReferenceIdentity,
    ResultProducerEvidenceIdentity,
    ResultProductionRecordIdentity,
    RetainedResultSourceIdentity,
    ScientificExecutionAuthoritySnapshotIdentity,
    ScientificExecutionAuthorityStateIdentity,
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
    TaskInvocationFailureIdentity,
    TaskInvocationOutcomeIdentity,
    TaskWorkflowMembershipIdentity,
    TaskWorkflowTransitionRecordIdentity,
    WorkflowDefinitionReferenceIdentity,
    WorkflowRunReplayResultIdentity,
    WorkflowRuntimeBundleIdentity,
    WorkflowTransitionSequenceIdentity,
)
from ksdft2effmass.workflows.runs.records import (
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeKind,
    DispatchObservationKind,
    DispatchObservationRecord,
    DispatchOutcomeKind,
    DispatchOutcomeRecord,
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
    ObligationDisposition,
    ObligationDispositionKind,
    RepresentedTaskResultProducer,
    ResultDependency,
    ResultObjectReference,
    ResultProductionRecord,
    ScientificDecisionOption,
    ScientificDecisionRequest,
    ScientificDecisionWorkflowTransitionRecord,
    ScientificExecutionAuthorityReference,
    SimulationDispatchEntry,
    SimulationDispatchObligation,
    SimulationDispatchOutcome,
    SimulationExecutionRequestCorrelation,
    TaskAttempt,
    TaskAttemptStatus,
    TaskFailureRecord,
    TaskInvocationFailure,
    TaskInvocationOutcome,
    TaskInvocationOutcomeKind,
    TaskWorkflowMembership,
    TaskWorkflowTransitionRecord,
    UnknownLegacyResultProducer,
)

from ...model import (
    ResultObject,
    ResultObjectIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ...observations import NormalizedObservationSet
from ...runs.aggregate import WorkflowRun
from ...runs.identities import (
    AuthorityContextIdentity,
    AuthorityReservationOutcomeIdentity,
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
    ScientificDecisionResolution,
)
from ..records import (
    WorkflowEncodedResultValue,
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowResultValueCodec,
    WorkflowResultValueDecodeResult,
    WorkflowResultValueEncodeResult,
)

type _ResultJson = None | bool | str | list[_ResultJson] | dict[str, _ResultJson]
type _RunValue = (
    None
    | tuple[_RunValue, ...]
    | AllOfTaskActivationSelection
    | AnyOfTaskActivationSelection
    | ArtifactManifestEntryIdentity
    | ArtifactManifestIdentity
    | AttemptIdentity
    | AuthorityContextIdentity
    | AuthorityReservationOutcome
    | AuthorityReservationOutcomeIdentity
    | AuthorityReservationOutcomeKind
    | ChildWorkflowCreationIdempotencyIdentity
    | ColoredPetriNetArcDefinition
    | ColoredPetriNetArcIdentity
    | ColoredPetriNetBinding
    | ColoredPetriNetBindingAssignment
    | ColoredPetriNetBindingSelectorIdentity
    | ColoredPetriNetBindingVariableIdentity
    | ColoredPetriNetColorDefinition
    | ColoredPetriNetColorIdentity
    | ColoredPetriNetDefinition
    | ColoredPetriNetDefinitionIdentity
    | ColoredPetriNetEnablementFailure
    | ColoredPetriNetEnablementFailureCode
    | ColoredPetriNetEnablementFailureIdentity
    | ColoredPetriNetEnablementResult
    | ColoredPetriNetEnablementResultIdentity
    | ColoredPetriNetExpressionEvaluatorIdentity
    | ColoredPetriNetFiringAudit
    | ColoredPetriNetFiringFailure
    | ColoredPetriNetFiringFailureCode
    | ColoredPetriNetFiringFailureIdentity
    | ColoredPetriNetFiringInput
    | ColoredPetriNetFiringOutcomeKind
    | ColoredPetriNetFiringResult
    | ColoredPetriNetFiringResultIdentity
    | ColoredPetriNetGuardExpression
    | ColoredPetriNetGuardOperator
    | ColoredPetriNetInhibitorEvaluation
    | ColoredPetriNetInhibitorPattern
    | ColoredPetriNetInputInscription
    | ColoredPetriNetInputMode
    | ColoredPetriNetMarking
    | ColoredPetriNetMarkingIdentity
    | ColoredPetriNetOrderingPolicyIdentity
    | ColoredPetriNetOutputInscription
    | ColoredPetriNetPlaceDefinition
    | ColoredPetriNetPlaceIdentity
    | ColoredPetriNetPlaceMarking
    | ColoredPetriNetProducedToken
    | ColoredPetriNetSelectionDirective
    | ColoredPetriNetSelectionDirectiveIdentity
    | ColoredPetriNetSelectionFailureCode
    | ColoredPetriNetSelectionOutcomeKind
    | ColoredPetriNetSelectionPolicy
    | ColoredPetriNetSelectionResult
    | ColoredPetriNetSelectionResultIdentity
    | ColoredPetriNetToken
    | ColoredPetriNetTokenIdentity
    | ColoredPetriNetTokenOccurrence
    | ColoredPetriNetTokenPattern
    | ColoredPetriNetTokenTemplate
    | ColoredPetriNetTransitionDefinition
    | ColoredPetriNetTransitionEnablerIdentity
    | ColoredPetriNetTransitionFirerIdentity
    | ColoredPetriNetTransitionIdentity
    | ColoredPetriNetValidationIssue
    | ColoredPetriNetValidationIssueCode
    | ColoredPetriNetValue
    | ColoredPetriNetValueExpression
    | ColoredPetriNetValueExpressionKind
    | ColoredPetriNetValueKind
    | DirectTaskActivationSelection
    | DispatchCreationIdempotencyIdentity
    | DispatchDestinationIdentity
    | DispatchObservationKind
    | DispatchObservationRecord
    | DispatchObservationRecordIdentity
    | DispatchOutcomeKind
    | DispatchOutcomeRecord
    | DispatchOutcomeRecordIdentity
    | DispatchResourceScopeIdentity
    | ExecutionGrantIdentity
    | ExecutionGrantRevisionIdentity
    | ExternalProducerAttemptIdentity
    | ExternalResultProducer
    | ExternalResultProducerIdentity
    | HumanAuthoredResultProducer
    | HumanResultAuthorIdentity
    | ImportedRetainedResultProducer
    | NativeOutputAdmission
    | NativeOutputAdmissionIdentity
    | NestedWorkflowInvocation
    | NestedWorkflowInvocationIdentity
    | NestedWorkflowInvocationIntentIdentity
    | NestedWorkflowInvocationIntent
    | NestedWorkflowTerminalObservation
    | NestedWorkflowTerminalObservationKind
    | NestedWorkflowInvocationKind
    | NestedWorkflowMembership
    | NestedWorkflowMembershipIdentity
    | NestedWorkflowObservationIdentity
    | ObligationDisposition
    | ObligationDispositionIdentity
    | ObligationDispositionKind
    | ObligationIdentity
    | OperationIdentity
    | RepresentedScientificDecisionIngressProducer
    | RepresentedTaskResultProducer
    | ResponseSourceIdentity
    | ResultArtifactRelationIdentity
    | ResultDependency
    | ResultDependencyIdentity
    | ResultObject
    | ResultObjectContentIdentity
    | ResultObjectDomainIdentity
    | ResultObjectIdentity
    | ResultObjectReference
    | ResultObjectReferenceIdentity
    | ResultObjectTypeIdentity
    | ResultProducerEvidenceIdentity
    | ResultProducerProvenanceIdentity
    | ResultProductionRecord
    | ResultProductionRecordIdentity
    | RetainedResultSourceIdentity
    | ScientificDecisionOption
    | ScientificDecisionOptionIdentity
    | ScientificDecisionRecorderIdentity
    | ScientificDecisionRequest
    | ScientificDecisionRequestIdentity
    | ScientificDecisionResolution
    | ScientificDecisionTransitionRecordIdentity
    | ScientificDecisionWorkflowTransitionRecord
    | ScientificExecutionAuthorityGrant
    | ScientificExecutionAuthorityReference
    | ScientificExecutionAuthoritySnapshot
    | ScientificExecutionAuthoritySnapshotIdentity
    | ScientificExecutionAuthorityStateIdentity
    | ScientificExecutionAuthorityVerificationKind
    | ScientificExecutionGrantState
    | ScientificExecutorIdentity
    | SimulationDispatchEntry
    | SimulationDispatchEntryIdentity
    | SimulationDispatchEntryReceiptIdentity
    | SimulationDispatchObligation
    | SimulationDispatchObservationIdentity
    | SimulationDispatchOutcome
    | SimulationDispatchOutcomeIdentity
    | SimulationExecutionAuthorizationOutcomeKind
    | SimulationExecutionAuthorizationPhase
    | SimulationExecutionAuthorizationRequest
    | SimulationExecutionAuthorizationResult
    | SimulationExecutionAuthorizationResultIdentity
    | SimulationExecutionRequestCorrelation
    | SimulationExecutionRequestCorrelationIdentity
    | SimulationExecutionRequestIdentity
    | TaskActivation
    | TaskActivationIdentity
    | TaskAttempt
    | TaskAttemptRecordIdentity
    | TaskAttemptStatus
    | TaskDefinitionIdentity
    | TaskFailureRecord
    | TaskFailureRecordIdentity
    | TaskGateSelection
    | TaskInputBinding
    | TaskInstance
    | TaskInstanceIdentity
    | TaskInvocationFailure
    | TaskInvocationFailureIdentity
    | TaskInvocationOutcome
    | TaskInvocationOutcomeIdentity
    | TaskInvocationOutcomeKind
    | TaskStartGate
    | TaskStartGateIdentity
    | TaskStartGateSet
    | TaskStartGateSetIdentity
    | TaskStartGateSetMode
    | TaskWorkflowMembership
    | TaskWorkflowMembershipIdentity
    | TaskWorkflowTransitionRecord
    | TaskWorkflowTransitionRecordIdentity
    | UnknownLegacyResultProducer
    | WorkflowDefinitionReferenceIdentity
    | WorkflowIdentity
    | WorkflowRun
    | WorkflowRunIdentity
    | WorkflowRunReplayResultIdentity
    | WorkflowRunRevisionIdentity
    | WorkflowRuntimeBundleIdentity
    | WorkflowTransitionSequenceIdentity
    | bool
    | bytes
    | datetime
    | float
    | int
    | str
)


class _WorkflowRunCodecFailure(Exception):
    """Carry sanitized represented failure across local aggregate traversal."""

    def __init__(
        self,
        failure: WorkflowPersistenceFailure,
        status: Literal["incompatible", "invalid", "corrupt", "error"],
    ) -> None:
        super().__init__("aggregate representation failed")
        self.failure = failure
        self.status = status


class _WorkflowRunWireUnsupported(Exception):
    """Signal that one bounded wire serializer does not own a value or tag."""


class _WorkflowRunWireSerializer:
    """Shared recursive wire grammar used by bounded serializer facets."""

    result_codec: WorkflowResultValueCodec

    def _encode(
        self, value: _RunValue, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _ResultJson:
        raise NotImplementedError

    def _decode(
        self, wire: _ResultJson, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _RunValue:
        raise NotImplementedError

    def _parse_DispatchOutcomeRecord_failure_record_identity(
        self, value: _RunValue
    ) -> TaskFailureRecordIdentity | None:
        raise NotImplementedError

    def _parse_NestedWorkflowInvocation_terminal_child_revision_identity(
        self, value: _RunValue
    ) -> WorkflowRunRevisionIdentity | None:
        raise NotImplementedError

    def _parse_ResultDependency_producer_workflow_run_identity(
        self, value: _RunValue
    ) -> WorkflowRunIdentity | None:
        raise NotImplementedError

    @staticmethod
    def _failure(
        phase: str, code: WorkflowPersistenceFailureCode
    ) -> _WorkflowRunCodecFailure:
        status: Literal["incompatible", "invalid", "corrupt", "error"]
        if code in (
            WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
            WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
        ):
            status = "incompatible"
        elif code in (
            WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
            WorkflowPersistenceFailureCode.CODEC_ERROR,
        ):
            status = "error"
        else:
            status = "invalid" if phase == "encode" else "corrupt"
        return _WorkflowRunCodecFailure(
            WorkflowPersistenceFailure(
                implementation_identity="ksdft2effmass.workflows.WorkflowRunSerializer:1",
                phase=phase,
                code=code,
                input_identities=(),
                expected="canonical run with exact result and binding metadata",
                observed=code.value,
                diagnostic="aggregate representation did not complete",
                claim_boundary=(
                    "software representation only; "
                    "no stored presence, replay or authority"
                ),
            ),
            status,
        )

    @staticmethod
    def _record(tag: str, fields: dict[str, _ResultJson]) -> _ResultJson:
        return {"type": tag, "fields": fields}

    @staticmethod
    def _fields(
        wire: _ResultJson, tag: str, names: tuple[str, ...]
    ) -> dict[str, _ResultJson]:
        if (
            not isinstance(wire, dict)
            or set(wire) != {"type", "fields"}
            or wire["type"] != tag
        ):
            raise ValueError("wrong tagged record")
        fields = wire["fields"]
        if not isinstance(fields, dict) or set(fields) != set(names):
            raise ValueError("wrong record field closure")
        return fields

    @staticmethod
    def _string(value: _ResultJson) -> str:
        if type(value) is not str:
            raise TypeError("expected exact string")
        return value

    @staticmethod
    def _exact[T](value: _RunValue, expected: type[T]) -> T:
        if type(value) is not expected:
            raise TypeError("wrong exact domain field type")
        return value

    @staticmethod
    def _items(value: _RunValue) -> tuple[_RunValue, ...]:
        if type(value) is not tuple:
            raise TypeError("expected immutable tuple")
        return value

    @staticmethod
    def _as_result(value: _RunValue) -> ResultObject:
        if (
            not isinstance(value, ResultObject)
            or type(value.identity) is not ResultObjectIdentity
        ):
            raise TypeError("expected a complete codec-supported result")
        return value

    def _remember(
        self,
        envelope: WorkflowEncodedResultValue,
        seen: dict[str, WorkflowEncodedResultValue],
    ) -> None:
        previous = seen.get(envelope.result_identity.value)
        if previous is not None and previous != envelope:
            raise self._failure(
                "decode", WorkflowPersistenceFailureCode.CONTENT_MISMATCH
            )
        seen[envelope.result_identity.value] = envelope

    def _encode_result(
        self, value: ResultObject, seen: dict[str, WorkflowEncodedResultValue]
    ) -> WorkflowEncodedResultValue:
        result = self.result_codec.encode(value)
        if type(result) is not WorkflowResultValueEncodeResult:
            raise TypeError("codec returned the wrong encode result type")
        if result.encoded is None:
            assert result.failure is not None and result.status != "encoded"
            raise _WorkflowRunCodecFailure(result.failure, result.status)
        envelope = result.encoded
        if envelope.result_identity != value.identity:
            raise self._failure(
                "encode", WorkflowPersistenceFailureCode.IDENTITY_MISMATCH
            )
        self._remember(envelope, seen)
        decoded = self.result_codec.decode(envelope)
        if type(decoded) is not WorkflowResultValueDecodeResult:
            raise TypeError("codec returned the wrong decode result type")
        if decoded.value is None:
            assert decoded.failure is not None and decoded.status != "decoded"
            raise _WorkflowRunCodecFailure(decoded.failure, decoded.status)
        if decoded.value.identity != envelope.result_identity:
            raise self._failure(
                "encode", WorkflowPersistenceFailureCode.IDENTITY_MISMATCH
            )
        checked = self.result_codec.encode(decoded.value)
        if type(checked) is not WorkflowResultValueEncodeResult:
            raise TypeError("codec returned the wrong encode result type")
        if checked.encoded is None:
            assert checked.failure is not None and checked.status != "encoded"
            raise _WorkflowRunCodecFailure(checked.failure, checked.status)
        if checked.encoded != envelope:
            raise self._failure(
                "encode", WorkflowPersistenceFailureCode.CONTENT_MISMATCH
            )
        # Nested sources participate in the same cross-occurrence agreement.
        if type(value) is NormalizedObservationSet:
            for source in value.sources:
                self._encode_result(source, seen)
        if type(decoded.value) is NormalizedObservationSet:
            for source in decoded.value.sources:
                self._encode_result(source, seen)
        return envelope

    def _decode_result(
        self,
        envelope: WorkflowEncodedResultValue,
        seen: dict[str, WorkflowEncodedResultValue],
    ) -> ResultObject:
        result = self.result_codec.decode(envelope)
        if type(result) is not WorkflowResultValueDecodeResult:
            raise TypeError("codec returned the wrong decode result type")
        if result.value is None:
            assert result.failure is not None and result.status != "decoded"
            raise _WorkflowRunCodecFailure(result.failure, result.status)
        if result.value.identity != envelope.result_identity:
            raise self._failure(
                "decode", WorkflowPersistenceFailureCode.IDENTITY_MISMATCH
            )
        self._remember(envelope, seen)
        if self._encode_result(result.value, seen) != envelope:
            raise self._failure(
                "decode", WorkflowPersistenceFailureCode.CONTENT_MISMATCH
            )
        return result.value

    def _check_reference(
        self, value: ResultObjectReference, seen: dict[str, WorkflowEncodedResultValue]
    ) -> None:
        envelope = self._encode_result(value.result, seen)
        if (
            value.concrete_type_identity != envelope.concrete_type_identity
            or value.owning_domain_identity != envelope.owning_domain_identity
            or value.content_identity != envelope.content_identity
        ):
            raise self._failure(
                "decode", WorkflowPersistenceFailureCode.CONTENT_MISMATCH
            )

    def _result_wire(self, envelope: WorkflowEncodedResultValue) -> _ResultJson:
        return self._record(
            "WorkflowEncodedResultValue",
            {
                "result_identity": self._record(
                    "ResultObjectIdentity", {"value": envelope.result_identity.value}
                ),
                "concrete_type_identity": self._record(
                    "ResultObjectTypeIdentity",
                    {"value": envelope.concrete_type_identity.value},
                ),
                "owning_domain_identity": self._record(
                    "ResultObjectDomainIdentity",
                    {"value": envelope.owning_domain_identity.value},
                ),
                "schema_identity": envelope.schema_identity,
                "content_identity": self._record(
                    "ResultObjectContentIdentity",
                    {"value": envelope.content_identity.value},
                ),
                "payload": self._record(
                    "bytes",
                    {"value": base64.b64encode(envelope.payload).decode("ascii")},
                ),
                "payload_digest": envelope.payload_digest,
            },
        )
