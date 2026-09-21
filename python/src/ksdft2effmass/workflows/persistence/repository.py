"""WorkflowRun repository protocol and atomic revision-store composition."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Literal, Protocol, cast, runtime_checkable
from uuid import uuid4

from ksdft2effmass.persistence import (
    AtomicRevisionStore,
    Commit,
    CommitResult,
    CommitStatus,
    Revision,
    RevisionReadRequest,
    RevisionReadResult,
    RevisionReadStatus,
    RevisionSelector,
)
from ksdft2effmass.workflows.runs.records import (
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeKind,
)

from ..model import (
    WorkflowRunIdentity,
)
from ..runs.authority import WorkflowRunClaimCommitReceipt
from ..runs.identities import (
    AuthorityReservationOutcomeIdentity,
    WorkflowRunClaimCommitReceiptIdentity,
    WorkflowRunRevisionIdentity,
)
from ..runs.replay import _WorkflowRunStructureValidator
from .records import (
    WorkflowPersistenceFailure,
    WorkflowPersistenceFailureCode,
    WorkflowRunClaimLoadResult,
    WorkflowRunLoadResult,
    WorkflowRunSnapshot,
    WorkflowRunTransaction,
    WorkflowRunWriteResult,
)
from .serialization.run import WorkflowRunSerializer
from .validation import WorkflowRunTransactionValidator


@runtime_checkable
class WorkflowRunRepository(Protocol):
    """Domain repository port; observations never grant advancement or effects."""

    def load(self, request: RevisionReadRequest) -> WorkflowRunLoadResult:
        """Read one exact request and return complete structurally checked evidence.

        Parameters
        ----------
        request
            Explicit stream and latest-or-revision selector with optional expectations.

        Returns
        -------
        WorkflowRunLoadResult
            Closed observation; only loaded contains a complete snapshot.
        """
        ...

    def commit(self, transaction: WorkflowRunTransaction) -> WorkflowRunWriteResult:
        """Validate and submit one complete transaction, without retry or replay.

        Parameters
        ----------
        transaction
            Complete candidate and exact predecessor, schema, content and key binding.

        Returns
        -------
        WorkflowRunWriteResult
            Closed write observation retaining underlying store evidence.
        """
        ...

    def load_claim(
        self,
        request: RevisionReadRequest,
        claimed_reservation_identity: AuthorityReservationOutcomeIdentity,
    ) -> WorkflowRunClaimLoadResult:
        """Reconcile historical commitment, never effect permission.

        Parameters
        ----------
        request
            Explicit revision with the complete reconciliation expectation group.
        claimed_reservation_identity
            Exact CLAIMED record selector in that historical revision.

        Returns
        -------
        WorkflowRunClaimLoadResult
            Historical snapshot and deterministically reconstructed receipt on loaded.
        """
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunAtomicRepository:
    """Bind complete WorkflowRun values to one explicit atomic store.

    Parameters
    ----------
    store
        Explicit structural AtomicRevisionStore dependency. No database is selected
        implicitly, and no native artifact or development storage is accessed.
    serializer
        Exact immutable serializer with the selected outward result codec.
    validator
        Exact transaction validator bound to this same serializer instance. Detached
        validators or differently configured serialization dependencies are rejected.

    Raises
    ------
    TypeError
        A dependency does not have its declared semantic type.
    ValueError
        The validator is not bound to this serializer instance.

    Notes
    -----
    Reads check shared request/address correlation, schema, SHA-256 content, complete
    reconstruction and structural closure; they do not compute replay equality.
    Writes read the exact predecessor (not latest), validate immutable extension and
    submit once. Shared CAS and idempotency decide committed versus conflict, including
    replay after later heads. No uncertainty authorizes automatic retry.

    Claim receipts require an exact current-in-that-revision CLAIMED record. The same
    versioned compact-JSON SHA-256 derivation serves acknowledged writes and confirmed
    complete-expectation reads. Persisted transaction, key and historical writer labels
    participate; fresh store result UUIDs do not. Labels establish consistency, not
    authentication, authority or permission to enter an external effect.
    """

    store: AtomicRevisionStore
    serializer: WorkflowRunSerializer
    validator: WorkflowRunTransactionValidator

    def __post_init__(self) -> None:
        """Require explicitly bound domain dependencies."""
        if not isinstance(self.store, AtomicRevisionStore):
            raise TypeError("store must implement AtomicRevisionStore")
        if type(self.serializer) is not WorkflowRunSerializer:
            raise TypeError("serializer must be WorkflowRunSerializer")
        if type(self.validator) is not WorkflowRunTransactionValidator:
            raise TypeError("validator must be WorkflowRunTransactionValidator")
        if self.validator.serializer is not self.serializer:
            raise ValueError("validator must bind the repository serializer")

    def load(self, request: RevisionReadRequest) -> WorkflowRunLoadResult:
        """Issue one read and verify its exact envelope and complete domain value.

        Parameters
        ----------
        request
            Exact shared request; complete expectations require explicit confirmation.

        Returns
        -------
        WorkflowRunLoadResult
            Loaded, absent, mismatch, incompatible, corrupt, indeterminate or error.
            Shared observations are retained even when domain binding fails.

        Raises
        ------
        TypeError
            The direct argument is not an exact RevisionReadRequest.
        """
        if type(request) is not RevisionReadRequest:
            raise TypeError("request must be RevisionReadRequest")
        observed: RevisionReadResult | None = None
        try:
            observed = self.store.read(request)
            if type(observed) is not RevisionReadResult:
                observed = None
                raise TypeError("store returned a wrong read type")
            return self._load_observation(request, observed)
        except Exception:
            return WorkflowRunLoadResult(
                status="error",
                request=request,
                store_result=observed,
                failure=self._failure(
                    "load",
                    "read boundary did not complete",
                    WorkflowPersistenceFailureCode.CODEC_ERROR,
                ),
            )

    def _load_observation(
        self, request: RevisionReadRequest, observed: RevisionReadResult
    ) -> WorkflowRunLoadResult:
        if (
            observed.request_id != request.request_id
            or observed.stream_id != request.stream_id
            or observed.selector is not request.selector
            or (
                observed.requested_revision_id is not None
                and observed.requested_revision_id != request.revision_id
            )
        ):
            return WorkflowRunLoadResult(
                status="error",
                request=request,
                store_result=observed,
                failure=self._failure("load", "substituted shared read response"),
            )
        if observed.status is not RevisionReadStatus.FOUND:
            return WorkflowRunLoadResult(
                status=cast(
                    Literal[
                        "absent",
                        "mismatch",
                        "incompatible",
                        "corrupt",
                        "indeterminate",
                        "error",
                    ],
                    observed.status.value,
                ),
                request=request,
                store_result=observed,
            )
        revision = observed.revision
        assert revision is not None
        if revision.stream_id != request.stream_id or (
            request.selector is RevisionSelector.EXPLICIT_REVISION
            and revision.revision_id != request.revision_id
        ):
            return WorkflowRunLoadResult(
                status="error",
                request=request,
                store_result=observed,
                failure=self._failure("load", "substituted revision address"),
            )
        if request.has_reconciliation_expectations and (
            observed.expectations_matched is not True
        ):
            return WorkflowRunLoadResult(
                status="error",
                request=request,
                store_result=observed,
                failure=self._failure("load", "missing store expectation confirmation"),
            )
        if request.has_reconciliation_expectations and (
            revision.predecessor_revision_id != request.expected_predecessor_revision_id
            or revision.schema_id != request.expected_schema_id
            or revision.content_id != request.expected_content_id
        ):
            return WorkflowRunLoadResult(
                status="corrupt",
                request=request,
                store_result=observed,
                failure=self._failure("load", "confirmed envelope expectations differ"),
            )
        if revision.schema_id != "ksdft2effmass.workflow-run:1":
            return WorkflowRunLoadResult(
                status="incompatible",
                request=request,
                store_result=observed,
                failure=self._failure(
                    "load",
                    "unsupported revision schema",
                    WorkflowPersistenceFailureCode.UNSUPPORTED_VERSION,
                ),
            )
        if revision.content_id != (
            revision.schema_id
            + ":sha256:"
            + hashlib.sha256(revision.payload).hexdigest()
        ):
            return WorkflowRunLoadResult(
                status="corrupt",
                request=request,
                store_result=observed,
                failure=self._failure(
                    "load",
                    "revision content digest differs",
                    WorkflowPersistenceFailureCode.CONTENT_MISMATCH,
                ),
            )
        decoded = self.serializer.deserialize(revision.payload)
        if decoded.status != "decoded":
            return WorkflowRunLoadResult(
                status=decoded.status,
                request=request,
                store_result=observed,
                failure=decoded.failure,
            )
        run, binding = decoded.run, decoded.binding
        assert run is not None and binding is not None
        predecessor = run.predecessor_revision_identity
        if (
            run.identity.value != revision.stream_id
            or run.revision_identity.value != revision.revision_id
            or (None if predecessor is None else predecessor.value)
            != revision.predecessor_revision_id
            or (
                request.has_reconciliation_expectations
                and binding.commit_idempotency_identity
                != request.expected_idempotency_id
            )
        ):
            return WorkflowRunLoadResult(
                status="corrupt",
                request=request,
                store_result=observed,
                failure=self._failure("load", "decoded aggregate binding differs"),
            )
        issue = _WorkflowRunStructureValidator().execute(run)
        if issue is not None:
            return WorkflowRunLoadResult(
                status="corrupt",
                request=request,
                store_result=observed,
                failure=self._failure(
                    "load",
                    "aggregate structural closure failed",
                    WorkflowPersistenceFailureCode.INVARIANT_VIOLATION,
                ),
            )
        return WorkflowRunLoadResult(
            status="loaded",
            request=request,
            store_result=observed,
            snapshot=WorkflowRunSnapshot(run=run, binding=binding, revision=revision),
        )

    def commit(self, transaction: WorkflowRunTransaction) -> WorkflowRunWriteResult:
        """Validate exact bytes and historical extension, then submit one Commit.

        Parameters
        ----------
        transaction
            Exact immutable transaction. A non-genesis predecessor is explicitly read.

        Returns
        -------
        WorkflowRunWriteResult
            Committed with snapshot and newly appended historical claim receipts only
            after exact acknowledgement; otherwise conflict, indeterminate, error,
            invalid or incompatible, without a snapshot or receipt.

        Raises
        ------
        TypeError
            The direct argument is not an exact WorkflowRunTransaction.
        """
        if type(transaction) is not WorkflowRunTransaction:
            raise TypeError("transaction must be WorkflowRunTransaction")
        predecessor_load: WorkflowRunLoadResult | None = None
        observed: CommitResult | None = None
        try:
            predecessor: WorkflowRunSnapshot | None = None
            expected = transaction.expected_predecessor_revision_identity
            if expected is not None:
                predecessor_load = self.load(
                    RevisionReadRequest(
                        request_id=str(uuid4()),
                        stream_id=transaction.run_identity.value,
                        selector=RevisionSelector.EXPLICIT_REVISION,
                        revision_id=expected.value,
                    )
                )
                if predecessor_load.status != "loaded":
                    status: Literal["invalid", "incompatible", "indeterminate", "error"]
                    if predecessor_load.status in (
                        "incompatible",
                        "indeterminate",
                        "error",
                    ):
                        status = predecessor_load.status
                    else:
                        status = "invalid"
                    return WorkflowRunWriteResult(
                        status=status,
                        transaction=transaction,
                        predecessor_load=predecessor_load,
                        failure=predecessor_load.failure
                        or self._failure("commit", "exact predecessor was not loaded"),
                    )
                predecessor = predecessor_load.snapshot
            validation = self.validator.execute(transaction, predecessor)
            if validation.status != "valid":
                return WorkflowRunWriteResult(
                    status=validation.status,
                    transaction=transaction,
                    predecessor_load=predecessor_load,
                    failure=validation.failure,
                )
            # Independently bind the exact transaction to the validated bytes at the
            # submission seam. No detached successful validation can swap a candidate.
            encoded = self.serializer.serialize(
                transaction.candidate, transaction.binding
            )
            if encoded.status != "encoded":
                return WorkflowRunWriteResult(
                    status=encoded.status,
                    transaction=transaction,
                    predecessor_load=predecessor_load,
                    failure=encoded.failure,
                )
            if (
                validation.transaction is not transaction
                or validation.predecessor is not predecessor
                or encoded.encoded != validation.encoded
            ):
                return WorkflowRunWriteResult(
                    status="invalid",
                    transaction=transaction,
                    predecessor_load=predecessor_load,
                    failure=self._failure(
                        "commit", "validation/serialization binding differs"
                    ),
                )
            assert validation.encoded is not None
            wire = validation.encoded
            run = transaction.candidate
            revision = Revision(
                stream_id=transaction.run_identity.value,
                revision_id=run.revision_identity.value,
                predecessor_revision_id=None if expected is None else expected.value,
                schema_id=wire.schema_identity,
                content_id=wire.content_identity,
                payload=wire.payload,
            )
            snapshot = WorkflowRunSnapshot(
                run=run, binding=transaction.binding, revision=revision
            )
            old_claims = (
                () if predecessor is None else predecessor.run.authority_reservations
            )
            old_ids = {claim.identity for claim in old_claims}
            new_claims = tuple(
                claim
                for claim in run.authority_reservations
                if claim.kind is AuthorityReservationOutcomeKind.CLAIMED
                and claim.identity not in old_ids
            )
            if any(
                not self._claim_at_revision(snapshot, claim) for claim in new_claims
            ):
                return WorkflowRunWriteResult(
                    status="invalid",
                    transaction=transaction,
                    predecessor_load=predecessor_load,
                    failure=self._failure(
                        "commit", "new claim does not name candidate revision"
                    ),
                )
            receipts = tuple(self._receipt(snapshot, claim) for claim in new_claims)
            submitted = Commit(
                expected_revision_id=revision.predecessor_revision_id,
                candidate=revision,
                idempotency_id=transaction.commit_idempotency_identity,
            )
            observed = self.store.commit(submitted)
            if type(observed) is not CommitResult:
                observed = None
                raise TypeError("store returned a wrong commit type")
            if (
                observed.stream_id != revision.stream_id
                or observed.idempotency_id != submitted.idempotency_id
                or (
                    observed.status is CommitStatus.COMMITTED
                    and observed.revision != revision
                )
                or (
                    observed.status is CommitStatus.CONFLICT
                    and observed.expected_revision_id != submitted.expected_revision_id
                )
            ):
                return WorkflowRunWriteResult(
                    status="error",
                    transaction=transaction,
                    store_result=observed,
                    predecessor_load=predecessor_load,
                    failure=self._failure(
                        "commit", "substituted shared commit response"
                    ),
                )
            if observed.status is not CommitStatus.COMMITTED:
                return WorkflowRunWriteResult(
                    status=cast(
                        Literal["conflict", "indeterminate", "error"],
                        observed.status.value,
                    ),
                    transaction=transaction,
                    store_result=observed,
                    predecessor_load=predecessor_load,
                )
            return WorkflowRunWriteResult(
                status="committed",
                transaction=transaction,
                store_result=observed,
                predecessor_load=predecessor_load,
                snapshot=snapshot,
                claim_receipts=receipts,
            )
        except Exception:
            return WorkflowRunWriteResult(
                status="error",
                transaction=transaction,
                store_result=observed,
                predecessor_load=predecessor_load,
                failure=self._failure(
                    "commit",
                    "commit boundary did not complete",
                    WorkflowPersistenceFailureCode.CODEC_ERROR,
                ),
            )

    def load_claim(
        self,
        request: RevisionReadRequest,
        claimed_reservation_identity: AuthorityReservationOutcomeIdentity,
    ) -> WorkflowRunClaimLoadResult:
        """Confirm one historical claim through one complete-expectation read.

        Parameters
        ----------
        request
            Explicit revision and complete predecessor/schema/content/key expectations.
            Latest or incomplete requests return error before any store read.
        claimed_reservation_identity
            Exact CLAIMED record in the addressed run and revision.

        Returns
        -------
        WorkflowRunClaimLoadResult
            Same seven read statuses. Missing selected claim is mismatch; malformed or
            copied historical claim is corrupt. Only loaded has a historical receipt.

        Raises
        ------
        TypeError
            Either direct argument has the wrong exact semantic type.
        """
        if type(request) is not RevisionReadRequest:
            raise TypeError("request must be RevisionReadRequest")
        if (
            type(claimed_reservation_identity)
            is not AuthorityReservationOutcomeIdentity
        ):
            raise TypeError(
                "claim selector must be AuthorityReservationOutcomeIdentity"
            )
        if (
            request.selector is not RevisionSelector.EXPLICIT_REVISION
            or not request.has_reconciliation_expectations
        ):
            return WorkflowRunClaimLoadResult(
                status="error",
                request=request,
                claimed_reservation_identity=claimed_reservation_identity,
                failure=self._failure(
                    "load_claim", "complete historical expectations required"
                ),
            )
        loaded = self.load(request)
        if loaded.status != "loaded":
            return WorkflowRunClaimLoadResult(
                status=loaded.status,
                request=request,
                claimed_reservation_identity=claimed_reservation_identity,
                store_result=loaded.store_result,
                failure=loaded.failure,
            )
        snapshot = loaded.snapshot
        assert snapshot is not None
        claim = next(
            (
                record
                for record in snapshot.run.authority_reservations
                if record.identity == claimed_reservation_identity
            ),
            None,
        )
        if claim is None or not self._claim_at_revision(snapshot, claim):
            return WorkflowRunClaimLoadResult(
                status="mismatch" if claim is None else "corrupt",
                request=request,
                claimed_reservation_identity=claimed_reservation_identity,
                store_result=loaded.store_result,
                failure=self._failure(
                    "load_claim", "selected claim absent or not at revision"
                ),
            )
        try:
            receipt = self._receipt(snapshot, claim)
        except Exception:
            return WorkflowRunClaimLoadResult(
                status="error",
                request=request,
                claimed_reservation_identity=claimed_reservation_identity,
                store_result=loaded.store_result,
                failure=self._failure(
                    "load_claim",
                    "receipt derivation did not complete",
                    WorkflowPersistenceFailureCode.CODEC_ERROR,
                ),
            )
        return WorkflowRunClaimLoadResult(
            status="loaded",
            request=request,
            claimed_reservation_identity=claimed_reservation_identity,
            store_result=loaded.store_result,
            snapshot=snapshot,
            receipt=receipt,
        )

    @staticmethod
    def _claim_at_revision(
        snapshot: WorkflowRunSnapshot, claim: AuthorityReservationOutcome
    ) -> bool:
        # Complete authorization/reservation closure was checked by the structural
        # owner. Here bind the selected historical event to this exact revision.
        return (
            claim.kind is AuthorityReservationOutcomeKind.CLAIMED
            and claim.workflow_run_identity == snapshot.run.identity
            and claim.workflow_run_revision_identity == snapshot.run.revision_identity
            and claim.expected_revision_identity
            == snapshot.run.predecessor_revision_identity
            and snapshot.revision.predecessor_revision_id is not None
        )

    @staticmethod
    def _receipt(
        snapshot: WorkflowRunSnapshot, claim: AuthorityReservationOutcome
    ) -> WorkflowRunClaimCommitReceipt:
        binding, revision = snapshot.binding, snapshot.revision
        operation_sequence = [
            "wfr-operation-v1",
            binding.transaction_identity,
            binding.persistence_implementation_identity,
            revision.stream_id,
            revision.revision_id,
            revision.predecessor_revision_id,
            revision.schema_id,
            revision.content_id,
            binding.commit_idempotency_identity,
        ]
        operation = (
            "wfr-operation-v1:sha256:"
            + hashlib.sha256(
                json.dumps(
                    operation_sequence,
                    ensure_ascii=True,
                    separators=(",", ":"),
                    allow_nan=False,
                ).encode("ascii")
            ).hexdigest()
        )
        receipt_sequence = [
            "wfr-claim-receipt-v1",
            operation,
            claim.identity.value,
            claim.authorization_result_identity.value,
        ]
        identity = (
            "wfr-claim-receipt-v1:sha256:"
            + hashlib.sha256(
                json.dumps(
                    receipt_sequence,
                    ensure_ascii=True,
                    separators=(",", ":"),
                    allow_nan=False,
                ).encode("ascii")
            ).hexdigest()
        )
        assert revision.predecessor_revision_id is not None
        return WorkflowRunClaimCommitReceipt(
            identity=WorkflowRunClaimCommitReceiptIdentity(identity),
            workflow_run_identity=WorkflowRunIdentity(revision.stream_id),
            committed_revision_identity=WorkflowRunRevisionIdentity(
                revision.revision_id
            ),
            predecessor_revision_identity=WorkflowRunRevisionIdentity(
                revision.predecessor_revision_id
            ),
            claimed_reservation_identity=claim.identity,
            claim_authorization_result_identity=claim.authorization_result_identity,
            workflow_run_content_identity=revision.content_id,
            persistence_operation_identity=operation,
            commit_idempotency_identity=binding.commit_idempotency_identity,
            persistence_implementation_identity=binding.persistence_implementation_identity,
        )

    @staticmethod
    def _failure(
        phase: str,
        observed: str,
        code: WorkflowPersistenceFailureCode = (
            WorkflowPersistenceFailureCode.IDENTITY_MISMATCH
        ),
    ) -> WorkflowPersistenceFailure:
        return WorkflowPersistenceFailure(
            implementation_identity="ksdft2effmass.workflows.WorkflowRunAtomicRepository:1",
            phase=phase,
            code=code,
            input_identities=(),
            expected="complete correlated domain and store evidence",
            observed=observed,
            diagnostic=observed,
            claim_boundary="no advancement, effect permission or automatic retry",
        )
