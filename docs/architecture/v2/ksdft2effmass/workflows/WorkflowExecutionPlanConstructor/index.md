# `WorkflowExecutionPlanConstructor`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Responsibility

`WorkflowExecutionPlanConstructor` is the cohesive ActionObject for compiling one
purely declarative `WorkflowExecutionPlan`. It consumes:

- one exact `WorkflowDefinition`;
- one ordered tuple of `TaskDefinition` values; and
- one ordered tuple of `NestedWorkflowTarget` values.

It validates complete composition closure, exact definition identity and order,
execution-kind types, and exact nested-target applicability. It returns one immutable
plan or raises the documented `TypeError`/`ValueError` for malformed supplied values.

## Exclusions

The constructor accepts no live Task, Workflow owner, dispatch effect, repository,
WorkflowRun, or registry. It performs no discovery, execution, authority decision,
child-run creation, persistence, or scientific interpretation.

Cross-object compilation belongs here rather than in module-level validators or
individual domain Tasks. Intrinsic field invariants remain on their DataObjects.

## Related architecture

- [Schematic](schematic.md)
- [`WorkflowExecutionPlan`](../WorkflowExecutionPlan/index.md)
- [`WorkflowExecutionBindingsConstructor`](../WorkflowExecutionBindingsConstructor/index.md)
