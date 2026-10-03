# `AbstractSimulationTask`

## Status

**Implemented architectural contract; local software-verification evidence passes.**

## Responsibility

`AbstractSimulationTask(AbstractScientificTask)` is the simulation route root. It fixes
`TaskExecutionKind.SIMULATION` and owns immutable operation definition and
backend-specific input correlation. It exposes no ordinary `execute(inputs,
TaskExecutionContext)` method.

The absence of that method is intentional: `TaskExecutionContext` carries correlation,
not execution authority. Protected external effects remain exclusively behind the
target `AbstractSimulationDispatchEffect`, which consumes an authority-bearing
`SimulationDispatchEffectRequest` after reservation and claim controls succeed.

## Runtime binding

A simulation `WorkflowTaskBinding` correlates the exact `AbstractSimulationTask` with
one explicit `AbstractSimulationDispatchEffect`. The binding creates no authority. The
Workflow control plane prepares and authorizes the request, reserves and claims the
obligation, invokes the effect, reconciles the dispatch outcome, and performs result
ingress.

Only confirmed ingress admits `TaskExecutionResults`. Rejected or indeterminate
simulation outcomes contain no such value. Nominal Task membership never proves that a
process ran, converged, or was scientifically accepted.

Concrete calculator integrations reuse this ABC and the generic `TaskDefinition`; they
do not create calculator-specific Task-definition schemas.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractSimulationDispatchEffect`](../AbstractSimulationDispatchEffect/index.md)
- [`WorkflowTaskBinding`](../WorkflowTaskBinding/index.md)
- [Workflow control plane](../control-plane.md)
