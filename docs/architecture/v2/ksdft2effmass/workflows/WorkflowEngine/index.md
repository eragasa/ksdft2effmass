# `WorkflowEngine`

## Status

**Accepted migration contract for the coordinated implementation run.**

## Responsibility

`WorkflowEngine` is a stateless ActionObject for invoking one exact ordinary
in-process activation from correlated declarative and runtime inputs:

```python
execute_in_process(
    bindings: WorkflowExecutionBindings,
    activation: TaskActivation,
) -> TaskExecutionResults
```

`WorkflowExecutionBindings` contains its exact `WorkflowExecutionPlan`. The engine
correlates Workflow and Task-instance identities, obtains the immutable planned
`TaskDefinition`, requires `IN_PROCESS`, derives `TaskExecutionContext`, invokes the
bound `AbstractInProcessScientificTask`, and requires exact `TaskExecutionResults`.

## Specialized routes

The coordinated migration does not make this method a universal dispatcher:

- `SIMULATION` fails closed and remains owned by the existing authority, reservation,
  claim, `AbstractSimulationDispatchEffect`, reconciliation, and ingress control
  plane; and
- `NESTED_WORKFLOW` fails closed and remains owned by distinct child-run control.

Future facade methods may compose those established ActionObjects only through a
separate accepted contract. The engine never invokes a simulation effect with
`TaskExecutionContext` and never executes child members with a parent context.

## Exclusions

The engine performs no adapter discovery, registry lookup, plan compilation, runtime
binding construction, persistence, durable-outcome construction, exception
translation, or scientific interpretation. Plan and binding constructors establish
closure before invocation.

## Related architecture

- [Schematic](schematic.md)
- [`WorkflowExecutionBindings`](../WorkflowExecutionBindings/index.md)
- [`AbstractInProcessScientificTask`](../AbstractInProcessScientificTask/index.md)
- [`TaskExecutionResults`](../TaskExecutionResults/index.md)
