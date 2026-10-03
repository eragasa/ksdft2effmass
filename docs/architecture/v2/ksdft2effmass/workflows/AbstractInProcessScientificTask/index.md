# `AbstractInProcessScientificTask`

## Status

**Accepted architectural contract; implementation pending.**

## Responsibility

`AbstractInProcessScientificTask(AbstractScientificTask)` is the sole ordinary
in-process route root. It fixes `TaskExecutionKind.IN_PROCESS` and owns the abstract
public operation:

```python
execute(
    inputs: tuple[TaskInputBinding, ...],
    context: TaskExecutionContext,
) -> TaskExecutionResults
```

The final generic `definition` remains owned by `AbstractTask`. Concrete subclasses
provide stable identity, immutable dependencies, and the cohesive scientific
operation. They return the shared concrete `TaskExecutionResults`; they do not define
operation-specific result containers.

## Boundary

`TaskExecutionContext` supplies exact correlation and no authority. This route is
therefore limited to operations that require no protected external effect. A Task does
not discover inputs, schedule itself, mutate a WorkflowRun, construct a durable
outcome, persist results, or infer scientific acceptance.

The engine requires the exact return type and propagates Task exceptions to the owning
control boundary. Durable confirmation remains a separate Workflow-control operation.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractScientificTask`](../AbstractScientificTask/index.md)
- [`TaskExecutionResults`](../TaskExecutionResults/index.md)
- [`WorkflowEngine`](../WorkflowEngine/index.md)
