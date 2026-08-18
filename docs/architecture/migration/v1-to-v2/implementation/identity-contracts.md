# Identity, version, immutable-result, and failure contract migration plan

## Status and identity

**Foundational implementation: human-accepted and closed under Option B.** The
canonical Task is `migration.v2.identity-contracts`. The resolved checkpoint
preserves the architecture response `B accepted`; the canonical Task lifecycle record
preserves the implementation activation and later human acceptance. No second
checkpoint was created
because no material alternative remained. Option B deliberately requires no
foundational runtime module, shared schema, fixture, or dependency. Concrete consumer
implementation, protected execution, successor activation, and human acceptance of
later consumer results remain unauthorized.

The normative semantic baseline is [Identity, version, and failure
contracts](../../../v2/identity-version-and-failure-contracts.md). The package
ownership transition is owned by the [package and module
crosswalk](../package-module-crosswalk.md). This page records implementation
planning without creating a second Task graph. The resolved ownership decision is
recorded by the applicable durable checkpoint.

## V1 source responsibilities

Current implemented identity and failure behavior is distributed among domain
owners rather than one shared runtime package.

| Current owner | Implemented responsibility | Compatibility significance |
|---|---|---|
| `ksdft2effmass.harness.identity` | Public `ContentIdentity` and `SnapshotIdentity` values used by the accepted v2 Harness configuration boundary | Both are fixed to schema version 1, `sha256`, and 64 lowercase hexadecimal characters |
| `ksdft2effmass.harness.pi.identity` | V1 Harness lexical aliases and validators, public byte-oriented `ArtifactIdentity`, and `HarnessInternalError` | The public wire and fixtures are accepted v1 compatibility surfaces |
| `ksdft2effmass.provenance.records` | Public sealed-artifact `ArtifactIdentity` containing logical artifact identity, SHA-256 digest, and byte size | It is not representation-compatible with the Harness `ArtifactIdentity` of the same class name |
| `ksdft2effmass.provenance.external_tools` and `.external_execution` | Tool, request, attempt, authorization, result, failure-stage, and failure-code values | These are domain records, not a root failure hierarchy |
| Record and wire owners throughout the package | Record-specific `schema_version` checks and domain-specific closed results | Version support and wire rejection remain with the represented record owner |

Direct consumers of `harness.pi.identity` include the v1 Harness Task, checkpoint,
configuration, resource, ownership, profile, validation, DB-document, wire, and
project-local migration modules. The accepted v2 configuration code directly
consumes `ContentIdentity` and `SnapshotIdentity`. Any cutover must therefore
inventory public imports, wire codecs, fixtures, error codes, and direct consumers;
an equal field shape does not establish equal meaning.

The two public `ArtifactIdentity` classes are intentionally treated as distinct:

- `harness.pi.ArtifactIdentity` identifies exact represented bytes by version,
  algorithm, and digest; and
- `provenance.ArtifactIdentity` identifies one sealed artifact by logical identity,
  digest, and byte size.

Neither may silently alias, replace, or deserialize as the other.

## Target concern and exclusions

The accepted v2 baseline already requires:

- distinct logical, revision, content, snapshot, operation, attempt, authority,
  obligation, and result identities;
- exact version binding with no ambient substitution of “latest”;
- immutable results and closed outcome variants;
- no fabricated identity for a phase that never began;
- new attempt identity for every retry;
- exact correlation and reconciliation identities for indeterminate effects; and
- explicit claim boundaries that do not imply scientific validity or authority.

This Task must stabilize those cross-package rules without absorbing domain-owned
identity fields, validation, persistence, serialization, scientific meaning, or
failure-code catalogs.

### Exclusions

The shared contract owns no:

- universal base class for all identities, results, or failures;
- nullable result aggregate spanning unrelated domains;
- generic serializer or repository;
- scientific operator, basis, gauge, energy-reference, unit, or geometry meaning;
- Task activation, execution grant, protected-operation authority, or acceptance;
- automatic conversion between the two current `ArtifactIdentity` contracts; or
- consumer implementation that belongs to Harness, persistence, Petri-net,
  Workflow, calculator, integration, or analysis Tasks.

## Containment decomposition

`migration.v2.identity-contracts` is one leaf Task beneath `migration.v2`; it has
no canonical child Tasks. Planning is decomposed into concerns within this Task,
not additional lifecycle Tasks:

1. identity-class and owner inventory;
2. accepted cross-package invariant baseline;
3. runtime ownership and public-compatibility decision;
4. exact post-decision implementation plan;
5. compatibility and software-verification contract; and
6. prerequisite receipt for consuming Tasks.

Downstream consumers remain owned by their existing Tasks, including
`migration.v2.harness.*`, `migration.v2.persistence.store`,
`migration.v2.petrinet.colored.values`, and `migration.v2.workflows.model`.

## Planning cascade

Planning may inspect all prospective consumers without activating them. For each
identity named by the normative v2 page, the implementation-planning inventory
must record:

- semantic owner and identity class;
- producer and consumers;
- derivation inputs and named algorithm where applicable;
- schema, definition, implementation, and normalization version bindings;
- persistence and wire owner;
- retry, reconciliation, and predecessor behavior;
- v1 or already-implemented v2 counterpart; and
- retain, transform, introduce, or retire disposition.

The inventory is planning input only. Consumer implementation waits for this
Task's accepted contract result and each consumer's own activation and prerequisite
facts.

### Option B ownership and conformance matrix

| Identity or result family | Nominal runtime owner | Required shared agreement |
|---|---|---|
| Harness Task, decision, configuration, resource, validation, compilation, projection-generation/publication, development operation/attempt/result, and development snapshot identities | `ksdft2effmass.harness` | Identity classes remain distinct; exact source/content/snapshot correlation; no selection, compilation, projection, or validation result grants authority |
| `HarnessStateIdentity`, development-authority-ledger identities, and development-operation-authorization-result identities | `ksdft2effmass.harness` | Normalized aggregate identity excludes protected authority/operation identities; protected authority state remains separate from ordinary Harness revision storage and Workflow execution authority |
| Workflow, WorkflowRun, runtime-bundle, replay-result, Task-definition/instance/gate/activation, operation, attempt, invocation-outcome, nested-invocation, ResultObject, grant, scientific-authority-snapshot, authorization-result, and obligation identities | `ksdft2effmass.workflows` | No ambient latest version; closed confirmed/rejected/indeterminate variants; new retry identities; exact authority and reconciliation correlation |
| Scientific `ArtifactManifest`, manifest-entry, artifact, producer-provenance-variant/revision, normalized-observation-set, and result/artifact-relation identities | `ksdft2effmass.workflows` | Exactly one closed producer-provenance variant; content/checksum/byte-count agreement; no fabricated Workflow lineage for external, fixture, human-authored, or legacy producers |
| Colored-Petri-net definition, marking, enablement-result, selection-result, directive, and firing-result identities | `ksdft2effmass.petrinet.colored` | Pure deterministic derivation; exact definition/marking/result closure; stale or mismatched identities reject firing |
| Revision, revision-read request/result, commit, idempotency, stream, schema, and store-implementation identities | `ksdft2effmass.persistence.store` | Opaque domain-neutral storage; exact compare-and-swap/idempotency closure; found/absent/mismatch/incompatible/corrupt/indeterminate/error remain distinct |
| Calculator input/output, executable-configuration, process-request/observation, and executor-protocol identities | `ksdft2effmass.calculators` | Exact input/output and implementation versions; no concrete integration identity becomes calculator authority |
| QE-native serialization, workspace, process, capture, discovery, parser, adaptation, and concrete failure-mapping identities | `ksdft2effmass.integration.quantumespresso` | Exact adaptation to calculator, Workflow, periodic, and Kohn–Sham contracts; no reverse integration dependency |
| Periodic, Kohn–Sham, and analysis identities | Their respective `periodic`, `ksdft`, and `analysis` owners | Units, coordinates, energy references, tolerances, implementation versions, and evidence classes remain explicit and domain-owned |
| `ContentIdentity` and `SnapshotIdentity` meanings | The owner of the identified bytes, canonical content, or closed snapshot | Same names do not imply one Python type; any boundary comparison names the algorithm, represented content, producer, and applicable version explicitly |

Shared conformance is semantic rather than inheritance-based. It requires exact
agreement only where two owners exchange or correlate values. It does not require
every domain to accept one identifier grammar, digest algorithm, failure-code enum,
or serialized member order.

### Normative per-identity inventory

Exact lexical derivation algorithms and wire members remain deferred where the
normative architecture defers them. “Binds” below identifies required semantic input,
not a selected encoding.

| Normative identity | Owner; producer and principal consumers | Required binding, version, persistence, and lifecycle disposition |
|---|---|---|
| `WorkflowIdentity` | `workflows`; authored/composed by `campaigns` or `application`, consumed by Workflow control, runs, replay, and provenance | Binds one reusable definition and its schema/definition versions; Workflow-owned persistence/wire; no v1 public counterpart, introduce |
| `WorkflowRunIdentity` | `workflows`; allocated by Workflow control, consumed by repositories, replay, nested invocation, results, and provenance | Binds one run independently of revision identity; Workflow persistence/wire; immutable identity across revisions; no fabricated historical counterpart, introduce |
| `WorkflowRuntimeBundleIdentity` | `workflows`; composed explicitly by `application`, consumed by `WorkflowRunReplayer` | Binds exact definitions, evaluators, adapter, schemas, normalization, and implementation versions; Workflow persistence/wire; immutable bundle, introduce |
| `WorkflowRunReplayResultIdentity` | `workflows`; produced by `WorkflowRunReplayer`, consumed by Workflow service and repositories | Binds exact run revision and runtime bundle plus replayer version; Workflow persistence/wire; one closed replay result, introduce |
| `TaskDefinitionIdentity` | `workflows`; authored/composed by campaign/application inputs, consumed by Workflow definitions and Task instances | Binds reusable scientific Task contract and schema/version; Workflow persistence/wire; distinct from development `HarnessTask`, introduce |
| `TaskInstanceIdentity` | `workflows`; produced by Workflow control, consumed by gates, activation, dispatch, outcomes, results, and provenance | Binds one run-scoped instance and exact Task definition; Workflow persistence/wire; new instance where the run contract requires it, introduce |
| `TaskStartGateSetIdentity` | `workflows`; produced with immutable Workflow composition policy, consumed by activation | Binds exact `any_of`/`all_of` mode, ordered members, and policy version; Workflow persistence/wire; absent for direct activation, introduce |
| `TaskActivationIdentity` | `workflows`; produced by the Workflow adapter/control boundary, consumed by invocation, dispatch, firing, and provenance | Binds Task instance, generic selection result, inputs, run, operation, attempt, and exactly one direct/any_of/all_of discriminant; Workflow persistence/wire; retry creates a new activation, introduce |
| `OperationIdentity` | The operation-owning domain; scientific Task invocation is `workflows`, development operation is `harness` | Binds one intended operation and applicable contract/implementation versions; owner persistence/wire; retry or new execution uses a new identity; current v1 request/correlation fields require owner-specific migration |
| `AttemptIdentity` | The attempt-owning domain; Workflow invocation is `workflows`, development attempt is `harness`, concrete process observation is owned by its calculator/integration boundary | Binds one bounded attempt, operation, predecessor attempt when applicable, and implementation version; owner persistence/wire; never reused for retry; map actual v1 attempt fields without aliasing domains |
| `TaskInvocationOutcomeIdentity` | `workflows`; produced by Workflow control, consumed by firing, result ingress, reconciliation, and persistence | Binds activation, operation, attempt, outcome variant, and Workflow implementation version; Workflow persistence/wire; one effective confirmed/rejected/indeterminate outcome, introduce |
| `NestedWorkflowInvocationIdentity` | `workflows`; produced by parent Workflow control, consumed by child creation, reconciliation, and parent admission | Binds parent run/revision/Task/activation/operation/attempt, child definition/run, inputs, and idempotency identity; Workflow persistence/wire; uncertainty retains the same identity and never duplicates automatically, introduce |
| `ResultObjectIdentity` | `workflows` defines the workflow-facing contract; concrete result type remains with its Task/calculator/analysis owner | Binds one immutable concrete result, producer provenance, schema/type, and applicable implementation version; referenced by Workflow persistence/manifests; retries never rewrite predecessor results; no generic v1 counterpart, introduce |
| `ColoredPetriNetDefinitionIdentity` | `petrinet.colored`; produced with one generic definition, consumed by validation, enablement, selection, firing, adapter, and replay | Binds exact definition plus expression/ordering/schema versions; Petri-net owner defines wire, Workflow stores references; v1 CPN definition mapping requires compatibility evidence |
| `ColoredPetriNetMarkingIdentity` | `petrinet.colored`; produced for one semantic marking, consumed by enablement, firing, WorkflowRun, and replay | Binds semantic multiset, definition/value representation, and ordering versions; Petri-net wire with Workflow references; v1 marking mapping requires semantic-order evidence |
| `ColoredPetriNetEnablementResultIdentity` | `petrinet.colored`; produced by enabler, consumed by selector, firing, and Workflow adapter | Binds exact definition, marking, enabled set, expression, enabler, and ordering versions; Petri-net result wire; stale identity rejects downstream use, introduce from v1 enablement behavior |
| `ColoredPetriNetSelectionResultIdentity` | `petrinet.colored`; produced by selector, consumed by firing and Workflow activation/decision origins | Binds exact enablement result, selected transition/binding, optional directive, selector, and ordering versions; Petri-net result wire; one canonical or permitted-directed result, introduce |
| `SnapshotIdentity` | Domain whose closed snapshot is represented; current configuration snapshot is `harness`, Workflow and authority snapshots remain with their owners | Binds exact closed source set/state plus normalization/resolver/contract versions; owner persistence/wire; same name across domains is not nominal interchange; retain current Harness type and introduce only demonstrated domain types |
| `ContentIdentity` | Domain owning the identified bytes or canonical represented content | Binds exact subject, named algorithm, canonicalization version when applicable, and digest/content value; stored/referenced by owner; equality never proves compatibility; retain current Harness type and adapt explicit provenance/checksum fields |
| `RevisionReadRequestIdentity` | `persistence.store`; produced by a domain repository, consumed by `AtomicRevisionStore` and reconciliation | Binds stream, latest/explicit selector, optional complete expectation set, and store-contract version; persistence wire; one immutable read request, introduce |
| `RevisionReadResultIdentity` | `persistence.store`; produced by `AtomicRevisionStore`, consumed by domain repositories | Binds request, stream, selector, store implementation/version, closed variant, diagnostics, and claim boundary; persistence wire; one found/absent/mismatch/incompatible/corrupt/indeterminate/error observation, introduce |
| `ExecutionGrantIdentity` | `workflows`; externally issued by the trusted authority boundary, consumed by authorization, reservation, claim, dispatch, and reconciliation | Binds one exact dispatch scope, issuer/source evidence, validity, and authority-contract version; Workflow stores grant reference/state evidence, not issuance authority; retry requires a new grant, introduce |
| `ScientificExecutionAuthoritySnapshotIdentity` | `workflows` owns the verified snapshot record consumed by its authorizer; trusted source remains external | Binds source/issuer, trust configuration, content/authentication checks, predecessor/revocation closure, validity/freshness, and resolver version; Workflow persistence/wire; immutable verified view, introduce |
| `SimulationExecutionAuthorizationResultIdentity` | `workflows`; produced by `SimulationExecutionAuthorizer`, consumed by request preparation, reservation/claim, executor check, and persistence | Binds operation phase, grant state, authority snapshot, dispatch inputs, authorizer version, and authorized/denied/error variant; Workflow persistence/wire; only authorized may proceed, introduce |
| `ObligationIdentity` | `workflows`; produced with durable dispatch preparation, consumed by reservation, claim, dispatch, ingress, disposition, and reconciliation | Binds exact request/activation/attempt/grant scope and Workflow contract version; Workflow persistence/wire; retained through indeterminate reconciliation and replaced for retry/new execution, introduce |

This inventory assigns every identity named by the normative v2 contract. Concrete
consumer Tasks refine only their owner-local fields, lexical forms, and wires without
changing these owners or correlation requirements.

### Version and failure ownership matrix

| Concern | Owner under Option B | Required behavior |
|---|---|---|
| Record or schema version | The record and serializer owner | Exact supported versions; unsupported input fails closed; no substitution of latest |
| Definition, expression, ordering, normalization, adapter, calculator, or implementation version | The ActionObject or definition owner | Exact version identity is bound into the produced result when required by its contract |
| Stable operational failure code | The operation's domain owner | Closed code set, operation phase, sanitized diagnostic, retryability only when known, and applicable exact identities |
| Closed operation outcome | The ActionObject or Workflow that performs the operation | Variant-specific fields only; rejected or indeterminate outcomes contain no invented success result |
| Unexpected programming failure | The local implementation boundary | Exception distinct from represented operational failure; no fabricated domain outcome |
| Scientific or numerical inadequacy | The scientific analysis or evidence owner | Never collapsed into a generic software failure code or inferred from process success |

## Implementation approach

### Accepted invariant baseline

First encode the already-selected semantic rules as a bounded contract matrix. The
matrix must distinguish nominal identity meaning from lexical representation and
must distinguish a structured domain failure from an unexpected programming error.
It must not infer interchangeability from a shared `str`, integer, digest, or field
shape.

### Post-decision source boundary

Under accepted Option B, define exact implementation paths only for normative
contract and conformance artifacts; do not create a shared runtime package. In this
model:

- concrete domain DataObjects retain their semantic identity names;
- closed outcomes remain with the operation that produces them;
- serializers and schemas remain with the represented domain contract;
- stable failure codes are domain-owned and versioned;
- unsupported versions produce closed represented failures where the owning
  operation has such a result boundary; and
- unexpected programming failures remain distinct from represented operational
  failures.

Option B introduces no foundational production module. This Task's implementation
artifact is the accepted normative contract, migration plan, compatibility matrix,
and cross-package verification plan. Concrete runtime types and tests are implemented
only by separately selected consumer Tasks.

### Cross-domain adaptation boundaries

| Boundary | Adapter or composition owner | Required identity behavior |
|---|---|---|
| Harness repository → shared revision store | `harness.persistence` | Map Harness-owned transaction/snapshot/schema/content identities into persistence-owned revision and commit values; preserve the nested generic result identity |
| Workflow repository → shared revision store | `workflows.persistence` | Perform the equivalent explicit mapping for WorkflowRun without making persistence import Workflow types |
| Workflow control → generic Petri net | `workflows` through `ColoredPetriNetWorkflowAdapter` | Map Workflow reasons and values into Petri-net-owned enablement, selection, and firing inputs; retain the exact generic result identities; forbid reverse imports |
| Workflow dispatch → calculator executor protocol | `workflows` with calculator-owned protocol values | Preserve activation, operation, attempt, grant, obligation, request, and returned ResultObject correlation without importing concrete integration behavior |
| Concrete QE integration → calculator/Workflow/observation contracts | `integration.quantumespresso` | Adapt concrete native/process identities into consumer-owned records; do not reinterpret content equality as scientific equivalence |
| V1 provenance records → Workflow artifact/provenance model | `workflows` through `migration.v2.workflows.artifacts-provenance` | Inventory fields and consumers, construct the applicable closed Workflow-owned manifest/provenance variant, preserve actual legacy limitations, and never alias the current provenance `ArtifactIdentity` to a Workflow identity merely because both name an artifact |
| Application composition → all domain operations | `application` | Construct and inject exact implementations; do not define substitute domain identities or silently coerce them |
| Pi request/result transport → application operation | `pi.agents` | Perform outer typed adaptation only; preserve application/domain result and failure meaning without granting authority |

There is no generic cross-domain adapter registry. Each adapter is owned by the
outward consumer that understands both its own contract and the inward dependency.

### Public compatibility inventory

Before implementation, assign an explicit disposition to:

- `ksdft2effmass.harness.ContentIdentity`;
- `ksdft2effmass.harness.SnapshotIdentity`;
- `ksdft2effmass.harness.pi.ArtifactIdentity`;
- `ksdft2effmass.provenance.ArtifactIdentity`;
- v1 Harness identifier, path, and version aliases;
- `HarnessInternalError`; and
- current record-specific schema-version checks.

The accepted Harness configuration identities remain supported unless a separate
human-approved compatibility change says otherwise. The provenance artifact record
retains its richer domain meaning. Transitional v1 Harness surfaces retire only
after all retained consumers and wire contracts have an explicit disposition.

| Existing surface | Option B disposition |
|---|---|
| `ksdft2effmass.harness.ContentIdentity` | Retain as the Harness-owned exact-source-content identity used by configuration |
| `ksdft2effmass.harness.SnapshotIdentity` | Retain as the Harness-owned resolved-configuration snapshot identity |
| `ksdft2effmass.harness.pi.ArtifactIdentity` | Retain unchanged as a v1 Harness wire contract until every retained Harness consumer is migrated; do not re-export it as another domain's artifact identity |
| `ksdft2effmass.provenance.ArtifactIdentity` | Retain its logical artifact ID, SHA-256, and byte-size meaning during migration. `migration.v2.workflows.artifacts-provenance` owns the field-by-field adaptation into Workflow-owned `ArtifactManifest` entries and closed producer-provenance variants. Do not alias the class or silently discard byte size, logical identity, source evidence, or limitations; retire the v1 surface only after every consumer has an explicit migrated or retained disposition |
| V1 Harness `Identifier`, path, and `Version` aliases | Retain for v1 consumers; new v2 domains define only their own demonstrated lexical contracts |
| `HarnessInternalError` | Retain as a v1 unexpected-programming/runtime exception; do not use it as the root structured operational failure |
| Record-local `schema_version` validation | Retain with each record/wire owner; shared conformance checks no-ambient-latest and fail-closed behavior rather than one numeric range |

### Exact future artifact and path plan

| Artifact | Exact path or owner | Disposition |
|---|---|---|
| Normative semantic contract | `docs/architecture/v2/identity-version-and-failure-contracts.md` | Remains the sole repository-wide semantic authority; update only when an accepted contract changes |
| Migration implementation plan and matrices | `docs/architecture/migration/v1-to-v2/implementation/identity-contracts.md` | Owned by this Task and completed before implementation closeout |
| Runtime production source owned by this foundational Task | None | Option B deliberately introduces no `contracts`, shared identity, shared result, or shared failure module |
| Existing Harness identities | `python/src/ksdft2effmass/harness/identity.py` | Retain; any behavior change requires separately authorized Harness implementation and public-contract work |
| Shared revision identities/results | `python/src/ksdft2effmass/persistence/store.py` | Future implementation belongs to `migration.v2.persistence.store` |
| Workflow identities/results/failures | `python/src/ksdft2effmass/workflows/` under paths selected by its owning Tasks | Exact internal modules remain deferred to `migration.v2.workflows.*` implementation planning |
| Workflow artifact/provenance identities and legacy adaptation | `python/src/ksdft2effmass/workflows/` under paths selected by `migration.v2.workflows.artifacts-provenance` | Implement the Workflow-owned `ArtifactManifest` and producer-provenance variants; preserve the current provenance surface until consumer migration and compatibility gates pass |
| Petri-net identities/results/failures | `python/src/ksdft2effmass/petrinet/colored/` under paths selected by its owning Tasks | Exact internal modules remain deferred to `migration.v2.petrinet.colored.*` implementation planning |
| Cross-package boundary evidence | `python/tests/software_verification/ksdft2effmass/integration/test__identity_contract_boundaries.py` | Create only after at least two implemented v2 owners expose a real boundary; artifact-owned software verification, not a universal type test |
| Domain identity evidence | The applicable domain's existing software-verification subtree | Each consumer Task owns intrinsic and wire tests for its own nominal types |
| Shared wire schema or canonical fixture | None selected | Create no shared schema/fixture until an exact cross-package wire or lexical contract is separately accepted |

The absence of a foundational source module is an intentional Option B result, not
missing implementation. This Task exports an accepted contract revision and
compatibility/conformance plan as prerequisite facts; downstream Tasks export the
runtime implementations.

## Prerequisite results

### Planning

Planning requires the accepted v1 snapshot, current source and public-import
inventory, normative v2 identity semantics, package/module crosswalk, and current
Harness configuration contract. These inputs are present.

### Implementation planning

The resolved Option B runtime-ownership decision satisfies the human-owned
planning prerequisite. The ownership, conformance, adaptation, compatibility,
verification, and future-path matrices in this page provide the exact foundational
implementation-planning inventory. Consumer implementation prerequisites do not
alter this completed planning result.

### Implementation

The foundational implementation prerequisites are satisfied: the Option B decision
is resolved, the normative semantic contract and exact compatibility dispositions are
accepted, the documentation-only implementation was explicitly activated, and no
predecessor, dependency, wire, or failure-semantics decision remains open for this
slice. The resulting implementation consists of the normative contract, ownership and
adaptation matrices, compatibility inventory, verification plan, and future artifact
plan maintained by this Task. It creates no source, test, schema, fixture, shared wire,
or dependency artifact. Those artifacts remain with separately activated consumer
Tasks when a demonstrated domain boundary requires them.

## Conditional human decisions

The runtime-ownership decision is resolved as Option B. The accepted architecture
selects semantic separation without a shared nominal Python owner. The alternatives
below are retained as the decision context, not as open choices.

### Option A — minimal shared runtime owner

Introduce a new inward `ksdft2effmass.contracts` package containing only genuinely
cross-domain lexical/version/content/snapshot/failure primitives. Domain packages
retain nominal domain identities, outcomes, serializers, repositories, and failure
catalogs. Existing Harness public identity names require an explicit re-export,
adapter, or versioned-retirement policy.

**Consequence:** adds a package and dependency edges, reduces duplicated primitive
implementation, and makes the shared public lexical contract a compatibility
boundary.

### Option B — structural contract with domain-owned runtime types

Keep the root v2 contract normative and behavioral while each package owns its
nominal Python identity, result, and failure values. Intentional small duplication is
verified through shared conformance cases where exact cross-package agreement is
required. Current Harness identities remain Harness-owned, and composition/wire
boundaries perform explicit correlation rather than relying on nominal type equality.

**Consequence:** adds no inward package or dependency edge and best preserves domain
ownership, but requires disciplined conformance tests and explicit adapters at real
cross-domain boundaries.

### Decision

The human selected **Option B** with the verbatim response `B accepted`. This matches
the accepted prohibition on a universal identity bucket, preserves existing Harness
compatibility, and keeps result, failure, serialization, and scientific meaning with
their domain owners. Shared runtime code may be reconsidered later only if repeated
implementation demonstrates a concrete cross-domain owner that cannot be represented
safely by conformance contracts.

The durable checkpoint
`.pi/checkpoints/migration.v2.identity-contracts.runtime-ownership.json` owns the
resolved response and resulting authorization boundary.

## Verification

### Software verification

This foundational Task introduces no runtime or wire artifact, so it owns no Python,
schema, fixture, or runtime-test change. Its applicable checks are agreement among the
normative contract, ownership and compatibility matrices, migration navigation, and
canonical lifecycle state. The behavioral checks below remain requirements for the
separately activated consumer that implements each demonstrated boundary:

- exact built-in scalar acceptance and Boolean rejection;
- identity-class non-interchangeability;
- immutable value and closed-variant behavior;
- supported and unsupported version handling;
- exact digest spelling and algorithm behavior only where the accepted owner fixes
  them;
- no ambient “latest” resolution;
- no result fields on rejected or indeterminate outcomes;
- no fabricated operation, attempt, producer, or artifact identities;
- new attempt and operation identities for retries;
- exact reconciliation identity preservation;
- stable domain failure codes and sanitized diagnostics;
- compatibility of retained Harness configuration identities;
- explicit non-equivalence of the two `ArtifactIdentity` contracts;
- dependency-direction and public-import agreement; and
- strict round trips only for separately accepted wire contracts.

### Evidence boundary

These checks establish software-contract behavior only. They do not establish
numerical verification, scientific validation, uncertainty quantification,
protected authority, or human acceptance.

## Cutover, retirement, and rollback

Cutover proceeds consumer by consumer:

1. accept the ownership decision and exact contract;
2. implement and verify the selected bounded surface;
3. preserve existing Harness and provenance public identities until their explicit
   compatibility gates pass;
4. migrate each consumer under its own Task;
5. retire only transitional v1 aliases, validators, or codecs with no retained
   consumer; and
6. update migration progress only for accepted repository state.

Before consumer migration, rollback removes only the unaccepted candidate. After a
consumer cutover, rollback restores the last accepted consumer and contract revision
without rewriting retained identities, failures, provenance, or serialized bytes.

## Residual limitations

- Runtime ownership and the foundational Option B implementation are complete; exact
  downstream consumer implementation details remain with their owning Tasks.
- Exact cross-package lexical forms, digest algorithms, canonical encodings, and
  wire schemas remain deferred except for already accepted domain contracts.
- The exact shared conformance-fixture location under Option B is unselected.
- Domain-specific Workflow, Petri-net, persistence, calculator, integration, and
  scientific identity fields remain with their consuming Tasks.
- Current source contains intentionally distinct and partially duplicated identity
  contracts; this plan does not claim they are defects or interchangeable.
- This foundational implementation introduced no production source, dependency
  change, consumer migration, or successor activation; this page does not authorize
  any of those later operations.
