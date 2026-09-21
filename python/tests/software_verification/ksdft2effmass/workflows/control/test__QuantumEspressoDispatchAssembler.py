r"""Software verification of ``QuantumEspressoDispatchAssembler``.

Evidence profile: routine

Bounded artifact scope: effect-free assembly from one dated QE manifest composition,
replay-equal persisted WorkflowRun predecessor, Task activation, and separately
supplied authority views.

Facet and represented meaning

The assembler produces a generic dispatch-control request without granting authority,
committing a successor, creating a workspace, or invoking an executor.

Intrinsic and cross-object scope

Tests cover exact successful assembly and fail-closed authority-scope mismatch.
Lifecycle persistence and process entry remain separately owned.

VVUQ and scientific exclusions

All values are synthetic test data. No executable is invoked, and the tests establish
no numerical verification, scientific validation, uncertainty quantification,
production authority, or human acceptance.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from ksdft2effmass.persistence import RevisionReadRequest, RevisionSelector
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
from ksdft2effmass.simulations.quantumespresso import (
    QuantumEspressoExecution,
    QuantumEspressoExecutionRequest,
    QuantumEspressoPlanner,
)
from ksdft2effmass.simulations.quantumespresso.dispatch_assembly import (
    QuantumEspressoDispatchAssembler,
    QuantumEspressoDispatchAssemblyOutcomeKind,
    QuantumEspressoDispatchAssemblyRequest,
)
from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeIdentity,
    DirectTaskActivationSelection,
    DispatchCreationIdempotencyIdentity,
    OperationIdentity,
    ScientificExecutionGrantState,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizationRequest,
    SimulationExecutionRequestCorrelationIdentity,
    TaskActivation,
    TaskAttemptRecordIdentity,
    TaskInstance,
    TaskWorkflowMembership,
    TaskWorkflowMembershipIdentity,
    WorkflowDefinitionReference,
    WorkflowDefinitionReferenceIdentity,
    WorkflowIdentity,
    WorkflowRun,
    WorkflowRunAtomicRepository,
    WorkflowRunCommitBinding,
    WorkflowRunIdentity,
    WorkflowRunRevisionIdentity,
    WorkflowRuntimeBundle,
    WorkflowRuntimeBundleIdentity,
    WorkflowRunTransaction,
)

from .resources.scenarios import ControlScenarioFactory
from .test__SimulationDispatchControlWorkflow import (
    TestSimulationDispatchControlWorkflow as ControlWorkflowEvidenceFactory,
)

pytestmark = pytest.mark.software_verification
SUT = QuantumEspressoDispatchAssembler


class TestQuantumEspressoDispatchAssembler:
    """Own software evidence for effect-free persisted QE request assembly."""

    @staticmethod
    def manifest() -> Path:
        """Evidence ID: This helper owns no identifier.

        Requirement: Name the maintained dated-v2 synthetic manifest.

        Acceptance: The returned path is absolute.
        """
        return (
            Path(__file__).parents[2]
            / "simulations"
            / "quantumespresso"
            / "resources"
            / "execution-manifest-v2.json"
        ).resolve()

    @staticmethod
    def predecessor(
        workflow_run_identity: WorkflowRunIdentity,
        task_instance: TaskInstance,
    ) -> tuple[WorkflowRun, WorkflowRuntimeBundle]:
        """Evidence ID: This helper owns no identifier.

        Requirement: Construct one replay-equal predecessor matching the QE plan.

        Acceptance: Run, bundle, and Task identities close exactly.
        """
        definition = ColoredPetriNetDefinition(
            ColoredPetriNetDefinitionIdentity("qe.dispatch.assembly.v1"),
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
        workflow_identity = WorkflowIdentity("workflow.qe.example01")
        reference = WorkflowDefinitionReference(
            identity=WorkflowDefinitionReferenceIdentity("definition-reference.qe"),
            workflow_identity=workflow_identity,
            workflow_definition_version=1,
            colored_petri_net_definition_identity=definition.identity,
            colored_petri_net_definition_version=1,
            task_definition_identities=(task_instance.definition_identity,),
            schema_version=1,
        )
        bundle = WorkflowRuntimeBundle(
            identity=WorkflowRuntimeBundleIdentity("bundle.qe.example01"),
            definition_reference=reference,
            schema_version=1,
            workflow_identity=workflow_identity,
            definition=definition,
            task_definition_identities=(task_instance.definition_identity,),
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
            identity=workflow_run_identity,
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
                    identity=TaskWorkflowMembershipIdentity("membership.qe.example01"),
                    workflow_run_identity=workflow_run_identity,
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
        return run, bundle

    @classmethod
    def request(
        cls, tmp_path: Path
    ) -> tuple[
        QuantumEspressoDispatchAssemblyRequest,
        WorkflowRunAtomicRepository,
    ]:
        """Evidence ID: This helper owns no identifier.

        Requirement: Persist one exact predecessor and construct assembly input.

        Acceptance: The read request carries complete revision expectations.
        """
        execution = QuantumEspressoPlanner().execute(
            QuantumEspressoExecutionRequest(manifest_path=cls.manifest())
        )
        local = execution.local_execution_plan
        execution_input = local.preparation_request.execution_input
        task_instance = TaskInstance(
            execution_input.task_instance_identity,
            execution_input.task_definition_identity,
            None,
        )
        predecessor, bundle = cls.predecessor(
            local.workflow_run_identity, task_instance
        )
        repository, serializer = ControlWorkflowEvidenceFactory.repository(
            tmp_path / "workflow.sqlite"
        )
        binding = WorkflowRunCommitBinding(
            transaction_identity="transaction.genesis.assembly",
            commit_idempotency_identity="commit.genesis.assembly",
            persistence_implementation_identity=(
                "ksdft2effmass.workflows.WorkflowRunAtomicRepository:1"
            ),
        )
        encoded = serializer.serialize(predecessor, binding)
        assert encoded.encoded is not None
        write = repository.commit(
            WorkflowRunTransaction(
                binding=binding,
                run_identity=predecessor.identity,
                expected_predecessor_revision_identity=None,
                candidate=predecessor,
                schema_identity=encoded.encoded.schema_identity,
                content_identity=encoded.encoded.content_identity,
            )
        )
        assert write.status == "committed"
        assert write.snapshot is not None
        revision = write.snapshot.revision
        read = RevisionReadRequest(
            request_id="read.qe.assembly",
            stream_id=revision.stream_id,
            selector=RevisionSelector.EXPLICIT_REVISION,
            revision_id=revision.revision_id,
            expected_predecessor_revision_id=revision.predecessor_revision_id,
            expected_schema_id=revision.schema_id,
            expected_content_id=revision.content_id,
            expected_idempotency_id=binding.commit_idempotency_identity,
        )
        activation = TaskActivation(
            identity=execution_input.activation_identity,
            workflow_identity=predecessor.workflow_identity,
            workflow_run_identity=predecessor.identity,
            task_instance=task_instance,
            operation_identity=execution_input.operation_identity,
            attempt_identity=execution_input.attempt_identity,
            inputs=(),
            selection=DirectTaskActivationSelection(
                ColoredPetriNetSelectionResultIdentity("0" * 64)
            ),
        )
        preparation_authorization, claim_authorization = cls.authority_requests(
            execution, activation
        )
        request = QuantumEspressoDispatchAssemblyRequest(
            execution=execution,
            predecessor_read_request=read,
            runtime_bundle=bundle,
            activation=activation,
            preparation_authorization_request=preparation_authorization,
            claim_authorization_request=claim_authorization,
            prepared_revision_identity=WorkflowRunRevisionIdentity("revision.prepared"),
            started_attempt_record_identity=TaskAttemptRecordIdentity(
                "attempt.example01.started"
            ),
            request_correlation_identity=(
                SimulationExecutionRequestCorrelationIdentity(
                    "correlation.qe.example01"
                )
            ),
            reservation_identity=AuthorityReservationOutcomeIdentity(
                "reservation.qe.example01"
            ),
            creation_idempotency_identity=DispatchCreationIdempotencyIdentity(
                "dispatch-create.qe.example01"
            ),
            preparation_commit_binding=WorkflowRunCommitBinding(
                transaction_identity="transaction.qe.prepared",
                commit_idempotency_identity="commit.qe.prepared",
                persistence_implementation_identity=(
                    "ksdft2effmass.workflows.WorkflowRunAtomicRepository:1"
                ),
            ),
            claim_revision_identity=WorkflowRunRevisionIdentity("revision.claimed"),
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity(
                "claim.qe.example01"
            ),
            claim_commit_binding=WorkflowRunCommitBinding(
                transaction_identity="transaction.qe.claimed",
                commit_idempotency_identity="commit.qe.claimed",
                persistence_implementation_identity=(
                    "ksdft2effmass.workflows.WorkflowRunAtomicRepository:1"
                ),
            ),
        )
        return request, repository

    @staticmethod
    def authority_requests(
        execution: QuantumEspressoExecution,
        activation: TaskActivation,
    ) -> tuple[
        SimulationExecutionAuthorizationRequest,
        SimulationExecutionAuthorizationRequest,
    ]:
        """Evidence ID: This helper owns no identifier.

        Requirement: Construct exact unused and reserved synthetic authority views.

        Acceptance: Both views retain manifest authority and local-plan scope.
        """
        if type(execution) is not QuantumEspressoExecution:
            raise TypeError("execution must be QuantumEspressoExecution")
        local = execution.local_execution_plan
        preparation = local.preparation_request
        execution_input = preparation.execution_input
        snapshot = replace(
            ControlScenarioFactory.snapshot(),
            identity=local.grant_authority_reference.snapshot_identity,
        )
        unused = replace(
            ControlScenarioFactory.grant(
                state=ScientificExecutionGrantState.UNUSED,
                input_result_reference_identities=(),
            ),
            authority_reference=local.grant_authority_reference,
            request_identity=preparation.simulation_execution_request_identity,
            workflow_run_identity=local.workflow_run_identity,
            task_definition_identity=execution_input.task_definition_identity,
            task_instance_identity=execution_input.task_instance_identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            executor_identity=preparation.scientific_executor_identity,
            destination_identity=preparation.dispatch_destination_identity,
            resource_scope_identities=(preparation.dispatch_resource_scope_identity,),
            input_result_reference_identities=local.input_result_reference_identities,
            input_artifact_entry_identities=local.input_artifact_entry_identities,
        )
        reserved = replace(
            unused,
            state=ScientificExecutionGrantState.RESERVED,
            reserved_obligation_identity=local.obligation_identity,
        )
        prepare = SimulationExecutionAuthorizationRequest(
            result_identity=preparation.authorization_result_identity,
            phase=SimulationExecutionAuthorizationPhase.PREPARATION,
            grant=unused,
            snapshot=snapshot,
            request_identity=preparation.simulation_execution_request_identity,
            workflow_run_identity=local.workflow_run_identity,
            task_definition_identity=execution_input.task_definition_identity,
            task_instance_identity=execution_input.task_instance_identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            executor_identity=preparation.scientific_executor_identity,
            destination_identity=preparation.dispatch_destination_identity,
            obligation_identity=local.obligation_identity,
            resource_scope_identities=(preparation.dispatch_resource_scope_identity,),
            input_result_reference_identities=(local.input_result_reference_identities),
            input_artifact_entry_identities=local.input_artifact_entry_identities,
            evaluated_at=ControlScenarioFactory.instant(2),
        )
        claim = SimulationExecutionAuthorizationRequest(
            result_identity=local.claim_authorization_result_identity,
            phase=SimulationExecutionAuthorizationPhase.CLAIM,
            grant=reserved,
            snapshot=snapshot,
            request_identity=preparation.simulation_execution_request_identity,
            workflow_run_identity=local.workflow_run_identity,
            task_definition_identity=execution_input.task_definition_identity,
            task_instance_identity=execution_input.task_instance_identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            executor_identity=preparation.scientific_executor_identity,
            destination_identity=preparation.dispatch_destination_identity,
            obligation_identity=local.obligation_identity,
            resource_scope_identities=(preparation.dispatch_resource_scope_identity,),
            input_result_reference_identities=(local.input_result_reference_identities),
            input_artifact_entry_identities=local.input_artifact_entry_identities,
            evaluated_at=ControlScenarioFactory.instant(2),
        )
        return prepare, claim

    def test_method__execute__assembles_from_replay_equal_persisted_state(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-DISPATCH-ASSEMBLY-001

        Requirement: Exact replay-equal persisted state and independently supplied
        authority inputs must produce one inert dispatch-control request.

        Acceptance: Assembly succeeds, retains the loaded predecessor, and creates no
        external run root.
        """
        request, repository = self.request(tmp_path)

        result = SUT(repository=repository).execute(request)

        assert result.kind is QuantumEspressoDispatchAssemblyOutcomeKind.ASSEMBLED
        assert result.control_request is not None
        assert result.control_request.preparation_request.predecessor_run.identity == (
            request.execution.local_execution_plan.workflow_run_identity
        )
        assert not request.execution.plan.external_runs_root.exists()

    def test_method__execute__mismatched_authority_scope_fails_closed(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-DISPATCH-ASSEMBLY-002

        Requirement: A grant scoped to another operation must not produce a lifecycle
        request or external effect.

        Acceptance: Assembly reports correlation failure and returns no control
        request.
        """
        request, repository = self.request(tmp_path)
        mismatched = replace(
            request,
            claim_authorization_request=replace(
                request.claim_authorization_request,
                operation_identity=OperationIdentity("operation.other"),
                grant=replace(
                    request.claim_authorization_request.grant,
                    operation_identity=OperationIdentity("operation.other"),
                ),
            ),
        )

        result = SUT(repository=repository).execute(mismatched)

        assert result.kind is (
            QuantumEspressoDispatchAssemblyOutcomeKind.CORRELATION_FAILED
        )
        assert result.control_request is None
