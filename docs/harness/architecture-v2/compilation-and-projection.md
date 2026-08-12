# Architecture v2 compilation and projection

> **Proposed architecture; inactive; not implemented; not accepted.**

This page separates deterministic normalization from artifact production. It
does not change the current publisher or any generated artifact.

## One semantic path

Proposed synchronization:

```text
authoritative sources
→ load immutable snapshot
→ compile normalized state
→ validate state
→ project complete candidate artifact set
→ validate candidate set
→ synchronize maintained artifacts
```

Proposed checking:

```text
authoritative sources
→ load immutable snapshot
→ compile normalized state
→ validate state
→ project complete candidate artifact set
→ compare with maintained artifacts
```

The same loader, compiler, validator, and projector would serve both operations.
`HarnessStateComparator` would compare exact artifacts and normalized semantic
state where appropriate, but would have no publication dependency or write
capability.

## Compilation boundary

`HarnessRepositoryLoader` would own explicit repository I/O and would return a
closed `HarnessSourceSnapshot`. `HarnessCompiler` would receive only that
snapshot, normalize identifiers and relationships, and return `HarnessState`.
It would not read the repository, invoke CLIs, publish files, or treat generated
projections as source inputs.

Compilation would preserve provenance from normalized values back to source
artifacts so a validation finding can name its authority source. It would not
retain mutable parser nodes, open SQLite connections, or temporary files in
`HarnessState`.

## Validation boundary

Domain validators would own domain rules: Task catalog, graph, checkpoint,
resource, evidence, capability, and generated-artifact invariants. Validation
composition would own deterministic ordering and cross-domain closure only.
This avoids a single validator becoming both domain authority and orchestration
fallback.

The proposed `ValidationResult` would state its exact claim boundary. Structural
success would not establish software test success, numerical verification,
scientific validation, uncertainty quantification, protected authorization, or
human acceptance.

## Projection boundary

`HarnessProjector` would map one validated `HarnessState` to one complete
`HarnessArtifactSet`. Projector-owned formats may include SQLite, deterministic
SQL, generated Task Markdown, indexes, and a projection manifest. A format is an
output strategy, not a separate authority model.

Projector requirements proposed for later implementation are:

- deterministic bytes from equivalent normalized state;
- complete output closure known before publication;
- no writes to maintained destinations;
- no source discovery;
- no action authorization;
- no partial projection presented as current; and
- explicit generated-artifact identities.

`HarnessSynchronizer` would own maintained publication, rollback, and stale
publisher-owned artifact handling. It would accept only a complete validated
artifact set. The projector would not publish, and the synchronizer would not
recompile policy.

## Current-to-target responsibility map

The map reflects current `origin/dev`; dispositions are planning recommendations,
not permission to edit.

| Current responsibility | Current owner/surface | Proposed target owner | Disposition | Reason |
|---|---|---|---|---|
| Control synchronization | `HarnessControlMigrator` | `HarnessSynchronizer` over compiled/projected state | `split_later` | Current owner combines request, generation validation, and publication |
| Source-aware control checking | `HarnessControlVerifier` | loader/compiler/validator/projector + `HarnessStateComparator` | `split_later` | Preserve one check operation while separating semantic owners |
| Repository validation composition | `HarnessValidator` | validation composition over explicit domain validators | `split_later` | Keep aggregation, move no domain rule into fallback composition |
| Candidate generation orchestration | private `local.control.generation` | `HarnessCompiler` + `HarnessProjector` | `split_later` | Compilation and projection currently share one builder |
| Canonical input resolution | private `local.control.inputs` | `HarnessRepositoryLoader` configuration | `rename_later` | Retain explicit canonical selection under snapshot ownership |
| Source-aware comparison | private `local.control.verification` | `HarnessStateComparator` | `rename_later` | Existing read-only comparison direction is useful |
| SQLite persistence mechanics | `local.dbcontrol` | private projector/synchronizer SQLite implementation | `split_later` | Tables and files should not define public architecture |
| Task-state bounded inspection | `TaskStateInspector` and dbcontrol reader | live-state query over explicit `HarnessState` | `replace_later` | Current query couples chain, Task documents, and SQLite projection |
| Resource validation | resource DataObjects/Actions and local adapters | `HarnessResourceCatalog` validator | `retain` | Existing distinct domain behavior remains meaningful |
| Python evidence validation | `PythonConformanceValidator` | evidence-domain validator consumed by composition | `retain` | Separate domain claim and existing maintained contract |
| Checkpoint validation | checkpoint records/validator/local composition | unresolved-decision domain validator | `merge_later` | Live plane needs unresolved decisions, not all historical records |
| Task handling | `HarnessTaskDeserializer`, Task projections | `HarnessTaskCatalog` compiler/validator | `replace_later` | Normalize live Task state without generated Markdown authority |
| Graph handling | `HarnessTaskGraphValidator`, `harness/task-graph.json` | `HarnessTaskGraph` compiler/validator | `replace_later` | Operational graph should be normalized, with JSON as projection if retained |
| Generated Task documentation | `_ControlProjector` | one projector strategy within `HarnessProjector` | `merge_later` | Avoid a parallel Task-document authority |
| SQLite projection | `_ControlProjector`/dbcontrol schema | private SQLite projector | `replace_later` | Enforce immutable projection lifecycle |
| SQL projection | `_ControlDatabase.deterministic_sql_export` | private SQL projector | `retain` | Deterministic recovery/inspection output remains useful |
| Projection manifest | `_ControlProjector` | `HarnessArtifactSet` manifest projection | `rename_later` | Preserve complete set identity under generated-state model |
| `harness_control.py sync/check` | maintained CLI | one future operator/command surface | `replace_later` | Preserve operations, not necessarily current argument shape |
| `validate_harness.py` | maintained CLI | validation action exposure | `retain` | Distinct repository validation remains useful |
| `inspect_task_state.py` | maintained CLI | normalized-state read action | `replace_later` | Preserve bounded inspection through new state boundary |
| Domain validation CLIs | 10 additional maintained CLIs | explicit developer capabilities or library calls | `unresolved` | Need actual operator profiles and downstream-use evidence before consolidation |
| Current generated control projections | SQLite, SQL, Task Markdown, manifests, graph | `HarnessArtifactSet` | `merge_later` | One artifact-set owner, multiple deterministic formats |
| Historical compatibility facades | retained dbcontrol facades/adapters | none after demonstrated parity | `delete_after_migration` | Pre-alpha migration need not preserve incidental internal structure |

### Disposition counts

| Disposition | Count |
|---|---:|
| `retain` | 5 |
| `rename_later` | 3 |
| `split_later` | 5 |
| `merge_later` | 4 |
| `replace_later` | 7 |
| `delete_after_migration` | 1 |
| `unresolved` | 1 |
| **Total** | **26** |

No current source is changed by this map. Exact deletion or compatibility
choices remain contingent on later parity and downstream-use evidence.
