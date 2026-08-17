# Development persistence

## Purpose

Harness persistence is lossless, revisioned storage of the same complete repository-derived `HarnessState`. Repository sources remain authoritative. Persistence provides reconstruction and concurrency control; it does not define another domain aggregate or authorize development work. The shared storage boundary is defined by [shared revision persistence](../persistence/index.md).

## Domain contract

| Object | Responsibility |
|---|---|
| `HarnessStateIdentity` | Identity of the complete normalized aggregate derived from repository sources and normalization versions, excluding authority-ledger and operation identities |
| `HarnessStateSnapshot` | One consistently selected, reconstructed, domain-validated complete revision |
| `HarnessStateLoadResult` | Closed `loaded`/`absent`/`mismatch`/`incompatible`/`corrupt`/`indeterminate`/`error` domain read outcome; only `loaded` contains a snapshot |
| `HarnessStateTransaction` | Expected revision plus one complete candidate successor and binding identities |
| `HarnessStateWriteResult` | Domain outcome mapped from the closed generic commit result without weakening aggregate closure |
| `HarnessStateSerializer` | Aggregate to or from the domain's versioned wire representation |
| `HarnessStateTransactionValidator` | Validate the exact transaction, candidate identity, revision, and aggregate closure |
| `HarnessStateRepository` | Domain-owned structural repository protocol |
| `HarnessStateAtomicRepository` | Concrete repository composed with the shared store, serializer, and validator |

A round trip must preserve every normalized value, relationship, ordering rule, and source-provenance identity required by the aggregate contract, including the canonically ordered sequence of every immutable `DevelopmentDecision` variant/revision and its predecessor/supersession history. Storage layout and physical bytes need not be equal unless the later wire contract requires canonical bytes.

## Composed repository

```mermaid
flowchart LR
    read_request["RevisionReadRequest"] --> repository["HarnessStateAtomicRepository"]
    transaction["HarnessStateTransaction"] --> repository
    validator["HarnessStateTransactionValidator"] --> repository
    serializer["HarnessStateSerializer"] --> repository
    repository --> store["AtomicRevisionStore"]
    store --> read_result["RevisionReadResult"]
    store --> commit_result["CommitResult"]
    read_result --> repository
    commit_result --> repository
    repository --> load_result["HarnessStateLoadResult"]
    repository --> write_result["HarnessStateWriteResult"]
```

`HarnessStateAtomicRepository` is not a passive DAO. It invokes the exact `HarnessStateTransactionValidator` and `HarnessStateSerializer`, binds their subject and bytes to the candidate aggregate, identities, expected revision, and idempotency identity, and only then submits one complete opaque revision. Detached validation cannot validate different bytes or another candidate. The shared store sees only identities and immutable payload bytes.

The repository performs domain transaction-to-bytes/identity binding and preserves aggregate-specific commit closure. On read it submits one explicit latest-or-revision `RevisionReadRequest`, maps every shared variant, verifies the found revision and any reconciliation identities, deserializes through `HarnessStateSerializer`, validates reconstructed aggregate identity and domain closure, and returns one closed `HarnessStateLoadResult`. Only `loaded` contains a snapshot; absence, reconciliation-identity mismatch, shared or domain incompatibility, corruption or deserialization failure, validation failure, indeterminate observation, and operational error remain represented and distinct.

The [shared persistence contract](../persistence/index.md) owns compare-and-swap, idempotency, generic read/commit outcomes, and single-stream atomicity. This domain repository maps those outcomes without weakening or redefining them.

The repository does not choose authority, normalize repository sources, interpret a human response, create a `DevelopmentDecision`, run unrelated domain validators, project views, or repair a successor. Authority-context, authorization-result, requested-operation, and permitted-path identities neither change `HarnessStateIdentity` nor enter the aggregate merely because an authorized operation persists it.

## Storage selection and separation

The initial concrete store and its dependency boundary are selected by the [shared persistence contract](../persistence/index.md). There is no `HarnessStateSQLiteRepository`; the domain repository composes the shared store structurally.

Application composition constructs that repository from the resolved `HarnessPersistenceConfiguration` contained by [`HarnessConfiguration`](configuration.md). Configuration contains immutable construction values only; it does not contain a live store, repository, serializer, validator, connection, credential, or authority grant. Authoritative `DevelopmentDecision` values follow the complete `HarnessState` repository rather than a separately configurable human-decision store.

The development `HarnessState` store/database is separate by default from the scientific `WorkflowRun` store/database. Shared implementation does not imply shared physical storage or cross-stream transactions.

`DevelopmentAuthorityLedger` and `DevelopmentOperationAuthorizationResult` remain separate protected control-plane state and operation evidence with their own identities, authentication/content-verification, and reconstruction requirements. Ordinary shared SQLite revision storage is not selected as its trusted persistence. Immutable projection generations, their identity-bound `SynchronizationResult` records, current-generation pointer publication, recovery markers, and quarantine records are separate derived publication state and never `HarnessState` revisions or reconstruction sources. Successful generation manifests and failed/indeterminate recovery records retain the applicable synchronization-result identity and content; no separate audit repository is introduced.

Conflicting revisions fail closed and are never merged silently. V1 Task status values remain migration inputs and historical evidence; they are not copied into a new lifecycle vocabulary. If a later migration is selected, it must be explicit and deterministic and retain input identity, output identity, and findings without implicitly changing selection, authority, or acceptance.

Persisted harness state excludes credentials, private keys, unrestricted environment content, and external scientific payloads. Cross-plane references use immutable identities rather than shared mutable rows.

## Deferred issues

- Exact HarnessState wire schema and whether canonical bytes are required.
- Exact SQLite schema, connection lifetime, locking/isolation/busy behavior, and failure-code encoding.
- Exact `HarnessStateLoadResult` wire representation.
- Backup, recovery, retention, compaction, and maximum aggregate size.
- Protected `DevelopmentAuthorityLedger` storage, signing, and transport mechanisms.

No migration class, integrity-verifier class, public SQLite configuration/initializer hierarchy, domain SQLite subclass, or extra persistence module split is selected.
