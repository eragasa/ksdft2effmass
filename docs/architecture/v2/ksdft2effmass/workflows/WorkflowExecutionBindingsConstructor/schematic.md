# `WorkflowExecutionBindingsConstructor` schematic

```mermaid
flowchart LR
    plan[WorkflowExecutionPlan] --> constructor[WorkflowExecutionBindingsConstructor]
    bindings[Ordered WorkflowTaskBindings] --> constructor
    constructor --> checks{Complete route-compatible closure?}
    checks -->|yes| runtime[WorkflowExecutionBindings]
    checks -->|no| reject[No runtime bindings]
```

The constructor validates runtime references against immutable plan snapshots. It does
not add those references to the plan.
