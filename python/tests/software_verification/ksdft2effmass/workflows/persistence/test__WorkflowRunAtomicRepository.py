r"""Software verification of ``WorkflowRunAtomicRepository``.

Bounded artifact scope: exact durable revisions and historical claim reconciliation.

Evidence profile: claim_bearing

Facet and represented meaning

Real isolated SQLite stores exercise reopen, stale CAS, replay and lost acknowledgement.
Literal prepared/claimed histories and independent receipt preimages are exact oracles.

Intrinsic and cross-object scope

The repository binds serializer, structural validator and store observations. Fault
adapters substitute finite protocol variants; no private SQLite table is modified.

VVUQ and scientific exclusions

Synthetic software verification, not replay equality, authentication, effect permission,
scientific execution, numerical verification or scientific validation.
"""

from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from typing import Literal

import pytest
from ksdft2effmass import persistence as p
from ksdft2effmass import workflows as w
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.workflows import WorkflowRunAtomicRepository

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunAtomicRepository


class TestWorkflowRunAtomicRepository:
    """Finite public-contract cases with literal durable receipt expectations."""

    class Store:
        """Record one seam and inject a named fault, delegating real durability."""

        def __init__(
            self, store: p.AtomicRevisionStore, mode: str = "ordinary"
        ) -> None:
            self.store = store
            self.mode = mode
            self.reads: list[p.RevisionReadRequest] = []
            self.commits: list[p.Commit] = []

        def read(self, request: p.RevisionReadRequest) -> p.RevisionReadResult:
            self.reads.append(request)
            if self.mode == "read_exception":
                raise RuntimeError("private text must not escape")
            result = self.store.read(request)
            if self.mode == "request":
                return replace(result, request_id="substituted")
            if self.mode == "stream" and result.revision is not None:
                return replace(
                    result,
                    stream_id="other-run",
                    revision=replace(result.revision, stream_id="other-run"),
                )
            if self.mode == "selector":
                return replace(result, selector=p.RevisionSelector.LATEST)
            if self.mode == "unconfirmed":
                return replace(result, expectations_matched=None)
            if self.mode == "revision" and result.revision is not None:
                return replace(
                    result, revision=replace(result.revision, revision_id="other")
                )
            if self.mode == "predecessor" and result.revision is not None:
                return replace(
                    result,
                    revision=replace(result.revision, predecessor_revision_id="other"),
                )
            if self.mode == "digest" and result.revision is not None:
                return replace(
                    result, revision=replace(result.revision, content_id="wrong")
                )
            if self.mode in ("incompatible", "corrupt", "indeterminate", "error"):
                return self.failure_read(request)
            return result

        def failure_read(self, request: p.RevisionReadRequest) -> p.RevisionReadResult:
            status = p.RevisionReadStatus(self.mode)
            return p.RevisionReadResult(
                result_id="fault-read",
                request_id=request.request_id,
                stream_id=request.stream_id,
                selector=request.selector,
                store_implementation_id="fault-store",
                store_version_id="fault:1",
                status=status,
                diagnostics=("retained diagnostic",),
                claim_boundary="synthetic read observation",
                unsupported_version_ids=("future",)
                if status is p.RevisionReadStatus.INCOMPATIBLE
                else (),
                compatibility_finding="unsupported"
                if status is p.RevisionReadStatus.INCOMPATIBLE
                else None,
                integrity_findings=("bad envelope",)
                if status is p.RevisionReadStatus.CORRUPT
                else (),
                failure=self.failure("read")
                if status
                in (p.RevisionReadStatus.INDETERMINATE, p.RevisionReadStatus.ERROR)
                else None,
            )

        @staticmethod
        def failure(phase: str) -> p.StoreOperationalFailure:
            return p.StoreOperationalFailure(
                failure_id="fault",
                operation_phase=phase,
                implementation_id="fault-store",
                code="injected",
                expected_condition="acknowledged observation",
                observed_condition="injected failure",
                diagnostic="sanitized",
                retryable=None,
                claim_boundary="no presence or retry conclusion",
            )

        def commit(self, commit: p.Commit) -> p.CommitResult:
            self.commits.append(commit)
            if self.mode == "before_commit":
                raise RuntimeError("private text must not escape")
            if self.mode in ("commit_indeterminate", "commit_error"):
                return p.CommitResult(
                    result_id="fault-commit",
                    idempotency_id=commit.idempotency_id,
                    stream_id=commit.candidate.stream_id,
                    store_implementation_id="fault-store",
                    store_version_id="fault:1",
                    status=p.CommitStatus(self.mode.removeprefix("commit_")),
                    diagnostics=("retained diagnostic",),
                    claim_boundary="injected failure",
                    failure=self.failure("commit"),
                )
            result = self.store.commit(commit)
            if self.mode == "lost_ack":
                raise RuntimeError("private text must not escape")
            if self.mode == "ack_key":
                return replace(result, idempotency_id="other-key")
            if self.mode == "ack_revision" and result.revision is not None:
                return replace(
                    result,
                    revision=replace(result.revision, content_id="other-content"),
                )
            return result

    @staticmethod
    def make_repository(store: p.AtomicRevisionStore) -> w.WorkflowRunAtomicRepository:
        serializer = w.WorkflowRunSerializer(
            result_codec=w.WorkflowResultValueSerializer(
                source_codec=QuantumEspressoResultValueSerializer()
            )
        )
        return SUT(
            store=store,
            serializer=serializer,
            validator=w.WorkflowRunTransactionValidator(serializer=serializer),
        )

    @classmethod
    def make_transaction(
        cls, label: Literal["prepared", "claimed"]
    ) -> w.WorkflowRunTransaction:
        name = (
            "prepared-run-v1.json" if label == "prepared" else "claim-receipt-v1.json"
        )
        payload = Path(__file__).with_name("resources").joinpath(name).read_bytes()
        serializer = w.WorkflowRunSerializer(
            result_codec=w.WorkflowResultValueSerializer(
                source_codec=QuantumEspressoResultValueSerializer()
            )
        )
        decoded = serializer.deserialize(payload)
        assert decoded.status == "decoded", decoded.failure
        assert decoded.run is not None and decoded.binding is not None
        content = (
            "e03973cea43dd84e0587c7f65f54a6f7a0a8997b1e5d823c8978b986d94e2fb5"
            if label == "prepared"
            else "b30a249018ea117d44cdf9afc83812fbc044392f023f4d1c7d50e54fe7b0fce8"
        )
        return w.WorkflowRunTransaction(
            binding=decoded.binding,
            candidate=decoded.run,
            run_identity=decoded.run.identity,
            expected_predecessor_revision_identity=decoded.run.predecessor_revision_identity,
            schema_identity="ksdft2effmass.workflow-run:1",
            content_identity="ksdft2effmass.workflow-run:1:sha256:" + content,
        )

    @classmethod
    def entry_transaction(
        cls, repo: w.WorkflowRunAtomicRepository, predecessor: w.WorkflowRunTransaction
    ) -> w.WorkflowRunTransaction:
        """Construct entry input; the retained claim names the consumed revision."""
        transaction = cls.successor(repo, predecessor, "entered")
        entry = w.SimulationDispatchEntry(
            identity=w.SimulationDispatchEntryIdentity("entry"),
            workflow_run_identity=predecessor.run_identity,
            predecessor_revision_identity=w.WorkflowRunRevisionIdentity("claimed"),
            committed_revision_identity=w.WorkflowRunRevisionIdentity("entered"),
            claimed_reservation_identity=w.AuthorityReservationOutcomeIdentity(
                "claimed"
            ),
            request_identity=w.SimulationExecutionRequestIdentity("request"),
            obligation_identity=w.ObligationIdentity("obligation"),
            receipt_identity=w.SimulationDispatchEntryReceiptIdentity("entry-receipt"),
            outcome_identity=w.SimulationDispatchOutcomeIdentity("outcome"),
        )
        return cls.rebind_candidate(
            repo, transaction, replace(transaction.candidate, dispatch_entries=(entry,))
        )

    @staticmethod
    def rebind_candidate(
        repo: w.WorkflowRunAtomicRepository,
        transaction: w.WorkflowRunTransaction,
        run: w.WorkflowRun,
    ) -> w.WorkflowRunTransaction:
        """Encode exact candidate input labels, not expected persistence outcomes."""
        encoded = repo.serializer.serialize(run, transaction.binding)
        assert encoded.encoded is not None, encoded.failure
        return replace(
            transaction,
            candidate=run,
            expected_predecessor_revision_identity=run.predecessor_revision_identity,
            content_identity=encoded.encoded.content_identity,
        )

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("committed_revision", id="entry_names_uncommitted_revision"),
            pytest.param("stale_predecessor", id="entry_consumes_noncurrent_claim"),
            pytest.param("genesis", id="entry_without_committed_predecessor"),
        ],
    )
    def test_method__commit__rejects_detached_entry_before_submission(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        variant: Literal["committed_revision", "stale_predecessor", "genesis"],
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-024

        Requirement: Incorrect entry introduction causes no shared-store submission.

        Method: Seed exact predecessor history then submit one detached entry variant.

        Oracle: New entry labels must match actual non-genesis transaction revisions.

        Acceptance: Invalid, retained transaction, no snapshot/receipt/store commit.

        Interpretation: Entry correlation checks apply at the public repository port.

        Limitations: Synthetic SQLite history, not execution permission or replay.
        """
        store = p.SQLiteAtomicRevisionStore(
            tmp_path / "entry.sqlite3", busy_timeout_ms=1000, max_payload_bytes=1048576
        )
        seed_repo = self.make_repository(store)
        predecessor = self.make_transaction("claimed")
        if variant != "genesis":
            assert self.seed(store, genesis_transaction).status == "committed"
        if variant == "stale_predecessor":
            predecessor = self.successor(seed_repo, predecessor)
            assert seed_repo.commit(predecessor).status == "committed"
        recording = self.Store(store)
        repo = self.make_repository(recording)
        transaction = self.entry_transaction(repo, predecessor)
        run = transaction.candidate
        if variant == "committed_revision":
            run = replace(
                run,
                dispatch_entries=(
                    replace(
                        run.dispatch_entries[0],
                        committed_revision_identity=w.WorkflowRunRevisionIdentity(
                            "never-committed"
                        ),
                    ),
                ),
            )
        elif variant == "genesis":
            run = replace(run, predecessor_revision_identity=None)
        transaction = self.rebind_candidate(repo, transaction, run)
        result = repo.commit(transaction)
        assert result.status == "invalid", result.failure
        assert result.transaction is transaction and result.store_result is None
        assert result.snapshot is None and result.claim_receipts == ()
        assert recording.commits == []

    def test_method__commit__retains_entry_revision_after_later_head(
        self, tmp_path: Path, genesis_transaction: w.WorkflowRunTransaction
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-025

        Requirement: A later head never rebinds a persisted entry's revision labels.

        Method: Commit entry and later revision, reopen, reload and replay entry commit.

        Oracle: Original entered revision and claimed predecessor remain unchanged.

        Acceptance: Reloaded entry bytes/labels agree; original commit replays exactly.

        Interpretation: Historical entry introduction is independent of current head.

        Limitations: Exact synthetic durability, not recovered entry permission.
        """
        path = tmp_path / "entry.sqlite3"
        store = p.SQLiteAtomicRevisionStore(
            path, busy_timeout_ms=1000, max_payload_bytes=1048576
        )
        assert self.seed(store, genesis_transaction).status == "committed"
        repo = self.make_repository(store)
        transaction = self.entry_transaction(repo, self.make_transaction("claimed"))
        written = repo.commit(transaction)
        assert written.status == "committed", written.failure
        assert written.snapshot is not None
        later = self.successor(repo, transaction, "after-entry")
        assert repo.commit(later).status == "committed"
        reopened = self.make_repository(
            p.SQLiteAtomicRevisionStore(
                path, busy_timeout_ms=1000, max_payload_bytes=1048576
            )
        )
        loaded = reopened.load(
            p.RevisionReadRequest(
                request_id="entry-reload",
                stream_id="run",
                selector=p.RevisionSelector.EXPLICIT_REVISION,
                revision_id="entered",
            )
        )
        assert loaded.status == "loaded", loaded.failure
        assert loaded.snapshot is not None
        assert loaded.snapshot.revision.payload == written.snapshot.revision.payload
        entry = loaded.snapshot.run.dispatch_entries[0]
        assert entry.predecessor_revision_identity == w.WorkflowRunRevisionIdentity(
            "claimed"
        )
        assert entry.committed_revision_identity == w.WorkflowRunRevisionIdentity(
            "entered"
        )
        replayed = reopened.commit(transaction)
        assert replayed.status == "committed", replayed.failure
        assert replayed.snapshot is not None
        assert replayed.snapshot.revision == written.snapshot.revision

    @staticmethod
    def expected_receipt() -> w.WorkflowRunClaimCommitReceipt:
        """Literal oracle independently hashed in claim-receipt-v1-expectations.json."""
        return w.WorkflowRunClaimCommitReceipt(
            identity=w.WorkflowRunClaimCommitReceiptIdentity(
                "wfr-claim-receipt-v1:sha256:d5367894f0f2ec7bd7c6a7173b457b49ac81159e25b9f01a2751086097c865eb"
            ),
            workflow_run_identity=w.WorkflowRunIdentity("run"),
            committed_revision_identity=w.WorkflowRunRevisionIdentity("claimed"),
            predecessor_revision_identity=w.WorkflowRunRevisionIdentity("prepared"),
            claimed_reservation_identity=w.AuthorityReservationOutcomeIdentity(
                "claimed"
            ),
            claim_authorization_result_identity=w.SimulationExecutionAuthorizationResultIdentity(
                "authorization-claim"
            ),
            workflow_run_content_identity="ksdft2effmass.workflow-run:1:sha256:b30a249018ea117d44cdf9afc83812fbc044392f023f4d1c7d50e54fe7b0fce8",
            persistence_operation_identity="wfr-operation-v1:sha256:4e5de8544bb7abdd09a48ec3fb51afc9e8c5e58ff8b1b3d72fd8aeed769ce71b",
            commit_idempotency_identity="claimed-key",
            persistence_implementation_identity="ksdft2effmass.workflows.WorkflowRunAtomicRepository:1",
        )

    @staticmethod
    def claim_request() -> p.RevisionReadRequest:
        return p.RevisionReadRequest(
            request_id="claim-read",
            stream_id="run",
            selector=p.RevisionSelector.EXPLICIT_REVISION,
            revision_id="claimed",
            expected_predecessor_revision_id="prepared",
            expected_schema_id="ksdft2effmass.workflow-run:1",
            expected_content_id="ksdft2effmass.workflow-run:1:sha256:b30a249018ea117d44cdf9afc83812fbc044392f023f4d1c7d50e54fe7b0fce8",
            expected_idempotency_id="claimed-key",
        )

    @classmethod
    def seed(
        cls, store: p.AtomicRevisionStore, genesis: w.WorkflowRunTransaction
    ) -> w.WorkflowRunWriteResult:
        repo = cls.make_repository(store)
        first = repo.commit(genesis)
        assert first.status == "committed", first.failure
        prepared = repo.commit(cls.make_transaction("prepared"))
        assert prepared.status == "committed", prepared.failure
        return repo.commit(cls.make_transaction("claimed"))

    @classmethod
    def successor(
        cls,
        repo: w.WorkflowRunAtomicRepository,
        transaction: w.WorkflowRunTransaction,
        revision: str = "later",
    ) -> w.WorkflowRunTransaction:
        run = replace(
            transaction.candidate,
            revision_identity=w.WorkflowRunRevisionIdentity(revision),
            predecessor_revision_identity=transaction.candidate.revision_identity,
        )
        binding = replace(
            transaction.binding,
            transaction_identity=revision + "-transaction",
            commit_idempotency_identity=revision + "-key",
        )
        encoded = repo.serializer.serialize(run, binding)
        assert encoded.encoded is not None
        return w.WorkflowRunTransaction(
            binding=binding,
            candidate=run,
            run_identity=run.identity,
            expected_predecessor_revision_identity=run.predecessor_revision_identity,
            schema_identity=encoded.encoded.schema_identity,
            content_identity=encoded.encoded.content_identity,
        )

    def test_method__commit__reopen_recovers_literal_historical_receipt(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-001

        Requirement: Acknowledged claim and restarted complete read derive one receipt.

        Method: Commit literal histories and reopen the real SQLite database.

        Oracle: Independent literal operation/receipt preimages and every receipt field.

        Acceptance: Both receipts equal the literal record, with exact confirmed bytes.

        Interpretation: Durable represented commitment survives loss of process state.

        Limitations: Historical commitment is not effect permission or replay equality.
        """
        path = tmp_path / "workflow.sqlite3"
        written = self.seed(
            p.SQLiteAtomicRevisionStore(
                path, busy_timeout_ms=1000, max_payload_bytes=1048576
            ),
            genesis_transaction,
        )
        assert written.status == "committed", written.failure
        assert written.claim_receipts == (self.expected_receipt(),)
        repo = self.make_repository(
            p.SQLiteAtomicRevisionStore(
                path, busy_timeout_ms=1000, max_payload_bytes=1048576
            )
        )
        read = repo.load_claim(
            self.claim_request(), w.AuthorityReservationOutcomeIdentity("claimed")
        )
        assert read.status == "loaded", read.failure
        assert read.receipt == self.expected_receipt()
        assert (
            read.store_result is not None
            and read.store_result.expectations_matched is True
        )
        assert read.snapshot is not None
        assert (
            read.snapshot.revision.payload
            == Path(__file__)
            .with_name("resources")
            .joinpath("claim-receipt-v1.json")
            .read_bytes()
        )

    def test_method__commit__replay_after_later_head_and_stale_cas(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-002

        Requirement: Historical idempotency is independent of current-head CAS.

        Method: Advance a real store, replay the claim, then submit a stale sibling.

        Oracle: Original receipt on replay, no receipt on later head or stale conflict.

        Acceptance: Replay is committed with fresh shared ID; sibling conflicts.

        Interpretation: Exact historical predecessor reads permit legitimate replay.

        Limitations: A copied claim in a later snapshot cannot be that revision's claim.
        """
        store = p.SQLiteAtomicRevisionStore(
            tmp_path / "workflow.sqlite3",
            busy_timeout_ms=1000,
            max_payload_bytes=1048576,
        )
        original = self.seed(store, genesis_transaction)
        repo = self.make_repository(store)
        claim = self.make_transaction("claimed")
        later = repo.commit(self.successor(repo, claim))
        assert later.status == "committed", later.failure
        assert later.claim_receipts == ()
        replay = repo.commit(claim)
        assert replay.status == "committed", replay.failure
        assert replay.claim_receipts == (self.expected_receipt(),)
        assert replay.store_result is not None and original.store_result is not None
        assert replay.store_result.result_id != original.store_result.result_id
        stale = repo.commit(self.successor(repo, claim, "sibling"))
        assert stale.status == "conflict", stale.failure
        assert stale.snapshot is None and stale.claim_receipts == ()
        historical = repo.load_claim(
            self.claim_request(), w.AuthorityReservationOutcomeIdentity("claimed")
        )
        assert historical.receipt == self.expected_receipt()
        assert later.snapshot is not None
        copied_request = replace(
            self.claim_request(),
            revision_id="later",
            expected_predecessor_revision_id="claimed",
            expected_content_id=later.snapshot.revision.content_id,
            expected_idempotency_id="later-key",
        )
        copied = repo.load_claim(
            copied_request, w.AuthorityReservationOutcomeIdentity("claimed")
        )
        assert copied.status == "corrupt" and copied.receipt is None

    @pytest.mark.parametrize(
        "mode,expected",
        [
            pytest.param("before_commit", "absent", id="failure_before_commit"),
            pytest.param("lost_ack", "loaded", id="lost_claim_acknowledgement"),
        ],
    )
    def test_method__commit__uncertainty_requires_separate_reconciliation(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        mode: str,
        expected: str,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-003

        Requirement: Exceptions yield no receipt and no implicit retry.

        Method: Inject precommit failure or postcommit lost acknowledgement in SQLite.

        Oracle: One submission and separately confirmed historical presence or absence.

        Acceptance: Error contains no receipt; restarted explicit claim read
        distinguishes.

        Interpretation: An error cannot establish whether a claim was committed.

        Limitations: No effect is entered or recovered by this reconciliation.
        """
        path = tmp_path / "workflow.sqlite3"
        store = p.SQLiteAtomicRevisionStore(
            path, busy_timeout_ms=1000, max_payload_bytes=1048576
        )
        repo = self.make_repository(store)
        assert repo.commit(genesis_transaction).status == "committed"
        assert repo.commit(self.make_transaction("prepared")).status == "committed"
        fault = self.Store(store, mode)
        written = self.make_repository(fault).commit(self.make_transaction("claimed"))
        assert written.status == "error"
        assert written.snapshot is None and written.claim_receipts == ()
        assert len(fault.commits) == 1
        assert (
            written.failure is not None
            and "private text" not in written.failure.diagnostic
        )
        recovered = self.make_repository(
            p.SQLiteAtomicRevisionStore(
                path, busy_timeout_ms=1000, max_payload_bytes=1048576
            )
        ).load_claim(
            self.claim_request(), w.AuthorityReservationOutcomeIdentity("claimed")
        )
        assert recovered.status == expected
        assert recovered.receipt == (
            self.expected_receipt() if expected == "loaded" else None
        )

    @pytest.mark.parametrize(
        "mode,status",
        [
            pytest.param("request", "error", id="substituted_request"),
            pytest.param("stream", "error", id="substituted_stream"),
            pytest.param("selector", "error", id="substituted_selector"),
            pytest.param("unconfirmed", "error", id="unconfirmed_found"),
            pytest.param("revision", "error", id="substituted_revision"),
            pytest.param("predecessor", "corrupt", id="confirmed_wrong_predecessor"),
            pytest.param("digest", "corrupt", id="confirmed_wrong_content"),
            pytest.param("read_exception", "error", id="read_exception"),
            pytest.param("incompatible", "incompatible", id="store_incompatible"),
            pytest.param("corrupt", "corrupt", id="store_corrupt"),
            pytest.param("indeterminate", "indeterminate", id="store_indeterminate"),
            pytest.param("error", "error", id="store_error"),
        ],
    )
    def test_method__load_claim__maps_observations_without_receipt(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        mode: str,
        status: str,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-004

        Requirement: Substitution, unconfirmed reads and every store failure yield no
        receipt.

        Method: Inject one finite shared observation after seeding a real claim.

        Oracle: Exact request/address/confirmation contract and closed status mapping.

        Acceptance: One read preserves available evidence with expected status, no
        receipt.

        Interpretation: FOUND alone is insufficient for historical commitment evidence.

        Limitations: Constructor-impossible false confirmation is tested by shared
        records.
        """
        store = p.SQLiteAtomicRevisionStore(
            tmp_path / "workflow.sqlite3",
            busy_timeout_ms=1000,
            max_payload_bytes=1048576,
        )
        assert self.seed(store, genesis_transaction).status == "committed"
        fault = self.Store(store, mode)
        request = self.claim_request()
        result = self.make_repository(fault).load_claim(
            request, w.AuthorityReservationOutcomeIdentity("claimed")
        )
        assert result.status == status, result.failure
        assert result.receipt is None and result.snapshot is None
        assert fault.reads == [request] and fault.commits == []
        if mode != "read_exception":
            assert result.store_result is not None
            if mode in ("incompatible", "corrupt", "indeterminate", "error"):
                assert result.store_result.result_id == "fault-read"
                assert result.store_result.diagnostics == ("retained diagnostic",)

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("latest", id="latest_selector"),
            pytest.param("incomplete", id="no_expectation_group"),
        ],
    )
    def test_method__load_claim__rejects_unconfirmed_request_before_read(
        self,
        tmp_path: Path,
        variant: str,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-005

        Requirement: Claim loads require explicit revision and complete expectations.

        Method: Supply latest or explicit request without expectations.

        Oracle: Pre-read historical reconciliation contract.

        Acceptance: Error with zero store reads or commits and no receipt.

        Interpretation: Ordinary loads cannot be silently promoted to confirmed claims.

        Limitations: No automatic discovery or second read is performed.
        """
        request = p.RevisionReadRequest(
            request_id="incomplete",
            stream_id="run",
            selector=p.RevisionSelector.LATEST
            if variant == "latest"
            else p.RevisionSelector.EXPLICIT_REVISION,
            revision_id=None if variant == "latest" else "claimed",
        )
        store = self.Store(
            p.SQLiteAtomicRevisionStore(
                tmp_path / "workflow.sqlite3",
                busy_timeout_ms=1000,
                max_payload_bytes=1048576,
            )
        )
        result = self.make_repository(store).load_claim(
            request, w.AuthorityReservationOutcomeIdentity("claimed")
        )
        assert result.status == "error" and result.receipt is None
        assert store.reads == [] and store.commits == []

    @pytest.mark.parametrize(
        "variant,status",
        [
            pytest.param("key", "mismatch", id="wrong_stored_key"),
            pytest.param("content", "mismatch", id="wrong_content_expectation"),
            pytest.param("predecessor", "mismatch", id="wrong_predecessor_expectation"),
            pytest.param("schema", "mismatch", id="wrong_schema_expectation"),
            pytest.param("absent", "absent", id="absent_revision"),
            pytest.param("missing_claim", "mismatch", id="absent_claim_selector"),
            pytest.param("reserved", "corrupt", id="reserved_not_claimed"),
        ],
    )
    def test_method__load_claim__rejects_historical_expectation_and_selector_mismatch(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        variant: str,
        status: str,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-006

        Requirement: Every complete expectation and claim selector binds exact history.

        Method: Change one expectation or selected revision/claim in real SQLite reads.

        Oracle: Shared mismatch/absence versus domain missing/malformed claim statuses.

        Acceptance: Exact expected status with no snapshot or receipt.

        Interpretation: Same run identity does not establish the requested claim.

        Limitations: No external authority is evaluated.
        """
        store = p.SQLiteAtomicRevisionStore(
            tmp_path / "workflow.sqlite3",
            busy_timeout_ms=1000,
            max_payload_bytes=1048576,
        )
        assert self.seed(store, genesis_transaction).status == "committed"
        request = self.claim_request()
        claim = "claimed"
        if variant == "key":
            request = replace(request, expected_idempotency_id="other")
        elif variant == "content":
            request = replace(request, expected_content_id="other")
        elif variant == "predecessor":
            request = replace(request, expected_predecessor_revision_id="other")
        elif variant == "schema":
            request = replace(request, expected_schema_id="other")
        elif variant == "absent":
            request = replace(request, revision_id="absent")
        elif variant == "missing_claim":
            claim = "missing"
        else:
            claim = "reserved"
        result = self.make_repository(store).load_claim(
            request, w.AuthorityReservationOutcomeIdentity(claim)
        )
        assert result.status == status, result.failure
        assert result.receipt is None and result.snapshot is None

    @pytest.mark.parametrize(
        "mode,status",
        [
            pytest.param("ack_key", "error", id="substituted_ack_key"),
            pytest.param("ack_revision", "error", id="substituted_ack_revision"),
            pytest.param(
                "commit_indeterminate", "indeterminate", id="indeterminate_commit"
            ),
            pytest.param("commit_error", "error", id="operational_commit_error"),
        ],
    )
    def test_method__commit__preserves_failure_and_substitution_evidence(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        mode: str,
        status: str,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-007

        Requirement: Wrong acknowledgement or shared failure never produces a snapshot.

        Method: Inject exact finite commit response variants at the shared boundary.

        Oracle: Candidate/key correlation and closed shared status mapping.

        Acceptance: One commit, expected status and retained complete shared result.

        Interpretation: A response label is not sufficient commitment evidence.

        Limitations: Shared failure does not establish presence or permission to retry.
        """
        fault = self.Store(
            p.SQLiteAtomicRevisionStore(
                tmp_path / "workflow.sqlite3",
                busy_timeout_ms=1000,
                max_payload_bytes=1048576,
            ),
            mode,
        )
        result = self.make_repository(fault).commit(genesis_transaction)
        assert result.status == status
        assert len(fault.commits) == 1
        assert result.store_result is not None
        assert result.snapshot is None and result.claim_receipts == ()

    def test_method__load_claim__payload_key_must_match_confirmed_store_key(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-008

        Requirement: Confirmed stored key cannot disagree with the persisted binding.

        Method: Store identical claim bytes under another generic key in another DB.

        Oracle: Ordinary load observes binding; complete confirmation rejects
        disagreement.

        Acceptance: Ordinary read is loaded; claimed-key mismatches and other-key is
        corrupt.

        Interpretation: Generic opaque storage does not validate domain commit binding.

        Limitations: This is a deliberately domain-invalid generic Commit, not
        authentication.
        """
        first = p.SQLiteAtomicRevisionStore(
            tmp_path / "first.sqlite3", busy_timeout_ms=1000, max_payload_bytes=1048576
        )
        original = self.seed(first, genesis_transaction)
        assert original.snapshot is not None
        second = p.SQLiteAtomicRevisionStore(
            tmp_path / "second.sqlite3", busy_timeout_ms=1000, max_payload_bytes=1048576
        )
        repo = self.make_repository(second)
        assert repo.commit(genesis_transaction).status == "committed"
        assert repo.commit(self.make_transaction("prepared")).status == "committed"
        assert (
            second.commit(
                p.Commit("prepared", original.snapshot.revision, "other-key")
            ).status
            is p.CommitStatus.COMMITTED
        )
        ordinary = repo.load(
            p.RevisionReadRequest("ordinary", "run", p.RevisionSelector.LATEST)
        )
        assert ordinary.status == "loaded"
        expected = repo.load_claim(
            self.claim_request(), w.AuthorityReservationOutcomeIdentity("claimed")
        )
        assert expected.status == "mismatch"
        confirmed = repo.load_claim(
            replace(self.claim_request(), expected_idempotency_id="other-key"),
            w.AuthorityReservationOutcomeIdentity("claimed"),
        )
        assert confirmed.status == "corrupt" and confirmed.receipt is None

    @pytest.mark.parametrize(
        "variant,status",
        [
            pytest.param("content", "invalid", id="detached_candidate_content"),
            pytest.param("writer", "incompatible", id="unknown_historical_writer"),
            pytest.param("schema", "incompatible", id="unknown_domain_schema"),
            pytest.param("closure", "invalid", id="dangling_history"),
        ],
    )
    def test_method__commit__invalid_candidate_never_reaches_store(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        variant: str,
        status: str,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-009

        Requirement: Candidate metadata/version/closure failure causes zero commits.

        Method: Submit one named invalid genesis variant through a recording store.

        Oracle: Reviewed validation and complete byte-binding rules.

        Acceptance: Exact rejection status, retained transaction, no shared commit.

        Interpretation: A caller-supplied content identity is not validation.

        Limitations: No scientific validity is claimed for accepted structure.
        """
        tx = genesis_transaction
        if variant == "content":
            tx = replace(tx, content_identity="wrong")
        elif variant == "writer":
            tx = replace(
                tx,
                binding=replace(
                    tx.binding, persistence_implementation_identity="future-writer"
                ),
            )
        elif variant == "schema":
            tx = replace(tx, schema_identity="future")
        else:
            prepared = self.make_transaction("prepared")
            broken = replace(
                prepared.candidate,
                revision_identity=tx.candidate.revision_identity,
                predecessor_revision_identity=None,
                task_memberships=(),
            )
            repo = self.make_repository(
                p.SQLiteAtomicRevisionStore(
                    tmp_path / "unused.sqlite3",
                    busy_timeout_ms=1000,
                    max_payload_bytes=1048576,
                )
            )
            encoded = repo.serializer.serialize(broken, tx.binding)
            assert encoded.encoded is not None
            tx = replace(
                tx, candidate=broken, content_identity=encoded.encoded.content_identity
            )
        fault = self.Store(
            p.SQLiteAtomicRevisionStore(
                tmp_path / "workflow.sqlite3",
                busy_timeout_ms=1000,
                max_payload_bytes=1048576,
            )
        )
        result = self.make_repository(fault).commit(tx)
        assert result.status == status, result.failure
        assert result.transaction is tx and result.store_result is None
        assert fault.commits == []

    @pytest.mark.parametrize(
        "variant,status",
        [
            pytest.param("space", "corrupt", id="noncanonical_domain_bytes"),
            pytest.param("run", "corrupt", id="decoded_run_address_differs"),
            pytest.param(
                "authorization", "corrupt", id="claim_authorization_not_authorized"
            ),
            pytest.param("phase", "corrupt", id="preparation_phase_in_claim"),
            pytest.param("binding", "corrupt", id="missing_commit_binding"),
        ],
    )
    def test_method__load_claim__checks_domain_bytes_after_store_confirmation(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        variant: str,
        status: str,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-011

        Requirement: Generic integrity and key confirmation do not establish domain
        closure.

        Method: Commit named altered domain bytes with correct generic content/key
        metadata.

        Oracle: Canonical grammar, supported writer and exact run/claim authorization
        links.

        Acceptance: Confirmed FOUND is retained but no receipt or snapshot is returned.

        Interpretation: Domain validation remains necessary after generic store
        integrity.

        Limitations: Retained authorization is not reevaluated or authenticated.
        """
        path = Path(__file__).with_name("resources") / "claim-receipt-v1.json"
        payload = path.read_bytes()
        if variant == "space":
            payload += b"\n"
        elif variant == "run":
            payload = payload.replace(b'"value":"run"', b'"value":"other-run"')
        elif variant == "authorization":
            payload = payload.replace(b'"value":"authorized"', b'"value":"rejected"', 1)
        elif variant == "phase":
            payload = payload.replace(b'"value":"claim"', b'"value":"preparation"')
        else:
            payload = payload.replace(b'"commit_binding":', b'"missing_binding":', 1)
        assert payload != path.read_bytes()
        result = self.load_altered_claim(tmp_path, genesis_transaction, payload)
        assert result.status == status, result.failure
        assert result.receipt is None and result.snapshot is None
        assert (
            result.store_result is not None
            and result.store_result.expectations_matched is True
        )

    def test_method__load_claim__rejects_unsupported_historical_writer(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-017

        Requirement: Unknown persisted writer versions remain incompatible.

        Method: Change only the historical writer label in otherwise complete wire.

        Oracle: Explicit supported writer version and generic expectation confirmation.

        Acceptance: Incompatible retains confirmed FOUND but no snapshot or receipt.

        Interpretation: The reader must not replace a historical writer with itself.

        Limitations: A recognized writer label is consistency, not authentication.
        """
        payload = (
            (Path(__file__).with_name("resources") / "claim-receipt-v1.json")
            .read_bytes()
            .replace(b"WorkflowRunAtomicRepository:1", b"WorkflowRunAtomicRepository:9")
        )
        result = self.load_altered_claim(tmp_path, genesis_transaction, payload)
        assert result.status == "incompatible", result.failure
        assert result.receipt is None and result.snapshot is None
        assert (
            result.store_result is not None
            and result.store_result.expectations_matched is True
        )

    def load_altered_claim(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        payload: bytes,
    ) -> w.WorkflowRunClaimLoadResult:
        """Stage exact bytes; domain statuses remain independent test oracles."""
        import hashlib

        store = p.SQLiteAtomicRevisionStore(
            tmp_path / "workflow.sqlite3",
            busy_timeout_ms=1000,
            max_payload_bytes=1048576,
        )
        repo = self.make_repository(store)
        assert repo.commit(genesis_transaction).status == "committed"
        assert repo.commit(self.make_transaction("prepared")).status == "committed"
        content = (
            "ksdft2effmass.workflow-run:1:sha256:" + hashlib.sha256(payload).hexdigest()
        )
        revision = p.Revision(
            "run",
            "claimed",
            "prepared",
            "ksdft2effmass.workflow-run:1",
            content,
            payload,
        )
        assert (
            store.commit(p.Commit("prepared", revision, "claimed-key")).status
            is p.CommitStatus.COMMITTED
        )
        return repo.load_claim(
            replace(self.claim_request(), expected_content_id=content),
            w.AuthorityReservationOutcomeIdentity("claimed"),
        )

    @pytest.mark.parametrize(
        "mode,status",
        [
            pytest.param("ordinary", "invalid", id="absent_predecessor"),
            pytest.param("incompatible", "incompatible", id="unsupported_predecessor"),
            pytest.param("corrupt", "invalid", id="corrupt_predecessor"),
            pytest.param("indeterminate", "indeterminate", id="uncertain_predecessor"),
            pytest.param("error", "error", id="failed_predecessor_read"),
        ],
    )
    def test_method__commit__predecessor_failure_never_submits(
        self,
        tmp_path: Path,
        mode: str,
        status: str,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-012

        Requirement: Exact predecessor failures preserve read evidence and prohibit
        commits.

        Method: Submit the literal claim through an absent or faulting predecessor
        store.

        Oracle: Explicit prepared revision request and closed read-to-write mapping.

        Acceptance: Exact status, one predecessor read, zero commits and no receipt.

        Interpretation: Read uncertainty cannot be collapsed into a CAS conflict.

        Limitations: No automatic retry or predecessor discovery occurs.
        """
        fault = self.Store(
            p.SQLiteAtomicRevisionStore(
                tmp_path / "workflow.sqlite3",
                busy_timeout_ms=1000,
                max_payload_bytes=1048576,
            ),
            mode,
        )
        result = self.make_repository(fault).commit(self.make_transaction("claimed"))
        assert result.status == status, result.failure
        assert result.predecessor_load is not None and result.store_result is None
        assert result.snapshot is None and result.claim_receipts == ()
        assert len(fault.reads) == 1 and fault.reads[0].revision_id == "prepared"
        assert fault.reads[0].selector is p.RevisionSelector.EXPLICIT_REVISION
        assert fault.commits == []

    def test_method__load__does_not_compute_replay_or_authorization(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-013

        Requirement: Persistence does not calculate replay or authorization results.

        Method: Prohibit those operations while storing and loading the literal
        histories.

        Oracle: Repository contract separates structural closure from executable
        services.

        Acceptance: Claim commit and confirmed read succeed without the prohibited
        calls.

        Interpretation: Historical commitment alone supplies no effect permission.

        Limitations: These synthetic retained authorizer labels are not authentication.
        """
        monkeypatch.setattr(w.WorkflowRunReplayer, "execute", self.prohibited)
        monkeypatch.setattr(w.SimulationExecutionAuthorizer, "execute", self.prohibited)
        store = p.SQLiteAtomicRevisionStore(
            tmp_path / "workflow.sqlite3",
            busy_timeout_ms=1000,
            max_payload_bytes=1048576,
        )
        assert self.seed(store, genesis_transaction).status == "committed"
        result = self.make_repository(store).load_claim(
            self.claim_request(), w.AuthorityReservationOutcomeIdentity("claimed")
        )
        assert result.receipt == self.expected_receipt()

    @staticmethod
    def prohibited(
        *args: w.WorkflowRun
        | w.WorkflowRuntimeBundle
        | w.SimulationExecutionAuthorizationRequest,
    ) -> None:
        raise AssertionError("persistence must not compute replay or authorization")

    def test_method__load__preserves_codec_operation_failure(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-014

        Requirement: A codec operation error remains error with its complete diagnosis.

        Method: Replace decoding with a typed closed error after committing real
        genesis.

        Oracle: Injected error object and preserved successful shared read evidence.

        Acceptance: Error propagates without snapshot and with the codec failure
        identity.

        Interpretation: Successful shared integrity is not successful reconstruction.

        Limitations: No store error or scientific algorithm is simulated.
        """
        store = p.SQLiteAtomicRevisionStore(
            tmp_path / "workflow.sqlite3",
            busy_timeout_ms=1000,
            max_payload_bytes=1048576,
        )
        repo = self.make_repository(store)
        assert repo.commit(genesis_transaction).status == "committed"
        monkeypatch.setattr(w.WorkflowRunSerializer, "deserialize", self.fail_decode)
        result = repo.load(
            p.RevisionReadRequest("read", "run", p.RevisionSelector.LATEST)
        )
        assert result.status == "error" and result.snapshot is None
        assert result.failure == self.decode_failure()
        assert (
            result.store_result is not None
            and result.store_result.status is p.RevisionReadStatus.FOUND
        )

    @staticmethod
    def decode_failure() -> w.WorkflowPersistenceFailure:
        return w.WorkflowPersistenceFailure(
            implementation_identity="fixture-codec:1",
            phase="decode",
            code=w.WorkflowPersistenceFailureCode.CODEC_ERROR,
            input_identities=("exact-payload-digest",),
            expected="complete decode",
            observed="operational failure",
            diagnostic="sanitized codec failure",
            claim_boundary="no reconstructed aggregate",
        )

    def fail_decode(self, payload: bytes) -> w.WorkflowRunDecodeResult:
        return w.WorkflowRunDecodeResult(status="error", failure=self.decode_failure())

    def test_method__commit__changed_transaction_cannot_alias_stored_key(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-015

        Requirement: Transaction labels are content-bound, not transient operation
        aliases.

        Method: Resubmit the same claim and key with changed persisted transaction
        label.

        Oracle: Original stored exact bytes and generic complete idempotency contract.

        Acceptance: Changed content conflicts and original historical receipt is
        unchanged.

        Interpretation: Identical run state is insufficient for identical committed
        bytes.

        Limitations: Stored labels are not authentication of a historical process.
        """
        store = p.SQLiteAtomicRevisionStore(
            tmp_path / "workflow.sqlite3",
            busy_timeout_ms=1000,
            max_payload_bytes=1048576,
        )
        assert self.seed(store, genesis_transaction).status == "committed"
        repo = self.make_repository(store)
        tx = self.make_transaction("claimed")
        binding = replace(tx.binding, transaction_identity="other-transaction")
        wire = repo.serializer.serialize(tx.candidate, binding)
        assert (
            wire.encoded is not None
            and wire.encoded.content_identity != tx.content_identity
        )
        changed = replace(
            tx, binding=binding, content_identity=wire.encoded.content_identity
        )
        result = repo.commit(changed)
        assert result.status == "conflict" and result.claim_receipts == ()
        assert (
            repo.load_claim(
                self.claim_request(), w.AuthorityReservationOutcomeIdentity("claimed")
            ).receipt
            == self.expected_receipt()
        )

    @pytest.mark.parametrize(
        "variant",
        [
            pytest.param("load", id="wrong_read_request_type"),
            pytest.param("commit", id="wrong_transaction_type"),
            pytest.param("claim_request", id="wrong_claim_request_type"),
            pytest.param("claim_selector", id="wrong_claim_selector_type"),
        ],
    )
    def test_method__arguments__rejects_wrong_semantic_types(
        self,
        tmp_path: Path,
        variant: str,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-016

        Requirement: Direct argument type errors are raised before any store operation.

        Method: Supply one exact string in place of a required request or record.

        Oracle: Public exact semantic type contract and empty store-call logs.

        Acceptance: TypeError is raised and no read or commit occurs.

        Interpretation: Operation failures do not hide caller type-contract violations.

        Limitations: Invalid intrinsic values remain with their record constructors.
        """
        fault = self.Store(
            p.SQLiteAtomicRevisionStore(
                tmp_path / "workflow.sqlite3",
                busy_timeout_ms=1000,
                max_payload_bytes=1048576,
            )
        )
        repo = self.make_repository(fault)
        with pytest.raises(TypeError):
            if variant == "load":
                repo.load("read")  # type: ignore[arg-type]
            elif variant == "commit":
                repo.commit("transaction")  # type: ignore[arg-type]
            elif variant == "claim_request":
                repo.load_claim(
                    "read",  # type: ignore[arg-type]
                    w.AuthorityReservationOutcomeIdentity("claimed"),
                )
            else:
                repo.load_claim(self.claim_request(), "claimed")  # type: ignore[arg-type]
        assert fault.reads == [] and fault.commits == []

    def test_method__commit__rejects_detached_validation_result(
        self,
        tmp_path: Path,
        genesis_transaction: w.WorkflowRunTransaction,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-018

        Requirement: Successful validation must retain the exact submitted transaction.

        Method: Inject valid-shaped evidence bound to a copied transaction object.

        Oracle: Reviewed same-transaction validation/serialization submission binding.

        Acceptance: Invalid retains the requested transaction and submits zero commits.

        Interpretation: A detached successful result is not permission to store bytes.

        Limitations: The actual validator is independently verified by its owner.
        """
        fault = self.Store(
            p.SQLiteAtomicRevisionStore(
                tmp_path / "workflow.sqlite3",
                busy_timeout_ms=1000,
                max_payload_bytes=1048576,
            )
        )
        repo = self.make_repository(fault)
        monkeypatch.setattr(
            w.WorkflowRunTransactionValidator, "execute", self.detached_validation
        )
        result = repo.commit(genesis_transaction)
        assert result.status == "invalid"
        assert result.transaction is genesis_transaction
        assert result.store_result is None and fault.commits == []

    def detached_validation(
        self,
        transaction: w.WorkflowRunTransaction,
        predecessor: w.WorkflowRunSnapshot | None = None,
    ) -> w.WorkflowRunValidationResult:
        payload = (
            Path(__file__).with_name("resources") / "genesis-record-envelope.json"
        ).read_bytes()
        return w.WorkflowRunValidationResult(
            status="valid",
            transaction=replace(transaction),
            predecessor=predecessor,
            encoded=w.WorkflowEncodedRun(
                schema_identity=transaction.schema_identity,
                content_identity=transaction.content_identity,
                payload=payload,
            ),
        )

    def test_constructor__dependencies__requires_same_serializer_and_is_immutable(
        self,
        tmp_path: Path,
    ) -> None:
        """Evidence ID: SV-WFR-REPOSITORY-010

        Requirement: Domain validator and serializer cannot be detached or rebound.

        Method: Mix independently configured dependencies and attempt assignment.

        Oracle: Exact serializer-instance binding and frozen repository contract.

        Acceptance: ValueError on detachment and FrozenInstanceError on mutation.

        Interpretation: Dependency binding is explicit, not ambient codec discovery.

        Limitations: Structural protocol membership alone is not store correctness.
        """
        store = p.SQLiteAtomicRevisionStore(
            tmp_path / "workflow.sqlite3",
            busy_timeout_ms=1000,
            max_payload_bytes=1048576,
        )
        repo, other = self.make_repository(store), self.make_repository(store)
        assert isinstance(repo, w.WorkflowRunRepository)
        with pytest.raises(ValueError):
            SUT(store=store, serializer=repo.serializer, validator=other.validator)
        with pytest.raises(FrozenInstanceError):
            repo.store = store  # type: ignore[misc]
