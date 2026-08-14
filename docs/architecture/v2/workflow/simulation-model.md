# Simulation model

## Simulation specification

`Simulation` is an immutable calculator-independent specification for one scientific operation. Its generic contract contains only identity and extension boundaries needed by scientific orchestration. Calculator-specific scientific and numerical input remains in a typed payload owned by the calculator package.

A simulation specification composes:

| Object | Responsibility |
|---|---|
| `SimulationIdentity` | Stable logical simulation identity |
| `CalculatorFamilyIdentity` | Required calculator family |
| `SimulationOperationKind` | Typed generic operation category |
| `SimulationPayloadReference` | Reference to a calculator-owned typed payload |
| `RequiredArtifactReference` | Required immutable input or pseudopotential |
| `ExpectedArtifactRole` | Declared output role |

Attempt identity belongs to an execution request, not the reusable `Simulation` definition.

Scientific parameters do not move into `ScientificWorkflow` merely because they influence workflow order.

## Typed features

Model features are typed source values. Tags used for selection or capability matching are derived deterministically from those values rather than maintained as a second mutable classification. A calculator-specific payload models only features demonstrated by accepted use cases. Exact canonical input bytes remain available when a complete structured renderer is not justified.

## Execution result

`SimulationExecutionResult` is immutable and separate from `Simulation`. It contains mechanical observations:

- simulation and request identities;
- execution status and external exit status;
- completion-marker presence;
- stdout and stderr artifact identities;
- generated artifact identities;
- elapsed time and peak RSS when available;
- calculator warnings; and
- source native-output identities.

It contains no scientific convergence or acceptance claim. A completed simulation is not mutated in place; a new result is correlated to the exact request and attempt. Re-execution requires a new attempt identity.

## Executor protocol

`SimulationExecutor` is a structural protocol with an operation equivalent to:

```python
execute_simulation(simulation: Simulation) -> SimulationExecutionResult
```

Implementations validate configuration and identities before performing bounded external effects. They reject unsupported typed features, missing required artifacts, executable drift, canonical input drift, and duplicate attempt use.

## Calculator-specific ownership

`ksdft2effmass.calculators` owns calculator-specific simulation payloads, configuration, and executors. The first demonstrated calculator family is Quantum ESPRESSO `pw.x`; other programs are not modeled as enum values of that contract because they have different inputs and outputs.

`ksdft2effmass.io` owns mechanical input/output translation. It does not own executor policy, scientific workflow order, or scientific interpretation.

## Normalization path

```text
Simulation
→ SimulationExecutor
→ SimulationExecutionResult
→ mechanical native-output parsing
→ normalized periodic and Kohn–Sham observations
→ ScientificAnalysis
→ ScientificDisposition
```

Every arrow has an explicit owner and preserves source identities.

## Unresolved issues

- Exact generic `SimulationOperationKind` vocabulary.
- Whether payloads are embedded immutable values or separately identified records.
- Canonical input identity when a structured renderer is used.
- Capability matching between payload features and executors.
- Resource requirements represented on `Simulation` versus execution request.
- Public asynchronous executor method, if required.
