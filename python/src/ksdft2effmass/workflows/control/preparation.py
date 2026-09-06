"""Effect-free preparation of one simulation dispatch successor candidate.

The preparer verifies deterministic replay of an exact predecessor, evaluates
preparation-phase authority, and constructs one complete candidate containing the
activation, started attempt, closed authorization result, authority reference,
request correlation, reservation, input dependencies, and durable obligation.  It
replays the candidate before returning it.  It performs no persistence, compare-and-
swap claim, effect, retry selection, result ingress, or scientific acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from typing import final

from ..model import AttemptIdentity, TaskActivation
from ..runs.aggregate import WorkflowRun
from ..runs.authority import (
    SimulationExecutionAuthorizationOutcomeKind,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizationRequest,
    SimulationExecutionAuthorizationResult,
)
from ..runs.identities import (
    AuthorityReservationOutcomeIdentity,
    DispatchCreationIdempotencyIdentity,
    SimulationExecutionRequestCorrelationIdentity,
    TaskAttemptRecordIdentity,
    WorkflowRunRevisionIdentity,
)
from ..runs.records import (
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeKind,
    ResultDependency,
    SimulationDispatchObligation,
    SimulationExecutionRequestCorrelation,
    TaskAttempt,
    TaskAttemptStatus,
)
from ..runs.replay import (
    WorkflowRunReplayer,
    WorkflowRunReplayOutcomeKind,
    WorkflowRunReplayResult,
    WorkflowRuntimeBundle,
)
from .authority import SimulationExecutionAuthorizer


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchPreparationRequest:
    """Request one deterministic pending-dispatch WorkflowRun candidate.

    Parameters
    ----------
    predecessor_run, runtime_bundle
        Exact predecessor and explicit runtime dependencies used for replay.
    activation
        New exact Task activation to append with its started attempt.
    authorization_request
        Preparation-phase authorization request for the same activation and run.
    next_revision_identity
        Caller-supplied successor revision identity.
    started_attempt_record_identity
        Caller-supplied identity for the initial started attempt-state record.
    request_correlation_identity, reservation_identity
        Caller-supplied identities for the request and reserved-authority records.
    creation_idempotency_identity
        Exact durable-obligation creation idempotency identity.
    input_dependencies
        Exact dependencies admitting every activation input.  The tuple is empty for
        an input-free Task and otherwise is supplied in lexical identity order.
    retry_of_attempt_identity
        Earlier terminal attempt retried by this new activation, otherwise ``None``.
    """

    predecessor_run: WorkflowRun
    runtime_bundle: WorkflowRuntimeBundle
    activation: TaskActivation
    authorization_request: SimulationExecutionAuthorizationRequest
    next_revision_identity: WorkflowRunRevisionIdentity
    started_attempt_record_identity: TaskAttemptRecordIdentity
    request_correlation_identity: SimulationExecutionRequestCorrelationIdentity
    reservation_identity: AuthorityReservationOutcomeIdentity
    creation_idempotency_identity: DispatchCreationIdempotencyIdentity
    input_dependencies: tuple[ResultDependency, ...] = ()
    retry_of_attempt_identity: AttemptIdentity | None = None

    def __post_init__(self) -> None:
        """Validate exact field types and canonical dependency ordering."""
        expected = (
            (self.predecessor_run, WorkflowRun, "predecessor_run"),
            (self.runtime_bundle, WorkflowRuntimeBundle, "runtime_bundle"),
            (self.activation, TaskActivation, "activation"),
            (
                self.authorization_request,
                SimulationExecutionAuthorizationRequest,
                "authorization_request",
            ),
            (
                self.next_revision_identity,
                WorkflowRunRevisionIdentity,
                "next_revision_identity",
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
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.input_dependencies) is not tuple or any(
            type(value) is not ResultDependency for value in self.input_dependencies
        ):
            raise TypeError("input_dependencies must be a tuple of ResultDependency")
        if self.input_dependencies != tuple(
            sorted(self.input_dependencies, key=lambda value: value.identity.value)
        ) or len({value.identity for value in self.input_dependencies}) != len(
            self.input_dependencies
        ):
            raise ValueError("input_dependencies must be unique and lexically sorted")
        if len({value.input_name for value in self.input_dependencies}) != len(
            self.input_dependencies
        ):
            raise ValueError(
                "input_dependencies must contain at most one record per input name"
            )
        retry = self.retry_of_attempt_identity
        if retry is not None and type(retry) is not AttemptIdentity:
            raise TypeError("retry_of_attempt_identity must be AttemptIdentity or None")


class SimulationDispatchPreparationOutcomeKind(StrEnum):
    """Closed outcome of effect-free dispatch preparation."""

    PREPARED = "prepared"
    DENIED = "denied"
    ERROR = "error"


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchPreparationResult:
    """Record a prepared candidate, authority denial, or preparation error.

    Parameters
    ----------
    kind
        Prepared, denied, or error outcome.
    request
        Exact preparation request.
    authorization_result
        Closed authorization result when authorization was reached; otherwise
        ``None`` for predecessor replay failure.
    predecessor_replay_result
        Exact replay result for the predecessor.
    candidate_run, candidate_replay_result
        Exact candidate and its equal replay result for ``prepared`` only.  On a
        candidate replay error, only ``candidate_replay_result`` is retained.
    diagnostics
        Empty for ``prepared`` and nonempty sanitized statements otherwise.
    """

    kind: SimulationDispatchPreparationOutcomeKind
    request: SimulationDispatchPreparationRequest
    authorization_result: SimulationExecutionAuthorizationResult | None
    predecessor_replay_result: WorkflowRunReplayResult
    candidate_run: WorkflowRun | None
    candidate_replay_result: WorkflowRunReplayResult | None
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact result types and closed outcome variants."""
        if type(self.kind) is not SimulationDispatchPreparationOutcomeKind:
            raise TypeError("kind must be SimulationDispatchPreparationOutcomeKind")
        if type(self.request) is not SimulationDispatchPreparationRequest:
            raise TypeError("request must be SimulationDispatchPreparationRequest")
        if (
            self.authorization_result is not None
            and type(self.authorization_result)
            is not SimulationExecutionAuthorizationResult
        ):
            raise TypeError(
                "authorization_result must be "
                "SimulationExecutionAuthorizationResult or None"
            )
        if type(self.predecessor_replay_result) is not WorkflowRunReplayResult:
            raise TypeError("predecessor_replay_result must be WorkflowRunReplayResult")
        if (
            self.candidate_run is not None
            and type(self.candidate_run) is not WorkflowRun
        ):
            raise TypeError("candidate_run must be WorkflowRun or None")
        if (
            self.candidate_replay_result is not None
            and type(self.candidate_replay_result) is not WorkflowRunReplayResult
        ):
            raise TypeError(
                "candidate_replay_result must be WorkflowRunReplayResult or None"
            )
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of strings")
        if any(not value for value in self.diagnostics):
            raise ValueError("diagnostics must not contain empty strings")
        if len(set(self.diagnostics)) != len(self.diagnostics):
            raise ValueError("diagnostics must not contain duplicates")
        predecessor = self.request.predecessor_run
        if (
            self.predecessor_replay_result.workflow_run_identity != predecessor.identity
            or self.predecessor_replay_result.revision_identity
            != predecessor.revision_identity
            or self.predecessor_replay_result.runtime_bundle_identity
            != self.request.runtime_bundle.identity
        ):
            raise ValueError(
                "predecessor replay result must identify the requested predecessor"
            )
        if self.candidate_replay_result is not None and (
            self.candidate_replay_result.workflow_run_identity != predecessor.identity
            or self.candidate_replay_result.revision_identity
            != self.request.next_revision_identity
            or self.candidate_replay_result.runtime_bundle_identity
            != self.request.runtime_bundle.identity
        ):
            raise ValueError(
                "candidate replay result must identify the requested successor"
            )
        prepared = self.kind is SimulationDispatchPreparationOutcomeKind.PREPARED
        if prepared:
            if (
                self.authorization_result is None
                or self.authorization_result.kind
                is not SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
                or self.predecessor_replay_result.outcome
                is not WorkflowRunReplayOutcomeKind.EQUAL
                or self.candidate_run is None
                or self.candidate_replay_result is None
                or self.candidate_replay_result.outcome
                is not WorkflowRunReplayOutcomeKind.EQUAL
                or self.diagnostics
            ):
                raise ValueError(
                    "prepared result requires two equal replays and candidate"
                )
            return
        if self.candidate_run is not None or not self.diagnostics:
            raise ValueError(
                "denied and error results prohibit candidate and require diagnostics"
            )
        if self.kind is SimulationDispatchPreparationOutcomeKind.DENIED:
            if (
                self.authorization_result is None
                or self.authorization_result.kind
                is not SimulationExecutionAuthorizationOutcomeKind.DENIED
                or self.candidate_replay_result is not None
            ):
                raise ValueError("denied result requires one denied authorization")


@dataclass(frozen=True, slots=True)
@final
class SimulationDispatchPreparer:
    """Construct and replay one effect-free pending-dispatch successor candidate.

    Parameters
    ----------
    authorizer
        Exact effect-free authorization ActionObject.
    replayer
        Exact deterministic WorkflowRun replay ActionObject.
    """

    authorizer: SimulationExecutionAuthorizer
    replayer: WorkflowRunReplayer

    def __post_init__(self) -> None:
        """Validate exact injected ActionObjects."""
        if type(self.authorizer) is not SimulationExecutionAuthorizer:
            raise TypeError("authorizer must be SimulationExecutionAuthorizer")
        if type(self.replayer) is not WorkflowRunReplayer:
            raise TypeError("replayer must be WorkflowRunReplayer")

    def execute(
        self,
        request: SimulationDispatchPreparationRequest,
    ) -> SimulationDispatchPreparationResult:
        """Replay, authorize, construct, and replay one candidate.

        Parameters
        ----------
        request
            Exact predecessor, runtime bundle, activation, authorization inputs, and
            caller-supplied record identities.

        Returns
        -------
        SimulationDispatchPreparationResult
            Closed prepared, denied, or error result.  No result performs persistence
            or an external effect.

        Raises
        ------
        TypeError
            If ``request`` is not the exact request DataObject.
        """
        if type(request) is not SimulationDispatchPreparationRequest:
            raise TypeError("request must be SimulationDispatchPreparationRequest")
        predecessor_replay = self.replayer.execute(
            request.predecessor_run, request.runtime_bundle
        )
        if predecessor_replay.outcome is not WorkflowRunReplayOutcomeKind.EQUAL:
            return self._error(
                request,
                predecessor_replay,
                None,
                None,
                "predecessor WorkflowRun is not replay-equal",
            )
        authorization = self.authorizer.execute(request.authorization_request)
        if authorization.kind is SimulationExecutionAuthorizationOutcomeKind.DENIED:
            return SimulationDispatchPreparationResult(
                kind=SimulationDispatchPreparationOutcomeKind.DENIED,
                request=request,
                authorization_result=authorization,
                predecessor_replay_result=predecessor_replay,
                candidate_run=None,
                candidate_replay_result=None,
                diagnostics=authorization.diagnostics,
            )
        if authorization.kind is SimulationExecutionAuthorizationOutcomeKind.ERROR:
            return self._error(
                request,
                predecessor_replay,
                authorization,
                None,
                authorization.diagnostics[0],
            )
        issue = self._precondition_issue(request)
        if issue is not None:
            return self._error(
                request,
                predecessor_replay,
                authorization,
                None,
                issue,
            )
        try:
            candidate = self._candidate(request, authorization)
        except ValueError:
            return self._error(
                request,
                predecessor_replay,
                authorization,
                None,
                "candidate construction rejected inconsistent correlations",
            )
        candidate_replay = self.replayer.execute(candidate, request.runtime_bundle)
        if candidate_replay.outcome is not WorkflowRunReplayOutcomeKind.EQUAL:
            return self._error(
                request,
                predecessor_replay,
                authorization,
                candidate_replay,
                "prepared candidate is not replay-equal",
            )
        return SimulationDispatchPreparationResult(
            kind=SimulationDispatchPreparationOutcomeKind.PREPARED,
            request=request,
            authorization_result=authorization,
            predecessor_replay_result=predecessor_replay,
            candidate_run=candidate,
            candidate_replay_result=candidate_replay,
            diagnostics=(),
        )

    @staticmethod
    def _precondition_issue(
        request: SimulationDispatchPreparationRequest,
    ) -> str | None:
        """Return the first non-authority preparation mismatch."""
        run = request.predecessor_run
        activation = request.activation
        authorization = request.authorization_request
        if authorization.phase is not SimulationExecutionAuthorizationPhase.PREPARATION:
            return "dispatch preparation requires preparation-phase authorization"
        if request.next_revision_identity == run.revision_identity:
            return "candidate revision must differ from predecessor revision"
        instances = {value.identity: value for value in run.task_instances}
        if (
            activation.workflow_identity != run.workflow_identity
            or activation.workflow_run_identity != run.identity
            or activation.task_instance.identity not in instances
            or instances[activation.task_instance.identity] != activation.task_instance
            or activation.identity in {value.identity for value in run.activations}
            or activation.operation_identity
            in {value.operation_identity for value in run.activations}
            or activation.attempt_identity
            in {value.attempt_identity for value in run.activations}
        ):
            return "activation is not a new exact member of the predecessor run"
        if (
            authorization.workflow_run_identity != run.identity
            or authorization.task_definition_identity
            != activation.task_instance.definition_identity
            or authorization.task_instance_identity != activation.task_instance.identity
            or authorization.activation_identity != activation.identity
            or authorization.operation_identity != activation.operation_identity
            or authorization.attempt_identity != activation.attempt_identity
        ):
            return "authorization request does not match the selected activation"
        references_by_result = {
            reference.result.identity: reference for reference in run.result_references
        }
        expected_reference_identities = tuple(
            sorted(
                (
                    references_by_result[binding.result.identity].identity
                    for binding in activation.inputs
                    if binding.result.identity in references_by_result
                ),
                key=lambda value: value.value,
            )
        )
        if len(expected_reference_identities) != len(activation.inputs) or (
            expected_reference_identities
            != authorization.input_result_reference_identities
        ):
            return "authorization inputs do not match retained activation results"
        dependencies_by_name = {
            dependency.input_name: dependency
            for dependency in request.input_dependencies
        }
        if set(dependencies_by_name) != {binding.name for binding in activation.inputs}:
            return "input dependencies must cover every activation input"
        for binding in activation.inputs:
            dependency = dependencies_by_name[binding.name]
            reference = references_by_result[binding.result.identity]
            if (
                dependency.result_reference_identity != reference.identity
                or dependency.consumer_workflow_run_identity != run.identity
                or dependency.consumer_task_instance_identity
                != activation.task_instance.identity
                or dependency.consumer_activation_identity != activation.identity
            ):
                return "input dependency does not match its activation binding"
        if any(
            request_identity in existing
            for request_identity, existing in (
                (
                    request.started_attempt_record_identity,
                    {value.identity for value in run.attempts},
                ),
                (
                    request.request_correlation_identity,
                    {value.identity for value in run.execution_request_correlations},
                ),
                (
                    request.reservation_identity,
                    {value.identity for value in run.authority_reservations},
                ),
                (
                    request.authorization_request.result_identity,
                    {value.identity for value in run.authorization_results},
                ),
            )
        ):
            return "a caller-supplied preparation identity already exists"
        if (
            activation.attempt_identity
            in {value.attempt_identity for value in run.attempts}
            or authorization.obligation_identity
            in {value.identity for value in run.dispatch_obligations}
            or authorization.grant.authority_reference.grant_identity
            in {value.grant_identity for value in run.authority_references}
            or any(
                dependency.identity
                in {value.identity for value in run.result_dependencies}
                for dependency in request.input_dependencies
            )
        ):
            return "a logical preparation identity already exists"
        return None

    @staticmethod
    def _candidate(
        request: SimulationDispatchPreparationRequest,
        authorization: SimulationExecutionAuthorizationResult,
    ) -> WorkflowRun:
        """Construct the complete immutable pending-dispatch candidate."""
        run = request.predecessor_run
        activation = request.activation
        auth_request = request.authorization_request
        authority_reference = auth_request.grant.authority_reference
        attempt = TaskAttempt(
            identity=request.started_attempt_record_identity,
            workflow_run_identity=run.identity,
            task_instance_identity=activation.task_instance.identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            status=TaskAttemptStatus.STARTED,
            retry_of_attempt_identity=request.retry_of_attempt_identity,
        )
        correlation = SimulationExecutionRequestCorrelation(
            identity=request.request_correlation_identity,
            workflow_run_identity=run.identity,
            task_instance_identity=activation.task_instance.identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            attempt_record_identity=attempt.identity,
            request_identity=auth_request.request_identity,
            executor_identity=auth_request.executor_identity,
            obligation_identity=auth_request.obligation_identity,
            grant_identity=authority_reference.grant_identity,
            authorization_result_identity=authorization.identity,
            input_result_reference_identities=(
                auth_request.input_result_reference_identities
            ),
            input_artifact_entry_identities=(
                auth_request.input_artifact_entry_identities
            ),
        )
        obligation = SimulationDispatchObligation(
            identity=auth_request.obligation_identity,
            workflow_run_identity=run.identity,
            workflow_run_revision_identity=request.next_revision_identity,
            request_identity=auth_request.request_identity,
            task_instance_identity=activation.task_instance.identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            executor_identity=auth_request.executor_identity,
            grant_identity=authority_reference.grant_identity,
            destination_identity=auth_request.destination_identity,
            resource_scope_identities=auth_request.resource_scope_identities,
            creation_idempotency_identity=request.creation_idempotency_identity,
        )
        reservation = AuthorityReservationOutcome(
            identity=request.reservation_identity,
            workflow_run_identity=run.identity,
            workflow_run_revision_identity=request.next_revision_identity,
            authority_reference=authority_reference,
            authorization_result_identity=authorization.identity,
            request_identity=auth_request.request_identity,
            activation_identity=activation.identity,
            operation_identity=activation.operation_identity,
            attempt_identity=activation.attempt_identity,
            attempt_record_identity=attempt.identity,
            obligation_identity=obligation.identity,
            expected_revision_identity=run.revision_identity,
            kind=AuthorityReservationOutcomeKind.RESERVED,
        )
        return replace(
            run,
            revision_identity=request.next_revision_identity,
            predecessor_revision_identity=run.revision_identity,
            activations=tuple(
                sorted(
                    run.activations + (activation,),
                    key=lambda value: value.identity.value,
                )
            ),
            attempts=run.attempts + (attempt,),
            result_dependencies=tuple(
                sorted(
                    run.result_dependencies + request.input_dependencies,
                    key=lambda value: value.identity.value,
                )
            ),
            authorization_results=tuple(
                sorted(
                    run.authorization_results + (authorization,),
                    key=lambda value: value.identity.value,
                )
            ),
            authority_references=tuple(
                sorted(
                    run.authority_references + (authority_reference,),
                    key=lambda value: value.grant_identity.value,
                )
            ),
            execution_request_correlations=tuple(
                sorted(
                    run.execution_request_correlations + (correlation,),
                    key=lambda value: value.identity.value,
                )
            ),
            authority_reservations=tuple(
                sorted(
                    run.authority_reservations + (reservation,),
                    key=lambda value: value.identity.value,
                )
            ),
            dispatch_obligations=tuple(
                sorted(
                    run.dispatch_obligations + (obligation,),
                    key=lambda value: value.identity.value,
                )
            ),
        )

    @staticmethod
    def _error(
        request: SimulationDispatchPreparationRequest,
        predecessor_replay: WorkflowRunReplayResult,
        authorization: SimulationExecutionAuthorizationResult | None,
        candidate_replay: WorkflowRunReplayResult | None,
        diagnostic: str,
    ) -> SimulationDispatchPreparationResult:
        """Construct one fail-closed preparation error."""
        return SimulationDispatchPreparationResult(
            kind=SimulationDispatchPreparationOutcomeKind.ERROR,
            request=request,
            authorization_result=authorization,
            predecessor_replay_result=predecessor_replay,
            candidate_run=None,
            candidate_replay_result=candidate_replay,
            diagnostics=(diagnostic,),
        )
