# V2-ISSUE-012: Projection publication rollback guarantee

**Severity:** High

**Scope:** Harness projection synchronization

## Conflict

The compiler architecture promises atomic publication, rollback restoration, and reader visibility of only complete old or new sets. Publication and persistence admit rollback or recovery failure, while supported-filesystem guarantees remain unresolved.

## Affected contracts

- `harness/compiler-architecture.md` — *Synchronization*, *Concurrency and consistency*, *Failure model*, and unresolved rollback guarantees
- `harness/persistence.md` — interrupted-write recovery

## Required resolution

Select and specify a supported publication strategy and its portability boundary. If complete multi-file atomic replacement cannot be guaranteed, use versioned destinations, atomic pointer switching, recovery markers, quarantine, or another explicit strategy and weaken unsupported guarantees.

## Acceptance condition

Reader-visible consistency and recovery claims are achievable on every supported filesystem, including interruption and rollback-failure cases.
