# `NestedWorkflowTask`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Responsibility

`NestedWorkflowTask(AbstractTask)` is the controlled child-Workflow route root. It
fixes `TaskExecutionKind.NESTED_WORKFLOW` and exposes one immutable
`child_workflow_definition: WorkflowDefinition`.

It has no scientific `execute` method. The nested control plane creates a distinct
child `WorkflowRun`, observes its terminal state, and reconciles an explicit export.
`WorkflowEngine.execute_in_process` fails closed for this route and creates no child
run. Parent Task context is never reused for child Tasks.

## Invariants

A concrete nested Task has one stable Task identity and one stable child Workflow
definition. Plan compilation snapshots both and rejects self-targeting or inconsistent
child-definition correlation where applicable. Runtime binding does not create a child
run, authority, result, or parent transition.

A confirmed child terminal observation may export explicit admitted ResultObjects as
`TaskExecutionResults`. Rejected, unequal, indeterminate, or incomplete child states
produce no result value and cannot advance the parent as confirmed.

`NestedWorkflowTask` is a nested-control specialization, not a scientific operation
and not a wrapper that executes child members sequentially.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractTask`](../AbstractTask/index.md)
- [`WorkflowDefinition`](../WorkflowDefinition/index.md)
- [`WorkflowEngine`](../WorkflowEngine/index.md)
- [WorkflowRun object model](../workflow-run.md)
