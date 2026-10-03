# `AbstractScientificTask`

## Status

**Accepted architectural contract; implementation pending.**

## Responsibility

`AbstractScientificTask(AbstractTask)` is a nominal grouping ABC for scientific
operations. It adds no execution method, route kind, scheduler, result container,
authority, or scientific policy.

Its two route descendants are:

- `AbstractInProcessScientificTask` for ordinary in-process execution; and
- `AbstractSimulationTask` for operations whose effects remain behind the
  authority-bearing simulation dispatch boundary.

A concrete class cannot inherit `AbstractScientificTask` alone: without exactly one
route root it remains ineligible for `WorkflowExecutionBindings`. The grouping exists
so architecture, typing, and review can distinguish scientific operations from
engine-control `NestedWorkflowTask` nodes without forcing both scientific routes to
share an unsafe execution method.

Scientific meaning remains with the concrete Task and its domain-owned inputs and
`AbstractResultObject` values. Membership is not evidence that a calculation ran or was accepted.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractTask`](../AbstractTask/index.md)
- [`AbstractInProcessScientificTask`](../AbstractInProcessScientificTask/index.md)
- [`AbstractSimulationTask`](../AbstractSimulationTask/index.md)
