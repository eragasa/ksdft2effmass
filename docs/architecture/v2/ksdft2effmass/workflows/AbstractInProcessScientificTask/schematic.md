# `AbstractInProcessScientificTask` schematic

```mermaid
flowchart LR
    activation[Exact TaskActivation] --> engine[WorkflowEngine]
    plan[WorkflowExecutionPlan] --> engine
    bindings[WorkflowExecutionBindings] --> engine
    engine --> context[TaskExecutionContext]
    context --> task[AbstractInProcessScientificTask.execute]
    inputs[Already-bound ResultObjects] --> task
    task --> results[TaskExecutionResults]
    results --> control[Durable outcome control]
```

The engine reaches this method only when the plan snapshot, runtime binding, and fixed
`in_process` route agree. Neither the activation nor context grants external execution
authority.
