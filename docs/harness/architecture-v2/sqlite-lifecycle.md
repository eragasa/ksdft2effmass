# Architecture v2 SQLite lifecycle

> **Proposed architecture; inactive; not implemented; not accepted.**

This proposal does not change current SQLite behavior, paths, schemas, or
commands. It specifies the target lifecycle needed to distinguish temporary
mutable construction from an immutable maintained projection.

## Proposed lifecycle

```text
authoritative sources
→ temporary mutable candidate database
→ validation
→ close all connections
→ checkpoint or remove transactional state
→ publish immutable SQLite projection
```

The candidate database would exist outside the maintained destination. Database
construction and validation could use write-capable connections only within the
temporary workspace. Publication would operate on closed bytes after
transactional state is checkpointed into the main database or removed.

## Eventual invariants

A later implementation should establish all of these together:

1. The maintained SQLite file is not live authority.
2. No maintained command opens the maintained projection with a write-capable
   connection.
3. Candidate construction occurs outside the maintained path.
4. Publication begins only after every candidate connection is closed.
5. Verification uses read-only immutable access or closed-byte/semantic
   comparison.
6. WAL, SHM, journal, staging, and backup files are never tracked.
7. Runtime concurrent queries, if needed, use a disposable untracked copy.
8. Deleting sidecars after execution is not treated as the architectural fix.

Sidecar cleanup alone is insufficient because it leaves ambiguous whether the
maintained file was ever a live mutable store, whether bytes include all
committed transactions, and whether a verifier can create new state beside the
tracked artifact.

## Candidate construction

The proposed SQLite projector would:

- create a new database under a caller-owned temporary root;
- apply schema and normalized state deterministically;
- use explicit transaction boundaries;
- run integrity and foreign-key checks;
- close cursors and connections in all success and failure paths;
- checkpoint WAL content when WAL mode is deliberately used, then return to a
  closed single-file representation; and
- expose only the closed candidate artifact to `HarnessArtifactSet`.

The proposal does not require WAL mode. If a simpler journal mode produces the
needed deterministic closed artifact, it may be preferred. Exact mode remains
an implementation decision supported by tests, not an architecture preference.

## Publication and rollback

`HarnessSynchronizer` would stage all generated artifacts, verify their complete
identities, and replace maintained destinations as one bounded publication
operation with a documented rollback boundary. SQLite publication would be no
special source of authority; it would be one artifact in the complete set.

Process-level replacement cannot promise filesystem-wide atomicity across power
loss. A later slice must state the supported guarantee precisely and test
partial-replacement recovery. Staging and backup artifacts would be temporary,
untracked, confined, and removed after success or retained only long enough for
in-process rollback.

## Verification

`HarnessStateComparator` would never publish. It would open the maintained
SQLite artifact with immutable read-only access when logical comparison is
needed, or compare closed candidate bytes when a canonical-byte contract is
explicitly established. Raw SQLite byte inequality alone would not imply
semantic drift unless canonical bytes become an accepted contract.

A verifier would neither discover nor delete arbitrary repository sidecars. The
architecture prevents their creation at the maintained path instead.

## Runtime query copies

If future concurrent query workloads require SQLite runtime features, the
operator would copy the immutable maintained projection to a disposable,
untracked runtime location. WAL, SHM, and journals would belong only to that
runtime copy and would carry no authority back into the repository.
