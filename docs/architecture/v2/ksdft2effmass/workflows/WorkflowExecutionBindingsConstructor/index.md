# `WorkflowExecutionBindingsConstructor`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Responsibility

`WorkflowExecutionBindingsConstructor` is the cohesive ActionObject for binding one
compiled declarative plan to one complete process-local adapter set. It consumes one
exact `WorkflowExecutionPlan` and one ordered tuple of `WorkflowTaskBinding` values.

It verifies:

- exact Task-instance membership and composition order;
- exact equality with each planned `TaskDefinition`;
- nominal route membership without incompatible overlap;
- required absence or presence of `AbstractSimulationDispatchEffect`;
- exact nested child-definition agreement; and
- complete closure with no missing, additional, duplicate, or reordered binding.

It returns `WorkflowExecutionBindings`. It does not execute an adapter or create
execution authority.

## Exclusions

The constructor performs no discovery, module search, entry-point loading, mutable
registration, persistence, activation selection, result construction, or scientific
interpretation. Runtime binding policy is centralized here rather than repeated in the
engine.

## Related architecture

- [Schematic](schematic.md)
- [`WorkflowExecutionBindings`](../WorkflowExecutionBindings/index.md)
- [`WorkflowExecutionPlanConstructor`](../WorkflowExecutionPlanConstructor/index.md)
- [`WorkflowEngine`](../WorkflowEngine/index.md)
