r"""Software verification of ``SQLiteAtomicRevisionStore``.

Evidence profile: claim_bearing

Bounded artifact scope: SQLiteAtomicRevisionStore local revision storage.

Facet and represented meaning

Exact opaque revisions, replay, consistency, private integrity and closed failures
are checked against the accepted persistence architecture and independent SQL data.

Intrinsic and cross-object scope

The store owns transaction policy; predecessor DataObject constructor evidence is
not duplicated. Fixture processes execute only installed Python against scratch.

VVUQ and scientific exclusions

Software verification only: no scientific calculation, domain validity, hardware
power-loss, network-filesystem, performance or human-acceptance claim.
"""

from __future__ import annotations

import ast
import selectors
import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
from functools import partial
from pathlib import Path
from threading import Barrier
from typing import cast
from unittest.mock import patch

import pytest

import ksdft2effmass.persistence as persistence
from ksdft2effmass.persistence import (
    AtomicRevisionStore,
    Commit,
    CommitStatus,
    Revision,
    RevisionReadRequest,
    RevisionReadResult,
    RevisionReadStatus,
    RevisionSelector,
    SQLiteAtomicRevisionStore,
)

pytestmark = pytest.mark.software_verification
SUT = SQLiteAtomicRevisionStore


class TestSQLiteAtomicRevisionStore:
    """Own local synthetic store evidence without retained instance state."""

    @staticmethod
    def make_store(
        path: Path, *, timeout: int = 1000, cap: int = 1024
    ) -> SQLiteAtomicRevisionStore:
        return SQLiteAtomicRevisionStore(
            path, busy_timeout_ms=timeout, max_payload_bytes=cap
        )

    @staticmethod
    def make_commit(
        *,
        revision: str = "r1",
        predecessor: str | None = None,
        key: str = "k1",
        stream: str = "s",
        payload: bytes = b"\x00\xff",
    ) -> Commit:
        return Commit(
            predecessor,
            Revision(stream, revision, predecessor, "schema", "content", payload),
            key,
        )

    @staticmethod
    def make_request(
        revision: str | None = None, *, stream: str = "s"
    ) -> RevisionReadRequest:
        return RevisionReadRequest(
            "request",
            stream,
            RevisionSelector.LATEST
            if revision is None
            else RevisionSelector.EXPLICIT_REVISION,
            revision,
        )

    @staticmethod
    def execute_sql(path: Path, sql: str) -> None:
        with sqlite3.connect(path) as connection:
            connection.executescript(sql)

    @staticmethod
    def observe_count(path: Path) -> int:
        with sqlite3.connect(path) as connection:
            row = cast(
                tuple[int],
                connection.execute("SELECT count(*) FROM revisions").fetchone(),
            )
            return row[0]

    def make_fixture(self, path: Path) -> SQLiteAtomicRevisionStore:
        self.execute_sql(
            path, (Path(__file__).parent / "resources/sqlite-v1.sql").read_text()
        )
        return self.make_store(path)

    @staticmethod
    def assert_corrupt_identities(
        result: RevisionReadResult, observed: tuple[tuple[str, str | None], ...]
    ) -> None:
        """Check one closed corrupt observation against explicit SQL-derived labels."""
        assert result.status is RevisionReadStatus.CORRUPT
        assert result.observed_identities == observed
        assert result.integrity_findings == ("Generic revision integrity failed.",)
        assert result.revision is None
        assert result.mismatched_fields == ()
        assert result.expected_identities == ()
        assert result.expectations_matched is None
        assert result.absence_observation is None

    @staticmethod
    def refuse_head_insert(
        connection: sqlite3.Connection,
        observed_counts: list[int],
        action: int,
        table: str | None,
        column: str | None,
        database: str | None,
        trigger: str | None,
    ) -> int:
        """Deny the head write only after observing the real uncommitted insertion."""
        if action == sqlite3.SQLITE_INSERT and table == "heads":
            row = cast(
                tuple[int],
                connection.execute("SELECT count(*) FROM revisions").fetchone(),
            )
            observed_counts.append(row[0])
            return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK

    @staticmethod
    def lose_acknowledgement(connection: sqlite3.Connection) -> None:
        connection.execute("COMMIT")
        raise sqlite3.OperationalError("sensitive path and payload must not escape")

    @staticmethod
    def interrupt_observation(connection: sqlite3.Connection, stream: str) -> None:
        raise sqlite3.OperationalError("sensitive observation")

    @staticmethod
    def close_with_failure(connection: sqlite3.Connection | None) -> str:
        if connection is not None:
            connection.close()
        return "connection_close_failed; established observation retained"

    def test_method__read__reopens_exact_history_and_absence(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-001

        Requirement: Complete initial and successor revisions survive reopen with
        explicit historical versus latest addressing and established absence.

        Method: Commit hand-specified revisions and read through a fresh instance.

        Oracle: Exact supplied public revision fields and explicit address contract.

        Acceptance: Every field and byte equals its input; latest is the successor;
        explicit and latest missing observations are absent without a revision.

        Interpretation: Failure detects incomplete storage or implicit selection.

        Limitations: Local synthetic process, not hardware durability evidence.
        """
        path = tmp_path / "store.db"
        first = self.make_commit()
        second = self.make_commit(
            revision="r2", predecessor="r1", key="k2", payload=b"next"
        )
        store = self.make_store(path)
        assert store.commit(first).revision == first.candidate
        assert store.commit(second).revision == second.candidate
        reopened = self.make_store(path)
        historical = reopened.read(self.make_request("r1"))
        assert historical.status is RevisionReadStatus.FOUND
        assert historical.revision == first.candidate
        assert historical.expectations_matched is None
        assert historical.requested_revision_id is None
        assert reopened.read(self.make_request()).revision == second.candidate
        absent = reopened.read(self.make_request("missing"))
        assert absent.status is RevisionReadStatus.ABSENT
        assert absent.requested_revision_id == "missing"
        assert absent.revision is None
        assert absent.absence_observation
        assert (
            reopened.read(self.make_request(stream="missing")).status
            is RevisionReadStatus.ABSENT
        )

    def test_method__commit__replays_original_after_head_advances(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-002

        Requirement: Exact idempotency replay precedes CAS and returns the original.

        Method: Advance a stream then resubmit its first commit via a new instance.

        Oracle: Original candidate and independently queried SQL revision count.

        Acceptance: Replay is committed with original revision, two rows remain,
        and latest still identifies the successor.

        Interpretation: Failure detects stale-CAS replay or duplicated history.

        Limitations: Cross-process persistence is separately exercised by crash tests.
        """
        path = tmp_path / "store.db"
        store = self.make_store(path)
        first = self.make_commit()
        assert store.commit(first).status is CommitStatus.COMMITTED
        assert (
            store.commit(
                self.make_commit(revision="r2", predecessor="r1", key="k2")
            ).status
            is CommitStatus.COMMITTED
        )
        replay = self.make_store(path).commit(first)
        assert replay.status is CommitStatus.COMMITTED
        assert replay.revision == first.candidate
        assert self.observe_count(path) == 2
        latest = store.read(self.make_request()).revision
        assert latest is not None and latest.revision_id == "r2"

    @pytest.mark.parametrize(
        "changed",
        [
            pytest.param(
                Revision("other", "r1", None, "schema", "content", b"\x00\xff"),
                id="stream",
            ),
            pytest.param(
                Revision("s", "other", None, "schema", "content", b"\x00\xff"),
                id="revision",
            ),
            pytest.param(
                Revision("s", "r1", "other", "schema", "content", b"\x00\xff"),
                id="predecessor_expectation",
            ),
            pytest.param(
                Revision("s", "r1", None, "other", "content", b"\x00\xff"), id="schema"
            ),
            pytest.param(
                Revision("s", "r1", None, "schema", "other", b"\x00\xff"), id="content"
            ),
            pytest.param(
                Revision("s", "r1", None, "schema", "content", b"changed"),
                id="bytes_same_content_label",
            ),
        ],
    )
    def test_method__commit__rejects_changed_idempotency_binding(
        self, tmp_path: Path, changed: Revision
    ) -> None:
        """Evidence ID: SV-SQLITE-003

        Requirement: Reusing one key with any changed bound field conflicts.

        Method: Commit an original then vary one field under the same key.

        Oracle: Complete Commit equality, independent of caller content label.

        Acceptance: Idempotency collision, no revision in result, one stored row.

        Interpretation: Failure detects digest-only or partially bound replay.

        Limitations: Database-wide keys do not coordinate separate databases.
        """
        path = tmp_path / "store.db"
        store = self.make_store(path)
        assert store.commit(self.make_commit()).status is CommitStatus.COMMITTED
        result = store.commit(Commit(changed.predecessor_revision_id, changed, "k1"))
        assert result.status is CommitStatus.CONFLICT
        assert result.conflict_code == "idempotency_collision"
        assert result.revision is None
        assert self.observe_count(path) == 1

    def test_method__commit__distinguishes_revision_and_cas_collisions(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-004

        Requirement: Address collision and stale expected head are distinct conflicts.

        Method: Use a fresh key for an existing address then a new stale candidate.

        Oracle: Existing r1 head and accepted conflict ordering.

        Acceptance: Revision collision then compare_and_swap, expected None and
        observed r1, with no additional row.

        Interpretation: Failure detects conflict collapse or mutation on refusal.

        Limitations: Synthetic single-stream cases only.
        """
        path = tmp_path / "store.db"
        store = self.make_store(path)
        assert store.commit(self.make_commit()).status is CommitStatus.COMMITTED
        assert (
            store.commit(self.make_commit(key="other")).conflict_code
            == "revision_collision"
        )
        result = store.commit(self.make_commit(revision="r2", key="k2"))
        assert result.status is CommitStatus.CONFLICT
        assert result.conflict_code == "compare_and_swap"
        assert result.expected_revision_id is None
        assert result.observed_revision_id == "r1"
        assert self.observe_count(path) == 1

    def test_method__commit__separates_streams_and_databases(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-005

        Requirement: Revision labels are stream-local; keys are database-local.

        Method: Use the same revision label in two streams and the same key in a
        different physical database.

        Oracle: Explicit independent stream/database addresses and input bytes.

        Acceptance: All commits succeed and each addressed payload is unchanged.

        Interpretation: Failure detects global revision identity or hidden store state.

        Limitations: No cross-stream atomicity or co-location authorization follows.
        """
        first = self.make_store(tmp_path / "development.db")
        second = self.make_store(tmp_path / "scientific-synthetic.db")
        assert first.commit(self.make_commit()).status is CommitStatus.COMMITTED
        other = self.make_commit(stream="other", key="other-key", payload=b"other")
        assert first.commit(other).revision == other.candidate
        separate = self.make_commit(payload=b"separate")
        assert second.commit(separate).revision == separate.candidate
        assert first.read(self.make_request()).revision == self.make_commit().candidate
        assert first.read(self.make_request(stream="other")).revision == other.candidate

    @pytest.mark.parametrize(
        "initialized",
        [
            pytest.param(False, id="concurrent_bootstrap"),
            pytest.param(True, id="existing_predecessor"),
        ],
    )
    def test_method__commit__serializes_competing_writers(
        self, tmp_path: Path, initialized: bool
    ) -> None:
        """Evidence ID: SV-SQLITE-006

        Requirement: Competing connections from one expected slot commit at most one.

        Method: Coordinate two worker threads, each owning a separate store connection.

        Oracle: Exactly one winner and one CAS conflict, independently counted rows.

        Acceptance: One committed, one conflict; head equals winning candidate and
        row count is one new revision plus the optional original.

        Interpretation: Failure detects initialization races or non-atomic CAS.

        Limitations: Bounded local contention, not throughput or fairness evidence.
        """
        path = tmp_path / "store.db"
        predecessor = "r1" if initialized else None
        if initialized:
            assert (
                self.make_store(path).commit(self.make_commit()).status
                is CommitStatus.COMMITTED
            )
        barrier = Barrier(2)
        left = self.make_commit(revision="left", predecessor=predecessor, key="left")
        right = self.make_commit(revision="right", predecessor=predecessor, key="right")
        with ThreadPoolExecutor(max_workers=2) as pool:
            a = pool.submit(self.commit_at_barrier, path, barrier, left)
            b = pool.submit(self.commit_at_barrier, path, barrier, right)
            results = (a.result(timeout=10), b.result(timeout=10))
        assert sorted(result.status for result in results) == [
            CommitStatus.COMMITTED,
            CommitStatus.CONFLICT,
        ]
        winner = next(
            result for result in results if result.status is CommitStatus.COMMITTED
        )
        loser = next(
            result for result in results if result.status is CommitStatus.CONFLICT
        )
        assert loser.conflict_code == "compare_and_swap"
        assert (
            self.make_store(path).read(self.make_request()).revision == winner.revision
        )
        assert self.observe_count(path) == (2 if initialized else 1)

    @staticmethod
    def commit_at_barrier(
        path: Path, barrier: Barrier, commit: Commit
    ) -> persistence.CommitResult:
        barrier.wait(timeout=5)
        return SQLiteAtomicRevisionStore(
            path, busy_timeout_ms=5000, max_payload_bytes=1024
        ).commit(commit)

    def test_method__commit__represents_lock_contention_without_retry(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-007

        Requirement: Lock contention is operational error, never CAS conflict.

        Method: Hold a raw IMMEDIATE transaction and use zero timeout, then release.

        Oracle: Native lock ownership and exact candidate retry after release.

        Acceptance: Error with busy code and no presence claim; retry commits once.

        Interpretation: Failure detects hidden retries or guessed conflicts.

        Limitations: No timing lower bound or starvation guarantee is asserted.
        """
        path = tmp_path / "store.db"
        store = self.make_store(path, timeout=0)
        assert store.read(self.make_request()).status is RevisionReadStatus.ABSENT
        with sqlite3.connect(path) as lock:
            lock.execute("BEGIN IMMEDIATE")
            result = store.commit(self.make_commit())
            assert result.status is CommitStatus.ERROR
            assert result.failure is not None and result.failure.code == "busy"
            assert result.revision is None and result.observed_revision_id is None
        assert store.commit(self.make_commit()).status is CommitStatus.COMMITTED
        assert self.observe_count(path) == 1

    def test_method__commit__rolls_back_precommit_sql_failure(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-008

        Requirement: A head-write failure must roll back the already inserted revision.

        Method: Deny the native head INSERT through sqlite3's authorizer after
        recording the real transaction's revision count, then submit a successor.

        Oracle: Fresh public reads and independent SQL row count after failure.

        Acceptance: Two rows are visible before head-write denial; error then
        leaves one original row, original head, and candidate absent on reopen.

        Interpretation: Failure detects split insertion/head transactions.

        Limitations: Native authorizer denial is software injection, not hardware loss.
        """
        path = tmp_path / "store.db"
        store = self.make_store(path)
        assert store.commit(self.make_commit()).status is CommitStatus.COMMITTED
        connection = sqlite3.connect(path, isolation_level=None)
        observed_counts: list[int] = []
        connection.set_authorizer(
            partial(self.refuse_head_insert, connection, observed_counts)
        )
        with patch.object(
            SQLiteAtomicRevisionStore, "_connect", return_value=connection
        ):
            result = store.commit(
                self.make_commit(revision="r2", predecessor="r1", key="k2")
            )
        assert observed_counts == [2]
        assert result.status is CommitStatus.ERROR
        assert result.failure is not None and result.failure.code == "sqlite_failure"
        assert self.observe_count(path) == 1
        assert (
            self.make_store(path).read(self.make_request()).revision
            == self.make_commit().candidate
        )
        assert store.read(self.make_request("r2")).status is RevisionReadStatus.ABSENT

    @pytest.mark.parametrize(
        "body",
        [
            pytest.param(
                "UPDATE revisions SET payload=X'01' WHERE revision=X'7232';",
                id="candidate_bytes_changed",
            ),
            pytest.param(
                "UPDATE revisions SET payload=X'01' WHERE revision=X'7231';",
                id="historical_bytes_changed",
            ),
            pytest.param(
                "DELETE FROM heads WHERE stream=X'6f74686572'; "
                "DELETE FROM revisions WHERE stream=X'6f74686572';",
                id="different_stream_deleted",
            ),
            pytest.param(
                "UPDATE revisions SET payload=X'01' WHERE stream=X'6f74686572';",
                id="different_stream_payload_changed",
            ),
            pytest.param(
                "UPDATE store_format SET version=2;",
                id="store_metadata_changed",
            ),
        ],
    )
    def test_method__commit__refuses_trigger_modified_revisions(
        self, tmp_path: Path, body: str
    ) -> None:
        """Evidence ID: SV-SQLITE-028

        Requirement: Unowned triggers must not permit a single-stream append to
        alter candidate bytes, existing history, another stream or store metadata.

        Method: Install an AFTER INSERT trigger with one destructive SQL body, then
        read, replay and submit a successor without removing the trigger.

        Oracle: Byte-identical database after refusal; exact original revisions and
        supported metadata remain readable after explicit test-only trigger removal.

        Acceptance: Read corrupt; replay and successor integrity_failure errors;
        unchanged file, two original rows and absent successor after trigger removal.

        Interpretation: Failure exposes admitted executable schema or destructive
        repair; early refusal is not evidence of rollback after insertion.

        Limitations: Generic integrity detection is not authentication against an
        actor rewriting the entire file after the transaction.
        """
        path = tmp_path / "store.db"
        store = self.make_store(path)
        assert store.commit(self.make_commit()).status is CommitStatus.COMMITTED
        other = self.make_commit(stream="other", key="other-key", payload=b"other")
        assert store.commit(other).status is CommitStatus.COMMITTED
        self.execute_sql(
            path,
            "CREATE TRIGGER alter_revision AFTER INSERT ON revisions BEGIN "
            f"{body} END;",
        )
        before = path.read_bytes()
        assert store.read(self.make_request()).status is RevisionReadStatus.CORRUPT
        replay = store.commit(self.make_commit())
        assert replay.status is CommitStatus.ERROR
        assert replay.failure is not None and replay.failure.code == "integrity_failure"
        result = store.commit(
            self.make_commit(revision="r2", predecessor="r1", key="k2")
        )
        assert result.status is CommitStatus.ERROR
        assert result.failure is not None and result.failure.code == "integrity_failure"
        assert path.read_bytes() == before
        assert self.observe_count(path) == 2
        self.execute_sql(path, "DROP TRIGGER alter_revision;")
        reopened = self.make_store(path)
        assert (
            reopened.read(self.make_request()).revision == self.make_commit().candidate
        )
        assert (
            reopened.read(self.make_request(stream="other")).revision == other.candidate
        )
        assert (
            reopened.read(self.make_request("r2")).status is RevisionReadStatus.ABSENT
        )

    @pytest.mark.parametrize(
        "phase",
        [
            pytest.param("before", id="termination_before_commit"),
            pytest.param("after", id="termination_after_commit"),
        ],
    )
    def test_method__commit__survives_actual_process_termination(
        self, tmp_path: Path, phase: str
    ) -> None:
        """Evidence ID: SV-SQLITE-009

        Requirement: Process loss around COMMIT leaves either complete old or new state.

        Method: Terminate an installed-Python fixture after its explicit
        boundary signal.

        Oracle: Fresh connection state and independently counted revisions.

        Acceptance: Before COMMIT retains only original; after COMMIT has complete
        successor and exact replay adds nothing.

        Interpretation: Failure detects partial revisions or lost committed state.

        Limitations: OS process termination, not power-loss or scientific execution.
        """
        path = tmp_path / "store.db"
        assert (
            self.make_store(path).commit(self.make_commit()).status
            is CommitStatus.COMMITTED
        )
        worker = Path(__file__).parent / "resources/sqlite_fault_worker.py"
        process = subprocess.Popen(
            [sys.executable, str(worker), str(path), phase],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            assert process.stdout is not None
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ)
                assert selector.select(timeout=10), "fixture did not reach boundary"
            assert process.stdout.readline().strip() == phase
        finally:
            process.terminate()
            process.communicate(timeout=10)
        store = self.make_store(path)
        expected = (
            self.make_commit()
            if phase == "before"
            else self.make_commit(
                revision="r2", predecessor="r1", key="k2", payload=b"next"
            )
        )
        assert store.read(self.make_request()).revision == expected.candidate
        assert self.observe_count(path) == (1 if phase == "before" else 2)
        replay = store.commit(expected)
        assert replay.status is CommitStatus.COMMITTED
        assert self.observe_count(path) == (1 if phase == "before" else 2)

    def test_method__commit__reconciles_lost_acknowledgement(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-010

        Requirement: Exception after a real COMMIT remains indeterminate
        until reconciled.

        Method: Inject lost acknowledgement, reopen and bind all expectation slots.

        Oracle: Public exact reconciliation and independent SQL count after replay.

        Acceptance: Indeterminate with sanitized commit_unacknowledged failure;
        fresh found confirms exact candidate and replay leaves one row.

        Interpretation: Failure detects guessed rollback or success from missing ack.

        Limitations: Narrow private seam controls failure only; SQLite commits for real.
        """
        path = tmp_path / "store.db"
        store = self.make_store(path)
        with patch.object(
            SQLiteAtomicRevisionStore,
            "_commit_transaction",
            staticmethod(self.lose_acknowledgement),
        ):
            result = store.commit(self.make_commit())
        assert result.status is CommitStatus.INDETERMINATE
        assert (
            result.failure is not None
            and result.failure.code == "commit_unacknowledged"
        )
        assert result.failure.operation_phase == "commit.acknowledge"
        assert result.revision is None
        assert "sensitive" not in str(result)
        request = RevisionReadRequest(
            "reconcile",
            "s",
            RevisionSelector.EXPLICIT_REVISION,
            "r1",
            None,
            "schema",
            "content",
            "k1",
        )
        found = self.make_store(path).read(request)
        assert found.status is RevisionReadStatus.FOUND
        assert found.expectations_matched is True
        assert found.revision == self.make_commit().candidate
        assert store.commit(self.make_commit()).status is CommitStatus.COMMITTED
        assert self.observe_count(path) == 1

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("content_id", id="content"),
            pytest.param("schema_id", id="schema"),
            pytest.param("predecessor_revision_id", id="predecessor"),
            pytest.param("idempotency_id", id="idempotency"),
            pytest.param("all", id="all_expectations"),
        ],
    )
    def test_method__read__reports_only_conflicting_expectations(
        self, tmp_path: Path, field: str
    ) -> None:
        """Evidence ID: SV-SQLITE-011

        Requirement: Mismatch reports the full expected set and only conflicting
        observed identities.

        Method: Read independent fixture r1 with one or all expectations changed.

        Oracle: Hand-authored fixture fields and sorted public expectation vocabulary.

        Acceptance: Mismatch contains exactly sorted conflicting observations
        and no payload.

        Interpretation: Failure detects incomplete reconciliation or result leakage.

        Limitations: No domain payload schema is interpreted.
        """
        store = self.make_fixture(tmp_path / "store.db")
        expected = (
            (
                "content_id",
                "different" if field in ("all", "content_id") else "content",
            ),
            (
                "idempotency_id",
                "different" if field in ("all", "idempotency_id") else "k1",
            ),
            (
                "predecessor_revision_id",
                "different" if field in ("all", "predecessor_revision_id") else None,
            ),
            ("schema_id", "different" if field in ("all", "schema_id") else "schema"),
        )
        request = RevisionReadRequest(
            "reconcile",
            "s",
            RevisionSelector.EXPLICIT_REVISION,
            "r1",
            expected[2][1],
            expected[3][1],
            expected[0][1],
            expected[1][1],
        )
        result = store.read(request)
        actual = (
            ("content_id", "content"),
            ("idempotency_id", "k1"),
            ("predecessor_revision_id", None),
            ("schema_id", "schema"),
        )
        assert result.status is RevisionReadStatus.MISMATCH
        assert result.expected_identities == expected
        assert result.observed_identities == (
            actual
            if field == "all"
            else tuple(pair for pair in actual if pair[0] == field)
        )
        assert result.mismatched_fields == (
            tuple(name for name, _ in actual) if field == "all" else (field,)
        )
        assert result.requested_revision_id == "r1"
        assert result.revision is None

    def test_method__read__accepts_independent_private_format_fixture(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-012

        Requirement: Supported private format and integrity framing preserve
        independent bytes.

        Method: Load hand-authored SQL and observe both historical and latest revisions.

        Oracle: Fixture literals and hand-specified public records, not
        serializer output.

        Acceptance: r1 and r2 are found with all six exact fields and bytes.

        Interpretation: Failure detects correlated serializer round-trip defects.

        Limitations: This private v1 format is not a domain wire or migration promise.
        """
        store = self.make_fixture(tmp_path / "store.db")
        assert store.read(self.make_request("r1")).revision == Revision(
            "s", "r1", None, "schema", "content", b"\x00\xff"
        )
        assert store.read(self.make_request()).revision == Revision(
            "s", "r2", "r1", "schema", "content", b"\x02"
        )

    @pytest.mark.parametrize(
        "sql",
        [
            pytest.param(
                "UPDATE revisions SET payload='wrong native type' "
                "WHERE revision=X'7231';",
                id="wrong_native_type",
            ),
            pytest.param(
                "UPDATE revisions SET digest=X'00' WHERE revision=X'7231';",
                id="truncated_digest",
            ),
            pytest.param(
                "UPDATE revisions SET payload=X'01' WHERE revision=X'7231';",
                id="changed_bytes",
            ),
            pytest.param(
                "DELETE FROM revisions WHERE revision=X'7231';",
                id="missing_predecessor",
            ),
            pytest.param(
                "UPDATE heads SET revision=X'6d697373696e67';", id="dangling_head"
            ),
            pytest.param("DELETE FROM heads;", id="missing_head"),
            pytest.param(
                "UPDATE revisions SET stream='s'; UPDATE heads SET stream='s';",
                id="text_addresses_cannot_hide_from_blob_lookup",
            ),
            pytest.param(
                "UPDATE revisions SET predecessor=X'7232', "
                "digest=X'389e9e1d69eefe03591c0ef1b375e97ca"
                "eca3796e0be288faf800474b4559816' WHERE revision=X'7231';",
                id="cycle_with_valid_digest",
            ),
            pytest.param(
                "UPDATE store_format SET version='bad';", id="wrong_metadata_type"
            ),
            pytest.param(
                "ALTER TABLE heads ADD COLUMN unexpected BLOB;",
                id="malformed_recognized_schema",
            ),
        ],
    )
    def test_method__read__refuses_corrupt_closure(
        self, tmp_path: Path, sql: str
    ) -> None:
        """Evidence ID: SV-SQLITE-013

        Requirement: Malformed generic integrity is corrupt, never found or absence.

        Method: Apply one corruption to independent SQL fixture, then read and commit.

        Oracle: Native type, fixed digest, same-stream closure and acyclic
        history rules.

        Acceptance: Read corrupt without revision; commit error with integrity_failure;
        no revision inserted by attempted write.

        Interpretation: Failure detects malformed-row acceptance or destructive repair.

        Limitations: Cycle digest is independently framed to reach graph validation;
        coordinated rewriting of both data and hash is not authentication evidence.
        """
        path = tmp_path / "store.db"
        store = self.make_fixture(path)
        self.execute_sql(path, sql)
        before = self.observe_count(path)
        result = store.read(self.make_request())
        assert result.status is RevisionReadStatus.CORRUPT
        assert result.integrity_findings and result.revision is None
        written = store.commit(
            self.make_commit(revision="r3", predecessor="r2", key="k3")
        )
        assert written.status is CommitStatus.ERROR
        assert (
            written.failure is not None and written.failure.code == "integrity_failure"
        )
        assert self.observe_count(path) == before

    @pytest.mark.parametrize(
        "sql,observed",
        [
            pytest.param(
                "UPDATE revisions SET digest=X'00' WHERE revision=X'7231';",
                (("content_id", "content"), ("revision_id", "r1")),
                id="readable_historical_digest_failure",
            ),
            pytest.param(
                "UPDATE revisions SET content=X'6f62736572766564' "
                "WHERE revision=X'7231';",
                (("content_id", "observed"), ("revision_id", "r1")),
                id="changed_readable_content_is_not_request_identity",
            ),
            pytest.param(
                "UPDATE revisions SET payload='bad' WHERE revision=X'7231';",
                (("content_id", "content"), ("revision_id", "r1")),
                id="payload_native_type_failure",
            ),
            pytest.param(
                "UPDATE revisions SET schema_id=X'ff' WHERE revision=X'7231';",
                (("content_id", "content"), ("revision_id", "r1")),
                id="other_identity_unreadable",
            ),
            pytest.param(
                "UPDATE revisions SET content=X'ff' WHERE revision=X'7231';",
                (("revision_id", "r1"),),
                id="only_revision_readable",
            ),
            pytest.param(
                "UPDATE revisions SET revision=X'ff' WHERE revision=X'7231';",
                (("content_id", "content"),),
                id="only_content_readable",
            ),
            pytest.param(
                "UPDATE revisions SET revision='r1' WHERE revision=X'7231';",
                (("content_id", "content"),),
                id="native_address_failure_keeps_content",
            ),
            pytest.param(
                "UPDATE revisions SET content=X'ff', revision=X'ff' "
                "WHERE revision=X'7231';",
                (),
                id="neither_identity_readable",
            ),
            pytest.param(
                "DELETE FROM heads;",
                (("content_id", "content"), ("revision_id", "r1")),
                id="missing_head_keeps_surviving_revision",
            ),
            pytest.param(
                "UPDATE heads SET revision=X'6d697373696e67';",
                (("revision_id", "missing"),),
                id="dangling_head_keeps_only_stored_reference",
            ),
            pytest.param(
                "DELETE FROM revisions WHERE revision=X'7231';",
                (("content_id", "content"), ("revision_id", "r2")),
                id="missing_predecessor_keeps_referring_revision",
            ),
            pytest.param(
                "UPDATE revisions SET predecessor=X'7232', "
                "digest=X'389e9e1d69eefe03591c0ef1b375e97ca"
                "eca3796e0be288faf800474b4559816' WHERE revision=X'7231';",
                (("content_id", "content"), ("revision_id", "r2")),
                id="cycle_keeps_revisited_revision",
            ),
            pytest.param(
                "UPDATE heads SET revision=X'7231';",
                (("content_id", "content"), ("revision_id", "r2")),
                id="orphan_keeps_unreachable_revision",
            ),
            pytest.param(
                "UPDATE store_format SET version='bad';",
                (),
                id="metadata_failure_does_not_fabricate_revision",
            ),
        ],
    )
    def test_method__read__retains_readable_corrupt_identities(
        self,
        tmp_path: Path,
        sql: str,
        observed: tuple[tuple[str, str | None], ...],
    ) -> None:
        """Evidence ID: SV-SQLITE-029

        Requirement: Corrupt outcomes retain sorted readable stored revision/content
        identities without returning a revision or claiming reconciliation success.

        Method: Mutate one native SQL fixture field or closure edge and read both
        latest and an explicit successor whose history includes the affected row.

        Oracle: Literal stored labels or head reference; invalid native types and
        invalid UTF-8 are not readable identity observations.

        Acceptance: Exact fault-local observation tuple, corrupt status and integrity
        finding; no payload, mismatch fields, expected identities or validity claim.

        Interpretation: Failure detects discarded readable evidence or substitution
        of requested identities for actual stored observations.

        Limitations: Labels are observations only, not verified content identities;
        one fault is reported, not an aggregate database-integrity audit.
        """
        path = tmp_path / "store.db"
        store = self.make_fixture(path)
        self.execute_sql(path, sql)
        self.assert_corrupt_identities(store.read(self.make_request()), observed)
        self.assert_corrupt_identities(store.read(self.make_request("r2")), observed)

    @pytest.mark.parametrize(
        "sql,version",
        [
            pytest.param(
                "UPDATE store_format SET version=2;", "store.2", id="unsupported_store"
            ),
            pytest.param(
                "UPDATE revisions SET envelope=2 WHERE revision=X'7231';",
                "envelope.2",
                id="unsupported_envelope",
            ),
        ],
    )
    def test_method__read__refuses_unsupported_versions(
        self, tmp_path: Path, sql: str, version: str
    ) -> None:
        """Evidence ID: SV-SQLITE-014

        Requirement: Unknown store or envelope version is incompatible and
        never migrated.

        Method: Modify one fixture version and attempt read and write.

        Oracle: Explicit private v1 support boundary and unchanged database bytes.

        Acceptance: Incompatible with exact version, commit unsupported_version error,
        database bytes unchanged and no revision returned.

        Interpretation: Failure detects guessed compatibility or implicit migration.

        Limitations: Caller schema_id is intentionally not treated as envelope version.
        """
        path = tmp_path / "store.db"
        store = self.make_fixture(path)
        self.execute_sql(path, sql)
        before = path.read_bytes()
        result = store.read(self.make_request())
        assert result.status is RevisionReadStatus.INCOMPATIBLE
        assert result.unsupported_version_ids == (version,)
        assert result.revision is None
        written = store.commit(
            self.make_commit(revision="r3", predecessor="r2", key="k3")
        )
        assert written.status is CommitStatus.ERROR
        assert (
            written.failure is not None
            and written.failure.code == "unsupported_version"
        )
        assert path.read_bytes() == before

    @pytest.mark.parametrize(
        "kind,status",
        [
            pytest.param(
                "unrelated", RevisionReadStatus.INCOMPATIBLE, id="unrelated_database"
            ),
            pytest.param("native", RevisionReadStatus.CORRUPT, id="not_a_database"),
        ],
    )
    def test_method__read__does_not_initialize_over_existing_content(
        self, tmp_path: Path, kind: str, status: RevisionReadStatus
    ) -> None:
        """Evidence ID: SV-SQLITE-015

        Requirement: Existing unrelated or non-database files must not be initialized.

        Method: Supply an unrelated SQL table or non-database bytes.

        Oracle: Original exact file bytes and closed compatibility/integrity outcomes.

        Acceptance: Expected refusal without revision or file mutation.

        Interpretation: Failure detects destructive bootstrap or fabricated absence.

        Limitations: These are synthetic files, never retained calculation data.
        """
        path = tmp_path / "store.db"
        if kind == "unrelated":
            self.execute_sql(
                path,
                "CREATE TABLE other (value TEXT); "
                "INSERT INTO other VALUES ('retained');",
            )
        else:
            path.write_bytes(b"not a sqlite database\x00" * 20)
        before = path.read_bytes()
        result = self.make_store(path).read(self.make_request())
        assert result.status is status
        assert result.revision is None
        assert path.read_bytes() == before

    @pytest.mark.parametrize(
        "payload",
        [
            pytest.param(b"", id="empty_bytes"),
            pytest.param(b"\x00\xff\x80", id="arbitrary_binary"),
        ],
    )
    def test_method__commit__preserves_full_identity_and_payload_domain(
        self, tmp_path: Path, payload: bytes
    ) -> None:
        """Evidence ID: SV-SQLITE-016

        Requirement: Accepted strings including NUL and surrogates remain exact
        BLOB identities.

        Method: Commit non-ASCII, NUL and unpaired surrogate identities and
        binary bytes.

        Oracle: Exact supplied public Commit, without Unicode normalization.

        Acceptance: Found and replay preserve all input fields and payload bytes.

        Interpretation: Failure detects SQL TEXT encoding or narrowing the
        accepted identity grammar.

        Limitations: No semantic interpretation of identities or bytes.
        """
        store = self.make_store(tmp_path / "store.db")
        commit = Commit(
            None,
            Revision(
                "s\x00é\ud800", "r\udfff", None, "schema\x00", "contenté", payload
            ),
            "key\ud800",
        )
        assert store.commit(commit).revision == commit.candidate
        assert (
            store.read(self.make_request(stream=commit.candidate.stream_id)).revision
            == commit.candidate
        )
        assert store.commit(commit).revision == commit.candidate

    def test_method__commit__enforces_payload_cap_without_partial_revision(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-017

        Requirement: Payload caps refuse oversize writes and reads, without truncation.

        Method: Write at cap then oversize, and reopen with a smaller cap.

        Oracle: Exact cap in bytes and independent row count.

        Acceptance: At-cap commits; over-cap write and read error with payload_limit,
        one complete row remains and no revision leaks on refusal.

        Interpretation: Failure detects partial payloads or mutation before
        resource refusal.

        Limitations: Native SQLite may impose smaller limits than configured.
        """
        path = tmp_path / "store.db"
        store = self.make_store(path, cap=2)
        assert store.commit(self.make_commit()).status is CommitStatus.COMMITTED
        result = store.commit(
            self.make_commit(revision="r2", predecessor="r1", key="k2", payload=b"big")
        )
        assert result.status is CommitStatus.ERROR
        assert result.failure is not None and result.failure.code == "payload_limit"
        read = self.make_store(path, cap=1).read(self.make_request())
        assert read.status is RevisionReadStatus.ERROR
        assert read.failure is not None and read.failure.code == "payload_limit"
        assert read.revision is None
        assert self.observe_count(path) == 1

    def test_method__read__distinguishes_setup_and_interrupted_observation(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-018

        Requirement: Setup error differs from uncertainty after observation begins.

        Method: Use missing parent then inject SQLite interruption during observation.

        Oracle: Explicit phase boundaries, sanitized failure codes and no
        presence claim.

        Acceptance: Missing parent is open_failed error without directory creation;
        interrupted read is read_interrupted indeterminate without payload.

        Interpretation: Failure detects false absence or leaked native diagnostics.

        Limitations: Private seam injects failure only, not a success oracle.
        """
        path = tmp_path / "missing" / "store.db"
        result = self.make_store(path).read(self.make_request())
        assert result.status is RevisionReadStatus.ERROR
        assert result.failure is not None and result.failure.code == "open_failed"
        assert result.failure.operation_phase == "read.open"
        assert not path.parent.exists()
        store = self.make_store(tmp_path / "store.db")
        with patch.object(
            SQLiteAtomicRevisionStore,
            "_stream",
            staticmethod(self.interrupt_observation),
        ):
            interrupted = store.read(self.make_request())
        assert interrupted.status is RevisionReadStatus.INDETERMINATE
        assert (
            interrupted.failure is not None
            and interrupted.failure.code == "read_interrupted"
        )
        assert interrupted.revision is None and "sensitive" not in str(interrupted)

    def test_method__read__represents_native_path_rejection(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-027

        Requirement: A native opener rejecting an absolute Path is an open error.

        Method: Construct an effect-free store with a NUL-containing filename and
        invoke both public operations.

        Oracle: Native filesystem names prohibit NUL, without a new Path grammar
        imposed by the public constructor.

        Acceptance: Both operations return error with open_failed and no revision.

        Interpretation: Failure leaks a driver exception instead of a closed result.

        Limitations: No file is created and no calculation path is accessed.
        """
        store = self.make_store(tmp_path / "invalid\x00database")
        read = store.read(self.make_request())
        written = store.commit(self.make_commit())
        assert read.status is RevisionReadStatus.ERROR
        assert written.status is CommitStatus.ERROR
        assert read.failure is not None and read.failure.code == "open_failed"
        assert written.failure is not None and written.failure.code == "open_failed"
        assert read.revision is None and written.revision is None

    def test_method__commit__retains_confirmed_evidence_on_close_trouble(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-019

        Requirement: Close trouble cannot erase an acknowledged commit observation.

        Method: Inject a close diagnostic after closing the real connection.

        Oracle: Fresh reopened candidate and independently committed result status.

        Acceptance: Committed result includes diagnostic and exact candidate persists.

        Interpretation: Failure detects invented rollback after established commit.

        Limitations: Narrow fault injection does not reproduce a native close failure.
        """
        path = tmp_path / "store.db"
        with patch.object(
            SQLiteAtomicRevisionStore, "_close", staticmethod(self.close_with_failure)
        ):
            result = self.make_store(path).commit(self.make_commit())
        assert result.status is CommitStatus.COMMITTED
        assert result.diagnostics == (
            "connection_close_failed; established observation retained",
        )
        assert (
            self.make_store(path).read(self.make_request()).revision
            == self.make_commit().candidate
        )

    def test_constructor__configuration__is_immutable_and_effect_free(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-020

        Requirement: Explicit configuration is immutable and constructor
        performs no I/O.

        Method: Construct, attempt mutation, then perform a first read.

        Oracle: Frozen dataclass semantics and documented read-side bootstrap boundary.

        Acceptance: Constructor creates nothing, mutation fails, first read initializes
        the file and returns absence.

        Interpretation: Failure detects hidden mutable configuration or
        constructor effects.

        Limitations: Runtime scratch only; no path discovery or parent creation.
        """
        path = tmp_path / "store.db"
        store = self.make_store(path)
        assert not path.exists()
        with pytest.raises(FrozenInstanceError):
            store.busy_timeout_ms = 5  # type: ignore[misc]
        assert store.read(self.make_request()).status is RevisionReadStatus.ABSENT
        assert path.exists()

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(True, id="boolean"),
            pytest.param("1", id="numeric_string"),
            pytest.param(1.0, id="float"),
        ],
    )
    def test_constructor__configuration__rejects_non_integer_limits(
        self, tmp_path: Path, value: bool | str | float
    ) -> None:
        """Evidence ID: SV-SQLITE-021

        Requirement: Numeric configuration accepts only built-in integers
        excluding bool.

        Method: Pass each wrong-type partition to both numeric slots.

        Oracle: Public semantic type contract without coercion.

        Acceptance: Each wrong type raises TypeError before database creation.

        Interpretation: Failure detects Boolean acceptance or implicit conversion.

        Limitations: Valid range boundaries have separate evidence.
        """
        path = tmp_path / "store.db"
        with pytest.raises(TypeError):
            SQLiteAtomicRevisionStore(path, busy_timeout_ms=value, max_payload_bytes=1)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            SQLiteAtomicRevisionStore(path, busy_timeout_ms=0, max_payload_bytes=value)  # type: ignore[arg-type]
        assert not path.exists()

    @pytest.mark.parametrize(
        "timeout,cap",
        [
            pytest.param(-1, 1, id="negative_timeout"),
            pytest.param(2147483648, 1, id="timeout_overflow"),
            pytest.param(0, 0, id="zero_payload_cap"),
            pytest.param(0, 2147483648, id="payload_cap_overflow"),
        ],
    )
    def test_constructor__configuration__rejects_out_of_range_limits(
        self, tmp_path: Path, timeout: int, cap: int
    ) -> None:
        """Evidence ID: SV-SQLITE-022

        Requirement: Configuration integers remain within explicit finite limits.

        Method: Supply each invalid range boundary.

        Oracle: Millisecond and byte ranges from the constructor contract.

        Acceptance: ValueError and no database file.

        Interpretation: Failure detects overflow or unsupported resource policy.

        Limitations: No large payload is allocated by these constructor tests.
        """
        path = tmp_path / "store.db"
        with pytest.raises(ValueError):
            SQLiteAtomicRevisionStore(
                path, busy_timeout_ms=timeout, max_payload_bytes=cap
            )
        assert not path.exists()

    def test_constructor__path__requires_absolute_concrete_path(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-023

        Requirement: Path configuration is explicit filesystem selection, not
        URI or memory.

        Method: Pass a string and a relative memory-style Path.

        Oracle: pathlib concrete absolute-path contract.

        Acceptance: Wrong type raises TypeError, relative Path raises ValueError;
        upper numeric boundary constructs without I/O.

        Interpretation: Failure detects implicit database selection or path coercion.

        Limitations: Absolute filenames resembling URI text remain ordinary files.
        """
        with pytest.raises(TypeError):
            SQLiteAtomicRevisionStore(
                "file:memory?mode=memory",  # type: ignore[arg-type]
                busy_timeout_ms=0,
                max_payload_bytes=1,
            )
        with pytest.raises(ValueError):
            self.make_store(Path(":memory:"))
        path = tmp_path / "store.db"
        SQLiteAtomicRevisionStore(
            path, busy_timeout_ms=2147483647, max_payload_bytes=2147483647
        )
        assert not path.exists()

    def test_method__arguments__rejects_wrong_record_types_before_io(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-024

        Requirement: read and commit require their exact immutable public records.

        Method: Supply closed wrong-type values at the call sites.

        Oracle: Public argument exception contract and absent file.

        Acceptance: TypeError for both calls before database I/O.

        Interpretation: Failure detects erased software input or partial execution.

        Limitations: Record intrinsic tests remain in predecessor evidence.
        """
        path = tmp_path / "store.db"
        store = self.make_store(path)
        with pytest.raises(TypeError):
            store.read("request")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            store.commit(b"commit")  # type: ignore[arg-type]
        assert not path.exists()

    def test_method__results__retains_correlation_and_frozen_observations(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-025

        Requirement: Store-produced observations retain exact source and
        distinct result identities.

        Method: Commit and read twice, checking correlation and attempted mutation.

        Oracle: Input identities, fixed implementation/version and immutable
        result contract.

        Acceptance: Exact correlations, independent result IDs, no mutable result
        or revision.

        Interpretation: Failure detects observation/source identity substitution.

        Limitations: Random observation IDs are not persistence or provenance
        authentication.
        """
        store = self.make_store(tmp_path / "store.db")
        commit = self.make_commit()
        result = store.commit(commit)
        request = self.make_request("r1")
        first, second = store.read(request), store.read(request)
        assert (result.idempotency_id, result.stream_id) == ("k1", "s")
        assert (first.request_id, first.stream_id, first.selector) == (
            request.request_id,
            request.stream_id,
            request.selector,
        )
        assert (
            first.store_implementation_id
            == "ksdft2effmass.persistence.SQLiteAtomicRevisionStore"
        )
        assert first.store_version_id == "1"
        assert (
            first.result_id != second.result_id and first.result_id != result.result_id
        )
        with pytest.raises(FrozenInstanceError):
            first.result_id = "changed"  # type: ignore[misc]
        assert first.revision is not None
        with pytest.raises(FrozenInstanceError):
            first.revision.payload = b"changed"  # type: ignore[misc]

    def test_public_api__package__exports_exact_store_surface(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-SQLITE-026

        Requirement: The concrete store adds exactly one supported export and
        no domain dependency.

        Method: Check public inventory, structural protocol and static import roots.

        Oracle: Accepted persistence architecture and explicit supported name inventory.

        Acceptance: Exact exports, protocol conformance, standard-library/store-only
        imports.

        Interpretation: Failure detects scope expansion or dependency inversion.

        Limitations: Static imports do not prove all runtime behavior; behavioral
        tests are separate.
        """
        assert set(persistence.__all__) == {
            "AtomicRevisionStore",
            "Commit",
            "CommitResult",
            "CommitStatus",
            "Revision",
            "RevisionReadRequest",
            "RevisionReadResult",
            "RevisionReadStatus",
            "RevisionSelector",
            "StoreOperationalFailure",
            "SQLiteAtomicRevisionStore",
        }
        assert isinstance(self.make_store(tmp_path / "store.db"), AtomicRevisionStore)
        source = Path(persistence.__file__).parent / "sqlite.py"
        tree = ast.parse(source.read_text())
        roots = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        absolute = {
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module
        }
        relative = {
            (node.level, node.module)
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.level
        }
        assert roots | absolute <= sys.stdlib_module_names
        assert relative == {(1, "store")}
