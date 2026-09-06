r"""Software verification of ``SimulationDispatchPreparer``.

Evidence profile: routine

Bounded artifact scope: the effect-free pending-dispatch candidate ActionObject.

Facet and represented meaning

The preparer requires an exactly replayable predecessor, evaluates preparation-phase
authority, and returns one replay-equal candidate containing the complete pending-work
record group.

Intrinsic and cross-object scope

The public ActionObject is the sole system under test.  The oracle is one empty generic
CPN marking and explicit runtime bundle, for which exact replay is hand-inspectable.

VVUQ and scientific exclusions

This is software verification only.  It performs no persistence, external calculation,
scientific validation, uncertainty quantification, authority issuance, or human
acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBindingSelectorIdentity,
    ColoredPetriNetDefinition,
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetExpressionEvaluatorIdentity,
    ColoredPetriNetMarking,
    ColoredPetriNetMarkingIdentity,
    ColoredPetriNetOrderingPolicyIdentity,
    ColoredPetriNetSelectionResultIdentity,
    ColoredPetriNetTransitionEnablerIdentity,
    ColoredPetriNetTransitionFirerIdentity,
)
from ksdft2effmass.workflows import (
    AttemptIdentity,
    DirectTaskActivationSelection,
    OperationIdentity,
    TaskActivation,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstance,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.control import (
    ScientificExecutionGrantState,
    SimulationDispatchPreparationOutcomeKind,
    SimulationDispatchPreparationRequest,
    SimulationDispatchPreparer,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizer,
)
from ksdft2effmass.workflows.runs import (
    AuthorityReservationOutcomeIdentity,
    DispatchCreationIdempotencyIdentity,
    SimulationExecutionRequestCorrelationIdentity,
    TaskAttemptRecordIdentity,
    TaskWorkflowMembership,
    TaskWorkflowMembershipIdentity,
    WorkflowDefinitionReference,
    WorkflowDefinitionReferenceIdentity,
    WorkflowRun,
    WorkflowRunReplayer,
    WorkflowRunRevisionIdentity,
    WorkflowRuntimeBundle,
    WorkflowRuntimeBundleIdentity,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchPreparer


class TestSimulationDispatchPreparer:
    """Own software evidence for effect-free dispatch preparation."""

    def test_execute__eligible_request__returns_complete_replay_equal_candidate(
        self,
    ) -> None:
        """Construct the complete pending-work group without an external effect.

        Evidence ID: SV-WFC-DISPATCH-PREPARER-001

        Requirement: Preparation from a replay-equal predecessor appends exactly one
        activation, started attempt, closed authorization result, authority reference,
        request correlation, reservation, and obligation and replay-verifies the
        candidate before returning it.

        Acceptance: The result is ``prepared`` with equal predecessor and candidate
        replay results and one record in every required pending-work collection.
        """
        request = self.make_request()
        result = SUT(SimulationExecutionAuthorizer(), WorkflowRunReplayer()).execute(
            request
        )

        assert result.kind is SimulationDispatchPreparationOutcomeKind.PREPARED
        assert result.candidate_run is not None
        assert result.candidate_run.predecessor_revision_identity == (
            request.predecessor_run.revision_identity
        )
        assert result.candidate_run.revision_identity == request.next_revision_identity
        assert len(result.candidate_run.activations) == 1
        assert len(result.candidate_run.attempts) == 1
        assert len(result.candidate_run.authorization_results) == 1
        assert len(result.candidate_run.authority_references) == 1
        assert len(result.candidate_run.execution_request_correlations) == 1
        assert len(result.candidate_run.authority_reservations) == 1
        assert len(result.candidate_run.dispatch_obligations) == 1
        assert result.candidate_replay_result is not None
        assert result.candidate_replay_result.outcome.value == "equal"

    def test_execute__revoked_authority__returns_denied_without_candidate(
        self,
    ) -> None:
        """Preserve authorization denial without constructing pending work.

        Evidence ID: SV-WFC-DISPATCH-PREPARER-002

        Requirement: A preparation-phase authority denial creates no candidate.

        Acceptance: A revoked grant returns ``denied`` with the closed authorization
        result and no candidate replay.
        """
        request = self.make_request()
        denied_authorization = ControlScenarioFactory.authorization_request(
            phase=SimulationExecutionAuthorizationPhase.PREPARATION,
            state=ScientificExecutionGrantState.REVOKED,
            result_identity="authorization.preparation.denied",
            input_result_reference_identities=(),
        )
        result = SUT(SimulationExecutionAuthorizer(), WorkflowRunReplayer()).execute(
            replace(request, authorization_request=denied_authorization)
        )

        assert result.kind is SimulationDispatchPreparationOutcomeKind.DENIED
        assert result.authorization_result is not None
        assert result.candidate_run is None
        assert result.candidate_replay_result is None

    def test_execute__stale_predecessor_bundle__fails_before_authorization(
        self,
    ) -> None:
        """Fail closed when the exact predecessor cannot be replayed.

        Evidence ID: SV-WFC-DISPATCH-PREPARER-003

        Requirement: A non-equal predecessor grants no candidate-construction path.

        Acceptance: A runtime-bundle identity mismatch returns ``error`` with no
        authorization result and no candidate.
        """
        request = self.make_request()
        stale_run = replace(
            request.predecessor_run,
            runtime_bundle_identity=WorkflowRuntimeBundleIdentity("bundle.stale"),
        )
        result = SUT(SimulationExecutionAuthorizer(), WorkflowRunReplayer()).execute(
            replace(request, predecessor_run=stale_run)
        )

        assert result.kind is SimulationDispatchPreparationOutcomeKind.ERROR
        assert result.authorization_result is None
        assert result.candidate_run is None

    @classmethod
    def make_request(cls) -> SimulationDispatchPreparationRequest:
        """Construct one exact replayable predecessor and preparation request."""
        run, bundle, task_instance = cls.make_predecessor()
        activation = TaskActivation(
            identity=TaskActivationIdentity("activation.one"),
            workflow_identity=run.workflow_identity,
            workflow_run_identity=run.identity,
            task_instance=task_instance,
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            inputs=(),
            selection=DirectTaskActivationSelection(
                ColoredPetriNetSelectionResultIdentity("0" * 64)
            ),
        )
        authorization = ControlScenarioFactory.authorization_request(
            phase=SimulationExecutionAuthorizationPhase.PREPARATION,
            state=ScientificExecutionGrantState.UNUSED,
            result_identity="authorization.preparation.one",
            input_result_reference_identities=(),
        )
        return SimulationDispatchPreparationRequest(
            predecessor_run=run,
            runtime_bundle=bundle,
            activation=activation,
            authorization_request=authorization,
            next_revision_identity=WorkflowRunRevisionIdentity("revision.prepared"),
            started_attempt_record_identity=TaskAttemptRecordIdentity(
                "attempt.one.started"
            ),
            request_correlation_identity=(
                SimulationExecutionRequestCorrelationIdentity("correlation.one")
            ),
            reservation_identity=AuthorityReservationOutcomeIdentity("reservation.one"),
            creation_idempotency_identity=DispatchCreationIdempotencyIdentity(
                "dispatch-create.one"
            ),
        )

    @staticmethod
    def make_predecessor() -> tuple[WorkflowRun, WorkflowRuntimeBundle, TaskInstance]:
        """Construct one empty-marking WorkflowRun and exact runtime bundle."""
        definition = ColoredPetriNetDefinition(
            ColoredPetriNetDefinitionIdentity("control.preparation.v1"),
            (),
            (),
            (),
            (),
            (),
        )
        marking = ColoredPetriNetMarking(
            ColoredPetriNetMarkingIdentity("marking.initial"),
            definition.identity,
            (),
        )
        workflow_identity = WorkflowIdentity("workflow.one")
        run_identity = WorkflowRunIdentity("run.one")
        task_definition_identity = TaskDefinitionIdentity("task.simulation.one")
        task_instance = TaskInstance(
            TaskInstanceIdentity("task-instance.one"),
            task_definition_identity,
            None,
        )
        reference = WorkflowDefinitionReference(
            identity=WorkflowDefinitionReferenceIdentity("definition-reference.one"),
            workflow_identity=workflow_identity,
            workflow_definition_version=1,
            colored_petri_net_definition_identity=definition.identity,
            colored_petri_net_definition_version=1,
            task_definition_identities=(task_definition_identity,),
            schema_version=1,
        )
        bundle = WorkflowRuntimeBundle(
            identity=WorkflowRuntimeBundleIdentity("bundle.one"),
            definition_reference=reference,
            schema_version=1,
            workflow_identity=workflow_identity,
            definition=definition,
            task_definition_identities=(task_definition_identity,),
            adapter_implementation_identity="workflow-cpn-adapter-v1",
            expression_evaluator_identity=ColoredPetriNetExpressionEvaluatorIdentity(
                "colored-petri-net-expression-evaluator-v1"
            ),
            ordering_policy_identity=ColoredPetriNetOrderingPolicyIdentity(
                "colored-petri-net-enablement-order-v1"
            ),
            transition_enabler_identity=ColoredPetriNetTransitionEnablerIdentity(
                "colored-petri-net-transition-enabler-v1"
            ),
            binding_selector_identity=ColoredPetriNetBindingSelectorIdentity(
                "colored-petri-net-binding-selector-v1"
            ),
            transition_firer_identity=ColoredPetriNetTransitionFirerIdentity(
                "colored-petri-net-transition-firer-v1"
            ),
        )
        run = WorkflowRun(
            identity=run_identity,
            revision_identity=WorkflowRunRevisionIdentity("revision.initial"),
            predecessor_revision_identity=None,
            workflow_identity=workflow_identity,
            definition_reference_identity=reference.identity,
            runtime_bundle_identity=bundle.identity,
            schema_version=1,
            adapter_implementation_identity="workflow-cpn-adapter-v1",
            task_instances=(task_instance,),
            task_memberships=(
                TaskWorkflowMembership(
                    identity=TaskWorkflowMembershipIdentity("membership.one"),
                    workflow_run_identity=run_identity,
                    workflow_identity=workflow_identity,
                    task_instance_identity=task_instance.identity,
                ),
            ),
            nested_memberships=(),
            nested_invocations=(),
            activations=(),
            attempts=(),
            outcomes=(),
            result_references=(),
            result_productions=(),
            native_output_admissions=(),
            result_dependencies=(),
            failures=(),
            authorization_results=(),
            authority_references=(),
            execution_request_correlations=(),
            authority_reservations=(),
            dispatch_obligations=(),
            dispatch_entries=(),
            dispatch_observations=(),
            dispatch_outcomes=(),
            obligation_dispositions=(),
            scientific_decision_requests=(),
            scientific_decision_resolutions=(),
            initial_marking=marking,
            current_marking=marking,
            transitions=(),
        )
        return run, bundle, task_instance
