# `NestedWorkflowTask` schematic

```mermaid
flowchart LR
    activation[TaskActivation] --> engine[WorkflowEngine.execute_in_process]
    engine --> closed[NESTED_WORKFLOW fails closed]
    parent[Parent WorkflowRun] --> control[Nested control plane]
    task[NestedWorkflowTask] --> control
    child_definition[WorkflowDefinition] --> task
    control --> intent[Nested invocation intent]
    intent --> child[Distinct child WorkflowRun]
    child --> terminal[Terminal observation]
    terminal --> confirmed{Confirmed and replay-equal?}
    confirmed -->|yes| export[Explicit child ResultObjects]
    export --> results[TaskExecutionResults]
    results --> successor[Parent successor]
    confirmed -->|no| none[No confirmed parent result]
```

Only the nested control plane creates or observes the child run. In-process engine
invocation fails closed before child creation. Child creation and parent advancement
are separate identity-correlated operations, and no child member receives the parent
Task's execution context.
