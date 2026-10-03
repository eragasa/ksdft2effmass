# `WorkflowExecutionPlan`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Classification

`WorkflowExecutionPlan` is one concrete frozen, slotted, non-subclassed declarative
DataObject. It contains:

- one immutable `WorkflowDefinition`;
- one ordered `TaskDefinition` for every composition `TaskInstance`; and
- one immutable `NestedWorkflowTarget` for every nested-Workflow Task.

It contains no live Workflow owner, Task adapter, dispatch effect, repository,
WorkflowRun, activation, result, authority, or process-local execution state.

## Invariants

Task definitions match composition membership and order exactly. Their identities equal
the corresponding `TaskInstance.definition_identity` values. There are no missing,
additional, duplicate, or reordered definitions.

Nested targets exist exactly for definitions whose execution kind is
`NESTED_WORKFLOW`; each target names the corresponding Task instance and immutable
child `WorkflowDefinition`. Non-nested Tasks have no target.

`WorkflowExecutionPlanConstructor` owns these cross-object checks. The resulting plan
is safe to compare and reason about independently of runtime adapter identity.

## Boundary

The plan is explicit declarative input, not a registry or executable aggregate.
`WorkflowExecutionBindings` supplies process-local adapters and effects and contains
this exact plan. The engine receives the validated bindings object as its single
composite execution argument, reads its already-correlated plan, and performs no
separate plan lookup or correlation.

No plan construction executes a Task, creates authority, opens a child run, persists
state, or establishes scientific validity.

## Related architecture

- [Schematic](schematic.md)
- [`WorkflowDefinition`](../WorkflowDefinition/index.md)
- [`NestedWorkflowTarget`](../NestedWorkflowTarget/index.md)
- [`WorkflowExecutionBindings`](../WorkflowExecutionBindings/index.md)
- [Plan/runtime conflation defect](../defects/defect00003-plan_runtime_binding_conflation.md)
