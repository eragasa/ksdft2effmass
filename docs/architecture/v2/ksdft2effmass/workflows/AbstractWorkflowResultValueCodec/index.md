# `AbstractWorkflowResultValueCodec`

## Status

**Accepted nominal-ABC migration contract; implementation pending.**

## Responsibility

`AbstractWorkflowResultValueCodec(ABC)` declares effect-free abstract `encode` and
`decode` operations for complete versioned concrete `AbstractResultObject` values.
Implementations retain their exact supported branches, schema identities, canonical
bytes, incompatibility rules, and closed failures.

The initial nominal implementations are `WorkflowResultValueSerializer`,
`QuantumEspressoResultValueSerializer`, `QuantityOfInterestResultValueSerializer`, and
`ApplicationResultValueSerializer`. There is no registry, discovery, reflection-based
fallback, mutable cache, or compatibility alias.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractResultObject`](../AbstractResultObject/index.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
