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
from .authority import SimulationExecutionAuthorizationResult
from .identities import (
    ResultProducerProvenanceIdentity,
    WorkflowDefinitionReferenceIdentity,
    WorkflowRunRevisionIdentity,
    WorkflowRuntimeBundleIdentity,
)
from .records import (
    AuthorityReservationOutcome,
    DispatchObservationRecord,
    DispatchOutcomeRecord,
    ExternalResultProducer,
    HumanAuthoredResultProducer,
    ImportedRetainedResultProducer,
    NativeOutputAdmission,
    NestedWorkflowInvocation,
    NestedWorkflowInvocationIntent,
    NestedWorkflowMembership,
    NestedWorkflowTerminalObservation,
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
    SimulationDispatchEntry,
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
    nested_invocation_intents, nested_terminal_observations
        Default-empty immutable intent and first-terminal history in the same v1
        contract. Combined invocation records remain unchanged. Child, creation-key
        and stable-attempt uniqueness spans both intent sources; observation links
        preserve their exact nominal type and are unique per intent.
    activations, attempts, outcomes
        Append-only invocation records.
    result_references, result_productions, native_output_admissions
        Exact confirmed result flow and dispatch-specific native-output admission.
    result_dependencies, failures
        Exact result-consumption and rejected failure correlations.
    authorization_results
        Closed effect-free preparation- and claim-phase authorization results.
    authority_references, execution_request_correlations, authority_reservations
        Externally supplied authority state and append-only reservation/claim records.
    dispatch_obligations, dispatch_entries, dispatch_observations, dispatch_outcomes
        Effect-free pending work, durable effect-entry state, append-only reconciliation
        evidence, and at most one
        final specialized outcome per obligation.
    obligation_dispositions
        Final dispatch-obligation disposition records.
    scientific_decision_requests, scientific_decision_resolutions
        Explicit no-Task scientific-decision ingress records.
    initial_marking, current_marking
        Exact initial and represented current generic markings.
    transitions
        One ordered history of successful task and scientific-decision origins.

    Notes
    -----
    Construction enforces exact collection types and local uniqueness.  The
    cross-record closure is checked by the shared structural validator used by
    :class:`WorkflowRunTransactionValidator` and :class:`WorkflowRunReplayer`.
    Computed replay equality requires the latter and an explicit runtime bundle.
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
    native_output_admissions: tuple[NativeOutputAdmission, ...]
    result_dependencies: tuple[ResultDependency, ...]
    failures: tuple[TaskFailureRecord, ...]
    authorization_results: tuple[SimulationExecutionAuthorizationResult, ...]
    authority_references: tuple[ScientificExecutionAuthorityReference, ...]
    execution_request_correlations: tuple[SimulationExecutionRequestCorrelation, ...]
    authority_reservations: tuple[AuthorityReservationOutcome, ...]
    dispatch_obligations: tuple[SimulationDispatchObligation, ...]
    dispatch_entries: tuple[SimulationDispatchEntry, ...]
    dispatch_observations: tuple[DispatchObservationRecord, ...]
    dispatch_outcomes: tuple[DispatchOutcomeRecord, ...]
    obligation_dispositions: tuple[ObligationDisposition, ...]
    scientific_decision_requests: tuple[ScientificDecisionRequest, ...]
    scientific_decision_resolutions: tuple[ScientificDecisionResolution, ...]
    initial_marking: ColoredPetriNetMarking
    current_marking: ColoredPetriNetMarking
    transitions: tuple[
        TaskWorkflowTransitionRecord | ScientificDecisionWorkflowTransitionRecord, ...
    ]

    nested_invocation_intents: tuple[NestedWorkflowInvocationIntent, ...] = ()
    nested_terminal_observations: tuple[NestedWorkflowTerminalObservation, ...] = ()

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

        for new_values, new_member_type, new_name in (
            (
                self.nested_invocation_intents,
                NestedWorkflowInvocationIntent,
                "nested_invocation_intents",
            ),
            (
                self.nested_terminal_observations,
                NestedWorkflowTerminalObservation,
                "nested_terminal_observations",
            ),
        ):
            if type(new_values) is not tuple or any(
                type(value) is not new_member_type for value in new_values
            ):
                raise TypeError(
                    f"{new_name} must be a tuple of {new_member_type.__name__}"
                )
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
            ("native_output_admissions", NativeOutputAdmission),
            ("result_dependencies", ResultDependency),
            ("failures", TaskFailureRecord),
            ("authorization_results", SimulationExecutionAuthorizationResult),
            ("authority_references", ScientificExecutionAuthorityReference),
            (
                "execution_request_correlations",
                SimulationExecutionRequestCorrelation,
            ),
            ("authority_reservations", AuthorityReservationOutcome),
            ("dispatch_obligations", SimulationDispatchObligation),
            ("dispatch_entries", SimulationDispatchEntry),
            ("dispatch_observations", DispatchObservationRecord),
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
            (self.native_output_admissions, "native_output_admissions"),
            (self.result_dependencies, "result_dependencies"),
            (self.failures, "failures"),
            (self.authorization_results, "authorization_results"),
            (self.nested_memberships, "nested_memberships"),
            (self.nested_invocations, "nested_invocations"),
            (self.nested_invocation_intents, "nested_invocation_intents"),
            (self.nested_terminal_observations, "nested_terminal_observations"),
            (
                self.execution_request_correlations,
                "execution_request_correlations",
            ),
            (self.authority_reservations, "authority_reservations"),
            (self.dispatch_obligations, "dispatch_obligations"),
            (self.dispatch_entries, "dispatch_entries"),
            (self.dispatch_observations, "dispatch_observations"),
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

        intent_sources = self.nested_invocations + self.nested_invocation_intents
        unique_collections = (
            (
                tuple(v.identity for v in self.nested_invocation_intents),
                "nested intent identities",
            ),
            (
                tuple(v.attempt_identity for v in intent_sources),
                "nested stable attempt identities",
            ),
            (
                tuple(v.identity for v in self.nested_terminal_observations)
                + tuple(
                    v.terminal_observation_identity
                    for v in self.nested_invocations
                    if v.terminal_observation_identity is not None
                ),
                "nested observation identities",
            ),
            (
                tuple(v.intent_identity for v in self.nested_terminal_observations),
                "nested observed intent identities",
            ),
            (
                tuple(
                    v.terminal_attempt_record_identity
                    for v in self.nested_terminal_observations
                ),
                "nested observation terminal attempt identities",
            ),
            (
                tuple(v.outcome_identity for v in self.nested_terminal_observations),
                "nested observation outcome identities",
            ),
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
                tuple(value.child_workflow_run_identity for value in intent_sources),
                "nested invocation child run identities",
            ),
            (
                tuple(
                    value.child_creation_idempotency_identity
                    for value in intent_sources
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
                tuple(value.identity for value in self.native_output_admissions),
                "native output admission identities",
            ),
            (
                tuple(
                    value.dispatch_outcome_record_identity
                    for value in self.native_output_admissions
                ),
                "native output admission dispatch identities",
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
                tuple(value.identity for value in self.authorization_results),
                "authorization result identities",
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
                tuple(
                    value.creation_idempotency_identity
                    for value in self.dispatch_obligations
                ),
                "dispatch creation idempotency identities",
            ),
            (
                tuple(value.identity for value in self.dispatch_entries),
                "dispatch entry identities",
            ),
            (
                tuple(value.obligation_identity for value in self.dispatch_entries),
                "dispatch entry obligation identities",
            ),
            (
                tuple(value.identity for value in self.dispatch_observations),
                "dispatch observation record identities",
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
