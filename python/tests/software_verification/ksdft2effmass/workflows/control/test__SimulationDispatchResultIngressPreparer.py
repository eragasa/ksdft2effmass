r"""Software verification of ``SimulationDispatchResultIngressPreparer``.

Evidence profile: routine

Bounded artifact scope: effect-free terminal simulation-dispatch result ingress.

Facet and represented meaning

The ActionObject constructs one replay-verified terminal WorkflowRun candidate from an
exact committed claim and reconciliation.

Intrinsic and cross-object scope

This module verifies integrated prepare, claim, reconciliation, terminal-record, and
replay closure without repository or calculator execution.

VVUQ and scientific exclusions

This is software verification only and establishes no persistence implementation,
external scientific execution, scientific validation, uncertainty quantification,
authority issuance, or human acceptance.
"""

from dataclasses import replace

import pytest

from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeIdentity,
    DispatchObservationRecordIdentity,
    DispatchOutcomeKind,
    DispatchOutcomeRecord,
    DispatchOutcomeRecordIdentity,
    ObligationDisposition,
    ObligationDispositionIdentity,
    ObligationDispositionKind,
    OperationIdentity,
    ScientificExecutionGrantState,
    SimulationDispatchClaimPreparer,
    SimulationDispatchClaimRequest,
    SimulationDispatchEntry,
    SimulationDispatchEntryIdentity,
    SimulationDispatchEntryReceipt,
    SimulationDispatchEntryReceiptIdentity,
    SimulationDispatchObservationIdentity,
    SimulationDispatchOutcomeIdentity,
    SimulationDispatchPreparer,
    SimulationDispatchReconciler,
    SimulationDispatchReconciliationRequest,
    SimulationDispatchRequest,
    SimulationDispatchResultIngressOutcomeKind,
    SimulationDispatchResultIngressPreparer,
    SimulationDispatchResultIngressRequest,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionAuthorizer,
    SimulationExecutionRequest,
    TaskAttemptRecordIdentity,
    TaskAttemptStatus,
    TaskFailureRecord,
    TaskFailureRecordIdentity,
    TaskInvocationFailureIdentity,
    TaskInvocationOutcome,
    TaskInvocationOutcomeIdentity,
    TaskInvocationOutcomeKind,
    WorkflowRunClaimCommitReceipt,
    WorkflowRunClaimCommitReceiptIdentity,
    WorkflowRunRevisionIdentity,
)
from ksdft2effmass.workflows.runs.replay import WorkflowRunReplayer

from .resources.scenarios import ControlScenarioFactory
from .test__SimulationDispatchPreparer import (
    TestSimulationDispatchPreparer as PreparationEvidenceFactory,
)

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchResultIngressPreparer


class TestSimulationDispatchResultIngressPreparer:
    """Own integrated software evidence for terminal result ingress."""

    def test_method__execute__retains_indeterminate_then_admits_rejection(
        self,
    ) -> None:
        """Retain uncertain evidence before one later replay-valid terminal successor.

        Evidence ID: SV-WCI-RESULT-INGRESS-PREPARER-001

        Requirement: Result ingress consumes a committed dispatch-entered revision and
        exact reconciliation, then constructs an observation or final candidate
        without persistence or another external effect.

        Acceptance: A claimed predecessor without durable dispatch-entry state fails;
        an indeterminate no-observation reconciliation appends only an observation and
        leaves the attempt pending; repeating its observation identity fails, an
        uncorrelated error observation remains appendable without closing
        the attempt, a later rejected observation appends the single replay-equal
        terminal outcome and disposition, and a second final outcome fails.
        """
        preparation_request = PreparationEvidenceFactory.make_request()
        preparation_result = SimulationDispatchPreparer(
            authorizer=SimulationExecutionAuthorizer(),
            replayer=WorkflowRunReplayer(),
        ).execute(preparation_request)
        assert preparation_result.candidate_run is not None
        prepared_run = preparation_result.candidate_run
        runtime_bundle = preparation_request.runtime_bundle
        preparation_authorization = prepared_run.authorization_results[0]
        execution_correlation = prepared_run.execution_request_correlations[0]
        obligation = prepared_run.dispatch_obligations[0]
        claim_result_identity = SimulationExecutionAuthorizationResultIdentity(
            "authorization.claim.ingress"
        )
        execution_request = SimulationExecutionRequest(
            correlation=execution_correlation,
            obligation=obligation,
            preparation_authorization=preparation_authorization,
        )
        claim_request = SimulationDispatchClaimRequest(
            predecessor_run=prepared_run,
            runtime_bundle=runtime_bundle,
            execution_request=execution_request,
            claim_authorization_request=replace(
                preparation_authorization.request,
                result_identity=claim_result_identity,
                phase=SimulationExecutionAuthorizationPhase.CLAIM,
                grant=replace(
                    preparation_authorization.request.grant,
                    state=ScientificExecutionGrantState.RESERVED,
                    reserved_obligation_identity=obligation.identity,
                ),
            ),
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity(
                "reservation.claimed.ingress"
            ),
            next_revision_identity=WorkflowRunRevisionIdentity(
                "revision.claimed.ingress"
            ),
        )
        claim_result = SimulationDispatchClaimPreparer(
            authorizer=SimulationExecutionAuthorizer(),
            replayer=WorkflowRunReplayer(),
        ).execute(claim_request)
        assert claim_result.candidate_run is not None
        claimed_run = claim_result.candidate_run
        claim_authorization = next(
            value
            for value in claimed_run.authorization_results
            if value.identity == claim_result_identity
        )
        claimed_reservation = next(
            value
            for value in claimed_run.authority_reservations
            if value.identity == claim_request.claimed_reservation_identity
        )
        receipt = WorkflowRunClaimCommitReceipt(
            identity=WorkflowRunClaimCommitReceiptIdentity("receipt.claim.ingress"),
            workflow_run_identity=claimed_run.identity,
            committed_revision_identity=claimed_run.revision_identity,
            predecessor_revision_identity=prepared_run.revision_identity,
            claimed_reservation_identity=claimed_reservation.identity,
            claim_authorization_result_identity=claim_authorization.identity,
            workflow_run_content_identity="sha256:claimed-ingress",
            persistence_operation_identity="cas.claim.ingress",
            commit_idempotency_identity="idempotency.claim.ingress",
            persistence_implementation_identity="synthetic-persistence.v1",
        )
        dispatch_request = SimulationDispatchRequest(
            execution_request=execution_request,
            claim_authorization_request=claim_authorization.request,
            claimed_reservation=claimed_reservation,
            claim_commit_receipt=receipt,
            outcome_identity=SimulationDispatchOutcomeIdentity(
                "dispatch-outcome.ingress"
            ),
            dispatch_entry_identity=SimulationDispatchEntryIdentity(
                "dispatch-entry.ingress"
            ),
            dispatch_entry_revision_identity=WorkflowRunRevisionIdentity(
                "revision.dispatch-entered.ingress"
            ),
        )
        entry_receipt = SimulationDispatchEntryReceipt(
            identity=SimulationDispatchEntryReceiptIdentity("entry-receipt.ingress"),
            dispatch_entry_identity=dispatch_request.dispatch_entry_identity,
            workflow_run_identity=claimed_run.identity,
            claim_commit_receipt_identity=receipt.identity,
            predecessor_revision_identity=claimed_run.revision_identity,
            committed_revision_identity=(
                dispatch_request.dispatch_entry_revision_identity
            ),
            claimed_reservation_identity=claimed_reservation.identity,
            obligation_identity=obligation.identity,
            outcome_identity=dispatch_request.outcome_identity,
            workflow_run_content_identity="sha256:dispatch-entered-ingress",
            persistence_operation_identity="cas.dispatch-entry.ingress",
            persistence_implementation_identity="synthetic-persistence.v1",
        )
        dispatch_entry = SimulationDispatchEntry(
            identity=entry_receipt.dispatch_entry_identity,
            workflow_run_identity=claimed_run.identity,
            predecessor_revision_identity=entry_receipt.predecessor_revision_identity,
            committed_revision_identity=entry_receipt.committed_revision_identity,
            claimed_reservation_identity=entry_receipt.claimed_reservation_identity,
            request_identity=execution_correlation.request_identity,
            obligation_identity=entry_receipt.obligation_identity,
            receipt_identity=entry_receipt.identity,
            outcome_identity=entry_receipt.outcome_identity,
        )
        dispatch_entered_run = replace(
            claimed_run,
            revision_identity=entry_receipt.committed_revision_identity,
            predecessor_revision_identity=claimed_run.revision_identity,
            dispatch_entries=(dispatch_entry,),
        )
        assert (
            WorkflowRunReplayer()
            .execute(dispatch_entered_run, runtime_bundle)
            .outcome.value
            == "equal"
        )
        reconciliation = SimulationDispatchReconciler.execute(
            SimulationDispatchReconciliationRequest(
                dispatch_request=dispatch_request,
                dispatch_entry_receipt=entry_receipt,
                observation_record_identity=DispatchObservationRecordIdentity(
                    "dispatch-observation.ingress"
                ),
                observations=(),
                reconciliation_identity_values=("reconciliation.read.ingress",),
            )
        )
        assert reconciliation.outcome is None
        request = SimulationDispatchResultIngressRequest(
            predecessor_run=dispatch_entered_run,
            runtime_bundle=runtime_bundle,
            reconciliation_result=reconciliation,
            next_revision_identity=WorkflowRunRevisionIdentity(
                "revision.observation.ingress"
            ),
            terminal_attempt=None,
            invocation_outcome=None,
            dispatch_outcome=None,
            obligation_dispositions=(),
            result_references=(),
            result_productions=(),
            native_output_admissions=(),
            failures=(),
            transition=None,
        )

        stale_predecessor = SUT(replayer=WorkflowRunReplayer()).execute(
            replace(
                request,
                predecessor_run=claimed_run,
                next_revision_identity=WorkflowRunRevisionIdentity(
                    "revision.stale-observation.ingress"
                ),
            )
        )
        assert stale_predecessor.kind is (
            SimulationDispatchResultIngressOutcomeKind.ERROR
        )
        assert stale_predecessor.diagnostics == (
            "dispatch-entry state is absent from the predecessor",
        )

        result = SUT(replayer=WorkflowRunReplayer()).execute(request)

        assert result.kind is SimulationDispatchResultIngressOutcomeKind.ADMITTED
        assert result.candidate_run is not None
        assert result.candidate_run.attempts == dispatch_entered_run.attempts
        assert result.candidate_run.outcomes == ()
        assert result.candidate_run.dispatch_observations == (
            reconciliation.observation_record,
        )
        assert result.candidate_run.dispatch_outcomes == ()
        assert result.candidate_run.obligation_dispositions == ()
        assert result.candidate_replay_result is not None
        assert result.candidate_replay_result.outcome.value == "equal"

        observed_run = result.candidate_run
        repeated = SUT(replayer=WorkflowRunReplayer()).execute(
            replace(
                request,
                predecessor_run=observed_run,
                next_revision_identity=WorkflowRunRevisionIdentity(
                    "revision.observation-repeated.ingress"
                ),
            )
        )
        assert repeated.kind is SimulationDispatchResultIngressOutcomeKind.ERROR
        assert repeated.diagnostics == ("dispatch observation identity already exists",)

        mismatch = replace(
            ControlScenarioFactory.outcome(),
            identity=dispatch_request.outcome_identity,
            observation_identity=SimulationDispatchObservationIdentity(
                "dispatch-observation-envelope.error.ingress"
            ),
            request_identity=execution_correlation.request_identity,
            workflow_run_identity=claimed_run.identity,
            task_instance_identity=execution_correlation.task_instance_identity,
            activation_identity=execution_correlation.activation_identity,
            operation_identity=OperationIdentity("operation.mismatched.ingress"),
            attempt_identity=execution_correlation.attempt_identity,
            executor_identity=execution_correlation.executor_identity,
            obligation_identity=obligation.identity,
            grant_identity=execution_correlation.grant_identity,
        )
        error_reconciliation = SimulationDispatchReconciler.execute(
            SimulationDispatchReconciliationRequest(
                dispatch_request=dispatch_request,
                dispatch_entry_receipt=entry_receipt,
                observation_record_identity=DispatchObservationRecordIdentity(
                    "dispatch-observation.error.ingress"
                ),
                observations=(mismatch,),
                reconciliation_identity_values=("reconciliation.error.ingress",),
            )
        )
        error_observation = SUT(replayer=WorkflowRunReplayer()).execute(
            replace(
                request,
                predecessor_run=observed_run,
                reconciliation_result=error_reconciliation,
                next_revision_identity=WorkflowRunRevisionIdentity(
                    "revision.observation-error.ingress"
                ),
            )
        )
        assert error_observation.kind is (
            SimulationDispatchResultIngressOutcomeKind.ADMITTED
        )
        assert error_observation.candidate_run is not None
        assert len(error_observation.candidate_run.dispatch_observations) == 2
        mismatched_entry_record = replace(
            error_reconciliation.observation_record,
            dispatch_entry_receipt_identity=SimulationDispatchEntryReceiptIdentity(
                "entry-receipt.other"
            ),
        )
        mismatched_entry_run = replace(
            error_observation.candidate_run,
            dispatch_observations=tuple(
                sorted(
                    (
                        reconciliation.observation_record,
                        mismatched_entry_record,
                    ),
                    key=lambda value: value.identity.value,
                )
            ),
        )
        mismatched_entry_replay = WorkflowRunReplayer().execute(
            mismatched_entry_run, runtime_bundle
        )
        assert mismatched_entry_replay.outcome.value == "error"
        assert mismatched_entry_replay.issues[0].diagnostic == (
            "dispatch observation must close over its exact request and obligation"
        )

        identity_collision_outcome = replace(
            mismatch,
            operation_identity=OperationIdentity("operation.collision.ingress"),
        )
        identity_collision_record = replace(
            error_reconciliation.observation_record,
            observed_outcomes=(mismatch, identity_collision_outcome),
        )
        identity_collision_run = replace(
            error_observation.candidate_run,
            dispatch_observations=tuple(
                sorted(
                    (
                        reconciliation.observation_record,
                        identity_collision_record,
                    ),
                    key=lambda value: value.identity.value,
                )
            ),
        )
        identity_collision_replay = WorkflowRunReplayer().execute(
            identity_collision_run, runtime_bundle
        )
        assert identity_collision_replay.outcome.value == "error"
        assert identity_collision_replay.issues[0].diagnostic == (
            "one dispatch observation identity cannot name unequal content"
        )
        observed_run = error_observation.candidate_run

        rejected = replace(
            ControlScenarioFactory.outcome(kind=DispatchOutcomeKind.REJECTED),
            identity=dispatch_request.outcome_identity,
            observation_identity=SimulationDispatchObservationIdentity(
                "dispatch-observation-envelope.rejected.ingress"
            ),
            request_identity=execution_correlation.request_identity,
            workflow_run_identity=claimed_run.identity,
            task_instance_identity=execution_correlation.task_instance_identity,
            activation_identity=execution_correlation.activation_identity,
            operation_identity=execution_correlation.operation_identity,
            attempt_identity=execution_correlation.attempt_identity,
            executor_identity=execution_correlation.executor_identity,
            obligation_identity=obligation.identity,
            grant_identity=execution_correlation.grant_identity,
        )
        final_reconciliation = SimulationDispatchReconciler.execute(
            SimulationDispatchReconciliationRequest(
                dispatch_request=dispatch_request,
                dispatch_entry_receipt=entry_receipt,
                observation_record_identity=DispatchObservationRecordIdentity(
                    "dispatch-observation.rejected.ingress"
                ),
                observations=(rejected,),
                reconciliation_identity_values=("reconciliation.final.ingress",),
            )
        )
        started = next(
            value
            for value in observed_run.attempts
            if value.attempt_identity == execution_correlation.attempt_identity
            and value.status is TaskAttemptStatus.STARTED
        )
        terminal = replace(
            started,
            identity=TaskAttemptRecordIdentity("attempt.rejected.ingress"),
            status=TaskAttemptStatus.REJECTED,
            predecessor_attempt_record_identity=started.identity,
        )
        assert rejected.failure is not None
        failure = TaskFailureRecord(
            identity=TaskFailureRecordIdentity("failure-record.ingress"),
            workflow_run_identity=observed_run.identity,
            task_instance_identity=execution_correlation.task_instance_identity,
            activation_identity=execution_correlation.activation_identity,
            operation_identity=execution_correlation.operation_identity,
            attempt_identity=execution_correlation.attempt_identity,
            terminal_attempt_record_identity=terminal.identity,
            failure=rejected.failure,
            request_identity=execution_correlation.request_identity,
        )
        dispatch_record = DispatchOutcomeRecord(
            identity=DispatchOutcomeRecordIdentity("dispatch-record.rejected.ingress"),
            envelope_identity=rejected.observation_identity,
            workflow_run_identity=observed_run.identity,
            request_identity=execution_correlation.request_identity,
            task_instance_identity=execution_correlation.task_instance_identity,
            activation_identity=execution_correlation.activation_identity,
            operation_identity=execution_correlation.operation_identity,
            attempt_identity=execution_correlation.attempt_identity,
            executor_identity=execution_correlation.executor_identity,
            obligation_identity=obligation.identity,
            grant_identity=execution_correlation.grant_identity,
            kind=DispatchOutcomeKind.REJECTED,
            failure_record_identity=failure.identity,
        )
        invocation = TaskInvocationOutcome(
            identity=TaskInvocationOutcomeIdentity("invocation.rejected.ingress"),
            workflow_run_identity=observed_run.identity,
            activation_identity=execution_correlation.activation_identity,
            operation_identity=execution_correlation.operation_identity,
            attempt_identity=execution_correlation.attempt_identity,
            terminal_attempt_record_identity=terminal.identity,
            kind=TaskInvocationOutcomeKind.REJECTED,
            failure_record_identity=failure.identity,
            dispatch_outcome_record_identity=dispatch_record.identity,
        )
        disposition = ObligationDisposition(
            identity=ObligationDispositionIdentity("disposition.rejected.ingress"),
            obligation_identity=obligation.identity,
            request_identity=execution_correlation.request_identity,
            dispatch_outcome_record_identity=dispatch_record.identity,
            attempt_record_identity=terminal.identity,
            kind=ObligationDispositionKind.REJECTED,
        )
        final_request = SimulationDispatchResultIngressRequest(
            predecessor_run=observed_run,
            runtime_bundle=runtime_bundle,
            reconciliation_result=final_reconciliation,
            next_revision_identity=WorkflowRunRevisionIdentity(
                "revision.rejected.ingress"
            ),
            terminal_attempt=terminal,
            invocation_outcome=invocation,
            dispatch_outcome=dispatch_record,
            obligation_dispositions=(disposition,),
            result_references=(),
            result_productions=(),
            native_output_admissions=(),
            failures=(failure,),
            transition=None,
        )

        final = SUT(replayer=WorkflowRunReplayer()).execute(final_request)

        assert final.kind is SimulationDispatchResultIngressOutcomeKind.ADMITTED
        assert final.candidate_run is not None
        assert len(final.candidate_run.dispatch_observations) == 3
        assert final.candidate_run.dispatch_outcomes == (dispatch_record,)
        assert final.candidate_run.outcomes == (invocation,)
        assert final.candidate_run.obligation_dispositions == (disposition,)
        assert final.candidate_replay_result is not None
        assert final.candidate_replay_result.outcome.value == "equal"

        assert rejected.failure is not None
        unequal_observed_failure = replace(
            rejected.failure,
            identity=TaskInvocationFailureIdentity(
                "runtime-failure.unequal-observation.ingress"
            ),
        )
        unequal_observed_outcome = replace(
            rejected,
            failure=unequal_observed_failure,
        )
        final_observation_record = final_reconciliation.observation_record
        unequal_observation_record = replace(
            final_observation_record,
            observed_outcomes=(unequal_observed_outcome,),
        )
        unequal_observation_run = replace(
            final.candidate_run,
            dispatch_observations=tuple(
                sorted(
                    tuple(
                        value
                        for value in final.candidate_run.dispatch_observations
                        if value.identity != final_observation_record.identity
                    )
                    + (unequal_observation_record,),
                    key=lambda value: value.identity.value,
                )
            ),
        )
        unequal_replay = WorkflowRunReplayer().execute(
            unequal_observation_run, runtime_bundle
        )
        assert unequal_replay.outcome.value == "error"
        assert unequal_replay.issues[0].diagnostic == (
            "rejected dispatch must close over its request-bound failure"
        )

        second_rejected = replace(
            rejected,
            observation_identity=SimulationDispatchObservationIdentity(
                "dispatch-observation-envelope.rejected-again.ingress"
            ),
        )
        second_reconciliation = SimulationDispatchReconciler.execute(
            replace(
                final_reconciliation.request,
                observation_record_identity=DispatchObservationRecordIdentity(
                    "dispatch-observation.rejected-again.ingress"
                ),
                observations=(second_rejected,),
                reconciliation_identity_values=(
                    "reconciliation.rejected-again.ingress",
                ),
            )
        )
        assert final.candidate_run is not None
        second_final = SUT(replayer=WorkflowRunReplayer()).execute(
            replace(
                final_request,
                predecessor_run=final.candidate_run,
                reconciliation_result=second_reconciliation,
                next_revision_identity=WorkflowRunRevisionIdentity(
                    "revision.rejected-again.ingress"
                ),
            )
        )
        assert second_final.kind is SimulationDispatchResultIngressOutcomeKind.ERROR
        assert second_final.diagnostics == (
            "dispatch obligation already has a final outcome",
        )
