"""Local SQLite storage of complete opaque revision envelopes.

The store owns atomic compare-and-swap, database-wide idempotency and private
SHA-256 integrity framing, not payload schemas or scientific validity. Each
operation owns one connection and transaction. No domain repository, migration,
external effect, or cross-database transaction is implemented here.
"""

from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import cast
from uuid import uuid4

from .store import (
    Commit,
    CommitResult,
    CommitStatus,
    IdentityObservation,
    Revision,
    RevisionReadRequest,
    RevisionReadResult,
    RevisionReadStatus,
    RevisionSelector,
    StoreOperationalFailure,
)

type _SQLiteValue = None | int | float | str | bytes
type _Row = tuple[_SQLiteValue, ...]

_IMPLEMENTATION = "ksdft2effmass.persistence.SQLiteAtomicRevisionStore"
_VERSION = "1"
_BOUNDARY = "Generic local storage observation only; no domain or scientific validity."
_TABLES = (
    (
        "store_format",
        "CREATE TABLE store_format (format BLOB NOT NULL, version INTEGER NOT NULL)",
    ),
    (
        "revisions",
        "CREATE TABLE revisions (stream BLOB NOT NULL, revision BLOB NOT NULL, "
        "predecessor BLOB, schema_id BLOB NOT NULL, content BLOB NOT NULL, "
        "payload BLOB NOT NULL, idempotency BLOB NOT NULL UNIQUE, "
        "envelope INTEGER NOT NULL, digest BLOB NOT NULL, "
        "PRIMARY KEY (stream, revision), FOREIGN KEY (stream, predecessor) "
        "REFERENCES revisions (stream, revision))",
    ),
    (
        "heads",
        "CREATE TABLE heads (stream BLOB PRIMARY KEY NOT NULL, revision BLOB NOT NULL, "
        "FOREIGN KEY (stream, revision) REFERENCES revisions (stream, revision))",
    ),
)
_FORMAT = b"ksdft2effmass.sqlite.revisions"


class _StorageFault(Exception):
    """Carry fixed sanitized findings and exact readable identity observations."""

    def __init__(
        self,
        code: str,
        version: str | None = None,
        *,
        observed: IdentityObservation = (),
    ) -> None:
        super().__init__(code)
        self.code = code
        self.version = version
        self.observed = observed


@dataclass(frozen=True, slots=True)
class _Envelope:
    revision: Revision
    idempotency_id: str


class _RevisionRowSerializer:
    """Own native-value decoding and private envelope-v1 integrity framing.

    The hash input is a fixed prefix followed by stream, revision, predecessor,
    schema, content, payload and idempotency. Present byte fields have unsigned
    eight-byte big-endian lengths. Predecessor has a one-byte 0/1 presence tag.
    Identity bytes use UTF-8 surrogatepass without normalization. This digest is
    not the domain content identity, authentication, or a public domain wire.
    """

    @staticmethod
    def encode_identity(value: str) -> bytes:
        return value.encode("utf-8", "surrogatepass")

    @staticmethod
    def decode_identity(value: _SQLiteValue) -> str:
        if type(value) is not bytes:
            raise _StorageFault("integrity_failure")
        try:
            result = value.decode("utf-8", "surrogatepass")
        except UnicodeError:
            raise _StorageFault("integrity_failure") from None
        if not result:
            raise _StorageFault("integrity_failure")
        return result

    @classmethod
    def encode(cls, envelope: _Envelope) -> _Row:
        revision = envelope.revision
        fields: tuple[bytes | None, ...] = (
            cls.encode_identity(revision.stream_id),
            cls.encode_identity(revision.revision_id),
            None
            if revision.predecessor_revision_id is None
            else cls.encode_identity(revision.predecessor_revision_id),
            cls.encode_identity(revision.schema_id),
            cls.encode_identity(revision.content_id),
            revision.payload,
            cls.encode_identity(envelope.idempotency_id),
        )
        digest = hashlib.sha256(b"ksdft2effmass.sqlite.revision.v1\x00")
        for index, encoded in enumerate(fields):
            if index == 2:
                digest.update(b"\x00" if encoded is None else b"\x01")
            if encoded is not None:
                digest.update(len(encoded).to_bytes(8, "big"))
                digest.update(encoded)
        return (*fields, 1, digest.digest())

    @classmethod
    def observe_identities(
        cls, revision: _SQLiteValue, content: _SQLiteValue = None
    ) -> IdentityObservation:
        """Retain independently readable stored labels, without asserting validity."""
        observed: list[tuple[str, str | None]] = []
        for name, value in (("content_id", content), ("revision_id", revision)):
            try:
                decoded = cls.decode_identity(value)
            except _StorageFault:
                continue
            observed.append((name, decoded))
        return tuple(observed)

    @classmethod
    def decode(cls, row: _Row, limit: int) -> _Envelope:
        if len(row) != 9:
            raise _StorageFault("integrity_failure")
        (
            stream,
            revision,
            predecessor,
            schema,
            content,
            payload,
            key,
            version,
            digest,
        ) = row
        observed = cls.observe_identities(revision, content)
        try:
            if type(version) is not int:
                raise _StorageFault("integrity_failure")
            if version != 1:
                raise _StorageFault("unsupported_version", f"envelope.{version}")
            if type(payload) is not bytes or type(digest) is not bytes:
                raise _StorageFault("integrity_failure")
            if len(payload) > limit:
                raise _StorageFault("payload_limit")
            value = Revision(
                cls.decode_identity(stream),
                cls.decode_identity(revision),
                None if predecessor is None else cls.decode_identity(predecessor),
                cls.decode_identity(schema),
                cls.decode_identity(content),
                payload,
            )
            envelope = _Envelope(value, cls.decode_identity(key))
            if cls.encode(envelope) != row:
                raise _StorageFault("integrity_failure")
        except _StorageFault as fault:
            raise _StorageFault(fault.code, fault.version, observed=observed) from None
        except TypeError, ValueError:
            raise _StorageFault("integrity_failure", observed=observed) from None
        return envelope


@dataclass(frozen=True, slots=True)
class SQLiteAtomicRevisionStore:
    """Atomically store opaque revisions in one explicit local SQLite file.

    Parameters
    ----------
    database_path : pathlib.Path
        Absolute filesystem path, not a URI or memory database. The parent must
        exist. Construction performs no I/O; the first operation, even a read,
        transactionally initializes a genuinely empty database.
    busy_timeout_ms : int
        Keyword-only built-in integer timeout in milliseconds, 0 through
        2,147,483,647. No retry loop is performed.
    max_payload_bytes : int
        Keyword-only built-in integer per-payload cap, 1 through 2,147,483,647
        bytes. Larger payloads return an operational failure, never truncation.
        SQLite native limits may be smaller and also yield operational failure.

    Raises
    ------
    TypeError
        Wrong semantic types, including Boolean, string or NumPy numeric values.
    ValueError
        Relative path or numeric value outside its declared range.

    Notes
    -----
    Configuration is immutable. Each call closes its private connection. SQLite
    DELETE journaling, FULL synchronization, foreign keys and a bounded busy
    timeout implement the local transaction boundary. Unsupported formats are
    refused, not migrated. Unowned triggers are refused before reads or writes.
    Payload bytes and history traversal remain in memory;
    no aggregate database-size, throughput, network-filesystem, backup, hardware
    power-loss or scientific-validation guarantee is made. Separate physical
    development and scientific databases remain the application's responsibility.

    Examples
    --------
    Construction alone creates no database:

    >>> from pathlib import Path
    >>> from ksdft2effmass.persistence import SQLiteAtomicRevisionStore
    >>> store = SQLiteAtomicRevisionStore(
    ...     Path('/explicit/local/revisions.sqlite3'),
    ...     busy_timeout_ms=1000, max_payload_bytes=1048576)
    """

    database_path: Path
    busy_timeout_ms: int = field(kw_only=True)
    max_payload_bytes: int = field(kw_only=True)

    def __post_init__(self) -> None:
        if not isinstance(self.database_path, Path):
            raise TypeError("database_path must be a concrete pathlib.Path")
        if not self.database_path.is_absolute():
            raise ValueError("database_path must be absolute")
        for name, value, minimum in (
            ("busy_timeout_ms", self.busy_timeout_ms, 0),
            ("max_payload_bytes", self.max_payload_bytes, 1),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if not minimum <= value <= 2147483647:
                raise ValueError(f"{name} is outside its supported range")

    def read(self, request: RevisionReadRequest) -> RevisionReadResult:
        """Observe latest or one exact historical address in a consistent read.

        Parameters
        ----------
        request : RevisionReadRequest
            Exact stream, selector, request identity and optional complete
            reconciliation expectations. No implicit selection is performed.

        Returns
        -------
        RevisionReadResult
            Found, absent, mismatch, incompatible, corrupt, indeterminate or
            error. Only found carries a revision. Setup failure is error;
            interrupted observation is indeterminate. Corrupt retains readable
            stored revision/content labels, not a payload or a validity claim.
            No automatic retry occurs.

        Raises
        ------
        TypeError
            If request is not the exact public request record, before I/O.
        """
        if type(request) is not RevisionReadRequest:
            raise TypeError("request must be RevisionReadRequest")
        connection: sqlite3.Connection | None = None
        phase = "read.open"
        result: RevisionReadResult
        try:
            connection = self._connect()
            phase = "read.setup"
            self._prepare(connection)
            connection.execute("BEGIN")
            phase = "read.observe"
            self._recognize(connection)
            head, revisions = self._stream(connection, request.stream_id)
            address = (
                head
                if request.selector is RevisionSelector.LATEST
                else request.revision_id
            )
            envelope = revisions.get(address) if address is not None else None
            result = self._read_observation(request, envelope)
        except _StorageFault as fault:
            result = self._read_fault(request, phase, fault)
        except (sqlite3.Error, OSError) as error:
            result = self._read_fault(request, phase, self._native_fault(error, phase))
        finally:
            diagnostic = self._close(connection)
        if diagnostic:
            result = replace(result, diagnostics=(*result.diagnostics, diagnostic))
        return result

    def commit(self, commit: Commit) -> CommitResult:
        """Compare and atomically append one complete revision to one stream.

        Parameters
        ----------
        commit : Commit
            Exact candidate, predecessor expectation and database-wide
            idempotency identity. Exact replay returns the original revision,
            even after the stream head advances; changed binding conflicts.

        Returns
        -------
        CommitResult
            Committed, conflict, indeterminate or error. SQL commit attempted
            without acknowledgement is indeterminate, regardless of rollback.
            Known precommit failure is error, not a compare-and-swap conflict.
            Confirmed commits retain their evidence even if close fails.

        Raises
        ------
        TypeError
            If commit is not the exact public Commit record, before I/O.
        """
        if type(commit) is not Commit:
            raise TypeError("commit must be Commit")
        connection: sqlite3.Connection | None = None
        phase = "commit.open"
        result: CommitResult
        try:
            if len(commit.candidate.payload) > self.max_payload_bytes:
                raise _StorageFault("payload_limit")
            connection = self._connect()
            phase = "commit.setup"
            self._prepare(connection)
            connection.execute("BEGIN IMMEDIATE")
            phase = "commit.observe"
            self._recognize(connection)
            result = self._candidate(connection, commit)
            if result.status is CommitStatus.COMMITTED:
                phase = "commit.acknowledge"
                self._commit_transaction(connection)
        except _StorageFault as fault:
            result = self._commit_fault(commit, phase, fault)
        except (sqlite3.Error, OSError) as error:
            result = self._commit_fault(commit, phase, self._native_fault(error, phase))
        finally:
            diagnostic = self._close(connection)
        if diagnostic:
            result = replace(result, diagnostics=(*result.diagnostics, diagnostic))
        return result

    def _connect(self) -> sqlite3.Connection:
        try:
            return sqlite3.connect(
                self.database_path,
                timeout=self.busy_timeout_ms / 1000,
                isolation_level=None,
            )
        except ValueError:
            # A concrete Path can contain a NUL rejected by the native opener.
            # Adapt that operational path failure only at the driver call.
            raise _StorageFault("open_failed") from None

    @staticmethod
    def _commit_transaction(connection: sqlite3.Connection) -> None:
        connection.execute("COMMIT")

    @staticmethod
    def _close(connection: sqlite3.Connection | None) -> str | None:
        if connection is None:
            return None
        try:
            connection.close()  # Close rolls back any still-open transaction.
        except sqlite3.Error, OSError:
            return "connection_close_failed; established observation retained"
        return None

    @staticmethod
    def _rows(
        connection: sqlite3.Connection, sql: str, parameters: _Row = ()
    ) -> tuple[_Row, ...]:
        # sqlite3's dynamically typed driver is adapted once to its closed native
        # representation. The serializer validates every used row and value.
        return tuple(cast(list[_Row], connection.execute(sql, parameters).fetchall()))

    def _recognize(self, connection: sqlite3.Connection) -> bool:
        tables = self._rows(
            connection,
            "SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name",
        )
        if not tables:
            if self._rows(connection, "SELECT name FROM sqlite_master"):
                raise _StorageFault("integrity_failure")
            return False
        if not any(row[0] == "store_format" for row in tables):
            raise _StorageFault("unsupported_version", "store.unrecognized")
        # Query shape only after checking the metadata table's actual layout.
        metadata_sql = next(row[1] for row in tables if row[0] == "store_format")
        if metadata_sql != _TABLES[0][1]:
            raise _StorageFault("integrity_failure")
        metadata = self._rows(connection, "SELECT format, version FROM store_format")
        if len(metadata) != 1 or len(metadata[0]) != 2:
            raise _StorageFault("integrity_failure")
        identity, version = metadata[0]
        if type(identity) is not bytes or type(version) is not int:
            raise _StorageFault("integrity_failure")
        if identity != _FORMAT or version != 1:
            raise _StorageFault("unsupported_version", f"store.{version}")
        if tables != tuple(sorted(_TABLES)):
            raise _StorageFault("integrity_failure")
        # The private schema owns no executable triggers. Refuse them before any
        # write, including replay, rather than letting one-stream SQL alter other
        # streams or metadata. The transaction lock prevents a schema-change race.
        if self._rows(
            connection,
            "SELECT name FROM sqlite_master WHERE type IN ('view', 'trigger')",
        ):
            raise _StorageFault("integrity_failure")
        # Invalid native addresses must not hide rows from BLOB-key lookups and
        # turn malformed represented state into a fabricated absence.
        for table in ("revisions", "heads"):
            fields = "revision, content" if table == "revisions" else "revision, NULL"
            malformed = self._rows(
                connection,
                f"SELECT {fields} FROM {table} WHERE typeof(stream) != 'blob' "
                "OR length(stream) = 0 OR typeof(revision) != 'blob' "
                "OR length(revision) = 0 ORDER BY stream, revision LIMIT 1",
            )
            if malformed:
                raise _StorageFault(
                    "integrity_failure",
                    observed=_RevisionRowSerializer.observe_identities(*malformed[0]),
                )
        return True

    def _prepare(self, connection: sqlite3.Connection) -> None:
        # Recognize under one snapshot before any journal-setting/schema change.
        connection.execute("BEGIN")
        recognized = self._recognize(connection)
        connection.execute("ROLLBACK")
        if not recognized:
            connection.execute("BEGIN IMMEDIATE")
            if not self._recognize(connection):
                for _, sql in _TABLES:
                    connection.execute(sql)
                connection.execute(
                    "INSERT INTO store_format VALUES (?, ?)", (_FORMAT, 1)
                )
            connection.execute("COMMIT")
        mode = self._rows(connection, "PRAGMA journal_mode=DELETE")
        if mode != (("delete",),):
            raise _StorageFault("sqlite_failure")
        connection.execute("PRAGMA synchronous=FULL")
        connection.execute("PRAGMA foreign_keys=ON")

    def _stream(
        self, connection: sqlite3.Connection, stream: str
    ) -> tuple[str | None, dict[str, _Envelope]]:
        encoded = _RevisionRowSerializer.encode_identity(stream)
        rows = self._rows(
            connection,
            "SELECT * FROM revisions WHERE stream=? ORDER BY revision",
            (encoded,),
        )
        values: dict[str, _Envelope] = {}
        for row in rows:
            envelope = _RevisionRowSerializer.decode(row, self.max_payload_bytes)
            if envelope.revision.stream_id != stream:
                raise _StorageFault(
                    "integrity_failure",
                    observed=_RevisionRowSerializer.observe_identities(row[1], row[4]),
                )
            values[envelope.revision.revision_id] = envelope
        heads = self._rows(
            connection, "SELECT revision FROM heads WHERE stream=?", (encoded,)
        )
        if not heads:
            if rows:
                raise _StorageFault(
                    "integrity_failure",
                    observed=_RevisionRowSerializer.observe_identities(
                        rows[0][1], rows[0][4]
                    ),
                )
            return None, values
        if len(heads) != 1 or len(heads[0]) != 1:
            raise _StorageFault("integrity_failure")
        head = _RevisionRowSerializer.decode_identity(heads[0][0])
        observed = _RevisionRowSerializer.observe_identities(heads[0][0])
        visited: set[str] = set()
        address: str | None = head
        while address is not None:
            if address in values:
                revision = values[address].revision
                observed = (
                    ("content_id", revision.content_id),
                    ("revision_id", revision.revision_id),
                )
            if address in visited or address not in values:
                raise _StorageFault("integrity_failure", observed=observed)
            visited.add(address)
            address = values[address].revision.predecessor_revision_id
        if visited != values.keys():
            orphan = values[min(values.keys() - visited)].revision
            raise _StorageFault(
                "integrity_failure",
                observed=(
                    ("content_id", orphan.content_id),
                    ("revision_id", orphan.revision_id),
                ),
            )
        return head, values

    def _candidate(
        self, connection: sqlite3.Connection, commit: Commit
    ) -> CommitResult:
        head, values = self._stream(connection, commit.candidate.stream_id)
        replay = self._rows(
            connection,
            "SELECT * FROM revisions WHERE idempotency=?",
            (_RevisionRowSerializer.encode_identity(commit.idempotency_id),),
        )
        conflict: str | None = None
        if replay:
            if len(replay) != 1:
                raise _StorageFault("integrity_failure")
            original = _RevisionRowSerializer.decode(replay[0], self.max_payload_bytes)
            self._stream(connection, original.revision.stream_id)
            if original == _Envelope(commit.candidate, commit.idempotency_id):
                return self._commit_result(
                    commit, CommitStatus.COMMITTED, revision=original.revision
                )
            conflict = "idempotency_collision"
        elif commit.candidate.revision_id in values:
            conflict = "revision_collision"
        elif head != commit.expected_revision_id:
            conflict = "compare_and_swap"
        if conflict:
            return self._commit_result(
                commit, CommitStatus.CONFLICT, conflict=conflict, head=head
            )
        connection.execute(
            "INSERT INTO revisions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            _RevisionRowSerializer.encode(
                _Envelope(commit.candidate, commit.idempotency_id)
            ),
        )
        connection.execute(
            "INSERT INTO heads VALUES (?, ?) ON CONFLICT(stream) "
            "DO UPDATE SET revision=excluded.revision",
            (
                _RevisionRowSerializer.encode_identity(commit.candidate.stream_id),
                _RevisionRowSerializer.encode_identity(commit.candidate.revision_id),
            ),
        )
        stored_head, stored_values = self._stream(
            connection, commit.candidate.stream_id
        )
        expected_values = {
            **values,
            commit.candidate.revision_id: _Envelope(
                commit.candidate, commit.idempotency_id
            ),
        }
        if (
            stored_head != commit.candidate.revision_id
            or stored_values != expected_values
        ):
            # Represented corruption must not acknowledge changed candidate
            # bytes or an altered historical revision.
            raise _StorageFault("integrity_failure")
        return self._commit_result(
            commit, CommitStatus.COMMITTED, revision=commit.candidate
        )

    @staticmethod
    def _commit_result(
        commit: Commit,
        status: CommitStatus,
        *,
        revision: Revision | None = None,
        conflict: str | None = None,
        head: str | None = None,
        failure: StoreOperationalFailure | None = None,
    ) -> CommitResult:
        return CommitResult(
            str(uuid4()),
            commit.idempotency_id,
            commit.candidate.stream_id,
            _IMPLEMENTATION,
            _VERSION,
            status,
            (),
            _BOUNDARY,
            revision,
            conflict,
            commit.expected_revision_id if conflict else None,
            head if conflict else None,
            failure,
        )

    @staticmethod
    def _read_result(
        request: RevisionReadRequest,
        status: RevisionReadStatus,
        *,
        revision: Revision | None = None,
        expected: IdentityObservation = (),
        observed: IdentityObservation = (),
        version: str | None = None,
        failure: StoreOperationalFailure | None = None,
    ) -> RevisionReadResult:
        return RevisionReadResult(
            str(uuid4()),
            request.request_id,
            request.stream_id,
            request.selector,
            _IMPLEMENTATION,
            _VERSION,
            status,
            (),
            _BOUNDARY,
            revision=revision,
            expectations_matched=True
            if revision and request.has_reconciliation_expectations
            else None,
            requested_revision_id=request.revision_id
            if status in (RevisionReadStatus.ABSENT, RevisionReadStatus.MISMATCH)
            else None,
            absence_observation="Consistent read established no requested address."
            if status is RevisionReadStatus.ABSENT
            else None,
            expected_identities=expected,
            observed_identities=observed,
            mismatched_fields=tuple(name for name, _ in observed)
            if status is RevisionReadStatus.MISMATCH
            else (),
            unsupported_version_ids=(version,) if version else (),
            compatibility_finding="Unsupported private store or envelope version."
            if version
            else None,
            integrity_findings=("Generic revision integrity failed.",)
            if status is RevisionReadStatus.CORRUPT
            else (),
            failure=failure,
        )

    def _read_observation(
        self, request: RevisionReadRequest, envelope: _Envelope | None
    ) -> RevisionReadResult:
        if envelope is None:
            return self._read_result(request, RevisionReadStatus.ABSENT)
        if request.has_reconciliation_expectations:
            expected: IdentityObservation = (
                ("content_id", request.expected_content_id),
                ("idempotency_id", request.expected_idempotency_id),
                ("predecessor_revision_id", request.expected_predecessor_revision_id),
                ("schema_id", request.expected_schema_id),
            )
            actual: IdentityObservation = (
                ("content_id", envelope.revision.content_id),
                ("idempotency_id", envelope.idempotency_id),
                ("predecessor_revision_id", envelope.revision.predecessor_revision_id),
                ("schema_id", envelope.revision.schema_id),
            )
            conflicting = tuple(
                value
                for value, expectation in zip(actual, expected, strict=True)
                if value != expectation
            )
            if conflicting:
                return self._read_result(
                    request,
                    RevisionReadStatus.MISMATCH,
                    expected=expected,
                    observed=conflicting,
                )
        return self._read_result(
            request, RevisionReadStatus.FOUND, revision=envelope.revision
        )

    @staticmethod
    def _native_fault(error: sqlite3.Error | OSError, phase: str) -> _StorageFault:
        code = (
            error.sqlite_errorcode & 255
            if isinstance(error, sqlite3.Error) and hasattr(error, "sqlite_errorcode")
            else None
        )
        if code in (sqlite3.SQLITE_CORRUPT, sqlite3.SQLITE_NOTADB):
            return _StorageFault("integrity_failure")
        if code in (sqlite3.SQLITE_BUSY, sqlite3.SQLITE_LOCKED):
            return _StorageFault("busy")
        return _StorageFault(
            "open_failed" if phase.endswith("open") else "sqlite_failure"
        )

    @staticmethod
    def _failure(phase: str, code: str) -> StoreOperationalFailure:
        return StoreOperationalFailure(
            str(uuid4()),
            phase,
            _IMPLEMENTATION,
            code,
            "Complete acknowledged operation",
            "Operation boundary failed",
            code,
            None,
            "No presence, absence, or retry permission inferred.",
        )

    def _read_fault(
        self, request: RevisionReadRequest, phase: str, fault: _StorageFault
    ) -> RevisionReadResult:
        if fault.code == "unsupported_version":
            return self._read_result(
                request, RevisionReadStatus.INCOMPATIBLE, version=fault.version
            )
        if fault.code == "integrity_failure":
            return self._read_result(
                request, RevisionReadStatus.CORRUPT, observed=fault.observed
            )
        interrupted = phase == "read.observe" and fault.code != "payload_limit"
        return self._read_result(
            request,
            RevisionReadStatus.INDETERMINATE
            if interrupted
            else RevisionReadStatus.ERROR,
            failure=self._failure(
                phase, "read_interrupted" if interrupted else fault.code
            ),
        )

    def _commit_fault(
        self, commit: Commit, phase: str, fault: _StorageFault
    ) -> CommitResult:
        uncertain = phase == "commit.acknowledge"
        return self._commit_result(
            commit,
            CommitStatus.INDETERMINATE if uncertain else CommitStatus.ERROR,
            failure=self._failure(
                phase, "commit_unacknowledged" if uncertain else fault.code
            ),
        )
