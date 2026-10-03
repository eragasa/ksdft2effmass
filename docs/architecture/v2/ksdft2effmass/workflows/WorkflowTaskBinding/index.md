# `WorkflowTaskBinding`

## Status

**Implemented runtime contract; local software-verification evidence passes.**

## Classification

`WorkflowTaskBinding` is one concrete frozen, slotted, non-subclassed process-local
DataObject containing:

- one `TaskInstanceIdentity`;
- one explicit concrete `AbstractTask`; and
- zero or one `AbstractSimulationDispatchEffect`.

It deliberately contains live runtime owners and therefore does not belong inside the
declarative `WorkflowExecutionPlan`.

## Route variants

The immutable Task definition determines the closed field shape:

- `IN_PROCESS`: the Task is an `AbstractInProcessScientificTask` and the effect is
  absent;
- `SIMULATION`: the Task is an `AbstractSimulationTask` and exactly one nominal
  `AbstractSimulationDispatchEffect` is present; and
- `NESTED_WORKFLOW`: the Task is a `NestedWorkflowTask` and the effect is absent.

The record rejects incompatible route overlap. Construction performs no effect and
creates no authority or child run.

`WorkflowExecutionBindingsConstructor` correlates each binding against one exact plan,
checks complete composition order, exact definition equality, and nested target
agreement, and produces `WorkflowExecutionBindings`.

## Immutability meaning

The record freezes the association, not hidden state inside a runtime adapter or its
ports. Runtime objects remain process-local and are excluded from declarative plan
equality and persistence.

## Related architecture

- [Schematic](schematic.md)
- [`WorkflowExecutionBindings`](../WorkflowExecutionBindings/index.md)
- [`AbstractSimulationDispatchEffect`](../AbstractSimulationDispatchEffect/index.md)
- [`WorkflowExecutionPlan`](../WorkflowExecutionPlan/index.md)
