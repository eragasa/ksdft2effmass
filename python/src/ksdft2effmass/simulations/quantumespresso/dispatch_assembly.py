"""Effect-free assembly of one persisted Quantum ESPRESSO dispatch lifecycle."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import final

from ksdft2effmass.persistence import RevisionReadRequest, RevisionSelector
from ksdft2effmass.workflows import (
    AttemptIdentity,
    AuthorityReservationOutcomeIdentity,
    DispatchCreationIdempotencyIdentity,
    ResultDependency,
    ScientificExecutionGrantState,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizationRequest,
    SimulationExecutionRequestCorrelationIdentity,
    TaskActivation,
    TaskAttemptRecordIdentity,
    WorkflowRun,
    WorkflowRunCommitBinding,
    WorkflowRunLoadResult,
    WorkflowRunReplayer,
    WorkflowRunReplayOutcomeKind,
    WorkflowRunReplayResult,
    WorkflowRunRepository,
    WorkflowRunRevisionIdentity,
    WorkflowRuntimeBundle,
)
from ksdft2effmass.workflows.control.lifecycle import (
    SimulationDispatchControlRequest,
)
from ksdft2effmass.workflows.control.preparation import (
    SimulationDispatchPreparationRequest,
)

from .planning import QuantumEspressoExecution


class QuantumEspressoDispatchAssemblyOutcomeKind(StrEnum):
    """Closed outcomes of persisted dispatch-request assembly."""

    ASSEMBLED = "assembled"
    LOAD_FAILED = "load_failed"
    REPLAY_FAILED = "replay_failed"
    CORRELATION_FAILED = "correlation_failed"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoDispatchAssemblyRequest:
    """Supply exact non-authorizing inputs for one persisted lifecycle request.

    The manifest-derived execution contributes project and local-executor correlation
    only. The activation, verified authority requests, runtime bundle, persistence
    read expectations, record identities, and commit bindings are supplied separately;
    none is inferred from a development decision or manifest authority reference.
    """

    execution: QuantumEspressoExecution
    predecessor_read_request: RevisionReadRequest
    runtime_bundle: WorkflowRuntimeBundle
    activation: TaskActivation
    preparation_authorization_request: SimulationExecutionAuthorizationRequest
    claim_authorization_request: SimulationExecutionAuthorizationRequest
    prepared_revision_identity: WorkflowRunRevisionIdentity
    started_attempt_record_identity: TaskAttemptRecordIdentity
    request_correlation_identity: SimulationExecutionRequestCorrelationIdentity
    reservation_identity: AuthorityReservationOutcomeIdentity
    creation_idempotency_identity: DispatchCreationIdempotencyIdentity
    preparation_commit_binding: WorkflowRunCommitBinding
    claim_revision_identity: WorkflowRunRevisionIdentity
    claimed_reservation_identity: AuthorityReservationOutcomeIdentity
    claim_commit_binding: WorkflowRunCommitBinding
    input_dependencies: tuple[ResultDependency, ...] = ()
    retry_of_attempt_identity: AttemptIdentity | None = None

    def __post_init__(self) -> None:
        expected = (
            (self.execution, QuantumEspressoExecution, "execution"),
            (
                self.predecessor_read_request,
                RevisionReadRequest,
                "predecessor_read_request",
            ),
            (self.runtime_bundle, WorkflowRuntimeBundle, "runtime_bundle"),
            (self.activation, TaskActivation, "activation"),
            (
                self.preparation_authorization_request,
                SimulationExecutionAuthorizationRequest,
                "preparation_authorization_request",
            ),
            (
                self.claim_authorization_request,
                SimulationExecutionAuthorizationRequest,
                "claim_authorization_request",
            ),
            (
                self.prepared_revision_identity,
                WorkflowRunRevisionIdentity,
                "prepared_revision_identity",
            ),
            (
                self.started_attempt_record_identity,
                TaskAttemptRecordIdentity,
                "started_attempt_record_identity",
            ),
            (
                self.request_correlation_identity,
                SimulationExecutionRequestCorrelationIdentity,
                "request_correlation_identity",
            ),
            (
                self.reservation_identity,
                AuthorityReservationOutcomeIdentity,
                "reservation_identity",
            ),
            (
                self.creation_idempotency_identity,
                DispatchCreationIdempotencyIdentity,
                "creation_idempotency_identity",
            ),
            (
                self.preparation_commit_binding,
                WorkflowRunCommitBinding,
                "preparation_commit_binding",
            ),
            (
                self.claim_revision_identity,
                WorkflowRunRevisionIdentity,
                "claim_revision_identity",
            ),
            (
                self.claimed_reservation_identity,
                AuthorityReservationOutcomeIdentity,
                "claimed_reservation_identity",
            ),
            (
                self.claim_commit_binding,
                WorkflowRunCommitBinding,
                "claim_commit_binding",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.input_dependencies) is not tuple or any(
            type(value) is not ResultDependency for value in self.input_dependencies
        ):
            raise TypeError("input_dependencies must contain ResultDependency values")
        if self.input_dependencies != tuple(
            sorted(self.input_dependencies, key=lambda value: value.identity.value)
        ) or len({value.identity for value in self.input_dependencies}) != len(
            self.input_dependencies
        ):
            raise ValueError("input_dependencies must be unique and lexically sorted")
        if (
            self.retry_of_attempt_identity is not None
            and type(self.retry_of_attempt_identity) is not AttemptIdentity
        ):
            raise TypeError("retry_of_attempt_identity must be AttemptIdentity or None")
        read = self.predecessor_read_request
        if (
            read.selector is not RevisionSelector.EXPLICIT_REVISION
            or read.revision_id is None
            or read.expected_schema_id is None
            or read.expected_content_id is None
            or read.expected_idempotency_id is None
        ):
            raise ValueError(
                "predecessor read must select one revision with complete expectations"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoDispatchAssemblyResult:
    """Record one assembled control request or one closed no-effect failure."""

    kind: QuantumEspressoDispatchAssemblyOutcomeKind
    request: QuantumEspressoDispatchAssemblyRequest
    load_result: WorkflowRunLoadResult
    replay_result: WorkflowRunReplayResult | None
    control_request: SimulationDispatchControlRequest | None
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.kind) is not QuantumEspressoDispatchAssemblyOutcomeKind:
            raise TypeError("kind must be QuantumEspressoDispatchAssemblyOutcomeKind")
        if type(self.request) is not QuantumEspressoDispatchAssemblyRequest:
            raise TypeError("request must be QuantumEspressoDispatchAssemblyRequest")
        if type(self.load_result) is not WorkflowRunLoadResult:
            raise TypeError("load_result must be WorkflowRunLoadResult")
        if self.replay_result is not None and type(self.replay_result) is not (
            WorkflowRunReplayResult
        ):
            raise TypeError("replay_result must be WorkflowRunReplayResult or None")
        if self.control_request is not None and type(self.control_request) is not (
            SimulationDispatchControlRequest
        ):
            raise TypeError(
                "control_request must be SimulationDispatchControlRequest or None"
            )
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must contain strings")
        if any(not value for value in self.diagnostics) or len(
            set(self.diagnostics)
        ) != len(self.diagnostics):
            raise ValueError("diagnostics must be nonempty when present and unique")
        if self.kind is QuantumEspressoDispatchAssemblyOutcomeKind.ASSEMBLED:
            if (
                self.load_result.status != "loaded"
                or self.replay_result is None
                or self.replay_result.outcome is not WorkflowRunReplayOutcomeKind.EQUAL
                or self.control_request is None
                or self.diagnostics
            ):
                raise ValueError(
                    "assembled result requires loaded replay-equal control request"
                )
        elif self.control_request is not None or not self.diagnostics:
            raise ValueError(
                "failed assembly prohibits control request and requires diagnostics"
            )
        elif (
            self.kind is QuantumEspressoDispatchAssemblyOutcomeKind.LOAD_FAILED
            and self.replay_result is not None
        ):
            raise ValueError("load failure prohibits a replay result")
        elif (
            self.kind
            in {
                QuantumEspressoDispatchAssemblyOutcomeKind.REPLAY_FAILED,
                QuantumEspressoDispatchAssemblyOutcomeKind.CORRELATION_FAILED,
            }
            and self.replay_result is None
        ):
            raise ValueError("post-load failure requires a replay result")


@dataclass(frozen=True, slots=True)
@final
class QuantumEspressoDispatchAssembler:
    """Load, replay, correlate, and assemble one no-effect dispatch request."""

    repository: WorkflowRunRepository

    def __post_init__(self) -> None:
        if not isinstance(self.repository, WorkflowRunRepository):
            raise TypeError("repository must implement WorkflowRunRepository")

    def execute(
        self, request: QuantumEspressoDispatchAssemblyRequest
    ) -> QuantumEspressoDispatchAssemblyResult:
        """Return an exact control request only from replay-equal correlated state."""
        if type(request) is not QuantumEspressoDispatchAssemblyRequest:
            raise TypeError("request must be QuantumEspressoDispatchAssemblyRequest")
        loaded = self.repository.load(request.predecessor_read_request)
        if loaded.status != "loaded" or loaded.snapshot is None:
            return self._failure(
                request,
                loaded,
                QuantumEspressoDispatchAssemblyOutcomeKind.LOAD_FAILED,
                None,
                "exact predecessor could not be loaded",
            )
        snapshot = loaded.snapshot
        replay = WorkflowRunReplayer().execute(snapshot.run, request.runtime_bundle)
        if replay.outcome is not WorkflowRunReplayOutcomeKind.EQUAL:
            return self._failure(
                request,
                loaded,
                QuantumEspressoDispatchAssemblyOutcomeKind.REPLAY_FAILED,
                replay,
                "persisted predecessor is not replay equal",
            )
        issue = self._correlation_issue(request, snapshot.run)
        if issue is not None:
            return self._failure(
                request,
                loaded,
                QuantumEspressoDispatchAssemblyOutcomeKind.CORRELATION_FAILED,
                replay,
                issue,
            )
        preparation = SimulationDispatchPreparationRequest(
            predecessor_run=snapshot.run,
            runtime_bundle=request.runtime_bundle,
            activation=request.activation,
            authorization_request=request.preparation_authorization_request,
            next_revision_identity=request.prepared_revision_identity,
            started_attempt_record_identity=request.started_attempt_record_identity,
            request_correlation_identity=request.request_correlation_identity,
            reservation_identity=request.reservation_identity,
            creation_idempotency_identity=request.creation_idempotency_identity,
            input_dependencies=request.input_dependencies,
            retry_of_attempt_identity=request.retry_of_attempt_identity,
        )
        local = request.execution.local_execution_plan
        control = SimulationDispatchControlRequest(
            preparation_request=preparation,
            preparation_commit_binding=request.preparation_commit_binding,
            claim_authorization_request=request.claim_authorization_request,
            claim_revision_identity=request.claim_revision_identity,
            claimed_reservation_identity=request.claimed_reservation_identity,
            claim_commit_binding=request.claim_commit_binding,
            dispatch_outcome_identity=local.dispatch_outcome_identity,
            dispatch_entry_identity=local.dispatch_entry_identity,
            dispatch_entry_revision_identity=local.dispatch_entry_revision_identity,
        )
        return QuantumEspressoDispatchAssemblyResult(
            kind=QuantumEspressoDispatchAssemblyOutcomeKind.ASSEMBLED,
            request=request,
            load_result=loaded,
            replay_result=replay,
            control_request=control,
            diagnostics=(),
        )

    @staticmethod
    def _correlation_issue(
        request: QuantumEspressoDispatchAssemblyRequest,
        loaded_run: WorkflowRun,
    ) -> str | None:
        """Return the first manifest, activation, authority, or load mismatch."""
        if type(loaded_run) is not WorkflowRun:
            raise TypeError("loaded_run must be WorkflowRun")
        local = request.execution.local_execution_plan
        preparation = local.preparation_request
        execution_input = preparation.execution_input
        activation = request.activation
        prepare = request.preparation_authorization_request
        claim = request.claim_authorization_request
        if (
            loaded_run.identity != local.workflow_run_identity
            or request.predecessor_read_request.stream_id
            != local.workflow_run_identity.value
        ):
            return "persisted WorkflowRun identity differs from the local plan"
        if activation.task_instance not in loaded_run.task_instances:
            return "activation Task instance is absent from the persisted predecessor"
        if (
            activation.workflow_run_identity != local.workflow_run_identity
            or activation.identity != execution_input.activation_identity
            or activation.task_instance.identity
            != execution_input.task_instance_identity
            or activation.task_instance.definition_identity
            != execution_input.task_definition_identity
            or activation.operation_identity != execution_input.operation_identity
            or activation.attempt_identity != execution_input.attempt_identity
        ):
            return "activation differs from the QE execution input"
        if (
            prepare.phase is not SimulationExecutionAuthorizationPhase.PREPARATION
            or prepare.grant.state is not ScientificExecutionGrantState.UNUSED
            or claim.phase is not SimulationExecutionAuthorizationPhase.CLAIM
            or claim.grant.state is not ScientificExecutionGrantState.RESERVED
        ):
            return "authority requests do not represent unused then reserved phases"
        expected_resources = (preparation.dispatch_resource_scope_identity,)
        for authorization in (prepare, claim):
            if (
                authorization.workflow_run_identity != local.workflow_run_identity
                or authorization.task_definition_identity
                != execution_input.task_definition_identity
                or authorization.task_instance_identity
                != execution_input.task_instance_identity
                or authorization.activation_identity
                != execution_input.activation_identity
                or authorization.operation_identity
                != execution_input.operation_identity
                or authorization.attempt_identity != execution_input.attempt_identity
                or authorization.executor_identity
                != preparation.scientific_executor_identity
                or authorization.destination_identity
                != preparation.dispatch_destination_identity
                or authorization.resource_scope_identities != expected_resources
                or authorization.obligation_identity != local.obligation_identity
                or authorization.input_result_reference_identities
                != local.input_result_reference_identities
                or authorization.input_artifact_entry_identities
                != local.input_artifact_entry_identities
                or authorization.grant.authority_reference
                != local.grant_authority_reference
            ):
                return "authority request scope differs from the local execution plan"
        if (
            prepare.request_identity
            != preparation.simulation_execution_request_identity
            or prepare.result_identity != preparation.authorization_result_identity
            or claim.request_identity != prepare.request_identity
            or claim.result_identity != local.claim_authorization_result_identity
            or not claim.grant.is_reserved_successor_of(
                prepare.grant, local.obligation_identity
            )
        ):
            return "authority lifecycle identities differ from the local plan"
        return None

    @staticmethod
    def _failure(
        request: QuantumEspressoDispatchAssemblyRequest,
        loaded: WorkflowRunLoadResult,
        kind: QuantumEspressoDispatchAssemblyOutcomeKind,
        replay: WorkflowRunReplayResult | None,
        diagnostic: str,
    ) -> QuantumEspressoDispatchAssemblyResult:
        """Construct one closed no-effect assembly failure."""
        return QuantumEspressoDispatchAssemblyResult(
            kind=kind,
            request=request,
            load_result=loaded,
            replay_result=replay,
            control_request=None,
            diagnostics=(diagnostic,),
        )
