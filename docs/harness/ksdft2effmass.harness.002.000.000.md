---
document_id: ksdft2effmass.harness.010.000.000
task_id: harness-simplification
parent: ksdft2effmass.harness.000.000.000
status: proposed
sphinx: excluded
---

# Harness simplification proposal

> **Proposed architecture.** Nothing in this topic is implemented or accepted by
> this documentation task.

The proposal reduces duplicated parsing, state synchronization, command
assembly, evidence indexing, and phase-specific agent configuration while
preserving the current generic/project-local boundary and explicit human
authority.

## Proposed components

| Document | Proposed responsibility |
|---|---|
| [harness.010.010.000](./ksdft2effmass.harness.010.010.000.md) | SQLite-backed operational state and event model |
| [harness.010.020.000](./ksdft2effmass.harness.010.020.000.md) | Extractable `harness.pi.evidence` subsystem |
| [harness.010.030.000](./ksdft2effmass.harness.010.030.000.md) | Durable project-agent and harness-agent sets |
| [harness.010.040.000](./ksdft2effmass.harness.010.040.000.md) | Maintained execution and validation interface |
| [harness.010.050.000](./ksdft2effmass.harness.010.050.000.md) | Incremental migration and extraction-readiness plan |

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

Return to the [repository harness index](./ksdft2effmass.harness.000.000.000.md).
