---
document_id: ksdft2effmass.harness.002.001.010
task_id: harness.simplification.docs-json.task-document-migration
parent: ksdft2effmass.harness.002.001.000
status: proposed-awaiting-human-review
sphinx: excluded
---

# Human review: per-file Task-document migration

> **Proposed, not active.** This page presents the complete migration Task for
> human review. It does not activate the Task, approve any file migration, or
> authorize chain cutover.

## Purpose

Resume the unfinished documentation/control authority merge. The migration must
produce canonical JSON Tasks capable of preserving the Task information currently
held in maintained documentation, while retaining documentation-owned project
meaning and preventing loss of LaTeX, Mermaid, code fences, directives, tables,
links, and other project-specific content.

The accepted attempt-1 inventories remain immutable. They established complete
path coverage for their revision but only seven partial mappings, zero fully
mapped paths, and residuals containing all 222 documentation paths and all 23
control paths. The one-Task JSON pilot therefore demonstrated mechanics but did
not complete the parent migration.

## Selected files

This first bounded migration covers exactly these six Task records:

1. `.pi/tasks/harness.simplification.docs-json.md`
2. `.pi/tasks/harness.simplification.docs-json.publication.md`
3. `.pi/tasks/harness.simplification.docs-json.publication.triage.md`
4. `.pi/tasks/harness.simplification.docs-json.publication.hierarchy.md`
5. `.pi/tasks/harness.simplification.docs-json.authority-catalog.md`
6. `.pi/tasks/harness.simplification.docs-json.documentation-correction.md`

No other Task or narrative document is migrated by this Task. The completed
`harness.simplification.docs-json.publication` parent is restored to operational
chain membership before activation so every selected source remains exactly
inspectable during migration.

## Information model

The exact `HarnessTask` fields are derived from reviewed documentation/control
mappings rather than selected in advance for implementation convenience.

| Proposed object | Kind | Responsibility |
|---|---|---|
| `HarnessTask` | DataObject | Immutable complete Task information and intrinsic invariants |
| `HarnessTaskSerializer` | ActionObject | Canonical versioned JSON serialization |
| `HarnessTaskDeserializer` | ActionObject | Strict JSON deserialization without information loss |
| `HarnessTaskGraphValidator` | ActionObject | Parent, prerequisite, and cross-Task compatibility |
| `HarnessTaskDocumentationRenderer` | ActionObject | Complete maintained Markdown rendering |
| `HarnessTaskDocumentationComparator` | ActionObject | Exact rendered/source comparison and unexplained-difference detection |
| `HarnessTaskDocumentationComparisonResult` | ResultObject | Structured differences, unmapped spans, and findings |

`TaskRecordAdapter` remains a compatibility adapter during migration. It does not
become the canonical Task model. Selection state remains separate from Task data.

## Two-list authority merge

The migration preserves the existing method:

```text
current documentation inventory
+ current selected control inventory
→ reviewed subject and source-span mappings
→ HarnessTask field contract
→ canonical JSON
→ deserialized HarnessTask
→ maintained Markdown rendering
→ exact comparison with the human-reviewed document
```

Every Task-relevant source span receives exactly one disposition:

- represented by an explicit `HarnessTask` field;
- retained as documentation-owned narrative and referenced by the Task;
- retained as historical evidence; or
- removed only through an explicit disposition for that exact file.

The new current-revision inventories are a second immutable migration attempt.
They do not overwrite the accepted attempt-1 catalogs or become runtime
registries.

## Per-file human gate

Files are processed serially. For one file, and only one file, the migration
prepares an immutable review packet containing:

- source path, Git object identity, byte count, and SHA-256;
- candidate `HarnessTask` values and canonical JSON;
- source-span mappings and unmapped spans;
- candidate maintained Markdown bytes;
- an exact source/rendered diff;
- explicit opaque-block treatment; and
- implementation and claim limitations.

The migration then stops. The human selects one disposition:

1. accept this file migration;
2. revise the mappings or candidate representation;
3. retain documentation ownership for identified content; or
4. defer this file.

No later packet is prepared until the current disposition is durably recorded.
Passing schema, round-trip, renderer, or comparison checks cannot replace this
human decision.

## Opaque project content

LaTeX equations, Mermaid blocks, code fences, directives, tables, links, and
other opaque project content are preserved byte-for-byte unless the human accepts
one stated transformation for the exact file under review. The migration may not
normalize whitespace, reflow prose, reinterpret syntax, or silently discard a
block.

## Selection-state boundary

The selected architecture uses Tasks as the Task graph and a separate minimal
selection-state record for active Task and activation facts. This Task may create
a candidate selection-state shadow after all six file migrations. The current
chain remains operational authority throughout this Task.

`TaskRecordAdapter` must retain mixed Markdown/JSON compatibility while
`TaskStateInspector` and maintained projections are updated for `HarnessTask` and
candidate selection-state inputs. Every selected Task must remain exactly
inspectable after every accepted file migration.

The migration retains exact pre-migration chain and source identities plus a
per-file old/new map. Each human-accepted file is a durable Git decision boundary;
rollback uses a normal revert to the preceding accepted boundary and never
rewrites historical chain evidence. Cutover, chain retirement, and migration of
the other Markdown Tasks require later review and separate authorization.

## Required evidence

Completion requires:

- reviewed current-revision documentation and control inventories;
- complete mappings for the six selected files;
- canonical JSON schema and valid/invalid fixtures;
- public API, typing, serialization, rendering, comparison, and graph tests;
- six separately accepted human-review packets;
- exact post-migration render agreement for every accepted file;
- mixed-format `TaskRecordAdapter` and exact `TaskStateInspector` agreement after
  every accepted file;
- maintained review-projection agreement;
- retained pre-migration identities and a verified non-destructive rollback map;
- chain/candidate selection-state shadow agreement;
- Sphinx warnings-as-errors, dependency and lockfile checks;
- one consolidated independent integration review; and
- no unresolved material finding.

These checks establish software-contract behavior only. They do not establish
scientific validity, publication readiness, release readiness, or human
acceptance beyond each exact recorded file disposition.

## Explicit exclusions

This Task does not authorize:

- batch acceptance or automatic continuation;
- migration outside the six selected files;
- operational chain cutover or deletion;
- SQLite, event logs, repository discovery, or new dependencies;
- scientific, publication, external, protected, or release work; or
- automatic successor activation.

## Human review question

Should `harness.simplification.docs-json.task-document-migration` be activated
with exactly the scope, serial file gates, preservation rules, object boundaries,
and exclusions stated on this page?

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [Incremental migration plan](ksdft2effmass.harness.002.001.009.md)
