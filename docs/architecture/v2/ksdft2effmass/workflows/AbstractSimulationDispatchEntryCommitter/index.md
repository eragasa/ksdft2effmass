# `AbstractSimulationDispatchEntryCommitter`

## Status

**Implemented nominal-ABC contract; local software-verification evidence passes.**

## Responsibility

`AbstractSimulationDispatchEntryCommitter(ABC)` is the nominal persistence port used by
simulation dispatch to commit one exact dispatch-entry transition. Its abstract method
retains the current closed request and `SimulationDispatchEntryResult` contract.

`WorkflowRunDispatchEntryCommitter` inherits explicitly. The ABC neither selects a
repository nor grants execution authority; it records the already prepared transition
through its concrete owner. Structural lookalikes and aliases are rejected.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractSimulationDispatchEffect`](../AbstractSimulationDispatchEffect/index.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
