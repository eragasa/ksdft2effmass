r"""Software verification of ``QuantumEspressoAuthorizedDispatchWorkflow``.

Evidence profile: routine

Bounded artifact scope: application composition between persisted generic Workflow
dispatch control and the integration-owned local QE effect port.

Facet and represented meaning

The Workflow consumes one exact lifecycle request and delegates reservation, claim,
durable dispatch entry, and at-most-once effect entry to their existing owners.

Intrinsic and cross-object scope

The maintained cases verify successful reservation, claim, durable dispatch entry,
one deterministic fixture effect, confirmed reconciliation, immutable result/native
output admission, obligation disposition, generic CPN result firing, and terminal
successor persistence. They also verify stale claim authority stopping before claim
commit, dispatch entry, workspace creation, or effect-port invocation.

VVUQ and scientific exclusions

All values are synthetic test data. One case invokes only the maintained deterministic
fixture executable, never Quantum ESPRESSO, and establishes no numerical verification,
scientific validation, uncertainty quantification, production readiness,
protected-execution authority, or human acceptance.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import cast
from unittest.mock import Mock

import pytest

from ksdft2effmass.integration.quantum_espresso import (
    LocalQuantumEspressoExecutor,
    QuantumEspressoCompletedOutcome,
    QuantumEspressoPwResult,
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.persistence import RevisionReadRequest, RevisionSelector
from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetBinding,
    ColoredPetriNetBindingAssignment,
    ColoredPetriNetBindingSelector,
    ColoredPetriNetBindingVariableIdentity,
    ColoredPetriNetFiringInput,
    ColoredPetriNetFiringOutcomeKind,
    ColoredPetriNetTransitionEnabler,
    ColoredPetriNetTransitionFirer,
    ColoredPetriNetTransitionIdentity,
    ColoredPetriNetValue,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.simulations.quantumespresso.execution import (
    QuantumEspressoAuthorizedDispatchWorkflow,
)
from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeKind,
    DispatchObservationRecordIdentity,
    DispatchOutcomeKind,
    DispatchOutcomeRecord,
    DispatchOutcomeRecordIdentity,
    NativeOutputAdmission,
    NativeOutputAdmissionIdentity,
    ObligationDisposition,
    ObligationDispositionIdentity,
    ObligationDispositionKind,
    RepresentedTaskResultProducer,
    ResultObjectReference,
    ResultObjectReferenceIdentity,
    ResultProducerProvenanceIdentity,
    ResultProductionRecord,
    ResultProductionRecordIdentity,
    ScientificExecutorIdentity,
    SimulationDispatchAdapterResult,
    SimulationDispatchAdapterResultKind,
    SimulationDispatchEntryOutcomeKind,
    SimulationDispatchReconciler,
    SimulationDispatchReconciliationOutcomeKind,
    SimulationDispatchReconciliationRequest,
    SimulationDispatchResultIngressOutcomeKind,
    SimulationDispatchResultIngressPreparer,
    SimulationDispatchResultIngressRequest,
    SimulationExecutionAuthorizer,
    TaskAttempt,
    TaskAttemptRecordIdentity,
    TaskAttemptStatus,
    TaskInvocationOutcome,
    TaskInvocationOutcomeIdentity,
    TaskInvocationOutcomeKind,
    TaskWorkflowTransitionRecord,
    TaskWorkflowTransitionRecordIdentity,
    WorkflowRunCommitBinding,
    WorkflowRunRevisionIdentity,
    WorkflowRunTransaction,
    WorkflowTransitionSequenceIdentity,
)
from ksdft2effmass.workflows.control.lifecycle import (
    SimulationDispatchControlFailure,
    SimulationDispatchControlFailureStage,
)
from ksdft2effmass.workflows.runs.replay import WorkflowRunReplayer

from .resources.local_qe_executor import LocalQuantumEspressoExecutorScenarioFactory
from .resources.scenarios import ControlScenarioFactory
from .test__SimulationDispatchControlWorkflow import (
    TestSimulationDispatchControlWorkflow as ControlWorkflowEvidenceFactory,
)

pytestmark = pytest.mark.software_verification
SUT = QuantumEspressoAuthorizedDispatchWorkflow


class TestQuantumEspressoAuthorizedDispatchWorkflow:
    """Own software evidence for persisted Workflow-to-QE dispatch composition."""

    def test_method__execute__persists_control_and_runs_fixture_once(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-AUTHORIZED-DISPATCH-002

        Requirement: Exact synthetic authority and replay-equal persisted state must
        traverse reservation, claim, immediate reauthorization, dispatch entry, one
        deterministic local fixture effect, confirmed reconciliation, result ingress,
        generic CPN firing, and terminal successor persistence.

        Acceptance: Dispatch entry and the replay-equal terminal successor are
        committed; the effect is invoked once; the immutable QE result, native-output
        admission, obligation disposition, CPN successor marking, completion marker,
        and local terminal record all retain exact correlation.
        """
        request = ControlWorkflowEvidenceFactory.control_request()
        run_root = (tmp_path / "runs").resolve()
        run_root.mkdir()
        executor = LocalQuantumEspressoExecutorScenarioFactory.execute(
            run_root, request
        )
        repository, serializer = ControlWorkflowEvidenceFactory.repository(
            tmp_path / "workflow.sqlite"
        )
        ControlWorkflowEvidenceFactory.commit_predecessor(
            repository, serializer, request
        )

        result = SUT(
            repository=repository,
            serializer=serializer,
            runtime_bundle=request.preparation_request.runtime_bundle,
            authorizer=SimulationExecutionAuthorizer(),
            executor=executor,
        ).execute(request)

        assert type(result) is SimulationDispatchAdapterResult
        assert result.kind is SimulationDispatchAdapterResultKind.DISPATCHED
        assert result.effect_invoked
        assert result.entry_result is not None
        assert result.entry_result.kind is SimulationDispatchEntryOutcomeKind.ENTERED
        assert result.request.claimed_reservation.kind is (
            AuthorityReservationOutcomeKind.CLAIMED
        )
        assert result.outcome is not None
        assert result.outcome.kind is DispatchOutcomeKind.CONFIRMED
        assert type(result.outcome.result) is QuantumEspressoPwResult
        assert type(result.outcome.result.evidence.calculator_outcome) is (
            QuantumEspressoCompletedOutcome
        )
        assert (run_root / "attempt-001" / "records" / "terminal.json").is_file()

        assert result.entry_result.receipt is not None
        reconciliation = SimulationDispatchReconciler.execute(
            SimulationDispatchReconciliationRequest(
                dispatch_request=result.request,
                dispatch_entry_receipt=result.entry_result.receipt,
                observation_record_identity=DispatchObservationRecordIdentity(
                    "dispatch-observation-record.control-fixture"
                ),
                observations=(result.outcome,),
                reconciliation_identity_values=(
                    "reconciliation.control-fixture.confirmed",
                ),
            )
        )
        assert reconciliation.kind is (
            SimulationDispatchReconciliationOutcomeKind.CONFIRMED
        )
        loaded = repository.load(
            RevisionReadRequest(
                request_id="read.dispatch-entered.control-fixture",
                stream_id=result.request.execution_request.correlation.workflow_run_identity.value,
                selector=RevisionSelector.LATEST,
            )
        )
        assert loaded.snapshot is not None
        dispatch_entered_run = loaded.snapshot.run
        correlation = result.request.execution_request.correlation
        started = next(
            value
            for value in dispatch_entered_run.attempts
            if value.attempt_identity == correlation.attempt_identity
            and value.status is TaskAttemptStatus.STARTED
        )
        terminal = TaskAttempt(
            identity=TaskAttemptRecordIdentity("attempt.control-fixture.confirmed"),
            workflow_run_identity=dispatch_entered_run.identity,
            task_instance_identity=correlation.task_instance_identity,
            activation_identity=correlation.activation_identity,
            operation_identity=correlation.operation_identity,
            attempt_identity=correlation.attempt_identity,
            status=TaskAttemptStatus.CONFIRMED,
            predecessor_attempt_record_identity=started.identity,
        )
        outcome_identity = TaskInvocationOutcomeIdentity(
            "invocation.control-fixture.confirmed"
        )
        production_identity = ResultProductionRecordIdentity(
            "production.control-fixture"
        )
        reference_identity = ResultObjectReferenceIdentity(
            "result-reference.control-fixture"
        )
        encoded_result = QuantumEspressoResultValueSerializer().encode(
            result.outcome.result
        )
        assert encoded_result.encoded is not None
        envelope = encoded_result.encoded
        producer = RepresentedTaskResultProducer(
            identity=ResultProducerProvenanceIdentity("producer.control-fixture"),
            workflow_identity=dispatch_entered_run.workflow_identity,
            workflow_run_identity=dispatch_entered_run.identity,
            task_instance_identity=correlation.task_instance_identity,
            activation_identity=correlation.activation_identity,
            operation_identity=correlation.operation_identity,
            attempt_identity=correlation.attempt_identity,
            terminal_attempt_record_identity=terminal.identity,
            outcome_identity=outcome_identity,
            production_identity=production_identity,
        )
        reference = ResultObjectReference(
            identity=reference_identity,
            result=result.outcome.result,
            concrete_type_identity=envelope.concrete_type_identity,
            owning_domain_identity=envelope.owning_domain_identity,
            content_identity=envelope.content_identity,
            producer_provenance=producer,
        )
        invocation = TaskInvocationOutcome(
            identity=outcome_identity,
            workflow_run_identity=dispatch_entered_run.identity,
            activation_identity=correlation.activation_identity,
            operation_identity=correlation.operation_identity,
            attempt_identity=correlation.attempt_identity,
            terminal_attempt_record_identity=terminal.identity,
            kind=TaskInvocationOutcomeKind.CONFIRMED,
            results=(reference,),
            production_record_identities=(production_identity,),
            dispatch_outcome_record_identity=DispatchOutcomeRecordIdentity(
                "dispatch-outcome-record.control-fixture"
            ),
        )
        external_binding = ColoredPetriNetBinding(
            ColoredPetriNetTransitionIdentity("complete.simulation"),
            (
                ColoredPetriNetBindingAssignment(
                    ColoredPetriNetBindingVariableIdentity("result"),
                    ColoredPetriNetValue(
                        ColoredPetriNetValueKind.STRING,
                        result.outcome.result.identity.value,
                    ),
                ),
            ),
        )
        definition = request.preparation_request.runtime_bundle.definition
        enablement = ColoredPetriNetTransitionEnabler().execute(
            definition, dispatch_entered_run.current_marking
        )
        selection = ColoredPetriNetBindingSelector().execute(definition, enablement)
        assert selection.selected_binding is not None
        firing = ColoredPetriNetTransitionFirer().execute(
            ColoredPetriNetFiringInput(
                definition,
                ColoredPetriNetTransitionIdentity("complete.simulation"),
                dispatch_entered_run.current_marking,
                enablement,
                selection,
                selection.selected_binding,
                None,
                external_binding,
            )
        )
        assert firing.outcome is ColoredPetriNetFiringOutcomeKind.SUCCESS
        production = ResultProductionRecord(
            identity=production_identity,
            workflow_run_identity=dispatch_entered_run.identity,
            task_instance_identity=correlation.task_instance_identity,
            activation_identity=correlation.activation_identity,
            operation_identity=correlation.operation_identity,
            attempt_identity=correlation.attempt_identity,
            terminal_attempt_record_identity=terminal.identity,
            outcome_identity=outcome_identity,
            result_reference_identity=reference_identity,
            result_artifact_relation_identities=(),
            external_output_binding=external_binding,
        )
        dispatch_record = DispatchOutcomeRecord(
            identity=DispatchOutcomeRecordIdentity(
                "dispatch-outcome-record.control-fixture"
            ),
            envelope_identity=result.outcome.observation_identity,
            workflow_run_identity=dispatch_entered_run.identity,
            request_identity=correlation.request_identity,
            task_instance_identity=correlation.task_instance_identity,
            activation_identity=correlation.activation_identity,
            operation_identity=correlation.operation_identity,
            attempt_identity=correlation.attempt_identity,
            executor_identity=correlation.executor_identity,
            obligation_identity=correlation.obligation_identity,
            grant_identity=correlation.grant_identity,
            kind=DispatchOutcomeKind.CONFIRMED,
            result_reference_identity=reference_identity,
        )
        native_output_manifest_identity = result.outcome.native_output_manifest_identity
        assert native_output_manifest_identity is not None
        admission = NativeOutputAdmission(
            identity=NativeOutputAdmissionIdentity(
                "native-output-admission.control-fixture"
            ),
            workflow_run_identity=dispatch_entered_run.identity,
            dispatch_outcome_record_identity=dispatch_record.identity,
            dispatch_envelope_identity=result.outcome.observation_identity,
            production_record_identity=production.identity,
            result_reference_identity=reference.identity,
            manifest_identity=native_output_manifest_identity,
            manifest_entry_identities=(
                result.outcome.native_output_manifest_entry_identities
            ),
        )
        disposition = ObligationDisposition(
            identity=ObligationDispositionIdentity(
                "obligation-disposition.control-fixture"
            ),
            obligation_identity=correlation.obligation_identity,
            request_identity=correlation.request_identity,
            dispatch_outcome_record_identity=dispatch_record.identity,
            attempt_record_identity=terminal.identity,
            kind=ObligationDispositionKind.CONFIRMED,
        )
        transition = TaskWorkflowTransitionRecord(
            identity=TaskWorkflowTransitionRecordIdentity(
                "transition-record.control-fixture"
            ),
            sequence_identity=WorkflowTransitionSequenceIdentity(
                "transition-sequence.control-fixture"
            ),
            sequence_index=len(dispatch_entered_run.transitions),
            workflow_identity=dispatch_entered_run.workflow_identity,
            workflow_run_identity=dispatch_entered_run.identity,
            definition_reference_identity=(
                dispatch_entered_run.definition_reference_identity
            ),
            runtime_bundle_identity=dispatch_entered_run.runtime_bundle_identity,
            activation_identity=correlation.activation_identity,
            operation_identity=correlation.operation_identity,
            attempt_identity=correlation.attempt_identity,
            terminal_attempt_record_identity=terminal.identity,
            outcome_identity=invocation.identity,
            result_production_identities=(production.identity,),
            firing_result=firing,
            request_correlation_identity=correlation.identity,
            dispatch_outcome_record_identity=dispatch_record.identity,
        )
        ingress_request = SimulationDispatchResultIngressRequest(
            predecessor_run=dispatch_entered_run,
            runtime_bundle=request.preparation_request.runtime_bundle,
            reconciliation_result=reconciliation,
            next_revision_identity=WorkflowRunRevisionIdentity(
                "revision.control-fixture.completed"
            ),
            terminal_attempt=terminal,
            invocation_outcome=invocation,
            dispatch_outcome=dispatch_record,
            obligation_dispositions=(disposition,),
            result_references=(reference,),
            result_productions=(production,),
            native_output_admissions=(admission,),
            failures=(),
            transition=transition,
        )
        ingress = SimulationDispatchResultIngressPreparer(
            replayer=WorkflowRunReplayer()
        ).execute(ingress_request)
        assert ingress.kind is SimulationDispatchResultIngressOutcomeKind.ADMITTED
        assert ingress.candidate_run is not None
        completion_binding = WorkflowRunCommitBinding(
            transaction_identity="transaction.control-fixture.completed",
            commit_idempotency_identity="commit.control-fixture.completed",
            persistence_implementation_identity=(
                "ksdft2effmass.workflows.WorkflowRunAtomicRepository:1"
            ),
        )
        completion_bytes = serializer.serialize(
            ingress.candidate_run, completion_binding
        )
        assert completion_bytes.encoded is not None
        committed = repository.commit(
            WorkflowRunTransaction(
                binding=completion_binding,
                run_identity=ingress.candidate_run.identity,
                expected_predecessor_revision_identity=(
                    dispatch_entered_run.revision_identity
                ),
                candidate=ingress.candidate_run,
                schema_identity=completion_bytes.encoded.schema_identity,
                content_identity=completion_bytes.encoded.content_identity,
            )
        )
        assert committed.status == "committed"
        assert ingress.candidate_run.current_marking == firing.successor_marking
        assert ingress.candidate_run.result_references == (reference,)
        assert ingress.candidate_run.native_output_admissions == (admission,)
        assert ingress.candidate_run.obligation_dispositions == (disposition,)

    def test_method__execute__stale_authority_performs_no_qe_effect(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-QE-AUTHORIZED-DISPATCH-001

        Requirement: Application composition must preserve generic claim-phase denial
        before claim commit, durable dispatch entry, or the integration-owned QE
        effect.

        Method: Bind the complete generic lifecycle and an autospecced local QE
        executor, then submit a claim request evaluated after its freshness bound.

        Oracle: The generic authorizer's closed stale-authority denial and a local-QE
        effect sentinel configured to fail if called.

        Acceptance: The result identifies claim-stage failure and the executor
        sentinel observes zero calls.

        Interpretation: A committed reservation and QE executor binding are not
        sufficient when claim authority is stale.

        Limitations: The denial path does not exercise a successful claim commit,
        dispatch-entry commit, or process invocation.
        """
        executor_mock = Mock(spec=LocalQuantumEspressoExecutor)
        executor_mock.executor_identity = ScientificExecutorIdentity("executor.one")
        executor_mock.execute.side_effect = AssertionError("QE effect was entered")
        executor = cast(LocalQuantumEspressoExecutor, executor_mock)
        request = ControlWorkflowEvidenceFactory.control_request()
        stale_request = replace(
            request,
            claim_authorization_request=replace(
                request.claim_authorization_request,
                evaluated_at=ControlScenarioFactory.instant(4),
            ),
        )
        repository, serializer = ControlWorkflowEvidenceFactory.repository(
            tmp_path / "workflow.sqlite"
        )
        ControlWorkflowEvidenceFactory.commit_predecessor(
            repository, serializer, stale_request
        )
        runtime_bundle = request.preparation_request.runtime_bundle
        workflow = SUT(
            repository=repository,
            serializer=serializer,
            runtime_bundle=runtime_bundle,
            authorizer=SimulationExecutionAuthorizer(),
            executor=executor,
        )

        result = workflow.execute(stale_request)

        assert type(result) is SimulationDispatchControlFailure
        assert result.stage is SimulationDispatchControlFailureStage.CLAIM
        executor_mock.execute.assert_not_called()
