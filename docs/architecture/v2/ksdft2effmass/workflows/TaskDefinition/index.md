# `TaskDefinition`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Classification

`TaskDefinition` is one concrete frozen, slotted, non-subclassed DataObject owned by
`ksdft2effmass.workflows`:

```python
@final
@dataclass(frozen=True, slots=True)
class TaskDefinition:
    identity: TaskDefinitionIdentity
    execution_kind: TaskExecutionKind
```

It identifies a reusable operation definition and its engine route. It contains no
run-scoped instance identity, scientific inputs, mutable adapter, effect port, child
run, result, authority, retry policy, or wire schema.

## Construction

Concrete Tasks do not construct operation-specific definition classes. `AbstractTask`
provides a final `definition` property that creates this generic value from:

- the concrete Task's stable `TaskDefinitionIdentity`; and
- the fixed execution kind supplied by its one route-root ABC.

The Task cannot override generic definition construction or independently select a
kind. Wrong exact field types raise `TypeError`.

## Use

`WorkflowExecutionPlan` snapshots `TaskDefinition` values in composition order.
`WorkflowExecutionBindingsConstructor` verifies every runtime adapter against the
snapshot. Engines route from the snapshot and do not reread route state from an
adapter.

`TaskDefinition` is architecture control data, not a scientific-model definition and
not proof that the operation ran.

## Related architecture

- [Schematic](schematic.md)
- [`TaskExecutionKind`](../TaskExecutionKind/index.md)
- [`AbstractTask`](../AbstractTask/index.md)
- [`WorkflowExecutionPlan`](../WorkflowExecutionPlan/index.md)
