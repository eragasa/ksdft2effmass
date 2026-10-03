# `TaskExecutionResults` schematic

## Status

**Implemented architectural schematic; local software-verification evidence passes.**

## Type boundary

```mermaid
classDiagram
    class AbstractResultObject {
        <<nominal ABC>>
        +identity ResultObjectIdentity*
    }
    class TaskExecutionResults {
        <<concrete frozen DataObject>>
        +results AbstractResultObject[]
    }
    class TaskInvocationOutcome {
        +results ResultObjectReference[]
        +production_record_identities ResultProductionRecordIdentity[]
    }

    TaskExecutionResults *-- AbstractResultObject : ordered nonempty tuple
    TaskInvocationOutcome --> TaskExecutionResults : requires admitted results
```

`TaskExecutionResults` has no subclasses. Variation belongs to the contained concrete
`AbstractResultObject` instances. The relation to `TaskInvocationOutcome` is a construction
prerequisite, not inheritance, persistence embedding, or proof of confirmation.

## Intrinsic construction

```mermaid
flowchart TB
    supplied[Supplied value] --> tuple_check{Exact tuple?}
    tuple_check -->|no| type_error[TypeError]
    tuple_check -->|yes| nonempty{At least one result?}
    nonempty -->|no| value_error[ValueError]
    nonempty -->|yes| result_check{Every member inherits AbstractResultObject?}
    result_check -->|no| type_error
    result_check -->|yes| identity_check{Exact ResultObjectIdentity values?}
    identity_check -->|no| type_error
    identity_check -->|yes| unique{Unique identities?}
    unique -->|no| value_error
    unique -->|yes| retained[TaskExecutionResults<br/>original order retained]
```

These checks establish only local result shape and identity uniqueness.

## Successful route convergence

```mermaid
flowchart LR
    inprocess[In-process scientific Task] --> inprocess_results[TaskExecutionResults]

    dispatch[Authority-correlated simulation dispatch] --> ingress[Confirmed result ingress]
    ingress --> simulation_results[TaskExecutionResults]

    child[Confirmed child Workflow export] --> nested_results[TaskExecutionResults]

    rejected[Rejected route] --> none[No TaskExecutionResults]
    indeterminate[Indeterminate route] --> none
```

The three successful routes share the same result-shape value without sharing their
execution, authority, dispatch, child-run, or admission mechanics.

## Durable confirmation

```mermaid
flowchart LR
    results[TaskExecutionResults] --> correlation[Workflow control correlation]
    production[One production record per result] --> correlation
    activation[Run, Task, activation, operation, attempt] --> correlation
    specialized[Applicable dispatch or nested evidence] --> correlation
    correlation --> admitted{All exact correlations admitted?}
    admitted -->|yes| confirmed[Confirmed TaskInvocationOutcome]
    admitted -->|no| no_outcome[No confirmed outcome]
```

`TaskExecutionResults` alone never reaches the confirmed branch. Workflow control must
retain positional agreement among contained results, result references, and production
records.

## Schema boundary

```mermaid
flowchart TB
    common[One TaskExecutionResults class] --> periodic[Periodic AbstractResultObject implementations]
    common --> qe[Quantum ESPRESSO AbstractResultObject implementations]
    common --> other[Other domain AbstractResultObject implementations]
    common -. no per-Task container subclass .-> prohibited[Operation-specific result-container schemas]
```

The common container remains one Workflow-control DataObject. Domain-specific result
schemas remain with the concrete `AbstractResultObject` owners; durable Workflow formats retain
outcome and result references rather than a duplicate container schema.
