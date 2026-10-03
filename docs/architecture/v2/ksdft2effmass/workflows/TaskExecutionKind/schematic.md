# `TaskExecutionKind` schematic

```mermaid
flowchart TB
    kind{TaskExecutionKind}
    kind -->|in_process| local[AbstractInProcessScientificTask]
    kind -->|simulation| simulation[AbstractSimulationTask and authority-bearing dispatch]
    kind -->|nested_workflow| nested[NestedWorkflowTask and child-run control]
    local --> results[TaskExecutionResults]
    simulation --> ingress[Confirmed result ingress]
    ingress --> results
    nested --> export[Confirmed child export]
    export --> results
```

The route-root ABC supplies the kind. Plan compilation verifies the immutable snapshot,
and the engine switches on that snapshot rather than ordered `isinstance` checks.
