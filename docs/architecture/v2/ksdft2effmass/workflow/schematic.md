# Scientific Workflow schematic

## Type relationships

```mermaid
classDiagram
    class AbstractTask {
        <<ABC>>
        +identity TaskDefinitionIdentity*
        +execute(inputs, context) ResultObject[]*
    }
    class AbstractWorkflow {
        <<ABC>>
        +workflow_identity WorkflowIdentity*
        +composition WorkflowComposition*
    }
    class NestedWorkflowTask {
        <<ABC>>
        +workflow AbstractWorkflow*
    }

    NestedWorkflowTask --|> AbstractTask
    NestedWorkflowTask --> AbstractWorkflow : targets child definition
```

There is deliberately no inheritance edge from `AbstractWorkflow` to `AbstractTask`.
The package exposes no structural `Task` or `Workflow` protocols and no compatibility
aliases for them.

## Ordinary Task activation

```mermaid
flowchart LR
    workflow[AbstractWorkflow definition] --> composition[WorkflowComposition]
    composition --> instance[TaskInstance]
    result[Already-bound ResultObjects] --> control[Workflow control]
    instance --> control
    gates[Start-gate policy] --> control
    control --> activation[TaskActivation]
    activation --> task[Concrete AbstractTask]
    task --> returned[Returned ResultObjects]
    returned --> outcome[TaskInvocationOutcome]
    outcome --> run[WorkflowRun successor]
```

The Task receives the exact context supplied by Workflow control. It does not discover
its instance, activation, operation, attempt, or authority.

## Nested Workflow activation

```mermaid
flowchart LR
    parent[Parent WorkflowRun] --> adapter[NestedWorkflowTask]
    child_definition[Child AbstractWorkflow] --> adapter
    adapter --> intent[Nested invocation intent]
    intent --> child[Distinct child WorkflowRun]
    child --> terminal[Terminal observation]
    terminal --> export{Confirmed?}
    export -->|yes| results[Explicit exported ResultObjects]
    export -->|no| none[No exported results]
    results --> parent_successor[Parent WorkflowRun successor]
```

A nested adapter does not execute child member Tasks with the parent Task context.
Child creation and parent advancement remain separate identity-correlated commits.
Only a confirmed replay-equal terminal child revision may export explicit results.

## Periodic-1D replay decomposition

```mermaid
flowchart LR
    input[Imported retained inputs] --> adapt[Input adaptation Task]
    adapt --> parent[Parent-model Task]
    parent --> fibers[Parent-fiber sampling Task]
    fibers --> frame[Band-frame transport Task]
    frame --> retained[Retained-space/operator Task]
    retained --> projection[Retained-operator projection Task]
    projection --> hopping[Complete hopping transform Task]
    hopping --> truncate[Range truncation Tasks]
    hopping --> fit[Range fitting Tasks]
    truncate --> compare[Historical comparison Task]
    fit --> compare
    compare --> prepare{Confirmed agreement?}
    prepare -->|yes| artifacts[Artifact preparation Task]
    prepare -->|no| rejected[No prepared artifact output]
```

The root replay Workflow owns this composition but performs none of the represented
scientific operations itself.
