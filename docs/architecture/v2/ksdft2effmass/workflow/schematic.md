# Scientific Workflow schematic

## Status

**Nominal-ABC implementation is locally software-verified; independent implementation review found no blocking findings.**

These diagrams represent the accepted Workflow class contracts, not current source
signatures. The repository-wide decision requires every remaining structural Protocol
to migrate to a nominal ABC; the expanded documentation gate is complete, but the
coordinated source migration has not started.

## Architecture gate

```mermaid
flowchart TB
    approval[Human: architecture gate approved] --> classes[Document target classes]
    classes --> defects[Map all consolidated defects]
    defects --> migration[Record one migration map]
    migration --> evidence[Specify required software evidence]
    evidence --> review{No contradiction or unresolved choice?}
    review -->|no| revise[Revise architecture]
    revise --> classes
    review -->|yes| complete[Documentation gate complete]
    complete --> implementation[One coordinated implementation run]

    approval -. does not start .-> implementation
    approval -. does not authorize .-> protected[Replay, external execution, push, or release]
```

The verbatim decision and bounded interpretation are retained in the
[architecture-gate record](../workflows/architecture-gate.md).

## Nominal Task hierarchy

```mermaid
classDiagram
    class AbstractTask {
        <<ABC>>
        +identity TaskDefinitionIdentity*
        +definition TaskDefinition
    }
    class AbstractScientificTask {
        <<grouping ABC; no route>>
    }
    class AbstractInProcessScientificTask {
        <<in_process route ABC>>
        +execute(inputs, context) TaskExecutionResults*
    }
    class AbstractSimulationTask {
        <<simulation route ABC; no direct effect>>
    }
    class NestedWorkflowTask {
        <<nested_workflow route ABC; no execute>>
        +child_workflow_definition WorkflowDefinition*
    }
    class AbstractSimulationDispatchEffect {
        <<ABC>>
        +executor_identity ScientificExecutorIdentity*
        +execute(request) SimulationDispatchOutcome*
    }

    AbstractScientificTask --|> AbstractTask
    AbstractInProcessScientificTask --|> AbstractScientificTask
    AbstractSimulationTask --|> AbstractScientificTask
    NestedWorkflowTask --|> AbstractTask
    AbstractSimulationTask --> AbstractSimulationDispatchEffect : runtime binding only
```

`AbstractTask` rejects multiple route roots and route or definition overrides.
`AbstractSimulationDispatchEffect` inherits directly from `ABC`; no evidence supports a
generic dispatch-effect base.

## Generic definitions

```mermaid
classDiagram
    class TaskDefinition {
        <<concrete frozen DataObject>>
        +identity TaskDefinitionIdentity
        +execution_kind TaskExecutionKind
    }
    class WorkflowDefinition {
        <<concrete frozen DataObject>>
        +identity WorkflowIdentity
        +composition WorkflowComposition
    }
    class AbstractTask
    class AbstractWorkflow {
        <<ABC>>
        +definition WorkflowDefinition
    }

    AbstractTask --> TaskDefinition : final generic construction
    AbstractWorkflow --> WorkflowDefinition : final generic construction
```

Concrete operations and Workflows add no definition subclasses or schemas.

## Nominal result, observation, and persistence boundaries

```mermaid
classDiagram
    class AbstractResultObject {
        <<ABC>>
    }
    class AbstractNormalizedObservationSource {
        <<ABC>>
    }
    class AbstractObservationCorrelationIdentity {
        <<ABC>>
    }
    class AbstractObservationNormalizationPolicySource {
        <<ABC>>
    }
    class AbstractWorkflowResultValueCodec {
        <<ABC>>
    }
    class AbstractWorkflowRunRepository {
        <<ABC>>
    }
    class AbstractSimulationDispatchEntryCommitter {
        <<ABC>>
    }

    AbstractResultObject <|-- AbstractNormalizedObservationSource
    AbstractNormalizedObservationSource --> AbstractObservationCorrelationIdentity
    AbstractNormalizedObservationSource --> AbstractObservationNormalizationPolicySource
    AbstractWorkflowResultValueCodec --> AbstractResultObject
    AbstractSimulationDispatchEntryCommitter --> AbstractWorkflowRunRepository
```

Every implementation inherits nominally. Structural lookalikes, virtual registration,
and aliases for retired Protocol names are unsupported.

## Declarative plan and runtime bindings

```mermaid
classDiagram
    class WorkflowExecutionPlan {
        <<declarative frozen DataObject>>
        +workflow_definition WorkflowDefinition
        +task_definitions TaskDefinition[]
        +nested_workflow_targets NestedWorkflowTarget[]
    }
    class WorkflowTaskBinding {
        <<process-local frozen DataObject>>
        +task_instance_identity TaskInstanceIdentity
        +task AbstractTask
        +simulation_effect AbstractSimulationDispatchEffect?
    }
    class WorkflowExecutionBindings {
        <<process-local frozen DataObject>>
        +plan WorkflowExecutionPlan
        +task_bindings WorkflowTaskBinding[]
    }
    class WorkflowExecutionPlanConstructor
    class WorkflowExecutionBindingsConstructor

    WorkflowExecutionPlanConstructor --> WorkflowExecutionPlan : compiles definitions
    WorkflowExecutionBindingsConstructor --> WorkflowExecutionPlan : validates against
    WorkflowExecutionBindings --> WorkflowExecutionPlan : exact plan
    WorkflowExecutionBindings *-- WorkflowTaskBinding
    WorkflowExecutionBindingsConstructor --> WorkflowExecutionBindings : constructs
```

The declarative plan contains no live adapter. Runtime bindings are explicit and
complete but are not declarative persistence or scientific provenance.

## In-process execution

```mermaid
flowchart LR
    activation[TaskActivation] --> engine[WorkflowEngine.execute_in_process]
    bindings[WorkflowExecutionBindings] --> engine
    engine --> kind{Planned TaskExecutionKind}
    kind -->|in_process| context[TaskExecutionContext]
    context --> task[AbstractInProcessScientificTask]
    task --> results[TaskExecutionResults]
    kind -->|simulation| simulation[Fail closed: simulation control required]
    kind -->|nested_workflow| nested[Fail closed: child-run control required]
```

The in-process method neither authorizes simulation nor executes child members.

## Simulation authority path

```mermaid
flowchart LR
    task[AbstractSimulationTask] --> binding[WorkflowTaskBinding]
    effect[AbstractSimulationDispatchEffect] --> binding
    activation[TaskActivation] --> control[Simulation control plane]
    binding --> control
    authority[Authorized grant and verified snapshot] --> control
    control --> request[SimulationDispatchEffectRequest]
    request --> effect
    effect --> outcome[Dispatch outcome]
    outcome --> ingress[Reconciliation and confirmed ingress]
    ingress -->|confirmed| results[TaskExecutionResults]
    ingress -->|otherwise| none[No TaskExecutionResults]
```

Only the authority-bearing effect request reaches external execution.

## Nested Workflow path

```mermaid
flowchart LR
    target[NestedWorkflowTarget] --> control[Nested control]
    task[NestedWorkflowTask] --> binding[WorkflowTaskBinding]
    binding --> control
    parent[Parent WorkflowRun] --> control
    control --> child[Distinct child WorkflowRun]
    child --> terminal[Terminal observation]
    terminal -->|confirmed and replay-equal| results[TaskExecutionResults]
    results --> successor[Parent successor]
```

## Result and durable-outcome boundary

```mermaid
flowchart LR
    supplied[Concrete AbstractResultObject values] --> results[TaskExecutionResults]
    results --> shape{Ordered, nonempty, exact, unique?}
    shape -->|no| invalid[No admitted execution results]
    shape -->|yes| correlation[Production and route correlation]
    correlation -->|complete| outcome[Confirmed TaskInvocationOutcome]
    correlation -->|incomplete| no_outcome[No confirmed outcome]
```

`TaskExecutionResults` establishes shape only. Durable confirmation retains authority,
production, activation, attempt, artifact, and route evidence with their existing
owners.

## Periodic-1D boundary

The periodic-1D Workflow remains paused. Its future in-process Tasks may be defined only
after the coordinated architecture migration and evidence gate complete. No replay is
authorized by this schematic.
