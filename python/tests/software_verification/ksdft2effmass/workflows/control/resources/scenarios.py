"""Synthetic software-control scenarios for control-ingress verification."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from ksdft2effmass.workflows import (
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    AttemptIdentity,
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeIdentity,
    AuthorityReservationOutcomeKind,
    DispatchCreationIdempotencyIdentity,
    DispatchDestinationIdentity,
    DispatchOutcomeKind,
    DispatchResourceScopeIdentity,
    ExecutionGrantIdentity,
    ExecutionGrantRevisionIdentity,
    ObligationIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    ResultObjectReferenceIdentity,
    ScientificExecutionAuthorityGrant,
    ScientificExecutionAuthorityReference,
    ScientificExecutionAuthoritySnapshot,
    ScientificExecutionAuthoritySnapshotIdentity,
    ScientificExecutionAuthorityStateIdentity,
    ScientificExecutionAuthorityVerificationKind,
    ScientificExecutionGrantState,
    ScientificExecutorIdentity,
    SimulationDispatchEffectRequest,
    SimulationDispatchEntryIdentity,
    SimulationDispatchEntryOutcomeKind,
    SimulationDispatchEntryReceipt,
    SimulationDispatchEntryReceiptIdentity,
    SimulationDispatchEntryResult,
    SimulationDispatchObligation,
    SimulationDispatchObservationIdentity,
    SimulationDispatchOutcome,
    SimulationDispatchOutcomeIdentity,
    SimulationDispatchRequest,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizationRequest,
    SimulationExecutionAuthorizationResult,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionAuthorizer,
    SimulationExecutionRequest,
    SimulationExecutionRequestCorrelation,
    SimulationExecutionRequestCorrelationIdentity,
    SimulationExecutionRequestIdentity,
    TaskActivationIdentity,
    TaskAttemptRecordIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
    TaskInvocationFailure,
    TaskInvocationFailureIdentity,
    WorkflowRunClaimCommitReceipt,
    WorkflowRunClaimCommitReceiptIdentity,
    WorkflowRunIdentity,
    WorkflowRunRevisionIdentity,
)


@dataclass(frozen=True, slots=True)
class SyntheticControlResult:
    """Minimal immutable ResultObject used only by software verification."""

    identity: ResultObjectIdentity


class RecordingSimulationDispatchEntryCommitter:
    """Provide a synthetic durable one-winner dispatch-entry boundary."""

    def __init__(self) -> None:
        """Start with no entered dispatch identities."""
        self._entered: set[SimulationDispatchEntryIdentity] = set()

    def execute(
        self, request: SimulationDispatchRequest
    ) -> SimulationDispatchEntryResult:
        """Return a receipt only to the first call for one dispatch entry."""
        identity = request.dispatch_entry_identity
        if identity in self._entered:
            return SimulationDispatchEntryResult(
                kind=SimulationDispatchEntryOutcomeKind.ALREADY_ENTERED,
                request=request,
                receipt=None,
                diagnostics=("dispatch entry was already committed",),
            )
        self._entered.add(identity)
        return SimulationDispatchEntryResult(
            kind=SimulationDispatchEntryOutcomeKind.ENTERED,
            request=request,
            receipt=ControlScenarioFactory.dispatch_entry_receipt(request),
            diagnostics=(),
        )


class RecordingSimulationDispatchEffect:
    """Record calls to one exact synthetic dispatch effect."""

    def __init__(
        self,
        *,
        executor_identity: ScientificExecutorIdentity,
        outcome: SimulationDispatchOutcome | None,
        raises: bool = False,
    ) -> None:
        """Configure the exact executor, returned outcome, and exception behavior."""
        self._executor_identity = executor_identity
        self._outcome = outcome
        self._raises = raises
        self._call_count = 0

    @property
    def executor_identity(self) -> ScientificExecutorIdentity:
        """Return the exact executor identity accepted by this fake."""
        return self._executor_identity

    @property
    def call_count(self) -> int:
        """Return the number of effect-port entries."""
        return self._call_count

    def execute(
        self,
        request: SimulationDispatchEffectRequest,
    ) -> SimulationDispatchOutcome:
        """Record one call and return the configured outcome or raise."""
        self._call_count += 1
        if self._raises:
            raise RuntimeError("synthetic effect failure")
        if self._outcome is None:
            raise RuntimeError("synthetic outcome is absent")
        return self._outcome


class ControlScenarioFactory:
    """Construct one hand-inspectable exact control-ingress scenario."""

    @staticmethod
    def instant(hour: int) -> datetime:
        """Return one UTC instant on the fixed synthetic scenario date."""
        return datetime(2026, 1, 1, hour, tzinfo=UTC)

    @classmethod
    def snapshot(
        cls,
        *,
        verification: ScientificExecutionAuthorityVerificationKind = (
            ScientificExecutionAuthorityVerificationKind.VERIFIED
        ),
    ) -> ScientificExecutionAuthoritySnapshot:
        """Return one synthetic authority snapshot."""
        return ScientificExecutionAuthoritySnapshot(
            identity=ScientificExecutionAuthoritySnapshotIdentity("snapshot.one"),
            source_identity="authority-source.one",
            issuer_identity="issuer.one",
            trust_configuration_identity="trust-config.one",
            content_verification_identity="content-check.one",
            authentication_verification_identity="authentication-check.one",
            predecessor_closure_identity="predecessor-check.one",
            revocation_closure_identity="revocation-check.one",
            content_verification=verification,
            authentication_verification=verification,
            predecessor_closure=verification,
            revocation_closure=verification,
            valid_from=cls.instant(0),
            valid_until=cls.instant(4),
            verified_at=cls.instant(1),
            fresh_until=cls.instant(3),
            resolver_implementation_identity="synthetic-authority-resolver.v1",
        )

    @staticmethod
    def authority_reference() -> ScientificExecutionAuthorityReference:
        """Return one exact authority reference shared by the scenario."""
        return ScientificExecutionAuthorityReference(
            grant_identity=ExecutionGrantIdentity("grant.one"),
            grant_revision_identity=ExecutionGrantRevisionIdentity(
                "grant-revision.one"
            ),
            snapshot_identity=ScientificExecutionAuthoritySnapshotIdentity(
                "snapshot.one"
            ),
            state_identity=ScientificExecutionAuthorityStateIdentity("grant-state.one"),
        )

    @classmethod
    def grant(
        cls,
        *,
        state: ScientificExecutionGrantState,
        input_result_reference_identities: tuple[ResultObjectReferenceIdentity, ...] = (
            ResultObjectReferenceIdentity("result-input.one"),
        ),
    ) -> ScientificExecutionAuthorityGrant:
        """Return one exact grant in the requested lifecycle state."""
        obligation = (
            None
            if state is ScientificExecutionGrantState.UNUSED
            else ObligationIdentity("obligation.one")
        )
        return ScientificExecutionAuthorityGrant(
            authority_reference=cls.authority_reference(),
            authority_source_identity="authority-source.one",
            issuer_identity="issuer.one",
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            task_definition_identity=TaskDefinitionIdentity("task.simulation.one"),
            task_instance_identity=TaskInstanceIdentity("task-instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            destination_identity=DispatchDestinationIdentity("destination.local"),
            resource_scope_identities=(
                DispatchResourceScopeIdentity("resource.cpu.one"),
            ),
            input_result_reference_identities=input_result_reference_identities,
            input_artifact_entry_identities=(
                ArtifactManifestEntryIdentity("artifact-input.one"),
            ),
            valid_from=cls.instant(0),
            valid_until=cls.instant(4),
            state=state,
            reserved_obligation_identity=obligation,
        )

    @classmethod
    def authorization_request(
        cls,
        *,
        phase: SimulationExecutionAuthorizationPhase,
        state: ScientificExecutionGrantState,
        result_identity: str,
        snapshot: ScientificExecutionAuthoritySnapshot | None = None,
        input_result_reference_identities: tuple[ResultObjectReferenceIdentity, ...] = (
            ResultObjectReferenceIdentity("result-input.one"),
        ),
    ) -> SimulationExecutionAuthorizationRequest:
        """Return one exact preparation- or claim-phase authorization request."""
        return SimulationExecutionAuthorizationRequest(
            result_identity=SimulationExecutionAuthorizationResultIdentity(
                result_identity
            ),
            phase=phase,
            grant=cls.grant(
                state=state,
                input_result_reference_identities=input_result_reference_identities,
            ),
            snapshot=cls.snapshot() if snapshot is None else snapshot,
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            task_definition_identity=TaskDefinitionIdentity("task.simulation.one"),
            task_instance_identity=TaskInstanceIdentity("task-instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            destination_identity=DispatchDestinationIdentity("destination.local"),
            obligation_identity=ObligationIdentity("obligation.one"),
            resource_scope_identities=(
                DispatchResourceScopeIdentity("resource.cpu.one"),
            ),
            input_result_reference_identities=input_result_reference_identities,
            input_artifact_entry_identities=(
                ArtifactManifestEntryIdentity("artifact-input.one"),
            ),
            evaluated_at=cls.instant(2),
        )

    @classmethod
    def preparation_authorization(cls) -> SimulationExecutionAuthorizationResult:
        """Return one authorized preparation-phase result."""
        return SimulationExecutionAuthorizer.execute(
            cls.authorization_request(
                phase=SimulationExecutionAuthorizationPhase.PREPARATION,
                state=ScientificExecutionGrantState.UNUSED,
                result_identity="authorization.prepare",
            )
        )

    @classmethod
    def execution_request(cls) -> SimulationExecutionRequest:
        """Return one prepared simulation execution request."""
        authorization = cls.preparation_authorization()
        correlation = SimulationExecutionRequestCorrelation(
            identity=SimulationExecutionRequestCorrelationIdentity(
                "request-correlation.one"
            ),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            task_instance_identity=TaskInstanceIdentity("task-instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            attempt_record_identity=TaskAttemptRecordIdentity("attempt.one.started"),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            obligation_identity=ObligationIdentity("obligation.one"),
            grant_identity=ExecutionGrantIdentity("grant.one"),
            authorization_result_identity=authorization.identity,
            input_result_reference_identities=(
                ResultObjectReferenceIdentity("result-input.one"),
            ),
            input_artifact_entry_identities=(
                ArtifactManifestEntryIdentity("artifact-input.one"),
            ),
        )
        obligation = SimulationDispatchObligation(
            identity=ObligationIdentity("obligation.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            workflow_run_revision_identity=WorkflowRunRevisionIdentity(
                "revision.prepared"
            ),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            task_instance_identity=TaskInstanceIdentity("task-instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            grant_identity=ExecutionGrantIdentity("grant.one"),
            destination_identity=DispatchDestinationIdentity("destination.local"),
            resource_scope_identities=(
                DispatchResourceScopeIdentity("resource.cpu.one"),
            ),
            creation_idempotency_identity=DispatchCreationIdempotencyIdentity(
                "dispatch-create.one"
            ),
        )
        return SimulationExecutionRequest(
            correlation=correlation,
            obligation=obligation,
            preparation_authorization=authorization,
        )

    @classmethod
    def claim_authorization_request(
        cls,
    ) -> SimulationExecutionAuthorizationRequest:
        """Return the immediate reserved-grant authorization request."""
        return cls.authorization_request(
            phase=SimulationExecutionAuthorizationPhase.CLAIM,
            state=ScientificExecutionGrantState.RESERVED,
            result_identity="authorization.claim",
        )

    @classmethod
    def claimed_reservation(cls) -> AuthorityReservationOutcome:
        """Return one represented successful claim record."""
        return AuthorityReservationOutcome(
            identity=AuthorityReservationOutcomeIdentity("claim.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            workflow_run_revision_identity=WorkflowRunRevisionIdentity(
                "revision.claimed"
            ),
            authority_reference=cls.authority_reference(),
            authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity("authorization.claim")
            ),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            attempt_record_identity=TaskAttemptRecordIdentity("attempt.one.started"),
            obligation_identity=ObligationIdentity("obligation.one"),
            expected_revision_identity=WorkflowRunRevisionIdentity("revision.prepared"),
            kind=AuthorityReservationOutcomeKind.CLAIMED,
            predecessor_reservation_identity=AuthorityReservationOutcomeIdentity(
                "reservation.one"
            ),
        )

    @classmethod
    def claim_commit_receipt(cls) -> WorkflowRunClaimCommitReceipt:
        """Return typed evidence for the exact committed claimed revision."""
        return WorkflowRunClaimCommitReceipt(
            identity=WorkflowRunClaimCommitReceiptIdentity("claim-receipt.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            committed_revision_identity=WorkflowRunRevisionIdentity("revision.claimed"),
            predecessor_revision_identity=WorkflowRunRevisionIdentity(
                "revision.prepared"
            ),
            claimed_reservation_identity=AuthorityReservationOutcomeIdentity(
                "claim.one"
            ),
            claim_authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity("authorization.claim")
            ),
            workflow_run_content_identity="claimed-run-content.one",
            persistence_operation_identity="commit-operation.one",
            commit_idempotency_identity="claim-commit.one",
            persistence_implementation_identity="synthetic-persistence.v1",
        )

    @classmethod
    def dispatch_request(cls) -> SimulationDispatchRequest:
        """Return one exact already-claimed dispatch request."""
        return SimulationDispatchRequest(
            execution_request=cls.execution_request(),
            claim_authorization_request=cls.claim_authorization_request(),
            claimed_reservation=cls.claimed_reservation(),
            claim_commit_receipt=cls.claim_commit_receipt(),
            outcome_identity=SimulationDispatchOutcomeIdentity("outcome.one"),
            dispatch_entry_identity=SimulationDispatchEntryIdentity("entry.one"),
            dispatch_entry_revision_identity=WorkflowRunRevisionIdentity(
                "revision.dispatch-entered"
            ),
        )

    @staticmethod
    def dispatch_entry_receipt(
        request: SimulationDispatchRequest,
    ) -> SimulationDispatchEntryReceipt:
        """Return synthetic persistence evidence for a newly won dispatch entry."""
        return SimulationDispatchEntryReceipt(
            identity=SimulationDispatchEntryReceiptIdentity("entry-receipt.one"),
            dispatch_entry_identity=request.dispatch_entry_identity,
            workflow_run_identity=(
                request.execution_request.correlation.workflow_run_identity
            ),
            claim_commit_receipt_identity=request.claim_commit_receipt.identity,
            predecessor_revision_identity=(
                request.claim_commit_receipt.committed_revision_identity
            ),
            committed_revision_identity=request.dispatch_entry_revision_identity,
            claimed_reservation_identity=request.claimed_reservation.identity,
            obligation_identity=request.execution_request.obligation.identity,
            outcome_identity=request.outcome_identity,
            workflow_run_content_identity="dispatch-entered-content.one",
            persistence_operation_identity="dispatch-entry-cas.one",
            persistence_implementation_identity="synthetic-persistence.v1",
        )

    @staticmethod
    def outcome(
        *,
        kind: DispatchOutcomeKind = DispatchOutcomeKind.CONFIRMED,
    ) -> SimulationDispatchOutcome:
        """Return one runtime outcome for the fixed scenario."""
        if kind is DispatchOutcomeKind.CONFIRMED:
            return SimulationDispatchOutcome(
                identity=SimulationDispatchOutcomeIdentity("outcome.one"),
                observation_identity=SimulationDispatchObservationIdentity(
                    "observation.confirmed.one"
                ),
                request_identity=SimulationExecutionRequestIdentity("request.one"),
                workflow_run_identity=WorkflowRunIdentity("run.one"),
                task_instance_identity=TaskInstanceIdentity("task-instance.one"),
                activation_identity=TaskActivationIdentity("activation.one"),
                operation_identity=OperationIdentity("operation.one"),
                attempt_identity=AttemptIdentity("attempt.one"),
                executor_identity=ScientificExecutorIdentity("executor.one"),
                obligation_identity=ObligationIdentity("obligation.one"),
                grant_identity=ExecutionGrantIdentity("grant.one"),
                kind=kind,
                result=SyntheticControlResult(ResultObjectIdentity("result.one")),
                native_output_manifest_identity=ArtifactManifestIdentity(
                    "manifest.one"
                ),
                native_output_manifest_entry_identities=(
                    ArtifactManifestEntryIdentity("manifest-entry.one"),
                ),
            )
        if kind is DispatchOutcomeKind.REJECTED:
            return SimulationDispatchOutcome(
                identity=SimulationDispatchOutcomeIdentity("outcome.one"),
                observation_identity=SimulationDispatchObservationIdentity(
                    "observation.rejected.one"
                ),
                request_identity=SimulationExecutionRequestIdentity("request.one"),
                workflow_run_identity=WorkflowRunIdentity("run.one"),
                task_instance_identity=TaskInstanceIdentity("task-instance.one"),
                activation_identity=TaskActivationIdentity("activation.one"),
                operation_identity=OperationIdentity("operation.one"),
                attempt_identity=AttemptIdentity("attempt.one"),
                executor_identity=ScientificExecutorIdentity("executor.one"),
                obligation_identity=ObligationIdentity("obligation.one"),
                grant_identity=ExecutionGrantIdentity("grant.one"),
                kind=kind,
                failure=TaskInvocationFailure(
                    identity=TaskInvocationFailureIdentity("failure.one"),
                    code="synthetic.rejected",
                    operation_phase="execution",
                    diagnostic="synthetic executor rejected the request",
                    retryable=False,
                    claim_boundary=("synthetic software verification only",),
                ),
            )
        return SimulationDispatchOutcome(
            identity=SimulationDispatchOutcomeIdentity("outcome.one"),
            observation_identity=SimulationDispatchObservationIdentity(
                "observation.indeterminate.one"
            ),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            task_instance_identity=TaskInstanceIdentity("task-instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            obligation_identity=ObligationIdentity("obligation.one"),
            grant_identity=ExecutionGrantIdentity("grant.one"),
            kind=kind,
            reconciliation_identity_values=("observation.one",),
        )
