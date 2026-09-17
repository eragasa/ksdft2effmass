r"""Software verification of ``WorkflowRunWriteResult``.

Bounded artifact scope: closed commit outcomes and complete retained evidence.

Evidence profile: claim_bearing

Facet and represented meaning

Committed alone carries a snapshot; pre-store rejection has no commit result.

Intrinsic and cross-object scope

Record variants use synthetic genesis and actual supported claim receipt inputs from
a real isolated SQLite lifecycle. Repository tests own acknowledgement and derivation.

VVUQ and scientific exclusions

Software verification of synthetic inputs, not durability, execution or science.
"""

from dataclasses import FrozenInstanceError, replace
from typing import Literal

import pytest
from ksdft2effmass.persistence import CommitResult, CommitStatus
from ksdft2effmass.workflows import (
    WorkflowPersistenceFailure,
    WorkflowRunLoadResult,
    WorkflowRunSnapshot,
    WorkflowRunTransaction,
    WorkflowRunWriteResult,
)

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunWriteResult


class TestWorkflowRunWriteResult:
    """Closed write evidence, not repository acknowledgement verification."""

    def test_constructor__committed__retains_actual_claim_receipt_tuple(
        self,
        persisted_claim_write: WorkflowRunWriteResult,
    ) -> None:
        """Evidence ID: SV-WFR-WRITE-007

        Requirement: Committed preserves complete newly appended historical receipts.

        Method: Reconstruct the container from a real acknowledged claim write.

        Oracle: Supplied complete transaction/snapshot/evidence and immutable receipt
        tuple.

        Acceptance: Exact tuple, snapshot and complete acknowledgement remain retained.

        Interpretation: The result container neither regenerates nor discards receipts.

        Limitations: Independent repository evidence owns historical digest derivation.
        """
        value = replace(persisted_claim_write)
        assert value.claim_receipts is persisted_claim_write.claim_receipts
        assert len(value.claim_receipts) == 1
        assert value.snapshot is persisted_claim_write.snapshot
        assert value.store_result is persisted_claim_write.store_result
        assert (
            value.claim_receipts[0].commit_idempotency_identity
            == value.transaction.commit_idempotency_identity
        )

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("duplicate", id="duplicate_receipt_identity"),
            pytest.param("conflicting_duplicate", id="same_identity_changed_binding"),
            pytest.param("failure", id="error_carries_claim_receipt"),
            pytest.param("conflict", id="conflict_carries_claim_receipt"),
        ],
    )
    def test_constructor__receipts__rejects_duplicate_or_failed_receipt_claims(
        self,
        persisted_claim_write: WorkflowRunWriteResult,
        record_failure: WorkflowPersistenceFailure,
        variant: str,
    ) -> None:
        """Evidence ID: SV-WFR-WRITE-008

        Requirement: Receipt identities cannot repeat and failures carry no receipts.

        Method: Duplicate an actual receipt or attach it to failed shared evidence.

        Oracle: Unique receipt identity and success-only receipt tuple contracts.

        Acceptance: Every named invalid construction raises ValueError.

        Interpretation: Changed receipt content cannot evade duplicate identity checks.

        Limitations: This constructor does not authenticate supplied receipt contents.
        """
        receipt = persisted_claim_write.claim_receipts[0]
        with pytest.raises(ValueError):
            if variant in ("duplicate", "conflicting_duplicate"):
                second = (
                    receipt
                    if variant == "duplicate"
                    else replace(receipt, commit_idempotency_identity="other-key")
                )
                replace(persisted_claim_write, claim_receipts=(receipt, second))
            elif variant == "failure":
                replace(
                    persisted_claim_write,
                    status="error",
                    snapshot=None,
                    failure=record_failure,
                )
            else:
                shared = CommitResult(
                    result_id="conflict",
                    idempotency_id="claimed-key",
                    stream_id="run",
                    store_implementation_id="fixture",
                    store_version_id="1",
                    status=CommitStatus.CONFLICT,
                    diagnostics=(),
                    claim_boundary="synthetic conflict",
                    conflict_code="stale",
                    expected_revision_id="prepared",
                    observed_revision_id="claimed",
                )
                replace(
                    persisted_claim_write,
                    status="conflict",
                    snapshot=None,
                    store_result=shared,
                )

    @staticmethod
    def make_committed(
        transaction: WorkflowRunTransaction, snapshot: WorkflowRunSnapshot
    ) -> WorkflowRunWriteResult:
        return WorkflowRunWriteResult(
            status="committed",
            transaction=transaction,
            snapshot=snapshot,
            store_result=CommitResult(
                result_id="commit-result",
                idempotency_id="genesis-key",
                stream_id="run",
                store_implementation_id="fixture-store",
                store_version_id="fixture:1",
                status=CommitStatus.COMMITTED,
                diagnostics=("synthetic acknowledgement",),
                claim_boundary="supplied record; no executed commit",
                revision=snapshot.revision,
            ),
        )

    def test_constructor__committed__retains_complete_evidence(
        self,
        genesis_transaction: WorkflowRunTransaction,
        genesis_snapshot: WorkflowRunSnapshot,
    ) -> None:
        """Evidence ID: SV-WFR-WRITE-001

        Requirement: Committed retains complete transaction, snapshot and shared result.

        Method: Construct a committed-shaped result from independent genesis records.

        Oracle: Supplied complete records and the no-claim genesis boundary.

        Acceptance: Transaction/snapshot persist; complete acknowledgement is retained.

        Interpretation: Record construction is not an observed store commit.

        Limitations: No acknowledged candidate substitution or receipt derivation test.
        """
        value = self.make_committed(genesis_transaction, genesis_snapshot)
        assert value.transaction is genesis_transaction
        assert value.snapshot is genesis_snapshot
        assert value.store_result is not None
        assert value.store_result.result_id == "commit-result"
        assert value.store_result.idempotency_id == "genesis-key"
        assert value.store_result.revision is genesis_snapshot.revision
        assert value.claim_receipts == ()
        assert value.failure is None

    def test_constructor__conflict__preserves_shared_observations(
        self, genesis_transaction: WorkflowRunTransaction
    ) -> None:
        """Evidence ID: SV-WFR-WRITE-002

        Requirement: Conflict requires and preserves complete shared conflict evidence.

        Method: Supply explicit expected/observed revision slots and conflict code.

        Oracle: Independent fixed shared conflict record.

        Acceptance: Shared result retains identity and no snapshot or receipt appears.

        Interpretation: A failed write cannot become a committed snapshot.

        Limitations: Compare-and-swap execution belongs to the shared store.
        """
        shared = CommitResult(
            result_id="conflict-result",
            idempotency_id="genesis-key",
            stream_id="run",
            store_implementation_id="fixture-store",
            store_version_id="fixture:1",
            status=CommitStatus.CONFLICT,
            diagnostics=(),
            claim_boundary="synthetic conflict record",
            conflict_code="head_changed",
            expected_revision_id=None,
            observed_revision_id="other-head",
        )
        value = WorkflowRunWriteResult(
            status="conflict", transaction=genesis_transaction, store_result=shared
        )
        assert value.store_result is shared
        assert value.snapshot is None
        assert value.claim_receipts == ()

    @pytest.mark.parametrize(
        "status",
        [
            pytest.param("invalid", id="candidate_rejected_before_store"),
            pytest.param("incompatible", id="version_rejected_before_store"),
            pytest.param("indeterminate", id="uncertain_commit"),
            pytest.param("error", id="operational_error"),
        ],
    )
    def test_constructor__nonsuccess__retains_domain_and_read_evidence(
        self,
        genesis_transaction: WorkflowRunTransaction,
        genesis_load: WorkflowRunLoadResult,
        record_failure: WorkflowPersistenceFailure,
        status: Literal["invalid", "incompatible", "indeterminate", "error"],
    ) -> None:
        """Evidence ID: SV-WFR-WRITE-003

        Requirement: Domain rejection preserves preceding read and failure evidence.

        Method: Construct each named failure using complete supplied records.

        Oracle: Reviewed status vocabulary and retained predecessor-load field.

        Acceptance: Failure/read persist with no invented commit, snapshot or receipt.

        Interpretation: A predecessor observation is not a write acknowledgement.

        Limitations: This constructor does not perform or classify an operation.
        """
        value = WorkflowRunWriteResult(
            status=status,
            transaction=genesis_transaction,
            predecessor_load=genesis_load,
            failure=record_failure,
        )
        assert value.status == status
        assert value.predecessor_load is genesis_load
        assert value.failure is record_failure
        assert value.store_result is None
        assert value.snapshot is None
        assert value.claim_receipts == ()

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("no_snapshot", id="committed_without_snapshot"),
            pytest.param("no_ack", id="committed_without_acknowledgement"),
            pytest.param("mixed", id="committed_with_failure"),
            pytest.param("failure_snapshot", id="error_with_snapshot"),
            pytest.param("prestore_ack", id="prestore_rejection_with_commit_result"),
            pytest.param("bare_conflict", id="conflict_without_shared_evidence"),
            pytest.param("bare_error", id="error_without_evidence"),
            pytest.param("unknown", id="unknown_status"),
        ],
    )
    def test_constructor__variant__rejects_invalid_evidence(
        self,
        variant: str,
        genesis_transaction: WorkflowRunTransaction,
        genesis_snapshot: WorkflowRunSnapshot,
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-WRITE-004

        Requirement: Unknown, mixed and unsupported write claims are invalid.

        Method: Remove required evidence or attach prohibited fields independently.

        Oracle: Closed committed/conflict/pre-store/nonsuccess field contract.

        Acceptance: Every invalid variant raises ValueError.

        Interpretation: Domain failure alone cannot establish a shared conflict.

        Limitations: Matching a real acknowledgement remains repository work.
        """
        value = self.make_committed(genesis_transaction, genesis_snapshot)
        with pytest.raises(ValueError):
            if variant == "no_snapshot":
                replace(value, snapshot=None)
            elif variant == "no_ack":
                replace(value, store_result=None)
            elif variant == "mixed":
                replace(value, failure=record_failure)
            elif variant == "failure_snapshot":
                replace(value, status="error", failure=record_failure)
            elif variant == "prestore_ack":
                replace(value, status="invalid", snapshot=None, failure=record_failure)
            elif variant == "bare_conflict":
                WorkflowRunWriteResult(
                    status="conflict",
                    transaction=genesis_transaction,
                    failure=record_failure,
                )
            elif variant == "bare_error":
                WorkflowRunWriteResult(status="error", transaction=genesis_transaction)
            else:
                replace(value, status="unknown")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("transaction", id="transaction_label_only"),
            pytest.param("store_result", id="commit_label_only"),
            pytest.param("predecessor_load", id="read_label_only"),
            pytest.param("snapshot", id="snapshot_label_only"),
            pytest.param("claim_receipts", id="mutable_receipt_collection"),
            pytest.param("failure", id="failure_text_only"),
            pytest.param("status", id="boolean_status"),
        ],
    )
    def test_constructor__types__rejects_wrong_fields(
        self,
        field: str,
        genesis_transaction: WorkflowRunTransaction,
        genesis_snapshot: WorkflowRunSnapshot,
    ) -> None:
        """Evidence ID: SV-WFR-WRITE-005

        Requirement: Write result fields have concrete immutable semantic types.

        Method: Replace one field with a closed explicit wrong-type input.

        Oracle: Declared concrete record and immutable receipt tuple contracts.

        Acceptance: Each wrong-type replacement raises TypeError.

        Interpretation: Mutable collections cannot become maintained receipts.

        Limitations: This does not establish correctness of receipt contents.
        """
        value = self.make_committed(genesis_transaction, genesis_snapshot)
        with pytest.raises(TypeError):
            if field == "transaction":
                replace(value, transaction="transaction")  # type: ignore[arg-type]
            elif field == "store_result":
                replace(value, store_result="result")  # type: ignore[arg-type]
            elif field == "predecessor_load":
                replace(value, predecessor_load="read")  # type: ignore[arg-type]
            elif field == "snapshot":
                replace(value, snapshot="snapshot")  # type: ignore[arg-type]
            elif field == "claim_receipts":
                replace(value, claim_receipts=[])  # type: ignore[arg-type]
            elif field == "failure":
                replace(value, failure="failure")  # type: ignore[arg-type]
            else:
                replace(value, status=True)  # type: ignore[arg-type]

    def test_field__status__is_immutable(
        self,
        genesis_transaction: WorkflowRunTransaction,
        record_failure: WorkflowPersistenceFailure,
    ) -> None:
        """Evidence ID: SV-WFR-WRITE-006

        Requirement: A failed write outcome cannot be relabeled in place.

        Method: Attempt status assignment on a represented error.

        Oracle: Frozen dataclass semantics and original status.

        Acceptance: FrozenInstanceError occurs and status remains error.

        Interpretation: Ordinary assignment cannot manufacture acknowledgement.

        Limitations: No effect-entry permission follows from this result record.
        """
        value = WorkflowRunWriteResult(
            status="error", transaction=genesis_transaction, failure=record_failure
        )
        with pytest.raises(FrozenInstanceError):
            value.status = "committed"  # type: ignore[misc]
        assert value.status == "error"
