---
document_id: ksdft2effmass.harness.002.000.000
task_id: harness-simplification
parent: ksdft2effmass.harness.000.000.000
status: proposed
sphinx: excluded
---

# Harness simplification plan

> **Program boundary.** This plan contains completed bounded work and proposed or
> deferred work. It is not accepted as a whole and activates no item.

The proposal reduces duplicated parsing, state synchronization, command
assembly, evidence indexing, and phase-specific agent configuration while
preserving the current generic/project-local boundary and explicit human
authority.

## Proposed components

| Document | Proposed responsibility |
|---|---|
| [harness.002.001.000](ksdft2effmass.harness.002.001.000.md) | Complete first-round navigation and current status distinctions |
| [harness.002.001.001](ksdft2effmass.harness.002.001.001.md) | SQLite-backed operational state and event model |
| [harness.002.001.002](ksdft2effmass.harness.002.001.002.md) | Extractable `harness.pi.evidence` subsystem |
| [harness.002.001.003](ksdft2effmass.harness.002.001.003.md) | Durable project-agent and harness-agent sets |
| [harness.002.001.007](ksdft2effmass.harness.002.001.007.md) | Maintained execution and validation interface |
| [harness.002.001.009](ksdft2effmass.harness.002.001.009.md) | Incremental migration and extraction-readiness plan |

## Design goals

- one operational source for current normalized state and relations;
- append-only events for provenance and recovery;
- clear separation between focused validation and full reconciliation;
- evidence records that can be extracted without project-domain policy;
- durable role definitions with task-specific scope supplied as data;
- structured command requests and results using the canonical project Python;
- compatibility adapters during migration rather than wholesale replacement.

## Preserved boundaries

The proposal does not move scientific meaning into the harness, make evidence
authoritative over human decisions, permit ambient repository discovery, add a
workflow engine, or authorize external execution. Historical files remain
retained evidence until an accepted migration defines archival treatment.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Previous:** [Current status and limitations](ksdft2effmass.harness.001.006.000.md)
- **Next:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Child:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)

Return to the [repository harness index](./ksdft2effmass.harness.000.000.000.md).
