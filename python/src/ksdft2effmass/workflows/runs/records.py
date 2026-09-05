"""Immutable records retained by one represented Workflow run."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBinding,
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetFiringOutcomeKind,
    ColoredPetriNetFiringResult,
    ColoredPetriNetTransitionIdentity,
)

from ..artifacts import ResultArtifactRelationIdentity
from ..model import (
    AttemptIdentity,
    OperationIdentity,
    ResultObject,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from .identities import (
    AuthorityContextIdentity,
    AuthorityReservationOutcomeIdentity,
    BoundaryReceiptIdentity,
    ChildWorkflowCreationIdempotencyIdentity,
    DispatchCreationIdempotencyIdentity,
    DispatchDestinationIdentity,
    DispatchOutcomeRecordIdentity,
    DispatchResourceScopeIdentity,
    ExecutionGrantIdentity,
    ExecutionGrantRevisionIdentity,
    ExternalProducerAttemptIdentity,
    ExternalResultProducerIdentity,
    HumanResultAuthorIdentity,
    NestedWorkflowInvocationIdentity,
    NestedWorkflowMembershipIdentity,
    NestedWorkflowObservationIdentity,
    ObligationDispositionIdentity,
    ObligationIdentity,
    ResponseSourceIdentity,
    ResultDependencyIdentity,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectReferenceIdentity,
    ResultObjectTypeIdentity,
    ResultProducerEvidenceIdentity,
    ResultProducerProvenanceIdentity,
    ResultProductionRecordIdentity,
    RetainedResultSourceIdentity,
    ScientificDecisionOptionIdentity,
    ScientificDecisionRecorderIdentity,
    ScientificDecisionRequestIdentity,
    ScientificDecisionTransitionRecordIdentity,
    ScientificExecutionAuthoritySnapshotIdentity,
    ScientificExecutionAuthorityStateIdentity,
    ScientificExecutorIdentity,
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
    WorkflowRunRevisionIdentity,
    WorkflowRuntimeBundleIdentity,
    WorkflowTransitionSequenceIdentity,
)


class TaskAttemptStatus(StrEnum):
    """Closed represented states of one bounded Task attempt."""

    STARTED = "started"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskAttempt:
    """Record one append-only state observation for a stable Task attempt.

    Parameters
    ----------
    identity
        Unique identity of this state record. Multiple records may share the stable
        ``attempt_identity`` but never this identity.
    workflow_run_identity
        Exact represented run that owns this state record.
    task_instance_identity
        Exact run-scoped Task instance being attempted.
    activation_identity
        Exact activation that initiated this attempt.
    operation_identity
        Intended operation identity. A retry uses another operation identity.
    attempt_identity
        Stable identity shared by every state record for this bounded attempt.
    status
        State represented by this record.
    predecessor_attempt_record_identity
        Immediately preceding state record for the same stable attempt. It is absent
        only on the initial ``started`` record.
    retry_of_attempt_identity
        Earlier stable attempt explicitly retried by this attempt, or ``None``. It is
        permitted only on the initial ``started`` record and never equals this
        attempt's identity.
    child_workflow_run_identity
        Distinct child run correlated to a nested Workflow attempt, otherwise
        ``None``. The record does not own child state.

    Notes
    -----
    Later state never replaces an earlier record. A terminal record appends after the
    initial record and names it as predecessor.
    """

    identity: TaskAttemptRecordIdentity
    workflow_run_identity: WorkflowRunIdentity
    task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    status: TaskAttemptStatus
    predecessor_attempt_record_identity: TaskAttemptRecordIdentity | None = None
    retry_of_attempt_identity: AttemptIdentity | None = None
    child_workflow_run_identity: WorkflowRunIdentity | None = None

    def __post_init__(self) -> None:
        """Validate nominal fields and intrinsic append-only variant rules."""
        expected = (
            (self.identity, TaskAttemptRecordIdentity, "identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.status) is not TaskAttemptStatus:
            raise TypeError("status must be TaskAttemptStatus")
        predecessor = self.predecessor_attempt_record_identity
        if (
            predecessor is not None
            and type(predecessor) is not TaskAttemptRecordIdentity
        ):
            raise TypeError(
                "predecessor_attempt_record_identity must be "
                "TaskAttemptRecordIdentity or None"
            )
        if predecessor == self.identity:
            raise ValueError(
                "an attempt state record cannot identify itself as predecessor"
            )
        retry = self.retry_of_attempt_identity
        if retry is not None and type(retry) is not AttemptIdentity:
            raise TypeError("retry_of_attempt_identity must be AttemptIdentity or None")
        child_run = self.child_workflow_run_identity
        if child_run is not None and type(child_run) is not WorkflowRunIdentity:
            raise TypeError(
                "child_workflow_run_identity must be WorkflowRunIdentity or None"
            )
        if retry == self.attempt_identity:
            raise ValueError("an attempt cannot retry itself")
        if self.status is TaskAttemptStatus.STARTED:
            if predecessor is not None:
                raise ValueError(
                    "an initial started record cannot have a state predecessor"
                )
            return
        if predecessor is None:
            raise ValueError("a terminal attempt record requires its state predecessor")
        if retry is not None:
            raise ValueError(
                "retry_of_attempt_identity belongs only on started records"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskInvocationFailure:
    """Retain one structured Task-domain failure without interpreting its meaning.

    Parameters
    ----------
    identity
        Exact failure identity.
    code
        Nonempty stable code owned by the producing Task domain.
    operation_phase
        Nonempty phase in which failure was established.
    diagnostic
        Sanitized nonempty diagnostic.  Credentials and restricted data are
        prohibited by the surrounding project policy.
    retryable
        ``True`` or ``False`` only when explicitly established, otherwise ``None``.
    claim_boundary
        Nonempty immutable statements limiting what this failure establishes.
    """

    identity: TaskInvocationFailureIdentity
    code: str
    operation_phase: str
    diagnostic: str
    retryable: bool | None
    claim_boundary: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact structured failure state."""
        if type(self.identity) is not TaskInvocationFailureIdentity:
            raise TypeError("identity must be TaskInvocationFailureIdentity")
        for name in ("code", "operation_phase", "diagnostic"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must not be empty")
        if self.retryable is not None and type(self.retryable) is not bool:
            raise TypeError("retryable must be bool or None")
        if type(self.claim_boundary) is not tuple or any(
            type(value) is not str for value in self.claim_boundary
        ):
            raise TypeError("claim_boundary must be a tuple of strings")
        if not self.claim_boundary or any(not value for value in self.claim_boundary):
            raise ValueError("claim_boundary must contain nonempty strings")


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskFailureRecord:
    """Correlate one structured Task failure to exact WorkflowRun state.

    Parameters
    ----------
    identity, workflow_run_identity, task_instance_identity
        Exact failure record, represented run, and failed Task instance.
    activation_identity, operation_identity, attempt_identity
        Exact failed invocation identities.
    terminal_attempt_record_identity
        Exact rejected terminal attempt-state record.
    failure
        Structured domain-owned :class:`TaskInvocationFailure`.
    request_identity
        Exact simulation request for a dispatch failure, otherwise ``None``.
    child_workflow_run_identity
        Exact child run for a nested failure, otherwise ``None``.
    claim_boundary
        Nonempty statements prohibiting a successful-firing interpretation.

    Notes
    -----
    This record owns correlation only. The producing Task domain owns the failure-code
    meaning. Request and child-run identities are present only for their applicable
    invocation origin.
    """

    identity: TaskFailureRecordIdentity
    workflow_run_identity: WorkflowRunIdentity
    task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    terminal_attempt_record_identity: TaskAttemptRecordIdentity
    failure: TaskInvocationFailure
    request_identity: SimulationExecutionRequestIdentity | None = None
    child_workflow_run_identity: WorkflowRunIdentity | None = None
    claim_boundary: tuple[str, ...] = (
        "no successful generic firing is represented by this failure",
    )

    def __post_init__(self) -> None:
        """Validate exact failure correlations and the no-success claim boundary."""
        expected = (
            (self.identity, TaskFailureRecordIdentity, "identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (
                self.terminal_attempt_record_identity,
                TaskAttemptRecordIdentity,
                "terminal_attempt_record_identity",
            ),
            (self.failure, TaskInvocationFailure, "failure"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        request = self.request_identity
        if (
            request is not None
            and type(request) is not SimulationExecutionRequestIdentity
        ):
            raise TypeError(
                "request_identity must be SimulationExecutionRequestIdentity or None"
            )
        child_run = self.child_workflow_run_identity
        if child_run is not None and type(child_run) is not WorkflowRunIdentity:
            raise TypeError(
                "child_workflow_run_identity must be WorkflowRunIdentity or None"
            )
        if type(self.claim_boundary) is not tuple or any(
            type(value) is not str for value in self.claim_boundary
        ):
            raise TypeError("claim_boundary must be a tuple of strings")
        if not self.claim_boundary or any(not value for value in self.claim_boundary):
            raise ValueError("claim_boundary must contain nonempty strings")


@dataclass(frozen=True, slots=True, kw_only=True)
class RepresentedTaskResultProducer:
    """Identify the exact represented Task production of one ResultObject.

    Parameters
    ----------
    identity
        Exact producer-provenance record identity.
    workflow_identity, workflow_run_identity, task_instance_identity
        Exact Workflow, represented run, and producing Task instance.
    activation_identity, operation_identity, attempt_identity
        Exact producing invocation identities.
    terminal_attempt_record_identity, outcome_identity, production_identity
        Exact confirmed terminal state, invocation outcome, and result-production
        record. Replay requires all three records to exist and correlate.
    """

    identity: ResultProducerProvenanceIdentity
    workflow_identity: WorkflowIdentity
    workflow_run_identity: WorkflowRunIdentity
    task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    terminal_attempt_record_identity: TaskAttemptRecordIdentity
    outcome_identity: TaskInvocationOutcomeIdentity
    production_identity: ResultProductionRecordIdentity

    def __post_init__(self) -> None:
        """Validate exact represented Task producer identities."""
        expected = (
            (self.identity, ResultProducerProvenanceIdentity, "identity"),
            (self.workflow_identity, WorkflowIdentity, "workflow_identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (
                self.terminal_attempt_record_identity,
                TaskAttemptRecordIdentity,
                "terminal_attempt_record_identity",
            ),
            (self.outcome_identity, TaskInvocationOutcomeIdentity, "outcome_identity"),
            (
                self.production_identity,
                ResultProductionRecordIdentity,
                "production_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")


@dataclass(frozen=True, slots=True, kw_only=True)
class RepresentedScientificDecisionIngressProducer:
    """Identify no-Task production of one scientific-decision resolution.

    Parameters
    ----------
    identity
        Exact producer-provenance record identity.
    workflow_identity, workflow_run_identity, request_identity
        Exact Workflow, represented run, and scientific-decision request.
    transition_record_identity, resolution_identity
        Exact decision-origin transition and immutable resolution ResultObject.
    recorder_identity, response_source_identity, authority_context_identity
        Exact recorder implementation, direct response source, and authority context.

    Notes
    -----
    The closed record deliberately has no Task-instance, activation, operation,
    attempt, or Task result-production fields.
    """

    identity: ResultProducerProvenanceIdentity
    workflow_identity: WorkflowIdentity
    workflow_run_identity: WorkflowRunIdentity
    request_identity: ScientificDecisionRequestIdentity
    transition_record_identity: ScientificDecisionTransitionRecordIdentity
    recorder_identity: ScientificDecisionRecorderIdentity
    response_source_identity: ResponseSourceIdentity
    authority_context_identity: AuthorityContextIdentity
    resolution_identity: ResultObjectIdentity

    def __post_init__(self) -> None:
        """Validate exact no-Task decision-ingress provenance identities."""
        expected = (
            (self.identity, ResultProducerProvenanceIdentity, "identity"),
            (self.workflow_identity, WorkflowIdentity, "workflow_identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.request_identity,
                ScientificDecisionRequestIdentity,
                "request_identity",
            ),
            (
                self.transition_record_identity,
                ScientificDecisionTransitionRecordIdentity,
                "transition_record_identity",
            ),
            (
                self.recorder_identity,
                ScientificDecisionRecorderIdentity,
                "recorder_identity",
            ),
            (
                self.response_source_identity,
                ResponseSourceIdentity,
                "response_source_identity",
            ),
            (
                self.authority_context_identity,
                AuthorityContextIdentity,
                "authority_context_identity",
            ),
            (self.resolution_identity, ResultObjectIdentity, "resolution_identity"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")


@dataclass(frozen=True, slots=True, kw_only=True)
class ExternalResultProducer:
    """Retain actual non-Workflow producer evidence without fabricated lineage.

    Parameters
    ----------
    identity
        Exact producer-provenance record identity.
    external_producer_identity, producer_attempt_identity
        Exact external producer and actual producer-attempt identities.
    evidence_identities
        Nonempty unique evidence identities in lexical order.
    limitations
        Nonempty statements describing the retained provenance limitations.
    """

    identity: ResultProducerProvenanceIdentity
    external_producer_identity: ExternalResultProducerIdentity
    producer_attempt_identity: ExternalProducerAttemptIdentity
    evidence_identities: tuple[ResultProducerEvidenceIdentity, ...]
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact external producer evidence and explicit limitations."""
        expected = (
            (self.identity, ResultProducerProvenanceIdentity, "identity"),
            (
                self.external_producer_identity,
                ExternalResultProducerIdentity,
                "external_producer_identity",
            ),
            (
                self.producer_attempt_identity,
                ExternalProducerAttemptIdentity,
                "producer_attempt_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        self._validate_evidence_and_limitations()

    def _validate_evidence_and_limitations(self) -> None:
        """Validate canonical evidence identities and nonempty limitations."""
        evidence = self.evidence_identities
        if type(evidence) is not tuple or any(
            type(value) is not ResultProducerEvidenceIdentity for value in evidence
        ):
            raise TypeError(
                "evidence_identities must be a tuple of ResultProducerEvidenceIdentity"
            )
        if (
            not evidence
            or evidence != tuple(sorted(evidence, key=lambda value: value.value))
            or len(set(evidence)) != len(evidence)
        ):
            raise ValueError("evidence identities must be nonempty, unique, and sorted")
        if type(self.limitations) is not tuple or any(
            type(value) is not str for value in self.limitations
        ):
            raise TypeError("limitations must be a tuple of strings")
        if not self.limitations or any(not value for value in self.limitations):
            raise ValueError("limitations must contain nonempty strings")


@dataclass(frozen=True, slots=True, kw_only=True)
class ImportedRetainedResultProducer:
    """Retain one imported result's actual source evidence and limitations.

    Parameters
    ----------
    identity, source_identity
        Exact provenance-record and retained-source identities.
    evidence_identities
        Nonempty unique evidence identities in lexical order.
    limitations
        Nonempty statements describing the retained provenance limitations.
    """

    identity: ResultProducerProvenanceIdentity
    source_identity: RetainedResultSourceIdentity
    evidence_identities: tuple[ResultProducerEvidenceIdentity, ...]
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact retained-source evidence without inventing lineage."""
        if type(self.identity) is not ResultProducerProvenanceIdentity:
            raise TypeError("identity must be ResultProducerProvenanceIdentity")
        if type(self.source_identity) is not RetainedResultSourceIdentity:
            raise TypeError("source_identity must be RetainedResultSourceIdentity")
        evidence = self.evidence_identities
        if type(evidence) is not tuple or any(
            type(value) is not ResultProducerEvidenceIdentity for value in evidence
        ):
            raise TypeError(
                "evidence_identities must be a tuple of ResultProducerEvidenceIdentity"
            )
        if (
            not evidence
            or evidence != tuple(sorted(evidence, key=lambda value: value.value))
            or len(set(evidence)) != len(evidence)
        ):
            raise ValueError("evidence identities must be nonempty, unique, and sorted")
        if type(self.limitations) is not tuple or any(
            type(value) is not str for value in self.limitations
        ):
            raise TypeError("limitations must be a tuple of strings")
        if not self.limitations or any(not value for value in self.limitations):
            raise ValueError("limitations must contain nonempty strings")


@dataclass(frozen=True, slots=True, kw_only=True)
class HumanAuthoredResultProducer:
    """Retain one declared human-authored result and its actual evidence.

    Parameters
    ----------
    identity, author_identity, source_identity
        Exact provenance-record, declared author, and retained-source identities.
    evidence_identities
        Nonempty unique evidence identities in lexical order.
    limitations
        Nonempty statements describing the retained provenance limitations.
    """

    identity: ResultProducerProvenanceIdentity
    author_identity: HumanResultAuthorIdentity
    source_identity: RetainedResultSourceIdentity
    evidence_identities: tuple[ResultProducerEvidenceIdentity, ...]
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact author/source evidence without granting authority."""
        expected = (
            (self.identity, ResultProducerProvenanceIdentity, "identity"),
            (self.author_identity, HumanResultAuthorIdentity, "author_identity"),
            (
                self.source_identity,
                RetainedResultSourceIdentity,
                "source_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        evidence = self.evidence_identities
        if type(evidence) is not tuple or any(
            type(value) is not ResultProducerEvidenceIdentity for value in evidence
        ):
            raise TypeError(
                "evidence_identities must be a tuple of ResultProducerEvidenceIdentity"
            )
        if (
            not evidence
            or evidence != tuple(sorted(evidence, key=lambda value: value.value))
            or len(set(evidence)) != len(evidence)
        ):
            raise ValueError("evidence identities must be nonempty, unique, and sorted")
        if type(self.limitations) is not tuple or any(
            type(value) is not str for value in self.limitations
        ):
            raise TypeError("limitations must be a tuple of strings")
        if not self.limitations or any(not value for value in self.limitations):
            raise ValueError("limitations must contain nonempty strings")


@dataclass(frozen=True, slots=True, kw_only=True)
class UnknownLegacyResultProducer:
    """Retain bounded legacy provenance with actual evidence and limitations.

    Parameters
    ----------
    identity, source_identity
        Exact provenance-record and retained legacy-source identities.
    evidence_identities
        Nonempty unique evidence identities in lexical order.
    limitations
        Nonempty statements explaining the unknown historical provenance.
    """

    identity: ResultProducerProvenanceIdentity
    source_identity: RetainedResultSourceIdentity
    evidence_identities: tuple[ResultProducerEvidenceIdentity, ...]
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact bounded legacy evidence without fabricating a producer."""
        if type(self.identity) is not ResultProducerProvenanceIdentity:
            raise TypeError("identity must be ResultProducerProvenanceIdentity")
        if type(self.source_identity) is not RetainedResultSourceIdentity:
            raise TypeError("source_identity must be RetainedResultSourceIdentity")
        evidence = self.evidence_identities
        if type(evidence) is not tuple or any(
            type(value) is not ResultProducerEvidenceIdentity for value in evidence
        ):
            raise TypeError(
                "evidence_identities must be a tuple of ResultProducerEvidenceIdentity"
            )
        if (
            not evidence
            or evidence != tuple(sorted(evidence, key=lambda value: value.value))
            or len(set(evidence)) != len(evidence)
        ):
            raise ValueError("evidence identities must be nonempty, unique, and sorted")
        if type(self.limitations) is not tuple or any(
            type(value) is not str for value in self.limitations
        ):
            raise TypeError("limitations must be a tuple of strings")
        if not self.limitations or any(not value for value in self.limitations):
            raise ValueError("limitations must contain nonempty strings")


@dataclass(frozen=True, slots=True, kw_only=True)
class ResultObjectReference:
    """Correlate one concrete immutable ResultObject and its exact producer.

    Parameters
    ----------
    identity
        Exact aggregate-local reference identity.
    result
        Concrete immutable object implementing :class:`ResultObject`.
    concrete_type_identity, owning_domain_identity
        Exact versioned result contract and responsible domain identities.
    content_identity
        Exact immutable represented-content identity supplied by the owning domain.
    producer_provenance
        Exactly one represented-Task, represented-decision, external, imported,
        human-authored, or unknown-legacy producer record.
    """

    identity: ResultObjectReferenceIdentity
    result: ResultObject
    concrete_type_identity: ResultObjectTypeIdentity
    owning_domain_identity: ResultObjectDomainIdentity
    content_identity: ResultObjectContentIdentity
    producer_provenance: (
        RepresentedTaskResultProducer
        | RepresentedScientificDecisionIngressProducer
        | ExternalResultProducer
        | ImportedRetainedResultProducer
        | HumanAuthoredResultProducer
        | UnknownLegacyResultProducer
    )

    def __post_init__(self) -> None:
        """Validate the concrete result and represented producer fields."""
        if type(self.identity) is not ResultObjectReferenceIdentity:
            raise TypeError("identity must be ResultObjectReferenceIdentity")
        if not isinstance(self.result, ResultObject):
            raise TypeError("result must implement ResultObject")
        if type(self.result.identity) is not ResultObjectIdentity:
            raise TypeError("result identity must be ResultObjectIdentity")
        expected = (
            (
                self.concrete_type_identity,
                ResultObjectTypeIdentity,
                "concrete_type_identity",
            ),
            (
                self.owning_domain_identity,
                ResultObjectDomainIdentity,
                "owning_domain_identity",
            ),
            (
                self.content_identity,
                ResultObjectContentIdentity,
                "content_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.producer_provenance) not in {
            RepresentedTaskResultProducer,
            RepresentedScientificDecisionIngressProducer,
            ExternalResultProducer,
            ImportedRetainedResultProducer,
            HumanAuthoredResultProducer,
            UnknownLegacyResultProducer,
        }:
            raise TypeError("producer_provenance must be a closed producer variant")


@dataclass(frozen=True, slots=True, kw_only=True)
class ResultProductionRecord:
    """Record one exact confirmed Task result and generic output binding.

    Parameters
    ----------
    identity, workflow_run_identity, task_instance_identity
        Exact production record, represented run, and producing Task instance.
    activation_identity, operation_identity, attempt_identity
        Exact producing invocation identities.
    terminal_attempt_record_identity, outcome_identity
        Exact confirmed terminal attempt-state record and invocation outcome.
    result_reference_identity
        Exact produced ResultObject reference.
    result_artifact_relation_identities
        Unique result-to-artifact relations in lexical identity order.
    external_output_binding
        Exact generic external binding used by the successful firing input.
    """

    identity: ResultProductionRecordIdentity
    workflow_run_identity: WorkflowRunIdentity
    task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    terminal_attempt_record_identity: TaskAttemptRecordIdentity
    outcome_identity: TaskInvocationOutcomeIdentity
    result_reference_identity: ResultObjectReferenceIdentity
    result_artifact_relation_identities: tuple[ResultArtifactRelationIdentity, ...]
    external_output_binding: ColoredPetriNetBinding

    def __post_init__(self) -> None:
        """Validate exact production correlations and immutable relation ordering."""
        expected = (
            (self.identity, ResultProductionRecordIdentity, "identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (
                self.terminal_attempt_record_identity,
                TaskAttemptRecordIdentity,
                "terminal_attempt_record_identity",
            ),
            (self.outcome_identity, TaskInvocationOutcomeIdentity, "outcome_identity"),
            (
                self.result_reference_identity,
                ResultObjectReferenceIdentity,
                "result_reference_identity",
            ),
            (
                self.external_output_binding,
                ColoredPetriNetBinding,
                "external_output_binding",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        relations = self.result_artifact_relation_identities
        if type(relations) is not tuple or any(
            type(value) is not ResultArtifactRelationIdentity for value in relations
        ):
            raise TypeError(
                "result_artifact_relation_identities must be a tuple of "
                "ResultArtifactRelationIdentity"
            )
        if relations != tuple(sorted(relations, key=lambda value: value.value)) or len(
            set(relations)
        ) != len(relations):
            raise ValueError(
                "result artifact relation identities must be unique and sorted"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class ResultDependency:
    """Record one explicit ResultObject-to-Task input dependency edge.

    Parameters
    ----------
    identity, result_reference_identity
        Exact dependency and consumed ResultObject-reference identities.
    producer_workflow_run_identity
        Producing run for represented Workflow provenance, otherwise ``None``.
    consumer_workflow_run_identity, consumer_task_instance_identity
        Exact consuming run and Task instance.
    consumer_activation_identity
        Exact consuming activation when already activated, otherwise ``None``.
    input_name
        Nonempty Task input name matching the activation binding when present.
    """

    identity: ResultDependencyIdentity
    result_reference_identity: ResultObjectReferenceIdentity
    producer_workflow_run_identity: WorkflowRunIdentity | None
    consumer_workflow_run_identity: WorkflowRunIdentity
    consumer_task_instance_identity: TaskInstanceIdentity
    consumer_activation_identity: TaskActivationIdentity | None
    input_name: str

    def __post_init__(self) -> None:
        """Validate exact dependency endpoints without inferring membership."""
        expected = (
            (self.identity, ResultDependencyIdentity, "identity"),
            (
                self.result_reference_identity,
                ResultObjectReferenceIdentity,
                "result_reference_identity",
            ),
            (
                self.consumer_workflow_run_identity,
                WorkflowRunIdentity,
                "consumer_workflow_run_identity",
            ),
            (
                self.consumer_task_instance_identity,
                TaskInstanceIdentity,
                "consumer_task_instance_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        producer = self.producer_workflow_run_identity
        if producer is not None and type(producer) is not WorkflowRunIdentity:
            raise TypeError(
                "producer_workflow_run_identity must be WorkflowRunIdentity or None"
            )
        activation = self.consumer_activation_identity
        if activation is not None and type(activation) is not TaskActivationIdentity:
            raise TypeError(
                "consumer_activation_identity must be TaskActivationIdentity or None"
            )
        if type(self.input_name) is not str:
            raise TypeError("input_name must be a string")
        if not self.input_name:
            raise ValueError("input_name must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskWorkflowMembership:
    """Record ordinary membership of one Task instance in one Workflow run.

    Parameters
    ----------
    identity
        Exact membership-record identity.
    workflow_run_identity, workflow_identity
        Exact represented run and reusable Workflow definition.
    task_instance_identity
        Exact run-scoped member Task instance.

    Notes
    -----
    Membership establishes composition correlation only. It grants no prerequisite,
    activation, execution-authority, or successful-outcome claim.
    """

    identity: TaskWorkflowMembershipIdentity
    workflow_run_identity: WorkflowRunIdentity
    workflow_identity: WorkflowIdentity
    task_instance_identity: TaskInstanceIdentity

    def __post_init__(self) -> None:
        """Validate exact ordinary membership identities."""
        expected = (
            (self.identity, TaskWorkflowMembershipIdentity, "identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (self.workflow_identity, WorkflowIdentity, "workflow_identity"),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")


@dataclass(frozen=True, slots=True, kw_only=True)
class NestedWorkflowMembership:
    """Correlate one parent Task instance to one distinct child Workflow run.

    Parameters
    ----------
    identity
        Exact nested-membership record identity.
    parent_workflow_run_identity, parent_revision_identity
        Exact parent run and revision at the represented correlation boundary.
    parent_task_instance_identity
        Exact parent Task instance invoking the child.
    child_workflow_identity, child_workflow_run_identity
        Exact child Workflow definition and distinct child run.

    Notes
    -----
    The record contains identities only. The child marking, ordered history, and
    revisions remain owned by the distinct child aggregate and persistence stream.
    """

    identity: NestedWorkflowMembershipIdentity
    parent_workflow_run_identity: WorkflowRunIdentity
    parent_revision_identity: WorkflowRunRevisionIdentity
    parent_task_instance_identity: TaskInstanceIdentity
    child_workflow_identity: WorkflowIdentity
    child_workflow_run_identity: WorkflowRunIdentity

    def __post_init__(self) -> None:
        """Validate exact parent/child identities and distinct run ownership."""
        expected = (
            (self.identity, NestedWorkflowMembershipIdentity, "identity"),
            (
                self.parent_workflow_run_identity,
                WorkflowRunIdentity,
                "parent_workflow_run_identity",
            ),
            (
                self.parent_revision_identity,
                WorkflowRunRevisionIdentity,
                "parent_revision_identity",
            ),
            (
                self.parent_task_instance_identity,
                TaskInstanceIdentity,
                "parent_task_instance_identity",
            ),
            (
                self.child_workflow_identity,
                WorkflowIdentity,
                "child_workflow_identity",
            ),
            (
                self.child_workflow_run_identity,
                WorkflowRunIdentity,
                "child_workflow_run_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if self.parent_workflow_run_identity == self.child_workflow_run_identity:
            raise ValueError(
                "a nested child Workflow run must be distinct from its parent"
            )


class NestedWorkflowInvocationKind(StrEnum):
    """Closed represented observations of one nested Workflow invocation."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True, slots=True, kw_only=True)
class NestedWorkflowInvocation:
    """Correlate one parent invocation to one distinct child Workflow run.

    Parameters
    ----------
    identity
        Exact nested-invocation record identity.
    parent_workflow_run_identity, parent_revision_identity
        Exact parent run and represented revision.
    parent_task_instance_identity
        Exact parent Task instance.
    activation_identity, operation_identity, attempt_identity
        Exact parent invocation identities.
    attempt_record_identity
        Exact current parent attempt-state record.
    child_workflow_identity, child_workflow_run_identity
        Exact child definition and distinct child run.
    input_result_reference_identities
        Unique child-input references in lexical identity order.
    child_creation_idempotency_identity
        Exact child-creation request identity.
    kind
        Closed observation variant.
    terminal_observation_identity, terminal_child_revision_identity
        Terminal observation and replayed child revision when required by ``kind``.
    replay_equal_child_result_identity
        Exact child replay result for a confirmed invocation.
    exported_result_reference_identities
        Confirmed child exports in lexical identity order.
    export_admission_dependency_identities
        Explicit parent-admission dependencies corresponding one-to-one to exports.
    failure_record_identity
        Parent-retained failure record for a rejected invocation.
    reconciliation_identity_values
        Unique lexical reconciliation identities for an indeterminate invocation.

    Notes
    -----
    ``pending`` contains no terminal observation. This record neither creates nor
    executes the child, embeds child marking/history, performs a read, nor claims
    cross-run atomicity.
    """

    identity: NestedWorkflowInvocationIdentity
    parent_workflow_run_identity: WorkflowRunIdentity
    parent_revision_identity: WorkflowRunRevisionIdentity
    parent_task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    attempt_record_identity: TaskAttemptRecordIdentity
    child_workflow_identity: WorkflowIdentity
    child_workflow_run_identity: WorkflowRunIdentity
    input_result_reference_identities: tuple[ResultObjectReferenceIdentity, ...]
    child_creation_idempotency_identity: ChildWorkflowCreationIdempotencyIdentity
    kind: NestedWorkflowInvocationKind
    terminal_observation_identity: NestedWorkflowObservationIdentity | None = None
    terminal_child_revision_identity: WorkflowRunRevisionIdentity | None = None
    replay_equal_child_result_identity: WorkflowRunReplayResultIdentity | None = None
    exported_result_reference_identities: tuple[ResultObjectReferenceIdentity, ...] = ()
    export_admission_dependency_identities: tuple[ResultDependencyIdentity, ...] = ()
    failure_record_identity: TaskFailureRecordIdentity | None = None
    reconciliation_identity_values: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate exact correlations and the closed observation variant."""
        expected = (
            (self.identity, NestedWorkflowInvocationIdentity, "identity"),
            (
                self.parent_workflow_run_identity,
                WorkflowRunIdentity,
                "parent_workflow_run_identity",
            ),
            (
                self.parent_revision_identity,
                WorkflowRunRevisionIdentity,
                "parent_revision_identity",
            ),
            (
                self.parent_task_instance_identity,
                TaskInstanceIdentity,
                "parent_task_instance_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (
                self.attempt_record_identity,
                TaskAttemptRecordIdentity,
                "attempt_record_identity",
            ),
            (
                self.child_workflow_identity,
                WorkflowIdentity,
                "child_workflow_identity",
            ),
            (
                self.child_workflow_run_identity,
                WorkflowRunIdentity,
                "child_workflow_run_identity",
            ),
            (
                self.child_creation_idempotency_identity,
                ChildWorkflowCreationIdempotencyIdentity,
                "child_creation_idempotency_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if self.parent_workflow_run_identity == self.child_workflow_run_identity:
            raise ValueError(
                "a nested child Workflow run must be distinct from its parent"
            )
        if type(self.kind) is not NestedWorkflowInvocationKind:
            raise TypeError("kind must be NestedWorkflowInvocationKind")
        self._require_sorted_unique_identities(
            self.input_result_reference_identities,
            ResultObjectReferenceIdentity,
            "input_result_reference_identities",
        )
        self._require_sorted_unique_identities(
            self.exported_result_reference_identities,
            ResultObjectReferenceIdentity,
            "exported_result_reference_identities",
        )
        self._require_sorted_unique_identities(
            self.export_admission_dependency_identities,
            ResultDependencyIdentity,
            "export_admission_dependency_identities",
        )
        observation = self.terminal_observation_identity
        if observation is not None and type(observation) is not (
            NestedWorkflowObservationIdentity
        ):
            raise TypeError(
                "terminal_observation_identity must be "
                "NestedWorkflowObservationIdentity or None"
            )
        child_revision = self.terminal_child_revision_identity
        if child_revision is not None and type(child_revision) is not (
            WorkflowRunRevisionIdentity
        ):
            raise TypeError(
                "terminal_child_revision_identity must be "
                "WorkflowRunRevisionIdentity or None"
            )
        replay_result = self.replay_equal_child_result_identity
        if replay_result is not None and type(replay_result) is not (
            WorkflowRunReplayResultIdentity
        ):
            raise TypeError(
                "replay_equal_child_result_identity must be "
                "WorkflowRunReplayResultIdentity or None"
            )
        failure = self.failure_record_identity
        if failure is not None and type(failure) is not TaskFailureRecordIdentity:
            raise TypeError(
                "failure_record_identity must be TaskFailureRecordIdentity or None"
            )
        reconciliations = self.reconciliation_identity_values
        if type(reconciliations) is not tuple or any(
            type(value) is not str for value in reconciliations
        ):
            raise TypeError("reconciliation_identity_values must be a tuple of strings")
        if any(not value for value in reconciliations):
            raise ValueError("reconciliation identities must not be empty")
        if reconciliations != tuple(sorted(reconciliations)) or len(
            set(reconciliations)
        ) != len(reconciliations):
            raise ValueError("reconciliation identities must be sorted and unique")

        valid = {
            NestedWorkflowInvocationKind.PENDING: (
                observation is None
                and child_revision is None
                and replay_result is None
                and not self.exported_result_reference_identities
                and not self.export_admission_dependency_identities
                and failure is None
                and not reconciliations
            ),
            NestedWorkflowInvocationKind.CONFIRMED: (
                observation is not None
                and child_revision is not None
                and replay_result is not None
                and bool(self.exported_result_reference_identities)
                and len(self.exported_result_reference_identities)
                == len(self.export_admission_dependency_identities)
                and failure is None
                and not reconciliations
            ),
            NestedWorkflowInvocationKind.REJECTED: (
                observation is not None
                and child_revision is None
                and replay_result is None
                and not self.exported_result_reference_identities
                and not self.export_admission_dependency_identities
                and failure is not None
                and not reconciliations
            ),
            NestedWorkflowInvocationKind.INDETERMINATE: (
                observation is not None
                and child_revision is None
                and replay_result is None
                and not self.exported_result_reference_identities
                and not self.export_admission_dependency_identities
                and failure is None
                and bool(reconciliations)
            ),
        }[self.kind]
        if not valid:
            raise ValueError(
                "nested invocation fields do not match the observation variant"
            )

    @staticmethod
    def _require_sorted_unique_identities(
        values: tuple[ResultObjectReferenceIdentity | ResultDependencyIdentity, ...],
        nominal_type: type[ResultObjectReferenceIdentity]
        | type[ResultDependencyIdentity],
        name: str,
    ) -> None:
        """Require a tuple of unique identities in lexical identity order."""
        if type(values) is not tuple or any(
            type(value) is not nominal_type for value in values
        ):
            raise TypeError(f"{name} must be a tuple of {nominal_type.__name__}")
        if values != tuple(sorted(values, key=lambda value: value.value)) or len(
            set(values)
        ) != len(values):
            raise ValueError(f"{name} must be unique and lexically sorted")


@dataclass(frozen=True, slots=True, kw_only=True)
class ScientificExecutionAuthorityReference:
    """Retain externally supplied authority state without creating authority.

    Parameters
    ----------
    grant_identity, grant_revision_identity
        Exact externally supplied grant and immutable grant revision.
    snapshot_identity, state_identity
        Exact supplied authority snapshot and grant state.
    """

    grant_identity: ExecutionGrantIdentity
    grant_revision_identity: ExecutionGrantRevisionIdentity
    snapshot_identity: ScientificExecutionAuthoritySnapshotIdentity
    state_identity: ScientificExecutionAuthorityStateIdentity

    def __post_init__(self) -> None:
        """Validate exact authority reference identities."""
        expected = (
            (self.grant_identity, ExecutionGrantIdentity, "grant_identity"),
            (
                self.grant_revision_identity,
                ExecutionGrantRevisionIdentity,
                "grant_revision_identity",
            ),
            (
                self.snapshot_identity,
                ScientificExecutionAuthoritySnapshotIdentity,
                "snapshot_identity",
            ),
            (
                self.state_identity,
                ScientificExecutionAuthorityStateIdentity,
                "state_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationExecutionRequestCorrelation:
    """Correlate an externally prepared request to exact WorkflowRun state.

    Parameters
    ----------
    identity, workflow_run_identity, task_instance_identity
        Exact correlation record, represented run, and requesting Task instance.
    activation_identity, operation_identity, attempt_identity
        Exact requesting invocation identities.
    attempt_record_identity
        Exact current attempt-state record.
    request_identity, executor_identity, obligation_identity
        Exact prepared request, selected executor, and durable obligation.
    grant_identity, authorization_result_identity
        Exact supplied grant and external authorization result.
    input_result_reference_identities
        Unique request inputs in lexical ResultObject-reference identity order.
    """

    identity: SimulationExecutionRequestCorrelationIdentity
    workflow_run_identity: WorkflowRunIdentity
    task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    attempt_record_identity: TaskAttemptRecordIdentity
    request_identity: SimulationExecutionRequestIdentity
    executor_identity: ScientificExecutorIdentity
    obligation_identity: ObligationIdentity
    grant_identity: ExecutionGrantIdentity
    authorization_result_identity: SimulationExecutionAuthorizationResultIdentity
    input_result_reference_identities: tuple[ResultObjectReferenceIdentity, ...]

    def __post_init__(self) -> None:
        """Validate exact request correlations and canonical input references."""
        expected = (
            (
                self.identity,
                SimulationExecutionRequestCorrelationIdentity,
                "identity",
            ),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (
                self.attempt_record_identity,
                TaskAttemptRecordIdentity,
                "attempt_record_identity",
            ),
            (
                self.request_identity,
                SimulationExecutionRequestIdentity,
                "request_identity",
            ),
            (self.executor_identity, ScientificExecutorIdentity, "executor_identity"),
            (self.obligation_identity, ObligationIdentity, "obligation_identity"),
            (self.grant_identity, ExecutionGrantIdentity, "grant_identity"),
            (
                self.authorization_result_identity,
                SimulationExecutionAuthorizationResultIdentity,
                "authorization_result_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        inputs = self.input_result_reference_identities
        if type(inputs) is not tuple or any(
            type(value) is not ResultObjectReferenceIdentity for value in inputs
        ):
            raise TypeError(
                "input_result_reference_identities must be a tuple of "
                "ResultObjectReferenceIdentity"
            )
        if inputs != tuple(sorted(inputs, key=lambda value: value.value)) or len(
            set(inputs)
        ) != len(inputs):
            raise ValueError(
                "input result reference identities must be unique and sorted"
            )


class AuthorityReservationOutcomeKind(StrEnum):
    """Closed append-only authority reservation states."""

    RESERVED = "reserved"
    CLAIMED = "claimed"


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthorityReservationOutcome:
    """Record reservation or claim of externally supplied one-dispatch authority.

    Parameters
    ----------
    identity
        Exact append-only reservation-outcome record identity.
    workflow_run_identity, workflow_run_revision_identity
        Exact represented run and revision owning the record.
    authority_reference, authorization_result_identity
        Exact supplied authority state and external authorization result.
    request_identity
        Exact prepared simulation request.
    activation_identity, operation_identity, attempt_identity
        Exact requesting invocation identities.
    attempt_record_identity, obligation_identity
        Exact current attempt-state record and durable obligation.
    expected_revision_identity
        Run revision expected by the external atomic claim operation.
    kind
        Whether this record represents reservation or subsequent claim.
    predecessor_reservation_identity
        Exact reservation predecessor required for ``claimed``; otherwise ``None``.

    Notes
    -----
    The record performs no authorization, compare-and-swap, claim, or effect.
    """

    identity: AuthorityReservationOutcomeIdentity
    workflow_run_identity: WorkflowRunIdentity
    workflow_run_revision_identity: WorkflowRunRevisionIdentity
    authority_reference: ScientificExecutionAuthorityReference
    authorization_result_identity: SimulationExecutionAuthorizationResultIdentity
    request_identity: SimulationExecutionRequestIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    attempt_record_identity: TaskAttemptRecordIdentity
    obligation_identity: ObligationIdentity
    expected_revision_identity: WorkflowRunRevisionIdentity
    kind: AuthorityReservationOutcomeKind
    predecessor_reservation_identity: AuthorityReservationOutcomeIdentity | None = None

    def __post_init__(self) -> None:
        """Validate exact fields and append-only reservation/claim discrimination."""
        expected = (
            (self.identity, AuthorityReservationOutcomeIdentity, "identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.workflow_run_revision_identity,
                WorkflowRunRevisionIdentity,
                "workflow_run_revision_identity",
            ),
            (
                self.authority_reference,
                ScientificExecutionAuthorityReference,
                "authority_reference",
            ),
            (
                self.authorization_result_identity,
                SimulationExecutionAuthorizationResultIdentity,
                "authorization_result_identity",
            ),
            (
                self.request_identity,
                SimulationExecutionRequestIdentity,
                "request_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (
                self.attempt_record_identity,
                TaskAttemptRecordIdentity,
                "attempt_record_identity",
            ),
            (self.obligation_identity, ObligationIdentity, "obligation_identity"),
            (
                self.expected_revision_identity,
                WorkflowRunRevisionIdentity,
                "expected_revision_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.kind) is not AuthorityReservationOutcomeKind:
            raise TypeError("kind must be AuthorityReservationOutcomeKind")
        predecessor = self.predecessor_reservation_identity
        if predecessor is not None and type(predecessor) is not (
            AuthorityReservationOutcomeIdentity
        ):
            raise TypeError(
                "predecessor_reservation_identity must be "
                "AuthorityReservationOutcomeIdentity or None"
            )
        if predecessor == self.identity:
            raise ValueError(
                "a reservation outcome cannot identify itself as predecessor"
            )
        if (
            self.kind is AuthorityReservationOutcomeKind.RESERVED
            and predecessor is not None
        ):
            raise ValueError("reserved authority cannot have a reservation predecessor")
        if self.kind is AuthorityReservationOutcomeKind.CLAIMED and predecessor is None:
            raise ValueError("claimed authority requires its reservation predecessor")


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchObligation:
    """Represent durable pending dispatch work without performing dispatch.

    Parameters
    ----------
    identity
        Exact obligation identity.
    workflow_run_identity, workflow_run_revision_identity
        Exact represented run and revision creating the obligation.
    request_identity, task_instance_identity
        Exact prepared request and requesting Task instance.
    activation_identity, operation_identity, attempt_identity
        Exact requesting invocation identities.
    executor_identity, grant_identity, destination_identity
        Exact selected executor, supplied grant, and external destination.
    resource_scope_identities
        Unique externally supplied resource scopes in lexical identity order.
    creation_idempotency_identity
        Exact idempotent obligation-creation request.
    """

    identity: ObligationIdentity
    workflow_run_identity: WorkflowRunIdentity
    workflow_run_revision_identity: WorkflowRunRevisionIdentity
    request_identity: SimulationExecutionRequestIdentity
    task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    executor_identity: ScientificExecutorIdentity
    grant_identity: ExecutionGrantIdentity
    destination_identity: DispatchDestinationIdentity
    resource_scope_identities: tuple[DispatchResourceScopeIdentity, ...]
    creation_idempotency_identity: DispatchCreationIdempotencyIdentity

    def __post_init__(self) -> None:
        """Validate exact obligation correlations and immutable resource scope."""
        expected = (
            (self.identity, ObligationIdentity, "identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.workflow_run_revision_identity,
                WorkflowRunRevisionIdentity,
                "workflow_run_revision_identity",
            ),
            (
                self.request_identity,
                SimulationExecutionRequestIdentity,
                "request_identity",
            ),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (self.executor_identity, ScientificExecutorIdentity, "executor_identity"),
            (self.grant_identity, ExecutionGrantIdentity, "grant_identity"),
            (
                self.destination_identity,
                DispatchDestinationIdentity,
                "destination_identity",
            ),
            (
                self.creation_idempotency_identity,
                DispatchCreationIdempotencyIdentity,
                "creation_idempotency_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        scopes = self.resource_scope_identities
        if type(scopes) is not tuple or any(
            type(value) is not DispatchResourceScopeIdentity for value in scopes
        ):
            raise TypeError(
                "resource_scope_identities must be a tuple of "
                "DispatchResourceScopeIdentity"
            )
        if scopes != tuple(sorted(scopes, key=lambda value: value.value)) or len(
            set(scopes)
        ) != len(scopes):
            raise ValueError("resource scope identities must be unique and sorted")


class DispatchOutcomeKind(StrEnum):
    """Closed specialized dispatch observations retained by WorkflowRun."""

    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True, slots=True, kw_only=True)
class DispatchOutcomeRecord:
    """Retain one specialized dispatch envelope and exact correlations.

    Parameters
    ----------
    identity, envelope_identity
        Exact aggregate record and specialized external envelope.
    workflow_run_identity, request_identity, task_instance_identity
        Exact represented run, prepared request, and requesting Task instance.
    activation_identity, operation_identity, attempt_identity
        Exact requesting invocation identities.
    executor_identity, obligation_identity, grant_identity
        Exact executor, durable obligation, and supplied grant.
    kind
        Closed dispatch observation variant.
    result_reference_identity
        Exact result reference for ``confirmed``; otherwise ``None``.
    failure_record_identity
        Exact failure record for ``rejected``; otherwise ``None``.
    reconciliation_identity_values
        Unique lexical reconciliation identities for ``indeterminate``.
    """

    identity: DispatchOutcomeRecordIdentity
    envelope_identity: SimulationDispatchOutcomeIdentity
    workflow_run_identity: WorkflowRunIdentity
    request_identity: SimulationExecutionRequestIdentity
    task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    executor_identity: ScientificExecutorIdentity
    obligation_identity: ObligationIdentity
    grant_identity: ExecutionGrantIdentity
    kind: DispatchOutcomeKind
    result_reference_identity: ResultObjectReferenceIdentity | None = None
    failure_record_identity: TaskFailureRecordIdentity | None = None
    reconciliation_identity_values: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate exact correlations and closed dispatch-outcome fields."""
        expected = (
            (self.identity, DispatchOutcomeRecordIdentity, "identity"),
            (
                self.envelope_identity,
                SimulationDispatchOutcomeIdentity,
                "envelope_identity",
            ),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.request_identity,
                SimulationExecutionRequestIdentity,
                "request_identity",
            ),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (self.executor_identity, ScientificExecutorIdentity, "executor_identity"),
            (self.obligation_identity, ObligationIdentity, "obligation_identity"),
            (self.grant_identity, ExecutionGrantIdentity, "grant_identity"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.kind) is not DispatchOutcomeKind:
            raise TypeError("kind must be DispatchOutcomeKind")
        result = self.result_reference_identity
        if result is not None and type(result) is not ResultObjectReferenceIdentity:
            raise TypeError(
                "result_reference_identity must be ResultObjectReferenceIdentity "
                "or None"
            )
        failure = self.failure_record_identity
        if failure is not None and type(failure) is not TaskFailureRecordIdentity:
            raise TypeError(
                "failure_record_identity must be TaskFailureRecordIdentity or None"
            )
        reconciliations = self.reconciliation_identity_values
        if type(reconciliations) is not tuple or any(
            type(value) is not str for value in reconciliations
        ):
            raise TypeError("reconciliation_identity_values must be a tuple of strings")
        if any(not value for value in reconciliations):
            raise ValueError("reconciliation identities must not be empty")
        if reconciliations != tuple(sorted(reconciliations)) or len(
            set(reconciliations)
        ) != len(reconciliations):
            raise ValueError("reconciliation identities must be sorted and unique")
        valid = {
            DispatchOutcomeKind.CONFIRMED: (
                result is not None and failure is None and not reconciliations
            ),
            DispatchOutcomeKind.REJECTED: (
                result is None and failure is not None and not reconciliations
            ),
            DispatchOutcomeKind.INDETERMINATE: (
                result is None and failure is None and bool(reconciliations)
            ),
        }[self.kind]
        if not valid:
            raise ValueError("dispatch fields do not match the outcome variant")


class ObligationDispositionKind(StrEnum):
    """Closed append-only states of one dispatch obligation."""

    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    INDETERMINATE = "indeterminate"
    COMPLETED = "completed"


@dataclass(frozen=True, slots=True, kw_only=True)
class ObligationDisposition:
    """Record append-only dispatch-obligation disposition without redispatch.

    Parameters
    ----------
    identity, obligation_identity, request_identity
        Exact disposition, durable obligation, and prepared request.
    dispatch_outcome_record_identity, attempt_record_identity
        Exact specialized dispatch outcome and correlated attempt-state record.
    kind
        Closed append-only disposition variant.
    predecessor_disposition_identity
        Exact predecessor required for ``completed``; otherwise ``None``.
    reconciliation_identity_values
        Unique lexical reconciliation identities required for ``indeterminate``.
    """

    identity: ObligationDispositionIdentity
    obligation_identity: ObligationIdentity
    request_identity: SimulationExecutionRequestIdentity
    dispatch_outcome_record_identity: DispatchOutcomeRecordIdentity
    attempt_record_identity: TaskAttemptRecordIdentity
    kind: ObligationDispositionKind
    predecessor_disposition_identity: ObligationDispositionIdentity | None = None
    reconciliation_identity_values: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate exact correlations and append-only disposition variants."""
        expected = (
            (self.identity, ObligationDispositionIdentity, "identity"),
            (self.obligation_identity, ObligationIdentity, "obligation_identity"),
            (
                self.request_identity,
                SimulationExecutionRequestIdentity,
                "request_identity",
            ),
            (
                self.dispatch_outcome_record_identity,
                DispatchOutcomeRecordIdentity,
                "dispatch_outcome_record_identity",
            ),
            (
                self.attempt_record_identity,
                TaskAttemptRecordIdentity,
                "attempt_record_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.kind) is not ObligationDispositionKind:
            raise TypeError("kind must be ObligationDispositionKind")
        predecessor = self.predecessor_disposition_identity
        if predecessor is not None and type(predecessor) is not (
            ObligationDispositionIdentity
        ):
            raise TypeError(
                "predecessor_disposition_identity must be "
                "ObligationDispositionIdentity or None"
            )
        if predecessor == self.identity:
            raise ValueError("an obligation disposition cannot precede itself")
        reconciliations = self.reconciliation_identity_values
        if type(reconciliations) is not tuple or any(
            type(value) is not str for value in reconciliations
        ):
            raise TypeError("reconciliation_identity_values must be a tuple of strings")
        if any(not value for value in reconciliations):
            raise ValueError("reconciliation identities must not be empty")
        if reconciliations != tuple(sorted(reconciliations)) or len(
            set(reconciliations)
        ) != len(reconciliations):
            raise ValueError("reconciliation identities must be sorted and unique")
        if self.kind is ObligationDispositionKind.COMPLETED:
            if predecessor is None or reconciliations:
                raise ValueError(
                    "completed disposition requires one predecessor and no "
                    "reconciliation identities"
                )
        elif predecessor is not None:
            raise ValueError(
                "only a completed disposition may name a disposition predecessor"
            )
        elif self.kind is ObligationDispositionKind.INDETERMINATE:
            if not reconciliations:
                raise ValueError(
                    "indeterminate disposition requires reconciliation identities"
                )
        elif reconciliations:
            raise ValueError(
                "confirmed and rejected dispositions prohibit reconciliation identities"
            )


@dataclass(frozen=True, slots=True)
class ScientificDecisionOption:
    """Represent one exact offered scientific-decision option.

    Parameters
    ----------
    identity
        Exact option identity unique within its request.
    value
        Nonempty exact built-in string selected by the transition output binding.
    """

    identity: ScientificDecisionOptionIdentity
    value: str

    def __post_init__(self) -> None:
        """Validate the exact option identity and nonempty declared value."""
        if type(self.identity) is not ScientificDecisionOptionIdentity:
            raise TypeError("identity must be ScientificDecisionOptionIdentity")
        if type(self.value) is not str:
            raise TypeError("decision option value must be a string")
        if not self.value:
            raise ValueError("decision option value must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class ScientificDecisionRequest:
    """Request one explicit response for one affected Workflow branch.

    Parameters
    ----------
    identity
        Exact request identity.
    question
        Nonempty question retained verbatim as represented request state.
    options
        Nonempty options with unique values in lexical option-identity order.
    declared_scope
        Nonempty description of the decision boundary.
    workflow_identity, workflow_run_identity
        Exact affected Workflow and represented run.
    affected_task_instance_identity, affected_transition_identity
        Exact branch-owning Task instance and generic ingress transition. These are
        affected-state correlations, not fabricated Task invocation lineage.
    required_response_source_identity, required_authority_context_identity
        Exact source and authority context required at the decision-ingress boundary.
    definition_identity, definition_version
        Nonempty request-definition identity and positive built-in integer version.
        Booleans are rejected as versions.

    Notes
    -----
    The request creates no Task, activation, attempt, authority, prompt, or effect.
    """

    identity: ScientificDecisionRequestIdentity
    question: str
    options: tuple[ScientificDecisionOption, ...]
    declared_scope: str
    workflow_identity: WorkflowIdentity
    workflow_run_identity: WorkflowRunIdentity
    affected_task_instance_identity: TaskInstanceIdentity
    affected_transition_identity: ColoredPetriNetTransitionIdentity
    required_response_source_identity: ResponseSourceIdentity
    required_authority_context_identity: AuthorityContextIdentity
    definition_identity: str
    definition_version: int

    def __post_init__(self) -> None:
        """Validate exact request fields and canonical offered-option ordering."""
        expected = (
            (self.identity, ScientificDecisionRequestIdentity, "identity"),
            (self.workflow_identity, WorkflowIdentity, "workflow_identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.affected_task_instance_identity,
                TaskInstanceIdentity,
                "affected_task_instance_identity",
            ),
            (
                self.affected_transition_identity,
                ColoredPetriNetTransitionIdentity,
                "affected_transition_identity",
            ),
            (
                self.required_response_source_identity,
                ResponseSourceIdentity,
                "required_response_source_identity",
            ),
            (
                self.required_authority_context_identity,
                AuthorityContextIdentity,
                "required_authority_context_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        for name in ("question", "declared_scope", "definition_identity"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must not be empty")
        if type(self.definition_version) is not int:
            raise TypeError("definition_version must be an integer excluding bool")
        if self.definition_version < 1:
            raise ValueError("definition_version must be positive")
        if type(self.options) is not tuple or any(
            type(option) is not ScientificDecisionOption for option in self.options
        ):
            raise TypeError("options must be a tuple of ScientificDecisionOption")
        if not self.options:
            raise ValueError("a scientific decision request requires options")
        if self.options != tuple(
            sorted(self.options, key=lambda option: option.identity.value)
        ) or len({option.identity for option in self.options}) != len(self.options):
            raise ValueError("decision options must be unique and lexically sorted")
        if len({option.value for option in self.options}) != len(self.options):
            raise ValueError("decision option values must be unique")


@dataclass(frozen=True, slots=True, kw_only=True)
class ScientificDecisionResolution:
    """Represent one immutable no-Task scientific-decision ResultObject.

    Parameters
    ----------
    identity, content_identity
        Exact ResultObject identity and immutable represented-content identity.
    request_identity
        Exact request resolved by this value.
    verbatim_response
        Nonempty response retained verbatim; no transport authentication is implied.
    normalized_option_identity
        Exactly one option offered by the request.
    response_source_identity, authority_context_identity
        Direct source and authority-context identities matching the request.
    boundary_receipt_identity
        Exact actually available application-boundary receipt, or ``None``.
    predecessor_resolution_identity, supersedes_resolution_identity
        Both absent for an initial resolution. A correction sets both to the same
        exact effective predecessor resolution.
    producer_provenance
        Exact :class:`RepresentedScientificDecisionIngressProducer` with no Task,
        activation, operation, or attempt fields.
    """

    identity: ResultObjectIdentity
    content_identity: ResultObjectContentIdentity
    request_identity: ScientificDecisionRequestIdentity
    verbatim_response: str
    normalized_option_identity: ScientificDecisionOptionIdentity
    response_source_identity: ResponseSourceIdentity
    authority_context_identity: AuthorityContextIdentity
    boundary_receipt_identity: BoundaryReceiptIdentity | None
    predecessor_resolution_identity: ResultObjectIdentity | None
    supersedes_resolution_identity: ResultObjectIdentity | None
    producer_provenance: RepresentedScientificDecisionIngressProducer

    def __post_init__(self) -> None:
        """Validate exact no-Task resolution and append-only correction fields."""
        expected = (
            (self.identity, ResultObjectIdentity, "identity"),
            (
                self.content_identity,
                ResultObjectContentIdentity,
                "content_identity",
            ),
            (
                self.request_identity,
                ScientificDecisionRequestIdentity,
                "request_identity",
            ),
            (
                self.normalized_option_identity,
                ScientificDecisionOptionIdentity,
                "normalized_option_identity",
            ),
            (
                self.response_source_identity,
                ResponseSourceIdentity,
                "response_source_identity",
            ),
            (
                self.authority_context_identity,
                AuthorityContextIdentity,
                "authority_context_identity",
            ),
            (
                self.producer_provenance,
                RepresentedScientificDecisionIngressProducer,
                "producer_provenance",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.verbatim_response) is not str:
            raise TypeError("verbatim_response must be a string")
        if not self.verbatim_response:
            raise ValueError("verbatim_response must not be empty")
        receipt = self.boundary_receipt_identity
        if receipt is not None and type(receipt) is not BoundaryReceiptIdentity:
            raise TypeError(
                "boundary_receipt_identity must be BoundaryReceiptIdentity or None"
            )
        predecessor = self.predecessor_resolution_identity
        supersedes = self.supersedes_resolution_identity
        for resolution_reference, name in (
            (predecessor, "predecessor_resolution_identity"),
            (supersedes, "supersedes_resolution_identity"),
        ):
            if (
                resolution_reference is not None
                and type(resolution_reference) is not ResultObjectIdentity
            ):
                raise TypeError(f"{name} must be ResultObjectIdentity or None")
        if predecessor == self.identity or supersedes == self.identity:
            raise ValueError("a scientific decision resolution cannot supersede itself")
        if (predecessor is None) != (supersedes is None) or (
            predecessor is not None and predecessor != supersedes
        ):
            raise ValueError(
                "a correction must name and supersede the same exact predecessor"
            )
        producer = self.producer_provenance
        if (
            producer.request_identity != self.request_identity
            or producer.response_source_identity != self.response_source_identity
            or producer.authority_context_identity != self.authority_context_identity
            or producer.resolution_identity != self.identity
        ):
            raise ValueError(
                "resolution and scientific-decision producer identities must agree"
            )


class TaskInvocationOutcomeKind(StrEnum):
    """Closed generic invocation outcomes owned by Workflow control."""

    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskInvocationOutcome:
    """Close one exact Task invocation as confirmed, rejected, or indeterminate.

    Parameters
    ----------
    identity
        Exact generic outcome identity.
    workflow_run_identity
        Exact represented run that owns this outcome.
    activation_identity, operation_identity, attempt_identity
        Exact invocation correlation shared with the activation and attempt.
    terminal_attempt_record_identity
        Exact terminal append-only state record closing this attempt.
    kind
        Closed outcome discriminator.
    results, production_record_identities
        Returned immutable ResultObject references and their production records.
        Present only for ``confirmed`` and paired in result order.
    failure_record_identity
        Aggregate-correlated structured failure record. Present only for ``rejected``.
    reconciliation_identity_values
        Sorted unique nonempty identities required to reconcile an
        ``indeterminate`` invocation.  Present only for that variant.

    Notes
    -----
    This envelope is Workflow control state, not a scientific ResultObject.
    """

    identity: TaskInvocationOutcomeIdentity
    workflow_run_identity: WorkflowRunIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    terminal_attempt_record_identity: TaskAttemptRecordIdentity
    kind: TaskInvocationOutcomeKind
    results: tuple[ResultObjectReference, ...] = ()
    production_record_identities: tuple[ResultProductionRecordIdentity, ...] = ()
    failure_record_identity: TaskFailureRecordIdentity | None = None
    reconciliation_identity_values: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Validate exact correlations and closed variant fields."""
        expected = (
            (self.identity, TaskInvocationOutcomeIdentity, "identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (
                self.terminal_attempt_record_identity,
                TaskAttemptRecordIdentity,
                "terminal_attempt_record_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.kind) is not TaskInvocationOutcomeKind:
            raise TypeError("kind must be TaskInvocationOutcomeKind")
        if type(self.results) is not tuple or any(
            type(result) is not ResultObjectReference for result in self.results
        ):
            raise TypeError("results must be a tuple of ResultObjectReference")
        result_identities = tuple(result.identity for result in self.results)
        if len(set(result_identities)) != len(result_identities):
            raise ValueError("result reference identities must be unique")
        productions = self.production_record_identities
        if type(productions) is not tuple or any(
            type(value) is not ResultProductionRecordIdentity for value in productions
        ):
            raise TypeError(
                "production_record_identities must be a tuple of "
                "ResultProductionRecordIdentity"
            )
        if len(set(productions)) != len(productions):
            raise ValueError("production record identities must be unique")
        failure = self.failure_record_identity
        if failure is not None and type(failure) is not TaskFailureRecordIdentity:
            raise TypeError(
                "failure_record_identity must be TaskFailureRecordIdentity or None"
            )
        if type(self.reconciliation_identity_values) is not tuple or any(
            type(value) is not str for value in self.reconciliation_identity_values
        ):
            raise TypeError("reconciliation_identity_values must be a tuple of strings")
        reconciliations = self.reconciliation_identity_values
        if any(not value for value in reconciliations):
            raise ValueError("reconciliation identities must not be empty")
        if reconciliations != tuple(sorted(reconciliations)) or len(
            set(reconciliations)
        ) != len(reconciliations):
            raise ValueError("reconciliation identities must be sorted and unique")

        valid = {
            TaskInvocationOutcomeKind.CONFIRMED: (
                bool(self.results)
                and len(self.results) == len(self.production_record_identities)
                and self.failure_record_identity is None
                and not self.reconciliation_identity_values
            ),
            TaskInvocationOutcomeKind.REJECTED: (
                not self.results
                and not self.production_record_identities
                and self.failure_record_identity is not None
                and not self.reconciliation_identity_values
            ),
            TaskInvocationOutcomeKind.INDETERMINATE: (
                not self.results
                and not self.production_record_identities
                and self.failure_record_identity is None
                and bool(self.reconciliation_identity_values)
            ),
        }[self.kind]
        if not valid:
            raise ValueError("invocation fields do not match the outcome variant")


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskWorkflowTransitionRecord:
    """Record one successful task-origin generic transition in canonical history.

    Parameters
    ----------
    identity
        Exact identity of this task-origin transition record.
    sequence_identity
        Identity of this position in the canonical transition sequence.
    sequence_index
        Zero-based exact built-in integer position in the run history. Booleans are
        rejected.
    workflow_identity, workflow_run_identity
        Exact Workflow and represented run.
    definition_reference_identity, runtime_bundle_identity
        Exact immutable definition reference and replay runtime bundle.
    activation_identity, operation_identity, attempt_identity
        Exact Task invocation correlations responsible for this transition.
    terminal_attempt_record_identity
        Exact append-only terminal attempt-state record.
    outcome_identity
        Exact confirmed invocation outcome responsible for this transition.
    result_production_identities
        Exact production records paired with the confirmed outcome results.
    firing_result
        Complete successful pure generic firing result, including its firing input,
        predecessor, successor, and audit facts.
    request_correlation_identity, dispatch_outcome_record_identity
        Exact simulation request and confirmed dispatch records when this transition
        ingests a dispatched result; both are absent for ordinary Task invocation.

    Notes
    -----
    Cross-record sequence and invocation closure are checked during replay.  This
    record performs no Task invocation or generic firing itself.
    """

    identity: TaskWorkflowTransitionRecordIdentity
    sequence_identity: WorkflowTransitionSequenceIdentity
    sequence_index: int
    workflow_identity: WorkflowIdentity
    workflow_run_identity: WorkflowRunIdentity
    definition_reference_identity: WorkflowDefinitionReferenceIdentity
    runtime_bundle_identity: WorkflowRuntimeBundleIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    terminal_attempt_record_identity: TaskAttemptRecordIdentity
    outcome_identity: TaskInvocationOutcomeIdentity
    result_production_identities: tuple[ResultProductionRecordIdentity, ...]
    firing_result: ColoredPetriNetFiringResult
    request_correlation_identity: (
        SimulationExecutionRequestCorrelationIdentity | None
    ) = None
    dispatch_outcome_record_identity: DispatchOutcomeRecordIdentity | None = None

    def __post_init__(self) -> None:
        """Validate local record fields and require a successful retained firing."""
        if type(self.sequence_index) is not int:
            raise TypeError("sequence_index must be an integer excluding bool")
        if self.sequence_index < 0:
            raise ValueError("sequence_index must be nonnegative")
        expected = (
            (self.identity, TaskWorkflowTransitionRecordIdentity, "identity"),
            (
                self.sequence_identity,
                WorkflowTransitionSequenceIdentity,
                "sequence_identity",
            ),
            (self.workflow_identity, WorkflowIdentity, "workflow_identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.definition_reference_identity,
                WorkflowDefinitionReferenceIdentity,
                "definition_reference_identity",
            ),
            (
                self.runtime_bundle_identity,
                WorkflowRuntimeBundleIdentity,
                "runtime_bundle_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (
                self.terminal_attempt_record_identity,
                TaskAttemptRecordIdentity,
                "terminal_attempt_record_identity",
            ),
            (self.outcome_identity, TaskInvocationOutcomeIdentity, "outcome_identity"),
            (self.firing_result, ColoredPetriNetFiringResult, "firing_result"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        productions = self.result_production_identities
        if type(productions) is not tuple or any(
            type(value) is not ResultProductionRecordIdentity for value in productions
        ):
            raise TypeError(
                "result_production_identities must be a tuple of "
                "ResultProductionRecordIdentity"
            )
        if not productions or len(set(productions)) != len(productions):
            raise ValueError("result production identities must be nonempty and unique")
        request = self.request_correlation_identity
        if request is not None and type(request) is not (
            SimulationExecutionRequestCorrelationIdentity
        ):
            raise TypeError(
                "request_correlation_identity must be "
                "SimulationExecutionRequestCorrelationIdentity or None"
            )
        dispatch = self.dispatch_outcome_record_identity
        if dispatch is not None and type(dispatch) is not DispatchOutcomeRecordIdentity:
            raise TypeError(
                "dispatch_outcome_record_identity must be "
                "DispatchOutcomeRecordIdentity or None"
            )
        if (request is None) != (dispatch is None):
            raise ValueError(
                "a dispatched task transition requires both request and dispatch "
                "correlations"
            )
        if self.firing_result.outcome is not ColoredPetriNetFiringOutcomeKind.SUCCESS:
            raise ValueError("a transition record requires a successful firing result")


@dataclass(frozen=True, slots=True, kw_only=True)
class ScientificDecisionWorkflowTransitionRecord:
    """Record one successful no-Task scientific-decision-origin transition.

    Parameters
    ----------
    identity
        Exact scientific-decision transition-record identity.
    sequence_identity, sequence_index
        Unique sequence-position identity and zero-based built-in integer index in the
        shared task/decision history. Booleans are rejected as indexes.
    workflow_identity, workflow_run_identity
        Exact Workflow and represented run.
    definition_reference_identity, runtime_bundle_identity
        Exact immutable definition reference and replay runtime bundle.
    request_identity, resolution_identity
        Exact scientific-decision request and immutable resolution ResultObject.
    producer_provenance_identity
        Exact represented no-Task decision-ingress producer record.
    firing_result
        Complete successful pure generic firing result. Its external output binding
        must contain exactly one string assignment equal to the normalized option value.

    Notes
    -----
    The class shape intentionally has no Task-instance, activation, operation,
    attempt, Task outcome, or Task result-production fields.
    """

    identity: ScientificDecisionTransitionRecordIdentity
    sequence_identity: WorkflowTransitionSequenceIdentity
    sequence_index: int
    workflow_identity: WorkflowIdentity
    workflow_run_identity: WorkflowRunIdentity
    definition_reference_identity: WorkflowDefinitionReferenceIdentity
    runtime_bundle_identity: WorkflowRuntimeBundleIdentity
    request_identity: ScientificDecisionRequestIdentity
    resolution_identity: ResultObjectIdentity
    producer_provenance_identity: ResultProducerProvenanceIdentity
    firing_result: ColoredPetriNetFiringResult

    def __post_init__(self) -> None:
        """Validate exact no-Task origin fields and successful generic firing."""
        expected = (
            (
                self.identity,
                ScientificDecisionTransitionRecordIdentity,
                "identity",
            ),
            (
                self.sequence_identity,
                WorkflowTransitionSequenceIdentity,
                "sequence_identity",
            ),
            (self.workflow_identity, WorkflowIdentity, "workflow_identity"),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.definition_reference_identity,
                WorkflowDefinitionReferenceIdentity,
                "definition_reference_identity",
            ),
            (
                self.runtime_bundle_identity,
                WorkflowRuntimeBundleIdentity,
                "runtime_bundle_identity",
            ),
            (
                self.request_identity,
                ScientificDecisionRequestIdentity,
                "request_identity",
            ),
            (self.resolution_identity, ResultObjectIdentity, "resolution_identity"),
            (
                self.producer_provenance_identity,
                ResultProducerProvenanceIdentity,
                "producer_provenance_identity",
            ),
            (self.firing_result, ColoredPetriNetFiringResult, "firing_result"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.sequence_index) is not int:
            raise TypeError("sequence_index must be an integer excluding bool")
        if self.sequence_index < 0:
            raise ValueError("sequence_index must be nonnegative")
        if self.firing_result.outcome is not ColoredPetriNetFiringOutcomeKind.SUCCESS:
            raise ValueError("a transition record requires a successful firing result")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowDefinitionReference:
    """Retain exact immutable Workflow and generic-definition version references.

    Parameters
    ----------
    identity
        Exact identity of this immutable definition-reference set.
    workflow_identity
        Reusable Workflow definition represented by the run.
    workflow_definition_version
        Positive built-in integer Workflow-definition version. Booleans are rejected.
    colored_petri_net_definition_identity
        Exact generic colored-Petri-net definition identity.
    colored_petri_net_definition_version
        Positive built-in integer generic-definition version. Booleans are rejected.
    task_definition_identities
        Unique Task-definition identities in lexical identity order.
    schema_version
        Positive built-in integer in-memory WorkflowRun schema version. Booleans are
        rejected.

    Notes
    -----
    Construction accepts positive versions so records can represent unsupported input.
    The current :class:`WorkflowRunReplayer` supports version 1 for all three version
    fields and returns ``unsupported_version`` for another value.
    """

    identity: WorkflowDefinitionReferenceIdentity
    workflow_identity: WorkflowIdentity
    workflow_definition_version: int
    colored_petri_net_definition_identity: ColoredPetriNetDefinitionIdentity
    colored_petri_net_definition_version: int
    task_definition_identities: tuple[TaskDefinitionIdentity, ...]
    schema_version: int

    def __post_init__(self) -> None:
        """Validate exact versions and canonical Task-definition references."""
        expected = (
            (self.identity, WorkflowDefinitionReferenceIdentity, "identity"),
            (self.workflow_identity, WorkflowIdentity, "workflow_identity"),
            (
                self.colored_petri_net_definition_identity,
                ColoredPetriNetDefinitionIdentity,
                "colored_petri_net_definition_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        for name in (
            "workflow_definition_version",
            "colored_petri_net_definition_version",
            "schema_version",
        ):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be an integer excluding bool")
            if value < 1:
                raise ValueError(f"{name} must be positive")
        identities = self.task_definition_identities
        if type(identities) is not tuple or any(
            type(value) is not TaskDefinitionIdentity for value in identities
        ):
            raise TypeError(
                "task_definition_identities must be a tuple of TaskDefinitionIdentity"
            )
        if identities != tuple(
            sorted(identities, key=lambda value: value.value)
        ) or len(set(identities)) != len(identities):
            raise ValueError(
                "task_definition_identities must be unique and lexically sorted"
            )
