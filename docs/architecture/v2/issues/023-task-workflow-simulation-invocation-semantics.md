# V2-ISSUE-023: Generic Task, nested Workflow, and simulation invocation semantics

**Severity:** High
**Scope:** Task invocation outcomes, nested Workflow execution, simulation dispatch, transition admission, and failure history
**Status:** Open

## Current conflict

The generic `Task.execute` contract has no closed failure or uncertainty outcome; nested Workflow run, marking, and failure propagation are undefined; and the simulation path inconsistently assigns invocation to the Task, executor, and `SimulationDispatchAdapter` without closing request-transition construction, result firing, or failure-to-history semantics.

## Affected contracts

- [`docs/architecture/v2/ksdft2effmass/workflows/task-and-colored-petri-net-adapter.md`](../ksdft2effmass/workflows/task-and-colored-petri-net-adapter.md) — generic Task success is described, but ordinary failure, uncertainty, nested Workflow state, and the selected invocation owner are not closed.
- [`docs/architecture/v2/ksdft2effmass/workflows/service-model.md`](../ksdft2effmass/workflows/service-model.md) — `SimulationDispatchAdapter` invokes the executor and commits request state without a complete generic Task lifecycle.
- [`docs/architecture/v2/ksdft2effmass/workflows/workflow-run.md`](../ksdft2effmass/workflows/workflow-run.md) — Task failure records exist without a generic invocation outcome that produces and admits them.
- [`docs/architecture/v2/ksdft2effmass/workflows/simulation-task-model.md`](../ksdft2effmass/workflows/simulation-task-model.md) — SimulationTask ownership overlaps the dispatch adapter and executor path.
- [`docs/architecture/v2/ksdft2effmass/calculators/index.md`](../ksdft2effmass/calculators/index.md) — simulation outcomes are specialized while generic Task failure and uncertainty remain absent.
- [`docs/architecture/v2/ksdft2effmass/calculators/quantum-espresso.md`](../ksdft2effmass/calculators/quantum-espresso.md) — the executor is invoked directly although the SimulationTask is said to return the output.
- [`docs/architecture/v2/identity-version-and-failure-contracts.md`](../identity-version-and-failure-contracts.md) — every operation requires a closed failure vocabulary that generic Task invocation lacks.
- [`docs/architecture/v2/separation-of-harness-and-workflow.md`](../separation-of-harness-and-workflow.md) — pre-effect request-transition ownership and failure recording are not assigned consistently.

## Missing contract

Architecture v2 lacks one Task invocation lifecycle covering ordinary in-process Tasks, externally dispatched simulation Tasks, and nested Workflows: invocation ownership, closed success/failure/indeterminate outcomes, request and result transition construction, child run/marking scope, retry and duplicate behavior, and failure admission to aggregate history.

## Exclusions and claim boundary

Cancellation and compensation are excluded unless required by the common invocation lifecycle. This record establishes no implementation, execution authority, verification, scientific validation, uncertainty quantification, or human acceptance.
