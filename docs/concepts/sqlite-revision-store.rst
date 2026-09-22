Local SQLite revision storage
=============================

``SQLiteAtomicRevisionStore`` implements the opaque single-stream contract through
Python's standard-library ``sqlite3``. This is provisional software functionality,
not domain validation, scientific validation, or human acceptance. Harness and
Workflow repositories still own their payloads, schema interpretation and validity.

Construction and effects
------------------------

Use the supported public import:

.. code-block:: python

   from pathlib import Path
   from ksdft2effmass.persistence import SQLiteAtomicRevisionStore

   store = SQLiteAtomicRevisionStore(
       Path('/explicit/local/revisions.sqlite3'),
       busy_timeout_ms=1000,
       max_payload_bytes=1048576,
   )

Construction retains immutable configuration and performs no I/O. The path must be
an absolute concrete ``pathlib.Path``. It selects a filesystem file, not a SQLite
URI or in-memory database. Parent directories must already exist. Each operation
opens and closes its own connection; there is no cached current stream or revision.
The first operation, including a read, privately initializes a genuinely empty
SQLite database within a transaction. A concurrent first caller rechecks emptiness
under the writer lock. Existing unrelated, malformed or unsupported stores are
refused rather than initialized over or migrated. The existing generated Harness
control database is not an input to this store.

``busy_timeout_ms`` accepts built-in integers from 0 to 2,147,483,647 milliseconds.
``max_payload_bytes`` accepts built-in integers from 1 to 2,147,483,647 bytes.
Booleans, numeric strings, floats and NumPy scalar integers are rejected with
``TypeError``. Out-of-range integers and relative paths raise ``ValueError``.
SQLite's native limits may be smaller; failures are represented, never truncation.
Oversized payloads are refused on writes and reads without returning partial data.
Native filename rejection, including a NUL-containing absolute Path, is represented
as ``open_failed`` rather than leaking the driver's exception.

Atomicity and identity
----------------------

A write uses ``BEGIN IMMEDIATE`` with DELETE rollback journaling, FULL
synchronization, foreign keys, and the configured bounded busy timeout. It inserts
one complete revision and advances its stream head in the same transaction. Before
COMMIT it rechecks the exact candidate and unchanged prior stream history.
The private schema owns no triggers: any trigger definition is refused during
recognition, before revision insertion, head updates or idempotency replay. This
prevents admitted executable schema from altering other streams or format metadata;
refusal does not repair or remove the trigger. CAS compares the current head with the exact expected predecessor; ``None`` means an
absent stream. No backoff loop, automatic retry, cross-stream commit or external
process effect is performed.

Revision addresses are pairs of stream and revision identity. An idempotency key
is unique within one physical database and binds every field of the complete
``Commit``, including payload bytes and stream. Exact replay is checked before
CAS and returns the original revision even after the head advances. A changed
binding produces ``idempotency_collision``; an existing address under another key
produces ``revision_collision``; otherwise a stale head produces
``compare_and_swap``. Caller content labels do not substitute for byte equality.
Separate databases have independent idempotency namespaces. Application composition
must retain separate physical development and scientific stores; sharing an
implementation is not authorization to co-locate them.

Reads use one consistent transaction for format recognition, stream closure,
selection and reconciliation. Explicit historical reads do not silently select
latest. Native stream/revision address types are checked across both tables so
malformed TEXT or empty addresses cannot hide rows from BLOB lookups and fabricate
absence. The relevant complete stream history is checked for native value types,
integrity digests, a valid head, same-stream predecessors and acyclic closure.
Missing heads with surviving revisions and dangling heads/predecessors are corrupt,
not absent. This implementation holds complete relevant history and payloads in
memory; the payload cap is not an aggregate-memory or database-size cap.

Private compatibility and integrity
-----------------------------------

The implementation identity is
``ksdft2effmass.persistence.SQLiteAtomicRevisionStore`` and its version identity is
``1``. The private format uses metadata, immutable revision rows and stream heads.
Store/envelope version 1 is supported; unknown versions are not guessed from a
caller's ``schema_id``. There is no earlier SQLite format to migrate and no public
initializer or migrator API. Domain wire schemas remain domain-owned.

Identities are exact BLOB-encoded UTF-8 with ``surrogatepass``, preserving NUL,
non-ASCII and unpaired surrogates without normalization. SQL NULL distinguishes an
absent predecessor from all present values; empty payload bytes remain valid BLOBs.
Envelope-v1 SHA-256 framing is documented on the private row serializer and in the
independently authored SQL fixture. It binds stream, revision, predecessor,
schema, content, payload and idempotency through length-delimited fields and a
predecessor-presence tag. This checksum detects represented corruption; it is not
caller content identity, domain canonicalization, a signature or authentication
against coordinated rewriting of both bytes and digest.

Closed outcomes and reconciliation
----------------------------------

Only a ``found`` read contains a complete revision. Without supplied expectations,
``expectations_matched`` is ``None``; a matching complete expectation group sets it
to ``True``. Mismatch contains the complete sorted expected identity set and only
the conflicting observed fields, without a payload. Observation result IDs are
fresh UUIDs, not substitutes for request, stream, revision or idempotency identity.

Operational diagnostics use fixed sanitized codes, not raw SQLite SQL, paths or
payloads. Important codes include ``busy``, ``open_failed``, ``payload_limit``,
``unsupported_version``, ``integrity_failure``, ``sqlite_failure``,
``read_interrupted`` and ``commit_unacknowledged``. Failure phase distinguishes setup
from observation. Retryability is unknown (``None``); no failure supplies retry
permission. Unsupported formats/envelopes produce read ``incompatible`` or commit
``error``; failed integrity produces read ``corrupt`` or commit ``error``.
A corrupt read retains sorted, independently readable stored ``revision_id`` and
``content_id`` labels from the faulting row, or the readable head reference when
its revision is missing. Closure failures identify the referring, revisited or
unreachable revision; a missing head identifies the first surviving revision in
stored-address order. Unreadable fields are omitted, never replaced with request
identities. Metadata/schema failures have no inferred revision observations. These
labels assert neither integrity nor reconciliation success and carry no payload
or mismatch fields. Only the first detected fault is reported, not a full audit.

Known precommit operational failure is ``error``, not a conflict. Failed read
observation is ``indeterminate`` when presence or integrity cannot be established;
open/setup failures remain ``error``. An exception after attempting SQL COMMIT but
before acknowledgement is ``indeterminate``, even if cleanup succeeds. A confirmed
commit survives connection-close trouble as established evidence with an additional
sanitized diagnostic, not an invented rollback.

After uncertain acknowledgement, submit an explicit ``RevisionReadRequest`` for
the original stream/revision with **all** predecessor, schema, content and
idempotency expectation slots. Matching ``found`` establishes that exact commit;
consistent ``absent`` permits byte-identical resubmission. Mismatch, incompatible,
corrupt, indeterminate or error preserves conflict or uncertainty and never grants
changed-identity retry. The store performs no retry itself.

Verification and limits
-----------------------

Class-owned software tests cover independent SQL compatibility literals, exact
replay and identity partitions, concurrent initialization/CAS, real lock contention,
trigger refusal (including cross-stream deletion and metadata mutation), native
head-write denial after an observed real revision insertion, installed-Python
fixture termination before/after COMMIT, lost-acknowledgement reconciliation and
malformed histories with independently valid cycle digests. Corrupt-read cases
check exact readable identity observations, including partially unreadable rows. These are synthetic local software tests, not electronic
structure execution, scientific evidence, or hardware power-loss tests.

No network-filesystem guarantee, backup/recovery procedure, retention/compaction
policy, throughput bound, unlimited complete-aggregate size or cross-database
transaction is established. See :doc:`../api/persistence` for the public records
and methods. Independent antagonistic implementation review remains a separate
operation gate and does not constitute human acceptance.
