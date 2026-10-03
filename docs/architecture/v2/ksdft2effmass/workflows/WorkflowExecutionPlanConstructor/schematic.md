# `WorkflowExecutionPlanConstructor` schematic

```mermaid
flowchart LR
    workflow[WorkflowDefinition] --> constructor[WorkflowExecutionPlanConstructor]
    tasks[Ordered TaskDefinitions] --> constructor
    nested[Ordered NestedWorkflowTargets] --> constructor
    constructor --> checks{Complete declarative closure?}
    checks -->|yes| plan[WorkflowExecutionPlan]
    checks -->|no| reject[No plan]
```

Only frozen declarative values cross this boundary. Runtime adapter closure belongs to
the separate bindings constructor.
