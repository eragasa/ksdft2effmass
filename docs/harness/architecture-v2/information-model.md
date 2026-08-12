# Architecture v2 information model

> **Proposed architecture; inactive; not implemented; not accepted.**

The following is a small candidate object model, not a frozen API or permission
to add modules.

## Source and normalized state

| Candidate object | Meaningful proposed ownership |
|---|---|
| `HarnessSourceArtifact` | Immutable bytes, canonical source identity, source kind, and content identity for one explicitly selected authority input |
| `HarnessSourceSnapshot` | One complete immutable observation $R$ with snapshot-level uniqueness and closure invariants |
| `HarnessTaskCatalog` | Live Task identity uniqueness and lifecycle eligibility for active, prospective, and resumable Tasks |
| `HarnessTaskGraph` | Operational relationships and graph invariants only |
| `HarnessSelectionState` | Explicit current selection independent of Task definitions |
| `HarnessActivation` | At most one active authorization, its authority, scope, and permitted transitions |
| `HarnessCapabilityCatalog` | Available agents, skills, and actions for composition; immutable during one operator run |
| `HarnessEvidenceCatalog` | Evidence declarations and claim classes, separate from authorization |
| `HarnessResourceCatalog` | Generic and project-local resource identities and permitted dependency direction |
| `HarnessState` | Cohesive normalized composition $S$, including cross-catalog identity closure without absorbing every domain invariant |

`HarnessSourceArtifact` would not imply one class per source format.
`HarnessSourceSnapshot` would own the observation boundary so compilation does
not repeatedly rediscover repository content. Catalogs would own cohesive domain
invariants rather than mirror individual files or SQLite tables.

## Generated and result state

| Candidate object | Meaningful proposed ownership |
|---|---|
| `HarnessGeneratedArtifact` | One generated path, kind, deterministic bytes, and content identity |
| `HarnessArtifactSet` | Complete unique output set and projection closure for one normalized state |
| `ValidationFinding` | One stable domain finding with severity and subject identity |
| `ValidationResult` | Deterministically ordered findings, status, and stated claim boundary |
| `HarnessSynchronizationResult` | Publication outcome, replaced paths, and rollback status; a ResultObject, not authority |

ResultObjects would be semantic DataObjects. Nominal `ResultObject` inheritance
would not be required.

## Actions

| Candidate action | Proposed responsibility |
|---|---|
| `HarnessRepositoryLoader` | Read explicitly selected authoritative sources once and return `HarnessSourceSnapshot` |
| `HarnessCompiler` | Deterministically normalize one snapshot into `HarnessState` |
| `HarnessValidator` | Compose domain validation and cross-domain validation over immutable state |
| `HarnessProjector` | Produce complete deterministic candidate `HarnessArtifactSet` without publication |
| `HarnessStateComparator` | Compare candidate and maintained artifacts; never publish |
| `HarnessSynchronizer` | Publish one validated complete artifact set and return a non-authoritative result |

The candidate public ActionObjects would be stateless with explicit inputs.
Filesystem reads belong to the loader, candidate writes to projector-owned
temporary workspace mechanics, and maintained publication to the synchronizer.
The compiler and validators would not discover files. The comparator would never
call the synchronizer.

## Proposed state relationships

```text
HarnessSourceSnapshot
  ├── source artifacts
  └── observation identity
          ↓ compile
HarnessState
  ├── Task catalog + Task graph + selection + activation
  ├── capability catalog
  ├── evidence catalog
  └── resource catalog
          ↓ validate/project
HarnessArtifactSet
  └── generated artifacts
```

A source artifact, normalized domain object, and generated artifact would remain
distinct even when all refer to similar content. Generated Markdown would not
be loaded back as Task authority. SQLite tables would not define the normalized
object model.

## Extension evaluation

Concrete immutable objects are provisionally preferred where extraction and
downstream reuse need stable explicit data. Private owners are provisionally
preferred for algorithms that have only one implementation. Protocols would be
considered only after real validator or projector families demonstrate
interchangeability. Unrestricted subclass/plugin extension is not recommended.
These choices remain proposed and need later human acceptance before public API
work.

## Unresolved contract details

Planning intentionally does not freeze:

- module names or exact stable import paths;
- serialization or wire formats;
- whether Task/evidence/resource catalogs share small private collection
  mechanics;
- validation finding codes and severity vocabulary;
- synchronization receipt shape;
- protocol use for validators or projectors; or
- compatibility policy for any current pre-alpha public harness object.

Those decisions require evidence from extraction or a separately activated
implementation slice, not speculation in this planning Task.
