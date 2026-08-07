---
document_id: ksdft2effmass.harness.010.050.000
task_id: harness-simplification.migration
parent: ksdft2effmass.harness.010.000.000
status: proposed
sphinx: excluded
---

# Incremental migration plan

> **Proposed architecture.** No migration, SQLite implementation, agent
> retirement, package extraction, or publication is authorized by this page.

The harness should evolve through bounded compatibility slices rather than a
wholesale replacement. Each slice retains a rollback path, compares structured
results, and changes one authority owner only after explicit acceptance.

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
5. **Durable agents.** Map phase-specific agents to stable project and harness
   roles. Compare request resolution before retiring duplicates.
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

See the [simplification overview](./ksdft2effmass.harness.010.000.000.md) and
[historical documentation](./ksdft2effmass.harness.090.000.000.md).
