# V2-ISSUE-020: Workflow replay computation and integrity ownership

**Severity:** High
**Scope:** WorkflowRun reconstruction, replay integrity, version resolution, and enforcement gates
**Status:** Open

## Current conflict

Replay equality is normative, while the repository and transaction validator are prohibited from computing transitions and no other component owns replay computation, version resolution, the integrity result, or the gate at which that result is enforced.

## Affected contracts

- [`docs/architecture/v2/index.md`](../index.md) — WorkflowRun is described as replayable while replay-computation ownership remains open.
- [`docs/architecture/v2/workflow/workflow-run.md`](../workflow/workflow-run.md) — replay equality is required, but repository and validator computation is forbidden and no replay owner is named.
- [`docs/architecture/v2/workflow/persistence.md`](../workflow/persistence.md) — repositories validate supplied successors without owning transition replay.
- [`docs/architecture/v2/persistence/index.md`](../persistence/index.md) — the shared store is domain-neutral and explicitly does not compute WorkflowRun integrity.
- [`docs/architecture/v2/separation-of-harness-and-workflow.md`](../separation-of-harness-and-workflow.md) — reconstruction depends on exact versioned workflow definitions and implementations whose resolver boundary is not closed.
- [`docs/architecture/migration/v1-to-v2/index.md`](../../migration/v1-to-v2/index.md) — migration requires replayable WorkflowRun state without naming the integrity computation boundary.

## Missing contract

The workflow layer lacks an owner for deterministic replay, exact definition/evaluator/adapter version resolution, a closed integrity result, and the mandatory load, advancement, or commit gates that consume that result without moving transition computation into persistence.

## Exclusions and claim boundary

Selection identity remains separately tracked by V2-ISSUE-007. Exact implementation identity spelling is excluded. This record establishes no implementation, verification, scientific validation, uncertainty quantification, or human acceptance.
