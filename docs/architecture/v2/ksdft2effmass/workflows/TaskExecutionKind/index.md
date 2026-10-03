# `TaskExecutionKind`

## Status

**Accepted architectural contract; implementation pending.**

## Contract

`TaskExecutionKind` is one closed Workflow-owned `StrEnum` with exactly three values:

- `IN_PROCESS = "in_process"`;
- `SIMULATION = "simulation"`; and
- `NESTED_WORKFLOW = "nested_workflow"`.

It identifies an engine route, not scientific meaning, execution authority, result
status, persistence state, or validation status. New concrete Tasks reuse these values;
they do not add operation-specific kinds.

A concrete Task never selects this value directly. Each route-root ABC supplies one
fixed kind, and `AbstractTask` uses that value when it constructs the generic
`TaskDefinition`. Runtime subclass enforcement rejects conflicting route roots or an
override of the route kind. Plan compilation repeats the agreement check.

Adding a fourth value is a public architecture change requiring a new cohesive engine
route, authority analysis, result integration, tests, and documentation. It is not a
convenience extension point.

## Schema economy

The enum is shared by every Task. There are no calculator-, campaign-, or
operation-specific execution-kind enums and no per-Task route schemas.

## Related architecture

- [Schematic](schematic.md)
- [`TaskDefinition`](../TaskDefinition/index.md)
- [`AbstractTask`](../AbstractTask/index.md)
- [Unclosed-route defect](../defects/defect00002-unclosed_task_execution_routes.md)
