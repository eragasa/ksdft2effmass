# V2-ISSUE-001: Simulation execution request context

**Severity:** Implementation blocker

**Scope:** Scientific workflow and calculator execution

## Conflict

`workflow/simulation-model.md` defines `SimulationExecutor` as accepting only a reusable `Simulation`. The executor is nevertheless required to validate and correlate request, attempt, run, authority, executor-configuration, and resource identities. Those request-scoped values deliberately do not belong to `Simulation`.

## Affected contracts

- `workflow/simulation-model.md` — *Simulation specification* and *Executor protocol*
- `workflow/control-plane.md` — *Dispatch invariants*
- `calculators/quantum-espresso.md` — executor validation contract

## Required resolution

Define an immutable calculator-independent `SimulationExecutionRequest`, or equivalent explicit input, carrying every request-scoped identity and grant required by the executor. The executor must not obtain them from ambient state.

A likely operation shape is:

```python
execute(request: SimulationExecutionRequest) -> SimulationExecutionResult
```

## Acceptance condition

Executor input, result, persistence, retry, and correlation contracts agree on exact run, request, attempt, simulation, authority, executor-configuration, and resource-policy identities.

This issue does not activate implementation or authorize external execution.
