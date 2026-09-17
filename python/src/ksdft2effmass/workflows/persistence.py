"""Typed complete WorkflowRun representation and atomic historical persistence.

Outward domains supply explicit codecs; protocol membership never establishes
serializability. These immutable envelopes and closed operation outcomes bind exact
bytes and nominal result metadata, not scientific validity or execution authority.
Aggregate encoded/run/decode, transaction, snapshot, load, write and claim-load
records provide intrinsic type, variant and byte-binding checks only. They do not
perform structural validation or establish stored presence. WorkflowRunSerializer
now traverses complete supported aggregate representations with an injected result
codec. WorkflowRunTransactionValidator checks exact candidate binding, retained
structural closure and byte-equivalent immutable predecessor extension without replay
or authorization computation. WorkflowRunAtomicRepository composes explicit shared
storage with those owners, preserving complete observations and deriving historical
claim receipts only after exact acknowledgement or confirmed reconciliation. Historical
commitment is not effect permission. No replay, native-file access, registry or dynamic
import occurs here; the separate entry service remains outside this module.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Literal, Never, Protocol, cast, runtime_checkable
from uuid import uuid4

from ksdft2effmass.persistence import (
    AtomicRevisionStore,
    Commit,
    CommitResult,
    CommitStatus,
    Revision,
    RevisionReadRequest,
    RevisionReadResult,
    RevisionReadStatus,
    RevisionSelector,
)
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

from .model import (
    ResultObject,
    ResultObjectIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from .observations import NormalizedObservationSet, NormalizedObservationSource
from .runs.aggregate import WorkflowRun
from .runs.authority import WorkflowRunClaimCommitReceipt
from .runs.identities import (
    AuthorityContextIdentity,
    AuthorityReservationOutcomeIdentity,
    BoundaryReceiptIdentity,
    ResponseSourceIdentity,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectTypeIdentity,
    ResultProducerProvenanceIdentity,
    ScientificDecisionOptionIdentity,
    ScientificDecisionRecorderIdentity,
    ScientificDecisionRequestIdentity,
    ScientificDecisionTransitionRecordIdentity,
    WorkflowRunClaimCommitReceiptIdentity,
    WorkflowRunRevisionIdentity,
)
from .runs.records import (
    RepresentedScientificDecisionIngressProducer,
    ScientificDecisionResolution,
)
from .runs.replay import _WorkflowRunStructureValidator

type _ResultJson = None | bool | str | list[_ResultJson] | dict[str, _ResultJson]
type _WorkflowValue = ScientificDecisionResolution | NormalizedObservationSet

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


class WorkflowPersistenceFailureCode(StrEnum):
    """Closed represented codec and persistence failure categories.

    Attributes
    ----------
    UNSUPPORTED_TYPE, UNSUPPORTED_VERSION
        No selected concrete type or wire-version implementation exists.
    MALFORMED_REPRESENTATION
        Known wire grammar, canonical bytes or field closure is violated.
    IDENTITY_MISMATCH, CONTENT_MISMATCH
        Nominal correlation or represented content binding disagrees.
    INVARIANT_VIOLATION
        Reconstructed known-domain values violate their constructor contract.
    REPRESENTATION_LIMIT
        Allocation or recursion limits prevented completion.
    CODEC_ERROR
        The operation failed without a reconstructed value.
    """

    UNSUPPORTED_TYPE = "unsupported_type"
    UNSUPPORTED_VERSION = "unsupported_version"
    MALFORMED_REPRESENTATION = "malformed_representation"
    IDENTITY_MISMATCH = "identity_mismatch"
    CONTENT_MISMATCH = "content_mismatch"
    INVARIANT_VIOLATION = "invariant_violation"
    REPRESENTATION_LIMIT = "representation_limit"
    CODEC_ERROR = "codec_error"


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowPersistenceFailure:
    """Immutable sanitized failure evidence, never a partial successful value.

    Parameters
    ----------
    implementation_identity
        Nonempty codec or persistence implementation and version label.
    phase
        Nonempty operation phase, such as ``encode`` or ``decode``.
    code
        Exact closed failure category.
    input_identities
        Ordered immutable tuple of nonempty applicable input identity labels.
        Empty means none was available; labels are observations, not authentication.
    expected, observed
        Nonempty represented expected and observed conditions.
    diagnostic
        Nonempty sanitized diagnostic. Implementations must not copy arbitrary
        exception text, payloads, credentials or native output here.
    claim_boundary
        Nonempty explicit limitation of the failure evidence.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        A required label or tuple member is empty.
    """

    implementation_identity: str
    phase: str
    code: WorkflowPersistenceFailureCode
    input_identities: tuple[str, ...]
    expected: str
    observed: str
    diagnostic: str
    claim_boundary: str

    def __post_init__(self) -> None:
        """Enforce immutable exact field and nonempty-label invariants."""
        for value in (
            self.implementation_identity,
            self.phase,
            self.expected,
            self.observed,
            self.diagnostic,
            self.claim_boundary,
        ):
            if type(value) is not str:
                raise TypeError("failure labels must be exact strings")
            if not value:
                raise ValueError("failure labels must not be empty")
        if type(self.code) is not WorkflowPersistenceFailureCode:
            raise TypeError("code must be WorkflowPersistenceFailureCode")
        if type(self.input_identities) is not tuple or any(
            type(value) is not str for value in self.input_identities
        ):
            raise TypeError("input_identities must be a tuple of exact strings")
        if any(not value for value in self.input_identities):
            raise ValueError("input identities must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowEncodedResultValue:
    """One complete concrete result envelope with exact SHA-256 byte binding.

    Parameters
    ----------
    result_identity
        Exact nominal identity of the concrete result.
    concrete_type_identity
        Exact supported import-name/version label selected by its codec.
    owning_domain_identity
        Exact domain owner of the concrete value contract.
    schema_identity
        Nonempty concrete payload schema label. This record does not decide support.
    content_identity
        Exact owning content label. Historical opaque labels are not interpreted
        as hashes; a separate payload digest always binds these bytes.
    payload
        Exact immutable bytes containing the complete concrete representation.
    payload_digest
        Lowercase SHA-256 hexadecimal digest of ``payload``. Construction checks
        exact agreement, but does not decode or authenticate the representation.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type, including mutable byte buffers.
    ValueError
        The schema is empty or the payload digest disagrees.
    """

    result_identity: ResultObjectIdentity
    concrete_type_identity: ResultObjectTypeIdentity
    owning_domain_identity: ResultObjectDomainIdentity
    schema_identity: str
    content_identity: ResultObjectContentIdentity
    payload: bytes
    payload_digest: str

    def __post_init__(self) -> None:
        """Enforce nominal fields and the exact-byte digest invariant."""
        if type(self.result_identity) is not ResultObjectIdentity:
            raise TypeError("result_identity must be ResultObjectIdentity")
        if type(self.concrete_type_identity) is not ResultObjectTypeIdentity:
            raise TypeError("concrete_type_identity must be ResultObjectTypeIdentity")
        if type(self.owning_domain_identity) is not ResultObjectDomainIdentity:
            raise TypeError("owning_domain_identity must be ResultObjectDomainIdentity")
        if type(self.content_identity) is not ResultObjectContentIdentity:
            raise TypeError("content_identity must be ResultObjectContentIdentity")
        if type(self.schema_identity) is not str:
            raise TypeError("schema_identity must be an exact string")
        if not self.schema_identity:
            raise ValueError("schema_identity must not be empty")
        if type(self.payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        if type(self.payload_digest) is not str:
            raise TypeError("payload_digest must be an exact string")
        if self.payload_digest != hashlib.sha256(self.payload).hexdigest():
            raise ValueError("payload_digest must match the exact payload SHA-256")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowResultValueEncodeResult:
    """Closed result of encoding one explicitly supported concrete value.

    Parameters
    ----------
    status
        Exactly ``encoded``, ``incompatible``, ``invalid`` or ``error``.
    encoded
        Complete envelope on success only; otherwise ``None``.
    failure
        Structured failure on nonsuccess only; otherwise ``None``.

    Raises
    ------
    TypeError
        Status, envelope or failure has the wrong semantic type.
    ValueError
        The status is unknown or fields do not match its variant.
    """

    status: Literal["encoded", "incompatible", "invalid", "error"]
    encoded: WorkflowEncodedResultValue | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Reject open statuses and success/failure field mixing."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in ("encoded", "incompatible", "invalid", "error"):
            raise ValueError("unknown encode status")
        if (
            self.encoded is not None
            and type(self.encoded) is not WorkflowEncodedResultValue
        ):
            raise TypeError("encoded must be WorkflowEncodedResultValue or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "encoded":
            if self.encoded is None or self.failure is not None:
                raise ValueError("encoded alone carries an envelope and no failure")
        elif self.encoded is not None or self.failure is None:
            raise ValueError("encode failure carries failure evidence and no envelope")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowResultValueDecodeResult:
    """Closed concrete result reconstruction outcome.

    Parameters
    ----------
    status
        Exactly ``decoded``, ``incompatible``, ``corrupt`` or ``error``.
    value
        Concrete ResultObject on success only. The selected codec, not structural
        protocol membership or this container, establishes supported exact type,
        complete reconstruction and operational immutability.
    failure
        Structured failure on nonsuccess only; otherwise ``None``.

    Raises
    ------
    TypeError
        Status, result identity or failure has the wrong semantic type.
    ValueError
        The status is unknown or fields do not match its variant.
    """

    status: Literal["decoded", "incompatible", "corrupt", "error"]
    value: ResultObject | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Validate result shape without claiming arbitrary protocol serialization."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in ("decoded", "incompatible", "corrupt", "error"):
            raise ValueError("unknown decode status")
        if self.value is not None and (
            not isinstance(self.value, ResultObject)
            or type(self.value.identity) is not ResultObjectIdentity
        ):
            raise TypeError("value must expose an exact ResultObjectIdentity")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "decoded":
            if self.value is None or self.failure is not None:
                raise ValueError("decoded alone carries a value and no failure")
        elif self.value is not None or self.failure is None:
            raise ValueError("decode failure carries failure evidence and no value")


@runtime_checkable
class WorkflowResultValueCodec(Protocol):
    """Explicit injected port for complete, versioned concrete result values.

    Domain implementations use exact concrete branches, not reflection or a registry.
    Unknown concrete types/versions are incompatible. Canonical known-wire corruption
    is distinct from incompatibility and operational error. Implementations perform
    no native-file reads or effects and retain no mutable serializer/cache state.
    """

    def encode(self, value: ResultObject) -> WorkflowResultValueEncodeResult:
        """Encode a supported exact concrete value or return a closed failure.

        Parameters
        ----------
        value
            A workflow-facing result, not a promise of serializability.

        Returns
        -------
        WorkflowResultValueEncodeResult
            Complete encoded value or incompatible, invalid or error evidence.

        Raises
        ------
        TypeError
            Input does not expose an exact nominal ResultObject identity.
        """
        ...

    def decode(
        self, value: WorkflowEncodedResultValue
    ) -> WorkflowResultValueDecodeResult:
        """Decode one complete concrete envelope without interpreting authority.

        Parameters
        ----------
        value
            Exact nominal metadata and content-bound immutable payload.

        Returns
        -------
        WorkflowResultValueDecodeResult
            Complete concrete value or incompatible, corrupt or error evidence.

        Raises
        ------
        TypeError
            Input is not an exact WorkflowEncodedResultValue.
        """
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunCommitBinding:
    """Durable labels to include in the complete aggregate payload.

    Parameters
    ----------
    transaction_identity
        Nonempty explicit caller-supplied stable operation label. Changing it must
        change the serialized aggregate bytes and content identity.
    commit_idempotency_identity
        Nonempty shared Commit key. Observing this label in bytes does not confirm
        the actual stored key; exact complete-expectation reconciliation is required.
    persistence_implementation_identity
        Nonempty historical writer/version label, never the current reader label.
        Future v1 writes require
        ``ksdft2effmass.workflows.WorkflowRunAtomicRepository:1``; readers must
        recognize support explicitly, not replace unknown writers.

    Raises
    ------
    TypeError
        Any label is not an exact built-in string.
    ValueError
        Any label is empty.

    Notes
    -----
    This intrinsic record alone derives no receipt, confirms no commit and grants no
    advancement or effect permission. Aggregate binding and reconciliation remain
    responsibilities of the serializer and future repository.
    """

    transaction_identity: str
    commit_idempotency_identity: str
    persistence_implementation_identity: str

    def __post_init__(self) -> None:
        """Enforce exact nonempty durable labels without selecting support."""
        for value in (
            self.transaction_identity,
            self.commit_idempotency_identity,
            self.persistence_implementation_identity,
        ):
            if type(value) is not str:
                raise TypeError("commit binding labels must be exact strings")
            if not value:
                raise ValueError("commit binding labels must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowEncodedRun:
    """Complete aggregate bytes and their domain content binding.

    Parameters
    ----------
    schema_identity
        Nonempty aggregate wire schema label; support is decided by the serializer.
    content_identity
        Exactly ``schema_identity + ':sha256:' + sha256(payload).hexdigest()``.
    payload
        Exact immutable bytes. Construction checks binding, not wire validity.

    Raises
    ------
    TypeError
        A field is not an exact string or exact bytes as declared.
    ValueError
        The schema is empty or the content identity does not bind these bytes.
    """

    schema_identity: str
    content_identity: str
    payload: bytes

    def __post_init__(self) -> None:
        """Check exact representation types and intrinsic content binding."""
        if (
            type(self.schema_identity) is not str
            or type(self.content_identity) is not str
        ):
            raise TypeError("schema and content identities must be exact strings")
        if type(self.payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        if not self.schema_identity:
            raise ValueError("schema_identity must not be empty")
        expected = (
            self.schema_identity + ":sha256:" + hashlib.sha256(self.payload).hexdigest()
        )
        if self.content_identity != expected:
            raise ValueError("content_identity must bind schema and exact payload")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunEncodeResult:
    """Closed aggregate encoding outcome without partial successful bytes.

    Parameters
    ----------
    status
        Exactly ``encoded``, ``incompatible``, ``invalid`` or ``error``.
    encoded
        Complete encoded run on success only; otherwise None.
    failure
        Complete sanitized failure on nonsuccess only; otherwise None.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        Status or success/failure field closure is invalid.
    """

    status: Literal["encoded", "incompatible", "invalid", "error"]
    encoded: WorkflowEncodedRun | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Enforce exact closed variant fields."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in ("encoded", "incompatible", "invalid", "error"):
            raise ValueError("unknown aggregate encode status")
        if self.encoded is not None and type(self.encoded) is not WorkflowEncodedRun:
            raise TypeError("encoded must be WorkflowEncodedRun or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "encoded":
            if self.encoded is None or self.failure is not None:
                raise ValueError("encoded requires bytes and prohibits failure")
        elif self.encoded is not None or self.failure is None:
            raise ValueError("nonsuccess requires failure and prohibits bytes")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunDecodeResult:
    """Closed complete aggregate and durable-binding reconstruction outcome.

    Parameters
    ----------
    status
        Exactly ``decoded``, ``incompatible``, ``corrupt`` or ``error``.
    run
        Complete immutable run on success only. No replay equality is implied.
    binding
        Complete persisted transaction/key/historical-writer labels on success only.
    failure
        Structured evidence on nonsuccess only; never a partial run or binding.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        Status or success/failure field closure is invalid.
    """

    status: Literal["decoded", "incompatible", "corrupt", "error"]
    run: WorkflowRun | None = None
    binding: WorkflowRunCommitBinding | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Keep complete successful reconstruction separate from failures."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in ("decoded", "incompatible", "corrupt", "error"):
            raise ValueError("unknown aggregate decode status")
        if self.run is not None and type(self.run) is not WorkflowRun:
            raise TypeError("run must be WorkflowRun or None")
        if (
            self.binding is not None
            and type(self.binding) is not WorkflowRunCommitBinding
        ):
            raise TypeError("binding must be WorkflowRunCommitBinding or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "decoded":
            if self.run is None or self.binding is None or self.failure is not None:
                raise ValueError("decoded requires complete run and binding only")
        elif self.run is not None or self.binding is not None or self.failure is None:
            raise ValueError("nonsuccess requires failure without run or binding")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunTransaction:
    """One complete candidate and explicit durable compare-and-swap metadata.

    Parameters
    ----------
    binding
        Single immutable owner of transaction, commit-key and historical writer labels.
    run_identity
        Exact nominal run targeted by the transaction.
    expected_predecessor_revision_identity
        Exact predecessor slot; None means genesis, not an unspecified expectation.
    candidate
        Complete immutable proposed run. Cross-object correlation, serialization,
        append-only history and version support belong to the transaction validator.
    schema_identity, content_identity
        Nonempty exact labels claimed for the complete candidate representation.
        Construction does not compute or verify its bytes.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        A schema or content label is empty.

    Notes
    -----
    Merely constructing this record never submits a commit or validates a candidate.
    """

    binding: WorkflowRunCommitBinding
    run_identity: WorkflowRunIdentity
    expected_predecessor_revision_identity: WorkflowRunRevisionIdentity | None
    candidate: WorkflowRun
    schema_identity: str
    content_identity: str

    def __post_init__(self) -> None:
        """Check only intrinsic field types and nonempty labels."""
        if type(self.binding) is not WorkflowRunCommitBinding:
            raise TypeError("binding must be WorkflowRunCommitBinding")
        if type(self.run_identity) is not WorkflowRunIdentity:
            raise TypeError("run_identity must be WorkflowRunIdentity")
        if (
            self.expected_predecessor_revision_identity is not None
            and type(self.expected_predecessor_revision_identity)
            is not WorkflowRunRevisionIdentity
        ):
            raise TypeError(
                "expected predecessor must be WorkflowRunRevisionIdentity or None"
            )
        if type(self.candidate) is not WorkflowRun:
            raise TypeError("candidate must be WorkflowRun")
        for value in (self.schema_identity, self.content_identity):
            if type(value) is not str:
                raise TypeError("representation labels must be exact strings")
            if not value:
                raise ValueError("representation labels must not be empty")

    @property
    def transaction_identity(self) -> str:
        """Exact operation label from the sole durable binding."""
        return self.binding.transaction_identity

    @property
    def commit_idempotency_identity(self) -> str:
        """Exact commit key from the sole durable binding, not store confirmation."""
        return self.binding.commit_idempotency_identity


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunSnapshot:
    """Complete reconstructed run, durable binding and exact retained revision.

    Parameters
    ----------
    run
        Complete immutable run; no identity-only or partial stand-in is accepted.
    binding
        Persisted transaction/key/historical-writer labels, not a reconstructed receipt.
    revision
        Exact shared revision envelope including immutable payload bytes.
        The repository, not this intrinsic container, verifies cross-object binding,
        digest, version and structural closure before returning a loaded snapshot.

    Raises
    ------
    TypeError
        Any input is not its exact declared concrete record type.

    Notes
    -----
    This container establishes neither durable presence nor replay equality, authority,
    advancement permission or effect entry. It performs no serialization or store I/O.
    """

    run: WorkflowRun
    binding: WorkflowRunCommitBinding
    revision: Revision

    def __post_init__(self) -> None:
        """Reject partial and wrong-type snapshot fields."""
        if type(self.run) is not WorkflowRun:
            raise TypeError("run must be WorkflowRun")
        if type(self.binding) is not WorkflowRunCommitBinding:
            raise TypeError("binding must be WorkflowRunCommitBinding")
        if type(self.revision) is not Revision:
            raise TypeError("revision must be Revision")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunLoadResult:
    """Closed domain read outcome preserving complete shared read evidence.

    Parameters
    ----------
    status
        Exactly loaded, absent, mismatch, incompatible, corrupt, indeterminate or error.
    request
        Exact read request, including selector and every reconciliation expectation.
    store_result
        Complete shared result when a store observation exists; otherwise None.
        Its result/request/store identities and variant-specific evidence are retained.
    snapshot
        Complete snapshot only for loaded; otherwise None.
    failure
        Domain failure for pre-read or domain rejection, otherwise None. Shared
        nonsuccess evidence may suffice without a separate domain failure.

    Raises
    ------
    TypeError
        An input has the wrong exact semantic type.
    ValueError
        Status or variant evidence closure fails.

    Notes
    -----
    Correlation of the independent request, shared observation and snapshot belongs
    to the repository. Construction is not a read and does not verify those links.
    """

    status: Literal[
        "loaded",
        "absent",
        "mismatch",
        "incompatible",
        "corrupt",
        "indeterminate",
        "error",
    ]
    request: RevisionReadRequest
    store_result: RevisionReadResult | None = None
    snapshot: WorkflowRunSnapshot | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Enforce success-only snapshots and retained nonsuccess evidence."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in (
            "loaded",
            "absent",
            "mismatch",
            "incompatible",
            "corrupt",
            "indeterminate",
            "error",
        ):
            raise ValueError("unknown domain load status")
        if type(self.request) is not RevisionReadRequest:
            raise TypeError("request must be RevisionReadRequest")
        if (
            self.store_result is not None
            and type(self.store_result) is not RevisionReadResult
        ):
            raise TypeError("store_result must be RevisionReadResult or None")
        if self.snapshot is not None and type(self.snapshot) is not WorkflowRunSnapshot:
            raise TypeError("snapshot must be WorkflowRunSnapshot or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "loaded":
            if (
                self.snapshot is None
                or self.store_result is None
                or self.store_result.status.value != "found"
                or self.failure is not None
            ):
                raise ValueError("loaded requires snapshot and found evidence only")
        elif self.status == "absent" and (
            self.store_result is None or self.store_result.status.value != "absent"
        ):
            raise ValueError("absent requires shared absence evidence")
        elif self.snapshot is not None:
            raise ValueError("nonsuccess prohibits a snapshot")
        elif self.failure is None and (
            self.store_result is None or self.store_result.status.value != self.status
        ):
            raise ValueError(
                "nonsuccess requires matching shared or domain failure evidence"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunWriteResult:
    """Closed domain commit outcome without lost shared evidence or effect permission.

    Parameters
    ----------
    status
        Exactly committed, conflict, indeterminate, error, invalid or incompatible.
    transaction
        Exact candidate transaction addressed by this outcome.
    store_result
        Complete shared commit result when submitted and observed, otherwise None.
    predecessor_load
        Complete predecessor-read evidence when obtained, otherwise None. This
        preserves read uncertainty or rejection without fabricating a commit result.
    snapshot
        Complete bound snapshot only for committed, otherwise None.
    claim_receipts
        Immutable ordered newly appended historical claim receipts on committed only;
        may be empty. They grant no effect-entry permission.
    failure
        Domain failure for rejection or operational error; None on committed.
        Shared nonsuccess evidence may suffice without a second domain failure.

    Raises
    ------
    TypeError
        An input has the wrong exact type or receipts are not an immutable tuple.
    ValueError
        Status or variant evidence closure fails, or receipt identities repeat.
    """

    status: Literal[
        "committed", "conflict", "indeterminate", "error", "invalid", "incompatible"
    ]
    transaction: WorkflowRunTransaction
    store_result: CommitResult | None = None
    predecessor_load: WorkflowRunLoadResult | None = None
    snapshot: WorkflowRunSnapshot | None = None
    claim_receipts: tuple[WorkflowRunClaimCommitReceipt, ...] = ()
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Keep acknowledged snapshots separate from rejection and uncertainty."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in (
            "committed",
            "conflict",
            "indeterminate",
            "error",
            "invalid",
            "incompatible",
        ):
            raise ValueError("unknown domain write status")
        if type(self.transaction) is not WorkflowRunTransaction:
            raise TypeError("transaction must be WorkflowRunTransaction")
        if (
            self.store_result is not None
            and type(self.store_result) is not CommitResult
        ):
            raise TypeError("store_result must be CommitResult or None")
        if (
            self.predecessor_load is not None
            and type(self.predecessor_load) is not WorkflowRunLoadResult
        ):
            raise TypeError("predecessor_load must be WorkflowRunLoadResult or None")
        if self.snapshot is not None and type(self.snapshot) is not WorkflowRunSnapshot:
            raise TypeError("snapshot must be WorkflowRunSnapshot or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if type(self.claim_receipts) is not tuple or any(
            type(receipt) is not WorkflowRunClaimCommitReceipt
            for receipt in self.claim_receipts
        ):
            raise TypeError("claim_receipts must be a tuple of exact claim receipts")
        identities = tuple(receipt.identity for receipt in self.claim_receipts)
        if len(set(identities)) != len(identities):
            raise ValueError("claim receipt identities must not repeat")
        if self.status == "committed":
            if (
                self.snapshot is None
                or self.store_result is None
                or self.store_result.status.value != "committed"
                or self.failure is not None
            ):
                raise ValueError(
                    "committed requires snapshot and acknowledged shared evidence"
                )
        elif self.status == "conflict" and (
            self.store_result is None or self.store_result.status.value != "conflict"
        ):
            raise ValueError("conflict requires shared conflict evidence")
        elif self.snapshot is not None or self.claim_receipts:
            raise ValueError("nonsuccess prohibits snapshot and claim receipts")
        elif self.failure is None and (
            self.store_result is None or self.store_result.status.value != self.status
        ):
            raise ValueError(
                "nonsuccess requires matching shared or domain failure evidence"
            )
        if self.status in ("invalid", "incompatible") and self.store_result is not None:
            raise ValueError("pre-store rejection prohibits a shared commit result")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunClaimLoadResult:
    """Closed historical claim observation, never effect-entry permission.

    Parameters
    ----------
    status
        Same seven statuses as WorkflowRunLoadResult. Only loaded carries a receipt.
    claimed_reservation_identity
        Exact requested nominal claim selector, retained even on nonsuccess.
    request
        Exact read request including every historical reconciliation expectation.
    store_result
        Complete underlying shared read evidence when present, otherwise None.
    snapshot
        Complete historical run snapshot on loaded only; otherwise None.
    receipt
        Reconstructed historical claim receipt on loaded only; otherwise None.
    failure
        Claim-specific failure on rejection after a loaded run; otherwise None.
        A matching shared nonsuccess may propagate without a second failure.

    Raises
    ------
    TypeError
        An input has the wrong exact semantic type.
    ValueError
        Status or success/failure closure fails.

    Notes
    -----
    The repository owns exact-revision expectation confirmation and receipt derivation.
    This record only retains the result and grants no advancement or effect authority.
    """

    status: Literal[
        "loaded",
        "absent",
        "mismatch",
        "incompatible",
        "corrupt",
        "indeterminate",
        "error",
    ]
    claimed_reservation_identity: AuthorityReservationOutcomeIdentity
    request: RevisionReadRequest
    store_result: RevisionReadResult | None = None
    snapshot: WorkflowRunSnapshot | None = None
    receipt: WorkflowRunClaimCommitReceipt | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Require both historical snapshot and receipt for loaded only."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in (
            "loaded",
            "absent",
            "mismatch",
            "incompatible",
            "corrupt",
            "indeterminate",
            "error",
        ):
            raise ValueError("unknown claim-load status")
        if (
            type(self.claimed_reservation_identity)
            is not AuthorityReservationOutcomeIdentity
        ):
            raise TypeError(
                "claimed_reservation_identity must be "
                "AuthorityReservationOutcomeIdentity"
            )
        if type(self.request) is not RevisionReadRequest:
            raise TypeError("request must be RevisionReadRequest")
        if (
            self.store_result is not None
            and type(self.store_result) is not RevisionReadResult
        ):
            raise TypeError("store_result must be RevisionReadResult or None")
        if self.snapshot is not None and type(self.snapshot) is not WorkflowRunSnapshot:
            raise TypeError("snapshot must be WorkflowRunSnapshot or None")
        if (
            self.receipt is not None
            and type(self.receipt) is not WorkflowRunClaimCommitReceipt
        ):
            raise TypeError("receipt must be WorkflowRunClaimCommitReceipt or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "loaded":
            if (
                self.snapshot is None
                or self.store_result is None
                or self.store_result.status.value != "found"
                or self.receipt is None
                or self.failure is not None
            ):
                raise ValueError("loaded claim requires loaded run and receipt only")
        elif self.snapshot is not None or self.receipt is not None:
            raise ValueError("nonsuccess prohibits snapshot and claim receipt")
        elif self.status == "absent" and (
            self.store_result is None or self.store_result.status.value != "absent"
        ):
            raise ValueError("absent requires shared absence evidence")
        elif self.failure is None and (
            self.store_result is None or self.store_result.status.value != self.status
        ):
            raise ValueError(
                "claim rejection requires shared or domain failure evidence"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunValidationResult:
    """Record validation bound to the exact transaction and predecessor inputs.

    Parameters
    ----------
    status
        Exactly ``valid``, ``invalid``, ``incompatible`` or ``error``.
    transaction
        The complete input transaction, retained without replacement.
    predecessor
        Explicit historical snapshot input, or None for genesis. This record alone
        does not establish that the predecessor was stored.
    encoded
        Exact validated candidate representation on valid only, otherwise None.
    failure
        Structured diagnostic on nonsuccess only, otherwise None.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        The status, variant closure or encoded transaction labels disagree.

    Notes
    -----
    This immutable result does not establish replay equality, stored presence,
    historical authentication, execution authority or scientific acceptance.
    """

    status: Literal["valid", "invalid", "incompatible", "error"]
    transaction: WorkflowRunTransaction
    predecessor: WorkflowRunSnapshot | None = None
    encoded: WorkflowEncodedRun | None = None
    failure: WorkflowPersistenceFailure | None = None

    def __post_init__(self) -> None:
        """Check exact fields and closed success/failure representation."""
        if type(self.status) is not str:
            raise TypeError("status must be an exact string")
        if self.status not in ("valid", "invalid", "incompatible", "error"):
            raise ValueError("unknown transaction validation status")
        if type(self.transaction) is not WorkflowRunTransaction:
            raise TypeError("transaction must be WorkflowRunTransaction")
        if (
            self.predecessor is not None
            and type(self.predecessor) is not WorkflowRunSnapshot
        ):
            raise TypeError("predecessor must be WorkflowRunSnapshot or None")
        if self.encoded is not None and type(self.encoded) is not WorkflowEncodedRun:
            raise TypeError("encoded must be WorkflowEncodedRun or None")
        if (
            self.failure is not None
            and type(self.failure) is not WorkflowPersistenceFailure
        ):
            raise TypeError("failure must be WorkflowPersistenceFailure or None")
        if self.status == "valid":
            if self.encoded is None or self.failure is not None:
                raise ValueError("valid requires encoded candidate without failure")
            if (
                self.encoded.schema_identity != self.transaction.schema_identity
                or self.encoded.content_identity != self.transaction.content_identity
            ):
                raise ValueError("encoded labels must match the input transaction")
        elif self.encoded is not None or self.failure is None:
            raise ValueError("nonsuccess requires failure without encoded candidate")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunTransactionValidator:
    """Validate exact candidate binding, retained closure and immutable extension.

    Parameters
    ----------
    serializer
        Exact immutable WorkflowRunSerializer with an explicit outward result codec.
        Wire mechanics and complete result-value equality remain serializer-owned.

    Notes
    -----
    Validation checks the same transaction/candidate, its schema/content labels,
    predecessor address and complete snapshot bytes, run-level correlations,
    contiguous zero-based transition order and retained predecessor-marking links.
    Collections extend by nominal identity; attempts and transitions retain sequence
    prefixes. Historical records and initial marking, Workflow/definition/runtime/
    schema/adapter identities remain byte-equivalent under the codec. This operation
    does not use NumPy-backed dataclass equality for historical comparison.
    Newly introduced dispatch entries must name this transaction's non-null
    predecessor and candidate revision; genesis entries are invalid. Historical
    entries retain their original introduction labels rather than being rebound
    to the current successor. A new nested intent introduces its membership,
    activation and STARTED group in this candidate revision. A new terminal
    observation requires its exact intent source in the actual predecessor and
    introduces its terminal attempt/outcome group atomically in this revision.
    Genesis observations and same-commit intent/terminal introduction are invalid.
    Historical intent and observations retain their original bytes and labels.

    Retained structural closure is distinct from computed replay equality. The
    current marking may remain replay-unequal. No transitions or authorization
    requests are evaluated, and no repository, native file or external effect is
    accessed. A supplied predecessor is an explicit input, not proof of storage.

    Raises
    ------
    TypeError
        The serializer is not its exact declared type.
    """

    serializer: WorkflowRunSerializer

    def __post_init__(self) -> None:
        """Require the explicit domain serializer dependency."""
        if type(self.serializer) is not WorkflowRunSerializer:
            raise TypeError("serializer must be WorkflowRunSerializer")

    def execute(
        self,
        transaction: WorkflowRunTransaction,
        predecessor: WorkflowRunSnapshot | None = None,
    ) -> WorkflowRunValidationResult:
        """Check a complete candidate against its explicitly addressed predecessor.

        Parameters
        ----------
        transaction
            Exact complete proposed transaction; its labels are never inferred.
        predecessor
            Exact historical snapshot for the expected predecessor, not latest.
            Required for a non-genesis transaction and prohibited for genesis.

        Returns
        -------
        WorkflowRunValidationResult
            Bound validated bytes on valid only. Invalid, incompatible and error
            preserve structured failures without a partial successful candidate.

        Raises
        ------
        TypeError
            A direct argument has the wrong exact semantic type.
        """
        if type(transaction) is not WorkflowRunTransaction:
            raise TypeError("transaction must be WorkflowRunTransaction")
        if predecessor is not None and type(predecessor) is not WorkflowRunSnapshot:
            raise TypeError("predecessor must be WorkflowRunSnapshot or None")
        try:
            return self._validate(transaction, predecessor)
        except MemoryError, RecursionError:
            code = WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
        except Exception:
            code = WorkflowPersistenceFailureCode.CODEC_ERROR
        return self._reject(
            transaction, predecessor, "error", code, "validation did not complete"
        )

    def _validate(
        self,
        transaction: WorkflowRunTransaction,
        predecessor: WorkflowRunSnapshot | None,
    ) -> WorkflowRunValidationResult:
        run = transaction.candidate
        expected = transaction.expected_predecessor_revision_identity
        if transaction.schema_identity != "ksdft2effmass.workflow-run:1":
            return self._reject(
                transaction,
                predecessor,
                "incompatible",
                WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                "transaction schema is not supported",
            )
        if (
            run.identity != transaction.run_identity
            or run.predecessor_revision_identity != expected
            or (expected is None) != (predecessor is None)
        ):
            return self._reject(
                transaction,
                predecessor,
                "invalid",
                WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                "candidate/run/predecessor slots do not agree",
            )
        encoded_result = self.serializer.serialize(run, transaction.binding)
        if encoded_result.status != "encoded":
            assert encoded_result.failure is not None
            return WorkflowRunValidationResult(
                status=encoded_result.status,
                transaction=transaction,
                predecessor=predecessor,
                failure=encoded_result.failure,
            )
        encoded = encoded_result.encoded
        assert encoded is not None
        if (
            transaction.schema_identity != encoded.schema_identity
            or transaction.content_identity != encoded.content_identity
        ):
            return self._reject(
                transaction,
                predecessor,
                "invalid",
                WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                "transaction labels do not bind the exact candidate bytes",
            )
        # Check structural links on the exact reconstructed candidate. Complete
        # equal-identity result content is bound by the codec, not NumPy dataclass
        # equality or a protocol-identity stand-in.
        decoded = self.serializer.deserialize(encoded.payload)
        if decoded.status != "decoded":
            assert decoded.failure is not None
            return WorkflowRunValidationResult(
                status="invalid" if decoded.status == "corrupt" else decoded.status,
                transaction=transaction,
                predecessor=predecessor,
                failure=decoded.failure,
            )
        assert decoded.run is not None
        issue = _WorkflowRunStructureValidator().execute(decoded.run)
        if issue is not None:
            return self._reject(
                transaction,
                predecessor,
                "invalid",
                WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                issue.code.value + ": " + issue.diagnostic,
            )
        if predecessor is not None:
            old = predecessor.run
            revision = predecessor.revision
            if (
                old.identity != run.identity
                or old.revision_identity != expected
                or revision.stream_id != old.identity.value
                or revision.revision_id != old.revision_identity.value
                or revision.predecessor_revision_id
                != (
                    None
                    if old.predecessor_revision_identity is None
                    else old.predecessor_revision_identity.value
                )
            ):
                return self._reject(
                    transaction,
                    predecessor,
                    "invalid",
                    WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                    "predecessor snapshot does not name the exact expected revision",
                )
            old_encoded_result = self.serializer.serialize(old, predecessor.binding)
            if old_encoded_result.status != "encoded":
                assert old_encoded_result.failure is not None
                return WorkflowRunValidationResult(
                    status=old_encoded_result.status,
                    transaction=transaction,
                    predecessor=predecessor,
                    failure=old_encoded_result.failure,
                )
            old_encoded = old_encoded_result.encoded
            assert old_encoded is not None
            if (
                old_encoded.schema_identity != revision.schema_id
                or old_encoded.content_identity != revision.content_id
                or old_encoded.payload != revision.payload
            ):
                return self._reject(
                    transaction,
                    predecessor,
                    "invalid",
                    WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                    "predecessor snapshot differs from its exact revision bytes",
                )
            old_issue = _WorkflowRunStructureValidator().execute(old)
            if old_issue is not None:
                return self._reject(
                    transaction,
                    predecessor,
                    "invalid",
                    WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                    "predecessor: "
                    + old_issue.code.value
                    + ": "
                    + old_issue.diagnostic,
                )
            projection = self._historical_projection(run, old)
            projection_result = self.serializer.serialize(
                projection, predecessor.binding
            )
            if projection_result.status != "encoded":
                assert projection_result.failure is not None
                return WorkflowRunValidationResult(
                    status=projection_result.status,
                    transaction=transaction,
                    predecessor=predecessor,
                    failure=projection_result.failure,
                )
            assert projection_result.encoded is not None
            if projection_result.encoded.payload != old_encoded.payload:
                return self._reject(
                    transaction,
                    predecessor,
                    "invalid",
                    WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                    "candidate rewrites or removes immutable predecessor state",
                )
        historical_entry_ids: set[SimulationDispatchEntryIdentity] = (
            set()
            if predecessor is None
            else {entry.identity for entry in predecessor.run.dispatch_entries}
        )
        if any(
            entry.identity not in historical_entry_ids
            and (
                expected is None
                or entry.predecessor_revision_identity != expected
                or entry.committed_revision_identity != run.revision_identity
            )
            for entry in run.dispatch_entries
        ):
            return self._reject(
                transaction,
                predecessor,
                "invalid",
                WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                "new dispatch entry must name its committing predecessor and revision",
            )
        introduction_issue = self._nested_introduction_issue(
            run, None if predecessor is None else predecessor.run
        )
        if introduction_issue is not None:
            return self._reject(
                transaction, predecessor, "invalid",
                WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                introduction_issue,
            )
        return WorkflowRunValidationResult(
            status="valid",
            transaction=transaction,
            predecessor=predecessor,
            encoded=encoded,
        )

    @staticmethod
    def _nested_introduction_issue(
        run: WorkflowRun, old: WorkflowRun | None
    ) -> str | None:
        """Bind new intent and terminal groups to actual transaction history."""
        old_sources = {
            v.identity: v
            for v in (
                ()
                if old is None
                else old.nested_invocations + old.nested_invocation_intents
            )
        }
        old_attempts = {v.identity for v in (() if old is None else old.attempts)}
        old_activations = {v.identity for v in (() if old is None else old.activations)}
        old_memberships = {
            v.identity for v in (() if old is None else old.nested_memberships)
        }
        old_observations = {
            v.identity
            for v in (() if old is None else old.nested_terminal_observations)
        }
        old_outcomes = {v.identity for v in (() if old is None else old.outcomes)}
        memberships = {v.child_workflow_run_identity: v for v in run.nested_memberships}
        intent_sources = run.nested_invocation_intents + tuple(
            v
            for v in run.nested_invocations
            if v.kind is NestedWorkflowInvocationKind.PENDING
        )
        for source in intent_sources:
            if source.identity in old_sources:
                continue
            started_identity = (
                source.started_attempt_record_identity
                if isinstance(source, NestedWorkflowInvocationIntent)
                else source.attempt_record_identity
            )
            membership = memberships.get(source.child_workflow_run_identity)
            if (
                source.parent_revision_identity != run.revision_identity
                or source.activation_identity in old_activations
                or started_identity in old_attempts
                or membership is None
                or membership.identity in old_memberships
            ):
                return (
                    "new nested intent must introduce its membership, activation "
                    "and STARTED group in the candidate revision"
                )
        for observation in run.nested_terminal_observations:
            if observation.identity in old_observations:
                continue
            predecessor_source = old_sources.get(observation.intent_identity)
            if (
                predecessor_source is None
                or (
                    isinstance(predecessor_source, NestedWorkflowInvocation)
                    and predecessor_source.kind
                    is not NestedWorkflowInvocationKind.PENDING
                )
                or observation.parent_revision_identity != run.revision_identity
                or observation.terminal_attempt_record_identity in old_attempts
                or observation.outcome_identity in old_outcomes
            ):
                return (
                    "new nested observation requires an actual predecessor intent "
                    "and a new terminal group in the candidate revision"
                )
        return None

    @staticmethod
    def _historical_projection(run: WorkflowRun, old: WorkflowRun) -> WorkflowRun:
        """Select old identities from the candidate; serializer owns byte comparison."""
        return replace(
            run,
            revision_identity=old.revision_identity,
            predecessor_revision_identity=old.predecessor_revision_identity,
            current_marking=old.current_marking,
            attempts=run.attempts[: len(old.attempts)],
            transitions=run.transitions[: len(old.transitions)],
            task_instances=tuple(
                v
                for v in run.task_instances
                if v.identity in {o.identity for o in old.task_instances}
            ),
            task_memberships=tuple(
                v
                for v in run.task_memberships
                if v.identity in {o.identity for o in old.task_memberships}
            ),
            nested_memberships=tuple(
                v
                for v in run.nested_memberships
                if v.identity in {o.identity for o in old.nested_memberships}
            ),
            nested_invocations=tuple(
                v
                for v in run.nested_invocations
                if v.identity in {o.identity for o in old.nested_invocations}
            ),
            nested_invocation_intents=tuple(
                v for v in run.nested_invocation_intents
                if v.identity in {o.identity for o in old.nested_invocation_intents}
            ),
            nested_terminal_observations=tuple(
                v for v in run.nested_terminal_observations
                if v.identity in {o.identity for o in old.nested_terminal_observations}
            ),
            activations=tuple(
                v
                for v in run.activations
                if v.identity in {o.identity for o in old.activations}
            ),
            outcomes=tuple(
                v
                for v in run.outcomes
                if v.identity in {o.identity for o in old.outcomes}
            ),
            result_references=tuple(
                v
                for v in run.result_references
                if v.identity in {o.identity for o in old.result_references}
            ),
            result_productions=tuple(
                v
                for v in run.result_productions
                if v.identity in {o.identity for o in old.result_productions}
            ),
            native_output_admissions=tuple(
                v
                for v in run.native_output_admissions
                if v.identity in {o.identity for o in old.native_output_admissions}
            ),
            result_dependencies=tuple(
                v
                for v in run.result_dependencies
                if v.identity in {o.identity for o in old.result_dependencies}
            ),
            failures=tuple(
                v
                for v in run.failures
                if v.identity in {o.identity for o in old.failures}
            ),
            authorization_results=tuple(
                v
                for v in run.authorization_results
                if v.identity in {o.identity for o in old.authorization_results}
            ),
            authority_references=tuple(
                v
                for v in run.authority_references
                if v.grant_identity
                in {o.grant_identity for o in old.authority_references}
            ),
            execution_request_correlations=tuple(
                v
                for v in run.execution_request_correlations
                if v.identity
                in {o.identity for o in old.execution_request_correlations}
            ),
            authority_reservations=tuple(
                v
                for v in run.authority_reservations
                if v.identity in {o.identity for o in old.authority_reservations}
            ),
            dispatch_obligations=tuple(
                v
                for v in run.dispatch_obligations
                if v.identity in {o.identity for o in old.dispatch_obligations}
            ),
            dispatch_entries=tuple(
                v
                for v in run.dispatch_entries
                if v.identity in {o.identity for o in old.dispatch_entries}
            ),
            dispatch_observations=tuple(
                v
                for v in run.dispatch_observations
                if v.identity in {o.identity for o in old.dispatch_observations}
            ),
            dispatch_outcomes=tuple(
                v
                for v in run.dispatch_outcomes
                if v.identity in {o.identity for o in old.dispatch_outcomes}
            ),
            obligation_dispositions=tuple(
                v
                for v in run.obligation_dispositions
                if v.identity in {o.identity for o in old.obligation_dispositions}
            ),
            scientific_decision_requests=tuple(
                v
                for v in run.scientific_decision_requests
                if v.identity in {o.identity for o in old.scientific_decision_requests}
            ),
            scientific_decision_resolutions=tuple(
                v
                for v in run.scientific_decision_resolutions
                if v.identity
                in {o.identity for o in old.scientific_decision_resolutions}
            ),
        )

    @staticmethod
    def _reject(
        transaction: WorkflowRunTransaction,
        predecessor: WorkflowRunSnapshot | None,
        status: Literal["invalid", "incompatible", "error"],
        code: WorkflowPersistenceFailureCode,
        diagnostic: str,
    ) -> WorkflowRunValidationResult:
        return WorkflowRunValidationResult(
            status=status,
            transaction=transaction,
            predecessor=predecessor,
            failure=WorkflowPersistenceFailure(
                implementation_identity="ksdft2effmass.workflows.WorkflowRunTransactionValidator:1",
                phase="transaction_validation",
                code=code,
                input_identities=(
                    transaction.transaction_identity,
                    transaction.run_identity.value,
                    transaction.candidate.revision_identity.value,
                ),
                expected=(
                    "exact candidate binding and immutable closed predecessor extension"
                ),
                observed=code.value,
                diagnostic=diagnostic,
                claim_boundary=(
                    "structural software validation only; "
                    "no replay, stored presence or authority"
                ),
            ),
        )


@runtime_checkable
class WorkflowRunRepository(Protocol):
    """Domain repository port; observations never grant advancement or effects."""

    def load(self, request: RevisionReadRequest) -> WorkflowRunLoadResult:
        """Read one exact request and return complete structurally checked evidence.

        Parameters
        ----------
        request
            Explicit stream and latest-or-revision selector with optional expectations.

        Returns
        -------
        WorkflowRunLoadResult
            Closed observation; only loaded contains a complete snapshot.
        """
        ...

    def commit(self, transaction: WorkflowRunTransaction) -> WorkflowRunWriteResult:
        """Validate and submit one complete transaction, without retry or replay.

        Parameters
        ----------
        transaction
            Complete candidate and exact predecessor, schema, content and key binding.

        Returns
        -------
        WorkflowRunWriteResult
            Closed write observation retaining underlying store evidence.
        """
        ...

    def load_claim(
        self,
        request: RevisionReadRequest,
        claimed_reservation_identity: AuthorityReservationOutcomeIdentity,
    ) -> WorkflowRunClaimLoadResult:
        """Reconcile historical commitment, never effect permission.

        Parameters
        ----------
        request
            Explicit revision with the complete reconciliation expectation group.
        claimed_reservation_identity
            Exact CLAIMED record selector in that historical revision.

        Returns
        -------
        WorkflowRunClaimLoadResult
            Historical snapshot and deterministically reconstructed receipt on loaded.
        """
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunAtomicRepository:
    """Bind complete WorkflowRun values to one explicit atomic store.

    Parameters
    ----------
    store
        Explicit structural AtomicRevisionStore dependency. No database is selected
        implicitly, and no native artifact or development storage is accessed.
    serializer
        Exact immutable serializer with the selected outward result codec.
    validator
        Exact transaction validator bound to this same serializer instance. Detached
        validators or differently configured serialization dependencies are rejected.

    Raises
    ------
    TypeError
        A dependency does not have its declared semantic type.
    ValueError
        The validator is not bound to this serializer instance.

    Notes
    -----
    Reads check shared request/address correlation, schema, SHA-256 content, complete
    reconstruction and structural closure; they do not compute replay equality.
    Writes read the exact predecessor (not latest), validate immutable extension and
    submit once. Shared CAS and idempotency decide committed versus conflict, including
    replay after later heads. No uncertainty authorizes automatic retry.

    Claim receipts require an exact current-in-that-revision CLAIMED record. The same
    versioned compact-JSON SHA-256 derivation serves acknowledged writes and confirmed
    complete-expectation reads. Persisted transaction, key and historical writer labels
    participate; fresh store result UUIDs do not. Labels establish consistency, not
    authentication, authority or permission to enter an external effect.
    """

    store: AtomicRevisionStore
    serializer: WorkflowRunSerializer
    validator: WorkflowRunTransactionValidator

    def __post_init__(self) -> None:
        """Require explicitly bound domain dependencies."""
        if not isinstance(self.store, AtomicRevisionStore):
            raise TypeError("store must implement AtomicRevisionStore")
        if type(self.serializer) is not WorkflowRunSerializer:
            raise TypeError("serializer must be WorkflowRunSerializer")
        if type(self.validator) is not WorkflowRunTransactionValidator:
            raise TypeError("validator must be WorkflowRunTransactionValidator")
        if self.validator.serializer is not self.serializer:
            raise ValueError("validator must bind the repository serializer")

    def load(self, request: RevisionReadRequest) -> WorkflowRunLoadResult:
        """Issue one read and verify its exact envelope and complete domain value.

        Parameters
        ----------
        request
            Exact shared request; complete expectations require explicit confirmation.

        Returns
        -------
        WorkflowRunLoadResult
            Loaded, absent, mismatch, incompatible, corrupt, indeterminate or error.
            Shared observations are retained even when domain binding fails.

        Raises
        ------
        TypeError
            The direct argument is not an exact RevisionReadRequest.
        """
        if type(request) is not RevisionReadRequest:
            raise TypeError("request must be RevisionReadRequest")
        observed: RevisionReadResult | None = None
        try:
            observed = self.store.read(request)
            if type(observed) is not RevisionReadResult:
                observed = None
                raise TypeError("store returned a wrong read type")
            return self._load_observation(request, observed)
        except Exception:
            return WorkflowRunLoadResult(
                status="error",
                request=request,
                store_result=observed,
                failure=self._failure(
                    "load",
                    "read boundary did not complete",
                    WorkflowPersistenceFailureCode.CODEC_ERROR,
                ),
            )

    def _load_observation(
        self, request: RevisionReadRequest, observed: RevisionReadResult
    ) -> WorkflowRunLoadResult:
        if (
            observed.request_id != request.request_id
            or observed.stream_id != request.stream_id
            or observed.selector is not request.selector
            or (
                observed.requested_revision_id is not None
                and observed.requested_revision_id != request.revision_id
            )
        ):
            return WorkflowRunLoadResult(
                status="error",
                request=request,
                store_result=observed,
                failure=self._failure("load", "substituted shared read response"),
            )
        if observed.status is not RevisionReadStatus.FOUND:
            return WorkflowRunLoadResult(
                status=cast(
                    Literal[
                        "absent",
                        "mismatch",
                        "incompatible",
                        "corrupt",
                        "indeterminate",
                        "error",
                    ],
                    observed.status.value,
                ),
                request=request,
                store_result=observed,
            )
        revision = observed.revision
        assert revision is not None
        if revision.stream_id != request.stream_id or (
            request.selector is RevisionSelector.EXPLICIT_REVISION
            and revision.revision_id != request.revision_id
        ):
            return WorkflowRunLoadResult(
                status="error",
                request=request,
                store_result=observed,
                failure=self._failure("load", "substituted revision address"),
            )
        if request.has_reconciliation_expectations and (
            observed.expectations_matched is not True
        ):
            return WorkflowRunLoadResult(
                status="error",
                request=request,
                store_result=observed,
                failure=self._failure("load", "missing store expectation confirmation"),
            )
        if request.has_reconciliation_expectations and (
            revision.predecessor_revision_id != request.expected_predecessor_revision_id
            or revision.schema_id != request.expected_schema_id
            or revision.content_id != request.expected_content_id
        ):
            return WorkflowRunLoadResult(
                status="corrupt",
                request=request,
                store_result=observed,
                failure=self._failure("load", "confirmed envelope expectations differ"),
            )
        if revision.schema_id != "ksdft2effmass.workflow-run:1":
            return WorkflowRunLoadResult(
                status="incompatible",
                request=request,
                store_result=observed,
                failure=self._failure(
                    "load",
                    "unsupported revision schema",
                    WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                ),
            )
        if revision.content_id != (
            revision.schema_id
            + ":sha256:"
            + hashlib.sha256(revision.payload).hexdigest()
        ):
            return WorkflowRunLoadResult(
                status="corrupt",
                request=request,
                store_result=observed,
                failure=self._failure(
                    "load",
                    "revision content digest differs",
                    WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                ),
            )
        decoded = self.serializer.deserialize(revision.payload)
        if decoded.status != "decoded":
            return WorkflowRunLoadResult(
                status=decoded.status,
                request=request,
                store_result=observed,
                failure=decoded.failure,
            )
        run, binding = decoded.run, decoded.binding
        assert run is not None and binding is not None
        predecessor = run.predecessor_revision_identity
        if (
            run.identity.value != revision.stream_id
            or run.revision_identity.value != revision.revision_id
            or (None if predecessor is None else predecessor.value)
            != revision.predecessor_revision_id
            or (
                request.has_reconciliation_expectations
                and binding.commit_idempotency_identity
                != request.expected_idempotency_id
            )
        ):
            return WorkflowRunLoadResult(
                status="corrupt",
                request=request,
                store_result=observed,
                failure=self._failure("load", "decoded aggregate binding differs"),
            )
        issue = _WorkflowRunStructureValidator().execute(run)
        if issue is not None:
            return WorkflowRunLoadResult(
                status="corrupt",
                request=request,
                store_result=observed,
                failure=self._failure(
                    "load",
                    "aggregate structural closure failed",
                    WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                ),
            )
        return WorkflowRunLoadResult(
            status="loaded",
            request=request,
            store_result=observed,
            snapshot=WorkflowRunSnapshot(run=run, binding=binding, revision=revision),
        )

    def commit(self, transaction: WorkflowRunTransaction) -> WorkflowRunWriteResult:
        """Validate exact bytes and historical extension, then submit one Commit.

        Parameters
        ----------
        transaction
            Exact immutable transaction. A non-genesis predecessor is explicitly read.

        Returns
        -------
        WorkflowRunWriteResult
            Committed with snapshot and newly appended historical claim receipts only
            after exact acknowledgement; otherwise conflict, indeterminate, error,
            invalid or incompatible, without a snapshot or receipt.

        Raises
        ------
        TypeError
            The direct argument is not an exact WorkflowRunTransaction.
        """
        if type(transaction) is not WorkflowRunTransaction:
            raise TypeError("transaction must be WorkflowRunTransaction")
        predecessor_load: WorkflowRunLoadResult | None = None
        observed: CommitResult | None = None
        try:
            predecessor: WorkflowRunSnapshot | None = None
            expected = transaction.expected_predecessor_revision_identity
            if expected is not None:
                predecessor_load = self.load(
                    RevisionReadRequest(
                        request_id=str(uuid4()),
                        stream_id=transaction.run_identity.value,
                        selector=RevisionSelector.EXPLICIT_REVISION,
                        revision_id=expected.value,
                    )
                )
                if predecessor_load.status != "loaded":
                    status: Literal["invalid", "incompatible", "indeterminate", "error"]
                    if predecessor_load.status in (
                        "incompatible",
                        "indeterminate",
                        "error",
                    ):
                        status = predecessor_load.status
                    else:
                        status = "invalid"
                    return WorkflowRunWriteResult(
                        status=status,
                        transaction=transaction,
                        predecessor_load=predecessor_load,
                        failure=predecessor_load.failure
                        or self._failure("commit", "exact predecessor was not loaded"),
                    )
                predecessor = predecessor_load.snapshot
            validation = self.validator.execute(transaction, predecessor)
            if validation.status != "valid":
                return WorkflowRunWriteResult(
                    status=validation.status,
                    transaction=transaction,
                    predecessor_load=predecessor_load,
                    failure=validation.failure,
                )
            # Independently bind the exact transaction to the validated bytes at the
            # submission seam. No detached successful validation can swap a candidate.
            encoded = self.serializer.serialize(
                transaction.candidate, transaction.binding
            )
            if encoded.status != "encoded":
                return WorkflowRunWriteResult(
                    status=encoded.status,
                    transaction=transaction,
                    predecessor_load=predecessor_load,
                    failure=encoded.failure,
                )
            if (
                validation.transaction is not transaction
                or validation.predecessor is not predecessor
                or encoded.encoded != validation.encoded
            ):
                return WorkflowRunWriteResult(
                    status="invalid",
                    transaction=transaction,
                    predecessor_load=predecessor_load,
                    failure=self._failure(
                        "commit", "validation/serialization binding differs"
                    ),
                )
            assert validation.encoded is not None
            wire = validation.encoded
            run = transaction.candidate
            revision = Revision(
                stream_id=transaction.run_identity.value,
                revision_id=run.revision_identity.value,
                predecessor_revision_id=None if expected is None else expected.value,
                schema_id=wire.schema_identity,
                content_id=wire.content_identity,
                payload=wire.payload,
            )
            snapshot = WorkflowRunSnapshot(
                run=run, binding=transaction.binding, revision=revision
            )
            old_claims = (
                () if predecessor is None else predecessor.run.authority_reservations
            )
            old_ids = {claim.identity for claim in old_claims}
            new_claims = tuple(
                claim
                for claim in run.authority_reservations
                if claim.kind is AuthorityReservationOutcomeKind.CLAIMED
                and claim.identity not in old_ids
            )
            if any(
                not self._claim_at_revision(snapshot, claim) for claim in new_claims
            ):
                return WorkflowRunWriteResult(
                    status="invalid",
                    transaction=transaction,
                    predecessor_load=predecessor_load,
                    failure=self._failure(
                        "commit", "new claim does not name candidate revision"
                    ),
                )
            receipts = tuple(self._receipt(snapshot, claim) for claim in new_claims)
            submitted = Commit(
                expected_revision_id=revision.predecessor_revision_id,
                candidate=revision,
                idempotency_id=transaction.commit_idempotency_identity,
            )
            observed = self.store.commit(submitted)
            if type(observed) is not CommitResult:
                observed = None
                raise TypeError("store returned a wrong commit type")
            if (
                observed.stream_id != revision.stream_id
                or observed.idempotency_id != submitted.idempotency_id
                or (
                    observed.status is CommitStatus.COMMITTED
                    and observed.revision != revision
                )
                or (
                    observed.status is CommitStatus.CONFLICT
                    and observed.expected_revision_id != submitted.expected_revision_id
                )
            ):
                return WorkflowRunWriteResult(
                    status="error",
                    transaction=transaction,
                    store_result=observed,
                    predecessor_load=predecessor_load,
                    failure=self._failure(
                        "commit", "substituted shared commit response"
                    ),
                )
            if observed.status is not CommitStatus.COMMITTED:
                return WorkflowRunWriteResult(
                    status=cast(
                        Literal["conflict", "indeterminate", "error"],
                        observed.status.value,
                    ),
                    transaction=transaction,
                    store_result=observed,
                    predecessor_load=predecessor_load,
                )
            return WorkflowRunWriteResult(
                status="committed",
                transaction=transaction,
                store_result=observed,
                predecessor_load=predecessor_load,
                snapshot=snapshot,
                claim_receipts=receipts,
            )
        except Exception:
            return WorkflowRunWriteResult(
                status="error",
                transaction=transaction,
                store_result=observed,
                predecessor_load=predecessor_load,
                failure=self._failure(
                    "commit",
                    "commit boundary did not complete",
                    WorkflowPersistenceFailureCode.CODEC_ERROR,
                ),
            )

    def load_claim(
        self,
        request: RevisionReadRequest,
        claimed_reservation_identity: AuthorityReservationOutcomeIdentity,
    ) -> WorkflowRunClaimLoadResult:
        """Confirm one historical claim through one complete-expectation read.

        Parameters
        ----------
        request
            Explicit revision and complete predecessor/schema/content/key expectations.
            Latest or incomplete requests return error before any store read.
        claimed_reservation_identity
            Exact CLAIMED record in the addressed run and revision.

        Returns
        -------
        WorkflowRunClaimLoadResult
            Same seven read statuses. Missing selected claim is mismatch; malformed or
            copied historical claim is corrupt. Only loaded has a historical receipt.

        Raises
        ------
        TypeError
            Either direct argument has the wrong exact semantic type.
        """
        if type(request) is not RevisionReadRequest:
            raise TypeError("request must be RevisionReadRequest")
        if (
            type(claimed_reservation_identity)
            is not AuthorityReservationOutcomeIdentity
        ):
            raise TypeError(
                "claim selector must be AuthorityReservationOutcomeIdentity"
            )
        if (
            request.selector is not RevisionSelector.EXPLICIT_REVISION
            or not request.has_reconciliation_expectations
        ):
            return WorkflowRunClaimLoadResult(
                status="error",
                request=request,
                claimed_reservation_identity=claimed_reservation_identity,
                failure=self._failure(
                    "load_claim", "complete historical expectations required"
                ),
            )
        loaded = self.load(request)
        if loaded.status != "loaded":
            return WorkflowRunClaimLoadResult(
                status=loaded.status,
                request=request,
                claimed_reservation_identity=claimed_reservation_identity,
                store_result=loaded.store_result,
                failure=loaded.failure,
            )
        snapshot = loaded.snapshot
        assert snapshot is not None
        claim = next(
            (
                record
                for record in snapshot.run.authority_reservations
                if record.identity == claimed_reservation_identity
            ),
            None,
        )
        if claim is None or not self._claim_at_revision(snapshot, claim):
            return WorkflowRunClaimLoadResult(
                status="mismatch" if claim is None else "corrupt",
                request=request,
                claimed_reservation_identity=claimed_reservation_identity,
                store_result=loaded.store_result,
                failure=self._failure(
                    "load_claim", "selected claim absent or not at revision"
                ),
            )
        try:
            receipt = self._receipt(snapshot, claim)
        except Exception:
            return WorkflowRunClaimLoadResult(
                status="error",
                request=request,
                claimed_reservation_identity=claimed_reservation_identity,
                store_result=loaded.store_result,
                failure=self._failure(
                    "load_claim",
                    "receipt derivation did not complete",
                    WorkflowPersistenceFailureCode.CODEC_ERROR,
                ),
            )
        return WorkflowRunClaimLoadResult(
            status="loaded",
            request=request,
            claimed_reservation_identity=claimed_reservation_identity,
            store_result=loaded.store_result,
            snapshot=snapshot,
            receipt=receipt,
        )

    @staticmethod
    def _claim_at_revision(
        snapshot: WorkflowRunSnapshot, claim: AuthorityReservationOutcome
    ) -> bool:
        # Complete authorization/reservation closure was checked by the structural
        # owner. Here bind the selected historical event to this exact revision.
        return (
            claim.kind is AuthorityReservationOutcomeKind.CLAIMED
            and claim.workflow_run_identity == snapshot.run.identity
            and claim.workflow_run_revision_identity == snapshot.run.revision_identity
            and claim.expected_revision_identity
            == snapshot.run.predecessor_revision_identity
            and snapshot.revision.predecessor_revision_id is not None
        )

    @staticmethod
    def _receipt(
        snapshot: WorkflowRunSnapshot, claim: AuthorityReservationOutcome
    ) -> WorkflowRunClaimCommitReceipt:
        binding, revision = snapshot.binding, snapshot.revision
        operation_sequence = [
            "wfr-operation-v1",
            binding.transaction_identity,
            binding.persistence_implementation_identity,
            revision.stream_id,
            revision.revision_id,
            revision.predecessor_revision_id,
            revision.schema_id,
            revision.content_id,
            binding.commit_idempotency_identity,
        ]
        operation = (
            "wfr-operation-v1:sha256:"
            + hashlib.sha256(
                json.dumps(
                    operation_sequence,
                    ensure_ascii=True,
                    separators=(",", ":"),
                    allow_nan=False,
                ).encode("ascii")
            ).hexdigest()
        )
        receipt_sequence = [
            "wfr-claim-receipt-v1",
            operation,
            claim.identity.value,
            claim.authorization_result_identity.value,
        ]
        identity = (
            "wfr-claim-receipt-v1:sha256:"
            + hashlib.sha256(
                json.dumps(
                    receipt_sequence,
                    ensure_ascii=True,
                    separators=(",", ":"),
                    allow_nan=False,
                ).encode("ascii")
            ).hexdigest()
        )
        assert revision.predecessor_revision_id is not None
        return WorkflowRunClaimCommitReceipt(
            identity=WorkflowRunClaimCommitReceiptIdentity(identity),
            workflow_run_identity=WorkflowRunIdentity(revision.stream_id),
            committed_revision_identity=WorkflowRunRevisionIdentity(
                revision.revision_id
            ),
            predecessor_revision_identity=WorkflowRunRevisionIdentity(
                revision.predecessor_revision_id
            ),
            claimed_reservation_identity=claim.identity,
            claim_authorization_result_identity=claim.authorization_result_identity,
            workflow_run_content_identity=revision.content_id,
            persistence_operation_identity=operation,
            commit_idempotency_identity=binding.commit_idempotency_identity,
            persistence_implementation_identity=binding.persistence_implementation_identity,
        )

    @staticmethod
    def _failure(
        phase: str,
        observed: str,
        code: WorkflowPersistenceFailureCode = (
            WorkflowPersistenceFailureCode.IDENTITY_MISMATCH
        ),
    ) -> WorkflowPersistenceFailure:
        return WorkflowPersistenceFailure(
            implementation_identity="ksdft2effmass.workflows.WorkflowRunAtomicRepository:1",
            phase=phase,
            code=code,
            input_identities=(),
            expected="complete correlated domain and store evidence",
            observed=observed,
            diagnostic=observed,
            claim_boundary="no advancement, effect permission or automatic retry",
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


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunSerializer:
    """Explicit complete version-one WorkflowRun wire serializer.

    Parameters
    ----------
    result_codec
        Explicit effect-free, operationally immutable outward result codec. Application
        composition supplies the selected seven-family codec; protocol membership
        alone does not establish concrete support. No registry or inward domain import
        is used.

    Notes
    -----
    The root has exactly ``schema``, ``run`` and ``commit_binding``. Schema is
    ``ksdft2effmass.workflow-run:1``; the historical writer is explicitly recognized as
    ``ksdft2effmass.workflows.WorkflowRunAtomicRepository:1``. Unknown versions are
    incompatible, not inferred legacy representations. Declared reachable fields
    (including null/default/derived fields) use literal field/constructor branches,
    subject to the exact empty-collection omission rule below.
    Records, nominal identities and enums use ``{type, fields}``; tuples are ordered
    arrays. Canonical bytes are sorted compact ASCII JSON without newline. Integers
    use tagged ``hex(int)`` strings (no Boolean coercion or decimal size limit), finite
    floats tagged ``float.hex()`` (preserving binary64 signed zero), bytes canonical
    base64, and UTC timestamps ISO-8601 with six fractional digits and ``+00:00``.

    Within v1, both empty ``nested_invocation_intents`` and
    ``nested_terminal_observations`` are omitted, preserving the original 34-field
    aggregate bytes. If either is nonempty, both keys are required in the 36-field
    extension. Single-key, unknown-field and explicitly both-empty extensions are
    corrupt; no second schema, writer or migration is introduced. A terminal intent
    reference retains its exact new-intent or combined-invocation nominal tag.

    Every result occurrence contains a complete injected-codec envelope. A local
    operation map checks repeated identities, including normalized sources, against
    every envelope field; it is not a type registry or persistent cache. References
    must agree with envelope type/domain/content metadata. Constructor-derived
    identities are reconstructed and compared, never overwritten. Exact re-encoding
    rejects constructor normalization of malformed wire. Allocation/recursion and
    operational failures are sanitized errors without partial values.

    This serializer performs no structural-history validation, replay, authorization,
    native I/O, store operation or receipt derivation. Successful reconstruction proves
    representation only, not scientific validity, provenance truth or effect permission.

    Raises
    ------
    TypeError
        The supplied dependency does not implement the explicit codec port.
    """

    result_codec: WorkflowResultValueCodec

    def __post_init__(self) -> None:
        """Require the explicitly supplied codec without discovering implementations."""
        if not isinstance(self.result_codec, WorkflowResultValueCodec):
            raise TypeError("result_codec must implement WorkflowResultValueCodec")

    def serialize(
        self, run: WorkflowRun, binding: WorkflowRunCommitBinding
    ) -> WorkflowRunEncodeResult:
        """Encode a complete run and its durable transaction/key/writer binding.

        Parameters
        ----------
        run
            Exact immutable WorkflowRun; only schema version one is supported.
        binding
            Exact immutable historical binding included in the content-bound payload.

        Returns
        -------
        WorkflowRunEncodeResult
            Complete bytes/content identity on encoded; incompatible, invalid or
            error with structured evidence and no partial bytes otherwise.

        Raises
        ------
        TypeError
            A direct argument has the wrong exact semantic type.
        """
        if (
            type(run) is not WorkflowRun
            or type(binding) is not WorkflowRunCommitBinding
        ):
            raise TypeError("serialize requires exact WorkflowRun and commit binding")
        inputs = (
            run.identity.value,
            run.revision_identity.value,
            binding.transaction_identity,
        )
        try:
            self._versions(run, binding, "encode")
            wire = self._encode(run, {})
            payload = self._json(self._root(wire, binding))
            reconstructed = self._exact(self._decode(wire, {}), WorkflowRun)
            if (
                self._json(self._root(self._encode(reconstructed, {}), binding))
                != payload
            ):
                raise self._failure(
                    "encode", WorkflowPersistenceFailureCode.CONTENT_MISMATCH
                )
            return WorkflowRunEncodeResult(
                status="encoded",
                encoded=WorkflowEncodedRun(
                    schema_identity="ksdft2effmass.workflow-run:1",
                    content_identity="ksdft2effmass.workflow-run:1:sha256:"
                    + hashlib.sha256(payload).hexdigest(),
                    payload=payload,
                ),
            )
        except _WorkflowRunCodecFailure as error:
            return WorkflowRunEncodeResult(
                status="invalid" if error.status == "corrupt" else error.status,
                failure=self._annotate_failure(error.failure, inputs, "encode"),
            )
        except MemoryError, RecursionError:
            failure = self._failure(
                "encode", WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
            )
        except TypeError, ValueError, OverflowError, KeyError:
            failure = self._failure(
                "encode", WorkflowPersistenceFailureCode.INVARIANT_VIOLATION
            )
        except Exception:
            failure = self._failure(
                "encode", WorkflowPersistenceFailureCode.CODEC_ERROR
            )
        return WorkflowRunEncodeResult(
            status="invalid" if failure.status == "corrupt" else failure.status,
            failure=self._annotate_failure(failure.failure, inputs, "encode"),
        )

    def deserialize(self, payload: bytes) -> WorkflowRunDecodeResult:
        """Decode canonical complete run bytes without checking stored presence.

        Parameters
        ----------
        payload
            Exact immutable ASCII JSON bytes, including the persisted commit binding.

        Returns
        -------
        WorkflowRunDecodeResult
            Complete run/binding on decoded only; incompatible, corrupt or error
            otherwise. Known malformed fields, tags, canonicality and derived identity
            mismatches never yield a partial run.

        Raises
        ------
        TypeError
            Payload is not exact bytes (mutable buffers and text are rejected).
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        inputs: tuple[str, ...] = ()
        try:
            inputs = ("sha256:" + hashlib.sha256(payload).hexdigest(),)
            wire = cast(
                _ResultJson,
                json.loads(
                    payload.decode("ascii"),
                    object_pairs_hook=self._unique_object,
                    parse_int=self._reject_number,
                    parse_float=self._reject_number,
                    parse_constant=self._reject_number,
                ),
            )
            if not isinstance(wire, dict) or set(wire) != {
                "schema",
                "run",
                "commit_binding",
            }:
                raise ValueError("wrong complete root fields")
            schema = self._string(wire["schema"])
            if schema != "ksdft2effmass.workflow-run:1":
                raise self._failure(
                    "decode", WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION
                )
            raw_binding = wire["commit_binding"]
            if not isinstance(raw_binding, dict) or set(raw_binding) != {
                "transaction_identity",
                "commit_idempotency_identity",
                "persistence_implementation_identity",
            }:
                raise ValueError("wrong durable binding fields")
            binding = WorkflowRunCommitBinding(
                transaction_identity=self._string(raw_binding["transaction_identity"]),
                commit_idempotency_identity=self._string(
                    raw_binding["commit_idempotency_identity"]
                ),
                persistence_implementation_identity=self._string(
                    raw_binding["persistence_implementation_identity"]
                ),
            )
            # Known schema canonicality is checked before constructing any domain run.
            if self._json(wire) != payload:
                raise ValueError("noncanonical aggregate bytes")
            run = self._exact(self._decode(wire["run"], {}), WorkflowRun)
            self._versions(run, binding, "decode")
            if self._json(self._root(self._encode(run, {}), binding)) != payload:
                raise self._failure(
                    "decode", WorkflowPersistenceFailureCode.CONTENT_MISMATCH
                )
            return WorkflowRunDecodeResult(status="decoded", run=run, binding=binding)
        except _WorkflowRunCodecFailure as error:
            return WorkflowRunDecodeResult(
                status="corrupt" if error.status == "invalid" else error.status,
                failure=self._annotate_failure(error.failure, inputs, "decode"),
            )
        except MemoryError, RecursionError:
            failure = self._failure(
                "decode", WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT
            )
        except TypeError, ValueError, OverflowError, KeyError:
            failure = self._failure(
                "decode", WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION
            )
        except Exception:
            failure = self._failure(
                "decode", WorkflowPersistenceFailureCode.CODEC_ERROR
            )
        return WorkflowRunDecodeResult(
            status="corrupt" if failure.status == "invalid" else failure.status,
            failure=self._annotate_failure(failure.failure, inputs, "decode"),
        )

    @staticmethod
    def _annotate_failure(
        failure: WorkflowPersistenceFailure, inputs: tuple[str, ...], phase: str
    ) -> WorkflowPersistenceFailure:
        if (
            failure.implementation_identity
            == "ksdft2effmass.workflows.WorkflowRunSerializer:1"
        ):
            return replace(failure, input_identities=inputs, phase=phase)
        return failure

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

    def _versions(
        self, run: WorkflowRun, binding: WorkflowRunCommitBinding, phase: str
    ) -> None:
        if (
            run.schema_version != 1
            or binding.persistence_implementation_identity
            != "ksdft2effmass.workflows.WorkflowRunAtomicRepository:1"
        ):
            raise self._failure(
                phase, WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION
            )

    @staticmethod
    def _root(run: _ResultJson, binding: WorkflowRunCommitBinding) -> _ResultJson:
        return {
            "schema": "ksdft2effmass.workflow-run:1",
            "run": run,
            "commit_binding": {
                "transaction_identity": binding.transaction_identity,
                "commit_idempotency_identity": binding.commit_idempotency_identity,
                "persistence_implementation_identity": (
                    binding.persistence_implementation_identity
                ),
            },
        }

    @staticmethod
    def _json(value: _ResultJson) -> bytes:
        return json.dumps(
            value,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("ascii")

    @staticmethod
    def _unique_object(pairs: list[tuple[str, _ResultJson]]) -> dict[str, _ResultJson]:
        """Own json's exact object-pairs hook with duplicate-member rejection."""
        result: dict[str, _ResultJson] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate member")
            result[key] = value
        return result

    @staticmethod
    def _reject_number(token: str) -> Never:
        """Own json's numeric hooks; numbers must use the explicit scalar grammar."""
        raise ValueError("raw numeric token")

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

    def _encode(
        self, value: _RunValue, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _ResultJson:
        if value is None:
            return None
        if type(value) is bool:
            return value
        if type(value) is str:
            return value
        if type(value) is int:
            return self._record("int", {"value": hex(value)})
        if type(value) is float:
            if not math.isfinite(value):
                raise ValueError("nonfinite float")
            return self._record("float", {"value": value.hex()})
        if type(value) is bytes:
            return self._record(
                "bytes", {"value": base64.b64encode(value).decode("ascii")}
            )
        if type(value) is datetime:
            if value.tzinfo is None or value.utcoffset() != timedelta(0):
                raise ValueError("timestamp must be UTC")
            return self._record(
                "datetime",
                {"value": value.astimezone(UTC).isoformat(timespec="microseconds")},
            )
        if type(value) is tuple:
            return [self._encode(item, seen) for item in value]
        if type(value) is AuthorityReservationOutcomeKind:
            return self._record(
                "AuthorityReservationOutcomeKind", {"value": value.value}
            )
        if type(value) is ColoredPetriNetEnablementFailureCode:
            return self._record(
                "ColoredPetriNetEnablementFailureCode", {"value": value.value}
            )
        if type(value) is ColoredPetriNetFiringFailureCode:
            return self._record(
                "ColoredPetriNetFiringFailureCode", {"value": value.value}
            )
        if type(value) is ColoredPetriNetFiringOutcomeKind:
            return self._record(
                "ColoredPetriNetFiringOutcomeKind", {"value": value.value}
            )
        if type(value) is ColoredPetriNetGuardOperator:
            return self._record("ColoredPetriNetGuardOperator", {"value": value.value})
        if type(value) is ColoredPetriNetInputMode:
            return self._record("ColoredPetriNetInputMode", {"value": value.value})
        if type(value) is ColoredPetriNetSelectionFailureCode:
            return self._record(
                "ColoredPetriNetSelectionFailureCode", {"value": value.value}
            )
        if type(value) is ColoredPetriNetSelectionOutcomeKind:
            return self._record(
                "ColoredPetriNetSelectionOutcomeKind", {"value": value.value}
            )
        if type(value) is ColoredPetriNetSelectionPolicy:
            return self._record(
                "ColoredPetriNetSelectionPolicy", {"value": value.value}
            )
        if type(value) is ColoredPetriNetValidationIssueCode:
            return self._record(
                "ColoredPetriNetValidationIssueCode", {"value": value.value}
            )
        if type(value) is ColoredPetriNetValueExpressionKind:
            return self._record(
                "ColoredPetriNetValueExpressionKind", {"value": value.value}
            )
        if type(value) is ColoredPetriNetValueKind:
            return self._record("ColoredPetriNetValueKind", {"value": value.value})
        if type(value) is DispatchObservationKind:
            return self._record("DispatchObservationKind", {"value": value.value})
        if type(value) is DispatchOutcomeKind:
            return self._record("DispatchOutcomeKind", {"value": value.value})
        if type(value) is NestedWorkflowInvocationKind:
            return self._record("NestedWorkflowInvocationKind", {"value": value.value})
        if type(value) is ObligationDispositionKind:
            return self._record("ObligationDispositionKind", {"value": value.value})
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
        if type(value) is TaskAttemptStatus:
            return self._record("TaskAttemptStatus", {"value": value.value})
        if type(value) is TaskInvocationOutcomeKind:
            return self._record("TaskInvocationOutcomeKind", {"value": value.value})
        if type(value) is TaskStartGateSetMode:
            return self._record("TaskStartGateSetMode", {"value": value.value})
        if type(value) is AllOfTaskActivationSelection:
            return self._record(
                "AllOfTaskActivationSelection",
                {
                    "gate_set_identity": self._encode(value.gate_set_identity, seen),
                    "selected_gates": self._encode(value.selected_gates, seen),
                    "selection_result_identity": self._encode(
                        value.selection_result_identity, seen
                    ),
                },
            )
        if type(value) is AnyOfTaskActivationSelection:
            return self._record(
                "AnyOfTaskActivationSelection",
                {
                    "gate_set_identity": self._encode(value.gate_set_identity, seen),
                    "selected_gate": self._encode(value.selected_gate, seen),
                    "selection_result_identity": self._encode(
                        value.selection_result_identity, seen
                    ),
                },
            )
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
        if type(value) is AttemptIdentity:
            return self._record(
                "AttemptIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
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
        if type(value) is ChildWorkflowCreationIdempotencyIdentity:
            return self._record(
                "ChildWorkflowCreationIdempotencyIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetArcDefinition:
            return self._record(
                "ColoredPetriNetArcDefinition",
                {
                    "identity": self._encode(value.identity, seen),
                    "place_identity": self._encode(value.place_identity, seen),
                    "transition_identity": self._encode(
                        value.transition_identity, seen
                    ),
                    "input_inscription": self._encode(value.input_inscription, seen),
                    "output_inscription": self._encode(value.output_inscription, seen),
                },
            )
        if type(value) is ColoredPetriNetArcIdentity:
            return self._record(
                "ColoredPetriNetArcIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetBinding:
            return self._record(
                "ColoredPetriNetBinding",
                {
                    "transition_identity": self._encode(
                        value.transition_identity, seen
                    ),
                    "assignments": self._encode(value.assignments, seen),
                },
            )
        if type(value) is ColoredPetriNetBindingAssignment:
            return self._record(
                "ColoredPetriNetBindingAssignment",
                {
                    "variable_identity": self._encode(value.variable_identity, seen),
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetBindingSelectorIdentity:
            return self._record(
                "ColoredPetriNetBindingSelectorIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetBindingVariableIdentity:
            return self._record(
                "ColoredPetriNetBindingVariableIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetColorDefinition:
            return self._record(
                "ColoredPetriNetColorDefinition",
                {
                    "identity": self._encode(value.identity, seen),
                    "allowed_value_kinds": self._encode(
                        value.allowed_value_kinds, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetColorIdentity:
            return self._record(
                "ColoredPetriNetColorIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetDefinition:
            return self._record(
                "ColoredPetriNetDefinition",
                {
                    "identity": self._encode(value.identity, seen),
                    "colors": self._encode(value.colors, seen),
                    "places": self._encode(value.places, seen),
                    "transitions": self._encode(value.transitions, seen),
                    "arcs": self._encode(value.arcs, seen),
                    "transition_priority": self._encode(
                        value.transition_priority, seen
                    ),
                    "selection_policy": self._encode(value.selection_policy, seen),
                },
            )
        if type(value) is ColoredPetriNetDefinitionIdentity:
            return self._record(
                "ColoredPetriNetDefinitionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetEnablementFailure:
            return self._record(
                "ColoredPetriNetEnablementFailure",
                {
                    "identity": self._encode(value.identity, seen),
                    "code": self._encode(value.code, seen),
                    "operation_phase": self._encode(value.operation_phase, seen),
                    "expected_condition": self._encode(value.expected_condition, seen),
                    "observed_condition": self._encode(value.observed_condition, seen),
                    "diagnostic": self._encode(value.diagnostic, seen),
                    "validation_issues": self._encode(value.validation_issues, seen),
                    "claim_boundary": self._encode(value.claim_boundary, seen),
                },
            )
        if type(value) is ColoredPetriNetEnablementFailureIdentity:
            return self._record(
                "ColoredPetriNetEnablementFailureIdentity",
                {
                    "result_identity": self._encode(value.result_identity, seen),
                },
            )
        if type(value) is ColoredPetriNetEnablementResult:
            return self._record(
                "ColoredPetriNetEnablementResult",
                {
                    "identity": self._encode(value.identity, seen),
                    "definition_identity": self._encode(
                        value.definition_identity, seen
                    ),
                    "selection_policy": self._encode(value.selection_policy, seen),
                    "marking_identity": self._encode(value.marking_identity, seen),
                    "expression_evaluator_identity": self._encode(
                        value.expression_evaluator_identity, seen
                    ),
                    "ordering_policy_identity": self._encode(
                        value.ordering_policy_identity, seen
                    ),
                    "transition_enabler_identity": self._encode(
                        value.transition_enabler_identity, seen
                    ),
                    "enabled_bindings": self._encode(value.enabled_bindings, seen),
                    "failure": self._encode(value.failure, seen),
                },
            )
        if type(value) is ColoredPetriNetEnablementResultIdentity:
            return self._record(
                "ColoredPetriNetEnablementResultIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetExpressionEvaluatorIdentity:
            return self._record(
                "ColoredPetriNetExpressionEvaluatorIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetFiringAudit:
            return self._record(
                "ColoredPetriNetFiringAudit",
                {
                    "consumed_occurrences": self._encode(
                        value.consumed_occurrences, seen
                    ),
                    "read_occurrences": self._encode(value.read_occurrences, seen),
                    "inhibitor_evaluations": self._encode(
                        value.inhibitor_evaluations, seen
                    ),
                    "produced_tokens": self._encode(value.produced_tokens, seen),
                    "firer_identity": self._encode(value.firer_identity, seen),
                },
            )
        if type(value) is ColoredPetriNetFiringFailure:
            return self._record(
                "ColoredPetriNetFiringFailure",
                {
                    "identity": self._encode(value.identity, seen),
                    "code": self._encode(value.code, seen),
                    "operation_phase": self._encode(value.operation_phase, seen),
                    "expected_condition": self._encode(value.expected_condition, seen),
                    "observed_condition": self._encode(value.observed_condition, seen),
                    "diagnostic": self._encode(value.diagnostic, seen),
                    "validation_issues": self._encode(value.validation_issues, seen),
                    "claim_boundary": self._encode(value.claim_boundary, seen),
                },
            )
        if type(value) is ColoredPetriNetFiringFailureIdentity:
            return self._record(
                "ColoredPetriNetFiringFailureIdentity",
                {
                    "result_identity": self._encode(value.result_identity, seen),
                },
            )
        if type(value) is ColoredPetriNetFiringInput:
            return self._record(
                "ColoredPetriNetFiringInput",
                {
                    "definition": self._encode(value.definition, seen),
                    "transition_identity": self._encode(
                        value.transition_identity, seen
                    ),
                    "predecessor_marking": self._encode(
                        value.predecessor_marking, seen
                    ),
                    "enablement_result": self._encode(value.enablement_result, seen),
                    "selection_result": self._encode(value.selection_result, seen),
                    "selected_binding": self._encode(value.selected_binding, seen),
                    "directive_identity": self._encode(value.directive_identity, seen),
                    "external_output_binding": self._encode(
                        value.external_output_binding, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetFiringResult:
            return self._record(
                "ColoredPetriNetFiringResult",
                {
                    "identity": self._encode(value.identity, seen),
                    "firing_input": self._encode(value.firing_input, seen),
                    "outcome": self._encode(value.outcome, seen),
                    "successor_marking": self._encode(value.successor_marking, seen),
                    "audit": self._encode(value.audit, seen),
                    "failure": self._encode(value.failure, seen),
                },
            )
        if type(value) is ColoredPetriNetFiringResultIdentity:
            return self._record(
                "ColoredPetriNetFiringResultIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetGuardExpression:
            return self._record(
                "ColoredPetriNetGuardExpression",
                {
                    "operator": self._encode(value.operator, seen),
                    "operands": self._encode(value.operands, seen),
                    "left": self._encode(value.left, seen),
                    "right": self._encode(value.right, seen),
                },
            )
        if type(value) is ColoredPetriNetInhibitorEvaluation:
            return self._record(
                "ColoredPetriNetInhibitorEvaluation",
                {
                    "arc_identity": self._encode(value.arc_identity, seen),
                    "place_identity": self._encode(value.place_identity, seen),
                    "pattern_index": self._encode(value.pattern_index, seen),
                    "matching_count": self._encode(value.matching_count, seen),
                },
            )
        if type(value) is ColoredPetriNetInhibitorPattern:
            return self._record(
                "ColoredPetriNetInhibitorPattern",
                {
                    "allowed_color_identities": self._encode(
                        value.allowed_color_identities, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetInputInscription:
            return self._record(
                "ColoredPetriNetInputInscription",
                {
                    "mode": self._encode(value.mode, seen),
                    "patterns": self._encode(value.patterns, seen),
                },
            )
        if type(value) is ColoredPetriNetMarking:
            return self._record(
                "ColoredPetriNetMarking",
                {
                    "identity": self._encode(value.identity, seen),
                    "definition_identity": self._encode(
                        value.definition_identity, seen
                    ),
                    "places": self._encode(value.places, seen),
                },
            )
        if type(value) is ColoredPetriNetMarkingIdentity:
            return self._record(
                "ColoredPetriNetMarkingIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetOrderingPolicyIdentity:
            return self._record(
                "ColoredPetriNetOrderingPolicyIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetOutputInscription:
            return self._record(
                "ColoredPetriNetOutputInscription",
                {
                    "templates": self._encode(value.templates, seen),
                },
            )
        if type(value) is ColoredPetriNetPlaceDefinition:
            return self._record(
                "ColoredPetriNetPlaceDefinition",
                {
                    "identity": self._encode(value.identity, seen),
                    "allowed_color_identities": self._encode(
                        value.allowed_color_identities, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetPlaceIdentity:
            return self._record(
                "ColoredPetriNetPlaceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetPlaceMarking:
            return self._record(
                "ColoredPetriNetPlaceMarking",
                {
                    "place_identity": self._encode(value.place_identity, seen),
                    "tokens": self._encode(value.tokens, seen),
                },
            )
        if type(value) is ColoredPetriNetProducedToken:
            return self._record(
                "ColoredPetriNetProducedToken",
                {
                    "arc_identity": self._encode(value.arc_identity, seen),
                    "place_identity": self._encode(value.place_identity, seen),
                    "template_index": self._encode(value.template_index, seen),
                    "token": self._encode(value.token, seen),
                },
            )
        if type(value) is ColoredPetriNetSelectionDirective:
            return self._record(
                "ColoredPetriNetSelectionDirective",
                {
                    "enablement_result_identity": self._encode(
                        value.enablement_result_identity, seen
                    ),
                    "binding": self._encode(value.binding, seen),
                    "identity": self._encode(value.identity, seen),
                },
            )
        if type(value) is ColoredPetriNetSelectionDirectiveIdentity:
            return self._record(
                "ColoredPetriNetSelectionDirectiveIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetSelectionResult:
            return self._record(
                "ColoredPetriNetSelectionResult",
                {
                    "enablement_result_identity": self._encode(
                        value.enablement_result_identity, seen
                    ),
                    "selector_identity": self._encode(value.selector_identity, seen),
                    "ordering_policy_identity": self._encode(
                        value.ordering_policy_identity, seen
                    ),
                    "outcome": self._encode(value.outcome, seen),
                    "selected_binding": self._encode(value.selected_binding, seen),
                    "directive": self._encode(value.directive, seen),
                    "failure_code": self._encode(value.failure_code, seen),
                    "identity": self._encode(value.identity, seen),
                },
            )
        if type(value) is ColoredPetriNetSelectionResultIdentity:
            return self._record(
                "ColoredPetriNetSelectionResultIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetToken:
            return self._record(
                "ColoredPetriNetToken",
                {
                    "color_identity": self._encode(value.color_identity, seen),
                    "value": self._encode(value.value, seen),
                    "token_identity": self._encode(value.token_identity, seen),
                },
            )
        if type(value) is ColoredPetriNetTokenIdentity:
            return self._record(
                "ColoredPetriNetTokenIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetTokenOccurrence:
            return self._record(
                "ColoredPetriNetTokenOccurrence",
                {
                    "arc_identity": self._encode(value.arc_identity, seen),
                    "place_identity": self._encode(value.place_identity, seen),
                    "pattern_index": self._encode(value.pattern_index, seen),
                    "occurrence_ordinal": self._encode(value.occurrence_ordinal, seen),
                    "token": self._encode(value.token, seen),
                },
            )
        if type(value) is ColoredPetriNetTokenPattern:
            return self._record(
                "ColoredPetriNetTokenPattern",
                {
                    "variable_identity": self._encode(value.variable_identity, seen),
                    "allowed_color_identities": self._encode(
                        value.allowed_color_identities, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetTokenTemplate:
            return self._record(
                "ColoredPetriNetTokenTemplate",
                {
                    "color_identity": self._encode(value.color_identity, seen),
                    "value_expression": self._encode(value.value_expression, seen),
                    "token_identity_expression": self._encode(
                        value.token_identity_expression, seen
                    ),
                },
            )
        if type(value) is ColoredPetriNetTransitionDefinition:
            return self._record(
                "ColoredPetriNetTransitionDefinition",
                {
                    "identity": self._encode(value.identity, seen),
                    "input_variable_identities": self._encode(
                        value.input_variable_identities, seen
                    ),
                    "external_output_variable_identities": self._encode(
                        value.external_output_variable_identities, seen
                    ),
                    "guard": self._encode(value.guard, seen),
                },
            )
        if type(value) is ColoredPetriNetTransitionEnablerIdentity:
            return self._record(
                "ColoredPetriNetTransitionEnablerIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetTransitionFirerIdentity:
            return self._record(
                "ColoredPetriNetTransitionFirerIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetTransitionIdentity:
            return self._record(
                "ColoredPetriNetTransitionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetValidationIssue:
            return self._record(
                "ColoredPetriNetValidationIssue",
                {
                    "code": self._encode(value.code, seen),
                    "path": self._encode(value.path, seen),
                    "related_identities": self._encode(value.related_identities, seen),
                    "message": self._encode(value.message, seen),
                },
            )
        if type(value) is ColoredPetriNetValue:
            return self._record(
                "ColoredPetriNetValue",
                {
                    "kind": self._encode(value.kind, seen),
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is ColoredPetriNetValueExpression:
            return self._record(
                "ColoredPetriNetValueExpression",
                {
                    "kind": self._encode(value.kind, seen),
                    "literal": self._encode(value.literal, seen),
                    "variable_identity": self._encode(value.variable_identity, seen),
                },
            )
        if type(value) is DirectTaskActivationSelection:
            return self._record(
                "DirectTaskActivationSelection",
                {
                    "selection_result_identity": self._encode(
                        value.selection_result_identity, seen
                    ),
                },
            )
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
        if type(value) is OperationIdentity:
            return self._record(
                "OperationIdentity",
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
        if type(value) is TaskActivation:
            return self._record(
                "TaskActivation",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "task_instance": self._encode(value.task_instance, seen),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "inputs": self._encode(value.inputs, seen),
                    "selection": self._encode(value.selection, seen),
                },
            )
        if type(value) is TaskActivationIdentity:
            return self._record(
                "TaskActivationIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskAttempt:
            return self._record(
                "TaskAttempt",
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
                    "status": self._encode(value.status, seen),
                    "predecessor_attempt_record_identity": self._encode(
                        value.predecessor_attempt_record_identity, seen
                    ),
                    "retry_of_attempt_identity": self._encode(
                        value.retry_of_attempt_identity, seen
                    ),
                    "child_workflow_run_identity": self._encode(
                        value.child_workflow_run_identity, seen
                    ),
                },
            )
        if type(value) is TaskAttemptRecordIdentity:
            return self._record(
                "TaskAttemptRecordIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskDefinitionIdentity:
            return self._record(
                "TaskDefinitionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskFailureRecord:
            return self._record(
                "TaskFailureRecord",
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
                    "failure": self._encode(value.failure, seen),
                    "request_identity": self._encode(value.request_identity, seen),
                    "child_workflow_run_identity": self._encode(
                        value.child_workflow_run_identity, seen
                    ),
                    "claim_boundary": self._encode(value.claim_boundary, seen),
                },
            )
        if type(value) is TaskFailureRecordIdentity:
            return self._record(
                "TaskFailureRecordIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskGateSelection:
            return self._record(
                "TaskGateSelection",
                {
                    "gate_identity": self._encode(value.gate_identity, seen),
                    "binding": self._encode(value.binding, seen),
                },
            )
        if type(value) is TaskInputBinding:
            return self._record(
                "TaskInputBinding",
                {
                    "name": self._encode(value.name, seen),
                    "result": self._encode(value.result, seen),
                },
            )
        if type(value) is TaskInstance:
            return self._record(
                "TaskInstance",
                {
                    "identity": self._encode(value.identity, seen),
                    "definition_identity": self._encode(
                        value.definition_identity, seen
                    ),
                    "start_gate_set": self._encode(value.start_gate_set, seen),
                },
            )
        if type(value) is TaskInstanceIdentity:
            return self._record(
                "TaskInstanceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskInvocationFailure:
            return self._record(
                "TaskInvocationFailure",
                {
                    "identity": self._encode(value.identity, seen),
                    "code": self._encode(value.code, seen),
                    "operation_phase": self._encode(value.operation_phase, seen),
                    "diagnostic": self._encode(value.diagnostic, seen),
                    "retryable": self._encode(value.retryable, seen),
                    "claim_boundary": self._encode(value.claim_boundary, seen),
                },
            )
        if type(value) is TaskInvocationFailureIdentity:
            return self._record(
                "TaskInvocationFailureIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskInvocationOutcome:
            return self._record(
                "TaskInvocationOutcome",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "terminal_attempt_record_identity": self._encode(
                        value.terminal_attempt_record_identity, seen
                    ),
                    "kind": self._encode(value.kind, seen),
                    "results": self._encode(value.results, seen),
                    "production_record_identities": self._encode(
                        value.production_record_identities, seen
                    ),
                    "failure_record_identity": self._encode(
                        value.failure_record_identity, seen
                    ),
                    "dispatch_outcome_record_identity": self._encode(
                        value.dispatch_outcome_record_identity, seen
                    ),
                    "reconciliation_identity_values": self._encode(
                        value.reconciliation_identity_values, seen
                    ),
                },
            )
        if type(value) is TaskInvocationOutcomeIdentity:
            return self._record(
                "TaskInvocationOutcomeIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskStartGate:
            return self._record(
                "TaskStartGate",
                {
                    "identity": self._encode(value.identity, seen),
                    "priority": self._encode(value.priority, seen),
                    "transition_identity": self._encode(
                        value.transition_identity, seen
                    ),
                },
            )
        if type(value) is TaskStartGateIdentity:
            return self._record(
                "TaskStartGateIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskStartGateSet:
            return self._record(
                "TaskStartGateSet",
                {
                    "identity": self._encode(value.identity, seen),
                    "mode": self._encode(value.mode, seen),
                    "gates": self._encode(value.gates, seen),
                },
            )
        if type(value) is TaskStartGateSetIdentity:
            return self._record(
                "TaskStartGateSetIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskWorkflowMembership:
            return self._record(
                "TaskWorkflowMembership",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
                    "task_instance_identity": self._encode(
                        value.task_instance_identity, seen
                    ),
                },
            )
        if type(value) is TaskWorkflowMembershipIdentity:
            return self._record(
                "TaskWorkflowMembershipIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskWorkflowTransitionRecord:
            return self._record(
                "TaskWorkflowTransitionRecord",
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
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "terminal_attempt_record_identity": self._encode(
                        value.terminal_attempt_record_identity, seen
                    ),
                    "outcome_identity": self._encode(value.outcome_identity, seen),
                    "result_production_identities": self._encode(
                        value.result_production_identities, seen
                    ),
                    "firing_result": self._encode(value.firing_result, seen),
                    "request_correlation_identity": self._encode(
                        value.request_correlation_identity, seen
                    ),
                    "dispatch_outcome_record_identity": self._encode(
                        value.dispatch_outcome_record_identity, seen
                    ),
                },
            )
        if type(value) is TaskWorkflowTransitionRecordIdentity:
            return self._record(
                "TaskWorkflowTransitionRecordIdentity",
                {
                    "value": self._encode(value.value, seen),
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
        if type(value) is WorkflowDefinitionReferenceIdentity:
            return self._record(
                "WorkflowDefinitionReferenceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowIdentity:
            return self._record(
                "WorkflowIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowRun:
            return self._record(
                "WorkflowRun",
                {
                    "identity": self._encode(value.identity, seen),
                    "revision_identity": self._encode(value.revision_identity, seen),
                    "predecessor_revision_identity": self._encode(
                        value.predecessor_revision_identity, seen
                    ),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
                    "definition_reference_identity": self._encode(
                        value.definition_reference_identity, seen
                    ),
                    "runtime_bundle_identity": self._encode(
                        value.runtime_bundle_identity, seen
                    ),
                    "schema_version": self._encode(value.schema_version, seen),
                    "adapter_implementation_identity": self._encode(
                        value.adapter_implementation_identity, seen
                    ),
                    "task_instances": self._encode(value.task_instances, seen),
                    "task_memberships": self._encode(value.task_memberships, seen),
                    "nested_memberships": self._encode(value.nested_memberships, seen),
                    "nested_invocations": self._encode(value.nested_invocations, seen),
                    **(
                        {
                            "nested_invocation_intents": self._encode(
                                value.nested_invocation_intents, seen
                            ),
                            "nested_terminal_observations": self._encode(
                                value.nested_terminal_observations, seen
                            ),
                        }
                        if value.nested_invocation_intents
                        or value.nested_terminal_observations
                        else {}
                    ),
                    "activations": self._encode(value.activations, seen),
                    "attempts": self._encode(value.attempts, seen),
                    "outcomes": self._encode(value.outcomes, seen),
                    "result_references": self._encode(value.result_references, seen),
                    "result_productions": self._encode(value.result_productions, seen),
                    "native_output_admissions": self._encode(
                        value.native_output_admissions, seen
                    ),
                    "result_dependencies": self._encode(
                        value.result_dependencies, seen
                    ),
                    "failures": self._encode(value.failures, seen),
                    "authorization_results": self._encode(
                        value.authorization_results, seen
                    ),
                    "authority_references": self._encode(
                        value.authority_references, seen
                    ),
                    "execution_request_correlations": self._encode(
                        value.execution_request_correlations, seen
                    ),
                    "authority_reservations": self._encode(
                        value.authority_reservations, seen
                    ),
                    "dispatch_obligations": self._encode(
                        value.dispatch_obligations, seen
                    ),
                    "dispatch_entries": self._encode(value.dispatch_entries, seen),
                    "dispatch_observations": self._encode(
                        value.dispatch_observations, seen
                    ),
                    "dispatch_outcomes": self._encode(value.dispatch_outcomes, seen),
                    "obligation_dispositions": self._encode(
                        value.obligation_dispositions, seen
                    ),
                    "scientific_decision_requests": self._encode(
                        value.scientific_decision_requests, seen
                    ),
                    "scientific_decision_resolutions": self._encode(
                        value.scientific_decision_resolutions, seen
                    ),
                    "initial_marking": self._encode(value.initial_marking, seen),
                    "current_marking": self._encode(value.current_marking, seen),
                    "transitions": self._encode(value.transitions, seen),
                },
            )
        if type(value) is WorkflowRunIdentity:
            return self._record(
                "WorkflowRunIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowRunReplayResultIdentity:
            return self._record(
                "WorkflowRunReplayResultIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowRunRevisionIdentity:
            return self._record(
                "WorkflowRunRevisionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowRuntimeBundleIdentity:
            return self._record(
                "WorkflowRuntimeBundleIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowTransitionSequenceIdentity:
            return self._record(
                "WorkflowTransitionSequenceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if (
            isinstance(value, ResultObject)
            and type(value.identity) is ResultObjectIdentity
        ):
            return self._result_wire(self._encode_result(value, seen))
        raise self._failure("encode", WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE)

    def _decode(
        self, wire: _ResultJson, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _RunValue:
        if wire is None:
            return None
        if type(wire) is bool:
            return wire
        if type(wire) is str:
            return wire
        if isinstance(wire, list):
            return tuple(self._decode(item, seen) for item in wire)
        if not isinstance(wire, dict) or set(wire) != {"type", "fields"}:
            raise ValueError("wrong tagged value shape")
        tag = self._string(wire["type"])
        if tag == "int":
            text = self._string(self._fields(wire, "int", ("value",))["value"])
            number = int(text, 16)
            if hex(number) != text:
                raise ValueError("noncanonical signed hexadecimal integer")
            return number
        if tag == "float":
            text = self._string(self._fields(wire, "float", ("value",))["value"])
            real = float.fromhex(text)
            if not math.isfinite(real) or real.hex() != text:
                raise ValueError("noncanonical finite binary64")
            return real
        if tag == "bytes":
            text = self._string(self._fields(wire, "bytes", ("value",))["value"])
            payload = base64.b64decode(text, validate=True)
            if base64.b64encode(payload).decode("ascii") != text:
                raise ValueError("noncanonical base64")
            return payload
        if tag == "datetime":
            text = self._string(self._fields(wire, "datetime", ("value",))["value"])
            instant = datetime.fromisoformat(text)
            if (
                instant.tzinfo is None
                or instant.utcoffset() != timedelta(0)
                or instant.isoformat(timespec="microseconds") != text
            ):
                raise ValueError("noncanonical UTC microsecond timestamp")
            return instant
        if tag == "WorkflowEncodedResultValue":
            fields = self._fields(
                wire,
                tag,
                (
                    "result_identity",
                    "concrete_type_identity",
                    "owning_domain_identity",
                    "schema_identity",
                    "content_identity",
                    "payload",
                    "payload_digest",
                ),
            )
            envelope = WorkflowEncodedResultValue(
                result_identity=self._exact(
                    self._decode(fields["result_identity"], seen), ResultObjectIdentity
                ),
                concrete_type_identity=self._exact(
                    self._decode(fields["concrete_type_identity"], seen),
                    ResultObjectTypeIdentity,
                ),
                owning_domain_identity=self._exact(
                    self._decode(fields["owning_domain_identity"], seen),
                    ResultObjectDomainIdentity,
                ),
                schema_identity=self._string(fields["schema_identity"]),
                content_identity=self._exact(
                    self._decode(fields["content_identity"], seen),
                    ResultObjectContentIdentity,
                ),
                payload=self._exact(self._decode(fields["payload"], seen), bytes),
                payload_digest=self._string(fields["payload_digest"]),
            )
            return self._decode_result(envelope, seen)
        if tag == "AuthorityReservationOutcomeKind":
            return AuthorityReservationOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetEnablementFailureCode":
            return ColoredPetriNetEnablementFailureCode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetFiringFailureCode":
            return ColoredPetriNetFiringFailureCode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetFiringOutcomeKind":
            return ColoredPetriNetFiringOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetGuardOperator":
            return ColoredPetriNetGuardOperator(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetInputMode":
            return ColoredPetriNetInputMode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetSelectionFailureCode":
            return ColoredPetriNetSelectionFailureCode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetSelectionOutcomeKind":
            return ColoredPetriNetSelectionOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetSelectionPolicy":
            return ColoredPetriNetSelectionPolicy(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetValidationIssueCode":
            return ColoredPetriNetValidationIssueCode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetValueExpressionKind":
            return ColoredPetriNetValueExpressionKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ColoredPetriNetValueKind":
            return ColoredPetriNetValueKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "DispatchObservationKind":
            return DispatchObservationKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "DispatchOutcomeKind":
            return DispatchOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "NestedWorkflowInvocationKind":
            return NestedWorkflowInvocationKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "ObligationDispositionKind":
            return ObligationDispositionKind(
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
        if tag == "TaskAttemptStatus":
            return TaskAttemptStatus(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "TaskInvocationOutcomeKind":
            return TaskInvocationOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "TaskStartGateSetMode":
            return TaskStartGateSetMode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        record: _RunValue
        if tag == "AllOfTaskActivationSelection":
            fields = self._fields(
                wire,
                tag,
                ("gate_set_identity", "selected_gates", "selection_result_identity"),
            )
            record = AllOfTaskActivationSelection(
                gate_set_identity=self._exact(
                    self._decode(fields["gate_set_identity"], seen),
                    TaskStartGateSetIdentity,
                ),
                selected_gates=tuple(
                    self._exact(item, TaskGateSelection)
                    for item in self._items(
                        self._decode(fields["selected_gates"], seen)
                    )
                ),
                selection_result_identity=self._exact(
                    self._decode(fields["selection_result_identity"], seen),
                    ColoredPetriNetSelectionResultIdentity,
                ),
            )
            return record
        if tag == "AnyOfTaskActivationSelection":
            fields = self._fields(
                wire,
                tag,
                ("gate_set_identity", "selected_gate", "selection_result_identity"),
            )
            record = AnyOfTaskActivationSelection(
                gate_set_identity=self._exact(
                    self._decode(fields["gate_set_identity"], seen),
                    TaskStartGateSetIdentity,
                ),
                selected_gate=self._exact(
                    self._decode(fields["selected_gate"], seen), TaskGateSelection
                ),
                selection_result_identity=self._exact(
                    self._decode(fields["selection_result_identity"], seen),
                    ColoredPetriNetSelectionResultIdentity,
                ),
            )
            return record
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
        if tag == "AttemptIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = AttemptIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
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
        if tag == "ChildWorkflowCreationIdempotencyIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ChildWorkflowCreationIdempotencyIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetArcDefinition":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "place_identity",
                    "transition_identity",
                    "input_inscription",
                    "output_inscription",
                ),
            )
            record = ColoredPetriNetArcDefinition(
                identity=self._exact(
                    self._decode(fields["identity"], seen), ColoredPetriNetArcIdentity
                ),
                place_identity=self._exact(
                    self._decode(fields["place_identity"], seen),
                    ColoredPetriNetPlaceIdentity,
                ),
                transition_identity=self._exact(
                    self._decode(fields["transition_identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
                input_inscription=self._parse_ColoredPetriNetArcDefinition_input_inscription(
                    self._decode(fields["input_inscription"], seen)
                ),
                output_inscription=self._parse_ColoredPetriNetArcDefinition_output_inscription(
                    self._decode(fields["output_inscription"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetArcIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetArcIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetBinding":
            fields = self._fields(wire, tag, ("transition_identity", "assignments"))
            record = ColoredPetriNetBinding(
                transition_identity=self._exact(
                    self._decode(fields["transition_identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
                assignments=tuple(
                    self._exact(item, ColoredPetriNetBindingAssignment)
                    for item in self._items(self._decode(fields["assignments"], seen))
                ),
            )
            return record
        if tag == "ColoredPetriNetBindingAssignment":
            fields = self._fields(wire, tag, ("variable_identity", "value"))
            record = ColoredPetriNetBindingAssignment(
                variable_identity=self._exact(
                    self._decode(fields["variable_identity"], seen),
                    ColoredPetriNetBindingVariableIdentity,
                ),
                value=self._exact(
                    self._decode(fields["value"], seen), ColoredPetriNetValue
                ),
            )
            return record
        if tag == "ColoredPetriNetBindingSelectorIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetBindingSelectorIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetBindingVariableIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetBindingVariableIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetColorDefinition":
            fields = self._fields(wire, tag, ("identity", "allowed_value_kinds"))
            record = ColoredPetriNetColorDefinition(
                identity=self._exact(
                    self._decode(fields["identity"], seen), ColoredPetriNetColorIdentity
                ),
                allowed_value_kinds=tuple(
                    self._exact(item, ColoredPetriNetValueKind)
                    for item in self._items(
                        self._decode(fields["allowed_value_kinds"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetColorIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetColorIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetDefinition":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "colors",
                    "places",
                    "transitions",
                    "arcs",
                    "transition_priority",
                    "selection_policy",
                ),
            )
            record = ColoredPetriNetDefinition(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetDefinitionIdentity,
                ),
                colors=tuple(
                    self._exact(item, ColoredPetriNetColorDefinition)
                    for item in self._items(self._decode(fields["colors"], seen))
                ),
                places=tuple(
                    self._exact(item, ColoredPetriNetPlaceDefinition)
                    for item in self._items(self._decode(fields["places"], seen))
                ),
                transitions=tuple(
                    self._exact(item, ColoredPetriNetTransitionDefinition)
                    for item in self._items(self._decode(fields["transitions"], seen))
                ),
                arcs=tuple(
                    self._exact(item, ColoredPetriNetArcDefinition)
                    for item in self._items(self._decode(fields["arcs"], seen))
                ),
                transition_priority=tuple(
                    self._exact(item, ColoredPetriNetTransitionIdentity)
                    for item in self._items(
                        self._decode(fields["transition_priority"], seen)
                    )
                ),
                selection_policy=self._exact(
                    self._decode(fields["selection_policy"], seen),
                    ColoredPetriNetSelectionPolicy,
                ),
            )
            return record
        if tag == "ColoredPetriNetDefinitionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetDefinitionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetEnablementFailure":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "code",
                    "operation_phase",
                    "expected_condition",
                    "observed_condition",
                    "diagnostic",
                    "validation_issues",
                    "claim_boundary",
                ),
            )
            record = ColoredPetriNetEnablementFailure(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetEnablementFailureIdentity,
                ),
                code=self._exact(
                    self._decode(fields["code"], seen),
                    ColoredPetriNetEnablementFailureCode,
                ),
                operation_phase=self._exact(
                    self._decode(fields["operation_phase"], seen), str
                ),
                expected_condition=self._exact(
                    self._decode(fields["expected_condition"], seen), str
                ),
                observed_condition=self._exact(
                    self._decode(fields["observed_condition"], seen), str
                ),
                diagnostic=self._exact(self._decode(fields["diagnostic"], seen), str),
                validation_issues=tuple(
                    self._exact(item, ColoredPetriNetValidationIssue)
                    for item in self._items(
                        self._decode(fields["validation_issues"], seen)
                    )
                ),
                claim_boundary=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["claim_boundary"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetEnablementFailureIdentity":
            fields = self._fields(wire, tag, ("result_identity",))
            record = ColoredPetriNetEnablementFailureIdentity(
                result_identity=self._exact(
                    self._decode(fields["result_identity"], seen),
                    ColoredPetriNetEnablementResultIdentity,
                ),
            )
            return record
        if tag == "ColoredPetriNetEnablementResult":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "definition_identity",
                    "selection_policy",
                    "marking_identity",
                    "expression_evaluator_identity",
                    "ordering_policy_identity",
                    "transition_enabler_identity",
                    "enabled_bindings",
                    "failure",
                ),
            )
            record = ColoredPetriNetEnablementResult(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetEnablementResultIdentity,
                ),
                definition_identity=self._exact(
                    self._decode(fields["definition_identity"], seen),
                    ColoredPetriNetDefinitionIdentity,
                ),
                selection_policy=self._exact(
                    self._decode(fields["selection_policy"], seen),
                    ColoredPetriNetSelectionPolicy,
                ),
                marking_identity=self._exact(
                    self._decode(fields["marking_identity"], seen),
                    ColoredPetriNetMarkingIdentity,
                ),
                expression_evaluator_identity=self._exact(
                    self._decode(fields["expression_evaluator_identity"], seen),
                    ColoredPetriNetExpressionEvaluatorIdentity,
                ),
                ordering_policy_identity=self._exact(
                    self._decode(fields["ordering_policy_identity"], seen),
                    ColoredPetriNetOrderingPolicyIdentity,
                ),
                transition_enabler_identity=self._exact(
                    self._decode(fields["transition_enabler_identity"], seen),
                    ColoredPetriNetTransitionEnablerIdentity,
                ),
                enabled_bindings=self._parse_ColoredPetriNetEnablementResult_enabled_bindings(
                    self._decode(fields["enabled_bindings"], seen)
                ),
                failure=self._parse_ColoredPetriNetEnablementResult_failure(
                    self._decode(fields["failure"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetEnablementResultIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetEnablementResultIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetExpressionEvaluatorIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetExpressionEvaluatorIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetFiringAudit":
            fields = self._fields(
                wire,
                tag,
                (
                    "consumed_occurrences",
                    "read_occurrences",
                    "inhibitor_evaluations",
                    "produced_tokens",
                    "firer_identity",
                ),
            )
            record = ColoredPetriNetFiringAudit(
                consumed_occurrences=tuple(
                    self._exact(item, ColoredPetriNetTokenOccurrence)
                    for item in self._items(
                        self._decode(fields["consumed_occurrences"], seen)
                    )
                ),
                read_occurrences=tuple(
                    self._exact(item, ColoredPetriNetTokenOccurrence)
                    for item in self._items(
                        self._decode(fields["read_occurrences"], seen)
                    )
                ),
                inhibitor_evaluations=tuple(
                    self._exact(item, ColoredPetriNetInhibitorEvaluation)
                    for item in self._items(
                        self._decode(fields["inhibitor_evaluations"], seen)
                    )
                ),
                produced_tokens=tuple(
                    self._exact(item, ColoredPetriNetProducedToken)
                    for item in self._items(
                        self._decode(fields["produced_tokens"], seen)
                    )
                ),
                firer_identity=self._exact(
                    self._decode(fields["firer_identity"], seen),
                    ColoredPetriNetTransitionFirerIdentity,
                ),
            )
            return record
        if tag == "ColoredPetriNetFiringFailure":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "code",
                    "operation_phase",
                    "expected_condition",
                    "observed_condition",
                    "diagnostic",
                    "validation_issues",
                    "claim_boundary",
                ),
            )
            record = ColoredPetriNetFiringFailure(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetFiringFailureIdentity,
                ),
                code=self._exact(
                    self._decode(fields["code"], seen), ColoredPetriNetFiringFailureCode
                ),
                operation_phase=self._exact(
                    self._decode(fields["operation_phase"], seen), str
                ),
                expected_condition=self._exact(
                    self._decode(fields["expected_condition"], seen), str
                ),
                observed_condition=self._exact(
                    self._decode(fields["observed_condition"], seen), str
                ),
                diagnostic=self._exact(self._decode(fields["diagnostic"], seen), str),
                validation_issues=tuple(
                    self._exact(item, ColoredPetriNetValidationIssue)
                    for item in self._items(
                        self._decode(fields["validation_issues"], seen)
                    )
                ),
                claim_boundary=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["claim_boundary"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetFiringFailureIdentity":
            fields = self._fields(wire, tag, ("result_identity",))
            record = ColoredPetriNetFiringFailureIdentity(
                result_identity=self._exact(
                    self._decode(fields["result_identity"], seen),
                    ColoredPetriNetFiringResultIdentity,
                ),
            )
            return record
        if tag == "ColoredPetriNetFiringInput":
            fields = self._fields(
                wire,
                tag,
                (
                    "definition",
                    "transition_identity",
                    "predecessor_marking",
                    "enablement_result",
                    "selection_result",
                    "selected_binding",
                    "directive_identity",
                    "external_output_binding",
                ),
            )
            record = ColoredPetriNetFiringInput(
                definition=self._exact(
                    self._decode(fields["definition"], seen), ColoredPetriNetDefinition
                ),
                transition_identity=self._exact(
                    self._decode(fields["transition_identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
                predecessor_marking=self._exact(
                    self._decode(fields["predecessor_marking"], seen),
                    ColoredPetriNetMarking,
                ),
                enablement_result=self._exact(
                    self._decode(fields["enablement_result"], seen),
                    ColoredPetriNetEnablementResult,
                ),
                selection_result=self._exact(
                    self._decode(fields["selection_result"], seen),
                    ColoredPetriNetSelectionResult,
                ),
                selected_binding=self._exact(
                    self._decode(fields["selected_binding"], seen),
                    ColoredPetriNetBinding,
                ),
                directive_identity=self._parse_ColoredPetriNetFiringInput_directive_identity(
                    self._decode(fields["directive_identity"], seen)
                ),
                external_output_binding=self._exact(
                    self._decode(fields["external_output_binding"], seen),
                    ColoredPetriNetBinding,
                ),
            )
            return record
        if tag == "ColoredPetriNetFiringResult":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "firing_input",
                    "outcome",
                    "successor_marking",
                    "audit",
                    "failure",
                ),
            )
            record = ColoredPetriNetFiringResult(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetFiringResultIdentity,
                ),
                firing_input=self._exact(
                    self._decode(fields["firing_input"], seen),
                    ColoredPetriNetFiringInput,
                ),
                outcome=self._exact(
                    self._decode(fields["outcome"], seen),
                    ColoredPetriNetFiringOutcomeKind,
                ),
                successor_marking=self._parse_ColoredPetriNetFiringResult_successor_marking(
                    self._decode(fields["successor_marking"], seen)
                ),
                audit=self._parse_ColoredPetriNetFiringResult_audit(
                    self._decode(fields["audit"], seen)
                ),
                failure=self._parse_ColoredPetriNetFiringResult_failure(
                    self._decode(fields["failure"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetFiringResultIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetFiringResultIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetGuardExpression":
            fields = self._fields(wire, tag, ("operator", "operands", "left", "right"))
            record = ColoredPetriNetGuardExpression(
                operator=self._exact(
                    self._decode(fields["operator"], seen), ColoredPetriNetGuardOperator
                ),
                operands=tuple(
                    self._exact(item, ColoredPetriNetGuardExpression)
                    for item in self._items(self._decode(fields["operands"], seen))
                ),
                left=self._parse_ColoredPetriNetGuardExpression_left(
                    self._decode(fields["left"], seen)
                ),
                right=self._parse_ColoredPetriNetGuardExpression_left(
                    self._decode(fields["right"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetInhibitorEvaluation":
            fields = self._fields(
                wire,
                tag,
                ("arc_identity", "place_identity", "pattern_index", "matching_count"),
            )
            record = ColoredPetriNetInhibitorEvaluation(
                arc_identity=self._exact(
                    self._decode(fields["arc_identity"], seen),
                    ColoredPetriNetArcIdentity,
                ),
                place_identity=self._exact(
                    self._decode(fields["place_identity"], seen),
                    ColoredPetriNetPlaceIdentity,
                ),
                pattern_index=self._exact(
                    self._decode(fields["pattern_index"], seen), int
                ),
                matching_count=self._exact(
                    self._decode(fields["matching_count"], seen), int
                ),
            )
            return record
        if tag == "ColoredPetriNetInhibitorPattern":
            fields = self._fields(wire, tag, ("allowed_color_identities",))
            record = ColoredPetriNetInhibitorPattern(
                allowed_color_identities=tuple(
                    self._exact(item, ColoredPetriNetColorIdentity)
                    for item in self._items(
                        self._decode(fields["allowed_color_identities"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetInputInscription":
            fields = self._fields(wire, tag, ("mode", "patterns"))
            record = ColoredPetriNetInputInscription(
                mode=self._exact(
                    self._decode(fields["mode"], seen), ColoredPetriNetInputMode
                ),
                patterns=tuple(
                    self._parse_ColoredPetriNetInputInscription_patterns_item(item)
                    for item in self._items(self._decode(fields["patterns"], seen))
                ),
            )
            return record
        if tag == "ColoredPetriNetMarking":
            fields = self._fields(
                wire, tag, ("identity", "definition_identity", "places")
            )
            record = ColoredPetriNetMarking(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetMarkingIdentity,
                ),
                definition_identity=self._exact(
                    self._decode(fields["definition_identity"], seen),
                    ColoredPetriNetDefinitionIdentity,
                ),
                places=tuple(
                    self._exact(item, ColoredPetriNetPlaceMarking)
                    for item in self._items(self._decode(fields["places"], seen))
                ),
            )
            return record
        if tag == "ColoredPetriNetMarkingIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetMarkingIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetOrderingPolicyIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetOrderingPolicyIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetOutputInscription":
            fields = self._fields(wire, tag, ("templates",))
            record = ColoredPetriNetOutputInscription(
                templates=tuple(
                    self._exact(item, ColoredPetriNetTokenTemplate)
                    for item in self._items(self._decode(fields["templates"], seen))
                ),
            )
            return record
        if tag == "ColoredPetriNetPlaceDefinition":
            fields = self._fields(wire, tag, ("identity", "allowed_color_identities"))
            record = ColoredPetriNetPlaceDefinition(
                identity=self._exact(
                    self._decode(fields["identity"], seen), ColoredPetriNetPlaceIdentity
                ),
                allowed_color_identities=tuple(
                    self._exact(item, ColoredPetriNetColorIdentity)
                    for item in self._items(
                        self._decode(fields["allowed_color_identities"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetPlaceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetPlaceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetPlaceMarking":
            fields = self._fields(wire, tag, ("place_identity", "tokens"))
            record = ColoredPetriNetPlaceMarking(
                place_identity=self._exact(
                    self._decode(fields["place_identity"], seen),
                    ColoredPetriNetPlaceIdentity,
                ),
                tokens=tuple(
                    self._exact(item, ColoredPetriNetToken)
                    for item in self._items(self._decode(fields["tokens"], seen))
                ),
            )
            return record
        if tag == "ColoredPetriNetProducedToken":
            fields = self._fields(
                wire, tag, ("arc_identity", "place_identity", "template_index", "token")
            )
            record = ColoredPetriNetProducedToken(
                arc_identity=self._exact(
                    self._decode(fields["arc_identity"], seen),
                    ColoredPetriNetArcIdentity,
                ),
                place_identity=self._exact(
                    self._decode(fields["place_identity"], seen),
                    ColoredPetriNetPlaceIdentity,
                ),
                template_index=self._exact(
                    self._decode(fields["template_index"], seen), int
                ),
                token=self._exact(
                    self._decode(fields["token"], seen), ColoredPetriNetToken
                ),
            )
            return record
        if tag == "ColoredPetriNetSelectionDirective":
            fields = self._fields(
                wire, tag, ("enablement_result_identity", "binding", "identity")
            )
            record = ColoredPetriNetSelectionDirective(
                enablement_result_identity=self._exact(
                    self._decode(fields["enablement_result_identity"], seen),
                    ColoredPetriNetEnablementResultIdentity,
                ),
                binding=self._exact(
                    self._decode(fields["binding"], seen), ColoredPetriNetBinding
                ),
            )
            if record.identity != self._exact(
                self._decode(fields["identity"], seen),
                ColoredPetriNetSelectionDirectiveIdentity,
            ):
                raise self._failure(
                    "decode", WorkflowPersistenceFailureCode.IDENTITY_MISMATCH
                )
            return record
        if tag == "ColoredPetriNetSelectionDirectiveIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetSelectionDirectiveIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetSelectionResult":
            fields = self._fields(
                wire,
                tag,
                (
                    "enablement_result_identity",
                    "selector_identity",
                    "ordering_policy_identity",
                    "outcome",
                    "selected_binding",
                    "directive",
                    "failure_code",
                    "identity",
                ),
            )
            record = ColoredPetriNetSelectionResult(
                enablement_result_identity=self._exact(
                    self._decode(fields["enablement_result_identity"], seen),
                    ColoredPetriNetEnablementResultIdentity,
                ),
                selector_identity=self._exact(
                    self._decode(fields["selector_identity"], seen),
                    ColoredPetriNetBindingSelectorIdentity,
                ),
                ordering_policy_identity=self._exact(
                    self._decode(fields["ordering_policy_identity"], seen),
                    ColoredPetriNetOrderingPolicyIdentity,
                ),
                outcome=self._exact(
                    self._decode(fields["outcome"], seen),
                    ColoredPetriNetSelectionOutcomeKind,
                ),
                selected_binding=self._parse_ColoredPetriNetSelectionResult_selected_binding(
                    self._decode(fields["selected_binding"], seen)
                ),
                directive=self._parse_ColoredPetriNetSelectionResult_directive(
                    self._decode(fields["directive"], seen)
                ),
                failure_code=self._parse_ColoredPetriNetSelectionResult_failure_code(
                    self._decode(fields["failure_code"], seen)
                ),
            )
            if record.identity != self._exact(
                self._decode(fields["identity"], seen),
                ColoredPetriNetSelectionResultIdentity,
            ):
                raise self._failure(
                    "decode", WorkflowPersistenceFailureCode.IDENTITY_MISMATCH
                )
            return record
        if tag == "ColoredPetriNetSelectionResultIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetSelectionResultIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetToken":
            fields = self._fields(
                wire, tag, ("color_identity", "value", "token_identity")
            )
            record = ColoredPetriNetToken(
                color_identity=self._exact(
                    self._decode(fields["color_identity"], seen),
                    ColoredPetriNetColorIdentity,
                ),
                value=self._exact(
                    self._decode(fields["value"], seen), ColoredPetriNetValue
                ),
                token_identity=self._parse_ColoredPetriNetToken_token_identity(
                    self._decode(fields["token_identity"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetTokenIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetTokenIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetTokenOccurrence":
            fields = self._fields(
                wire,
                tag,
                (
                    "arc_identity",
                    "place_identity",
                    "pattern_index",
                    "occurrence_ordinal",
                    "token",
                ),
            )
            record = ColoredPetriNetTokenOccurrence(
                arc_identity=self._exact(
                    self._decode(fields["arc_identity"], seen),
                    ColoredPetriNetArcIdentity,
                ),
                place_identity=self._exact(
                    self._decode(fields["place_identity"], seen),
                    ColoredPetriNetPlaceIdentity,
                ),
                pattern_index=self._exact(
                    self._decode(fields["pattern_index"], seen), int
                ),
                occurrence_ordinal=self._exact(
                    self._decode(fields["occurrence_ordinal"], seen), int
                ),
                token=self._exact(
                    self._decode(fields["token"], seen), ColoredPetriNetToken
                ),
            )
            return record
        if tag == "ColoredPetriNetTokenPattern":
            fields = self._fields(
                wire, tag, ("variable_identity", "allowed_color_identities")
            )
            record = ColoredPetriNetTokenPattern(
                variable_identity=self._exact(
                    self._decode(fields["variable_identity"], seen),
                    ColoredPetriNetBindingVariableIdentity,
                ),
                allowed_color_identities=tuple(
                    self._exact(item, ColoredPetriNetColorIdentity)
                    for item in self._items(
                        self._decode(fields["allowed_color_identities"], seen)
                    )
                ),
            )
            return record
        if tag == "ColoredPetriNetTokenTemplate":
            fields = self._fields(
                wire,
                tag,
                ("color_identity", "value_expression", "token_identity_expression"),
            )
            record = ColoredPetriNetTokenTemplate(
                color_identity=self._exact(
                    self._decode(fields["color_identity"], seen),
                    ColoredPetriNetColorIdentity,
                ),
                value_expression=self._exact(
                    self._decode(fields["value_expression"], seen),
                    ColoredPetriNetValueExpression,
                ),
                token_identity_expression=self._parse_ColoredPetriNetGuardExpression_left(
                    self._decode(fields["token_identity_expression"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetTransitionDefinition":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "input_variable_identities",
                    "external_output_variable_identities",
                    "guard",
                ),
            )
            record = ColoredPetriNetTransitionDefinition(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
                input_variable_identities=tuple(
                    self._exact(item, ColoredPetriNetBindingVariableIdentity)
                    for item in self._items(
                        self._decode(fields["input_variable_identities"], seen)
                    )
                ),
                external_output_variable_identities=tuple(
                    self._exact(item, ColoredPetriNetBindingVariableIdentity)
                    for item in self._items(
                        self._decode(
                            fields["external_output_variable_identities"], seen
                        )
                    )
                ),
                guard=self._exact(
                    self._decode(fields["guard"], seen), ColoredPetriNetGuardExpression
                ),
            )
            return record
        if tag == "ColoredPetriNetTransitionEnablerIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetTransitionEnablerIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetTransitionFirerIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetTransitionFirerIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetTransitionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = ColoredPetriNetTransitionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetValidationIssue":
            fields = self._fields(
                wire, tag, ("code", "path", "related_identities", "message")
            )
            record = ColoredPetriNetValidationIssue(
                code=self._exact(
                    self._decode(fields["code"], seen),
                    ColoredPetriNetValidationIssueCode,
                ),
                path=tuple(
                    self._exact(item, str)
                    for item in self._items(self._decode(fields["path"], seen))
                ),
                related_identities=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["related_identities"], seen)
                    )
                ),
                message=self._exact(self._decode(fields["message"], seen), str),
            )
            return record
        if tag == "ColoredPetriNetValue":
            fields = self._fields(wire, tag, ("kind", "value"))
            record = ColoredPetriNetValue(
                kind=self._exact(
                    self._decode(fields["kind"], seen), ColoredPetriNetValueKind
                ),
                value=self._parse_ColoredPetriNetValue_value(
                    self._decode(fields["value"], seen)
                ),
            )
            return record
        if tag == "ColoredPetriNetValueExpression":
            fields = self._fields(wire, tag, ("kind", "literal", "variable_identity"))
            record = ColoredPetriNetValueExpression(
                kind=self._exact(
                    self._decode(fields["kind"], seen),
                    ColoredPetriNetValueExpressionKind,
                ),
                literal=self._parse_ColoredPetriNetValueExpression_literal(
                    self._decode(fields["literal"], seen)
                ),
                variable_identity=self._parse_ColoredPetriNetValueExpression_variable_identity(
                    self._decode(fields["variable_identity"], seen)
                ),
            )
            return record
        if tag == "DirectTaskActivationSelection":
            fields = self._fields(wire, tag, ("selection_result_identity",))
            record = DirectTaskActivationSelection(
                selection_result_identity=self._exact(
                    self._decode(fields["selection_result_identity"], seen),
                    ColoredPetriNetSelectionResultIdentity,
                ),
            )
            return record
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
        if tag == "OperationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = OperationIdentity(
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
        if tag == "TaskActivation":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_identity",
                    "workflow_run_identity",
                    "task_instance",
                    "operation_identity",
                    "attempt_identity",
                    "inputs",
                    "selection",
                ),
            )
            record = TaskActivation(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskActivationIdentity
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                task_instance=self._exact(
                    self._decode(fields["task_instance"], seen), TaskInstance
                ),
                operation_identity=self._exact(
                    self._decode(fields["operation_identity"], seen), OperationIdentity
                ),
                attempt_identity=self._exact(
                    self._decode(fields["attempt_identity"], seen), AttemptIdentity
                ),
                inputs=tuple(
                    self._exact(item, TaskInputBinding)
                    for item in self._items(self._decode(fields["inputs"], seen))
                ),
                selection=self._parse_TaskActivation_selection(
                    self._decode(fields["selection"], seen)
                ),
            )
            return record
        if tag == "TaskActivationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskActivationIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskAttempt":
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
                    "status",
                    "predecessor_attempt_record_identity",
                    "retry_of_attempt_identity",
                    "child_workflow_run_identity",
                ),
            )
            record = TaskAttempt(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskAttemptRecordIdentity
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
                status=self._exact(
                    self._decode(fields["status"], seen), TaskAttemptStatus
                ),
                predecessor_attempt_record_identity=self._parse_TaskAttempt_predecessor_attempt_record_identity(
                    self._decode(fields["predecessor_attempt_record_identity"], seen)
                ),
                retry_of_attempt_identity=self._parse_TaskAttempt_retry_of_attempt_identity(
                    self._decode(fields["retry_of_attempt_identity"], seen)
                ),
                child_workflow_run_identity=self._parse_ResultDependency_producer_workflow_run_identity(
                    self._decode(fields["child_workflow_run_identity"], seen)
                ),
            )
            return record
        if tag == "TaskAttemptRecordIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskAttemptRecordIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskDefinitionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskDefinitionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskFailureRecord":
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
                    "failure",
                    "request_identity",
                    "child_workflow_run_identity",
                    "claim_boundary",
                ),
            )
            record = TaskFailureRecord(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskFailureRecordIdentity
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
                failure=self._exact(
                    self._decode(fields["failure"], seen), TaskInvocationFailure
                ),
                request_identity=self._parse_TaskFailureRecord_request_identity(
                    self._decode(fields["request_identity"], seen)
                ),
                child_workflow_run_identity=self._parse_ResultDependency_producer_workflow_run_identity(
                    self._decode(fields["child_workflow_run_identity"], seen)
                ),
                claim_boundary=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["claim_boundary"], seen)
                    )
                ),
            )
            return record
        if tag == "TaskFailureRecordIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskFailureRecordIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskGateSelection":
            fields = self._fields(wire, tag, ("gate_identity", "binding"))
            record = TaskGateSelection(
                gate_identity=self._exact(
                    self._decode(fields["gate_identity"], seen), TaskStartGateIdentity
                ),
                binding=self._exact(
                    self._decode(fields["binding"], seen), ColoredPetriNetBinding
                ),
            )
            return record
        if tag == "TaskInputBinding":
            fields = self._fields(wire, tag, ("name", "result"))
            record = TaskInputBinding(
                name=self._exact(self._decode(fields["name"], seen), str),
                result=self._as_result(self._decode(fields["result"], seen)),
            )
            return record
        if tag == "TaskInstance":
            fields = self._fields(
                wire, tag, ("identity", "definition_identity", "start_gate_set")
            )
            record = TaskInstance(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskInstanceIdentity
                ),
                definition_identity=self._exact(
                    self._decode(fields["definition_identity"], seen),
                    TaskDefinitionIdentity,
                ),
                start_gate_set=self._parse_TaskInstance_start_gate_set(
                    self._decode(fields["start_gate_set"], seen)
                ),
            )
            return record
        if tag == "TaskInstanceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskInstanceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskInvocationFailure":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "code",
                    "operation_phase",
                    "diagnostic",
                    "retryable",
                    "claim_boundary",
                ),
            )
            record = TaskInvocationFailure(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    TaskInvocationFailureIdentity,
                ),
                code=self._exact(self._decode(fields["code"], seen), str),
                operation_phase=self._exact(
                    self._decode(fields["operation_phase"], seen), str
                ),
                diagnostic=self._exact(self._decode(fields["diagnostic"], seen), str),
                retryable=self._parse_TaskInvocationFailure_retryable(
                    self._decode(fields["retryable"], seen)
                ),
                claim_boundary=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["claim_boundary"], seen)
                    )
                ),
            )
            return record
        if tag == "TaskInvocationFailureIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskInvocationFailureIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskInvocationOutcome":
            fields = self._fields(
                wire,
                tag,
                (
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
                    "dispatch_outcome_record_identity",
                    "reconciliation_identity_values",
                ),
            )
            record = TaskInvocationOutcome(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    TaskInvocationOutcomeIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
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
                kind=self._exact(
                    self._decode(fields["kind"], seen), TaskInvocationOutcomeKind
                ),
                results=tuple(
                    self._exact(item, ResultObjectReference)
                    for item in self._items(self._decode(fields["results"], seen))
                ),
                production_record_identities=tuple(
                    self._exact(item, ResultProductionRecordIdentity)
                    for item in self._items(
                        self._decode(fields["production_record_identities"], seen)
                    )
                ),
                failure_record_identity=self._parse_DispatchOutcomeRecord_failure_record_identity(
                    self._decode(fields["failure_record_identity"], seen)
                ),
                dispatch_outcome_record_identity=self._parse_TaskInvocationOutcome_dispatch_outcome_record_identity(
                    self._decode(fields["dispatch_outcome_record_identity"], seen)
                ),
                reconciliation_identity_values=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["reconciliation_identity_values"], seen)
                    )
                ),
            )
            return record
        if tag == "TaskInvocationOutcomeIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskInvocationOutcomeIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskStartGate":
            fields = self._fields(
                wire, tag, ("identity", "priority", "transition_identity")
            )
            record = TaskStartGate(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskStartGateIdentity
                ),
                priority=self._exact(self._decode(fields["priority"], seen), int),
                transition_identity=self._exact(
                    self._decode(fields["transition_identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
            )
            return record
        if tag == "TaskStartGateIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskStartGateIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskStartGateSet":
            fields = self._fields(wire, tag, ("identity", "mode", "gates"))
            record = TaskStartGateSet(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskStartGateSetIdentity
                ),
                mode=self._exact(
                    self._decode(fields["mode"], seen), TaskStartGateSetMode
                ),
                gates=tuple(
                    self._exact(item, TaskStartGate)
                    for item in self._items(self._decode(fields["gates"], seen))
                ),
            )
            return record
        if tag == "TaskStartGateSetIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskStartGateSetIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskWorkflowMembership":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "workflow_identity",
                    "task_instance_identity",
                ),
            )
            record = TaskWorkflowMembership(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    TaskWorkflowMembershipIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
                ),
                task_instance_identity=self._exact(
                    self._decode(fields["task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
            )
            return record
        if tag == "TaskWorkflowMembershipIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskWorkflowMembershipIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskWorkflowTransitionRecord":
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
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "terminal_attempt_record_identity",
                    "outcome_identity",
                    "result_production_identities",
                    "firing_result",
                    "request_correlation_identity",
                    "dispatch_outcome_record_identity",
                ),
            )
            record = TaskWorkflowTransitionRecord(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    TaskWorkflowTransitionRecordIdentity,
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
                result_production_identities=tuple(
                    self._exact(item, ResultProductionRecordIdentity)
                    for item in self._items(
                        self._decode(fields["result_production_identities"], seen)
                    )
                ),
                firing_result=self._exact(
                    self._decode(fields["firing_result"], seen),
                    ColoredPetriNetFiringResult,
                ),
                request_correlation_identity=self._parse_TaskWorkflowTransitionRecord_request_correlation_identity(
                    self._decode(fields["request_correlation_identity"], seen)
                ),
                dispatch_outcome_record_identity=self._parse_TaskInvocationOutcome_dispatch_outcome_record_identity(
                    self._decode(fields["dispatch_outcome_record_identity"], seen)
                ),
            )
            return record
        if tag == "TaskWorkflowTransitionRecordIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskWorkflowTransitionRecordIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
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
        if tag == "WorkflowDefinitionReferenceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowDefinitionReferenceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowRun":
            raw_run_fields = wire["fields"]
            extension_names = (
                ("nested_invocation_intents", "nested_terminal_observations")
                if isinstance(raw_run_fields, dict)
                and (
                    "nested_invocation_intents" in raw_run_fields
                    or "nested_terminal_observations" in raw_run_fields
                )
                else ()
            )
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "revision_identity",
                    "predecessor_revision_identity",
                    "workflow_identity",
                    "definition_reference_identity",
                    "runtime_bundle_identity",
                    "schema_version",
                    "adapter_implementation_identity",
                    "task_instances",
                    "task_memberships",
                    "nested_memberships",
                    "nested_invocations",
                    "activations",
                    "attempts",
                    "outcomes",
                    "result_references",
                    "result_productions",
                    "native_output_admissions",
                    "result_dependencies",
                    "failures",
                    "authorization_results",
                    "authority_references",
                    "execution_request_correlations",
                    "authority_reservations",
                    "dispatch_obligations",
                    "dispatch_entries",
                    "dispatch_observations",
                    "dispatch_outcomes",
                    "obligation_dispositions",
                    "scientific_decision_requests",
                    "scientific_decision_resolutions",
                    "initial_marking",
                    "current_marking",
                    "transitions",
                    *extension_names,
                ),
            )
            record = WorkflowRun(
                identity=self._exact(
                    self._decode(fields["identity"], seen), WorkflowRunIdentity
                ),
                revision_identity=self._exact(
                    self._decode(fields["revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                predecessor_revision_identity=self._parse_NestedWorkflowInvocation_terminal_child_revision_identity(
                    self._decode(fields["predecessor_revision_identity"], seen)
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
                ),
                definition_reference_identity=self._exact(
                    self._decode(fields["definition_reference_identity"], seen),
                    WorkflowDefinitionReferenceIdentity,
                ),
                runtime_bundle_identity=self._exact(
                    self._decode(fields["runtime_bundle_identity"], seen),
                    WorkflowRuntimeBundleIdentity,
                ),
                schema_version=self._exact(
                    self._decode(fields["schema_version"], seen), int
                ),
                adapter_implementation_identity=self._exact(
                    self._decode(fields["adapter_implementation_identity"], seen), str
                ),
                task_instances=tuple(
                    self._exact(item, TaskInstance)
                    for item in self._items(
                        self._decode(fields["task_instances"], seen)
                    )
                ),
                task_memberships=tuple(
                    self._exact(item, TaskWorkflowMembership)
                    for item in self._items(
                        self._decode(fields["task_memberships"], seen)
                    )
                ),
                nested_memberships=tuple(
                    self._exact(item, NestedWorkflowMembership)
                    for item in self._items(
                        self._decode(fields["nested_memberships"], seen)
                    )
                ),
                nested_invocations=tuple(
                    self._exact(item, NestedWorkflowInvocation)
                    for item in self._items(
                        self._decode(fields["nested_invocations"], seen)
                    )
                ),
                nested_invocation_intents=(
                    tuple(
                        self._exact(item, NestedWorkflowInvocationIntent)
                        for item in self._items(
                            self._decode(fields["nested_invocation_intents"], seen)
                        )
                    )
                    if extension_names
                    else ()
                ),
                nested_terminal_observations=(
                    tuple(
                        self._exact(item, NestedWorkflowTerminalObservation)
                        for item in self._items(
                            self._decode(fields["nested_terminal_observations"], seen)
                        )
                    )
                    if extension_names
                    else ()
                ),
                activations=tuple(
                    self._exact(item, TaskActivation)
                    for item in self._items(self._decode(fields["activations"], seen))
                ),
                attempts=tuple(
                    self._exact(item, TaskAttempt)
                    for item in self._items(self._decode(fields["attempts"], seen))
                ),
                outcomes=tuple(
                    self._exact(item, TaskInvocationOutcome)
                    for item in self._items(self._decode(fields["outcomes"], seen))
                ),
                result_references=tuple(
                    self._exact(item, ResultObjectReference)
                    for item in self._items(
                        self._decode(fields["result_references"], seen)
                    )
                ),
                result_productions=tuple(
                    self._exact(item, ResultProductionRecord)
                    for item in self._items(
                        self._decode(fields["result_productions"], seen)
                    )
                ),
                native_output_admissions=tuple(
                    self._exact(item, NativeOutputAdmission)
                    for item in self._items(
                        self._decode(fields["native_output_admissions"], seen)
                    )
                ),
                result_dependencies=tuple(
                    self._exact(item, ResultDependency)
                    for item in self._items(
                        self._decode(fields["result_dependencies"], seen)
                    )
                ),
                failures=tuple(
                    self._exact(item, TaskFailureRecord)
                    for item in self._items(self._decode(fields["failures"], seen))
                ),
                authorization_results=tuple(
                    self._exact(item, SimulationExecutionAuthorizationResult)
                    for item in self._items(
                        self._decode(fields["authorization_results"], seen)
                    )
                ),
                authority_references=tuple(
                    self._exact(item, ScientificExecutionAuthorityReference)
                    for item in self._items(
                        self._decode(fields["authority_references"], seen)
                    )
                ),
                execution_request_correlations=tuple(
                    self._exact(item, SimulationExecutionRequestCorrelation)
                    for item in self._items(
                        self._decode(fields["execution_request_correlations"], seen)
                    )
                ),
                authority_reservations=tuple(
                    self._exact(item, AuthorityReservationOutcome)
                    for item in self._items(
                        self._decode(fields["authority_reservations"], seen)
                    )
                ),
                dispatch_obligations=tuple(
                    self._exact(item, SimulationDispatchObligation)
                    for item in self._items(
                        self._decode(fields["dispatch_obligations"], seen)
                    )
                ),
                dispatch_entries=tuple(
                    self._exact(item, SimulationDispatchEntry)
                    for item in self._items(
                        self._decode(fields["dispatch_entries"], seen)
                    )
                ),
                dispatch_observations=tuple(
                    self._exact(item, DispatchObservationRecord)
                    for item in self._items(
                        self._decode(fields["dispatch_observations"], seen)
                    )
                ),
                dispatch_outcomes=tuple(
                    self._exact(item, DispatchOutcomeRecord)
                    for item in self._items(
                        self._decode(fields["dispatch_outcomes"], seen)
                    )
                ),
                obligation_dispositions=tuple(
                    self._exact(item, ObligationDisposition)
                    for item in self._items(
                        self._decode(fields["obligation_dispositions"], seen)
                    )
                ),
                scientific_decision_requests=tuple(
                    self._exact(item, ScientificDecisionRequest)
                    for item in self._items(
                        self._decode(fields["scientific_decision_requests"], seen)
                    )
                ),
                scientific_decision_resolutions=tuple(
                    self._exact(item, ScientificDecisionResolution)
                    for item in self._items(
                        self._decode(fields["scientific_decision_resolutions"], seen)
                    )
                ),
                initial_marking=self._exact(
                    self._decode(fields["initial_marking"], seen),
                    ColoredPetriNetMarking,
                ),
                current_marking=self._exact(
                    self._decode(fields["current_marking"], seen),
                    ColoredPetriNetMarking,
                ),
                transitions=tuple(
                    self._parse_WorkflowRun_transitions_item(item)
                    for item in self._items(self._decode(fields["transitions"], seen))
                ),
            )
            return record
        if tag == "WorkflowRunIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowRunIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowRunReplayResultIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowRunReplayResultIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowRunRevisionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowRunRevisionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowRuntimeBundleIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowRuntimeBundleIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowTransitionSequenceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowTransitionSequenceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        raise self._failure("decode", WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE)

    def _parse_AuthorityReservationOutcome_predecessor_reservation_identity(
        self, value: _RunValue
    ) -> AuthorityReservationOutcomeIdentity | None:
        if type(value) is AuthorityReservationOutcomeIdentity:
            return self._exact(value, AuthorityReservationOutcomeIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetArcDefinition_input_inscription(
        self, value: _RunValue
    ) -> ColoredPetriNetInputInscription | None:
        if type(value) is ColoredPetriNetInputInscription:
            return self._exact(value, ColoredPetriNetInputInscription)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetArcDefinition_output_inscription(
        self, value: _RunValue
    ) -> ColoredPetriNetOutputInscription | None:
        if type(value) is ColoredPetriNetOutputInscription:
            return self._exact(value, ColoredPetriNetOutputInscription)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetEnablementResult_enabled_bindings(
        self, value: _RunValue
    ) -> tuple[ColoredPetriNetBinding, ...] | None:
        if type(value) is tuple:
            return tuple(
                self._exact(item, ColoredPetriNetBinding) for item in self._items(value)
            )
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetEnablementResult_failure(
        self, value: _RunValue
    ) -> ColoredPetriNetEnablementFailure | None:
        if type(value) is ColoredPetriNetEnablementFailure:
            return self._exact(value, ColoredPetriNetEnablementFailure)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetFiringInput_directive_identity(
        self, value: _RunValue
    ) -> ColoredPetriNetSelectionDirectiveIdentity | None:
        if type(value) is ColoredPetriNetSelectionDirectiveIdentity:
            return self._exact(value, ColoredPetriNetSelectionDirectiveIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetFiringResult_successor_marking(
        self, value: _RunValue
    ) -> ColoredPetriNetMarking | None:
        if type(value) is ColoredPetriNetMarking:
            return self._exact(value, ColoredPetriNetMarking)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetFiringResult_audit(
        self, value: _RunValue
    ) -> ColoredPetriNetFiringAudit | None:
        if type(value) is ColoredPetriNetFiringAudit:
            return self._exact(value, ColoredPetriNetFiringAudit)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetFiringResult_failure(
        self, value: _RunValue
    ) -> ColoredPetriNetFiringFailure | None:
        if type(value) is ColoredPetriNetFiringFailure:
            return self._exact(value, ColoredPetriNetFiringFailure)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetGuardExpression_left(
        self, value: _RunValue
    ) -> ColoredPetriNetValueExpression | None:
        if type(value) is ColoredPetriNetValueExpression:
            return self._exact(value, ColoredPetriNetValueExpression)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetInputInscription_patterns_item(
        self, value: _RunValue
    ) -> ColoredPetriNetTokenPattern | ColoredPetriNetInhibitorPattern:
        if type(value) is ColoredPetriNetTokenPattern:
            return self._exact(value, ColoredPetriNetTokenPattern)
        if type(value) is ColoredPetriNetInhibitorPattern:
            return self._exact(value, ColoredPetriNetInhibitorPattern)
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetSelectionResult_selected_binding(
        self, value: _RunValue
    ) -> ColoredPetriNetBinding | None:
        if type(value) is ColoredPetriNetBinding:
            return self._exact(value, ColoredPetriNetBinding)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetSelectionResult_directive(
        self, value: _RunValue
    ) -> ColoredPetriNetSelectionDirective | None:
        if type(value) is ColoredPetriNetSelectionDirective:
            return self._exact(value, ColoredPetriNetSelectionDirective)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetSelectionResult_failure_code(
        self, value: _RunValue
    ) -> ColoredPetriNetSelectionFailureCode | None:
        if type(value) is ColoredPetriNetSelectionFailureCode:
            return self._exact(value, ColoredPetriNetSelectionFailureCode)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetToken_token_identity(
        self, value: _RunValue
    ) -> ColoredPetriNetTokenIdentity | None:
        if type(value) is ColoredPetriNetTokenIdentity:
            return self._exact(value, ColoredPetriNetTokenIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetValue_value(
        self, value: _RunValue
    ) -> None | bool | int | float | str | tuple[str, ...]:
        if value is None:
            return None
        if type(value) is bool:
            return self._exact(value, bool)
        if type(value) is int:
            return self._exact(value, int)
        if type(value) is float:
            return self._exact(value, float)
        if type(value) is str:
            return self._exact(value, str)
        if type(value) is tuple:
            return tuple(self._exact(item, str) for item in self._items(value))
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetValueExpression_literal(
        self, value: _RunValue
    ) -> ColoredPetriNetValue | None:
        if type(value) is ColoredPetriNetValue:
            return self._exact(value, ColoredPetriNetValue)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_ColoredPetriNetValueExpression_variable_identity(
        self, value: _RunValue
    ) -> ColoredPetriNetBindingVariableIdentity | None:
        if type(value) is ColoredPetriNetBindingVariableIdentity:
            return self._exact(value, ColoredPetriNetBindingVariableIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

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

    def _parse_ObligationDisposition_predecessor_disposition_identity(
        self, value: _RunValue
    ) -> ObligationDispositionIdentity | None:
        if type(value) is ObligationDispositionIdentity:
            return self._exact(value, ObligationDispositionIdentity)
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

    def _parse_ScientificExecutionAuthorityGrant_reserved_obligation_identity(
        self, value: _RunValue
    ) -> ObligationIdentity | None:
        if type(value) is ObligationIdentity:
            return self._exact(value, ObligationIdentity)
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

    def _parse_SimulationExecutionAuthorizationResult_authorized_grant_state(
        self, value: _RunValue
    ) -> ScientificExecutionGrantState | None:
        if type(value) is ScientificExecutionGrantState:
            return self._exact(value, ScientificExecutionGrantState)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskActivation_selection(
        self, value: _RunValue
    ) -> (
        DirectTaskActivationSelection
        | AnyOfTaskActivationSelection
        | AllOfTaskActivationSelection
    ):
        if type(value) is DirectTaskActivationSelection:
            return self._exact(value, DirectTaskActivationSelection)
        if type(value) is AnyOfTaskActivationSelection:
            return self._exact(value, AnyOfTaskActivationSelection)
        if type(value) is AllOfTaskActivationSelection:
            return self._exact(value, AllOfTaskActivationSelection)
        raise TypeError("wrong closed field variant")

    def _parse_TaskAttempt_predecessor_attempt_record_identity(
        self, value: _RunValue
    ) -> TaskAttemptRecordIdentity | None:
        if type(value) is TaskAttemptRecordIdentity:
            return self._exact(value, TaskAttemptRecordIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskAttempt_retry_of_attempt_identity(
        self, value: _RunValue
    ) -> AttemptIdentity | None:
        if type(value) is AttemptIdentity:
            return self._exact(value, AttemptIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskFailureRecord_request_identity(
        self, value: _RunValue
    ) -> SimulationExecutionRequestIdentity | None:
        if type(value) is SimulationExecutionRequestIdentity:
            return self._exact(value, SimulationExecutionRequestIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskInstance_start_gate_set(
        self, value: _RunValue
    ) -> TaskStartGateSet | None:
        if type(value) is TaskStartGateSet:
            return self._exact(value, TaskStartGateSet)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskInvocationFailure_retryable(self, value: _RunValue) -> bool | None:
        if type(value) is bool:
            return self._exact(value, bool)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskInvocationOutcome_dispatch_outcome_record_identity(
        self, value: _RunValue
    ) -> DispatchOutcomeRecordIdentity | None:
        if type(value) is DispatchOutcomeRecordIdentity:
            return self._exact(value, DispatchOutcomeRecordIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskWorkflowTransitionRecord_request_correlation_identity(
        self, value: _RunValue
    ) -> SimulationExecutionRequestCorrelationIdentity | None:
        if type(value) is SimulationExecutionRequestCorrelationIdentity:
            return self._exact(value, SimulationExecutionRequestCorrelationIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_WorkflowRun_transitions_item(
        self, value: _RunValue
    ) -> TaskWorkflowTransitionRecord | ScientificDecisionWorkflowTransitionRecord:
        if type(value) is TaskWorkflowTransitionRecord:
            return self._exact(value, TaskWorkflowTransitionRecord)
        if type(value) is ScientificDecisionWorkflowTransitionRecord:
            return self._exact(value, ScientificDecisionWorkflowTransitionRecord)
        raise TypeError("wrong closed field variant")


class _WorkflowSourceCodecFailure(Exception):
    """Carry a complete nested codec failure across local wire traversal only."""

    def __init__(
        self,
        failure: WorkflowPersistenceFailure,
        status: Literal["incompatible", "invalid", "corrupt", "error"] = "corrupt",
    ) -> None:
        super().__init__("nested source codec did not produce a complete value")
        self.failure = failure
        self.status = status


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowResultValueSerializer:
    """Lossless version-one codec for two exact Workflow-owned result families.

    Parameters
    ----------
    source_codec
        Explicit effect-free, operationally immutable source codec implementing
        ``WorkflowResultValueCodec``. Application composition supplies the QE codec.
        It must support only exact concrete sources, never protocol stand-ins.
        The dependency is retained without a registry, discovery or inward import.

    Notes
    -----
    ``workflow-result:1`` uses canonical sorted compact ASCII JSON without newline,
    explicit ``type``/``fields`` records and nominal tags. Decisions retain every
    field, including verbatim Unicode response and opaque owning content identity;
    that label is compared, not reinterpreted as a hash. Sets retain ordered complete
    source envelopes with canonical base64 payload bytes. Their content identity is
    ``workflow-result:1:sha256:<digest>`` over the complete payload. A separate SHA-256
    digest always binds bytes. Nested decode/re-encode must agree on every envelope
    field. Unknown schemas/types are incompatible; invalid known wire is corrupt.
    No native I/O, scientific transformation, authority interpretation or replay occurs.
    This codec does not serialize a complete WorkflowRun or retain an identity cache.

    Raises
    ------
    TypeError
        ``source_codec`` does not implement the explicit codec port.
    """

    source_codec: WorkflowResultValueCodec

    def __post_init__(self) -> None:
        """Require the explicit source port without discovering its implementation."""
        if not isinstance(self.source_codec, WorkflowResultValueCodec):
            raise TypeError("source_codec must implement WorkflowResultValueCodec")

    def encode(self, value: ResultObject) -> WorkflowResultValueEncodeResult:
        """Encode a complete decision or normalized set with exact source envelopes.

        Parameters
        ----------
        value
            Workflow-facing result; only the two exact supported classes encode.

        Returns
        -------
        WorkflowResultValueEncodeResult
            Complete envelope or incompatible/invalid/error without a partial value.
            Nested codec failures retain their complete diagnostic evidence.

        Raises
        ------
        TypeError
            Input does not expose an exact nominal ResultObject identity.
        """
        if (
            not isinstance(value, ResultObject)
            or type(value.identity) is not ResultObjectIdentity
        ):
            raise TypeError("value must expose an exact ResultObjectIdentity")
        if (
            type(value) is not ScientificDecisionResolution
            and type(value) is not NormalizedObservationSet
        ):
            return WorkflowResultValueEncodeResult(
                status="incompatible",
                failure=self._failure(
                    "encode",
                    WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
                    (value.identity.value,),
                ),
            )
        try:
            payload = self._payload(value)
            digest = hashlib.sha256(payload).hexdigest()
            tag = (
                "ScientificDecisionResolution"
                if type(value) is ScientificDecisionResolution
                else "NormalizedObservationSet"
            )
            content = (
                value.content_identity
                if type(value) is ScientificDecisionResolution
                else ResultObjectContentIdentity(f"workflow-result:1:sha256:{digest}")
            )
            return WorkflowResultValueEncodeResult(
                status="encoded",
                encoded=WorkflowEncodedResultValue(
                    result_identity=value.identity,
                    concrete_type_identity=ResultObjectTypeIdentity(
                        f"ksdft2effmass.workflows.{tag}:1"
                    ),
                    owning_domain_identity=ResultObjectDomainIdentity(
                        "ksdft2effmass.workflows"
                    ),
                    schema_identity="workflow-result:1",
                    content_identity=content,
                    payload=payload,
                    payload_digest=digest,
                ),
            )
        except _WorkflowSourceCodecFailure as error:
            return WorkflowResultValueEncodeResult(
                status="invalid" if error.status == "corrupt" else error.status,
                failure=error.failure,
            )
        except MemoryError, RecursionError:
            failure = self._failure(
                "encode",
                WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
                (value.identity.value,),
            )
        except TypeError, ValueError, OverflowError:
            failure = self._failure(
                "encode",
                WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                (value.identity.value,),
            )
        except Exception:
            failure = self._failure(
                "encode",
                WorkflowPersistenceFailureCode.CODEC_ERROR,
                (value.identity.value,),
            )
        status: Literal["incompatible", "invalid", "error"] = "invalid"
        if failure.code in (
            WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
            WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
        ):
            status = "incompatible"
        elif failure.code in (
            WorkflowPersistenceFailureCode.CODEC_ERROR,
            WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
        ):
            status = "error"
        return WorkflowResultValueEncodeResult(status=status, failure=failure)

    def decode(
        self, value: WorkflowEncodedResultValue
    ) -> WorkflowResultValueDecodeResult:
        """Reconstruct complete immutable values after exact envelope agreement.

        Parameters
        ----------
        value
            Exact complete content-bound envelope in a supported schema and type.

        Returns
        -------
        WorkflowResultValueDecodeResult
            Concrete value or incompatible/corrupt/error evidence. Missing, extra or
            duplicate fields, noncanonical bytes, wrong tags and constructor invariant
            failures never return a partial result. Nested failures are preserved.

        Raises
        ------
        TypeError
            Input is not an exact WorkflowEncodedResultValue.
        """
        if type(value) is not WorkflowEncodedResultValue:
            raise TypeError("value must be WorkflowEncodedResultValue")
        inputs = (
            value.result_identity.value,
            value.schema_identity,
            value.concrete_type_identity.value,
        )
        if value.schema_identity != "workflow-result:1":
            return WorkflowResultValueDecodeResult(
                status="incompatible",
                failure=self._failure(
                    "decode", WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION, inputs
                ),
            )
        label = value.concrete_type_identity.value
        if label not in (
            "ksdft2effmass.workflows.ScientificDecisionResolution:1",
            "ksdft2effmass.workflows.NormalizedObservationSet:1",
        ):
            return WorkflowResultValueDecodeResult(
                status="incompatible",
                failure=self._failure(
                    "decode", WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE, inputs
                ),
            )
        try:
            if value.owning_domain_identity.value != "ksdft2effmass.workflows":
                raise _WorkflowSourceCodecFailure(
                    self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                        inputs,
                    )
                )
            # Exact json callbacks close the representation union before typed parsing.
            wire = cast(
                _ResultJson,
                json.loads(
                    value.payload.decode("ascii"),
                    object_pairs_hook=self._unique_object,
                    parse_int=self._reject_number,
                    parse_float=self._reject_number,
                    parse_constant=self._reject_number,
                ),
            )
            result: _WorkflowValue
            if label == "ksdft2effmass.workflows.ScientificDecisionResolution:1":
                result = self._decode_decision(wire)
                content = result.content_identity
            else:
                fields = self._fields(
                    wire, "NormalizedObservationSet", ("identity", "sources")
                )
                sources = fields["sources"]
                if not isinstance(sources, list):
                    raise TypeError("sources must be an ordered array")
                result = NormalizedObservationSet(
                    identity=ResultObjectIdentity(
                        self._label(fields["identity"], "ResultObjectIdentity")
                    ),
                    sources=tuple(self._decode_source(item) for item in sources),
                )
                content = ResultObjectContentIdentity(
                    f"workflow-result:1:sha256:{hashlib.sha256(value.payload).hexdigest()}"
                )
            if result.identity != value.result_identity:
                raise _WorkflowSourceCodecFailure(
                    self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                        inputs,
                    )
                )
            if (
                content != value.content_identity
                or hashlib.sha256(value.payload).hexdigest() != value.payload_digest
            ):
                raise _WorkflowSourceCodecFailure(
                    self._failure(
                        "decode",
                        WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                        inputs,
                    )
                )
            if self._payload(result) != value.payload:
                raise ValueError("noncanonical complete payload")
            return WorkflowResultValueDecodeResult(status="decoded", value=result)
        except _WorkflowSourceCodecFailure as error:
            return WorkflowResultValueDecodeResult(
                status="corrupt" if error.status == "invalid" else error.status,
                failure=error.failure,
            )
        except MemoryError, RecursionError:
            failure = self._failure(
                "decode", WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT, inputs
            )
        except TypeError, ValueError, OverflowError, KeyError:
            failure = self._failure(
                "decode",
                WorkflowPersistenceFailureCode.MALFORMED_REPRESENTATION,
                inputs,
            )
        except Exception:
            failure = self._failure(
                "decode", WorkflowPersistenceFailureCode.CODEC_ERROR, inputs
            )
        status: Literal["incompatible", "corrupt", "error"] = "corrupt"
        if failure.code in (
            WorkflowPersistenceFailureCode.UNSUPPORTED_TYPE,
            WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
        ):
            status = "incompatible"
        elif failure.code in (
            WorkflowPersistenceFailureCode.CODEC_ERROR,
            WorkflowPersistenceFailureCode.REPRESENTATION_LIMIT,
        ):
            status = "error"
        return WorkflowResultValueDecodeResult(status=status, failure=failure)

    @staticmethod
    def _failure(
        phase: str, code: WorkflowPersistenceFailureCode, identities: tuple[str, ...]
    ) -> WorkflowPersistenceFailure:
        return WorkflowPersistenceFailure(
            implementation_identity="ksdft2effmass.workflows.WorkflowResultValueSerializer:1",
            phase=phase,
            code=code,
            input_identities=identities,
            expected="complete canonical Workflow value and matching envelope",
            observed=code.value,
            diagnostic="Workflow result codec did not produce a complete value",
            claim_boundary="software representation only; no authority or science",
        )

    @staticmethod
    def _unique_object(pairs: list[tuple[str, _ResultJson]]) -> dict[str, _ResultJson]:
        """Own json's exact object-pairs hook, rejecting duplicate members."""
        result: dict[str, _ResultJson] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate member")
            result[key] = value
        return result

    @staticmethod
    def _reject_number(token: str) -> Never:
        """Own json numeric hooks; raw numeric tokens are outside this wire."""
        raise ValueError("untagged numeric token")

    @staticmethod
    def _record(tag: str, fields: dict[str, _ResultJson]) -> _ResultJson:
        return {"type": tag, "fields": fields}

    @classmethod
    def _nominal(cls, tag: str, value: str) -> _ResultJson:
        return cls._record(tag, {"value": value})

    @staticmethod
    def _fields(
        value: _ResultJson, tag: str, names: tuple[str, ...]
    ) -> dict[str, _ResultJson]:
        if (
            not isinstance(value, dict)
            or set(value) != {"type", "fields"}
            or value["type"] != tag
        ):
            raise ValueError("wrong record shape or tag")
        fields = value["fields"]
        if not isinstance(fields, dict) or set(fields) != set(names):
            raise ValueError("wrong field inventory")
        return fields

    @staticmethod
    def _string(value: _ResultJson) -> str:
        if type(value) is not str:
            raise TypeError("expected exact string")
        return value

    @classmethod
    def _label(cls, value: _ResultJson, tag: str) -> str:
        return cls._string(cls._fields(value, tag, ("value",))["value"])

    def _payload(self, value: _WorkflowValue) -> bytes:
        if type(value) is ScientificDecisionResolution:
            wire = self._decision(value)
        elif type(value) is NormalizedObservationSet:
            # Reconstruct the set to recheck membership/provenance before encoding.
            checked = NormalizedObservationSet(
                identity=value.identity, sources=value.sources
            )
            wire = self._record(
                "NormalizedObservationSet",
                {
                    "identity": self._nominal(
                        "ResultObjectIdentity", checked.identity.value
                    ),
                    "sources": [
                        self._encode_source(source) for source in checked.sources
                    ],
                },
            )
        else:
            raise TypeError("unsupported exact Workflow result type")
        return json.dumps(
            wire,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("ascii")

    def _encode_source(self, source: NormalizedObservationSource) -> _ResultJson:
        result = self.source_codec.encode(source)
        if result.encoded is None:
            assert result.failure is not None
            if result.status == "encoded":
                raise ValueError("successful source codec omitted its envelope")
            raise _WorkflowSourceCodecFailure(result.failure, result.status)
        envelope = result.encoded
        if envelope.result_identity != source.identity:
            raise _WorkflowSourceCodecFailure(
                self._failure(
                    "encode",
                    WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                    (source.identity.value,),
                )
            )
        wire = self._record(
            "WorkflowEncodedResultValue",
            {
                "result_identity": self._nominal(
                    "ResultObjectIdentity", envelope.result_identity.value
                ),
                "concrete_type_identity": self._nominal(
                    "ResultObjectTypeIdentity", envelope.concrete_type_identity.value
                ),
                "owning_domain_identity": self._nominal(
                    "ResultObjectDomainIdentity", envelope.owning_domain_identity.value
                ),
                "schema_identity": envelope.schema_identity,
                "content_identity": self._nominal(
                    "ResultObjectContentIdentity", envelope.content_identity.value
                ),
                "payload": self._nominal(
                    "bytes", base64.b64encode(envelope.payload).decode("ascii")
                ),
                "payload_digest": envelope.payload_digest,
            },
        )
        # A source success must reconstruct as a source and bind identical bytes.
        self._decode_source(wire)
        return wire

    def _decode_source(self, wire: _ResultJson) -> NormalizedObservationSource:
        fields = self._fields(
            wire,
            "WorkflowEncodedResultValue",
            (
                "result_identity",
                "concrete_type_identity",
                "owning_domain_identity",
                "schema_identity",
                "content_identity",
                "payload",
                "payload_digest",
            ),
        )
        text = self._label(fields["payload"], "bytes")
        payload = base64.b64decode(text, validate=True)
        if base64.b64encode(payload).decode("ascii") != text:
            raise ValueError("noncanonical base64")
        envelope = WorkflowEncodedResultValue(
            result_identity=ResultObjectIdentity(
                self._label(fields["result_identity"], "ResultObjectIdentity")
            ),
            concrete_type_identity=ResultObjectTypeIdentity(
                self._label(
                    fields["concrete_type_identity"], "ResultObjectTypeIdentity"
                )
            ),
            owning_domain_identity=ResultObjectDomainIdentity(
                self._label(
                    fields["owning_domain_identity"], "ResultObjectDomainIdentity"
                )
            ),
            schema_identity=self._string(fields["schema_identity"]),
            content_identity=ResultObjectContentIdentity(
                self._label(fields["content_identity"], "ResultObjectContentIdentity")
            ),
            payload=payload,
            payload_digest=self._string(fields["payload_digest"]),
        )
        decoded = self.source_codec.decode(envelope)
        if decoded.value is None:
            assert decoded.failure is not None
            if decoded.status == "decoded":
                raise ValueError("successful source codec omitted its value")
            raise _WorkflowSourceCodecFailure(decoded.failure, decoded.status)
        source = decoded.value
        if (
            not isinstance(source, NormalizedObservationSource)
            or source.identity != envelope.result_identity
        ):
            raise _WorkflowSourceCodecFailure(
                self._failure(
                    "decode",
                    WorkflowPersistenceFailureCode.IDENTITY_MISMATCH,
                    (envelope.result_identity.value,),
                )
            )
        encoded = self.source_codec.encode(source)
        if encoded.encoded is None:
            assert encoded.failure is not None
            if encoded.status == "encoded":
                raise ValueError("successful source codec omitted its envelope")
            raise _WorkflowSourceCodecFailure(encoded.failure, encoded.status)
        if encoded.encoded != envelope:
            raise _WorkflowSourceCodecFailure(
                self._failure(
                    "decode",
                    WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                    (source.identity.value,),
                )
            )
        return source

    @classmethod
    def _decision(cls, value: ScientificDecisionResolution) -> _ResultJson:
        producer = value.producer_provenance
        wire = cls._record(
            "ScientificDecisionResolution",
            {
                "identity": cls._nominal("ResultObjectIdentity", value.identity.value),
                "content_identity": cls._nominal(
                    "ResultObjectContentIdentity", value.content_identity.value
                ),
                "request_identity": cls._nominal(
                    "ScientificDecisionRequestIdentity", value.request_identity.value
                ),
                "verbatim_response": value.verbatim_response,
                "normalized_option_identity": cls._nominal(
                    "ScientificDecisionOptionIdentity",
                    value.normalized_option_identity.value,
                ),
                "response_source_identity": cls._nominal(
                    "ResponseSourceIdentity", value.response_source_identity.value
                ),
                "authority_context_identity": cls._nominal(
                    "AuthorityContextIdentity", value.authority_context_identity.value
                ),
                "boundary_receipt_identity": None
                if value.boundary_receipt_identity is None
                else cls._nominal(
                    "BoundaryReceiptIdentity", value.boundary_receipt_identity.value
                ),
                "predecessor_resolution_identity": None
                if value.predecessor_resolution_identity is None
                else cls._nominal(
                    "ResultObjectIdentity", value.predecessor_resolution_identity.value
                ),
                "supersedes_resolution_identity": None
                if value.supersedes_resolution_identity is None
                else cls._nominal(
                    "ResultObjectIdentity", value.supersedes_resolution_identity.value
                ),
                "producer_provenance": cls._record(
                    "RepresentedScientificDecisionIngressProducer",
                    {
                        "identity": cls._nominal(
                            "ResultProducerProvenanceIdentity", producer.identity.value
                        ),
                        "workflow_identity": cls._nominal(
                            "WorkflowIdentity", producer.workflow_identity.value
                        ),
                        "workflow_run_identity": cls._nominal(
                            "WorkflowRunIdentity", producer.workflow_run_identity.value
                        ),
                        "request_identity": cls._nominal(
                            "ScientificDecisionRequestIdentity",
                            producer.request_identity.value,
                        ),
                        "transition_record_identity": cls._nominal(
                            "ScientificDecisionTransitionRecordIdentity",
                            producer.transition_record_identity.value,
                        ),
                        "recorder_identity": cls._nominal(
                            "ScientificDecisionRecorderIdentity",
                            producer.recorder_identity.value,
                        ),
                        "response_source_identity": cls._nominal(
                            "ResponseSourceIdentity",
                            producer.response_source_identity.value,
                        ),
                        "authority_context_identity": cls._nominal(
                            "AuthorityContextIdentity",
                            producer.authority_context_identity.value,
                        ),
                        "resolution_identity": cls._nominal(
                            "ResultObjectIdentity", producer.resolution_identity.value
                        ),
                    },
                ),
            },
        )
        cls._decode_decision(wire)
        return wire

    @classmethod
    def _decode_decision(cls, wire: _ResultJson) -> ScientificDecisionResolution:
        fields = cls._fields(
            wire,
            "ScientificDecisionResolution",
            (
                "identity",
                "content_identity",
                "request_identity",
                "verbatim_response",
                "normalized_option_identity",
                "response_source_identity",
                "authority_context_identity",
                "boundary_receipt_identity",
                "predecessor_resolution_identity",
                "supersedes_resolution_identity",
                "producer_provenance",
            ),
        )
        producer = cls._fields(
            fields["producer_provenance"],
            "RepresentedScientificDecisionIngressProducer",
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
        receipt = fields["boundary_receipt_identity"]
        predecessor = fields["predecessor_resolution_identity"]
        supersedes = fields["supersedes_resolution_identity"]
        return ScientificDecisionResolution(
            identity=ResultObjectIdentity(
                cls._label(fields["identity"], "ResultObjectIdentity")
            ),
            content_identity=ResultObjectContentIdentity(
                cls._label(fields["content_identity"], "ResultObjectContentIdentity")
            ),
            request_identity=ScientificDecisionRequestIdentity(
                cls._label(
                    fields["request_identity"], "ScientificDecisionRequestIdentity"
                )
            ),
            verbatim_response=cls._string(fields["verbatim_response"]),
            normalized_option_identity=ScientificDecisionOptionIdentity(
                cls._label(
                    fields["normalized_option_identity"],
                    "ScientificDecisionOptionIdentity",
                )
            ),
            response_source_identity=ResponseSourceIdentity(
                cls._label(fields["response_source_identity"], "ResponseSourceIdentity")
            ),
            authority_context_identity=AuthorityContextIdentity(
                cls._label(
                    fields["authority_context_identity"], "AuthorityContextIdentity"
                )
            ),
            boundary_receipt_identity=None
            if receipt is None
            else BoundaryReceiptIdentity(
                cls._label(receipt, "BoundaryReceiptIdentity")
            ),
            predecessor_resolution_identity=None
            if predecessor is None
            else ResultObjectIdentity(cls._label(predecessor, "ResultObjectIdentity")),
            supersedes_resolution_identity=None
            if supersedes is None
            else ResultObjectIdentity(cls._label(supersedes, "ResultObjectIdentity")),
            producer_provenance=RepresentedScientificDecisionIngressProducer(
                identity=ResultProducerProvenanceIdentity(
                    cls._label(producer["identity"], "ResultProducerProvenanceIdentity")
                ),
                workflow_identity=WorkflowIdentity(
                    cls._label(producer["workflow_identity"], "WorkflowIdentity")
                ),
                workflow_run_identity=WorkflowRunIdentity(
                    cls._label(producer["workflow_run_identity"], "WorkflowRunIdentity")
                ),
                request_identity=ScientificDecisionRequestIdentity(
                    cls._label(
                        producer["request_identity"],
                        "ScientificDecisionRequestIdentity",
                    )
                ),
                transition_record_identity=ScientificDecisionTransitionRecordIdentity(
                    cls._label(
                        producer["transition_record_identity"],
                        "ScientificDecisionTransitionRecordIdentity",
                    )
                ),
                recorder_identity=ScientificDecisionRecorderIdentity(
                    cls._label(
                        producer["recorder_identity"],
                        "ScientificDecisionRecorderIdentity",
                    )
                ),
                response_source_identity=ResponseSourceIdentity(
                    cls._label(
                        producer["response_source_identity"], "ResponseSourceIdentity"
                    )
                ),
                authority_context_identity=AuthorityContextIdentity(
                    cls._label(
                        producer["authority_context_identity"],
                        "AuthorityContextIdentity",
                    )
                ),
                resolution_identity=ResultObjectIdentity(
                    cls._label(producer["resolution_identity"], "ResultObjectIdentity")
                ),
            ),
        )
