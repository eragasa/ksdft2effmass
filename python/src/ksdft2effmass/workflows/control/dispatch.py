"""Typed Workflow-owned simulation dispatch-effect boundary.

This module implements the architecture-facing effect port selected for Workflow
control ingress.  The adapter repeats claim-phase authorization, verifies exact
prepared-request, claimed-reservation, obligation, and executor correlations, and
invokes an injected effect only after a newly won dispatch-entry compare-and-swap.
It performs no authority issuance, persistence implementation, retry, executor
discovery, native-file access, result ingress, generic colored-Petri-net firing, or
scientific acceptance.

An application supplies the concrete effect implementation and may wrap this
architecture-facing contract in its own physicist-facing public API.  Workflow code
does not import calculator or integration implementations.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from typing import Protocol, final, runtime_checkable
from uuid import uuid4

from ...persistence import Revision, RevisionReadRequest, RevisionSelector
from ..persistence import (
    WorkflowRunCommitBinding,
    WorkflowRunRepository,
    WorkflowRunSerializer,
    WorkflowRunSnapshot,
    WorkflowRunTransaction,
)
from ..runs.authority import (
    ScientificExecutionGrantState,
    SimulationDispatchEntryReceipt,
    SimulationExecutionAuthorizationOutcomeKind,
    SimulationExecutionAuthorizationPhase,
    SimulationExecutionAuthorizationRequest,
    SimulationExecutionAuthorizationResult,
    WorkflowRunClaimCommitReceipt,
)
from ..runs.identities import (
    ScientificExecutorIdentity,
    SimulationDispatchEntryIdentity,
    SimulationDispatchEntryReceiptIdentity,
    SimulationDispatchOutcomeIdentity,
    WorkflowRunRevisionIdentity,
)
from ..runs.records import (
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeKind,
    SimulationDispatchEntry,
    SimulationDispatchObligation,
    SimulationDispatchOutcome,
    SimulationExecutionRequestCorrelation,
)
from ..runs.replay import (
    WorkflowRunReplayer,
    WorkflowRunReplayOutcomeKind,
    WorkflowRuntimeBundle,
)
from .authority import SimulationExecutionAuthorizer


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationExecutionRequest:
    """Represent one prepared simulation request ready for a later claim.

    Parameters
    ----------
    correlation
        Exact aggregate correlation for the prepared request.
    obligation
        Exact durable dispatch obligation created with the request transaction.
    preparation_authorization
        Exact authorized preparation-phase result over the same request, grant,
        activation, attempt, executor, destination, resources, and inputs.

    Notes
    -----
    This request is immutable control state.  It neither claims its grant nor
    identifies a calculator implementation object.
    """

    correlation: SimulationExecutionRequestCorrelation
    obligation: SimulationDispatchObligation
    preparation_authorization: SimulationExecutionAuthorizationResult

    def __post_init__(self) -> None:
        """Validate intrinsic field types and exact preparation correlations."""
        if type(self.correlation) is not SimulationExecutionRequestCorrelation:
            raise TypeError("correlation must be SimulationExecutionRequestCorrelation")
        if type(self.obligation) is not SimulationDispatchObligation:
            raise TypeError("obligation must be SimulationDispatchObligation")
        if type(self.preparation_authorization) is not (
            SimulationExecutionAuthorizationResult
        ):
            raise TypeError(
                "preparation_authorization must be "
                "SimulationExecutionAuthorizationResult"
            )
        authorization = self.preparation_authorization
        request = authorization.request
        correlation = self.correlation
        obligation = self.obligation
        if (
            authorization.kind
            is not SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
            or request.phase is not SimulationExecutionAuthorizationPhase.PREPARATION
            or authorization.authorized_grant_state
            is not ScientificExecutionGrantState.UNUSED
        ):
            raise ValueError("preparation_authorization must authorize an unused grant")
        if (
            correlation.request_identity != request.request_identity
            or correlation.workflow_run_identity != request.workflow_run_identity
            or correlation.task_instance_identity != request.task_instance_identity
            or correlation.activation_identity != request.activation_identity
            or correlation.operation_identity != request.operation_identity
            or correlation.attempt_identity != request.attempt_identity
            or correlation.executor_identity != request.executor_identity
            or correlation.obligation_identity != request.obligation_identity
            or correlation.grant_identity
            != request.grant.authority_reference.grant_identity
            or correlation.authorization_result_identity != authorization.identity
            or correlation.input_result_reference_identities
            != request.input_result_reference_identities
            or correlation.input_artifact_entry_identities
            != request.input_artifact_entry_identities
        ):
            raise ValueError(
                "request correlation and preparation authorization must agree"
            )
        if (
            obligation.identity != correlation.obligation_identity
            or obligation.workflow_run_identity != correlation.workflow_run_identity
            or obligation.request_identity != correlation.request_identity
            or obligation.task_instance_identity != correlation.task_instance_identity
            or obligation.activation_identity != correlation.activation_identity
            or obligation.operation_identity != correlation.operation_identity
            or obligation.attempt_identity != correlation.attempt_identity
            or obligation.executor_identity != correlation.executor_identity
            or obligation.grant_identity != correlation.grant_identity
            or obligation.destination_identity != request.destination_identity
            or obligation.resource_scope_identities != request.resource_scope_identities
        ):
            raise ValueError("dispatch obligation and prepared request must agree")


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchRequest:
    """Request one effect invocation for an exact already-claimed dispatch.

    Parameters
    ----------
    execution_request
        Exact prepared request and durable obligation.
    claim_authorization_request
        Claim-phase authorization request evaluated immediately before the effect.
    claimed_reservation
        Append-only claimed reservation committed before this request was supplied.
    claim_commit_receipt
        Typed persistence evidence naming the exact committed claimed revision,
        claim record, and claim-phase authorization result.
    outcome_identity
        Caller-supplied identity reserved for the runtime dispatch outcome.
    dispatch_entry_identity, dispatch_entry_revision_identity
        Caller-supplied identities for the durable dispatch-entry state and its
        claimed-to-entered WorkflowRun revision.

    Notes
    -----
    Construction checks the supplied committed-claim evidence.  It performs no
    persistence operation and does not independently authenticate the receipt.
    """

    execution_request: SimulationExecutionRequest
    claim_authorization_request: SimulationExecutionAuthorizationRequest
    claimed_reservation: AuthorityReservationOutcome
    claim_commit_receipt: WorkflowRunClaimCommitReceipt
    outcome_identity: SimulationDispatchOutcomeIdentity
    dispatch_entry_identity: SimulationDispatchEntryIdentity
    dispatch_entry_revision_identity: WorkflowRunRevisionIdentity

    def __post_init__(self) -> None:
        """Validate exact request types and claim-phase discrimination."""
        if type(self.execution_request) is not SimulationExecutionRequest:
            raise TypeError("execution_request must be SimulationExecutionRequest")
        if type(self.claim_authorization_request) is not (
            SimulationExecutionAuthorizationRequest
        ):
            raise TypeError(
                "claim_authorization_request must be "
                "SimulationExecutionAuthorizationRequest"
            )
        if type(self.claimed_reservation) is not AuthorityReservationOutcome:
            raise TypeError("claimed_reservation must be AuthorityReservationOutcome")
        if type(self.claim_commit_receipt) is not WorkflowRunClaimCommitReceipt:
            raise TypeError(
                "claim_commit_receipt must be WorkflowRunClaimCommitReceipt"
            )
        if type(self.outcome_identity) is not SimulationDispatchOutcomeIdentity:
            raise TypeError(
                "outcome_identity must be SimulationDispatchOutcomeIdentity"
            )
        if type(self.dispatch_entry_identity) is not SimulationDispatchEntryIdentity:
            raise TypeError(
                "dispatch_entry_identity must be SimulationDispatchEntryIdentity"
            )
        if type(self.dispatch_entry_revision_identity) is not (
            WorkflowRunRevisionIdentity
        ):
            raise TypeError(
                "dispatch_entry_revision_identity must be WorkflowRunRevisionIdentity"
            )
        if (
            self.dispatch_entry_revision_identity
            == self.claim_commit_receipt.committed_revision_identity
        ):
            raise ValueError(
                "dispatch entry revision must differ from the claimed revision"
            )
        if (
            self.claim_authorization_request.phase
            is not SimulationExecutionAuthorizationPhase.CLAIM
        ):
            raise ValueError("claim_authorization_request must use claim phase")
        if self.claimed_reservation.kind is not AuthorityReservationOutcomeKind.CLAIMED:
            raise ValueError("claimed_reservation must have claimed kind")
        execution = self.execution_request
        correlation = execution.correlation
        obligation = execution.obligation
        claim = self.claimed_reservation
        receipt = self.claim_commit_receipt
        authorization = self.claim_authorization_request
        preparation = execution.preparation_authorization.request
        if (
            authorization.request_identity != correlation.request_identity
            or authorization.workflow_run_identity != correlation.workflow_run_identity
            or authorization.task_definition_identity
            != preparation.task_definition_identity
            or authorization.task_instance_identity
            != correlation.task_instance_identity
            or authorization.activation_identity != correlation.activation_identity
            or authorization.operation_identity != correlation.operation_identity
            or authorization.attempt_identity != correlation.attempt_identity
            or authorization.executor_identity != correlation.executor_identity
            or authorization.destination_identity != obligation.destination_identity
            or authorization.obligation_identity != obligation.identity
            or authorization.resource_scope_identities
            != obligation.resource_scope_identities
            or authorization.input_result_reference_identities
            != correlation.input_result_reference_identities
            or authorization.input_artifact_entry_identities
            != preparation.input_artifact_entry_identities
            or authorization.grant.authority_reference
            != preparation.grant.authority_reference
            or not authorization.grant.is_reserved_successor_of(
                preparation.grant,
                obligation.identity,
            )
            or claim.workflow_run_identity != correlation.workflow_run_identity
            or claim.authorization_result_identity != authorization.result_identity
            or claim.request_identity != correlation.request_identity
            or claim.activation_identity != correlation.activation_identity
            or claim.operation_identity != correlation.operation_identity
            or claim.attempt_identity != correlation.attempt_identity
            or claim.attempt_record_identity != correlation.attempt_record_identity
            or claim.obligation_identity != obligation.identity
            or claim.authority_reference != authorization.grant.authority_reference
            or claim.expected_revision_identity
            != obligation.workflow_run_revision_identity
            or receipt.workflow_run_identity != correlation.workflow_run_identity
            or receipt.committed_revision_identity
            != claim.workflow_run_revision_identity
            or receipt.predecessor_revision_identity
            != obligation.workflow_run_revision_identity
            or receipt.claimed_reservation_identity != claim.identity
            or receipt.claim_authorization_result_identity
            != authorization.result_identity
        ):
            raise ValueError(
                "dispatch request, claim authorization, claim, and commit receipt "
                "must agree"
            )


class SimulationDispatchEntryOutcomeKind(StrEnum):
    """Closed result of the persistence-owned dispatch-entry compare-and-swap."""

    ENTERED = "entered"
    ALREADY_ENTERED = "already_entered"
    ERROR = "error"


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchEntryResult:
    """Record whether one persistence-owned dispatch-entry CAS was newly won.

    Parameters
    ----------
    kind
        Newly entered, already entered, or persistence-boundary error.
    request
        Exact claimed dispatch submitted to the persistence owner.
    receipt
        Typed commit evidence present only for the newly entered winner.
    diagnostics
        Empty for ``entered`` and nonempty sanitized diagnostics otherwise.

    Notes
    -----
    ``already_entered`` is not idempotent success for effect invocation. It proves
    that this adapter call did not win entry and therefore must not enter the effect.
    """

    kind: SimulationDispatchEntryOutcomeKind
    request: SimulationDispatchRequest
    receipt: SimulationDispatchEntryReceipt | None
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact result discrimination and winner receipt closure."""
        if type(self.kind) is not SimulationDispatchEntryOutcomeKind:
            raise TypeError("kind must be SimulationDispatchEntryOutcomeKind")
        if type(self.request) is not SimulationDispatchRequest:
            raise TypeError("request must be SimulationDispatchRequest")
        if self.receipt is not None and type(self.receipt) is not (
            SimulationDispatchEntryReceipt
        ):
            raise TypeError("receipt must be SimulationDispatchEntryReceipt or None")
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of strings")
        if any(not value for value in self.diagnostics) or len(
            set(self.diagnostics)
        ) != len(self.diagnostics):
            raise ValueError("diagnostics must be nonempty when present and unique")
        if self.kind is SimulationDispatchEntryOutcomeKind.ENTERED:
            if self.receipt is None or self.diagnostics:
                raise ValueError(
                    "entered result requires one receipt and no diagnostics"
                )
            request = self.request
            receipt = self.receipt
            claim_receipt = request.claim_commit_receipt
            if (
                receipt.dispatch_entry_identity != request.dispatch_entry_identity
                or receipt.workflow_run_identity
                != request.execution_request.correlation.workflow_run_identity
                or receipt.claim_commit_receipt_identity != claim_receipt.identity
                or receipt.predecessor_revision_identity
                != claim_receipt.committed_revision_identity
                or receipt.committed_revision_identity
                != request.dispatch_entry_revision_identity
                or receipt.claimed_reservation_identity
                != request.claimed_reservation.identity
                or receipt.obligation_identity
                != request.execution_request.obligation.identity
                or receipt.outcome_identity != request.outcome_identity
            ):
                raise ValueError(
                    "dispatch entry receipt must close over the exact claimed request"
                )
        elif self.receipt is not None or not self.diagnostics:
            raise ValueError(
                "already-entered and error results prohibit receipts and require "
                "diagnostics"
            )


@runtime_checkable
class SimulationDispatchEntryCommitter(Protocol):
    """Persistence-owned port for one claimed-to-dispatch-entered CAS.

    Every authorization-valid, exactly correlated adapter invocation calls this port.
    Exactly the newly successful durable winner commits a ``SimulationDispatchEntry``
    and returns ``entered``; duplicate, stale, losing, or previously entered calls
    return ``already_entered`` or ``error`` and never authorize effect entry.
    """

    def execute(
        self, request: SimulationDispatchRequest
    ) -> SimulationDispatchEntryResult:
        """Attempt one durable dispatch-entry compare-and-swap."""
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
@final
class WorkflowRunDispatchEntryCommitter:
    """Win one durable entry before an external effect may be invoked.

    Parameters
    ----------
    repository
        Explicit WorkflowRun repository port. Historical receipt recovery is not
        entry permission; no hidden retry or permission cache is used.
    serializer
        Exact serializer used by repository composition and its validator. An
        arbitrary structural repository's internal configuration is not inspected.
        Complete candidate bytes and observable acknowledgements are checked.
    runtime_bundle
        Immutable exact definition and implementation identities for both replay
        gates. Only ``equal`` allows submission.

    Raises
    ------
    TypeError
        A dependency has the wrong semantic type.

    Notes
    -----
    Every call first reconciles all historical receipt fields, then separately
    checks the exact latest head. A fresh UUID4 entry receipt and commit key bind
    one invocation's candidate. Only its exact acknowledged commit returns
    ``entered``. Collision resistance and a conforming atomic repository are
    assumed; labels do not authenticate a process. Lost acknowledgement returns
    no permission and is never retried. Crash after durable entry may leave the
    effect unperformed: this is not exactly-once completion.
    """

    repository: WorkflowRunRepository
    serializer: WorkflowRunSerializer
    runtime_bundle: WorkflowRuntimeBundle

    def __post_init__(self) -> None:
        if not isinstance(self.repository, WorkflowRunRepository):
            raise TypeError("repository must implement WorkflowRunRepository")
        if type(self.serializer) is not WorkflowRunSerializer:
            raise TypeError("serializer must be WorkflowRunSerializer")
        if type(self.runtime_bundle) is not WorkflowRuntimeBundle:
            raise TypeError("runtime_bundle must be WorkflowRuntimeBundle")

    def execute(
        self, request: SimulationDispatchRequest
    ) -> SimulationDispatchEntryResult:
        """Reconcile history, replay the current head and submit at most one CAS.

        Parameters
        ----------
        request
            Exact claimed request and supplied historical receipt.

        Returns
        -------
        SimulationDispatchEntryResult
            Only newly acknowledged exact candidate commitment returns a receipt.
            Already-entered, stale, incompatible, uncertain and failed operations
            return no receipt and confer no effect or retry permission.

        Raises
        ------
        TypeError
            The direct input is not an exact SimulationDispatchRequest.
        """
        if type(request) is not SimulationDispatchRequest:
            raise TypeError("request must be SimulationDispatchRequest")
        try:
            return self._execute(request)
        except Exception:
            # An exception can follow durable commitment: never retry or infer absence.
            return self._denied(request, "entry boundary did not complete; no retry")

    def _execute(
        self, request: SimulationDispatchRequest
    ) -> SimulationDispatchEntryResult:
        supplied = request.claim_commit_receipt
        read = RevisionReadRequest(
            request_id=str(uuid4()),
            stream_id=supplied.workflow_run_identity.value,
            selector=RevisionSelector.EXPLICIT_REVISION,
            revision_id=supplied.committed_revision_identity.value,
            expected_predecessor_revision_id=supplied.predecessor_revision_identity.value,
            expected_schema_id="ksdft2effmass.workflow-run:1",
            expected_content_id=supplied.workflow_run_content_identity,
            expected_idempotency_id=supplied.commit_idempotency_identity,
        )
        historical = self.repository.load_claim(
            read, supplied.claimed_reservation_identity
        )
        if (
            historical.status != "loaded"
            or historical.request != read
            or historical.receipt != supplied
            or historical.snapshot is None
            or historical.claimed_reservation_identity
            != supplied.claimed_reservation_identity
            or historical.store_result is None
            or historical.store_result.request_id != read.request_id
            or historical.store_result.stream_id != read.stream_id
            or historical.store_result.selector is not read.selector
            or historical.store_result.expectations_matched is not True
            or historical.store_result.revision != historical.snapshot.revision
        ):
            return self._denied(request, "historical claim receipt was not reconciled")
        snapshot = historical.snapshot
        run = snapshot.run
        if (
            snapshot.revision.stream_id != read.stream_id
            or snapshot.revision.revision_id != read.revision_id
            or snapshot.revision.predecessor_revision_id
            != read.expected_predecessor_revision_id
            or snapshot.revision.schema_id != read.expected_schema_id
            or snapshot.revision.content_id != read.expected_content_id
            or snapshot.binding.commit_idempotency_identity
            != read.expected_idempotency_id
            or snapshot.binding.persistence_implementation_identity
            != supplied.persistence_implementation_identity
        ):
            return self._denied(request, "historical snapshot differs from receipt")
        if (
            request.claimed_reservation not in run.authority_reservations
            or request.execution_request.correlation
            not in run.execution_request_correlations
            or request.execution_request.obligation not in run.dispatch_obligations
            or request.execution_request.preparation_authorization
            not in run.authorization_results
            or not any(
                value.request == request.claim_authorization_request
                and value.identity == supplied.claim_authorization_result_identity
                and value.kind is SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
                for value in run.authorization_results
            )
        ):
            return self._denied(
                request, "supplied request differs from historical claim"
            )
        current = self._current(request)
        if current is None:
            return self._denied(request, "current head could not be verified")
        if self._has_entry(current, request):
            return self._denied(request, "dispatch was already entered", already=True)
        if (
            current.revision != snapshot.revision
            or current.binding != snapshot.binding
            or not self._snapshot_agrees(snapshot, current.revision, current.binding)
            or WorkflowRunReplayer().execute(current.run, self.runtime_bundle).outcome
            is not WorkflowRunReplayOutcomeKind.EQUAL
        ):
            return self._denied(request, "current head is stale or not replay equal")

        receipt_identity = SimulationDispatchEntryReceiptIdentity(str(uuid4()))
        binding = WorkflowRunCommitBinding(
            transaction_identity=str(uuid4()),
            commit_idempotency_identity=str(uuid4()),
            persistence_implementation_identity="ksdft2effmass.workflows.WorkflowRunAtomicRepository:1",
        )
        entry = SimulationDispatchEntry(
            identity=request.dispatch_entry_identity,
            workflow_run_identity=run.identity,
            predecessor_revision_identity=run.revision_identity,
            committed_revision_identity=request.dispatch_entry_revision_identity,
            claimed_reservation_identity=request.claimed_reservation.identity,
            request_identity=request.execution_request.correlation.request_identity,
            obligation_identity=request.execution_request.obligation.identity,
            receipt_identity=receipt_identity,
            outcome_identity=request.outcome_identity,
        )
        candidate = replace(
            current.run,
            revision_identity=request.dispatch_entry_revision_identity,
            predecessor_revision_identity=run.revision_identity,
            dispatch_entries=tuple(
                sorted(
                    (*current.run.dispatch_entries, entry),
                    key=lambda value: value.identity.value,
                )
            ),
        )
        if WorkflowRunReplayer().execute(
            candidate, self.runtime_bundle
        ).outcome is not (WorkflowRunReplayOutcomeKind.EQUAL):
            return self._denied(request, "entry candidate is not replay equal")
        encoded = self.serializer.serialize(candidate, binding)
        if encoded.status != "encoded" or encoded.encoded is None:
            return self._denied(request, "entry candidate could not be serialized")
        wire = encoded.encoded
        transaction = WorkflowRunTransaction(
            binding=binding,
            run_identity=candidate.identity,
            expected_predecessor_revision_identity=run.revision_identity,
            candidate=candidate,
            schema_identity=wire.schema_identity,
            content_identity=wire.content_identity,
        )
        expected = Revision(
            stream_id=candidate.identity.value,
            revision_id=candidate.revision_identity.value,
            predecessor_revision_id=run.revision_identity.value,
            schema_id=wire.schema_identity,
            content_id=wire.content_identity,
            payload=wire.payload,
        )
        result = self.repository.commit(transaction)
        if result.status == "conflict":
            after = self._current(request)
            if after is not None and self._has_entry(after, request):
                return self._denied(request, "another invocation entered", already=True)
            return self._denied(request, "entry compare-and-swap conflicted")
        if result.status != "committed":
            return self._denied(request, "entry commit was not acknowledged; no retry")
        acknowledged = result.store_result
        returned = result.transaction
        returned_wire = self.serializer.serialize(returned.candidate, returned.binding)
        if (
            acknowledged is None
            or acknowledged.idempotency_id != binding.commit_idempotency_identity
            or acknowledged.stream_id != expected.stream_id
            or acknowledged.revision != expected
            or result.snapshot is None
            or not self._snapshot_agrees(result.snapshot, expected, binding)
            or returned.binding != binding
            or returned.run_identity != transaction.run_identity
            or returned.expected_predecessor_revision_identity != run.revision_identity
            or returned.schema_identity != wire.schema_identity
            or returned.content_identity != wire.content_identity
            or returned_wire.status != "encoded"
            or returned_wire.encoded != wire
        ):
            return self._denied(
                request, "entry acknowledgement substituted the candidate"
            )
        return SimulationDispatchEntryResult(
            kind=SimulationDispatchEntryOutcomeKind.ENTERED,
            request=request,
            receipt=SimulationDispatchEntryReceipt(
                identity=receipt_identity,
                dispatch_entry_identity=entry.identity,
                workflow_run_identity=run.identity,
                claim_commit_receipt_identity=supplied.identity,
                predecessor_revision_identity=run.revision_identity,
                committed_revision_identity=candidate.revision_identity,
                claimed_reservation_identity=entry.claimed_reservation_identity,
                obligation_identity=entry.obligation_identity,
                outcome_identity=entry.outcome_identity,
                workflow_run_content_identity=wire.content_identity,
                persistence_operation_identity=binding.transaction_identity,
                persistence_implementation_identity="ksdft2effmass.workflows.WorkflowRunDispatchEntryCommitter:1",
            ),
            diagnostics=(),
        )

    def _current(
        self, request: SimulationDispatchRequest
    ) -> WorkflowRunSnapshot | None:
        read = RevisionReadRequest(
            request_id=str(uuid4()),
            stream_id=request.claim_commit_receipt.workflow_run_identity.value,
            selector=RevisionSelector.LATEST,
        )
        result = self.repository.load(read)
        if (
            result.status != "loaded"
            or result.request != read
            or result.snapshot is None
            or result.store_result is None
            or result.store_result.request_id != read.request_id
            or result.store_result.stream_id != read.stream_id
            or result.store_result.selector is not read.selector
            or result.store_result.revision != result.snapshot.revision
        ):
            return None
        snapshot = result.snapshot
        if snapshot.revision.stream_id != read.stream_id or not self._snapshot_agrees(
            snapshot, snapshot.revision, snapshot.binding
        ):
            return None
        return snapshot

    def _snapshot_agrees(
        self,
        snapshot: WorkflowRunSnapshot,
        revision: Revision,
        binding: WorkflowRunCommitBinding,
    ) -> bool:
        encoded = self.serializer.serialize(snapshot.run, snapshot.binding)
        return (
            snapshot.binding == binding
            and snapshot.revision == revision
            and snapshot.run.identity.value == revision.stream_id
            and snapshot.run.revision_identity.value == revision.revision_id
            and (
                None
                if snapshot.run.predecessor_revision_identity is None
                else snapshot.run.predecessor_revision_identity.value
            )
            == revision.predecessor_revision_id
            and encoded.status == "encoded"
            and encoded.encoded is not None
            and encoded.encoded.schema_identity == revision.schema_id
            and encoded.encoded.content_identity == revision.content_id
            and encoded.encoded.payload == revision.payload
        )

    @staticmethod
    def _has_entry(
        snapshot: WorkflowRunSnapshot, request: SimulationDispatchRequest
    ) -> bool:
        return any(
            entry.obligation_identity == request.execution_request.obligation.identity
            and entry.claimed_reservation_identity
            == request.claimed_reservation.identity
            and entry.request_identity
            == request.execution_request.correlation.request_identity
            for entry in snapshot.run.dispatch_entries
        )

    @staticmethod
    def _denied(
        request: SimulationDispatchRequest,
        diagnostic: str,
        *,
        already: bool = False,
    ) -> SimulationDispatchEntryResult:
        return SimulationDispatchEntryResult(
            kind=(
                SimulationDispatchEntryOutcomeKind.ALREADY_ENTERED
                if already
                else SimulationDispatchEntryOutcomeKind.ERROR
            ),
            request=request,
            receipt=None,
            diagnostics=(diagnostic,),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchEffectRequest:
    """Supply one authorized, claimed, and newly entered dispatch to an effect port.

    Parameters
    ----------
    execution_request
        Exact prepared simulation request.
    claim_authorization
        Exact authorized claim-phase result produced immediately before invocation.
    claimed_reservation
        Exact append-only claimed reservation.
    claim_commit_receipt
        Typed evidence naming the committed claimed WorkflowRun revision.
    dispatch_entry_receipt
        Typed evidence returned only to the newly won dispatch-entry CAS caller.
    outcome_identity
        Exact identity that the effect must retain in its returned outcome.

    Notes
    -----
    The request conveys represented authority; it does not issue authority.  A
    concrete effect implementation remains responsible for its independent
    executor-boundary authorization check.
    """

    execution_request: SimulationExecutionRequest
    claim_authorization: SimulationExecutionAuthorizationResult
    claimed_reservation: AuthorityReservationOutcome
    claim_commit_receipt: WorkflowRunClaimCommitReceipt
    dispatch_entry_receipt: SimulationDispatchEntryReceipt
    outcome_identity: SimulationDispatchOutcomeIdentity

    def __post_init__(self) -> None:
        """Validate field types and exact dispatch-entry correlation."""
        if type(self.execution_request) is not SimulationExecutionRequest:
            raise TypeError("execution_request must be SimulationExecutionRequest")
        if type(self.claim_authorization) is not (
            SimulationExecutionAuthorizationResult
        ):
            raise TypeError(
                "claim_authorization must be SimulationExecutionAuthorizationResult"
            )
        if type(self.claimed_reservation) is not AuthorityReservationOutcome:
            raise TypeError("claimed_reservation must be AuthorityReservationOutcome")
        if type(self.claim_commit_receipt) is not WorkflowRunClaimCommitReceipt:
            raise TypeError(
                "claim_commit_receipt must be WorkflowRunClaimCommitReceipt"
            )
        if type(self.dispatch_entry_receipt) is not SimulationDispatchEntryReceipt:
            raise TypeError(
                "dispatch_entry_receipt must be SimulationDispatchEntryReceipt"
            )
        if type(self.outcome_identity) is not SimulationDispatchOutcomeIdentity:
            raise TypeError(
                "outcome_identity must be SimulationDispatchOutcomeIdentity"
            )
        if (
            self.claim_authorization.kind
            is not SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
            or self.claim_authorization.request.phase
            is not SimulationExecutionAuthorizationPhase.CLAIM
            or self.claim_authorization.authorized_grant_state
            is not ScientificExecutionGrantState.RESERVED
        ):
            raise ValueError("claim_authorization must authorize a reserved grant")
        if self.claimed_reservation.kind is not AuthorityReservationOutcomeKind.CLAIMED:
            raise ValueError("claimed_reservation must have claimed kind")
        dispatch_request = SimulationDispatchRequest(
            execution_request=self.execution_request,
            claim_authorization_request=self.claim_authorization.request,
            claimed_reservation=self.claimed_reservation,
            claim_commit_receipt=self.claim_commit_receipt,
            outcome_identity=self.outcome_identity,
            dispatch_entry_identity=self.dispatch_entry_receipt.dispatch_entry_identity,
            dispatch_entry_revision_identity=(
                self.dispatch_entry_receipt.committed_revision_identity
            ),
        )
        entry_result = SimulationDispatchEntryResult(
            kind=SimulationDispatchEntryOutcomeKind.ENTERED,
            request=dispatch_request,
            receipt=self.dispatch_entry_receipt,
            diagnostics=(),
        )
        if (
            dispatch_request.claim_authorization_request.result_identity
            != self.claim_authorization.identity
            or entry_result.receipt is not self.dispatch_entry_receipt
        ):
            raise ValueError(
                "effect request authorization and dispatch entry must match the claim"
            )


@runtime_checkable
class SimulationDispatchEffect(Protocol):
    """Architecture-facing consumer port for one claimed simulation dispatch.

    Applications adapt calculator-owned executors to this protocol and may wrap it
    in application-specific public APIs.  An implementation must independently
    check executor-bound authority, invoke at most once, return exact correlations,
    and never retry an indeterminate operation.
    """

    @property
    def executor_identity(self) -> ScientificExecutorIdentity:
        """Return the exact executor identity accepted by this effect."""
        ...

    def execute(
        self,
        request: SimulationDispatchEffectRequest,
    ) -> SimulationDispatchOutcome:
        """Perform one independently authorized external simulation effect."""
        ...


class SimulationDispatchAdapterResultKind(StrEnum):
    """Closed result kind for dispatch-adapter orchestration."""

    DISPATCHED = "dispatched"
    DENIED = "denied"
    ALREADY_ENTERED = "already_entered"
    ERROR = "error"
    INDETERMINATE = "indeterminate"


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchAdapterResult:
    """Record whether dispatch was invoked and which outcome was established.

    Parameters
    ----------
    kind
        Dispatched, denied, pre-effect error, or post-invocation indeterminate.
    request
        Exact originating dispatch request including committed-claim evidence.
    authorization_result
        Exact immediate claim-phase authorization result.
    entry_result
        Persistence-owned CAS result when dispatch entry was attempted; otherwise
        ``None`` for pre-entry denial or error.
    outcome
        Exact runtime outcome for ``dispatched`` only.
    effect_invoked
        Whether the effect port was entered.  It is true for ``dispatched`` and
        post-invocation ``indeterminate`` only.
    diagnostics
        Empty for ``dispatched`` and nonempty sanitized diagnostics otherwise.
    """

    kind: SimulationDispatchAdapterResultKind
    request: SimulationDispatchRequest
    authorization_result: SimulationExecutionAuthorizationResult
    entry_result: SimulationDispatchEntryResult | None
    outcome: SimulationDispatchOutcome | None
    effect_invoked: bool
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact result discrimination and effect-invocation claim."""
        if type(self.kind) is not SimulationDispatchAdapterResultKind:
            raise TypeError("kind must be SimulationDispatchAdapterResultKind")
        if type(self.request) is not SimulationDispatchRequest:
            raise TypeError("request must be SimulationDispatchRequest")
        if type(self.authorization_result) is not (
            SimulationExecutionAuthorizationResult
        ):
            raise TypeError(
                "authorization_result must be SimulationExecutionAuthorizationResult"
            )
        if self.entry_result is not None and type(self.entry_result) is not (
            SimulationDispatchEntryResult
        ):
            raise TypeError(
                "entry_result must be SimulationDispatchEntryResult or None"
            )
        if self.entry_result is not None and self.entry_result.request != self.request:
            raise ValueError("entry_result must belong to the originating request")
        if (
            self.outcome is not None
            and type(self.outcome) is not SimulationDispatchOutcome
        ):
            raise TypeError("outcome must be SimulationDispatchOutcome or None")
        if type(self.effect_invoked) is not bool:
            raise TypeError("effect_invoked must be bool")
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of strings")
        if any(not value for value in self.diagnostics):
            raise ValueError("diagnostics must not contain empty strings")
        if len(set(self.diagnostics)) != len(self.diagnostics):
            raise ValueError("diagnostics must not contain duplicates")
        if self.authorization_result.request != (
            self.request.claim_authorization_request
        ):
            raise ValueError(
                "authorization_result must belong to the originating dispatch request"
            )
        if self.outcome is not None and not SimulationDispatchAdapter._outcome_agrees(
            self.request, self.outcome
        ):
            raise ValueError("outcome must belong to the originating dispatch request")
        valid = {
            SimulationDispatchAdapterResultKind.DISPATCHED: (
                self.entry_result is not None
                and self.entry_result.kind is SimulationDispatchEntryOutcomeKind.ENTERED
                and self.outcome is not None
                and self.effect_invoked
                and not self.diagnostics
                and self.authorization_result.kind
                is SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
            ),
            SimulationDispatchAdapterResultKind.DENIED: (
                self.entry_result is None
                and self.outcome is None
                and not self.effect_invoked
                and bool(self.diagnostics)
                and self.authorization_result.kind
                is SimulationExecutionAuthorizationOutcomeKind.DENIED
            ),
            SimulationDispatchAdapterResultKind.ALREADY_ENTERED: (
                self.entry_result is not None
                and self.entry_result.kind
                is SimulationDispatchEntryOutcomeKind.ALREADY_ENTERED
                and self.outcome is None
                and not self.effect_invoked
                and self.diagnostics == self.entry_result.diagnostics
                and self.authorization_result.kind
                is SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
            ),
            SimulationDispatchAdapterResultKind.ERROR: (
                self.outcome is None
                and not self.effect_invoked
                and bool(self.diagnostics)
                and (
                    self.entry_result is None
                    or self.entry_result.kind
                    is SimulationDispatchEntryOutcomeKind.ERROR
                )
                and self.authorization_result.kind
                in {
                    SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED,
                    SimulationExecutionAuthorizationOutcomeKind.ERROR,
                }
            ),
            SimulationDispatchAdapterResultKind.INDETERMINATE: (
                self.entry_result is not None
                and self.entry_result.kind is SimulationDispatchEntryOutcomeKind.ENTERED
                and self.outcome is None
                and self.effect_invoked
                and bool(self.diagnostics)
                and self.authorization_result.kind
                is SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED
            ),
        }[self.kind]
        if not valid:
            raise ValueError("adapter result fields do not match the result kind")


@dataclass(frozen=True, slots=True)
@final
class SimulationDispatchAdapter:
    """Authorize and invoke one exact application-supplied dispatch effect.

    Parameters
    ----------
    authorizer
        Effect-free ActionObject used for the immediate claim-phase check.
    entry_committer
        Persistence-owned compare-and-swap port invoked once by every adapter call.
    effect
        Application-supplied architecture-facing effect port bound to one exact
        executor identity.

    Notes
    -----
    Persistence must establish the represented claim before constructing the input
    request. The adapter invokes the injected persistence-owned compare-and-swap port
    and enters the effect only when that call newly wins dispatch entry. It owns no
    persistence implementation and treats an already-entered result as non-authority.
    """

    authorizer: SimulationExecutionAuthorizer
    entry_committer: SimulationDispatchEntryCommitter
    effect: SimulationDispatchEffect

    def __post_init__(self) -> None:
        """Validate exact injected ActionObject and structural ports."""
        if type(self.authorizer) is not SimulationExecutionAuthorizer:
            raise TypeError("authorizer must be SimulationExecutionAuthorizer")
        if not isinstance(self.entry_committer, SimulationDispatchEntryCommitter):
            raise TypeError(
                "entry_committer must implement SimulationDispatchEntryCommitter"
            )
        if not isinstance(self.effect, SimulationDispatchEffect):
            raise TypeError("effect must implement SimulationDispatchEffect")
        if type(self.effect.executor_identity) is not ScientificExecutorIdentity:
            raise TypeError(
                "effect executor_identity must be ScientificExecutorIdentity"
            )

    def execute(
        self,
        request: SimulationDispatchRequest,
    ) -> SimulationDispatchAdapterResult:
        """Perform the immediate authorization check and invoke at most once.

        Parameters
        ----------
        request
            Exact prepared request, claim-phase authorization input, represented
            successful claim, typed commit receipt, and reserved outcome identity.

        Returns
        -------
        SimulationDispatchAdapterResult
            Closed result distinguishing pre-effect denial/error from an established
            runtime outcome or post-invocation indeterminacy.

        Raises
        ------
        TypeError
            If ``request`` is not the exact request DataObject.
        Exception
            An exception raised by the application-supplied effect is propagated.
            Because the effect boundary was entered, propagation provides no claim
            that the external operation did not occur and no retry authority.
        """
        if type(request) is not SimulationDispatchRequest:
            raise TypeError("request must be SimulationDispatchRequest")
        authorization = self.authorizer.execute(request.claim_authorization_request)
        if authorization.kind is SimulationExecutionAuthorizationOutcomeKind.DENIED:
            return SimulationDispatchAdapterResult(
                kind=SimulationDispatchAdapterResultKind.DENIED,
                request=request,
                authorization_result=authorization,
                entry_result=None,
                outcome=None,
                effect_invoked=False,
                diagnostics=authorization.diagnostics,
            )
        if authorization.kind is SimulationExecutionAuthorizationOutcomeKind.ERROR:
            return SimulationDispatchAdapterResult(
                kind=SimulationDispatchAdapterResultKind.ERROR,
                request=request,
                authorization_result=authorization,
                entry_result=None,
                outcome=None,
                effect_invoked=False,
                diagnostics=authorization.diagnostics,
            )
        correlation_issue = self._correlation_issue(request, authorization)
        if correlation_issue is not None:
            return SimulationDispatchAdapterResult(
                kind=SimulationDispatchAdapterResultKind.ERROR,
                request=request,
                authorization_result=authorization,
                entry_result=None,
                outcome=None,
                effect_invoked=False,
                diagnostics=(correlation_issue,),
            )
        entry_result = self.entry_committer.execute(request)
        if (
            type(entry_result) is not SimulationDispatchEntryResult
            or entry_result.request != request
        ):
            return SimulationDispatchAdapterResult(
                kind=SimulationDispatchAdapterResultKind.ERROR,
                request=request,
                authorization_result=authorization,
                entry_result=None,
                outcome=None,
                effect_invoked=False,
                diagnostics=(
                    "dispatch-entry committer returned a result for another request",
                ),
            )
        if entry_result.kind is SimulationDispatchEntryOutcomeKind.ALREADY_ENTERED:
            return SimulationDispatchAdapterResult(
                kind=SimulationDispatchAdapterResultKind.ALREADY_ENTERED,
                request=request,
                authorization_result=authorization,
                entry_result=entry_result,
                outcome=None,
                effect_invoked=False,
                diagnostics=entry_result.diagnostics,
            )
        if entry_result.kind is SimulationDispatchEntryOutcomeKind.ERROR:
            return SimulationDispatchAdapterResult(
                kind=SimulationDispatchAdapterResultKind.ERROR,
                request=request,
                authorization_result=authorization,
                entry_result=entry_result,
                outcome=None,
                effect_invoked=False,
                diagnostics=entry_result.diagnostics,
            )
        assert entry_result.receipt is not None
        effect_request = SimulationDispatchEffectRequest(
            execution_request=request.execution_request,
            claim_authorization=authorization,
            claimed_reservation=request.claimed_reservation,
            claim_commit_receipt=request.claim_commit_receipt,
            dispatch_entry_receipt=entry_result.receipt,
            outcome_identity=request.outcome_identity,
        )
        outcome = self.effect.execute(effect_request)
        if not self._outcome_agrees(request, outcome):
            return SimulationDispatchAdapterResult(
                kind=SimulationDispatchAdapterResultKind.INDETERMINATE,
                request=request,
                authorization_result=authorization,
                entry_result=entry_result,
                outcome=None,
                effect_invoked=True,
                diagnostics=(
                    "dispatch effect returned an outcome with mismatched correlation",
                ),
            )
        return SimulationDispatchAdapterResult(
            kind=SimulationDispatchAdapterResultKind.DISPATCHED,
            request=request,
            authorization_result=authorization,
            entry_result=entry_result,
            outcome=outcome,
            effect_invoked=True,
            diagnostics=(),
        )

    def _correlation_issue(
        self,
        request: SimulationDispatchRequest,
        authorization: SimulationExecutionAuthorizationResult,
    ) -> str | None:
        """Return the first pre-effect correlation failure, if present."""
        execution = request.execution_request
        correlation = execution.correlation
        obligation = execution.obligation
        claim = request.claimed_reservation
        authorization_request = authorization.request
        preparation_request = execution.preparation_authorization.request
        receipt = request.claim_commit_receipt
        if self.effect.executor_identity != correlation.executor_identity:
            return "dispatch effect executor does not match the prepared request"
        if (
            authorization_request.request_identity != correlation.request_identity
            or authorization_request.workflow_run_identity
            != correlation.workflow_run_identity
            or authorization_request.task_definition_identity
            != preparation_request.task_definition_identity
            or authorization_request.task_instance_identity
            != correlation.task_instance_identity
            or authorization_request.activation_identity
            != correlation.activation_identity
            or authorization_request.operation_identity
            != correlation.operation_identity
            or authorization_request.attempt_identity != correlation.attempt_identity
            or authorization_request.executor_identity != correlation.executor_identity
            or authorization_request.obligation_identity != obligation.identity
            or authorization_request.destination_identity
            != obligation.destination_identity
            or authorization_request.resource_scope_identities
            != obligation.resource_scope_identities
            or authorization_request.input_result_reference_identities
            != correlation.input_result_reference_identities
            or authorization_request.input_artifact_entry_identities
            != preparation_request.input_artifact_entry_identities
            or not authorization_request.grant.is_reserved_successor_of(
                preparation_request.grant,
                obligation.identity,
            )
        ):
            return "claim authorization does not match the prepared request"
        if (
            claim.authorization_result_identity != authorization.identity
            or claim.request_identity != correlation.request_identity
            or claim.activation_identity != correlation.activation_identity
            or claim.operation_identity != correlation.operation_identity
            or claim.attempt_identity != correlation.attempt_identity
            or claim.attempt_record_identity != correlation.attempt_record_identity
            or claim.obligation_identity != obligation.identity
            or claim.authority_reference
            != authorization_request.grant.authority_reference
            or claim.expected_revision_identity
            != obligation.workflow_run_revision_identity
            or receipt.workflow_run_identity != correlation.workflow_run_identity
            or receipt.committed_revision_identity
            != claim.workflow_run_revision_identity
            or receipt.predecessor_revision_identity
            != obligation.workflow_run_revision_identity
            or receipt.claimed_reservation_identity != claim.identity
            or receipt.claim_authorization_result_identity != authorization.identity
        ):
            return "claimed reservation does not match the authorized obligation"
        return None

    @staticmethod
    def _outcome_agrees(
        request: SimulationDispatchRequest,
        outcome: SimulationDispatchOutcome,
    ) -> bool:
        """Return whether a runtime outcome closes over the exact dispatched request."""
        if type(outcome) is not SimulationDispatchOutcome:
            return False
        correlation = request.execution_request.correlation
        obligation = request.execution_request.obligation
        authority_reference = (
            request.claim_authorization_request.grant.authority_reference
        )
        grant_identity = authority_reference.grant_identity
        return (
            outcome.identity == request.outcome_identity
            and outcome.request_identity == correlation.request_identity
            and outcome.workflow_run_identity == correlation.workflow_run_identity
            and outcome.task_instance_identity == correlation.task_instance_identity
            and outcome.activation_identity == correlation.activation_identity
            and outcome.operation_identity == correlation.operation_identity
            and outcome.attempt_identity == correlation.attempt_identity
            and outcome.executor_identity == correlation.executor_identity
            and outcome.obligation_identity == obligation.identity
            and outcome.grant_identity == grant_identity
        )
