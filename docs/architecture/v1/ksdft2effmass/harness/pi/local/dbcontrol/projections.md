# `ksdft2effmass.harness.pi.local.dbcontrol.projections` in v1

## Maintained projection set

The private projection synchronizer publishes a complete generated set containing:

- `harness/state/harness-control.sqlite3`;
- `harness/state/harness-control.sql`;
- `harness/state/projection-manifest.json`;
- `harness/task-graph.json`;
- resource-manifest projections; and
- the Python evidence module inventory.

## Publication path

```mermaid
flowchart LR
    sources["Canonical sources"] --> candidate["Temporary candidate"]
    candidate --> validate["Candidate validation"]
    validate --> close["Close mutable resources"]
    close --> publish["Publish complete set"]
```

Candidate construction occurs in a temporary workspace. Publication follows validation and closes database resources first. Partial candidates are not intended to represent current control state.

## Source-aware verification

The private projection verifier reconstructs the candidate without publication and checks:

- SQLite integrity and foreign keys;
- control schema version;
- normalized semantic content and digest;
- deterministic SQL;
- projection-manifest agreement; and
- exact projector-owned projections.

Raw SQLite byte differences do not by themselves establish semantic drift.

Generated projections do not target `docs/`; maintained documentation remains human-authored.

## Scientific views

V1 has calculation-specific summaries and manifests but no general scientific projection model over `ScientificWorkflowRun`. Dashboards or graphs, where present, remain derived evidence and cannot authorize execution or accept results.
