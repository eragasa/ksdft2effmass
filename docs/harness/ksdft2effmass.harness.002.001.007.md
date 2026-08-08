---
document_id: ksdft2effmass.harness.002.001.007
task_id: harness-simplification.execution
parent: ksdft2effmass.harness.002.001.000
status: proposed
sphinx: excluded
---

# Maintained execution interface

> **Proposed architecture.** The current generic harness intentionally has no
> command runner. This page proposes one bounded maintained interface; it does
> not authorize command execution.

The proposed interface represents a command request and result without shell
interpretation or ambient environment selection.

## Capability decomposition

| Decomposition | Responsibility |
|---|---|
| [harness.002.001.008](./ksdft2effmass.harness.002.001.008.md) | Skill, durable/inactive-agent, ActionObject, and tool capability ownership rationalization |

## Canonical interpreter

Repository Python commands use:

```text
python/.venv/bin/python
```

The executable identity should be explicit in every maintained request. `uv`
may provision that environment, but a recorded command must not silently switch
to the repository-root `.venv`, system Python, or whichever interpreter appears
first on `PATH`.

## Request record

A proposed request would contain an argument vector, absolute working directory,
controlled environment additions, timeout, input identities, validation mode,
and expected structured observation. It would contain no shell string, secret,
open handle, or executable callback.

## Result record

A proposed result would distinguish:

- process start and completion;
- exit status and timeout;
- stdout/stderr artifact identities;
- structured-observation parse status;
- selected validator status;
- aggregate status.

A successful process exit could not override a failed or missing nested
observation.

## Validation modes

**Focused validation** would execute the smallest declared checks for changed
owners and direct dependents. **Full reconciliation** would execute the declared
cross-record and repository consistency checks required at a durable boundary.
The mode is input data, not inferred from command names.

## Safety boundary

The interface would not itself authorize a protected action, remote execution,
Git mutation, dependency installation, release, or scientific calculation.
Callers must establish authority before dispatch. Sensitive environment values
must never enter durable request or result records.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [Executable harness-tool placement contract](ksdft2effmass.harness.002.001.006.md)
- **Next:** [Harness capability ownership rationalization](ksdft2effmass.harness.002.001.008.md)
