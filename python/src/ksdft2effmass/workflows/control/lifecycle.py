"""Persisted reservation-to-claim-to-dispatch Workflow composition.

This module composes existing effect-free preparation and claim ActionObjects,
explicit WorkflowRun commits, immediate dispatch authorization, durable dispatch
entry, and one injected simulation effect. It issues no authority, discovers no
executor, retries no operation, and interprets no scientific result.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import final

from ..persistence import (
    WorkflowRunCommitBinding,
    WorkflowRunRepository,
    WorkflowRunSerializer,
    WorkflowRunTransaction,
    WorkflowRunWriteResult,
)
from ..runs.aggregate import WorkflowRun
from ..runs.authority import SimulationExecutionAuthorizationRequest
from ..runs.identities import (
    AuthorityReservationOutcomeIdentity,
    SimulationDispatchEntryIdentity,
    SimulationDispatchOutcomeIdentity,
    WorkflowRunRevisionIdentity,
)
from ..runs.replay import WorkflowRunReplayer, WorkflowRuntimeBundle
from .authority import SimulationExecutionAuthorizer
from .claim import (
    SimulationDispatchClaimOutcomeKind,
    SimulationDispatchClaimPreparer,
    SimulationDispatchClaimRequest,
    SimulationDispatchClaimResult,
)
from .dispatch import (
    SimulationDispatchAdapter,
    SimulationDispatchAdapterResult,
    SimulationDispatchEffect,
    SimulationDispatchRequest,
    SimulationExecutionRequest,
    WorkflowRunDispatchEntryCommitter,
)
from .preparation import (
    SimulationDispatchPreparationOutcomeKind,
    SimulationDispatchPreparationRequest,
    SimulationDispatchPreparationResult,
    SimulationDispatchPreparer,
)


class SimulationDispatchControlFailureStage(StrEnum):
    """Closed pre-dispatch failure stage for lifecycle composition."""

    PREPARATION = "preparation"
    PREPARATION_SERIALIZATION = "preparation_serialization"
    PREPARATION_COMMIT = "preparation_commit"
    CLAIM = "claim"
    CLAIM_SERIALIZATION = "claim_serialization"
    CLAIM_COMMIT = "claim_commit"
    CLAIM_RECEIPT = "claim_receipt"


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchControlRequest:
    """Supply exact identities and bindings for one persisted dispatch lifecycle.

    Parameters
    ----------
    preparation_request
        Exact effect-free request that constructs the reserved candidate.
    preparation_commit_binding
        Caller-supplied durable transaction and idempotency labels for that candidate.
    claim_authorization_request
        Exact reserved-grant authorization input for claim preparation.
    claim_revision_identity, claimed_reservation_identity
        Caller-supplied identities for the claimed successor and append-only claim.
    claim_commit_binding
        Caller-supplied durable transaction and idempotency labels for the claim.
    dispatch_outcome_identity
        Identity reserved for the specialized runtime dispatch outcome.
    dispatch_entry_identity, dispatch_entry_revision_identity
        Caller-supplied durable dispatch-entry and successor-revision identities.

    Notes
    -----
    The request carries no permission by itself. In particular, commit labels,
    manifest correlations, and authority references are not execution grants.
    """

    preparation_request: SimulationDispatchPreparationRequest
    preparation_commit_binding: WorkflowRunCommitBinding
    claim_authorization_request: SimulationExecutionAuthorizationRequest
    claim_revision_identity: WorkflowRunRevisionIdentity
    claimed_reservation_identity: AuthorityReservationOutcomeIdentity
    claim_commit_binding: WorkflowRunCommitBinding
    dispatch_outcome_identity: SimulationDispatchOutcomeIdentity
    dispatch_entry_identity: SimulationDispatchEntryIdentity
    dispatch_entry_revision_identity: WorkflowRunRevisionIdentity

    def __post_init__(self) -> None:
        expected = (
            (
                self.preparation_request,
                SimulationDispatchPreparationRequest,
                "preparation_request",
            ),
            (
                self.preparation_commit_binding,
                WorkflowRunCommitBinding,
                "preparation_commit_binding",
            ),
            (
                self.claim_authorization_request,
                SimulationExecutionAuthorizationRequest,
                "claim_authorization_request",
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
            (
                self.dispatch_outcome_identity,
                SimulationDispatchOutcomeIdentity,
                "dispatch_outcome_identity",
            ),
            (
                self.dispatch_entry_identity,
                SimulationDispatchEntryIdentity,
                "dispatch_entry_identity",
            ),
            (
                self.dispatch_entry_revision_identity,
                WorkflowRunRevisionIdentity,
                "dispatch_entry_revision_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        revisions = (
            self.preparation_request.predecessor_run.revision_identity,
            self.preparation_request.next_revision_identity,
            self.claim_revision_identity,
            self.dispatch_entry_revision_identity,
        )
        if len(set(revisions)) != len(revisions):
            raise ValueError("lifecycle revision identities must be distinct")
        if self.preparation_commit_binding == self.claim_commit_binding:
            raise ValueError("preparation and claim commit bindings must differ")


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchControlFailure:
    """Record one closed failure before the dispatch adapter returns a result."""

    request: SimulationDispatchControlRequest
    stage: SimulationDispatchControlFailureStage
    diagnostics: tuple[str, ...]
    preparation_result: SimulationDispatchPreparationResult | None = None
    preparation_write_result: WorkflowRunWriteResult | None = None
    claim_result: SimulationDispatchClaimResult | None = None
    claim_write_result: WorkflowRunWriteResult | None = None

    def __post_init__(self) -> None:
        if type(self.request) is not SimulationDispatchControlRequest:
            raise TypeError("request must be SimulationDispatchControlRequest")
        if type(self.stage) is not SimulationDispatchControlFailureStage:
            raise TypeError("stage must be SimulationDispatchControlFailureStage")
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of strings")
        if not self.diagnostics or any(not value for value in self.diagnostics):
            raise ValueError("diagnostics must contain nonempty strings")
        if len(set(self.diagnostics)) != len(self.diagnostics):
            raise ValueError("diagnostics must not contain duplicates")
        optional = (
            (
                self.preparation_result,
                SimulationDispatchPreparationResult,
                "preparation_result",
            ),
            (
                self.preparation_write_result,
                WorkflowRunWriteResult,
                "preparation_write_result",
            ),
            (self.claim_result, SimulationDispatchClaimResult, "claim_result"),
            (
                self.claim_write_result,
                WorkflowRunWriteResult,
                "claim_write_result",
            ),
        )
        for value, nominal_type, name in optional:
            if value is not None and type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__} or None")
        if self.stage is SimulationDispatchControlFailureStage.PREPARATION:
            if self.preparation_result is None:
                raise ValueError("preparation failure requires preparation_result")
            return
        if self.preparation_result is None or (
            self.preparation_result.kind
            is not SimulationDispatchPreparationOutcomeKind.PREPARED
        ):
            raise ValueError("post-preparation failure requires a prepared result")
        if self.stage is (
            SimulationDispatchControlFailureStage.PREPARATION_SERIALIZATION
        ):
            return
        if self.preparation_write_result is None:
            raise ValueError("post-serialization failure requires preparation write")
        if self.stage is SimulationDispatchControlFailureStage.PREPARATION_COMMIT:
            return
        if self.preparation_write_result.status != "committed":
            raise ValueError("claim-stage failure requires committed preparation")
        if self.claim_result is None:
            raise ValueError("claim-stage failure requires claim_result")
        if self.stage in {
            SimulationDispatchControlFailureStage.CLAIM,
            SimulationDispatchControlFailureStage.CLAIM_SERIALIZATION,
        }:
            return
        if self.claim_write_result is None:
            raise ValueError("post-claim serialization failure requires claim write")


@dataclass(frozen=True, slots=True)
@final
class SimulationDispatchControlWorkflow:
    """Persist one reservation and claim before authorized effect dispatch.

    Parameters
    ----------
    repository, serializer
        Exact persistence dependencies for reservation, claim, and dispatch entry.
    runtime_bundle
        Exact immutable replay dependencies used at every advancement gate.
    authorizer
        Effect-free preparation, claim, and immediate dispatch authorizer.
    effect
        Exact application-supplied simulation effect entered at most once.

    Notes
    -----
    This Workflow is generic and calculator-independent. It performs no grant
    issuance, authority-source access, retry, result ingress, CPN result firing,
    scientific interpretation, or acceptance.
    """

    repository: WorkflowRunRepository
    serializer: WorkflowRunSerializer
    runtime_bundle: WorkflowRuntimeBundle
    authorizer: SimulationExecutionAuthorizer
    effect: SimulationDispatchEffect

    def __post_init__(self) -> None:
        if not isinstance(self.repository, WorkflowRunRepository):
            raise TypeError("repository must implement WorkflowRunRepository")
        if type(self.serializer) is not WorkflowRunSerializer:
            raise TypeError("serializer must be WorkflowRunSerializer")
        if type(self.runtime_bundle) is not WorkflowRuntimeBundle:
            raise TypeError("runtime_bundle must be WorkflowRuntimeBundle")
        if type(self.authorizer) is not SimulationExecutionAuthorizer:
            raise TypeError("authorizer must be SimulationExecutionAuthorizer")
        if not isinstance(self.effect, SimulationDispatchEffect):
            raise TypeError("effect must implement SimulationDispatchEffect")

    def execute(
        self, request: SimulationDispatchControlRequest
    ) -> SimulationDispatchAdapterResult | SimulationDispatchControlFailure:
        """Persist reservation and claim, then attempt one authorized dispatch."""
        if type(request) is not SimulationDispatchControlRequest:
            raise TypeError("request must be SimulationDispatchControlRequest")
        replayer = WorkflowRunReplayer()
        preparation = SimulationDispatchPreparer(self.authorizer, replayer).execute(
            request.preparation_request
        )
        if preparation.kind is not SimulationDispatchPreparationOutcomeKind.PREPARED:
            return self._failure(
                request,
                SimulationDispatchControlFailureStage.PREPARATION,
                preparation.diagnostics,
                preparation_result=preparation,
            )
        candidate = preparation.candidate_run
        assert candidate is not None
        preparation_write = self._commit(
            candidate,
            request.preparation_request.predecessor_run.revision_identity,
            request.preparation_commit_binding,
        )
        if preparation_write is None:
            return self._failure(
                request,
                SimulationDispatchControlFailureStage.PREPARATION_SERIALIZATION,
                ("prepared candidate could not be serialized",),
                preparation_result=preparation,
            )
        if not self._commit_agrees(
            preparation_write, candidate, request.preparation_commit_binding
        ):
            return self._failure(
                request,
                SimulationDispatchControlFailureStage.PREPARATION_COMMIT,
                ("prepared candidate commit was not exactly acknowledged",),
                preparation_result=preparation,
                preparation_write_result=preparation_write,
            )
        execution_request = self._execution_request(preparation)
        claim_request = SimulationDispatchClaimRequest(
            predecessor_run=candidate,
            runtime_bundle=self.runtime_bundle,
            execution_request=execution_request,
            claim_authorization_request=request.claim_authorization_request,
            next_revision_identity=request.claim_revision_identity,
            claimed_reservation_identity=request.claimed_reservation_identity,
        )
        claim = SimulationDispatchClaimPreparer(self.authorizer, replayer).execute(
            claim_request
        )
        if claim.kind is not SimulationDispatchClaimOutcomeKind.CLAIMED:
            return self._failure(
                request,
                SimulationDispatchControlFailureStage.CLAIM,
                claim.diagnostics,
                preparation_result=preparation,
                preparation_write_result=preparation_write,
                claim_result=claim,
            )
        claim_candidate = claim.candidate_run
        assert claim_candidate is not None
        claim_write = self._commit(
            claim_candidate,
            candidate.revision_identity,
            request.claim_commit_binding,
        )
        if claim_write is None:
            return self._failure(
                request,
                SimulationDispatchControlFailureStage.CLAIM_SERIALIZATION,
                ("claimed candidate could not be serialized",),
                preparation_result=preparation,
                preparation_write_result=preparation_write,
                claim_result=claim,
            )
        if not self._commit_agrees(
            claim_write, claim_candidate, request.claim_commit_binding
        ):
            return self._failure(
                request,
                SimulationDispatchControlFailureStage.CLAIM_COMMIT,
                ("claimed candidate commit was not exactly acknowledged",),
                preparation_result=preparation,
                preparation_write_result=preparation_write,
                claim_result=claim,
                claim_write_result=claim_write,
            )
        claimed = claim.claimed_reservation
        assert claimed is not None
        receipts = tuple(
            value
            for value in claim_write.claim_receipts
            if value.claimed_reservation_identity == claimed.identity
            and value.claim_authorization_result_identity
            == request.claim_authorization_request.result_identity
        )
        if len(receipts) != 1:
            return self._failure(
                request,
                SimulationDispatchControlFailureStage.CLAIM_RECEIPT,
                ("claim commit did not return one exact claim receipt",),
                preparation_result=preparation,
                preparation_write_result=preparation_write,
                claim_result=claim,
                claim_write_result=claim_write,
            )
        dispatch_request = SimulationDispatchRequest(
            execution_request=execution_request,
            claim_authorization_request=request.claim_authorization_request,
            claimed_reservation=claimed,
            claim_commit_receipt=receipts[0],
            outcome_identity=request.dispatch_outcome_identity,
            dispatch_entry_identity=request.dispatch_entry_identity,
            dispatch_entry_revision_identity=request.dispatch_entry_revision_identity,
        )
        return SimulationDispatchAdapter(
            authorizer=self.authorizer,
            entry_committer=WorkflowRunDispatchEntryCommitter(
                repository=self.repository,
                serializer=self.serializer,
                runtime_bundle=self.runtime_bundle,
            ),
            effect=self.effect,
        ).execute(dispatch_request)

    def _commit(
        self,
        candidate: WorkflowRun,
        predecessor_revision_identity: WorkflowRunRevisionIdentity,
        binding: WorkflowRunCommitBinding,
    ) -> WorkflowRunWriteResult | None:
        """Serialize and submit one exact candidate without retry."""
        if type(candidate) is not WorkflowRun:
            raise TypeError("candidate must be WorkflowRun")
        encoded = self.serializer.serialize(candidate, binding)
        if encoded.status != "encoded" or encoded.encoded is None:
            return None
        wire = encoded.encoded
        return self.repository.commit(
            WorkflowRunTransaction(
                binding=binding,
                run_identity=candidate.identity,
                expected_predecessor_revision_identity=predecessor_revision_identity,
                candidate=candidate,
                schema_identity=wire.schema_identity,
                content_identity=wire.content_identity,
            )
        )

    @staticmethod
    def _commit_agrees(
        result: WorkflowRunWriteResult,
        candidate: WorkflowRun,
        binding: WorkflowRunCommitBinding,
    ) -> bool:
        """Return whether one commit exactly acknowledged its supplied candidate."""
        if type(candidate) is not WorkflowRun:
            raise TypeError("candidate must be WorkflowRun")
        return (
            result.status == "committed"
            and result.snapshot is not None
            and result.snapshot.run == candidate
            and result.snapshot.binding == binding
            and result.transaction.candidate == candidate
            and result.transaction.binding == binding
        )

    @staticmethod
    def _execution_request(
        preparation: SimulationDispatchPreparationResult,
    ) -> SimulationExecutionRequest:
        """Construct the exact execution request from one prepared candidate."""
        candidate = preparation.candidate_run
        authorization = preparation.authorization_result
        assert candidate is not None
        assert authorization is not None
        source = preparation.request
        correlation = tuple(
            value
            for value in candidate.execution_request_correlations
            if value.identity == source.request_correlation_identity
        )
        obligation = tuple(
            value
            for value in candidate.dispatch_obligations
            if value.identity == source.authorization_request.obligation_identity
        )
        if len(correlation) != 1 or len(obligation) != 1:
            raise ValueError("prepared candidate lacks exact execution request records")
        return SimulationExecutionRequest(
            correlation=correlation[0],
            obligation=obligation[0],
            preparation_authorization=authorization,
        )

    @staticmethod
    def _failure(
        request: SimulationDispatchControlRequest,
        stage: SimulationDispatchControlFailureStage,
        diagnostics: tuple[str, ...],
        *,
        preparation_result: SimulationDispatchPreparationResult | None = None,
        preparation_write_result: WorkflowRunWriteResult | None = None,
        claim_result: SimulationDispatchClaimResult | None = None,
        claim_write_result: WorkflowRunWriteResult | None = None,
    ) -> SimulationDispatchControlFailure:
        """Construct one closed lifecycle failure result."""
        return SimulationDispatchControlFailure(
            request=request,
            stage=stage,
            diagnostics=diagnostics,
            preparation_result=preparation_result,
            preparation_write_result=preparation_write_result,
            claim_result=claim_result,
            claim_write_result=claim_write_result,
        )
