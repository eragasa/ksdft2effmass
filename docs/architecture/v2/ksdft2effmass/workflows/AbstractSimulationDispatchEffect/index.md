# `AbstractSimulationDispatchEffect`

## Status

**Implemented nominal authority boundary; local software-verification evidence passes.**

## Responsibility

`AbstractSimulationDispatchEffect` is the nominal ABC for one claimed external
simulation effect. It replaces the structural `SimulationDispatchEffect` protocol
without a compatibility alias.

Its abstract public contract is:

```python
@property
@abstractmethod
def executor_identity(self) -> ScientificExecutorIdentity: ...

@abstractmethod
def execute(
    self,
    request: SimulationDispatchEffectRequest,
) -> SimulationDispatchOutcome: ...
```

The exact request is constructed only after Workflow control correlates the simulation
Task instance, activation, attempt, executor, inputs, configuration, reserved grant,
verified authority snapshot, dispatch obligation, successful claim, and dispatch-entry
receipt.

## Authority and result boundary

The ABC supplies no authority itself. A concrete implementation must independently
check executor-bound authority, invoke at most once, preserve exact correlations, and
never retry an indeterminate effect. It returns the established closed dispatch
outcome, not `TaskExecutionResults` directly. Reconciliation and confirmed result
ingress admit the concrete results.

`AbstractSimulationTask` exposes no direct effect method. A simulation runtime binding
correlates it with one explicit `AbstractSimulationDispatchEffect`; construction alone
performs no effect and grants no authority.

## Inheritance and discovery

Concrete executors inherit this ABC nominally. Structural lookalikes, module discovery,
entry points, mutable registries, and identity-based executor lookup are unsupported.
Calculator integrations do not define operation-specific dispatch-effect ABCs.

## Related architecture

- [Schematic](schematic.md)
- [`AbstractSimulationTask`](../AbstractSimulationTask/index.md)
- [`WorkflowTaskBinding`](../WorkflowTaskBinding/index.md)
- [Workflow control plane](../control-plane.md)
- [Repository-wide Protocol-to-ABC migration](../../protocol-to-abc-migration.md)
