# `AbstractWorkflow`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Responsibility

`AbstractWorkflow` is the independent nominal ABC for a reusable definition-only
Workflow owner. It is not an `AbstractTask` and has no execution method.

Concrete subclasses provide stable `identity: WorkflowIdentity` and immutable
`composition: WorkflowComposition`. The ABC provides a final generic
`definition: WorkflowDefinition` property and rejects overriding that construction.
Concrete Workflows therefore do not create per-Workflow definition classes or schemas.

## Boundary

The owner may organize domain-specific constants needed to construct its immutable
composition, but it does not retain a WorkflowRun, runtime Task adapter, effect port,
activation, result, repository, or mutable execution state. `WorkflowExecutionPlan`
retains the resulting `WorkflowDefinition`, not this live owner.

Workflow definitions own composition and gate policy. Member Tasks own scientific
operations. Nested execution targets a child `WorkflowDefinition` and creates a
distinct child run.

## Related architecture

- [Schematic](schematic.md)
- [`WorkflowDefinition`](../WorkflowDefinition/index.md)
- [`WorkflowExecutionPlan`](../WorkflowExecutionPlan/index.md)
- [`NestedWorkflowTask`](../NestedWorkflowTask/index.md)
