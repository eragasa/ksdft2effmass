# `NestedWorkflowTarget`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Contract

`NestedWorkflowTarget` is one concrete frozen, slotted, non-subclassed DataObject that
correlates:

- one `TaskInstanceIdentity`; and
- one immutable child `WorkflowDefinition`.

It supplies the declarative child target required by a nested Task without retaining a
live `NestedWorkflowTask` adapter in `WorkflowExecutionPlan`.

`WorkflowExecutionPlanConstructor` requires exactly one target for every nested Task
definition, no target for other execution kinds, unique Task-instance identities, and
membership in the owning Workflow composition. A target creates no child run and
exports no result.

All nested Tasks reuse this class. Child domain variation remains in the contained
`WorkflowDefinition`, not in target subclasses or schemas.

## Related architecture

- [Schematic](schematic.md)
- [`NestedWorkflowTask`](../NestedWorkflowTask/index.md)
- [`WorkflowExecutionPlan`](../WorkflowExecutionPlan/index.md)
