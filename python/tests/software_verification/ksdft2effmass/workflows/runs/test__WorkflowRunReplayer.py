r"""Software verification of ``WorkflowRunReplayer``.

Evidence profile: routine

Bounded artifact scope: the public effect-free ``WorkflowRunReplayer`` ActionObject.

Facet and represented meaning

The replayer reconstructs one canonical task-origin and scientific-decision-origin
WorkflowRun marking history, including nested child-run and control-state correlations,
from retained pure CPN firing inputs and one explicit immutable runtime bundle.

Intrinsic and cross-object scope

``WorkflowRunReplayer`` is the sole system under test. The oracle is a hand-built
one-transition generic net whose exact predecessor and successor markings are derived
through the independently public pure CPN contract. Nested evidence uses explicit
parent/child identities and parent admission dependencies from the accepted contract.

VVUQ and scientific exclusions

This is software verification only. Exact represented replay establishes no Task
execution, persistence, scientific calculation, validation, uncertainty
quantification, authority, or human acceptance.
"""

from dataclasses import dataclass, replace

import pytest

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetArcDefinition,
    ColoredPetriNetArcIdentity,
    ColoredPetriNetBinding,
    ColoredPetriNetBindingAssignment,
    ColoredPetriNetBindingSelector,
    ColoredPetriNetBindingVariableIdentity,
    ColoredPetriNetColorDefinition,
    ColoredPetriNetColorIdentity,
    ColoredPetriNetDefinition,
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetFiringInput,
    ColoredPetriNetFiringOutcomeKind,
    ColoredPetriNetFiringResultIdentity,
    ColoredPetriNetGuardExpression,
    ColoredPetriNetGuardOperator,
    ColoredPetriNetInputInscription,
    ColoredPetriNetInputMode,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingIdentity,
    ColoredPetriNetOutputInscription,
    ColoredPetriNetPlaceDefinition,
    ColoredPetriNetPlaceIdentity,
    ColoredPetriNetPlaceMarking,
    ColoredPetriNetSelectionResultIdentity,
    ColoredPetriNetToken,
    ColoredPetriNetTokenIdentity,
    ColoredPetriNetTokenPattern,
    ColoredPetriNetTokenTemplate,
    ColoredPetriNetTransitionDefinition,
    ColoredPetriNetTransitionEnabler,
    ColoredPetriNetTransitionFirer,
    ColoredPetriNetTransitionIdentity,
    ColoredPetriNetValue,
    ColoredPetriNetValueExpression,
    ColoredPetriNetValueExpressionKind,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.workflows import (
    AttemptIdentity,
    DirectTaskActivationSelection,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivation,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    AuthorityContextIdentity,
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeIdentity,
    AuthorityReservationOutcomeKind,
    ChildWorkflowCreationIdempotencyIdentity,
    DispatchCreationIdempotencyIdentity,
    DispatchDestinationIdentity,
    DispatchOutcomeKind,
    DispatchOutcomeRecord,
    DispatchOutcomeRecordIdentity,
    DispatchResourceScopeIdentity,
    ExecutionGrantIdentity,
    ExecutionGrantRevisionIdentity,
    ExternalProducerAttemptIdentity,
    ExternalResultProducer,
    ExternalResultProducerIdentity,
    NestedWorkflowInvocation,
    NestedWorkflowInvocationIdentity,
    NestedWorkflowInvocationKind,
    NestedWorkflowMembership,
    NestedWorkflowMembershipIdentity,
    NestedWorkflowObservationIdentity,
    ObligationIdentity,
    RepresentedScientificDecisionIngressProducer,
    RepresentedTaskResultProducer,
    ResponseSourceIdentity,
    ResultDependency,
    ResultDependencyIdentity,
    ResultObjectContentIdentity,
    ResultObjectDomainIdentity,
    ResultObjectReference,
    ResultObjectReferenceIdentity,
    ResultObjectTypeIdentity,
    ResultProducerEvidenceIdentity,
    ResultProducerProvenanceIdentity,
    ResultProductionRecord,
    ResultProductionRecordIdentity,
    ScientificDecisionOption,
    ScientificDecisionOptionIdentity,
    ScientificDecisionRecorderIdentity,
    ScientificDecisionRequest,
    ScientificDecisionRequestIdentity,
    ScientificDecisionResolution,
    ScientificDecisionTransitionRecordIdentity,
    ScientificDecisionWorkflowTransitionRecord,
    ScientificExecutionAuthorityReference,
    ScientificExecutionAuthoritySnapshotIdentity,
    ScientificExecutionAuthorityStateIdentity,
    ScientificExecutorIdentity,
    SimulationDispatchObligation,
    SimulationDispatchOutcomeIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestCorrelation,
    SimulationExecutionRequestCorrelationIdentity,
    SimulationExecutionRequestIdentity,
    TaskAttempt,
    TaskAttemptRecordIdentity,
    TaskAttemptStatus,
    TaskFailureRecord,
    TaskFailureRecordIdentity,
    TaskInvocationFailure,
    TaskInvocationFailureIdentity,
    TaskInvocationOutcome,
    TaskInvocationOutcomeIdentity,
    TaskInvocationOutcomeKind,
    TaskWorkflowMembership,
    TaskWorkflowMembershipIdentity,
    TaskWorkflowTransitionRecord,
    TaskWorkflowTransitionRecordIdentity,
    WorkflowDefinitionReference,
    WorkflowDefinitionReferenceIdentity,
    WorkflowRun,
    WorkflowRunReplayer,
    WorkflowRunReplayIssueCode,
    WorkflowRunReplayOutcomeKind,
    WorkflowRunReplayResultIdentity,
    WorkflowRunRevisionIdentity,
    WorkflowRuntimeBundle,
    WorkflowRuntimeBundleIdentity,
    WorkflowTransitionSequenceIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunReplayer


@dataclass(frozen=True, slots=True)
class _SyntheticResult:
    """Provide one immutable ResultObject returned by the synthetic Task."""

    identity: ResultObjectIdentity


class TestWorkflowRunReplayer:
    """Own software evidence for deterministic WorkflowRun replay."""

    @staticmethod
    def make_definition() -> ColoredPetriNetDefinition:
        """Construct one hand-inspectable consume-and-produce CPN definition."""
        color = ColoredPetriNetColorDefinition(
            ColoredPetriNetColorIdentity("workflow-result"),
            (ColoredPetriNetValueKind.STRING,),
        )
        input_place = ColoredPetriNetPlaceDefinition(
            ColoredPetriNetPlaceIdentity("prepared"), (color.identity,)
        )
        output_place = ColoredPetriNetPlaceDefinition(
            ColoredPetriNetPlaceIdentity("completed"), (color.identity,)
        )
        input_variable = ColoredPetriNetBindingVariableIdentity("input")
        output_variable = ColoredPetriNetBindingVariableIdentity("output")
        transition = ColoredPetriNetTransitionDefinition(
            ColoredPetriNetTransitionIdentity("execute"),
            (input_variable,),
            (output_variable,),
            ColoredPetriNetGuardExpression(ColoredPetriNetGuardOperator.TRUE),
        )
        input_arc = ColoredPetriNetArcDefinition(
            ColoredPetriNetArcIdentity("execute.input"),
            input_place.identity,
            transition.identity,
            ColoredPetriNetInputInscription(
                ColoredPetriNetInputMode.CONSUME,
                (ColoredPetriNetTokenPattern(input_variable, (color.identity,)),),
            ),
        )
        output_expression = ColoredPetriNetValueExpression(
            ColoredPetriNetValueExpressionKind.VARIABLE,
            variable_identity=output_variable,
        )
        output_arc = ColoredPetriNetArcDefinition(
            ColoredPetriNetArcIdentity("execute.output"),
            output_place.identity,
            transition.identity,
            output_inscription=ColoredPetriNetOutputInscription(
                (
                    ColoredPetriNetTokenTemplate(
                        color.identity,
                        output_expression,
                        output_expression,
                    ),
                )
            ),
        )
        return ColoredPetriNetDefinition(
            ColoredPetriNetDefinitionIdentity("workflow.replay.test.v1"),
            (color,),
            (input_place, output_place),
            (transition,),
            (input_arc, output_arc),
            (transition.identity,),
        )

    @staticmethod
    def make_initial_marking(
        definition: ColoredPetriNetDefinition,
    ) -> ColoredPetriNetMarking:
        """Construct the exact predecessor with one individually identified token."""
        color = definition.colors[0].identity
        places = {place.identity.value: place.identity for place in definition.places}
        token = ColoredPetriNetToken(
            color,
            ColoredPetriNetValue(ColoredPetriNetValueKind.STRING, "input.one"),
            ColoredPetriNetTokenIdentity("input.token.one"),
        )
        return ColoredPetriNetMarking(
            ColoredPetriNetMarkingIdentity("marking.initial"),
            definition.identity,
            (
                ColoredPetriNetPlaceMarking(places["prepared"], (token,)),
                ColoredPetriNetPlaceMarking(places["completed"], ()),
            ),
        )

    @classmethod
    def make_run_and_bundle(cls) -> tuple[WorkflowRun, WorkflowRuntimeBundle]:
        """Construct one exact successful task-origin WorkflowRun revision."""
        definition = cls.make_definition()
        initial = cls.make_initial_marking(definition)
        enablement = ColoredPetriNetTransitionEnabler().execute(definition, initial)
        selection = ColoredPetriNetBindingSelector().execute(definition, enablement)
        assert selection.selected_binding is not None
        external = ColoredPetriNetBinding(
            ColoredPetriNetTransitionIdentity("execute"),
            (
                ColoredPetriNetBindingAssignment(
                    ColoredPetriNetBindingVariableIdentity("output"),
                    ColoredPetriNetValue(ColoredPetriNetValueKind.STRING, "result.one"),
                ),
            ),
        )
        firing = ColoredPetriNetTransitionFirer().execute(
            ColoredPetriNetFiringInput(
                definition,
                ColoredPetriNetTransitionIdentity("execute"),
                initial,
                enablement,
                selection,
                selection.selected_binding,
                None,
                external,
            )
        )
        assert firing.outcome is ColoredPetriNetFiringOutcomeKind.SUCCESS
        assert firing.successor_marking is not None
        assert firing.audit is not None

        workflow_identity = WorkflowIdentity("workflow.one")
        run_identity = WorkflowRunIdentity("run.one")
        task_instance = TaskInstance(
            TaskInstanceIdentity("instance.one"),
            TaskDefinitionIdentity("task.one"),
            None,
        )
        operation_identity = OperationIdentity("operation.one")
        attempt_identity = AttemptIdentity("attempt.one")
        activation = TaskActivation(
            TaskActivationIdentity("activation.one"),
            workflow_identity,
            run_identity,
            task_instance,
            operation_identity,
            attempt_identity,
            (),
            DirectTaskActivationSelection(selection.identity),
        )
        started_attempt = TaskAttempt(
            identity=TaskAttemptRecordIdentity("attempt.one.started"),
            workflow_run_identity=run_identity,
            task_instance_identity=task_instance.identity,
            activation_identity=activation.identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            status=TaskAttemptStatus.STARTED,
        )
        terminal_attempt = TaskAttempt(
            identity=TaskAttemptRecordIdentity("attempt.one.confirmed"),
            workflow_run_identity=run_identity,
            task_instance_identity=task_instance.identity,
            activation_identity=activation.identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            status=TaskAttemptStatus.CONFIRMED,
            predecessor_attempt_record_identity=started_attempt.identity,
        )
        outcome_identity = TaskInvocationOutcomeIdentity("outcome.one")
        production_identity = ResultProductionRecordIdentity("production.one")
        result_reference = ResultObjectReference(
            identity=ResultObjectReferenceIdentity("result-reference.one"),
            result=_SyntheticResult(ResultObjectIdentity("result.one")),
            concrete_type_identity=ResultObjectTypeIdentity("synthetic-result.v1"),
            owning_domain_identity=ResultObjectDomainIdentity("test.synthetic"),
            content_identity=ResultObjectContentIdentity("content.result.one"),
            producer_provenance=RepresentedTaskResultProducer(
                identity=ResultProducerProvenanceIdentity("producer.one"),
                workflow_identity=workflow_identity,
                workflow_run_identity=run_identity,
                task_instance_identity=task_instance.identity,
                activation_identity=activation.identity,
                operation_identity=operation_identity,
                attempt_identity=attempt_identity,
                terminal_attempt_record_identity=terminal_attempt.identity,
                outcome_identity=outcome_identity,
                production_identity=production_identity,
            ),
        )
        outcome = TaskInvocationOutcome(
            identity=outcome_identity,
            workflow_run_identity=run_identity,
            activation_identity=activation.identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_attempt.identity,
            kind=TaskInvocationOutcomeKind.CONFIRMED,
            results=(result_reference,),
            production_record_identities=(production_identity,),
        )
        production = ResultProductionRecord(
            identity=production_identity,
            workflow_run_identity=run_identity,
            task_instance_identity=task_instance.identity,
            activation_identity=activation.identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_attempt.identity,
            outcome_identity=outcome.identity,
            result_reference_identity=result_reference.identity,
            result_artifact_relation_identities=(),
            external_output_binding=external,
        )
        transition = TaskWorkflowTransitionRecord(
            identity=TaskWorkflowTransitionRecordIdentity("transition.task.one"),
            sequence_identity=WorkflowTransitionSequenceIdentity("sequence.zero"),
            sequence_index=0,
            workflow_identity=workflow_identity,
            workflow_run_identity=run_identity,
            definition_reference_identity=WorkflowDefinitionReferenceIdentity(
                "definition-reference.one"
            ),
            runtime_bundle_identity=WorkflowRuntimeBundleIdentity("bundle.one"),
            activation_identity=activation.identity,
            operation_identity=operation_identity,
            attempt_identity=attempt_identity,
            terminal_attempt_record_identity=terminal_attempt.identity,
            outcome_identity=outcome.identity,
            result_production_identities=(production.identity,),
            firing_result=firing,
        )
        bundle_identity = WorkflowRuntimeBundleIdentity("bundle.one")
        definition_reference = WorkflowDefinitionReference(
            identity=WorkflowDefinitionReferenceIdentity("definition-reference.one"),
            workflow_identity=workflow_identity,
            workflow_definition_version=1,
            colored_petri_net_definition_identity=definition.identity,
            colored_petri_net_definition_version=1,
            task_definition_identities=(task_instance.definition_identity,),
            schema_version=1,
        )
        bundle = WorkflowRuntimeBundle(
            identity=bundle_identity,
            definition_reference=definition_reference,
            schema_version=1,
            workflow_identity=workflow_identity,
            definition=definition,
            task_definition_identities=(task_instance.definition_identity,),
            adapter_implementation_identity="workflow-cpn-adapter-v1",
            expression_evaluator_identity=enablement.expression_evaluator_identity,
            ordering_policy_identity=enablement.ordering_policy_identity,
            transition_enabler_identity=enablement.transition_enabler_identity,
            binding_selector_identity=selection.selector_identity,
            transition_firer_identity=firing.audit.firer_identity,
        )
        run = WorkflowRun(
            identity=run_identity,
            revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            predecessor_revision_identity=WorkflowRunRevisionIdentity(
                "revision.initial"
            ),
            workflow_identity=workflow_identity,
            definition_reference_identity=definition_reference.identity,
            runtime_bundle_identity=bundle_identity,
            schema_version=1,
            adapter_implementation_identity="workflow-cpn-adapter-v1",
            task_instances=(task_instance,),
            task_memberships=(
                TaskWorkflowMembership(
                    identity=TaskWorkflowMembershipIdentity("membership.task.one"),
                    workflow_run_identity=run_identity,
                    workflow_identity=workflow_identity,
                    task_instance_identity=task_instance.identity,
                ),
            ),
            nested_memberships=(),
            nested_invocations=(),
            activations=(activation,),
            attempts=(started_attempt, terminal_attempt),
            outcomes=(outcome,),
            result_references=(result_reference,),
            result_productions=(production,),
            result_dependencies=(),
            failures=(),
            authority_references=(),
            execution_request_correlations=(),
            authority_reservations=(),
            dispatch_obligations=(),
            dispatch_outcomes=(),
            obligation_dispositions=(),
            scientific_decision_requests=(),
            scientific_decision_resolutions=(),
            initial_marking=initial,
            current_marking=firing.successor_marking,
            transitions=(transition,),
        )
        return run, bundle

    def test_method__execute__returns_equal_for_exact_reconstruction(self) -> None:
        """Replay one exact successful transition to the retained current marking.

        Evidence ID: SV-WFR-REPLAY-001

        Requirement: Exact runtime identities and retained pure firing inputs
        reconstruct the represented current marking.

        Acceptance: Repeated replay returns equal closed results with deterministic
        identities and the exact retained current marking.
        """
        run, bundle = self.make_run_and_bundle()

        first = SUT().execute(run, bundle)
        second = SUT().execute(run, bundle)

        assert first == second
        assert first.outcome is WorkflowRunReplayOutcomeKind.EQUAL
        assert first.reconstructed_marking == run.current_marking
        assert first.issues == ()

    def test_method__execute__returns_equal_for_empty_history(self) -> None:
        """Treat an unchanged initial marking as a complete empty replay.

        Evidence ID: SV-WFR-REPLAY-005

        Requirement: A transition-free run whose current marking equals its initial
        marking is replay-equal without fabricating an invocation.

        Acceptance: Removing the represented invocation history and restoring the
        initial marking returns ``equal`` with that marking.
        """
        run, bundle = self.make_run_and_bundle()
        empty = replace(
            run,
            predecessor_revision_identity=None,
            activations=(),
            attempts=(),
            outcomes=(),
            result_references=(),
            result_productions=(),
            current_marking=run.initial_marking,
            transitions=(),
        )

        result = SUT().execute(empty, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.EQUAL
        assert result.reconstructed_marking == run.initial_marking

    def test_method__execute__retains_non_success_outcomes_without_firing(self) -> None:
        """Replay rejected and indeterminate attempts without inventing transitions.

        Evidence ID: SV-WFR-REPLAY-006

        Requirement: Rejected and indeterminate invocation outcomes produce no
        successful generic firing and remain compatible with an unchanged marking.

        Acceptance: Both closed non-success variants replay ``equal`` with empty
        transition history and the exact initial marking.
        """
        run, bundle = self.make_run_and_bundle()
        original_attempt = run.attempts[-1]
        original_outcome = run.outcomes[0]
        rejected_attempt = replace(original_attempt, status=TaskAttemptStatus.REJECTED)
        failure_record_identity = TaskFailureRecordIdentity("failure-record.one")
        rejected_outcome = replace(
            original_outcome,
            kind=TaskInvocationOutcomeKind.REJECTED,
            results=(),
            production_record_identities=(),
            failure_record_identity=failure_record_identity,
        )
        failure_record = TaskFailureRecord(
            identity=failure_record_identity,
            workflow_run_identity=run.identity,
            task_instance_identity=run.task_instances[0].identity,
            activation_identity=run.activations[0].identity,
            operation_identity=run.activations[0].operation_identity,
            attempt_identity=rejected_attempt.attempt_identity,
            terminal_attempt_record_identity=rejected_attempt.identity,
            failure=TaskInvocationFailure(
                identity=TaskInvocationFailureIdentity("failure.one"),
                code="synthetic_failure",
                operation_phase="test_operation",
                diagnostic="synthetic software-verification failure",
                retryable=False,
                claim_boundary=("synthetic software-verification input",),
            ),
        )
        indeterminate_attempt = replace(
            original_attempt, status=TaskAttemptStatus.INDETERMINATE
        )
        indeterminate_outcome = replace(
            original_outcome,
            kind=TaskInvocationOutcomeKind.INDETERMINATE,
            results=(),
            production_record_identities=(),
            reconciliation_identity_values=("reconciliation.one",),
        )
        rejected_run = replace(
            run,
            attempts=(run.attempts[0], rejected_attempt),
            outcomes=(rejected_outcome,),
            result_references=(),
            result_productions=(),
            failures=(failure_record,),
            current_marking=run.initial_marking,
            transitions=(),
        )
        indeterminate_run = replace(
            run,
            attempts=(run.attempts[0], indeterminate_attempt),
            outcomes=(indeterminate_outcome,),
            result_references=(),
            result_productions=(),
            failures=(),
            current_marking=run.initial_marking,
            transitions=(),
        )

        rejected = SUT().execute(rejected_run, bundle)
        indeterminate = SUT().execute(indeterminate_run, bundle)

        assert rejected.outcome is WorkflowRunReplayOutcomeKind.EQUAL
        assert indeterminate.outcome is WorkflowRunReplayOutcomeKind.EQUAL
        assert rejected.reconstructed_marking == run.initial_marking
        assert indeterminate.reconstructed_marking == run.initial_marking

    def test_method__execute__replays_append_only_retry_history(self) -> None:
        """Replay a confirmed transition with a later rejected retry history.

        Evidence ID: SV-WFR-REPLAY-029

        Requirement: A retry uses new operation, activation, and attempt identities,
        names the earlier terminal attempt, and preserves every prior state record.

        Acceptance: The retained confirmed first attempt and non-firing rejected retry
        replay ``equal``; a second retry branching from the stale first attempt fails.
        """
        run, bundle = self.make_run_and_bundle()
        first_activation = run.activations[0]
        retry_operation = OperationIdentity("operation.two")
        retry_attempt_identity = AttemptIdentity("attempt.two")
        retry_activation = TaskActivation(
            TaskActivationIdentity("activation.two"),
            run.workflow_identity,
            run.identity,
            run.task_instances[0],
            retry_operation,
            retry_attempt_identity,
            (),
            first_activation.selection,
        )
        retry_started = TaskAttempt(
            identity=TaskAttemptRecordIdentity("attempt.two.started"),
            workflow_run_identity=run.identity,
            task_instance_identity=run.task_instances[0].identity,
            activation_identity=retry_activation.identity,
            operation_identity=retry_operation,
            attempt_identity=retry_attempt_identity,
            status=TaskAttemptStatus.STARTED,
            retry_of_attempt_identity=first_activation.attempt_identity,
        )
        retry_terminal = TaskAttempt(
            identity=TaskAttemptRecordIdentity("attempt.two.rejected"),
            workflow_run_identity=run.identity,
            task_instance_identity=run.task_instances[0].identity,
            activation_identity=retry_activation.identity,
            operation_identity=retry_operation,
            attempt_identity=retry_attempt_identity,
            status=TaskAttemptStatus.REJECTED,
            predecessor_attempt_record_identity=retry_started.identity,
        )
        failure = TaskFailureRecord(
            identity=TaskFailureRecordIdentity("failure-record.two"),
            workflow_run_identity=run.identity,
            task_instance_identity=run.task_instances[0].identity,
            activation_identity=retry_activation.identity,
            operation_identity=retry_operation,
            attempt_identity=retry_attempt_identity,
            terminal_attempt_record_identity=retry_terminal.identity,
            failure=TaskInvocationFailure(
                identity=TaskInvocationFailureIdentity("failure.two"),
                code="synthetic.retry.rejected",
                operation_phase="retry",
                diagnostic="synthetic rejected retry",
                retryable=False,
                claim_boundary=("software verification only",),
            ),
        )
        retry_outcome = TaskInvocationOutcome(
            identity=TaskInvocationOutcomeIdentity("outcome.two"),
            workflow_run_identity=run.identity,
            activation_identity=retry_activation.identity,
            operation_identity=retry_operation,
            attempt_identity=retry_attempt_identity,
            terminal_attempt_record_identity=retry_terminal.identity,
            kind=TaskInvocationOutcomeKind.REJECTED,
            failure_record_identity=failure.identity,
        )
        changed = replace(
            run,
            activations=run.activations + (retry_activation,),
            attempts=run.attempts + (retry_started, retry_terminal),
            outcomes=run.outcomes + (retry_outcome,),
            failures=(failure,),
        )

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.EQUAL
        assert result.reconstructed_marking == run.current_marking

        branch_operation = OperationIdentity("operation.three")
        branch_attempt_identity = AttemptIdentity("attempt.three")
        branch_activation = TaskActivation(
            TaskActivationIdentity("activation.three"),
            run.workflow_identity,
            run.identity,
            run.task_instances[0],
            branch_operation,
            branch_attempt_identity,
            (),
            first_activation.selection,
        )
        branch_started = TaskAttempt(
            identity=TaskAttemptRecordIdentity("attempt.three.started"),
            workflow_run_identity=run.identity,
            task_instance_identity=run.task_instances[0].identity,
            activation_identity=branch_activation.identity,
            operation_identity=branch_operation,
            attempt_identity=branch_attempt_identity,
            status=TaskAttemptStatus.STARTED,
            retry_of_attempt_identity=first_activation.attempt_identity,
        )
        branched = replace(
            changed,
            activations=tuple(
                sorted(
                    changed.activations + (branch_activation,),
                    key=lambda value: value.identity.value,
                )
            ),
            attempts=changed.attempts + (branch_started,),
        )

        branch_result = SUT().execute(branched, bundle)

        assert branch_result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in branch_result.issues) == (
            WorkflowRunReplayIssueCode.ATTEMPT_CORRELATION_ERROR,
        )

    def test_method__execute__returns_unequal_only_after_completed_replay(self) -> None:
        """Distinguish completed reconstruction from a differing stored final state.

        Evidence ID: SV-WFR-REPLAY-002

        Requirement: A completed transition replay whose reconstructed final marking
        differs from the stored current marking returns ``unequal`` with that
        reconstructed marking.

        Acceptance: Replacing only the stored current marking returns ``unequal`` and
        ``CURRENT_MARKING_UNEQUAL``.
        """
        run, bundle = self.make_run_and_bundle()
        changed = replace(run, current_marking=run.initial_marking)

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.UNEQUAL
        assert result.reconstructed_marking == run.current_marking
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.CURRENT_MARKING_UNEQUAL,
        )

    def test_method__execute__rejects_unsupported_runtime_identity(self) -> None:
        """Stop before replay when the explicit runtime bundle is incompatible.

        Evidence ID: SV-WFR-REPLAY-003

        Requirement: Runtime identity mismatch produces ``unsupported_version`` and
        no reconstructed marking.

        Acceptance: Replacing the adapter identity returns the exact closed outcome
        and implementation-identity issue.
        """
        run, bundle = self.make_run_and_bundle()
        unsupported = replace(
            bundle, adapter_implementation_identity="workflow-cpn-adapter-v2"
        )

        result = SUT().execute(run, unsupported)

        assert result.outcome is WorkflowRunReplayOutcomeKind.UNSUPPORTED_VERSION
        assert result.reconstructed_marking is None
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.IMPLEMENTATION_IDENTITY_MISMATCH,
        )

    def test_method__execute__errors_on_broken_predecessor_chain(self) -> None:
        """Fail closed when retained history does not begin at reconstructed state.

        Evidence ID: SV-WFR-REPLAY-004

        Requirement: Every transition predecessor must equal the rolling
        reconstructed marking.

        Acceptance: Replacing the retained firing predecessor returns ``error`` and
        ``PREDECESSOR_MARKING_MISMATCH`` without a reconstructed marking.
        """
        run, bundle = self.make_run_and_bundle()
        transition = run.transitions[0]
        firing = transition.firing_result
        alternate = replace(
            run.initial_marking,
            identity=ColoredPetriNetMarkingIdentity("marking.alternate"),
        )
        changed_input = replace(firing.firing_input, predecessor_marking=alternate)
        changed_firing = replace(firing, firing_input=changed_input)
        changed_transition = replace(transition, firing_result=changed_firing)
        changed = replace(run, transitions=(changed_transition,))

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert result.reconstructed_marking is None
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.PREDECESSOR_MARKING_MISMATCH,
        )

    def test_method__execute__rejects_stale_selection_identity(self) -> None:
        """Reject a retained firing input with a stale generic selection identity.

        Evidence ID: SV-WFR-REPLAY-027

        Requirement: Task activation and generic firing input identify the same exact
        selection result.

        Acceptance: Replacing only the activation's retained selection-result identity
        returns a transition/outcome correlation error.
        """
        run, bundle = self.make_run_and_bundle()
        transition = run.transitions[0]
        assert type(transition) is TaskWorkflowTransitionRecord
        changed_activation = replace(
            run.activations[0],
            selection=DirectTaskActivationSelection(
                ColoredPetriNetSelectionResultIdentity("0" * 64)
            ),
        )
        changed = replace(run, activations=(changed_activation,))

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.OUTCOME_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_retained_firing_result_mismatch(self) -> None:
        """Reject retained firing evidence that differs from pure recomputation.

        Evidence ID: SV-WFR-REPLAY-028

        Requirement: Replay compares the complete recomputed firing result with the
        retained result rather than accepting only its successor marking.

        Acceptance: Replacing only the firing-result content identity returns the
        firing-result mismatch error.
        """
        run, bundle = self.make_run_and_bundle()
        transition = run.transitions[0]
        assert type(transition) is TaskWorkflowTransitionRecord
        changed_firing = replace(
            transition.firing_result,
            identity=ColoredPetriNetFiringResultIdentity("0" * 64),
        )
        changed = replace(
            run,
            transitions=(replace(transition, firing_result=changed_firing),),
        )

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.FIRING_RESULT_MISMATCH,
        )

    def test_method__execute__rejects_reordered_attempt_state_history(self) -> None:
        """Reject a terminal attempt state ordered before its predecessor.

        Evidence ID: SV-WFR-REPLAY-007

        Requirement: Attempt-state records are append-only and each terminal record
        follows its exact same-attempt predecessor.

        Acceptance: Reversing the two attempt-state records returns ``error`` with an
        attempt-correlation issue and no reconstructed marking.
        """
        run, bundle = self.make_run_and_bundle()
        changed = replace(run, attempts=tuple(reversed(run.attempts)))

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert result.reconstructed_marking is None
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.ATTEMPT_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_unbound_terminal_attempt_record(self) -> None:
        """Reject an outcome naming no retained terminal attempt-state record.

        Evidence ID: SV-WFR-REPLAY-008

        Requirement: Every invocation outcome identifies the exact retained terminal
        state record for its stable attempt.

        Acceptance: Replacing that identity with an absent record returns ``error``
        with an outcome-correlation issue and no reconstructed marking.
        """
        run, bundle = self.make_run_and_bundle()
        outcome = replace(
            run.outcomes[0],
            terminal_attempt_record_identity=TaskAttemptRecordIdentity(
                "attempt.one.absent"
            ),
        )
        changed = replace(run, outcomes=(outcome,))

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert result.reconstructed_marking is None
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.OUTCOME_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_unbound_result_production(self) -> None:
        """Reject a production record naming no retained ResultObject reference.

        Evidence ID: SV-WFR-REPLAY-009

        Requirement: A confirmed outcome, its ResultObject reference, producer
        provenance, production record, and transition close over one invocation.

        Acceptance: Replacing the production's result-reference identity returns
        ``error`` with a result-correlation issue and no reconstructed marking.
        """
        run, bundle = self.make_run_and_bundle()
        production = replace(
            run.result_productions[0],
            result_reference_identity=ResultObjectReferenceIdentity(
                "result-reference.absent"
            ),
        )
        changed = replace(run, result_productions=(production,))

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert result.reconstructed_marking is None
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.RESULT_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_mismatched_result_dependency(self) -> None:
        """Reject a dependency whose producer run differs from result provenance.

        Evidence ID: SV-WFR-REPLAY-010

        Requirement: Result dependencies preserve exact producer and consumer run
        identities independently of Workflow membership.

        Acceptance: A dependency naming another producer run returns ``error`` with
        a dependency-correlation issue and no reconstructed marking.
        """
        run, bundle = self.make_run_and_bundle()
        dependency = ResultDependency(
            identity=ResultDependencyIdentity("dependency.one"),
            result_reference_identity=run.result_references[0].identity,
            producer_workflow_run_identity=WorkflowRunIdentity("run.other"),
            consumer_workflow_run_identity=run.identity,
            consumer_task_instance_identity=run.task_instances[0].identity,
            consumer_activation_identity=None,
            input_name="upstream",
        )
        changed = replace(run, result_dependencies=(dependency,))

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert result.reconstructed_marking is None
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.DEPENDENCY_CORRELATION_ERROR,
        )

    def test_method__execute__replays_pending_dispatch_control_state(self) -> None:
        """Retain correlated authority and pending dispatch state without an effect.

        Evidence ID: SV-WFR-REPLAY-015

        Requirement: One request atomically correlates externally supplied authority,
        reservation, and an obligation while producing no successful firing.

        Acceptance: A correlation-valid pending dispatch revision replays ``equal`` at
        its unchanged initial marking.
        """
        run, bundle = self.make_run_and_bundle()
        authority = ScientificExecutionAuthorityReference(
            grant_identity=ExecutionGrantIdentity("grant.one"),
            grant_revision_identity=ExecutionGrantRevisionIdentity(
                "grant-revision.one"
            ),
            snapshot_identity=ScientificExecutionAuthoritySnapshotIdentity(
                "authority-snapshot.one"
            ),
            state_identity=ScientificExecutionAuthorityStateIdentity(
                "authority-state.unused"
            ),
        )
        request_identity = SimulationExecutionRequestIdentity("request.one")
        obligation_identity = ObligationIdentity("obligation.one")
        authorization_identity = SimulationExecutionAuthorizationResultIdentity(
            "authorization.one"
        )
        executor_identity = ScientificExecutorIdentity("executor.one")
        started_attempt = run.attempts[0]
        request = SimulationExecutionRequestCorrelation(
            identity=SimulationExecutionRequestCorrelationIdentity("correlation.one"),
            workflow_run_identity=run.identity,
            task_instance_identity=run.task_instances[0].identity,
            activation_identity=run.activations[0].identity,
            operation_identity=run.activations[0].operation_identity,
            attempt_identity=run.activations[0].attempt_identity,
            attempt_record_identity=started_attempt.identity,
            request_identity=request_identity,
            executor_identity=executor_identity,
            obligation_identity=obligation_identity,
            grant_identity=authority.grant_identity,
            authorization_result_identity=authorization_identity,
            input_result_reference_identities=(),
        )
        obligation = SimulationDispatchObligation(
            identity=obligation_identity,
            workflow_run_identity=run.identity,
            workflow_run_revision_identity=run.revision_identity,
            request_identity=request_identity,
            task_instance_identity=request.task_instance_identity,
            activation_identity=request.activation_identity,
            operation_identity=request.operation_identity,
            attempt_identity=request.attempt_identity,
            executor_identity=executor_identity,
            grant_identity=authority.grant_identity,
            destination_identity=DispatchDestinationIdentity("destination.one"),
            resource_scope_identities=(DispatchResourceScopeIdentity("resource.cpu"),),
            creation_idempotency_identity=DispatchCreationIdempotencyIdentity(
                "dispatch-create.one"
            ),
        )
        reservation = AuthorityReservationOutcome(
            identity=AuthorityReservationOutcomeIdentity("reservation.one"),
            workflow_run_identity=run.identity,
            workflow_run_revision_identity=run.revision_identity,
            authority_reference=authority,
            authorization_result_identity=authorization_identity,
            request_identity=request_identity,
            activation_identity=request.activation_identity,
            operation_identity=request.operation_identity,
            attempt_identity=request.attempt_identity,
            attempt_record_identity=started_attempt.identity,
            obligation_identity=obligation_identity,
            expected_revision_identity=run.revision_identity,
            kind=AuthorityReservationOutcomeKind.RESERVED,
        )
        pending = replace(
            run,
            attempts=(started_attempt,),
            outcomes=(),
            result_references=(),
            result_productions=(),
            authority_references=(authority,),
            execution_request_correlations=(request,),
            authority_reservations=(reservation,),
            dispatch_obligations=(obligation,),
            current_marking=run.initial_marking,
            transitions=(),
        )

        result = SUT().execute(pending, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.EQUAL
        assert result.reconstructed_marking == run.initial_marking

    def test_method__execute__rejects_request_input_not_bound_to_activation(
        self,
    ) -> None:
        """Reject a dispatch request naming an input absent from its activation.

        Evidence ID: SV-WFR-REPLAY-030

        Requirement: Execution-request input references equal the ResultObjects already
        bound to the exact retained activation.

        Acceptance: Adding an unrelated retained external result only to the request
        returns a control-state correlation error.
        """
        pending, bundle = self.make_pending_dispatch_run()
        external_reference = self.make_external_reference("request-input")
        request = replace(
            pending.execution_request_correlations[0],
            input_result_reference_identities=(external_reference.identity,),
        )
        changed = replace(
            pending,
            result_references=(external_reference,),
            execution_request_correlations=(request,),
        )

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_unclosed_task_producer_from_dispatch(
        self,
    ) -> None:
        """Reject dispatch presence as a substitute for represented Task closure.

        Evidence ID: SV-WFR-REPLAY-031

        Requirement: A represented-Task producer always closes over its actual
        outcome and production; a confirmed specialized dispatch cannot bypass them.

        Acceptance: A claimed/confirmed dispatch with fabricated absent Task outcome
        and production identities returns a result correlation error.
        """
        pending, bundle = self.make_pending_dispatch_run()
        request = pending.execution_request_correlations[0]
        reserved = pending.authority_reservations[0]
        claimed = replace(
            reserved,
            identity=AuthorityReservationOutcomeIdentity("reservation.two"),
            kind=AuthorityReservationOutcomeKind.CLAIMED,
            predecessor_reservation_identity=reserved.identity,
        )
        reference = ResultObjectReference(
            identity=ResultObjectReferenceIdentity("result-reference.dispatch"),
            result=_SyntheticResult(ResultObjectIdentity("result.dispatch")),
            concrete_type_identity=ResultObjectTypeIdentity("synthetic-result.v1"),
            owning_domain_identity=ResultObjectDomainIdentity("test.dispatch"),
            content_identity=ResultObjectContentIdentity("content.dispatch"),
            producer_provenance=RepresentedTaskResultProducer(
                identity=ResultProducerProvenanceIdentity("producer.dispatch"),
                workflow_identity=pending.workflow_identity,
                workflow_run_identity=pending.identity,
                task_instance_identity=request.task_instance_identity,
                activation_identity=request.activation_identity,
                operation_identity=request.operation_identity,
                attempt_identity=request.attempt_identity,
                terminal_attempt_record_identity=TaskAttemptRecordIdentity(
                    "attempt.dispatch.absent"
                ),
                outcome_identity=TaskInvocationOutcomeIdentity(
                    "outcome.dispatch.absent"
                ),
                production_identity=ResultProductionRecordIdentity(
                    "production.dispatch.absent"
                ),
            ),
        )
        dispatch = DispatchOutcomeRecord(
            identity=DispatchOutcomeRecordIdentity("dispatch-outcome.one"),
            envelope_identity=SimulationDispatchOutcomeIdentity("envelope.one"),
            workflow_run_identity=pending.identity,
            request_identity=request.request_identity,
            task_instance_identity=request.task_instance_identity,
            activation_identity=request.activation_identity,
            operation_identity=request.operation_identity,
            attempt_identity=request.attempt_identity,
            executor_identity=request.executor_identity,
            obligation_identity=request.obligation_identity,
            grant_identity=request.grant_identity,
            kind=DispatchOutcomeKind.CONFIRMED,
            result_reference_identity=reference.identity,
        )
        changed = replace(
            pending,
            authority_reservations=(reserved, claimed),
            dispatch_outcomes=(dispatch,),
            result_references=(reference,),
        )

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.RESULT_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_dispatch_failure_without_terminal_attempt(
        self,
    ) -> None:
        """Reject a dispatch failure naming no retained rejected attempt state.

        Evidence ID: SV-WFR-REPLAY-032

        Requirement: Rejected dispatch failure correlation closes over the exact
        retained rejected terminal attempt and contains no child-run correlation.

        Acceptance: A request-bound failure naming an absent terminal record returns a
        control-state correlation error.
        """
        pending, bundle = self.make_pending_dispatch_run()
        request = pending.execution_request_correlations[0]
        reserved = pending.authority_reservations[0]
        claimed = replace(
            reserved,
            identity=AuthorityReservationOutcomeIdentity("reservation.two"),
            kind=AuthorityReservationOutcomeKind.CLAIMED,
            predecessor_reservation_identity=reserved.identity,
        )
        failure = TaskFailureRecord(
            identity=TaskFailureRecordIdentity("failure-record.dispatch"),
            workflow_run_identity=pending.identity,
            task_instance_identity=request.task_instance_identity,
            activation_identity=request.activation_identity,
            operation_identity=request.operation_identity,
            attempt_identity=request.attempt_identity,
            terminal_attempt_record_identity=TaskAttemptRecordIdentity(
                "attempt.dispatch.absent"
            ),
            request_identity=request.request_identity,
            failure=TaskInvocationFailure(
                identity=TaskInvocationFailureIdentity("failure.dispatch"),
                code="synthetic.dispatch.rejected",
                operation_phase="dispatch",
                diagnostic="synthetic dispatch rejection",
                retryable=False,
                claim_boundary=("software verification only",),
            ),
        )
        dispatch = DispatchOutcomeRecord(
            identity=DispatchOutcomeRecordIdentity("dispatch-outcome.one"),
            envelope_identity=SimulationDispatchOutcomeIdentity("envelope.one"),
            workflow_run_identity=pending.identity,
            request_identity=request.request_identity,
            task_instance_identity=request.task_instance_identity,
            activation_identity=request.activation_identity,
            operation_identity=request.operation_identity,
            attempt_identity=request.attempt_identity,
            executor_identity=request.executor_identity,
            obligation_identity=request.obligation_identity,
            grant_identity=request.grant_identity,
            kind=DispatchOutcomeKind.REJECTED,
            failure_record_identity=failure.identity,
        )
        changed = replace(
            pending,
            authority_reservations=(reserved, claimed),
            dispatch_outcomes=(dispatch,),
            failures=(failure,),
        )

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
        )

    def test_method__execute__replays_no_task_decision_origin(self) -> None:
        """Replay a closed scientific-decision origin without Task lineage.

        Evidence ID: SV-WFR-REPLAY-014

        Requirement: A scientific-decision-origin record closes over request,
        resolution, direct source/authority identities, and no Task invocation fields,
        then participates in the same canonical pure firing replay.

        Acceptance: The correlation-valid aggregate returns ``equal`` without
        fabricating Task lineage.
        """
        run, bundle = self.make_decision_origin_run()

        result = SUT().execute(run, bundle)

        transition = run.transitions[0]
        assert type(transition) is ScientificDecisionWorkflowTransitionRecord
        assert not hasattr(transition, "activation_identity")
        assert result.outcome is WorkflowRunReplayOutcomeKind.EQUAL
        assert result.reconstructed_marking == run.current_marking
        assert result.issues == ()

    def test_method__execute__accepts_evidence_closed_external_result_reference(
        self,
    ) -> None:
        """Replay retained external input without fabricated Workflow production.

        Evidence ID: SV-WFR-REPLAY-017

        Requirement: A genuine non-Workflow result may be retained without local Task
        production only when its closed producer variant carries actual evidence and
        explicit limitations.

        Acceptance: A transition-free run containing that reference replays ``equal``
        without introducing Workflow producer identities.
        """
        run, bundle = self.make_run_and_bundle()
        external_reference = ResultObjectReference(
            identity=ResultObjectReferenceIdentity("reference.external"),
            result=_SyntheticResult(ResultObjectIdentity("result.external")),
            concrete_type_identity=ResultObjectTypeIdentity("synthetic-result.v1"),
            owning_domain_identity=ResultObjectDomainIdentity("test.external"),
            content_identity=ResultObjectContentIdentity("content.external"),
            producer_provenance=ExternalResultProducer(
                identity=ResultProducerProvenanceIdentity("producer.external"),
                external_producer_identity=ExternalResultProducerIdentity(
                    "external-producer.one"
                ),
                producer_attempt_identity=ExternalProducerAttemptIdentity(
                    "external-attempt.one"
                ),
                evidence_identities=(
                    ResultProducerEvidenceIdentity("evidence.external.one"),
                ),
                limitations=("synthetic software-verification provenance only",),
            ),
        )
        changed = replace(
            run,
            activations=(),
            attempts=(),
            outcomes=(),
            result_references=(external_reference,),
            result_productions=(),
            current_marking=run.initial_marking,
            transitions=(),
        )

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.EQUAL
        assert result.reconstructed_marking == run.initial_marking

    def test_method__execute__replays_task_and_decision_origins_in_one_history(
        self,
    ) -> None:
        """Replay task and decision origins through one canonical marking sequence.

        Evidence ID: SV-WFR-REPLAY-016

        Requirement: Task and scientific-decision transitions participate in one
        contiguous ordered history and share the same generic replay semantics.

        Acceptance: A hand-built two-step mixed-origin history returns ``equal`` at
        the exact retained final marking.
        """
        run, bundle = self.make_both_origin_run()

        result = SUT().execute(run, bundle)

        assert tuple(type(transition) for transition in run.transitions) == (
            TaskWorkflowTransitionRecord,
            ScientificDecisionWorkflowTransitionRecord,
        )
        assert result.outcome is WorkflowRunReplayOutcomeKind.EQUAL
        assert result.reconstructed_marking == run.current_marking

    def test_method__execute__rejects_noncanonical_mixed_origin_sequence(
        self,
    ) -> None:
        """Reject mixed-origin records that are not stored in canonical order.

        Evidence ID: SV-WFR-REPLAY-018

        Requirement: One global zero-based sequence orders every transition origin.

        Acceptance: Reversing a valid mixed-origin tuple returns the explicit
        non-canonical-history error before firing replay.
        """
        run, bundle = self.make_both_origin_run()
        changed = replace(run, transitions=tuple(reversed(run.transitions)))

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.NONCANONICAL_TRANSITION_ORDER,
        )

    def test_method__execute__rejects_decision_transition_mismatch(self) -> None:
        """Reject a decision whose request names another CPN transition.

        Evidence ID: SV-WFR-REPLAY-019

        Requirement: Request, resolution, producer, and firing close over the same
        affected transition and exact identities.

        Acceptance: Changing only the requested CPN transition returns a scientific
        decision correlation error.
        """
        run, bundle = self.make_decision_origin_run()
        changed_request = replace(
            run.scientific_decision_requests[0],
            affected_transition_identity=ColoredPetriNetTransitionIdentity("other"),
        )
        changed = replace(run, scientific_decision_requests=(changed_request,))

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.SCIENTIFIC_DECISION_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_decision_output_binding_mismatch(self) -> None:
        """Reject a decision firing that does not bind the selected option value.

        Evidence ID: SV-WFR-REPLAY-020

        Requirement: The scientific-decision resolution and generic output binding
        represent one exact normalized option.

        Acceptance: A self-consistent firing for another output value returns a
        scientific-decision correlation error rather than replay equality.
        """
        run, bundle = self.make_decision_origin_run()
        transition = run.transitions[0]
        assert type(transition) is ScientificDecisionWorkflowTransitionRecord
        wrong_binding = ColoredPetriNetBinding(
            ColoredPetriNetTransitionIdentity("execute"),
            (
                ColoredPetriNetBindingAssignment(
                    ColoredPetriNetBindingVariableIdentity("output"),
                    ColoredPetriNetValue(ColoredPetriNetValueKind.STRING, "B"),
                ),
            ),
        )
        wrong_firing = ColoredPetriNetTransitionFirer().execute(
            replace(
                transition.firing_result.firing_input,
                external_output_binding=wrong_binding,
            )
        )
        assert wrong_firing.outcome is ColoredPetriNetFiringOutcomeKind.SUCCESS
        assert wrong_firing.successor_marking is not None
        changed = replace(
            run,
            current_marking=wrong_firing.successor_marking,
            transitions=(replace(transition, firing_result=wrong_firing),),
        )

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.SCIENTIFIC_DECISION_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_activation_without_initial_attempt(self) -> None:
        """Reject a retained activation with no append-only attempt history.

        Evidence ID: SV-WFR-REPLAY-021

        Requirement: Every retained TaskActivation owns exactly one initial started
        attempt-state record.

        Acceptance: Removing all attempt and downstream records while retaining the
        activation returns an attempt correlation error.
        """
        run, bundle = self.make_run_and_bundle()
        changed = replace(
            run,
            attempts=(),
            outcomes=(),
            result_references=(),
            result_productions=(),
            current_marking=run.initial_marking,
            transitions=(),
        )

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.ATTEMPT_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_unretained_activation_input(self) -> None:
        """Reject an activation input with no result-reference/dependency closure.

        Evidence ID: SV-WFR-REPLAY-022

        Requirement: Every bound activation input has one exact aggregate result
        reference and activation-scoped dependency edge.

        Acceptance: Adding only the input binding returns a dependency correlation
        error.
        """
        run, bundle = self.make_run_and_bundle()
        unretained = _SyntheticResult(ResultObjectIdentity("result.unretained"))
        activation = replace(
            run.activations[0],
            inputs=(TaskInputBinding("input", unretained),),
        )
        changed = replace(run, activations=(activation,))

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.DEPENDENCY_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_matching_but_unsupported_versions(self) -> None:
        """Reject mutually matching version numbers not implemented by replay.

        Evidence ID: SV-WFR-REPLAY-023

        Requirement: Runtime compatibility establishes supported versions, not merely
        equality between run and bundle fields.

        Acceptance: Matching schema version 2, Workflow-definition version 2, and
        adapter version 2 each return ``unsupported_version`` with their issue family.
        """
        run, bundle = self.make_run_and_bundle()
        schema_reference = replace(bundle.definition_reference, schema_version=2)
        schema_bundle = replace(
            bundle,
            definition_reference=schema_reference,
            schema_version=2,
        )
        schema_result = SUT().execute(replace(run, schema_version=2), schema_bundle)
        definition_bundle = replace(
            bundle,
            definition_reference=replace(
                bundle.definition_reference, workflow_definition_version=2
            ),
        )
        definition_result = SUT().execute(run, definition_bundle)
        adapter_result = SUT().execute(
            replace(run, adapter_implementation_identity="workflow-cpn-adapter-v2"),
            replace(
                bundle,
                adapter_implementation_identity="workflow-cpn-adapter-v2",
            ),
        )

        assert schema_result.outcome is WorkflowRunReplayOutcomeKind.UNSUPPORTED_VERSION
        assert tuple(issue.code for issue in schema_result.issues) == (
            WorkflowRunReplayIssueCode.SCHEMA_VERSION_MISMATCH,
        )
        assert (
            definition_result.outcome
            is WorkflowRunReplayOutcomeKind.UNSUPPORTED_VERSION
        )
        assert tuple(issue.code for issue in definition_result.issues) == (
            WorkflowRunReplayIssueCode.DEFINITION_IDENTITY_MISMATCH,
        )
        assert (
            adapter_result.outcome is WorkflowRunReplayOutcomeKind.UNSUPPORTED_VERSION
        )
        assert tuple(issue.code for issue in adapter_result.issues) == (
            WorkflowRunReplayIssueCode.IMPLEMENTATION_IDENTITY_MISMATCH,
        )

    def test_method__execute__rejects_branching_decision_corrections(self) -> None:
        """Reject two corrections that both name one stale predecessor.

        Evidence ID: SV-WFR-REPLAY-024

        Requirement: Each correction consumes the latest effective same-request
        resolution; concurrent or stale predecessors never branch decision history.

        Acceptance: A three-record history whose third resolution names the initial
        predecessor returns a scientific-decision correlation error.
        """
        run, bundle = self.make_decision_origin_run()
        initial_resolution = run.scientific_decision_resolutions[0]
        initial_transition = run.transitions[0]
        assert type(initial_transition) is ScientificDecisionWorkflowTransitionRecord
        corrections: list[
            tuple[
                ScientificDecisionResolution,
                ResultObjectReference,
                ScientificDecisionWorkflowTransitionRecord,
            ]
        ] = []
        for index, suffix in enumerate(("two", "three"), start=1):
            resolution_identity = ResultObjectIdentity(f"decision-resolution.{suffix}")
            transition_identity = ScientificDecisionTransitionRecordIdentity(
                f"decision-transition.{suffix}"
            )
            producer = replace(
                initial_resolution.producer_provenance,
                identity=ResultProducerProvenanceIdentity(
                    f"decision-producer.{suffix}"
                ),
                transition_record_identity=transition_identity,
                resolution_identity=resolution_identity,
            )
            resolution = replace(
                initial_resolution,
                identity=resolution_identity,
                content_identity=ResultObjectContentIdentity(
                    f"decision-content.{suffix}"
                ),
                predecessor_resolution_identity=initial_resolution.identity,
                supersedes_resolution_identity=initial_resolution.identity,
                producer_provenance=producer,
            )
            reference = replace(
                run.result_references[0],
                identity=ResultObjectReferenceIdentity(f"decision-reference.{suffix}"),
                result=resolution,
                content_identity=resolution.content_identity,
                producer_provenance=producer,
            )
            transition = replace(
                initial_transition,
                identity=transition_identity,
                sequence_identity=WorkflowTransitionSequenceIdentity(
                    f"sequence.{suffix}"
                ),
                sequence_index=index,
                resolution_identity=resolution.identity,
                producer_provenance_identity=producer.identity,
            )
            corrections.append((resolution, reference, transition))
        changed = replace(
            run,
            result_references=tuple(
                sorted(
                    run.result_references
                    + tuple(reference for _, reference, _ in corrections),
                    key=lambda value: value.identity.value,
                )
            ),
            scientific_decision_resolutions=tuple(
                sorted(
                    run.scientific_decision_resolutions
                    + tuple(resolution for resolution, _, _ in corrections),
                    key=lambda value: value.identity.value,
                )
            ),
            transitions=run.transitions
            + tuple(transition for _, _, transition in corrections),
        )

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.SCIENTIFIC_DECISION_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_missing_task_membership(self) -> None:
        """Reject a run-scoped Task instance with no ordinary membership record.

        Evidence ID: SV-WFR-REPLAY-013

        Requirement: Every run-scoped Task instance has exactly one explicit ordinary
        Workflow membership independent of activation or result dependency.

        Acceptance: Removing that membership returns ``error`` with the membership
        correlation issue and no reconstructed marking.
        """
        run, bundle = self.make_run_and_bundle()
        changed = replace(run, task_memberships=())

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert result.reconstructed_marking is None
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.MEMBERSHIP_CORRELATION_ERROR,
        )

    def test_method__execute__replays_confirmed_nested_export_correlation(self) -> None:
        """Replay a parent while retaining a distinct terminal child reference.

        Evidence ID: SV-WFR-REPLAY-011

        Requirement: Parent and child histories remain separate, while a confirmed
        nested outcome names a replay-equal terminal child revision and admits each
        explicit child export through one parent dependency.

        Acceptance: The parent replay returns ``equal`` without embedding or replaying
        a child marking or transition history.
        """
        run, bundle = self.make_confirmed_nested_run()

        result = SUT().execute(run, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.EQUAL
        assert result.reconstructed_marking == run.current_marking
        assert run.nested_invocations[0].child_workflow_run_identity != run.identity

    def test_method__execute__rejects_missing_nested_export_admission(self) -> None:
        """Reject a child export whose declared parent admission is absent.

        Evidence ID: SV-WFR-REPLAY-012

        Requirement: Membership alone never admits a child ResultObject; every
        confirmed export requires its exact ResultDependency in the parent aggregate.

        Acceptance: Removing the admission dependency returns ``error`` with the
        nested-export correlation issue and no reconstructed marking.
        """
        run, bundle = self.make_confirmed_nested_run()
        changed = replace(run, result_dependencies=())

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert result.reconstructed_marking is None
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.NESTED_WORKFLOW_EXPORT_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_nested_revision_mismatch(self) -> None:
        """Reject inconsistent parent revision references for one child invocation.

        Evidence ID: SV-WFR-REPLAY-025

        Requirement: Nested membership and invocation records close over one exact
        parent revision while child history remains separate.

        Acceptance: Changing only the invocation parent revision returns a nested
        Workflow correlation error.
        """
        run, bundle = self.make_confirmed_nested_run()
        invocation = replace(
            run.nested_invocations[0],
            parent_revision_identity=WorkflowRunRevisionIdentity("revision.other"),
        )
        changed = replace(run, nested_invocations=(invocation,))

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.NESTED_WORKFLOW_CORRELATION_ERROR,
        )

    def test_method__execute__rejects_control_revision_mismatch(self) -> None:
        """Reject inconsistent reservation and obligation revision references.

        Evidence ID: SV-WFR-REPLAY-026

        Requirement: One authority reservation closes over the exact WorkflowRun
        revision retained by its dispatch obligation and expected-revision input.

        Acceptance: Changing only the obligation revision returns a control-state
        correlation error.
        """
        run, bundle = self.make_run_and_bundle()
        started_attempt = run.attempts[0]
        activation = run.activations[0]
        authority = ScientificExecutionAuthorityReference(
            grant_identity=ExecutionGrantIdentity("grant.one"),
            grant_revision_identity=ExecutionGrantRevisionIdentity(
                "grant.revision.one"
            ),
            snapshot_identity=ScientificExecutionAuthoritySnapshotIdentity(
                "authority.snapshot.one"
            ),
            state_identity=ScientificExecutionAuthorityStateIdentity(
                "authority.state.one"
            ),
        )
        request = SimulationExecutionRequestCorrelation(
            identity=SimulationExecutionRequestCorrelationIdentity(
                "request-correlation.one"
            ),
            workflow_run_identity=run.identity,
            task_instance_identity=run.task_instances[0].identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            attempt_record_identity=started_attempt.identity,
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            obligation_identity=ObligationIdentity("obligation.one"),
            grant_identity=authority.grant_identity,
            authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity("authorization.one")
            ),
            input_result_reference_identities=(),
        )
        reservation = AuthorityReservationOutcome(
            identity=AuthorityReservationOutcomeIdentity("reservation.one"),
            workflow_run_identity=run.identity,
            workflow_run_revision_identity=run.revision_identity,
            authority_reference=authority,
            authorization_result_identity=request.authorization_result_identity,
            request_identity=request.request_identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            attempt_record_identity=started_attempt.identity,
            obligation_identity=request.obligation_identity,
            expected_revision_identity=run.revision_identity,
            kind=AuthorityReservationOutcomeKind.RESERVED,
        )
        obligation = SimulationDispatchObligation(
            identity=request.obligation_identity,
            workflow_run_identity=run.identity,
            workflow_run_revision_identity=WorkflowRunRevisionIdentity(
                "revision.other"
            ),
            request_identity=request.request_identity,
            task_instance_identity=run.task_instances[0].identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            executor_identity=request.executor_identity,
            grant_identity=authority.grant_identity,
            destination_identity=DispatchDestinationIdentity("destination.one"),
            resource_scope_identities=(DispatchResourceScopeIdentity("resource.one"),),
            creation_idempotency_identity=DispatchCreationIdempotencyIdentity(
                "dispatch.one"
            ),
        )
        changed = replace(
            run,
            authority_references=(authority,),
            execution_request_correlations=(request,),
            authority_reservations=(reservation,),
            dispatch_obligations=(obligation,),
            current_marking=run.initial_marking,
            transitions=(),
        )

        result = SUT().execute(changed, bundle)

        assert result.outcome is WorkflowRunReplayOutcomeKind.ERROR
        assert tuple(issue.code for issue in result.issues) == (
            WorkflowRunReplayIssueCode.CONTROL_STATE_CORRELATION_ERROR,
        )

    @staticmethod
    def make_external_reference(label: str) -> ResultObjectReference:
        """Construct one evidence-closed synthetic external ResultObject reference."""
        return ResultObjectReference(
            identity=ResultObjectReferenceIdentity(f"reference.external.{label}"),
            result=_SyntheticResult(ResultObjectIdentity(f"result.external.{label}")),
            concrete_type_identity=ResultObjectTypeIdentity("synthetic-result.v1"),
            owning_domain_identity=ResultObjectDomainIdentity("test.external"),
            content_identity=ResultObjectContentIdentity(f"content.external.{label}"),
            producer_provenance=ExternalResultProducer(
                identity=ResultProducerProvenanceIdentity(f"producer.external.{label}"),
                external_producer_identity=ExternalResultProducerIdentity(
                    "external-producer.one"
                ),
                producer_attempt_identity=ExternalProducerAttemptIdentity(
                    f"external-attempt.{label}"
                ),
                evidence_identities=(
                    ResultProducerEvidenceIdentity(f"evidence.external.{label}"),
                ),
                limitations=("synthetic software-verification provenance only",),
            ),
        )

    @classmethod
    def make_pending_dispatch_run(
        cls,
    ) -> tuple[WorkflowRun, WorkflowRuntimeBundle]:
        """Construct one exact reserved, not-yet-dispatched aggregate."""
        run, bundle = cls.make_run_and_bundle()
        authority = ScientificExecutionAuthorityReference(
            grant_identity=ExecutionGrantIdentity("grant.one"),
            grant_revision_identity=ExecutionGrantRevisionIdentity(
                "grant-revision.one"
            ),
            snapshot_identity=ScientificExecutionAuthoritySnapshotIdentity(
                "authority-snapshot.one"
            ),
            state_identity=ScientificExecutionAuthorityStateIdentity(
                "authority-state.unused"
            ),
        )
        request_identity = SimulationExecutionRequestIdentity("request.one")
        obligation_identity = ObligationIdentity("obligation.one")
        authorization_identity = SimulationExecutionAuthorizationResultIdentity(
            "authorization.one"
        )
        executor_identity = ScientificExecutorIdentity("executor.one")
        started_attempt = run.attempts[0]
        request = SimulationExecutionRequestCorrelation(
            identity=SimulationExecutionRequestCorrelationIdentity("correlation.one"),
            workflow_run_identity=run.identity,
            task_instance_identity=run.task_instances[0].identity,
            activation_identity=run.activations[0].identity,
            operation_identity=run.activations[0].operation_identity,
            attempt_identity=run.activations[0].attempt_identity,
            attempt_record_identity=started_attempt.identity,
            request_identity=request_identity,
            executor_identity=executor_identity,
            obligation_identity=obligation_identity,
            grant_identity=authority.grant_identity,
            authorization_result_identity=authorization_identity,
            input_result_reference_identities=(),
        )
        obligation = SimulationDispatchObligation(
            identity=obligation_identity,
            workflow_run_identity=run.identity,
            workflow_run_revision_identity=run.revision_identity,
            request_identity=request_identity,
            task_instance_identity=request.task_instance_identity,
            activation_identity=request.activation_identity,
            operation_identity=request.operation_identity,
            attempt_identity=request.attempt_identity,
            executor_identity=executor_identity,
            grant_identity=authority.grant_identity,
            destination_identity=DispatchDestinationIdentity("destination.one"),
            resource_scope_identities=(DispatchResourceScopeIdentity("resource.cpu"),),
            creation_idempotency_identity=DispatchCreationIdempotencyIdentity(
                "dispatch-create.one"
            ),
        )
        reservation = AuthorityReservationOutcome(
            identity=AuthorityReservationOutcomeIdentity("reservation.one"),
            workflow_run_identity=run.identity,
            workflow_run_revision_identity=run.revision_identity,
            authority_reference=authority,
            authorization_result_identity=authorization_identity,
            request_identity=request_identity,
            activation_identity=request.activation_identity,
            operation_identity=request.operation_identity,
            attempt_identity=request.attempt_identity,
            attempt_record_identity=started_attempt.identity,
            obligation_identity=obligation_identity,
            expected_revision_identity=run.revision_identity,
            kind=AuthorityReservationOutcomeKind.RESERVED,
        )
        return (
            replace(
                run,
                attempts=(started_attempt,),
                outcomes=(),
                result_references=(),
                result_productions=(),
                authority_references=(authority,),
                execution_request_correlations=(request,),
                authority_reservations=(reservation,),
                dispatch_obligations=(obligation,),
                current_marking=run.initial_marking,
                transitions=(),
            ),
            bundle,
        )

    @classmethod
    def make_decision_origin_run(
        cls,
    ) -> tuple[WorkflowRun, WorkflowRuntimeBundle]:
        """Construct one correlation-valid no-Task decision-origin aggregate."""
        run, bundle = cls.make_run_and_bundle()
        firing = run.transitions[0].firing_result
        request_identity = ScientificDecisionRequestIdentity("decision-request.one")
        source_identity = ResponseSourceIdentity("response-source.one")
        authority_identity = AuthorityContextIdentity("authority-context.one")
        option = ScientificDecisionOption(
            ScientificDecisionOptionIdentity("option.a"), "A"
        )
        request = ScientificDecisionRequest(
            identity=request_identity,
            question="Select the represented synthetic branch.",
            options=(option,),
            declared_scope="synthetic software-verification branch",
            workflow_identity=run.workflow_identity,
            workflow_run_identity=run.identity,
            affected_task_instance_identity=run.task_instances[0].identity,
            affected_transition_identity=firing.firing_input.transition_identity,
            required_response_source_identity=source_identity,
            required_authority_context_identity=authority_identity,
            definition_identity="scientific-decision-request.v1",
            definition_version=1,
        )
        resolution_identity = ResultObjectIdentity("decision-resolution.one")
        transition_identity = ScientificDecisionTransitionRecordIdentity(
            "decision-transition.one"
        )
        producer = RepresentedScientificDecisionIngressProducer(
            identity=ResultProducerProvenanceIdentity("decision-producer.one"),
            workflow_identity=run.workflow_identity,
            workflow_run_identity=run.identity,
            request_identity=request_identity,
            transition_record_identity=transition_identity,
            recorder_identity=ScientificDecisionRecorderIdentity("recorder.v1"),
            response_source_identity=source_identity,
            authority_context_identity=authority_identity,
            resolution_identity=resolution_identity,
        )
        resolution = ScientificDecisionResolution(
            identity=resolution_identity,
            content_identity=ResultObjectContentIdentity("decision-content.one"),
            request_identity=request_identity,
            verbatim_response="A",
            normalized_option_identity=option.identity,
            response_source_identity=source_identity,
            authority_context_identity=authority_identity,
            boundary_receipt_identity=None,
            predecessor_resolution_identity=None,
            supersedes_resolution_identity=None,
            producer_provenance=producer,
        )
        reference = ResultObjectReference(
            identity=ResultObjectReferenceIdentity("decision-reference.one"),
            result=resolution,
            concrete_type_identity=ResultObjectTypeIdentity(
                "scientific-decision-resolution.v1"
            ),
            owning_domain_identity=ResultObjectDomainIdentity(
                "ksdft2effmass.workflows"
            ),
            content_identity=resolution.content_identity,
            producer_provenance=producer,
        )
        decision_external = ColoredPetriNetBinding(
            ColoredPetriNetTransitionIdentity("execute"),
            (
                ColoredPetriNetBindingAssignment(
                    ColoredPetriNetBindingVariableIdentity("output"),
                    ColoredPetriNetValue(ColoredPetriNetValueKind.STRING, option.value),
                ),
            ),
        )
        decision_firing = ColoredPetriNetTransitionFirer().execute(
            replace(
                firing.firing_input,
                external_output_binding=decision_external,
            )
        )
        assert decision_firing.outcome is ColoredPetriNetFiringOutcomeKind.SUCCESS
        assert decision_firing.successor_marking is not None
        transition = ScientificDecisionWorkflowTransitionRecord(
            identity=transition_identity,
            sequence_identity=WorkflowTransitionSequenceIdentity("sequence.zero"),
            sequence_index=0,
            workflow_identity=run.workflow_identity,
            workflow_run_identity=run.identity,
            definition_reference_identity=run.definition_reference_identity,
            runtime_bundle_identity=run.runtime_bundle_identity,
            request_identity=request.identity,
            resolution_identity=resolution.identity,
            producer_provenance_identity=producer.identity,
            firing_result=decision_firing,
        )
        return (
            replace(
                run,
                activations=(),
                attempts=(),
                outcomes=(),
                result_references=(reference,),
                result_productions=(),
                scientific_decision_requests=(request,),
                scientific_decision_resolutions=(resolution,),
                current_marking=decision_firing.successor_marking,
                transitions=(transition,),
            ),
            bundle,
        )

    @classmethod
    def make_both_origin_run(
        cls,
    ) -> tuple[WorkflowRun, WorkflowRuntimeBundle]:
        """Construct one two-step task-then-decision canonical replay history."""
        run, bundle = cls.make_run_and_bundle()
        definition = bundle.definition
        prepared = next(
            place
            for place in run.initial_marking.places
            if place.place_identity.value == "prepared"
        )
        second_input = ColoredPetriNetToken(
            definition.colors[0].identity,
            ColoredPetriNetValue(ColoredPetriNetValueKind.STRING, "input.two"),
            ColoredPetriNetTokenIdentity("input.token.two"),
        )
        initial = ColoredPetriNetMarking(
            ColoredPetriNetMarkingIdentity("marking.two-inputs"),
            definition.identity,
            tuple(
                replace(place, tokens=prepared.tokens + (second_input,))
                if place.place_identity == prepared.place_identity
                else place
                for place in run.initial_marking.places
            ),
        )
        first_enablement = ColoredPetriNetTransitionEnabler().execute(
            definition, initial
        )
        first_selection = ColoredPetriNetBindingSelector().execute(
            definition, first_enablement
        )
        assert first_selection.selected_binding is not None
        first_input = replace(
            run.transitions[0].firing_result.firing_input,
            predecessor_marking=initial,
            enablement_result=first_enablement,
            selection_result=first_selection,
            selected_binding=first_selection.selected_binding,
        )
        first_firing = ColoredPetriNetTransitionFirer().execute(first_input)
        assert first_firing.outcome is ColoredPetriNetFiringOutcomeKind.SUCCESS
        assert first_firing.successor_marking is not None
        activation = replace(
            run.activations[0],
            selection=DirectTaskActivationSelection(first_selection.identity),
        )
        task_transition = replace(run.transitions[0], firing_result=first_firing)

        second_enablement = ColoredPetriNetTransitionEnabler().execute(
            definition, first_firing.successor_marking
        )
        second_selection = ColoredPetriNetBindingSelector().execute(
            definition, second_enablement
        )
        assert second_selection.selected_binding is not None
        decision_external = ColoredPetriNetBinding(
            ColoredPetriNetTransitionIdentity("execute"),
            (
                ColoredPetriNetBindingAssignment(
                    ColoredPetriNetBindingVariableIdentity("output"),
                    ColoredPetriNetValue(ColoredPetriNetValueKind.STRING, "A"),
                ),
            ),
        )
        second_firing = ColoredPetriNetTransitionFirer().execute(
            ColoredPetriNetFiringInput(
                definition,
                ColoredPetriNetTransitionIdentity("execute"),
                first_firing.successor_marking,
                second_enablement,
                second_selection,
                second_selection.selected_binding,
                None,
                decision_external,
            )
        )
        assert second_firing.outcome is ColoredPetriNetFiringOutcomeKind.SUCCESS
        assert second_firing.successor_marking is not None

        request_identity = ScientificDecisionRequestIdentity("decision-request.two")
        source_identity = ResponseSourceIdentity("response-source.one")
        authority_identity = AuthorityContextIdentity("authority-context.one")
        option = ScientificDecisionOption(
            ScientificDecisionOptionIdentity("option.a"), "A"
        )
        request = ScientificDecisionRequest(
            identity=request_identity,
            question="Select the represented synthetic branch.",
            options=(option,),
            declared_scope="synthetic mixed-origin replay",
            workflow_identity=run.workflow_identity,
            workflow_run_identity=run.identity,
            affected_task_instance_identity=run.task_instances[0].identity,
            affected_transition_identity=ColoredPetriNetTransitionIdentity("execute"),
            required_response_source_identity=source_identity,
            required_authority_context_identity=authority_identity,
            definition_identity="scientific-decision-request.v1",
            definition_version=1,
        )
        resolution_identity = ResultObjectIdentity("decision-resolution.two")
        decision_transition_identity = ScientificDecisionTransitionRecordIdentity(
            "decision-transition.two"
        )
        producer = RepresentedScientificDecisionIngressProducer(
            identity=ResultProducerProvenanceIdentity("decision-producer.two"),
            workflow_identity=run.workflow_identity,
            workflow_run_identity=run.identity,
            request_identity=request.identity,
            transition_record_identity=decision_transition_identity,
            recorder_identity=ScientificDecisionRecorderIdentity("recorder.v1"),
            response_source_identity=source_identity,
            authority_context_identity=authority_identity,
            resolution_identity=resolution_identity,
        )
        resolution = ScientificDecisionResolution(
            identity=resolution_identity,
            content_identity=ResultObjectContentIdentity("decision-content.two"),
            request_identity=request.identity,
            verbatim_response="A",
            normalized_option_identity=option.identity,
            response_source_identity=source_identity,
            authority_context_identity=authority_identity,
            boundary_receipt_identity=None,
            predecessor_resolution_identity=None,
            supersedes_resolution_identity=None,
            producer_provenance=producer,
        )
        reference = ResultObjectReference(
            identity=ResultObjectReferenceIdentity("decision-reference.two"),
            result=resolution,
            concrete_type_identity=ResultObjectTypeIdentity(
                "scientific-decision-resolution.v1"
            ),
            owning_domain_identity=ResultObjectDomainIdentity(
                "ksdft2effmass.workflows"
            ),
            content_identity=resolution.content_identity,
            producer_provenance=producer,
        )
        decision_transition = ScientificDecisionWorkflowTransitionRecord(
            identity=decision_transition_identity,
            sequence_identity=WorkflowTransitionSequenceIdentity("sequence.one"),
            sequence_index=1,
            workflow_identity=run.workflow_identity,
            workflow_run_identity=run.identity,
            definition_reference_identity=run.definition_reference_identity,
            runtime_bundle_identity=run.runtime_bundle_identity,
            request_identity=request.identity,
            resolution_identity=resolution.identity,
            producer_provenance_identity=producer.identity,
            firing_result=second_firing,
        )
        return (
            replace(
                run,
                initial_marking=initial,
                current_marking=second_firing.successor_marking,
                activations=(activation,),
                result_references=tuple(
                    sorted(
                        run.result_references + (reference,),
                        key=lambda value: value.identity.value,
                    )
                ),
                scientific_decision_requests=(request,),
                scientific_decision_resolutions=(resolution,),
                transitions=(task_transition, decision_transition),
            ),
            bundle,
        )

    @classmethod
    def make_confirmed_nested_run(
        cls,
    ) -> tuple[WorkflowRun, WorkflowRuntimeBundle]:
        """Construct one parent run with an explicitly admitted child export."""
        run, bundle = cls.make_run_and_bundle()
        child_workflow_identity = WorkflowIdentity("workflow.child")
        child_run_identity = WorkflowRunIdentity("run.child")
        child_reference = replace(
            run.result_references[0],
            producer_provenance=RepresentedTaskResultProducer(
                identity=ResultProducerProvenanceIdentity("producer.child"),
                workflow_identity=child_workflow_identity,
                workflow_run_identity=child_run_identity,
                task_instance_identity=TaskInstanceIdentity("instance.child"),
                activation_identity=TaskActivationIdentity("activation.child"),
                operation_identity=OperationIdentity("operation.child"),
                attempt_identity=AttemptIdentity("attempt.child"),
                terminal_attempt_record_identity=TaskAttemptRecordIdentity(
                    "attempt.child.confirmed"
                ),
                outcome_identity=TaskInvocationOutcomeIdentity("outcome.child"),
                production_identity=ResultProductionRecordIdentity("production.child"),
            ),
        )
        started_attempt = replace(
            run.attempts[0], child_workflow_run_identity=child_run_identity
        )
        terminal_attempt = replace(
            run.attempts[1], child_workflow_run_identity=child_run_identity
        )
        outcome = replace(run.outcomes[0], results=(child_reference,))
        admission = ResultDependency(
            identity=ResultDependencyIdentity("dependency.child-admission"),
            result_reference_identity=child_reference.identity,
            producer_workflow_run_identity=child_run_identity,
            consumer_workflow_run_identity=run.identity,
            consumer_task_instance_identity=run.task_instances[0].identity,
            consumer_activation_identity=run.activations[0].identity,
            input_name="export.result.one",
        )
        membership = NestedWorkflowMembership(
            identity=NestedWorkflowMembershipIdentity("membership.child"),
            parent_workflow_run_identity=run.identity,
            parent_revision_identity=run.revision_identity,
            parent_task_instance_identity=run.task_instances[0].identity,
            child_workflow_identity=child_workflow_identity,
            child_workflow_run_identity=child_run_identity,
        )
        invocation = NestedWorkflowInvocation(
            identity=NestedWorkflowInvocationIdentity("invocation.child"),
            parent_workflow_run_identity=run.identity,
            parent_revision_identity=run.revision_identity,
            parent_task_instance_identity=run.task_instances[0].identity,
            activation_identity=run.activations[0].identity,
            operation_identity=run.activations[0].operation_identity,
            attempt_identity=run.activations[0].attempt_identity,
            attempt_record_identity=terminal_attempt.identity,
            child_workflow_identity=child_workflow_identity,
            child_workflow_run_identity=child_run_identity,
            input_result_reference_identities=(),
            child_creation_idempotency_identity=(
                ChildWorkflowCreationIdempotencyIdentity("child-create.one")
            ),
            kind=NestedWorkflowInvocationKind.CONFIRMED,
            terminal_observation_identity=NestedWorkflowObservationIdentity(
                "observation.child.terminal"
            ),
            terminal_child_revision_identity=WorkflowRunRevisionIdentity(
                "revision.child.terminal"
            ),
            replay_equal_child_result_identity=WorkflowRunReplayResultIdentity(
                "b" * 64
            ),
            exported_result_reference_identities=(child_reference.identity,),
            export_admission_dependency_identities=(admission.identity,),
        )
        return (
            replace(
                run,
                nested_memberships=(membership,),
                nested_invocations=(invocation,),
                attempts=(started_attempt, terminal_attempt),
                outcomes=(outcome,),
                result_references=(child_reference,),
                result_dependencies=(admission,),
            ),
            bundle,
        )
