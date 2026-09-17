"""Finite typed repository fault ports for synthetic entry-service evidence."""

import time
from dataclasses import replace
from pathlib import Path
from threading import Barrier
from typing import Literal

from ksdft2effmass.persistence import RevisionReadRequest
from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeIdentity,
    WorkflowRunAtomicRepository,
    WorkflowRunClaimLoadResult,
    WorkflowRunLoadResult,
    WorkflowRunRevisionIdentity,
    WorkflowRunTransaction,
    WorkflowRunWriteResult,
)

type EntryAcknowledgementMode = Literal[
    "normal", "lost_ack", "wrong_key", "wrong_snapshot", "wrong_transaction"
]
type EntryReadMode = Literal[
    "normal",
    "historical_request_id",
    "historical_binding",
    "current_request_id",
    "current_run",
]


class EntryRepositoryProbe:
    """Record submissions and inject one explicit postcommit fault or rendezvous."""

    def __init__(
        self,
        repository: WorkflowRunAtomicRepository,
        *,
        mode: EntryAcknowledgementMode = "normal",
        read_mode: EntryReadMode = "normal",
        barrier: Barrier | None = None,
        rendezvous: Path | None = None,
        participant: str = "local",
    ) -> None:
        self.repository = repository
        self.mode = mode
        self.read_mode = read_mode
        self.barrier = barrier
        self.rendezvous = rendezvous
        self.participant = participant
        self.transactions: list[WorkflowRunTransaction] = []

    def load(self, request: RevisionReadRequest) -> WorkflowRunLoadResult:
        result = self.repository.load(request)
        if self.read_mode == "current_request_id":
            assert result.store_result is not None
            return replace(
                result,
                store_result=replace(result.store_result, request_id="substituted"),
            )
        if self.read_mode == "current_run":
            assert result.snapshot is not None
            return replace(
                result,
                snapshot=replace(
                    result.snapshot,
                    run=replace(
                        result.snapshot.run,
                        revision_identity=WorkflowRunRevisionIdentity("substituted"),
                    ),
                ),
            )
        return result

    def load_claim(
        self,
        request: RevisionReadRequest,
        claimed_reservation_identity: AuthorityReservationOutcomeIdentity,
    ) -> WorkflowRunClaimLoadResult:
        result = self.repository.load_claim(request, claimed_reservation_identity)
        if self.read_mode == "historical_request_id":
            assert result.store_result is not None
            return replace(
                result,
                store_result=replace(result.store_result, request_id="substituted"),
            )
        if self.read_mode == "historical_binding":
            assert result.snapshot is not None
            return replace(
                result,
                snapshot=replace(
                    result.snapshot,
                    binding=replace(
                        result.snapshot.binding, transaction_identity="substituted"
                    ),
                ),
            )
        return result

    def commit(self, transaction: WorkflowRunTransaction) -> WorkflowRunWriteResult:
        self.transactions.append(transaction)
        if self.barrier is not None:
            self.barrier.wait(timeout=10)
        if self.rendezvous is not None:
            (self.rendezvous / f"ready-{self.participant}").touch()
            deadline = time.monotonic() + 15
            while len(tuple(self.rendezvous.glob("ready-*"))) != 2:
                if time.monotonic() > deadline:
                    raise RuntimeError("fixture rendezvous timed out")
                time.sleep(0.01)
        result = self.repository.commit(transaction)
        if self.mode == "lost_ack":
            raise RuntimeError("synthetic postcommit acknowledgement loss")
        if self.mode == "wrong_key":
            assert result.store_result is not None
            return replace(
                result,
                store_result=replace(result.store_result, idempotency_id="substituted"),
            )
        if self.mode == "wrong_snapshot":
            assert result.snapshot is not None
            return replace(
                result,
                snapshot=replace(
                    result.snapshot,
                    revision=replace(result.snapshot.revision, payload=b"substituted"),
                ),
            )
        if self.mode == "wrong_transaction":
            return replace(
                result,
                transaction=replace(
                    transaction,
                    binding=replace(
                        transaction.binding, transaction_identity="substituted"
                    ),
                ),
            )
        return result
