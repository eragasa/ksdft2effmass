---
document_id: ksdft2effmass.harness.010.010.000
task_id: harness-simplification.state
parent: ksdft2effmass.harness.010.000.000
status: proposed
sphinx: excluded
---

# Unified state model

> **Proposed architecture.** The current harness does not use SQLite as its
> operational state owner.

The proposed model stores normalized current operational state in one
project-local SQLite database while retaining version-controlled source records
and historical evidence according to explicit import and archival rules.

## Proposed state classes

| State | Examples | Proposed treatment |
|---|---|---|
| Definitions | Tasks, agents, skills, resource identities, ownership scopes | Versioned rows imported from maintained source records with source identity. |
| Current state | Task lifecycle, active chain relation, unresolved checkpoint, route selection | Transactional current rows with validated transitions. |
| Events | Activation, validation observation, checkpoint decision, state transition | Append-only ordered records referencing the acting authority and inputs. |
| Evidence references | Reports, checksums, command results, review findings | Immutable identities and locations; large artifacts remain outside the database. |
| Derived views | Ready tasks, unresolved decisions, ownership overlap, stale evidence | Recomputable queries, never independent authority. |

## Authority and provenance

A database row would not grant authority by existing. Every state transition
would reference the controlling task, applicable human decision, source record,
and prior state. Human responses remain distinguishable from agent findings and
deterministic observations.

The database should preserve event history without copying complete chat
transcripts or large calculation outputs. Credentials and restricted data remain
prohibited.

## Transactions and reconciliation

One transaction should update related current-state rows and append the
corresponding event. Full reconciliation should verify source identities,
foreign-key relations, lifecycle rules, evidence references, and exported
version-controlled summaries. A derived export may support review and Git diffs,
but must not become a second mutable source of truth.

## Compatibility boundary

Initial adapters would read the existing JSON and Markdown records and populate
a candidate database. During migration, read-only comparison would establish
agreement before any current-state owner changes. The proposal does not authorize
deleting or rewriting historical records.

See the [simplification overview](./ksdft2effmass.harness.010.000.000.md).
