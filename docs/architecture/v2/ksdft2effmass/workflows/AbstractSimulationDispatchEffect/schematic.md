# `AbstractSimulationDispatchEffect` schematic

```mermaid
classDiagram
    class AbstractSimulationDispatchEffect {
        <<ABC>>
        +executor_identity ScientificExecutorIdentity*
        +execute(request) SimulationDispatchOutcome*
    }
    class SimulationDispatchEffectRequest
    class SimulationDispatchOutcome
    class ConcreteSimulationExecutor

    ConcreteSimulationExecutor --|> AbstractSimulationDispatchEffect
    AbstractSimulationDispatchEffect --> SimulationDispatchEffectRequest : consumes
    AbstractSimulationDispatchEffect --> SimulationDispatchOutcome : returns
```

```mermaid
flowchart LR
    prepared[Prepared simulation dispatch] --> authorize[Authority check]
    authorize -->|authorized| reserve[Reserve grant and obligation]
    authorize -->|denied or error| stop[No effect]
    reserve --> claim[Expected-revision claim]
    claim -->|won| request[SimulationDispatchEffectRequest]
    claim -->|lost| stop
    request --> effect[AbstractSimulationDispatchEffect]
    effect --> outcome[Confirmed, rejected, or indeterminate outcome]
    outcome --> reconcile[Reconciliation and ingress]
    reconcile -->|confirmed| results[TaskExecutionResults]
```

The nominal effect ABC is the only external-execution method. The simulation Task and
its runtime binding do not bypass the authority-bearing request.
