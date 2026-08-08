---
document_id: ksdft2effmass.harness.002.001.009
task_id: harness-simplification.migration
parent: ksdft2effmass.harness.002.001.000
status: proposed
sphinx: excluded
---

# Incremental migration plan

> **Incremental architecture.** Durable-role creation, project-role
> simplification, and retirement of historical phase roles from selectable PI
> discovery are complete. SQLite implementation, agent-file deletion, package
> extraction, and publication remain inactive and unauthorized.

The harness should evolve through bounded compatibility slices rather than a
wholesale replacement. Each slice retains a rollback path, compares structured
results, and changes one authority owner only after explicit acceptance.

## Current stage disposition

Completed:

- `harness-simplification.agents.durable-roles`
- `harness-simplification.agents.project-role-simplification`
- `harness-simplification.agents.live-discovery-cleanup`
- `harness-simplification.agents.live-discovery`
- `harness-simplification.agents.historical-retirement`

Inactive and unauthorized:

- `harness-simplification.execution.review-dispatch-idempotency`
  (`deferred_inactive`)
- `harness-simplification.agents.delegation-validation`
- `harness-simplification.evidence-and-sqlite`

The 24 historical phase-specific harness records remain present byte-for-byte
and are disabled only from selectable discovery by project-level
`.pi/settings.json`. The 10 durable roles remain selectable. Historical file
presence and runtime discoverability grant no task authority.

## Proposed stages

1. **Inventory and contracts.** Freeze the current readers, writers, identities,
   relations, commands, and claim boundaries. Identify duplicated mechanisms and
   authoritative owners.
2. **Read-only state import.** Import existing task, chain, checkpoint, ownership,
   route, and evidence references into a candidate SQLite database. Compare
   derived views with current validators without changing authority.
3. **Evidence subsystem.** Introduce generic evidence records and reconciliation
   behind adapters. Preserve existing evidence IDs and historical files.
4. **Execution records.** Represent focused and full commands with explicit
   `python/.venv/bin/python`, argument vectors, controlled environment, and
   structured results. Keep existing scripts as the execution backend.
5. **Durable agents.** Durable harness capability roles now exist. Project-role
   simplification, live-discovery changes, delegation validation, and any later
   retirement remain separate proposed slices.
6. **State-owner cutover.** Move one operational record family at a time to the
   accepted state interface, with exports and rollback verified at each step.
7. **Extraction readiness.** Build a disposable generic package candidate without
   local Python, local resources, `.pi` state, scientific modules, or repository
   fallback. This demonstrates readiness only; it does not publish a package.
8. **Retirement.** Remove duplicate readers or legacy routes only after retained
   compatibility and rollback requirements are satisfied.

## Comparison policy

Structured comparisons classify differences as equivalent, intentional,
deferred, or defect. Deferred and defect results block authority changes.
Timestamps, temporary paths, and presentation may be normalized only by an
accepted rule.

## Extraction boundary

A future generic extraction candidate may contain generic Python, schemas,
fixtures, skills, evidence records, and validation interfaces. Project-local
Python, profiles, route configuration, agents, operational state, and scientific
policy remain in the project.

## Completion boundary

Each stage requires its own authorization, ownership, focused validation,
reconciliation, read-only review, and human acceptance where applicable. No
stage automatically activates the next.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [Harness capability ownership rationalization](ksdft2effmass.harness.002.001.008.md)
- **Next:** [Human review interface](ksdft2effmass.harness.003.000.000.md)
