"""Effect-free preparation of one claimed WorkflowRun successor candidate."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from typing import final

from ..runs.aggregate import WorkflowRun
from ..runs.authority import (
    SimulationExecutionAuthorizationOutcomeKind,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizationRequest,
    SimulationExecutionAuthorizationResult,
)
from ..runs.identities import (
    AuthorityReservationOutcomeIdentity,
    WorkflowRunRevisionIdentity,
)
from ..runs.records import (
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeKind,
)
from ..runs.replay import (
    WorkflowRunReplayer,
    WorkflowRunReplayOutcomeKind,
    WorkflowRunReplayResult,
    WorkflowRuntimeBundle,
)
from .authority import SimulationExecutionAuthorizer
from .dispatch import SimulationExecutionRequest


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchClaimRequest:
    """Request one replay-verified claimed WorkflowRun candidate.

    Parameters
    ----------
    predecessor_run, runtime_bundle
        Exact prepared predecessor and explicit runtime dependencies.
    execution_request
        Exact preparation correlation, obligation, and retained authorization result.
    claim_authorization_request
        Distinct claim-phase authorization request over the reserved grant view.
    next_revision_identity
        Caller-supplied revision identity for the claimed successor.
    claimed_reservation_identity
        Caller-supplied identity for the append-only claim record.
    """

    predecessor_run: WorkflowRun
    runtime_bundle: WorkflowRuntimeBundle
    execution_request: SimulationExecutionRequest
    claim_authorization_request: SimulationExecutionAuthorizationRequest
    next_revision_identity: WorkflowRunRevisionIdentity
    claimed_reservation_identity: AuthorityReservationOutcomeIdentity

    def __post_init__(self) -> None:
        """Validate exact claim-preparation input types and phase."""
        expected = (
            (self.predecessor_run, WorkflowRun, "predecessor_run"),
            (self.runtime_bundle, WorkflowRuntimeBundle, "runtime_bundle"),
            (
                self.execution_request,
                SimulationExecutionRequest,
                "execution_request",
            ),
            (
                self.claim_authorization_request,
                SimulationExecutionAuthorizationRequest,
                "claim_authorization_request",
            ),
            (
                self.next_revision_identity,
                WorkflowRunRevisionIdentity,
                "next_revision_identity",
            ),
            (
                self.claimed_reservation_identity,
                AuthorityReservationOutcomeIdentity,
                "claimed_reservation_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if (
            self.claim_authorization_request.phase
            is not SimulationExecutionAuthorizationPhase.CLAIM
        ):
            raise ValueError("claim_authorization_request must use claim phase")


class SimulationDispatchClaimOutcomeKind(StrEnum):
    """Closed outcomes of effect-free claim preparation."""

    CLAIMED = "claimed"
    DENIED = "denied"
    ERROR = "error"


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchClaimResult:
    """Record a replay-verified claim candidate, denial, or error."""

    kind: SimulationDispatchClaimOutcomeKind
    request: SimulationDispatchClaimRequest
    authorization_result: SimulationExecutionAuthorizationResult | None
    predecessor_replay_result: WorkflowRunReplayResult
    candidate_run: WorkflowRun | None
    candidate_replay_result: WorkflowRunReplayResult | None
    claimed_reservation: AuthorityReservationOutcome | None
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact result types and closed variants."""
        if type(self.kind) is not SimulationDispatchClaimOutcomeKind:
            raise TypeError("kind must be SimulationDispatchClaimOutcomeKind")
        if type(self.request) is not SimulationDispatchClaimRequest:
            raise TypeError("request must be SimulationDispatchClaimRequest")
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
        if (
            self.claimed_reservation is not None
            and type(self.claimed_reservation) is not AuthorityReservationOutcome
        ):
            raise TypeError(
                "claimed_reservation must be AuthorityReservationOutcome or None"
            )
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of strings")
        if any(not value for value in self.diagnostics) or len(
            set(self.diagnostics)
        ) != len(self.diagnostics):
            raise ValueError("diagnostics must be nonempty when present and unique")
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
        if self.kind is SimulationDispatchClaimOutcomeKind.CLAIMED:
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
                or self.claimed_reservation is None
                or self.diagnostics
            ):
                raise ValueError(
                    "claimed result requires authorization, claim, candidate, and "
                    "two equal replays"
                )
            if (
                self.candidate_run.identity != self.request.predecessor_run.identity
                or self.candidate_run.revision_identity
                != self.request.next_revision_identity
                or self.claimed_reservation.identity
                != self.request.claimed_reservation_identity
            ):
                raise ValueError("claimed result identities must match its request")
            return
        if (
            self.candidate_run is not None
            or self.candidate_replay_result is not None
            or self.claimed_reservation is not None
            or not self.diagnostics
        ):
            raise ValueError(
                "denied and error results prohibit candidate state and require "
                "diagnostics"
            )
        if self.kind is SimulationDispatchClaimOutcomeKind.DENIED and (
            self.authorization_result is None
            or self.authorization_result.kind
            is not SimulationExecutionAuthorizationOutcomeKind.DENIED
        ):
            raise ValueError("denied result requires one denied authorization")


@dataclass(frozen=True, slots=True)
@final
class SimulationDispatchClaimPreparer:
    """Construct and replay one claim candidate without persistence or an effect."""

    authorizer: SimulationExecutionAuthorizer
    replayer: WorkflowRunReplayer

    def __post_init__(self) -> None:
        """Validate exact injected ActionObjects."""
        if type(self.authorizer) is not SimulationExecutionAuthorizer:
            raise TypeError("authorizer must be SimulationExecutionAuthorizer")
        if type(self.replayer) is not WorkflowRunReplayer:
            raise TypeError("replayer must be WorkflowRunReplayer")

    def execute(
        self, request: SimulationDispatchClaimRequest
    ) -> SimulationDispatchClaimResult:
        """Replay, authorize, construct, and replay one claimed successor."""
        if type(request) is not SimulationDispatchClaimRequest:
            raise TypeError("request must be SimulationDispatchClaimRequest")
        predecessor_replay = self.replayer.execute(
            request.predecessor_run, request.runtime_bundle
        )
        if predecessor_replay.outcome is not WorkflowRunReplayOutcomeKind.EQUAL:
            return self._error(
                request,
                predecessor_replay,
                None,
                "prepared predecessor is not replay-equal",
            )
        authorization = self.authorizer.execute(request.claim_authorization_request)
        if authorization.kind is SimulationExecutionAuthorizationOutcomeKind.DENIED:
            return SimulationDispatchClaimResult(
                kind=SimulationDispatchClaimOutcomeKind.DENIED,
                request=request,
                authorization_result=authorization,
                predecessor_replay_result=predecessor_replay,
                candidate_run=None,
                candidate_replay_result=None,
                claimed_reservation=None,
                diagnostics=authorization.diagnostics,
            )
        if authorization.kind is SimulationExecutionAuthorizationOutcomeKind.ERROR:
            return self._error(
                request,
                predecessor_replay,
                authorization,
                authorization.diagnostics[0],
            )
        issue = self._precondition_issue(request, authorization)
        if issue is not None:
            return self._error(
                request,
                predecessor_replay,
                authorization,
                issue,
            )
        reservation = self._reservation(request, authorization)
        try:
            candidate = replace(
                request.predecessor_run,
                revision_identity=request.next_revision_identity,
                predecessor_revision_identity=(
                    request.predecessor_run.revision_identity
                ),
                authorization_results=tuple(
                    sorted(
                        request.predecessor_run.authorization_results
                        + (authorization,),
                        key=lambda value: value.identity.value,
                    )
                ),
                authority_reservations=tuple(
                    sorted(
                        request.predecessor_run.authority_reservations + (reservation,),
                        key=lambda value: value.identity.value,
                    )
                ),
            )
        except ValueError:
            return self._error(
                request,
                predecessor_replay,
                authorization,
                "claim candidate construction rejected inconsistent correlations",
            )
        candidate_replay = self.replayer.execute(candidate, request.runtime_bundle)
        if candidate_replay.outcome is not WorkflowRunReplayOutcomeKind.EQUAL:
            return self._error(
                request,
                predecessor_replay,
                authorization,
                "claim candidate is not replay-equal",
            )
        return SimulationDispatchClaimResult(
            kind=SimulationDispatchClaimOutcomeKind.CLAIMED,
            request=request,
            authorization_result=authorization,
            predecessor_replay_result=predecessor_replay,
            candidate_run=candidate,
            candidate_replay_result=candidate_replay,
            claimed_reservation=reservation,
            diagnostics=(),
        )

    @staticmethod
    def _precondition_issue(
        request: SimulationDispatchClaimRequest,
        authorization: SimulationExecutionAuthorizationResult,
    ) -> str | None:
        """Return the first claim-preparation correlation error."""
        run = request.predecessor_run
        execution = request.execution_request
        correlation = execution.correlation
        obligation = execution.obligation
        preparation = execution.preparation_authorization
        claim_request = authorization.request
        if request.next_revision_identity == run.revision_identity:
            return "claim candidate revision must differ from predecessor revision"
        if obligation.workflow_run_revision_identity != run.revision_identity:
            return "prepared obligation must belong to the predecessor revision"
        if (
            correlation not in run.execution_request_correlations
            or obligation not in run.dispatch_obligations
            or preparation not in run.authorization_results
        ):
            return "execution request records are absent from the predecessor"
        reserved = tuple(
            value
            for value in run.authority_reservations
            if value.obligation_identity == obligation.identity
            and value.kind is AuthorityReservationOutcomeKind.RESERVED
        )
        claims = tuple(
            value
            for value in run.authority_reservations
            if value.obligation_identity == obligation.identity
            and value.kind is AuthorityReservationOutcomeKind.CLAIMED
        )
        if len(reserved) != 1 or claims:
            return "claim requires one unclaimed exact reservation"
        reservation = reserved[0]
        if (
            request.claimed_reservation_identity
            in {value.identity for value in run.authority_reservations}
            or authorization.identity
            in {value.identity for value in run.authorization_results}
            or reservation.authorization_result_identity != preparation.identity
            or reservation.request_identity != correlation.request_identity
            or reservation.activation_identity != correlation.activation_identity
            or reservation.operation_identity != correlation.operation_identity
            or reservation.attempt_identity != correlation.attempt_identity
            or reservation.attempt_record_identity
            != correlation.attempt_record_identity
            or reservation.obligation_identity != obligation.identity
            or claim_request.request_identity != correlation.request_identity
            or claim_request.workflow_run_identity != run.identity
            or claim_request.task_definition_identity
            != preparation.request.task_definition_identity
            or claim_request.task_instance_identity
            != correlation.task_instance_identity
            or claim_request.activation_identity != correlation.activation_identity
            or claim_request.operation_identity != correlation.operation_identity
            or claim_request.attempt_identity != correlation.attempt_identity
            or claim_request.executor_identity != correlation.executor_identity
            or claim_request.destination_identity != obligation.destination_identity
            or claim_request.obligation_identity != obligation.identity
            or claim_request.resource_scope_identities
            != obligation.resource_scope_identities
            or claim_request.input_result_reference_identities
            != correlation.input_result_reference_identities
            or claim_request.input_artifact_entry_identities
            != preparation.request.input_artifact_entry_identities
            or not claim_request.grant.is_reserved_successor_of(
                preparation.request.grant,
                obligation.identity,
            )
        ):
            return "claim authorization does not close over the exact reservation"
        return None

    @staticmethod
    def _reservation(
        request: SimulationDispatchClaimRequest,
        authorization: SimulationExecutionAuthorizationResult,
    ) -> AuthorityReservationOutcome:
        """Construct the append-only claimed reservation record."""
        execution = request.execution_request
        correlation = execution.correlation
        obligation = execution.obligation
        reserved = next(
            value
            for value in request.predecessor_run.authority_reservations
            if value.obligation_identity == obligation.identity
            and value.kind is AuthorityReservationOutcomeKind.RESERVED
        )
        return AuthorityReservationOutcome(
            identity=request.claimed_reservation_identity,
            workflow_run_identity=request.predecessor_run.identity,
            workflow_run_revision_identity=request.next_revision_identity,
            authority_reference=authorization.request.grant.authority_reference,
            authorization_result_identity=authorization.identity,
            request_identity=correlation.request_identity,
            activation_identity=correlation.activation_identity,
            operation_identity=correlation.operation_identity,
            attempt_identity=correlation.attempt_identity,
            attempt_record_identity=correlation.attempt_record_identity,
            obligation_identity=obligation.identity,
            expected_revision_identity=request.predecessor_run.revision_identity,
            kind=AuthorityReservationOutcomeKind.CLAIMED,
            predecessor_reservation_identity=reserved.identity,
        )

    @staticmethod
    def _error(
        request: SimulationDispatchClaimRequest,
        predecessor_replay: WorkflowRunReplayResult,
        authorization: SimulationExecutionAuthorizationResult | None,
        diagnostic: str,
    ) -> SimulationDispatchClaimResult:
        """Construct one fail-closed claim-preparation error."""
        return SimulationDispatchClaimResult(
            kind=SimulationDispatchClaimOutcomeKind.ERROR,
            request=request,
            authorization_result=authorization,
            predecessor_replay_result=predecessor_replay,
            candidate_run=None,
            candidate_replay_result=None,
            claimed_reservation=None,
            diagnostics=(diagnostic,),
        )
