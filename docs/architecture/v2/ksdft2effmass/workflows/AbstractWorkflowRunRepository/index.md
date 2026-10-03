# `AbstractWorkflowRunRepository`

## Status

**Accepted nominal-ABC migration contract; implementation pending.**

## Responsibility

`AbstractWorkflowRunRepository(ABC)` is the Workflow-owned nominal repository port. It
declares abstract `load`, `commit`, and `load_claim` operations with the existing
closed Workflow persistence results. Repository observations never grant Workflow
advancement or external-effect authority.

`WorkflowRunAtomicRepository` inherits explicitly and composes one
`AbstractAtomicRevisionStore`, exact serializer, and exact validator. Structural
lookalikes, repository discovery, database selection, and compatibility aliases are
prohibited.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractAtomicRevisionStore`](../../persistence/AbstractAtomicRevisionStore/index.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
