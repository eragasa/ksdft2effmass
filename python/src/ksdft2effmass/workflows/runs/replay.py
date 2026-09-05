"""Effect-free deterministic reconstruction of represented Workflow runs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
from typing import final

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBindingSelectorIdentity,
    ColoredPetriNetDefinition,
    ColoredPetriNetExpressionEvaluatorIdentity,
    ColoredPetriNetFiringOutcomeKind,
    ColoredPetriNetMarking,
    ColoredPetriNetOrderingPolicyIdentity,
    ColoredPetriNetTransitionEnablerIdentity,
    ColoredPetriNetTransitionFirer,
    ColoredPetriNetTransitionFirerIdentity,
    ColoredPetriNetValueKind,
)

from ..model import (
    AttemptIdentity,
    ResultObjectIdentity,
    TaskActivation,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from .aggregate import (
    WorkflowRun,
)
from .identities import (
    DispatchOutcomeRecordIdentity,
    ObligationIdentity,
    ResultDependencyIdentity,
    ResultObjectReferenceIdentity,
    ResultProductionRecordIdentity,
    ScientificDecisionTransitionRecordIdentity,
    TaskAttemptRecordIdentity,
    TaskFailureRecordIdentity,
    TaskInvocationOutcomeIdentity,
    WorkflowRunReplayResultIdentity,
    WorkflowRunRevisionIdentity,
    WorkflowRuntimeBundleIdentity,
)
from .records import (
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeKind,
    DispatchOutcomeKind,
    ExternalResultProducer,
    HumanAuthoredResultProducer,
    ImportedRetainedResultProducer,
    NestedWorkflowInvocationKind,
    ObligationDispositionKind,
    RepresentedScientificDecisionIngressProducer,
    RepresentedTaskResultProducer,
    ResultDependency,
    ResultObjectReference,
    ScientificDecisionWorkflowTransitionRecord,
    TaskAttempt,
    TaskAttemptStatus,
    TaskFailureRecord,
    TaskInvocationOutcome,
    TaskInvocationOutcomeKind,
    TaskWorkflowTransitionRecord,
    UnknownLegacyResultProducer,
    WorkflowDefinitionReference,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRuntimeBundle:
    """Supply exact immutable dependencies accepted for deterministic replay.

    Parameters
    ----------
    identity
        Exact runtime-bundle identity referenced by the WorkflowRun.
    definition_reference
        Exact immutable Workflow, generic-definition, Task-definition, and schema
        version reference represented by this bundle.
    schema_version
        Positive exact built-in integer for the in-memory WorkflowRun contract.
    workflow_identity
        Reusable Workflow definition represented by the bundle.
    definition
        Exact generic colored-Petri-net definition used for replay.
    task_definition_identities
        Unique Task definitions in lexical identity order.
    adapter_implementation_identity
        Nonempty identity of the Workflow-to-CPN adapter semantics represented by
        the run.  Replay verifies correlation but does not invoke the adapter.
    expression_evaluator_identity
        Exact generic expression-evaluator identity expected in retained transitions.
    ordering_policy_identity
        Exact generic ordering-policy identity expected in retained transitions.
    transition_enabler_identity
        Exact generic transition-enabler identity expected in retained transitions.
    binding_selector_identity
        Exact generic binding-selector identity expected in retained transitions.
    transition_firer_identity
        Exact generic transition-firer identity expected in retained transitions.

    Notes
    -----
    The current replayer supports ``workflow-cpn-adapter-v1`` and the version-1
    evaluator, enablement ordering, enabler, selector, and firer identities emitted by
    :mod:`ksdft2effmass.petrinet.colored`. Other identities remain representable but
    produce ``unsupported_version`` rather than replay.
    """

    identity: WorkflowRuntimeBundleIdentity
    definition_reference: WorkflowDefinitionReference
    schema_version: int
    workflow_identity: WorkflowIdentity
    definition: ColoredPetriNetDefinition
    task_definition_identities: tuple[TaskDefinitionIdentity, ...]
    adapter_implementation_identity: str
    expression_evaluator_identity: ColoredPetriNetExpressionEvaluatorIdentity
    ordering_policy_identity: ColoredPetriNetOrderingPolicyIdentity
    transition_enabler_identity: ColoredPetriNetTransitionEnablerIdentity
    binding_selector_identity: ColoredPetriNetBindingSelectorIdentity
    transition_firer_identity: ColoredPetriNetTransitionFirerIdentity

    def __post_init__(self) -> None:
        """Validate the explicit immutable runtime dependency set."""
        expected = (
            (self.identity, WorkflowRuntimeBundleIdentity, "identity"),
            (
                self.definition_reference,
                WorkflowDefinitionReference,
                "definition_reference",
            ),
            (self.workflow_identity, WorkflowIdentity, "workflow_identity"),
            (self.definition, ColoredPetriNetDefinition, "definition"),
            (
                self.expression_evaluator_identity,
                ColoredPetriNetExpressionEvaluatorIdentity,
                "expression_evaluator_identity",
            ),
            (
                self.ordering_policy_identity,
                ColoredPetriNetOrderingPolicyIdentity,
                "ordering_policy_identity",
            ),
            (
                self.transition_enabler_identity,
                ColoredPetriNetTransitionEnablerIdentity,
                "transition_enabler_identity",
            ),
            (
                self.binding_selector_identity,
                ColoredPetriNetBindingSelectorIdentity,
                "binding_selector_identity",
            ),
            (
                self.transition_firer_identity,
                ColoredPetriNetTransitionFirerIdentity,
                "transition_firer_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be an integer excluding bool")
        if self.schema_version < 1:
            raise ValueError("schema_version must be positive")
        if type(self.task_definition_identities) is not tuple or any(
            type(value) is not TaskDefinitionIdentity
            for value in self.task_definition_identities
        ):
            raise TypeError(
                "task_definition_identities must be a tuple of TaskDefinitionIdentity"
            )
        identities = self.task_definition_identities
        if identities != tuple(sorted(identities, key=lambda item: item.value)) or len(
            set(identities)
        ) != len(identities):
            raise ValueError(
                "task_definition_identities must be unique and lexically sorted"
            )
        reference = self.definition_reference
        if (
            reference.workflow_identity != self.workflow_identity
            or reference.colored_petri_net_definition_identity
            != self.definition.identity
            or reference.task_definition_identities != self.task_definition_identities
            or reference.schema_version != self.schema_version
        ):
            raise ValueError(
                "runtime bundle values must agree with its exact definition reference"
            )
        if type(self.adapter_implementation_identity) is not str:
            raise TypeError("adapter_implementation_identity must be a string")
        if not self.adapter_implementation_identity:
            raise ValueError("adapter_implementation_identity must not be empty")


class WorkflowRunReplayOutcomeKind(StrEnum):
    """Closed deterministic WorkflowRun replay outcomes."""

    EQUAL = "equal"
    UNEQUAL = "unequal"
    UNSUPPORTED_VERSION = "unsupported_version"
    ERROR = "error"


class WorkflowRunReplayIssueCode(StrEnum):
    """Closed reasons why replay did not establish exact equality."""

    RUNTIME_BUNDLE_MISMATCH = "runtime_bundle_mismatch"
    SCHEMA_VERSION_MISMATCH = "schema_version_mismatch"
    WORKFLOW_IDENTITY_MISMATCH = "workflow_identity_mismatch"
    DEFINITION_IDENTITY_MISMATCH = "definition_identity_mismatch"
    TASK_DEFINITION_MISMATCH = "task_definition_mismatch"
    IMPLEMENTATION_IDENTITY_MISMATCH = "implementation_identity_mismatch"
    ACTIVATION_CORRELATION_ERROR = "activation_correlation_error"
    ATTEMPT_CORRELATION_ERROR = "attempt_correlation_error"
    OUTCOME_CORRELATION_ERROR = "outcome_correlation_error"
    RESULT_CORRELATION_ERROR = "result_correlation_error"
    DEPENDENCY_CORRELATION_ERROR = "dependency_correlation_error"
    FAILURE_CORRELATION_ERROR = "failure_correlation_error"
    MEMBERSHIP_CORRELATION_ERROR = "membership_correlation_error"
    NESTED_WORKFLOW_CORRELATION_ERROR = "nested_workflow_correlation_error"
    NESTED_WORKFLOW_EXPORT_CORRELATION_ERROR = (
        "nested_workflow_export_correlation_error"
    )
    CONTROL_STATE_CORRELATION_ERROR = "control_state_correlation_error"
    SCIENTIFIC_DECISION_CORRELATION_ERROR = "scientific_decision_correlation_error"
    NONCANONICAL_TRANSITION_ORDER = "noncanonical_transition_order"
    PREDECESSOR_MARKING_MISMATCH = "predecessor_marking_mismatch"
    FIRING_REPLAY_FAILED = "firing_replay_failed"
    FIRING_RESULT_MISMATCH = "firing_result_mismatch"
    CURRENT_MARKING_UNEQUAL = "current_marking_unequal"


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunReplayIssue:
    """Describe one deterministic WorkflowRun replay limitation or failure.

    Parameters
    ----------
    code
        Stable Workflow-owned issue code.
    operation_phase
        Nonempty replay phase.
    diagnostic
        Nonempty diagnostic bounded to software replay behavior.
    """

    code: WorkflowRunReplayIssueCode
    operation_phase: str
    diagnostic: str

    def __post_init__(self) -> None:
        """Validate exact issue fields."""
        if type(self.code) is not WorkflowRunReplayIssueCode:
            raise TypeError("code must be WorkflowRunReplayIssueCode")
        for name in ("operation_phase", "diagnostic"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunReplayResult:
    """Represent one closed deterministic replay outcome.

    Parameters
    ----------
    identity
        Content identity derived from the represented result fields.
    workflow_run_identity, revision_identity, runtime_bundle_identity
        Exact replay input correlations.
    outcome
        ``equal``, ``unequal``, ``unsupported_version``, or ``error``.
    reconstructed_marking
        Completed reconstructed marking for ``equal`` and ``unequal`` only.
    issues
        Empty for ``equal`` and nonempty for every other outcome.
    claim_boundary
        Nonempty statements limiting the result to represented deterministic software
        replay; they grant no authority or scientific acceptance.

    Notes
    -----
    An ``equal`` result establishes only exact software replay for represented
    generic state.  It grants no execution authority or scientific acceptance.
    """

    identity: WorkflowRunReplayResultIdentity
    workflow_run_identity: WorkflowRunIdentity
    revision_identity: WorkflowRunRevisionIdentity
    runtime_bundle_identity: WorkflowRuntimeBundleIdentity
    outcome: WorkflowRunReplayOutcomeKind
    reconstructed_marking: ColoredPetriNetMarking | None
    issues: tuple[WorkflowRunReplayIssue, ...]
    claim_boundary: tuple[str, ...] = field(
        default=(
            "deterministic represented WorkflowRun replay only",
            "no Task invocation, persistence, or external effect",
            "no scientific validation, acceptance, or authority",
        )
    )

    def __post_init__(self) -> None:
        """Enforce exact nominal fields and closed replay-result variants."""
        expected = (
            (self.identity, WorkflowRunReplayResultIdentity, "identity"),
            (self.workflow_run_identity, WorkflowRunIdentity, "workflow_run_identity"),
            (self.revision_identity, WorkflowRunRevisionIdentity, "revision_identity"),
            (
                self.runtime_bundle_identity,
                WorkflowRuntimeBundleIdentity,
                "runtime_bundle_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.outcome) is not WorkflowRunReplayOutcomeKind:
            raise TypeError("outcome must be WorkflowRunReplayOutcomeKind")
        if (
            self.reconstructed_marking is not None
            and type(self.reconstructed_marking) is not ColoredPetriNetMarking
        ):
            raise TypeError(
                "reconstructed_marking must be ColoredPetriNetMarking or None"
            )
        if type(self.issues) is not tuple or any(
            type(issue) is not WorkflowRunReplayIssue for issue in self.issues
        ):
            raise TypeError("issues must be a tuple of WorkflowRunReplayIssue")
        if type(self.claim_boundary) is not tuple or any(
            type(value) is not str for value in self.claim_boundary
        ):
            raise TypeError("claim_boundary must be a tuple of strings")
        if not self.claim_boundary or any(not value for value in self.claim_boundary):
            raise ValueError("claim_boundary must contain nonempty strings")

        completed = self.outcome in {
            WorkflowRunReplayOutcomeKind.EQUAL,
            WorkflowRunReplayOutcomeKind.UNEQUAL,
        }
        valid = (
            (
                self.outcome is WorkflowRunReplayOutcomeKind.EQUAL
                and self.reconstructed_marking is not None
                and not self.issues
            )
            or (
                self.outcome is WorkflowRunReplayOutcomeKind.UNEQUAL
                and self.reconstructed_marking is not None
                and bool(self.issues)
            )
            or (
                not completed
                and self.reconstructed_marking is None
                and bool(self.issues)
            )
        )
        if not valid:
            raise ValueError("replay fields do not match the outcome variant")


@final
class WorkflowRunReplayer:
    """Effect-free ActionObject for exact WorkflowRun reconstruction.

    The replayer accepts one immutable run revision and one explicit runtime bundle.
    It performs no ambient version discovery.  Unsupported versions return
    ``unsupported_version`` before replay; malformed correlations or failed generic
    reconstruction return ``error``; completed reconstruction returns ``equal`` or
    ``unequal`` according to the retained current marking.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Reject subclass-injected replay policy."""
        raise TypeError("WorkflowRunReplayer does not support subclasses")

    def execute(
        self, run: WorkflowRun, runtime_bundle: WorkflowRuntimeBundle
    ) -> WorkflowRunReplayResult:
        """Replay ``run`` deterministically with ``runtime_bundle``.

        Parameters
        ----------
        run
            Exact immutable WorkflowRun revision.
        runtime_bundle
            Explicit definition and implementation-version set.

        Returns
        -------
        WorkflowRunReplayResult
            Closed exact replay outcome.

        Raises
        ------
        TypeError
            Either argument has the wrong exact public type.
        """
        if type(run) is not WorkflowRun:
            raise TypeError("run must be WorkflowRun")
        if type(runtime_bundle) is not WorkflowRuntimeBundle:
            raise TypeError("runtime_bundle must be WorkflowRuntimeBundle")

        unsupported = self._unsupported_issue(run, runtime_bundle)
        if unsupported is not None:
            return self._result(
                run,
                runtime_bundle,
                WorkflowRunReplayOutcomeKind.UNSUPPORTED_VERSION,
                None,
                (unsupported,),
            )

        correlation_issue = self._correlation_issue(run)
        if correlation_issue is not None:
            return self._result(
                run,
                runtime_bundle,
                WorkflowRunReplayOutcomeKind.ERROR,
                None,
                (correlation_issue,),
            )

        expected_indexes = tuple(range(len(run.transitions)))
        observed_indexes = tuple(
            transition.sequence_index for transition in run.transitions
        )
        if observed_indexes != expected_indexes:
            return self._error(
                run,
                runtime_bundle,
                WorkflowRunReplayIssueCode.NONCANONICAL_TRANSITION_ORDER,
                "transition_order",
                "transition indexes must be contiguous and start at zero",
            )

        activations = {value.identity: value for value in run.activations}
        attempts = {value.identity: value for value in run.attempts}
        outcomes = {value.identity: value for value in run.outcomes}
        current = run.initial_marking
        for transition in run.transitions:
            firing_input = transition.firing_result.firing_input
            if type(transition) is TaskWorkflowTransitionRecord:
                activation = activations.get(transition.activation_identity)
                attempt = attempts.get(transition.terminal_attempt_record_identity)
                outcome = outcomes.get(transition.outcome_identity)
                if activation is None:
                    return self._error(
                        run,
                        runtime_bundle,
                        WorkflowRunReplayIssueCode.ACTIVATION_CORRELATION_ERROR,
                        "transition_correlation",
                        "transition activation is absent from the WorkflowRun",
                    )
                if attempt is None:
                    return self._error(
                        run,
                        runtime_bundle,
                        WorkflowRunReplayIssueCode.ATTEMPT_CORRELATION_ERROR,
                        "transition_correlation",
                        "transition attempt is absent from the WorkflowRun",
                    )
                if outcome is None:
                    return self._error(
                        run,
                        runtime_bundle,
                        WorkflowRunReplayIssueCode.OUTCOME_CORRELATION_ERROR,
                        "transition_correlation",
                        "transition outcome is absent from the WorkflowRun",
                    )
                if not self._transition_correlations_match(
                    transition, activation, attempt, outcome
                ):
                    return self._error(
                        run,
                        runtime_bundle,
                        WorkflowRunReplayIssueCode.OUTCOME_CORRELATION_ERROR,
                        "transition_correlation",
                        (
                            "transition, activation, attempt, and outcome identities "
                            "differ"
                        ),
                    )
            if firing_input.predecessor_marking != current:
                return self._error(
                    run,
                    runtime_bundle,
                    WorkflowRunReplayIssueCode.PREDECESSOR_MARKING_MISMATCH,
                    "transition_replay",
                    "retained predecessor differs from reconstructed state",
                )
            implementation_issue = self._transition_implementation_issue(
                transition, runtime_bundle
            )
            if implementation_issue is not None:
                return self._result(
                    run,
                    runtime_bundle,
                    WorkflowRunReplayOutcomeKind.UNSUPPORTED_VERSION,
                    None,
                    (implementation_issue,),
                )
            replayed = ColoredPetriNetTransitionFirer().execute(firing_input)
            if replayed.outcome is not ColoredPetriNetFiringOutcomeKind.SUCCESS:
                assert replayed.failure is not None
                return self._error(
                    run,
                    runtime_bundle,
                    WorkflowRunReplayIssueCode.FIRING_REPLAY_FAILED,
                    "transition_replay",
                    f"{replayed.failure.code.value}: {replayed.failure.diagnostic}",
                )
            if replayed != transition.firing_result:
                return self._error(
                    run,
                    runtime_bundle,
                    WorkflowRunReplayIssueCode.FIRING_RESULT_MISMATCH,
                    "transition_replay",
                    "recomputed firing result differs from retained firing result",
                )
            assert replayed.successor_marking is not None
            current = replayed.successor_marking

        if current != run.current_marking:
            issue = WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.CURRENT_MARKING_UNEQUAL,
                operation_phase="final_comparison",
                diagnostic=(
                    "reconstructed final marking differs from retained current marking"
                ),
            )
            return self._result(
                run,
                runtime_bundle,
                WorkflowRunReplayOutcomeKind.UNEQUAL,
                current,
                (issue,),
            )
        return self._result(
            run,
            runtime_bundle,
            WorkflowRunReplayOutcomeKind.EQUAL,
            current,
            (),
        )

    @staticmethod
    def _unsupported_issue(
        run: WorkflowRun, runtime_bundle: WorkflowRuntimeBundle
    ) -> WorkflowRunReplayIssue | None:
        """Return the first deterministic runtime-version mismatch, if any."""
        definition_reference = runtime_bundle.definition_reference
        checks = (
            (
                run.schema_version != 1 or definition_reference.schema_version != 1,
                WorkflowRunReplayIssueCode.SCHEMA_VERSION_MISMATCH,
                "WorkflowRun replay supports schema version 1 only",
            ),
            (
                definition_reference.workflow_definition_version != 1
                or definition_reference.colored_petri_net_definition_version != 1,
                WorkflowRunReplayIssueCode.DEFINITION_IDENTITY_MISMATCH,
                (
                    "WorkflowRun replay supports Workflow and CPN definition "
                    "version 1 only"
                ),
            ),
            (
                runtime_bundle.adapter_implementation_identity
                != "workflow-cpn-adapter-v1"
                or runtime_bundle.expression_evaluator_identity.value
                != "colored-petri-net-expression-evaluator-v1"
                or runtime_bundle.ordering_policy_identity.value
                != "colored-petri-net-enablement-order-v1"
                or runtime_bundle.transition_enabler_identity.value
                != "colored-petri-net-transition-enabler-v1"
                or runtime_bundle.binding_selector_identity.value
                != "colored-petri-net-binding-selector-v1"
                or runtime_bundle.transition_firer_identity.value
                != "colored-petri-net-transition-firer-v1",
                WorkflowRunReplayIssueCode.IMPLEMENTATION_IDENTITY_MISMATCH,
                "WorkflowRun replay does not support the supplied implementations",
            ),
            (
                run.runtime_bundle_identity != runtime_bundle.identity,
                WorkflowRunReplayIssueCode.RUNTIME_BUNDLE_MISMATCH,
                "run references another runtime bundle",
            ),
            (
                run.definition_reference_identity
                != runtime_bundle.definition_reference.identity,
                WorkflowRunReplayIssueCode.DEFINITION_IDENTITY_MISMATCH,
                "run references another Workflow definition reference",
            ),
            (
                run.schema_version != runtime_bundle.schema_version,
                WorkflowRunReplayIssueCode.SCHEMA_VERSION_MISMATCH,
                "run and runtime bundle schema versions differ",
            ),
            (
                run.workflow_identity != runtime_bundle.workflow_identity,
                WorkflowRunReplayIssueCode.WORKFLOW_IDENTITY_MISMATCH,
                "run and runtime bundle Workflow identities differ",
            ),
            (
                run.initial_marking.definition_identity
                != runtime_bundle.definition.identity
                or run.current_marking.definition_identity
                != runtime_bundle.definition.identity,
                WorkflowRunReplayIssueCode.DEFINITION_IDENTITY_MISMATCH,
                "run marking definition identities differ from the runtime definition",
            ),
            (
                run.adapter_implementation_identity
                != runtime_bundle.adapter_implementation_identity,
                WorkflowRunReplayIssueCode.IMPLEMENTATION_IDENTITY_MISMATCH,
                "run and runtime bundle adapter identities differ",
            ),
            (
                tuple(
                    sorted(
                        {
                            instance.definition_identity
                            for instance in run.task_instances
                        },
                        key=lambda identity: identity.value,
                    )
                )
                != runtime_bundle.task_definition_identities,
                WorkflowRunReplayIssueCode.TASK_DEFINITION_MISMATCH,
                "run Task definitions differ from the runtime bundle",
            ),
        )
        for failed, code, diagnostic in checks:
            if failed:
                return WorkflowRunReplayIssue(
                    code=code,
                    operation_phase="runtime_compatibility",
                    diagnostic=diagnostic,
                )
        return None

    @staticmethod
    def _correlation_issue(run: WorkflowRun) -> WorkflowRunReplayIssue | None:
        """Return the first malformed run-level Task correlation, if any."""
        instances = {instance.identity: instance for instance in run.task_instances}
        activations = {
            activation.identity: activation for activation in run.activations
        }
        for activation in run.activations:
            if (
                activation.workflow_identity != run.workflow_identity
                or activation.workflow_run_identity != run.identity
                or activation.task_instance.identity not in instances
                or instances[activation.task_instance.identity]
                != activation.task_instance
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.ACTIVATION_CORRELATION_ERROR,
                    operation_phase="aggregate_correlation",
                    diagnostic="activation does not belong to the represented run",
                )

        membership_instances: set[TaskInstanceIdentity] = set()
        for membership in run.task_memberships:
            if (
                membership.workflow_run_identity != run.identity
                or membership.workflow_identity != run.workflow_identity
                or membership.task_instance_identity not in instances
                or membership.task_instance_identity in membership_instances
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.MEMBERSHIP_CORRELATION_ERROR,
                    operation_phase="aggregate_correlation",
                    diagnostic=(
                        "ordinary Task membership does not close over one exact "
                        "run-scoped instance"
                    ),
                )
            membership_instances.add(membership.task_instance_identity)
        if membership_instances != set(instances):
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.MEMBERSHIP_CORRELATION_ERROR,
                operation_phase="aggregate_correlation",
                diagnostic="every run-scoped Task instance requires one membership",
            )

        observed_records: dict[TaskAttemptRecordIdentity, TaskAttempt] = {}
        started_attempts: set[AttemptIdentity] = set()
        started_activations: set[TaskActivationIdentity] = set()
        terminal_attempts: dict[AttemptIdentity, TaskAttempt] = {}
        retry_successors: set[AttemptIdentity] = set()
        terminal_record_identities: set[TaskAttemptRecordIdentity] = set()
        for attempt in run.attempts:
            resolved_activation = activations.get(attempt.activation_identity)
            if resolved_activation is None or (
                attempt.workflow_run_identity != run.identity
                or attempt.task_instance_identity
                != resolved_activation.task_instance.identity
                or attempt.operation_identity != resolved_activation.operation_identity
                or attempt.attempt_identity != resolved_activation.attempt_identity
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.ATTEMPT_CORRELATION_ERROR,
                    operation_phase="aggregate_correlation",
                    diagnostic="attempt does not match its represented activation",
                )
            if attempt.status is TaskAttemptStatus.STARTED:
                if attempt.attempt_identity in started_attempts:
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.ATTEMPT_CORRELATION_ERROR,
                        operation_phase="aggregate_correlation",
                        diagnostic="a stable attempt has more than one started record",
                    )
                retry = attempt.retry_of_attempt_identity
                if retry is not None:
                    retry_predecessor = terminal_attempts.get(retry)
                    if (
                        retry_predecessor is None
                        or retry_predecessor.task_instance_identity
                        != attempt.task_instance_identity
                        or retry in retry_successors
                    ):
                        return WorkflowRunReplayIssue(
                            code=WorkflowRunReplayIssueCode.ATTEMPT_CORRELATION_ERROR,
                            operation_phase="aggregate_correlation",
                            diagnostic=(
                                "retry predecessor must be the earlier unbranched "
                                "terminal attempt for the same Task instance"
                            ),
                        )
                    retry_successors.add(retry)
                if attempt.activation_identity in started_activations:
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.ATTEMPT_CORRELATION_ERROR,
                        operation_phase="aggregate_correlation",
                        diagnostic=(
                            "an activation has more than one initial attempt record"
                        ),
                    )
                started_attempts.add(attempt.attempt_identity)
                started_activations.add(attempt.activation_identity)
                observed_records[attempt.identity] = attempt
                continue

            predecessor_identity = attempt.predecessor_attempt_record_identity
            assert predecessor_identity is not None
            predecessor = observed_records.get(predecessor_identity)
            if (
                predecessor is None
                or predecessor.attempt_identity != attempt.attempt_identity
                or predecessor.task_instance_identity != attempt.task_instance_identity
                or predecessor.activation_identity != attempt.activation_identity
                or predecessor.operation_identity != attempt.operation_identity
                or predecessor.child_workflow_run_identity
                != attempt.child_workflow_run_identity
                or attempt.attempt_identity in terminal_attempts
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.ATTEMPT_CORRELATION_ERROR,
                    operation_phase="aggregate_correlation",
                    diagnostic=(
                        "terminal attempt state must append once after its exact "
                        "same-attempt predecessor"
                    ),
                )
            terminal_attempts[attempt.attempt_identity] = attempt
            terminal_record_identities.add(attempt.identity)
            observed_records[attempt.identity] = attempt

        if started_activations != set(activations):
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.ATTEMPT_CORRELATION_ERROR,
                operation_phase="aggregate_correlation",
                diagnostic="every activation requires one initial attempt record",
            )

        expected_status = {
            TaskInvocationOutcomeKind.CONFIRMED: TaskAttemptStatus.CONFIRMED,
            TaskInvocationOutcomeKind.REJECTED: TaskAttemptStatus.REJECTED,
            TaskInvocationOutcomeKind.INDETERMINATE: TaskAttemptStatus.INDETERMINATE,
        }
        outcome_terminal_records: set[TaskAttemptRecordIdentity] = set()
        for outcome in run.outcomes:
            resolved_attempt = observed_records.get(
                outcome.terminal_attempt_record_identity
            )
            if resolved_attempt is None or (
                outcome.workflow_run_identity != run.identity
                or outcome.activation_identity != resolved_attempt.activation_identity
                or outcome.operation_identity != resolved_attempt.operation_identity
                or outcome.attempt_identity != resolved_attempt.attempt_identity
                or resolved_attempt.status is not expected_status[outcome.kind]
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.OUTCOME_CORRELATION_ERROR,
                    operation_phase="aggregate_correlation",
                    diagnostic="outcome does not match its terminal attempt record",
                )
            outcome_terminal_records.add(outcome.terminal_attempt_record_identity)
        if outcome_terminal_records != terminal_record_identities:
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.OUTCOME_CORRELATION_ERROR,
                operation_phase="aggregate_correlation",
                diagnostic="every terminal attempt record requires exactly one outcome",
            )

        outcomes = {value.identity: value for value in run.outcomes}
        references = {value.identity: value for value in run.result_references}
        productions = {value.identity: value for value in run.result_productions}
        dependencies = {value.identity: value for value in run.result_dependencies}
        failures = {value.identity: value for value in run.failures}
        for activation in run.activations:
            for input_binding in activation.inputs:
                matching_references = tuple(
                    reference
                    for reference in references.values()
                    if reference.result.identity == input_binding.result.identity
                )
                if len(matching_references) != 1:
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.DEPENDENCY_CORRELATION_ERROR,
                        operation_phase="aggregate_correlation",
                        diagnostic=(
                            "every activation input requires one exact retained result "
                            "reference"
                        ),
                    )
                reference = matching_references[0]
                matching_dependencies = tuple(
                    dependency
                    for dependency in dependencies.values()
                    if dependency.result_reference_identity == reference.identity
                    and dependency.consumer_workflow_run_identity == run.identity
                    and dependency.consumer_task_instance_identity
                    == activation.task_instance.identity
                    and dependency.consumer_activation_identity == activation.identity
                    and dependency.input_name == input_binding.name
                )
                if len(matching_dependencies) != 1:
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.DEPENDENCY_CORRELATION_ERROR,
                        operation_phase="aggregate_correlation",
                        diagnostic=(
                            "every activation input requires one exact result "
                            "dependency"
                        ),
                    )
        nested_issue = WorkflowRunReplayer._nested_correlation_issue(
            run,
            instances,
            activations,
            observed_records,
            outcomes,
            references,
            dependencies,
            failures,
        )
        if nested_issue is not None:
            return nested_issue
        control_issue = WorkflowRunReplayer._control_state_correlation_issue(
            run,
            instances,
            activations,
            observed_records,
            references,
            failures,
        )
        if control_issue is not None:
            return control_issue
        nested_by_outcome = {
            outcome.identity: invocation
            for invocation in run.nested_invocations
            if invocation.kind is not NestedWorkflowInvocationKind.PENDING
            for outcome in run.outcomes
            if outcome.activation_identity == invocation.activation_identity
            and outcome.operation_identity == invocation.operation_identity
            and outcome.attempt_identity == invocation.attempt_identity
        }
        confirmed_nested_by_outcome = {
            identity: invocation
            for identity, invocation in nested_by_outcome.items()
            if invocation.kind is NestedWorkflowInvocationKind.CONFIRMED
        }
        admission_dependencies = {
            identity
            for invocation in run.nested_invocations
            for identity in invocation.export_admission_dependency_identities
        }
        consumed_productions: set[ResultProductionRecordIdentity] = set()
        consumed_failures: set[TaskFailureRecordIdentity] = set()
        for outcome in run.outcomes:
            activation = activations[outcome.activation_identity]
            if outcome.kind is TaskInvocationOutcomeKind.CONFIRMED:
                for reference, production_identity in zip(
                    outcome.results,
                    outcome.production_record_identities,
                    strict=True,
                ):
                    stored_reference = references.get(reference.identity)
                    production = productions.get(production_identity)
                    producer = reference.producer_provenance
                    nested_invocation = confirmed_nested_by_outcome.get(
                        outcome.identity
                    )
                    local_producer = (
                        type(producer) is RepresentedTaskResultProducer
                        and producer.workflow_identity == run.workflow_identity
                        and producer.workflow_run_identity == run.identity
                        and producer.task_instance_identity
                        == activation.task_instance.identity
                        and producer.activation_identity == activation.identity
                        and producer.operation_identity == outcome.operation_identity
                        and producer.attempt_identity == outcome.attempt_identity
                        and producer.terminal_attempt_record_identity
                        == outcome.terminal_attempt_record_identity
                        and producer.outcome_identity == outcome.identity
                        and producer.production_identity == production_identity
                    )
                    child_export_producer = (
                        type(producer) is RepresentedTaskResultProducer
                        and nested_invocation is not None
                        and reference.identity
                        in nested_invocation.exported_result_reference_identities
                        and producer.workflow_identity
                        == nested_invocation.child_workflow_identity
                        and producer.workflow_run_identity
                        == nested_invocation.child_workflow_run_identity
                    )
                    if (
                        stored_reference != reference
                        or production is None
                        or production.result_reference_identity != reference.identity
                        or production.workflow_run_identity != run.identity
                        or production.task_instance_identity
                        != activation.task_instance.identity
                        or production.activation_identity != activation.identity
                        or production.operation_identity != outcome.operation_identity
                        or production.attempt_identity != outcome.attempt_identity
                        or production.terminal_attempt_record_identity
                        != outcome.terminal_attempt_record_identity
                        or production.outcome_identity != outcome.identity
                        or not (local_producer or child_export_producer)
                    ):
                        return WorkflowRunReplayIssue(
                            code=WorkflowRunReplayIssueCode.RESULT_CORRELATION_ERROR,
                            operation_phase="aggregate_correlation",
                            diagnostic=(
                                "confirmed result, producer, and production records "
                                "must close over one exact invocation"
                            ),
                        )
                    consumed_productions.add(production.identity)
                continue
            if outcome.kind is TaskInvocationOutcomeKind.REJECTED:
                assert outcome.failure_record_identity is not None
                failure = failures.get(outcome.failure_record_identity)
                nested_invocation = nested_by_outcome.get(outcome.identity)
                expected_child_run = (
                    None
                    if nested_invocation is None
                    else nested_invocation.child_workflow_run_identity
                )
                if failure is None or (
                    failure.workflow_run_identity != run.identity
                    or failure.task_instance_identity
                    != activation.task_instance.identity
                    or failure.activation_identity != activation.identity
                    or failure.operation_identity != outcome.operation_identity
                    or failure.attempt_identity != outcome.attempt_identity
                    or failure.terminal_attempt_record_identity
                    != outcome.terminal_attempt_record_identity
                    or failure.child_workflow_run_identity != expected_child_run
                ):
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.FAILURE_CORRELATION_ERROR,
                        operation_phase="aggregate_correlation",
                        diagnostic=(
                            "rejected outcome must close over one exact failure record"
                        ),
                    )
                consumed_failures.add(failure.identity)
        if consumed_productions != set(productions):
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.RESULT_CORRELATION_ERROR,
                operation_phase="aggregate_correlation",
                diagnostic=(
                    "every result production must belong to one confirmed outcome"
                ),
            )
        dispatch_failure_identities = {
            outcome.failure_record_identity
            for outcome in run.dispatch_outcomes
            if outcome.kind is DispatchOutcomeKind.REJECTED
            and outcome.failure_record_identity is not None
        }
        if consumed_failures | dispatch_failure_identities != set(failures):
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.FAILURE_CORRELATION_ERROR,
                operation_phase="aggregate_correlation",
                diagnostic="every failure record must belong to one rejected outcome",
            )

        for dependency in run.result_dependencies:
            dependency_reference = references.get(dependency.result_reference_identity)
            instance = instances.get(dependency.consumer_task_instance_identity)
            expected_producer_run: WorkflowRunIdentity | None = None
            if dependency_reference is not None:
                producer = dependency_reference.producer_provenance
                if type(producer) is RepresentedTaskResultProducer:
                    expected_producer_run = producer.workflow_run_identity
                elif type(producer) is RepresentedScientificDecisionIngressProducer:
                    expected_producer_run = producer.workflow_run_identity
            if (
                dependency_reference is None
                or instance is None
                or dependency.consumer_workflow_run_identity != run.identity
                or dependency.producer_workflow_run_identity != expected_producer_run
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.DEPENDENCY_CORRELATION_ERROR,
                    operation_phase="aggregate_correlation",
                    diagnostic="result dependency endpoints do not close in the run",
                )
            consumer_activation_identity = dependency.consumer_activation_identity
            if dependency.identity in admission_dependencies:
                continue
            if consumer_activation_identity is None:
                continue
            consumer = activations.get(consumer_activation_identity)
            if consumer is None or consumer.task_instance.identity != instance.identity:
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.DEPENDENCY_CORRELATION_ERROR,
                    operation_phase="aggregate_correlation",
                    diagnostic="result dependency consumer activation is inconsistent",
                )
            matching_inputs = tuple(
                value
                for value in consumer.inputs
                if value.name == dependency.input_name
                and value.result.identity == dependency_reference.result.identity
            )
            if len(matching_inputs) != 1:
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.DEPENDENCY_CORRELATION_ERROR,
                    operation_phase="aggregate_correlation",
                    diagnostic=(
                        "result dependency must match one exact activation input"
                    ),
                )

        decision_issue = WorkflowRunReplayer._scientific_decision_correlation_issue(
            run, instances, references
        )
        if decision_issue is not None:
            return decision_issue
        result_reference_issue = WorkflowRunReplayer._result_reference_closure_issue(
            run, references
        )
        if result_reference_issue is not None:
            return result_reference_issue

        outcomes = {value.identity: value for value in run.outcomes}
        request_correlations = {
            value.identity: value for value in run.execution_request_correlations
        }
        dispatch_outcomes = {value.identity: value for value in run.dispatch_outcomes}
        for transition in run.transitions:
            if type(transition) is ScientificDecisionWorkflowTransitionRecord:
                continue
            assert type(transition) is TaskWorkflowTransitionRecord
            transition_outcome = outcomes.get(transition.outcome_identity)
            if transition_outcome is None or (
                transition.workflow_identity != run.workflow_identity
                or transition.workflow_run_identity != run.identity
                or transition.definition_reference_identity
                != run.definition_reference_identity
                or transition.runtime_bundle_identity != run.runtime_bundle_identity
                or transition.result_production_identities
                != transition_outcome.production_record_identities
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.RESULT_CORRELATION_ERROR,
                    operation_phase="transition_correlation",
                    diagnostic=(
                        "transition production identities must equal its confirmed "
                        "outcome"
                    ),
                )
            request_identity = transition.request_correlation_identity
            dispatch_identity = transition.dispatch_outcome_record_identity
            if request_identity is not None and dispatch_identity is not None:
                request = request_correlations.get(request_identity)
                dispatch = dispatch_outcomes.get(dispatch_identity)
                if (
                    request is None
                    or dispatch is None
                    or dispatch.kind is not DispatchOutcomeKind.CONFIRMED
                    or dispatch.request_identity != request.request_identity
                    or dispatch.activation_identity != transition.activation_identity
                    or dispatch.operation_identity != transition.operation_identity
                    or dispatch.attempt_identity != transition.attempt_identity
                    or dispatch.result_reference_identity
                    not in {result.identity for result in transition_outcome.results}
                ):
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                        operation_phase="transition_correlation",
                        diagnostic=(
                            "dispatched task transition must close over one confirmed "
                            "request and dispatch outcome"
                        ),
                    )
            for production_identity in transition.result_production_identities:
                production = productions[production_identity]
                if (
                    production.external_output_binding
                    != transition.firing_result.firing_input.external_output_binding
                ):
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.RESULT_CORRELATION_ERROR,
                        operation_phase="transition_correlation",
                        diagnostic=(
                            "result production binding must equal the retained "
                            "firing input"
                        ),
                    )
        return None

    @staticmethod
    def _result_reference_closure_issue(
        run: WorkflowRun,
        references: dict[ResultObjectReferenceIdentity, ResultObjectReference],
    ) -> WorkflowRunReplayIssue | None:
        """Return the first ResultObject reference without exact producer closure."""
        produced_references = {
            production.result_reference_identity
            for production in run.result_productions
        }
        dependent_references = {
            dependency.result_reference_identity
            for dependency in run.result_dependencies
        }
        resolution_identities = {
            resolution.identity for resolution in run.scientific_decision_resolutions
        }
        for reference in references.values():
            producer = reference.producer_provenance
            if type(producer) is RepresentedTaskResultProducer:
                locally_produced = (
                    producer.workflow_run_identity == run.identity
                    and reference.identity in produced_references
                )
                imported_from_represented_run = (
                    producer.workflow_run_identity != run.identity
                    and reference.identity in dependent_references
                )
                if not (locally_produced or imported_from_represented_run):
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.RESULT_CORRELATION_ERROR,
                        operation_phase="aggregate_correlation",
                        diagnostic=(
                            "represented Task result reference lacks local production "
                            "or cross-run dependency closure"
                        ),
                    )
                continue
            if type(producer) is RepresentedScientificDecisionIngressProducer:
                if (
                    producer.workflow_run_identity != run.identity
                    or reference.result.identity not in resolution_identities
                ):
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.RESULT_CORRELATION_ERROR,
                        operation_phase="aggregate_correlation",
                        diagnostic=(
                            "scientific-decision result reference lacks exact local "
                            "resolution closure"
                        ),
                    )
                continue
            if type(producer) not in {
                ExternalResultProducer,
                ImportedRetainedResultProducer,
                HumanAuthoredResultProducer,
                UnknownLegacyResultProducer,
            }:
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.RESULT_CORRELATION_ERROR,
                    operation_phase="aggregate_correlation",
                    diagnostic="result reference has an unsupported producer variant",
                )
        return None

    @staticmethod
    def _control_state_correlation_issue(
        run: WorkflowRun,
        instances: dict[TaskInstanceIdentity, TaskInstance],
        activations: dict[TaskActivationIdentity, TaskActivation],
        attempt_records: dict[TaskAttemptRecordIdentity, TaskAttempt],
        references: dict[ResultObjectReferenceIdentity, ResultObjectReference],
        failures: dict[TaskFailureRecordIdentity, TaskFailureRecord],
    ) -> WorkflowRunReplayIssue | None:
        """Return the first malformed authority, request, or dispatch correlation."""
        authority_by_grant = {
            reference.grant_identity: reference
            for reference in run.authority_references
        }
        requests = {
            request.request_identity: request
            for request in run.execution_request_correlations
        }
        obligations = {
            obligation.identity: obligation for obligation in run.dispatch_obligations
        }
        reservations_by_obligation: dict[
            ObligationIdentity, list[AuthorityReservationOutcome]
        ] = {}
        for reservation in run.authority_reservations:
            reservations_by_obligation.setdefault(
                reservation.obligation_identity, []
            ).append(reservation)

        for request in requests.values():
            activation = activations.get(request.activation_identity)
            attempt = attempt_records.get(request.attempt_record_identity)
            obligation = obligations.get(request.obligation_identity)
            authority = authority_by_grant.get(request.grant_identity)
            input_identities = set(request.input_result_reference_identities)
            if (
                request.workflow_run_identity != run.identity
                or request.task_instance_identity not in instances
                or activation is None
                or activation.task_instance.identity != request.task_instance_identity
                or activation.operation_identity != request.operation_identity
                or activation.attempt_identity != request.attempt_identity
                or attempt is None
                or attempt.activation_identity != request.activation_identity
                or attempt.operation_identity != request.operation_identity
                or attempt.attempt_identity != request.attempt_identity
                or obligation is None
                or authority is None
                or input_identities
                != {
                    reference.identity
                    for reference in references.values()
                    for input_binding in activation.inputs
                    if reference.result.identity == input_binding.result.identity
                }
                or obligation.workflow_run_identity != run.identity
                or obligation.request_identity != request.request_identity
                or obligation.task_instance_identity != request.task_instance_identity
                or obligation.activation_identity != request.activation_identity
                or obligation.operation_identity != request.operation_identity
                or obligation.attempt_identity != request.attempt_identity
                or obligation.executor_identity != request.executor_identity
                or obligation.grant_identity != request.grant_identity
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                    operation_phase="control_state_correlation",
                    diagnostic=(
                        "request, authority, activation, attempt, and obligation must "
                        "close over one exact dispatch intent"
                    ),
                )
            reservation_history = reservations_by_obligation.get(
                request.obligation_identity, []
            )
            reserved_records = tuple(
                record
                for record in reservation_history
                if record.kind is AuthorityReservationOutcomeKind.RESERVED
            )
            claimed_records = tuple(
                record
                for record in reservation_history
                if record.kind is AuthorityReservationOutcomeKind.CLAIMED
            )
            if len(reserved_records) != 1 or len(claimed_records) > 1:
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                    operation_phase="control_state_correlation",
                    diagnostic=(
                        "one obligation requires one reservation and at most one claim"
                    ),
                )
            reserved = reserved_records[0]
            if (
                reserved.kind is not AuthorityReservationOutcomeKind.RESERVED
                or reserved.workflow_run_identity != run.identity
                or reserved.workflow_run_revision_identity
                != obligation.workflow_run_revision_identity
                or reserved.expected_revision_identity
                != obligation.workflow_run_revision_identity
                or reserved.authority_reference != authority
                or reserved.authorization_result_identity
                != request.authorization_result_identity
                or reserved.request_identity != request.request_identity
                or reserved.activation_identity != request.activation_identity
                or reserved.operation_identity != request.operation_identity
                or reserved.attempt_identity != request.attempt_identity
                or reserved.attempt_record_identity != request.attempt_record_identity
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                    operation_phase="control_state_correlation",
                    diagnostic="reservation does not match its exact dispatch request",
                )
            if claimed_records:
                claimed = claimed_records[0]
                if (
                    claimed.kind is not AuthorityReservationOutcomeKind.CLAIMED
                    or claimed.predecessor_reservation_identity != reserved.identity
                    or claimed.workflow_run_identity != reserved.workflow_run_identity
                    or claimed.workflow_run_revision_identity
                    != reserved.workflow_run_revision_identity
                    or claimed.expected_revision_identity
                    != reserved.expected_revision_identity
                    or claimed.authority_reference != reserved.authority_reference
                    or claimed.authorization_result_identity
                    != reserved.authorization_result_identity
                    or claimed.request_identity != reserved.request_identity
                    or claimed.activation_identity != reserved.activation_identity
                    or claimed.operation_identity != reserved.operation_identity
                    or claimed.attempt_identity != reserved.attempt_identity
                    or claimed.attempt_record_identity
                    != reserved.attempt_record_identity
                    or claimed.obligation_identity != reserved.obligation_identity
                ):
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                        operation_phase="control_state_correlation",
                        diagnostic=(
                            "claimed authority must append once after its exact "
                            "reservation"
                        ),
                    )

        if set(obligations) != {
            request.obligation_identity for request in requests.values()
        } or set(reservations_by_obligation) != set(obligations):
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                operation_phase="control_state_correlation",
                diagnostic=(
                    "every obligation and reservation history requires one exact "
                    "request"
                ),
            )

        outcomes = {outcome.identity: outcome for outcome in run.dispatch_outcomes}
        if len({outcome.obligation_identity for outcome in outcomes.values()}) != len(
            outcomes
        ):
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                operation_phase="control_state_correlation",
                diagnostic="one obligation cannot retain multiple dispatch outcomes",
            )
        for outcome in outcomes.values():
            resolved_request = requests.get(outcome.request_identity)
            reservation_history = reservations_by_obligation.get(
                outcome.obligation_identity, []
            )
            claims = tuple(
                record
                for record in reservation_history
                if record.kind is AuthorityReservationOutcomeKind.CLAIMED
            )
            latest_claim = claims[0] if len(claims) == 1 else None
            if resolved_request is None or (
                outcome.workflow_run_identity != run.identity
                or outcome.task_instance_identity
                != resolved_request.task_instance_identity
                or outcome.activation_identity != resolved_request.activation_identity
                or outcome.operation_identity != resolved_request.operation_identity
                or outcome.attempt_identity != resolved_request.attempt_identity
                or outcome.executor_identity != resolved_request.executor_identity
                or outcome.obligation_identity != resolved_request.obligation_identity
                or outcome.grant_identity != resolved_request.grant_identity
                or latest_claim is None
                or latest_claim.kind is not AuthorityReservationOutcomeKind.CLAIMED
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                    operation_phase="control_state_correlation",
                    diagnostic="dispatch outcome does not match its exact request",
                )
            if (
                outcome.kind is DispatchOutcomeKind.CONFIRMED
                and outcome.result_reference_identity not in references
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                    operation_phase="control_state_correlation",
                    diagnostic="confirmed dispatch result reference is absent",
                )
            if outcome.kind is DispatchOutcomeKind.REJECTED:
                assert outcome.failure_record_identity is not None
                failure = failures.get(outcome.failure_record_identity)
                failed_attempt = (
                    None
                    if failure is None
                    else attempt_records.get(failure.terminal_attempt_record_identity)
                )
                if (
                    failure is None
                    or failed_attempt is None
                    or failed_attempt.status is not TaskAttemptStatus.REJECTED
                    or failed_attempt.task_instance_identity
                    != outcome.task_instance_identity
                    or failed_attempt.activation_identity != outcome.activation_identity
                    or failed_attempt.operation_identity != outcome.operation_identity
                    or failed_attempt.attempt_identity != outcome.attempt_identity
                    or failure.workflow_run_identity != run.identity
                    or failure.task_instance_identity != outcome.task_instance_identity
                    or failure.activation_identity != outcome.activation_identity
                    or failure.operation_identity != outcome.operation_identity
                    or failure.attempt_identity != outcome.attempt_identity
                    or failure.request_identity != outcome.request_identity
                    or failure.child_workflow_run_identity is not None
                ):
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                        operation_phase="control_state_correlation",
                        diagnostic=(
                            "rejected dispatch must close over its request-bound "
                            "failure"
                        ),
                    )

        dispositions = {
            disposition.identity: disposition
            for disposition in run.obligation_dispositions
        }
        initial_dispositions_by_outcome: set[DispatchOutcomeRecordIdentity] = set()
        expected_initial_disposition = {
            DispatchOutcomeKind.CONFIRMED: ObligationDispositionKind.CONFIRMED,
            DispatchOutcomeKind.REJECTED: ObligationDispositionKind.REJECTED,
            DispatchOutcomeKind.INDETERMINATE: ObligationDispositionKind.INDETERMINATE,
        }
        for disposition in run.obligation_dispositions:
            resolved_outcome = outcomes.get(
                disposition.dispatch_outcome_record_identity
            )
            attempt = attempt_records.get(disposition.attempt_record_identity)
            if resolved_outcome is None or (
                disposition.obligation_identity != resolved_outcome.obligation_identity
                or disposition.request_identity != resolved_outcome.request_identity
                or attempt is None
                or attempt.activation_identity != resolved_outcome.activation_identity
                or attempt.operation_identity != resolved_outcome.operation_identity
                or attempt.attempt_identity != resolved_outcome.attempt_identity
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                    operation_phase="control_state_correlation",
                    diagnostic=(
                        "obligation disposition does not match its dispatch outcome"
                    ),
                )
            predecessor_identity = disposition.predecessor_disposition_identity
            if predecessor_identity is None:
                if (
                    disposition.dispatch_outcome_record_identity
                    in initial_dispositions_by_outcome
                    or disposition.kind
                    is not expected_initial_disposition[resolved_outcome.kind]
                ):
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                        operation_phase="control_state_correlation",
                        diagnostic=(
                            "a dispatch outcome permits one matching initial "
                            "obligation disposition"
                        ),
                    )
                initial_dispositions_by_outcome.add(
                    disposition.dispatch_outcome_record_identity
                )
            else:
                predecessor = dispositions.get(predecessor_identity)
                if (
                    predecessor is None
                    or predecessor.obligation_identity
                    != disposition.obligation_identity
                    or predecessor.request_identity != disposition.request_identity
                    or predecessor.dispatch_outcome_record_identity
                    != disposition.dispatch_outcome_record_identity
                    or predecessor.attempt_record_identity
                    != disposition.attempt_record_identity
                    or predecessor.kind is not ObligationDispositionKind.CONFIRMED
                ):
                    return WorkflowRunReplayIssue(
                        code=WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
                        operation_phase="control_state_correlation",
                        diagnostic=(
                            "completed disposition must append after its exact "
                            "confirmed predecessor"
                        ),
                    )
        return None

    @staticmethod
    def _scientific_decision_correlation_issue(
        run: WorkflowRun,
        instances: dict[TaskInstanceIdentity, TaskInstance],
        references: dict[ResultObjectReferenceIdentity, ResultObjectReference],
    ) -> WorkflowRunReplayIssue | None:
        """Return the first malformed no-Task scientific-decision correlation."""
        requests = {
            request.identity: request for request in run.scientific_decision_requests
        }
        transitions = {
            transition.identity: transition
            for transition in run.transitions
            if type(transition) is ScientificDecisionWorkflowTransitionRecord
        }
        consumed_transitions: set[ScientificDecisionTransitionRecordIdentity] = set()
        for request in requests.values():
            if (
                request.workflow_identity != run.workflow_identity
                or request.workflow_run_identity != run.identity
                or request.affected_task_instance_identity not in instances
            ):
                return WorkflowRunReplayIssue(
                    code=(
                        WorkflowRunReplayIssueCode.SCIENTIFIC_DECISION_CORRELATION_ERROR
                    ),
                    operation_phase="scientific_decision_correlation",
                    diagnostic=(
                        "decision request must identify the represented Workflow, "
                        "run, and affected Task instance"
                    ),
                )

        for resolution in run.scientific_decision_resolutions:
            resolved_request = requests.get(resolution.request_identity)
            producer = resolution.producer_provenance
            transition = transitions.get(producer.transition_record_identity)
            matching_references = tuple(
                reference
                for reference in references.values()
                if reference.result.identity == resolution.identity
            )
            selected_option = (
                None
                if resolved_request is None
                else next(
                    (
                        option
                        for option in resolved_request.options
                        if option.identity == resolution.normalized_option_identity
                    ),
                    None,
                )
            )
            matching_output_assignments = (
                ()
                if transition is None or selected_option is None
                else tuple(
                    assignment
                    for assignment in (
                        transition.firing_result.firing_input.external_output_binding.assignments
                    )
                    if assignment.value.kind is ColoredPetriNetValueKind.STRING
                    and assignment.value.value == selected_option.value
                )
            )
            if (
                resolved_request is None
                or selected_option is None
                or resolution.response_source_identity
                != resolved_request.required_response_source_identity
                or resolution.authority_context_identity
                != resolved_request.required_authority_context_identity
                or producer.workflow_identity != run.workflow_identity
                or producer.workflow_run_identity != run.identity
                or transition is None
                or transition.workflow_identity != run.workflow_identity
                or transition.workflow_run_identity != run.identity
                or transition.definition_reference_identity
                != run.definition_reference_identity
                or transition.runtime_bundle_identity != run.runtime_bundle_identity
                or transition.request_identity != resolved_request.identity
                or transition.resolution_identity != resolution.identity
                or transition.producer_provenance_identity != producer.identity
                or transition.firing_result.firing_input.transition_identity
                != resolved_request.affected_transition_identity
                or len(matching_output_assignments) != 1
                or len(matching_references) != 1
                or matching_references[0].content_identity
                != resolution.content_identity
                or matching_references[0].producer_provenance != producer
            ):
                return WorkflowRunReplayIssue(
                    code=(
                        WorkflowRunReplayIssueCode.SCIENTIFIC_DECISION_CORRELATION_ERROR
                    ),
                    operation_phase="scientific_decision_correlation",
                    diagnostic=(
                        "decision request, resolution, no-Task provenance, result "
                        "reference, and transition must close exactly"
                    ),
                )
            consumed_transitions.add(transition.identity)
        for request in requests.values():
            history = sorted(
                (
                    resolution
                    for resolution in run.scientific_decision_resolutions
                    if resolution.request_identity == request.identity
                ),
                key=lambda resolution: (
                    transitions[
                        resolution.producer_provenance.transition_record_identity
                    ].sequence_index
                ),
            )
            effective_predecessor: ResultObjectIdentity | None = None
            for resolution in history:
                if resolution.predecessor_resolution_identity != effective_predecessor:
                    return WorkflowRunReplayIssue(
                        code=(
                            WorkflowRunReplayIssueCode.SCIENTIFIC_DECISION_CORRELATION_ERROR
                        ),
                        operation_phase="scientific_decision_correlation",
                        diagnostic=(
                            "decision correction must consume the exact effective "
                            "same-request predecessor"
                        ),
                    )
                effective_predecessor = resolution.identity
        if consumed_transitions != set(transitions):
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.SCIENTIFIC_DECISION_CORRELATION_ERROR,
                operation_phase="scientific_decision_correlation",
                diagnostic=(
                    "every scientific-decision transition requires one exact resolution"
                ),
            )
        return None

    @staticmethod
    def _nested_correlation_issue(
        run: WorkflowRun,
        instances: dict[TaskInstanceIdentity, TaskInstance],
        activations: dict[TaskActivationIdentity, TaskActivation],
        attempt_records: dict[TaskAttemptRecordIdentity, TaskAttempt],
        outcomes: dict[TaskInvocationOutcomeIdentity, TaskInvocationOutcome],
        references: dict[ResultObjectReferenceIdentity, ResultObjectReference],
        dependencies: dict[ResultDependencyIdentity, ResultDependency],
        failures: dict[TaskFailureRecordIdentity, TaskFailureRecord],
    ) -> WorkflowRunReplayIssue | None:
        """Return the first malformed nested-run or export correlation."""
        memberships = {
            membership.child_workflow_run_identity: membership
            for membership in run.nested_memberships
        }
        invocations = {
            invocation.child_workflow_run_identity: invocation
            for invocation in run.nested_invocations
        }
        if set(memberships) != set(invocations):
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.NESTED_WORKFLOW_CORRELATION_ERROR,
                operation_phase="nested_correlation",
                diagnostic=(
                    "every nested membership and invocation must name the same one "
                    "distinct child run"
                ),
            )

        nested_attempts = {
            attempt.attempt_identity: attempt.child_workflow_run_identity
            for attempt in run.attempts
            if attempt.child_workflow_run_identity is not None
        }
        invocation_attempts: set[AttemptIdentity] = set()
        consumed_admissions: set[ResultDependencyIdentity] = set()
        exported_references: set[ResultObjectReferenceIdentity] = set()
        expected_attempt_status = {
            NestedWorkflowInvocationKind.CONFIRMED: TaskAttemptStatus.CONFIRMED,
            NestedWorkflowInvocationKind.REJECTED: TaskAttemptStatus.REJECTED,
            NestedWorkflowInvocationKind.INDETERMINATE: TaskAttemptStatus.INDETERMINATE,
        }
        expected_outcome_kind = {
            NestedWorkflowInvocationKind.CONFIRMED: TaskInvocationOutcomeKind.CONFIRMED,
            NestedWorkflowInvocationKind.REJECTED: TaskInvocationOutcomeKind.REJECTED,
            NestedWorkflowInvocationKind.INDETERMINATE: (
                TaskInvocationOutcomeKind.INDETERMINATE
            ),
        }
        for child_run_identity, invocation in invocations.items():
            membership = memberships[child_run_identity]
            activation = activations.get(invocation.activation_identity)
            attempt = attempt_records.get(invocation.attempt_record_identity)
            if (
                invocation.parent_workflow_run_identity != run.identity
                or membership.parent_workflow_run_identity != run.identity
                or membership.parent_revision_identity
                != invocation.parent_revision_identity
                or membership.parent_task_instance_identity
                != invocation.parent_task_instance_identity
                or membership.child_workflow_identity
                != invocation.child_workflow_identity
                or membership.child_workflow_run_identity
                != invocation.child_workflow_run_identity
                or invocation.parent_task_instance_identity not in instances
                or activation is None
                or activation.task_instance.identity
                != invocation.parent_task_instance_identity
                or activation.operation_identity != invocation.operation_identity
                or activation.attempt_identity != invocation.attempt_identity
                or attempt is None
                or attempt.task_instance_identity
                != invocation.parent_task_instance_identity
                or attempt.activation_identity != invocation.activation_identity
                or attempt.operation_identity != invocation.operation_identity
                or attempt.attempt_identity != invocation.attempt_identity
                or attempt.child_workflow_run_identity
                != invocation.child_workflow_run_identity
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.NESTED_WORKFLOW_CORRELATION_ERROR,
                    operation_phase="nested_correlation",
                    diagnostic=(
                        "nested membership, activation, attempt, and child identities "
                        "must close over one parent invocation"
                    ),
                )
            invocation_attempts.add(invocation.attempt_identity)

            input_references = tuple(
                references.get(identity)
                for identity in invocation.input_result_reference_identities
            )
            if any(reference is None for reference in input_references):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.NESTED_WORKFLOW_CORRELATION_ERROR,
                    operation_phase="nested_correlation",
                    diagnostic="nested invocation input references must exist",
                )
            input_result_identities = {
                reference.result.identity
                for reference in input_references
                if reference is not None
            }
            if input_result_identities != {
                binding.result.identity for binding in activation.inputs
            }:
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.NESTED_WORKFLOW_CORRELATION_ERROR,
                    operation_phase="nested_correlation",
                    diagnostic=(
                        "nested invocation inputs must equal its activation inputs"
                    ),
                )

            matching_outcomes = tuple(
                outcome
                for outcome in outcomes.values()
                if outcome.activation_identity == invocation.activation_identity
                and outcome.operation_identity == invocation.operation_identity
                and outcome.attempt_identity == invocation.attempt_identity
            )
            if invocation.kind is NestedWorkflowInvocationKind.PENDING:
                if attempt.status is not TaskAttemptStatus.STARTED or matching_outcomes:
                    return WorkflowRunReplayIssue(
                        code=(
                            WorkflowRunReplayIssueCode.NESTED_WORKFLOW_CORRELATION_ERROR
                        ),
                        operation_phase="nested_correlation",
                        diagnostic=(
                            "pending nested invocation requires one started attempt "
                            "and no generic outcome"
                        ),
                    )
                continue

            expected_status = expected_attempt_status[invocation.kind]
            expected_kind = expected_outcome_kind[invocation.kind]
            if (
                attempt.status is not expected_status
                or len(matching_outcomes) != 1
                or matching_outcomes[0].kind is not expected_kind
                or matching_outcomes[0].terminal_attempt_record_identity
                != attempt.identity
            ):
                return WorkflowRunReplayIssue(
                    code=WorkflowRunReplayIssueCode.NESTED_WORKFLOW_CORRELATION_ERROR,
                    operation_phase="nested_correlation",
                    diagnostic=(
                        "terminal nested observation must match one exact attempt "
                        "and generic outcome"
                    ),
                )
            outcome = matching_outcomes[0]
            if invocation.kind is NestedWorkflowInvocationKind.REJECTED:
                if (
                    outcome.failure_record_identity
                    != invocation.failure_record_identity
                    or invocation.failure_record_identity not in failures
                ):
                    return WorkflowRunReplayIssue(
                        code=(
                            WorkflowRunReplayIssueCode.NESTED_WORKFLOW_CORRELATION_ERROR
                        ),
                        operation_phase="nested_correlation",
                        diagnostic=(
                            "rejected nested invocation must name its exact failure"
                        ),
                    )
                continue
            if invocation.kind is NestedWorkflowInvocationKind.INDETERMINATE:
                if (
                    outcome.reconciliation_identity_values
                    != invocation.reconciliation_identity_values
                ):
                    return WorkflowRunReplayIssue(
                        code=(
                            WorkflowRunReplayIssueCode.NESTED_WORKFLOW_CORRELATION_ERROR
                        ),
                        operation_phase="nested_correlation",
                        diagnostic=(
                            "indeterminate nested invocation must preserve exact "
                            "reconciliation identities"
                        ),
                    )
                continue

            outcome_reference_identities = tuple(
                sorted(
                    (reference.identity for reference in outcome.results),
                    key=lambda identity: identity.value,
                )
            )
            if (
                outcome_reference_identities
                != invocation.exported_result_reference_identities
            ):
                return WorkflowRunReplayIssue(
                    code=(
                        WorkflowRunReplayIssueCode.NESTED_WORKFLOW_EXPORT_CORRELATION_ERROR
                    ),
                    operation_phase="nested_export_correlation",
                    diagnostic=(
                        "confirmed nested outcome must contain exactly its explicit "
                        "child exports"
                    ),
                )
            for reference_identity, dependency_identity in zip(
                invocation.exported_result_reference_identities,
                invocation.export_admission_dependency_identities,
                strict=True,
            ):
                reference = references.get(reference_identity)
                dependency = dependencies.get(dependency_identity)
                if (
                    reference is None
                    or reference.identity in exported_references
                    or type(reference.producer_provenance)
                    is not RepresentedTaskResultProducer
                    or reference.producer_provenance.workflow_identity
                    != invocation.child_workflow_identity
                    or reference.producer_provenance.workflow_run_identity
                    != invocation.child_workflow_run_identity
                    or dependency is None
                    or dependency.identity in consumed_admissions
                    or dependency.result_reference_identity != reference.identity
                    or dependency.producer_workflow_run_identity
                    != invocation.child_workflow_run_identity
                    or dependency.consumer_workflow_run_identity != run.identity
                    or dependency.consumer_task_instance_identity
                    != invocation.parent_task_instance_identity
                    or dependency.consumer_activation_identity
                    != invocation.activation_identity
                ):
                    return WorkflowRunReplayIssue(
                        code=(
                            WorkflowRunReplayIssueCode.NESTED_WORKFLOW_EXPORT_CORRELATION_ERROR
                        ),
                        operation_phase="nested_export_correlation",
                        diagnostic=(
                            "each child export requires one exact parent admission "
                            "dependency while retaining child producer provenance"
                        ),
                    )
                exported_references.add(reference.identity)
                consumed_admissions.add(dependency.identity)

        invocation_children = {
            invocation.attempt_identity: invocation.child_workflow_run_identity
            for invocation in run.nested_invocations
        }
        if (
            len(invocation_children) != len(run.nested_invocations)
            or nested_attempts != invocation_children
            or set(invocation_children) != invocation_attempts
        ):
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.NESTED_WORKFLOW_CORRELATION_ERROR,
                operation_phase="nested_correlation",
                diagnostic=(
                    "every child-correlated attempt must belong to one nested "
                    "invocation"
                ),
            )
        all_admissions = {
            identity
            for invocation in run.nested_invocations
            for identity in invocation.export_admission_dependency_identities
        }
        if consumed_admissions != all_admissions:
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.NESTED_WORKFLOW_EXPORT_CORRELATION_ERROR,
                operation_phase="nested_export_correlation",
                diagnostic=(
                    "every declared child export admission must close exactly once"
                ),
            )
        return None

    @staticmethod
    def _transition_correlations_match(
        transition: TaskWorkflowTransitionRecord,
        activation: TaskActivation,
        attempt: TaskAttempt,
        outcome: TaskInvocationOutcome,
    ) -> bool:
        """Return whether one transition closes over one confirmed invocation."""
        return (
            transition.activation_identity == activation.identity
            and transition.operation_identity == activation.operation_identity
            and transition.attempt_identity == activation.attempt_identity
            and attempt.activation_identity == activation.identity
            and attempt.operation_identity == activation.operation_identity
            and attempt.attempt_identity == activation.attempt_identity
            and attempt.status is TaskAttemptStatus.CONFIRMED
            and transition.terminal_attempt_record_identity == attempt.identity
            and outcome.terminal_attempt_record_identity == attempt.identity
            and outcome.activation_identity == activation.identity
            and outcome.operation_identity == activation.operation_identity
            and outcome.attempt_identity == activation.attempt_identity
            and outcome.kind is TaskInvocationOutcomeKind.CONFIRMED
            and transition.firing_result.firing_input.selection_result.identity
            == activation.selection.selection_result_identity
        )

    @staticmethod
    def _transition_implementation_issue(
        transition: TaskWorkflowTransitionRecord
        | ScientificDecisionWorkflowTransitionRecord,
        runtime_bundle: WorkflowRuntimeBundle,
    ) -> WorkflowRunReplayIssue | None:
        """Return an unsupported-version issue for one retained derivation."""
        firing = transition.firing_result
        firing_input = firing.firing_input
        enablement = firing_input.enablement_result
        selection = firing_input.selection_result
        assert firing.audit is not None
        checks = (
            firing_input.definition != runtime_bundle.definition,
            enablement.expression_evaluator_identity
            != runtime_bundle.expression_evaluator_identity,
            enablement.ordering_policy_identity
            != runtime_bundle.ordering_policy_identity,
            enablement.transition_enabler_identity
            != runtime_bundle.transition_enabler_identity,
            selection.selector_identity != runtime_bundle.binding_selector_identity,
            selection.ordering_policy_identity
            != runtime_bundle.ordering_policy_identity,
            firing.audit.firer_identity != runtime_bundle.transition_firer_identity,
        )
        if any(checks):
            return WorkflowRunReplayIssue(
                code=WorkflowRunReplayIssueCode.IMPLEMENTATION_IDENTITY_MISMATCH,
                operation_phase="transition_compatibility",
                diagnostic=(
                    "retained transition uses a definition or implementation identity "
                    "outside the runtime bundle"
                ),
            )
        return None

    @classmethod
    def _error(
        cls,
        run: WorkflowRun,
        runtime_bundle: WorkflowRuntimeBundle,
        code: WorkflowRunReplayIssueCode,
        phase: str,
        diagnostic: str,
    ) -> WorkflowRunReplayResult:
        """Construct one closed replay error; this helper owns no evidence claim."""
        issue = WorkflowRunReplayIssue(
            code=code,
            operation_phase=phase,
            diagnostic=diagnostic,
        )
        return cls._result(
            run,
            runtime_bundle,
            WorkflowRunReplayOutcomeKind.ERROR,
            None,
            (issue,),
        )

    @staticmethod
    def _result(
        run: WorkflowRun,
        runtime_bundle: WorkflowRuntimeBundle,
        outcome: WorkflowRunReplayOutcomeKind,
        reconstructed_marking: ColoredPetriNetMarking | None,
        issues: tuple[WorkflowRunReplayIssue, ...],
    ) -> WorkflowRunReplayResult:
        """Construct one deterministically identified closed replay result."""
        state = {
            "domain": "ksdft2effmass.workflows.workflow-run-replay-result-v1",
            "run": run.identity.value,
            "revision": run.revision_identity.value,
            "runtime_bundle": runtime_bundle.identity.value,
            "outcome": outcome.value,
            "reconstructed_marking": (
                None
                if reconstructed_marking is None
                else WorkflowRunReplayer._marking_content_state(reconstructed_marking)
            ),
            "issues": [
                [issue.code.value, issue.operation_phase, issue.diagnostic]
                for issue in issues
            ],
        }
        digest = sha256(
            json.dumps(
                state,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        return WorkflowRunReplayResult(
            identity=WorkflowRunReplayResultIdentity(digest),
            workflow_run_identity=run.identity,
            revision_identity=run.revision_identity,
            runtime_bundle_identity=runtime_bundle.identity,
            outcome=outcome,
            reconstructed_marking=reconstructed_marking,
            issues=issues,
        )

    @staticmethod
    def _marking_content_state(marking: ColoredPetriNetMarking) -> str:
        """Return deterministic length-delimited state for replay-result identity."""
        fields = [marking.identity.value, marking.definition_identity.value]
        for place in marking.places:
            fields.append(place.place_identity.value)
            for token in place.tokens:
                fields.extend(
                    (
                        token.color_identity.value,
                        token.value.kind.value,
                        WorkflowRunReplayer._generic_value_state(token.value.value),
                        (
                            ""
                            if token.token_identity is None
                            else token.token_identity.value
                        ),
                    )
                )
        return "".join(f"{len(value)}:{value}" for value in fields)

    @staticmethod
    def _generic_value_state(
        value: None | bool | int | float | str | tuple[str, ...],
    ) -> str:
        """Return one exact generic value representation for result identity."""
        if value is None:
            return "none"
        if type(value) is bool:
            return "true" if value else "false"
        if type(value) is int:
            return str(value)
        if type(value) is float:
            return value.hex()
        if type(value) is tuple:
            return json.dumps(list(value), ensure_ascii=False, separators=(",", ":"))
        assert type(value) is str
        return value
