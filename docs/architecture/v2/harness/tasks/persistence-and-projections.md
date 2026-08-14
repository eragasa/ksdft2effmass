# Harness Task persistence and projections

## Authoritative records

Harness Task persistence retains immutable revisions of:

- Task definitions and catalogs;
- Task graphs;
- development selections;
- Task closures;
- decision and authority references;
- evidence and review references;
- completion records; and
- acceptance records.

Persistence owns transaction, revision, migration, and recovery behavior. It does not own Task meaning, eligibility policy, transition policy, or human authority.

## Repository actions

| ActionObject | Responsibility |
|---|---|
| `HarnessTaskRepository` | Read and append authoritative Task-family records under explicit transaction rules |
| `HarnessTaskSerializer` | Own versioned Task-definition wire representation |
| `HarnessTaskClosureSerializer` | Own versioned closure wire representation |
| `DevelopmentTaskSelectionSerializer` | Own selection wire representation |
| `HarnessTaskProjectionBuilder` | Build derived human-readable or machine-readable views |
| `HarnessTaskProjectionComparator` | Compare projections with authoritative source revisions |

Repository methods return immutable persistence ResultObjects. Serializers and repositories remain separate from DataObjects.

## Projection boundary

Generated Task pages, indexes, dashboards, graphs, SQLite-derived views, and similar outputs are deterministic projections. Architecture v2 places generated views outside human-authored `docs/`. Existing generated Markdown pages under `docs/harness/tasks/` remain V1 migration inputs until the separately governed documentation cutover moves or retires them. Every projection identifies its authoritative input revisions and compiler identity.

A projection may not:

- create or mutate a Task;
- create or alter a closure;
- activate or select work;
- resolve a decision;
- establish completion or acceptance; or
- become authority merely because it is committed.

## Recovery

Authoritative records must support deterministic reconstruction and comparison. Recovery validates identity, schema version, referential integrity, revision ordering, and projection agreement without rewriting accepted history.

## Unresolved issues

- Final authoritative storage technology and transaction model.
- Whether closures and selections share one transaction boundary.
- Migration strategy for current Task JSON, task graph, SQLite, and generated Markdown.
- Projection-retention policy after human-authored documentation is separated from generated views.
- Long-term retention of superseded selections and closures.
