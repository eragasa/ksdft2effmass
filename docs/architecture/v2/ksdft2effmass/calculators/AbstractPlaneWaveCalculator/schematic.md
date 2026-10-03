# `AbstractPlaneWaveCalculator` schematic

```mermaid
classDiagram
    class AbstractPlaneWaveCalculator~InputT, OutputT~ {
        <<ABC>>
        +execute(InputT, TaskExecutionContext) OutputT*
    }
    class ConcretePlaneWaveCalculator
    class AbstractSimulationDispatchEffect {
        <<ABC>>
        +execute(SimulationDispatchEffectRequest) SimulationDispatchOutcome*
    }

    AbstractPlaneWaveCalculator <|-- ConcretePlaneWaveCalculator
    AbstractPlaneWaveCalculator ..> AbstractSimulationDispatchEffect : distinct authority boundary
```

Nominal calculator membership supplies no external-effect authority. The two abstract
contracts are not interchangeable merely because both may use an `execute` name.
