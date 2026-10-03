# `WorkflowExecutionBindings`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Classification

`WorkflowExecutionBindings` is one concrete frozen, slotted, non-subclassed
process-local DataObject containing:

- one exact `WorkflowExecutionPlan`; and
- one ordered `WorkflowTaskBinding` for every planned Task instance.

It is the explicit runtime companion to the declarative plan. It is not a registry,
plugin catalog, durable run record, or discovery mechanism.

## Invariants

Bindings match plan composition membership and order exactly. Every binding's Task
identity and generic definition equal the corresponding immutable plan snapshot. The
route-specific binding shape is valid, and each nested Task's child definition equals
the applicable `NestedWorkflowTarget`.

No missing, additional, duplicate, reordered, structurally supplied, or
route-incompatible adapter is accepted. `WorkflowExecutionBindingsConstructor` owns
these cross-object checks.

## Lifetime and persistence

The bindings object freezes association for one process-local execution environment.
It may reference effect ports and other runtime dependencies, so it is excluded from
plan hashing, declarative persistence, and scientific provenance. Durable Workflow
records retain exact executor and effect evidence through their existing records.

The engine receives this exact correlated bindings object explicitly and reads its
contained plan. It performs no separate plan correlation and no adapter lookup.

## Related architecture

- [Schematic](schematic.md)
- [`WorkflowExecutionPlan`](../WorkflowExecutionPlan/index.md)
- [`WorkflowTaskBinding`](../WorkflowTaskBinding/index.md)
- [`WorkflowExecutionBindingsConstructor`](../WorkflowExecutionBindingsConstructor/index.md)
