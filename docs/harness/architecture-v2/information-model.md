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

## Governed-operation responsibilities

The proposed [operation lifecycle](operation-lifecycle.md) needs responsibilities
for an operation request, repository and execution context, preflight result,
implementation receipt, verification result, review request/result, human
decision, and operation lifecycle state. These are information boundaries, not
a frozen list of public classes. Existing DataObjects, `LocalValidationResult`,
`ValidationResult`, and other ResultObjects should be reused where sufficient;
Architecture v2 must not manufacture one class for every lifecycle state.

The lifecycle keeps execution recording separate from correctness and
acceptance. An implementation receipt records candidate changes or outputs. A
verification result evaluates declared deterministic requirements. A read-only
review result is conditional and grants no mutation authority. A human decision
is represented only when the operation's declared claim boundary requires it.

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

## Repository execution context

The following proposed public concepts make repository ownership explicit. They
are candidate contracts only and are not implemented.

| Candidate concept | Meaningful proposed ownership |
|---|---|
| `RepositoryContext` | Immutable observation of repository execution context for one explicit root |
| `RepositoryContextRequirement` | Immutable statement of only the context conditions required by one operation |
| `ObserveRepositoryContext` | Read-only ActionObject that observes context from an explicit repository root |
| `ValidateRepositoryContext` | Read-only ActionObject applying one requirement to one observed context and returning `LocalValidationResult` |

Candidate `RepositoryContext` semantics include the canonical repository root,
worktree-specific Git directory, Git common directory, HEAD revision, invocation
directory as diagnostic information, and dirty state as diagnostic information
or an explicitly requested constraint. The contract would not freeze a field
until a demonstrated operation justifies it.

Candidate `RepositoryContextRequirement` conditions include an expected
canonical root, expected worktree Git directory, expected starting revision,
permitted dirty-state policy, exact authoritative input identities, and an
optional control digest only when control state is genuinely an input. It would
not become a global session digest or collect conditions irrelevant to an
operation.

`ObserveRepositoryContext` would receive an explicit root, canonically resolve
and confine repository paths beneath it, and use root-qualified Git operations.
It would not discover a repository from ambient `cwd`; the invocation directory
could be retained only as a diagnostic observation.

`ValidateRepositoryContext` would implement:

```text
RepositoryContextRequirement
+ RepositoryContext
→ LocalValidationResult
```

It would use existing structured findings, including the proposed stable finding
`HARNESS.CONTEXT.WORKTREE_MISMATCH`. No new ResultObject is proposed because
`LocalValidationResult` has not been shown to be insufficient.

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
- validation finding codes and severity vocabulary beyond the demonstrated
  `HARNESS.CONTEXT.WORKTREE_MISMATCH` proposal;
- exact fields or serialization for repository-context concepts;
- protocol use for validators or projectors; or
- compatibility policy for any current pre-alpha public harness object.

Those decisions require evidence from extraction or a separately activated
implementation slice, not speculation in this planning Task.

## Deferred operation observation

Operation transitions and ResultObjects may feed optional operation receipts and
only later a telemetry projection. A later, explicitly deferred concept may
compose existing outcomes without participating in correctness:

```text
Action ResultObject
+ starting RepositoryContext
+ ending RepositoryContext
→ HarnessOperationReceipt
```

A candidate receipt may eventually retain an opaque operation ID, optional
session correlation ID, Action identity, starting and ending contexts, outcome,
existing structured findings, diagnostic monotonic duration, and implementation
version. It would not grant authority, replace validation, redefine findings, or
be required for safe Action execution.

Receipt and persistence design remains unresolved pending inspection of Pi's
actual session records: which relevant events Pi already stores; whether extra
harness events are needed; session and subagent correlation; JSONL versus one
JSON file per operation; usefulness of a local SQLite query projection;
retention and deletion policy; a privacy allowlist; recurrence analysis; and
whether any tracked failure-pattern catalog is justified. Telemetry would
observe execution only; it would not authorize transitions, replace validation,
or automatically create Tasks or checkpoints.

The proposal does not prematurely specify a closed failure taxonomy, tracked
occurrence counts, tracked “most recent” timestamps, automatic failure
promotion, automatic checkpoint or Task creation, or a second authoritative
database.
