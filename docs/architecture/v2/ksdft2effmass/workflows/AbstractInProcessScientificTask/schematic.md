# `AbstractInProcessScientificTask` schematic

```mermaid
flowchart LR
    activation[Exact TaskActivation] --> engine[WorkflowEngine]
    plan[WorkflowExecutionPlan] --> bindings[WorkflowExecutionBindings]
    bindings --> engine
    engine --> context[TaskExecutionContext]
    context --> task[AbstractInProcessScientificTask.execute]
    inputs[Already-bound ResultObjects] --> task
    task --> results[TaskExecutionResults]
    results --> control[Durable outcome control]
```

The engine receives only the activation and validated bindings. It reads the plan
contained by those bindings and reaches this method only when the plan snapshot,
runtime binding, and fixed `in_process` route agree. Neither the activation nor context
grants external execution authority.
