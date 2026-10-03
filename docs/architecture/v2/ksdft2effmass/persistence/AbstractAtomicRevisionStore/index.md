# `AbstractAtomicRevisionStore`

## Status

**Accepted nominal-ABC migration contract; implementation pending.**

## Responsibility

`AbstractAtomicRevisionStore(ABC)` is the domain-neutral nominal port for one opaque
single-stream revision store. It declares abstract `read(RevisionReadRequest) ->
RevisionReadResult` and `commit(Commit) -> CommitResult` methods. The existing closed
outcomes, compare-and-swap, idempotency, content identity, and indeterminate-result
semantics remain unchanged.

`SQLiteAtomicRevisionStore` inherits explicitly. Matching methods without inheritance,
virtual registration, discovery, and compatibility aliases are rejected.

## Related architecture

- [Schematic](schematic.md)
- [Persistence package](../index.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
