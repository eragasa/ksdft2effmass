"""Immutable snapshot-plus-history aggregate for one represented Workflow run."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetMarking,
)

from ..model import (
    TaskActivation,
    TaskInstance,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from .identities import (
    ResultProducerProvenanceIdentity,
    WorkflowDefinitionReferenceIdentity,
    WorkflowRunRevisionIdentity,
    WorkflowRuntimeBundleIdentity,
)
from .records import (
    AuthorityReservationOutcome,
    DispatchOutcomeRecord,
    ExternalResultProducer,
    HumanAuthoredResultProducer,
    ImportedRetainedResultProducer,
    NestedWorkflowInvocation,
    NestedWorkflowMembership,
    ObligationDisposition,
    RepresentedScientificDecisionIngressProducer,
    RepresentedTaskResultProducer,
    ResultDependency,
    ResultObjectReference,
    ResultProductionRecord,
    ScientificDecisionRequest,
    ScientificDecisionResolution,
    ScientificDecisionWorkflowTransitionRecord,
    ScientificExecutionAuthorityReference,
    SimulationDispatchObligation,
    SimulationExecutionRequestCorrelation,
    TaskAttempt,
    TaskFailureRecord,
    TaskInvocationOutcome,
    TaskWorkflowMembership,
    TaskWorkflowTransitionRecord,
    UnknownLegacyResultProducer,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRun:
    """Represent one immutable WorkflowRun revision and canonical ordered history.

    Parameters
    ----------
    identity, revision_identity, predecessor_revision_identity
        Stable run identity, exact immutable revision identity, and optional exact
        predecessor revision identity.
    workflow_identity, definition_reference_identity, runtime_bundle_identity
        Exact Workflow, immutable definition-reference, and runtime-bundle
        correlations.
    schema_version, adapter_implementation_identity
        In-memory contract version and represented adapter implementation identity.
    task_instances, task_memberships, nested_memberships, nested_invocations
        Immutable ordinary composition and distinct child-run correlations. Child
        marking and transition history are never embedded.
    activations, attempts, outcomes
        Append-only invocation records.
    result_references, result_productions, result_dependencies, failures
        Exact confirmed result flow and rejected failure correlations.
    authority_references, execution_request_correlations, authority_reservations
        Externally supplied authority state and append-only reservation/claim records.
    dispatch_obligations, dispatch_outcomes, obligation_dispositions
        Effect-free pending-work, specialized outcome, and disposition records.
    scientific_decision_requests, scientific_decision_resolutions
        Explicit no-Task scientific-decision ingress records.
    initial_marking, current_marking
        Exact initial and represented current generic markings.
    transitions
        One ordered history of successful task and scientific-decision origins.

    Notes
    -----
    Construction enforces exact collection types and local uniqueness.  The
    cross-record and replay closure is established only by
    :class:`WorkflowRunReplayer` for an explicit runtime bundle.
    """

    identity: WorkflowRunIdentity
    revision_identity: WorkflowRunRevisionIdentity
    predecessor_revision_identity: WorkflowRunRevisionIdentity | None
    workflow_identity: WorkflowIdentity
    definition_reference_identity: WorkflowDefinitionReferenceIdentity
    runtime_bundle_identity: WorkflowRuntimeBundleIdentity
    schema_version: int
    adapter_implementation_identity: str
    task_instances: tuple[TaskInstance, ...]
    task_memberships: tuple[TaskWorkflowMembership, ...]
    nested_memberships: tuple[NestedWorkflowMembership, ...]
    nested_invocations: tuple[NestedWorkflowInvocation, ...]
    activations: tuple[TaskActivation, ...]
    attempts: tuple[TaskAttempt, ...]
    outcomes: tuple[TaskInvocationOutcome, ...]
    result_references: tuple[ResultObjectReference, ...]
    result_productions: tuple[ResultProductionRecord, ...]
    result_dependencies: tuple[ResultDependency, ...]
    failures: tuple[TaskFailureRecord, ...]
    authority_references: tuple[ScientificExecutionAuthorityReference, ...]
    execution_request_correlations: tuple[SimulationExecutionRequestCorrelation, ...]
    authority_reservations: tuple[AuthorityReservationOutcome, ...]
    dispatch_obligations: tuple[SimulationDispatchObligation, ...]
    dispatch_outcomes: tuple[DispatchOutcomeRecord, ...]
    obligation_dispositions: tuple[ObligationDisposition, ...]
    scientific_decision_requests: tuple[ScientificDecisionRequest, ...]
    scientific_decision_resolutions: tuple[ScientificDecisionResolution, ...]
    initial_marking: ColoredPetriNetMarking
    current_marking: ColoredPetriNetMarking
    transitions: tuple[
        TaskWorkflowTransitionRecord | ScientificDecisionWorkflowTransitionRecord, ...
    ]

    def __post_init__(self) -> None:
        """Validate immutable collection shape and owner-local uniqueness."""
        expected = (
            (self.identity, WorkflowRunIdentity, "identity"),
            (self.revision_identity, WorkflowRunRevisionIdentity, "revision_identity"),
            (self.workflow_identity, WorkflowIdentity, "workflow_identity"),
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
            (self.initial_marking, ColoredPetriNetMarking, "initial_marking"),
            (self.current_marking, ColoredPetriNetMarking, "current_marking"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        predecessor = self.predecessor_revision_identity
        if (
            predecessor is not None
            and type(predecessor) is not WorkflowRunRevisionIdentity
        ):
            raise TypeError(
                "predecessor_revision_identity must be "
                "WorkflowRunRevisionIdentity or None"
            )
        if predecessor == self.revision_identity:
            raise ValueError(
                "a WorkflowRun revision cannot identify itself as predecessor"
            )
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be an integer excluding bool")
        if self.schema_version < 1:
            raise ValueError("schema_version must be positive")
        if type(self.adapter_implementation_identity) is not str:
            raise TypeError("adapter_implementation_identity must be a string")
        if not self.adapter_implementation_identity:
            raise ValueError("adapter_implementation_identity must not be empty")

        collections = (
            ("task_instances", TaskInstance),
            ("task_memberships", TaskWorkflowMembership),
            ("nested_memberships", NestedWorkflowMembership),
            ("nested_invocations", NestedWorkflowInvocation),
            ("activations", TaskActivation),
            ("attempts", TaskAttempt),
            ("outcomes", TaskInvocationOutcome),
            ("result_references", ResultObjectReference),
            ("result_productions", ResultProductionRecord),
            ("result_dependencies", ResultDependency),
            ("failures", TaskFailureRecord),
            ("authority_references", ScientificExecutionAuthorityReference),
            (
                "execution_request_correlations",
                SimulationExecutionRequestCorrelation,
            ),
            ("authority_reservations", AuthorityReservationOutcome),
            ("dispatch_obligations", SimulationDispatchObligation),
            ("dispatch_outcomes", DispatchOutcomeRecord),
            ("obligation_dispositions", ObligationDisposition),
            ("scientific_decision_requests", ScientificDecisionRequest),
            ("scientific_decision_resolutions", ScientificDecisionResolution),
        )
        for name, member_type in collections:
            values = getattr(self, name)
            if type(values) is not tuple or any(
                type(value) is not member_type for value in values
            ):
                raise TypeError(f"{name} must be a tuple of {member_type.__name__}")
        if type(self.transitions) is not tuple or any(
            type(value)
            not in {
                TaskWorkflowTransitionRecord,
                ScientificDecisionWorkflowTransitionRecord,
            }
            for value in self.transitions
        ):
            raise TypeError(
                "transitions must be a tuple of task-origin or "
                "scientific-decision-origin records"
            )
        if self.authority_references != tuple(
            sorted(
                self.authority_references,
                key=lambda reference: reference.grant_identity.value,
            )
        ):
            raise ValueError("authority_references must be in lexical grant order")
        canonical_collections = (
            (self.task_instances, "task_instances"),
            (self.task_memberships, "task_memberships"),
            (self.activations, "activations"),
            (self.outcomes, "outcomes"),
            (self.result_references, "result_references"),
            (self.result_productions, "result_productions"),
            (self.result_dependencies, "result_dependencies"),
            (self.failures, "failures"),
            (self.nested_memberships, "nested_memberships"),
            (self.nested_invocations, "nested_invocations"),
            (
                self.execution_request_correlations,
                "execution_request_correlations",
            ),
            (self.authority_reservations, "authority_reservations"),
            (self.dispatch_obligations, "dispatch_obligations"),
            (self.dispatch_outcomes, "dispatch_outcomes"),
            (self.obligation_dispositions, "obligation_dispositions"),
            (self.scientific_decision_requests, "scientific_decision_requests"),
            (
                self.scientific_decision_resolutions,
                "scientific_decision_resolutions",
            ),
        )
        for values, name in canonical_collections:
            if values != tuple(sorted(values, key=lambda value: value.identity.value)):
                raise ValueError(f"{name} must be in lexical identity order")

        unique_collections = (
            (
                tuple(value.identity for value in self.task_instances),
                "task instance identities",
            ),
            (
                tuple(value.identity for value in self.task_memberships),
                "task membership identities",
            ),
            (
                tuple(value.identity for value in self.nested_memberships),
                "nested membership identities",
            ),
            (
                tuple(
                    value.child_workflow_run_identity
                    for value in self.nested_memberships
                ),
                "nested membership child run identities",
            ),
            (
                tuple(value.identity for value in self.nested_invocations),
                "nested invocation identities",
            ),
            (
                tuple(
                    value.child_workflow_run_identity
                    for value in self.nested_invocations
                ),
                "nested invocation child run identities",
            ),
            (
                tuple(
                    value.child_creation_idempotency_identity
                    for value in self.nested_invocations
                ),
                "child creation idempotency identities",
            ),
            (
                tuple(value.identity for value in self.activations),
                "activation identities",
            ),
            (
                tuple(value.operation_identity for value in self.activations),
                "activation operation identities",
            ),
            (
                tuple(value.attempt_identity for value in self.activations),
                "activation attempt identities",
            ),
            (
                tuple(value.identity for value in self.attempts),
                "attempt record identities",
            ),
            (
                tuple(value.identity for value in self.outcomes),
                "outcome identities",
            ),
            (
                tuple(value.attempt_identity for value in self.outcomes),
                "outcome attempt identities",
            ),
            (
                tuple(value.identity for value in self.result_references),
                "result reference identities",
            ),
            (
                tuple(value.result.identity for value in self.result_references),
                "concrete result identities",
            ),
            (
                tuple(value.identity for value in self.result_productions),
                "result production identities",
            ),
            (
                tuple(value.identity for value in self.result_dependencies),
                "result dependency identities",
            ),
            (
                tuple(value.identity for value in self.failures),
                "failure record identities",
            ),
            (
                tuple(value.grant_identity for value in self.authority_references),
                "authority reference grant identities",
            ),
            (
                tuple(value.identity for value in self.execution_request_correlations),
                "execution request correlation identities",
            ),
            (
                tuple(
                    value.request_identity
                    for value in self.execution_request_correlations
                ),
                "execution request identities",
            ),
            (
                tuple(value.identity for value in self.authority_reservations),
                "authority reservation identities",
            ),
            (
                tuple(value.identity for value in self.dispatch_obligations),
                "dispatch obligation identities",
            ),
            (
                tuple(value.identity for value in self.dispatch_outcomes),
                "dispatch outcome record identities",
            ),
            (
                tuple(value.envelope_identity for value in self.dispatch_outcomes),
                "dispatch envelope identities",
            ),
            (
                tuple(value.identity for value in self.obligation_dispositions),
                "obligation disposition identities",
            ),
            (
                tuple(value.identity for value in self.scientific_decision_requests),
                "scientific decision request identities",
            ),
            (
                tuple(value.identity for value in self.scientific_decision_resolutions),
                "scientific decision resolution identities",
            ),
            (
                tuple(value.failure.identity for value in self.failures),
                "structured failure identities",
            ),
            (
                tuple(value.identity for value in self.transitions),
                "transition record identities",
            ),
            (
                tuple(value.sequence_identity for value in self.transitions),
                "transition sequence identities",
            ),
            (
                tuple(value.sequence_index for value in self.transitions),
                "transition sequence indexes",
            ),
        )
        for identities, owner in unique_collections:
            if len(set(identities)) != len(identities):
                raise ValueError(f"{owner} must be unique")
        producers: dict[
            ResultProducerProvenanceIdentity,
            RepresentedTaskResultProducer
            | RepresentedScientificDecisionIngressProducer
            | ExternalResultProducer
            | ImportedRetainedResultProducer
            | HumanAuthoredResultProducer
            | UnknownLegacyResultProducer,
        ] = {}
        for reference in self.result_references:
            producer = reference.producer_provenance
            existing = producers.get(producer.identity)
            if existing is not None and existing != producer:
                raise ValueError(
                    "one result producer provenance identity cannot name conflicting "
                    "records"
                )
            producers[producer.identity] = producer
