# Compiler architecture

## Purpose

The development-harness compiler converts authoritative repository sources into one normalized model of development state. Validators inspect that model, and projectors derive read-only artifacts from it.

Here, **compiler** means a deterministic source-to-model transformation. It does not mean a Python compiler, a scientific workflow engine, or a calculator input generator.

The compiler architecture has three goals:

1. interpret each authoritative source exactly once;
2. give validation, synchronization, and checking the same normalized state; and
3. prevent generated artifacts from becoming a second source of authority.

## Components

```mermaid
flowchart TD
    sources["Authoritative sources"] --> loader["Repository loader"]
    loader --> load_result["HarnessSourceLoadResult"]
    load_result --> snapshot["HarnessSourceSnapshot"]
    snapshot --> compiler["HarnessCompiler"]
    compiler --> compilation["HarnessCompilationResult"]
    compilation --> state["HarnessState"]
    state --> validators["Domain validators"]
    validators --> validation["State ValidationResult"]

    signature_requirement["DevelopmentTaskSignatureRequirementResult"]
    authority["Optional successful DevelopmentAuthorityContextResolutionResult"]
    state --> project_authorizer["DevelopmentOperationAuthorizer<br/>projection"]
    signature_requirement --> project_authorizer
    authority --> project_authorizer
    project_request["Exact projection inputs"] --> project_authorizer
    project_authorizer --> project_authorization["Projection authorization"]
    state --> projector["HarnessProjector"]
    validation --> projector
    project_authorization --> projector
    projector --> projection_result["HarnessProjectionResult"]
    projection_result --> artifacts["Immutable HarnessArtifactSet"]

    artifacts --> candidate_validator["HarnessArtifactSetValidator"]
    candidate_validator --> candidate_validation["Candidate ValidationResult"]

    artifacts --> sync_authorizer["DevelopmentOperationAuthorizer<br/>synchronization"]
    signature_requirement --> sync_authorizer
    authority --> sync_authorizer
    sync_request["Exact synchronization inputs"] --> sync_authorizer
    sync_authorizer --> sync_authorization["Synchronization authorization"]
    artifacts --> synchronizer["HarnessSynchronizer"]
    candidate_validation --> synchronizer
    sync_authorization --> synchronizer
    synchronizer --> pointer["Current-generation pointer"]

    pointer --> resolver["HarnessProjectionGenerationResolver"]
    resolver --> maintained["Resolved immutable generation"]

    artifacts --> compare_authorizer["DevelopmentOperationAuthorizer<br/>comparison"]
    signature_requirement --> compare_authorizer
    authority --> compare_authorizer
    compare_request["Exact comparison inputs"] --> compare_authorizer
    compare_authorizer --> compare_authorization["Comparison authorization"]
    artifacts --> comparator["HarnessStateComparator"]
    candidate_validation --> comparator
    compare_authorization --> comparator
    maintained --> comparator
```

| Component         | Input                                  | Output                  | Responsibility                                                            |
| ----------------- | -------------------------------------- | ----------------------- | ------------------------------------------------------------------------- |
| Repository loader | Explicit root and source contract | `HarnessSourceLoadResult` | Returns one closed snapshot or an identified load failure with no snapshot. |
| Harness compiler  | `HarnessSourceSnapshot` | `HarnessCompilationResult` | Constructs one complete unique normalized state or fails with no state when normalization is unrepresentable. |
| Domain validators | `HarnessState` | `ValidationResult` | Evaluate representable domain rules without changing state. |
| Development-operation authorizer | Exact state and operation identities plus `DevelopmentTaskSignatureRequirementResult` and, only when required, a successful `DevelopmentAuthorityContextResolutionResult` | `DevelopmentOperationAuthorizationResult` | Resolves the default unsigned or exact signed-gate outcome without changing state or performing the target operation. |
| Harness projector | State, its applicable passing `ValidationResult`, exact affirmative projection authorization, and explicit projection inputs | `HarnessProjectionResult` | Produces one complete candidate set or a represented blocked outcome without projection. |
| Artifact-set validator | Complete `HarnessArtifactSet` plus explicit `HarnessArtifactValidationPolicy` and `HarnessArtifactValidationContext` | `ValidationResult` | Owns post-projection invariants and binds its result to the exact candidate, policy, context, and validator identities. |
| Synchronizer | Complete candidate, its applicable passing candidate `ValidationResult`, exact affirmative synchronization authorization, and publication policy/context | `SynchronizationResult` | Verifies exact bindings and preconditions, then stages and validates a new immutable generation and atomically replaces the regular current-generation pointer on a supported filesystem; it neither silently validates, authorizes, nor repairs. |
| Generation resolver | Explicit projection target and resolver policy/context | `HarnessProjectionGenerationResolutionResult` | Reads the pointer once, validates pointer and generation closure, and returns one immutable generation or a fail-closed represented outcome. |
| Comparator | Complete candidate, its applicable passing candidate `ValidationResult`, one resolved immutable maintained generation, and exact affirmative comparison authorization | `ComparisonResult` | Verifies exact bindings and preconditions, then reports drift without validation, authorization, writing, or repair; blocked or invalid input yields a represented outcome without comparison. |

## One semantic path

Synchronization and checking share the same loading, compilation, validation, and projection stages:

```mermaid
flowchart TB
    input["Authoritative inputs"] --> load["Load immutable snapshot"]
    load --> compile["Compile normalized state"]
    compile --> outcome{"Compilation succeeded?"}
    outcome -->|No| stop["Return failed result; no HarnessState"]
    outcome -->|Yes| validate["Validate state"]
    validate --> authorize["Resolve exact projection authorization"]
    authorize --> project["Verify bindings and project immutable complete candidate set"]
    project --> candidate_validate["Validate exact candidate set"]
    candidate_validate --> mode{"Operation"}
    mode -->|Synchronize| sync_authorize["Resolve exact synchronization authorization"]
    sync_authorize --> publish["Verify bindings, stage generation, and switch pointer"]
    mode -->|Check| compare_authorize["Resolve exact comparison authorization"]
    compare_authorize --> resolve["Resolve current generation once"]
    resolve --> compare["Verify bindings and compare immutable sets"]
```

There is no synchronization-only parser and no check-only interpretation of source authority. If both operations observe the same input identities and versions, they must construct equivalent normalized state and candidate artifacts.

## Object model

The compiler architecture separates immutable state from reusable operations. It does not require a common base class. Three immutable aggregates define the principal boundaries:

```text
HarnessSourceSnapshot
    ↓ HarnessCompiler
HarnessState
    ↓ domain validators
ValidationResult
    ↓ HarnessProjector
HarnessArtifactSet
    ↓ HarnessArtifactSetValidator
candidate ValidationResult
```

Sources are observed in `HarnessSourceSnapshot`, domain meaning is normalized in `HarnessState`, and derived files are packaged in `HarnessArtifactSet`.

### Source model

`HarnessSourceSnapshot` is the complete immutable compiler input.

| Object | Role |
|---|---|
| `HarnessSourceIdentity` | Identifies one source by repository-relative path, source kind, format version, and content identity. |
| `HarnessSourceRecord` | Contains the parsed value from one authoritative source. |
| `HarnessSourceProvenance` | Maps a parsed value or field to its source identity and location. |
| `HarnessSourceSnapshot` | Contains the closed collection of identities, records, and provenance observed together. |

```mermaid
classDiagram
    class HarnessSourceSnapshot
    class HarnessSourceIdentity
    class HarnessSourceRecord
    class HarnessSourceProvenance

    HarnessSourceSnapshot *-- HarnessSourceIdentity : identifies
    HarnessSourceSnapshot *-- HarnessSourceRecord : contains
    HarnessSourceRecord --> HarnessSourceIdentity : originates from
    HarnessSourceRecord --> HarnessSourceProvenance : located by
```

A snapshot is closed: compilation cannot request an additional source after the loader returns it. Source records retain parsed values rather than mutable parser objects or open files.

### Normalized state model

`HarnessState` is the complete immutable repository-derived normalized aggregate. Repository sources remain authoritative. It is not an authority ledger, database, or collection of generated files. Lossless revisioned persistence stores this same aggregate and must not define a competing domain aggregate.

| Object | Role |
|---|---|
| `HarnessStateIdentity` | Identifies the normalized semantic state under an explicit model version. |
| `HarnessTaskRegistry` | Derived immutable index over normalized canonical development Task definitions. |
| `DevelopmentTaskSelection` | Identifies repository-derived requested/selected work state, if any; grants no authority or permission. |
| `DevelopmentDecision` sequence | Canonically ordered immutable unresolved and resolved/revised development-decision values stored directly in `HarnessState`. |
| `HarnessCapabilityCatalog` | Contains available development capabilities and their identities. |
| `HarnessResourceCatalog` | Contains resource identities and dependency closure. |
| `HarnessEvidenceCatalog` | Contains evidence identities, owners, and claim boundaries. |
| `HarnessState` | Aggregates the normalized development domains and their source provenance. |

```mermaid
classDiagram
    class HarnessState
    class HarnessStateIdentity
    class HarnessTaskRegistry
    class DevelopmentTaskSelection
    class DevelopmentDecision
    class HarnessCapabilityCatalog
    class HarnessResourceCatalog
    class HarnessEvidenceCatalog

    HarnessState --> HarnessStateIdentity : identified by
    HarnessState *-- HarnessTaskRegistry : contains
    HarnessState *-- DevelopmentTaskSelection : contains
    HarnessState *-- DevelopmentDecision : canonically ordered sequence
    HarnessState *-- HarnessCapabilityCatalog : contains
    HarnessState *-- HarnessResourceCatalog : contains
    HarnessState *-- HarnessEvidenceCatalog : contains
```

Every normalized object retains source provenance. When one complete unique normalized state can be constructed, representable cross-record inconsistencies remain available for deterministic validation with source-correlated findings. Malformed, unsupported, ambiguous, or otherwise unrepresentable source input yields a failed `HarnessCompilationResult` with no `HarnessState`; the compiler never chooses an arbitrary winner.

### Validation model

[Development validation](validation.md) owns the exact `ValidationFinding`,
`ValidationRuleIdentity`, and leaf-or-composite `ValidationResult` contract,
including its closed statuses, field invariants, precedence, and claim boundary.
The compiler supplies normalized subjects and source provenance to validators; it
does not redefine validation outcomes.

### Projection and generation DataObjects

| Object | Role |
|---|---|
| `HarnessArtifact` | Represents one derived file with path, projection kind, format version, bytes, and content identity. |
| `HarnessArtifactManifest` | Declares the complete path, content-identity, format-version, and generating-state closure of a candidate set. |
| `HarnessArtifactSetIdentity` | Identifies the complete immutable candidate set, including its manifest identity. |
| `HarnessArtifactSet` | Forms the immutable candidate unit derived from one validated state. |
| `HarnessProjectionGenerationIdentity` | Identifies one immutable published generation independently of its directory name. |
| `HarnessProjectionGenerationManifest` | Declares generation identity, candidate-set and manifest identities, content closure, generating-state identity, predecessor generation, lifecycle status, and supported projection/format versions. |
| `HarnessProjectionPointerManifest` | Small regular-file value with pointer identity/revision, target identity, generation identity, generation-manifest/content identities, predecessor pointer identity, and pointer format version. |
| `HarnessProjectionRecoveryRecord` | Identifies an incomplete, corrupt, or quarantined generation, observed phase/state, failure identity, candidate/generation identities when known, and recovery-marker/quarantine location; it grants no repair or deletion authority. |

```mermaid
classDiagram
    class HarnessProjectionResult
    class HarnessArtifactSet
    class HarnessArtifactManifest
    class HarnessArtifact
    class HarnessStateIdentity
    class ValidationResult
    class DevelopmentOperationAuthorizationResult

    HarnessProjectionResult --> HarnessStateIdentity : exact subject
    HarnessProjectionResult --> ValidationResult : consumes state validation
    HarnessProjectionResult --> DevelopmentOperationAuthorizationResult : consumes projection authorization
    HarnessProjectionResult *-- HarnessArtifactSet : projected contains
    HarnessArtifactSet --> HarnessStateIdentity : derived from
    HarnessArtifactSet *-- HarnessArtifactManifest : declares closure
    HarnessArtifactSet *-- HarnessArtifact : contains
    HarnessArtifactManifest --> HarnessArtifact : identifies
```

### ResultObjects

| Object | Meaning |
|---|---|
| `HarnessSourceLoadResult` | Closed `loaded` or `failed` source-loading outcome; only loaded contains one closed `HarnessSourceSnapshot`. |
| `HarnessCompilationResult` | Closed succeeded-or-failed normalization outcome; only succeeded contains one complete unique `HarnessState`. |
| `ValidationResult` | Ordered findings and the exact claim boundary of validation. |
| `DevelopmentAuthorityContextResolutionResult` | Closed resolved-or-failed authority-context outcome; only resolved contains one usable `DevelopmentAuthorityContext`. |
| `DevelopmentTaskSignatureRequirementResult` | Closed resolution of the exact configured-Task signature requirement; absence deterministically means `not_required`. |
| `DevelopmentOperationAuthorizationResult` | Closed `signature_not_required`, `authorized`, `denied`, or `error` outcome for one exact operation and requirement result; it grants no broader authority and performs no target operation. |
| `HarnessProjectionResult` | Closed projected-or-blocked outcome; only projected contains one complete immutable `HarnessArtifactSet`. |
| `SynchronizationResult` | Exact candidate/predecessor, candidate and staged validation, authorization and authority-context, publication policy/context, verified target preconditions, operation/attempt, generation, pointer observation, lifecycle, and recovery/reconciliation outcome identities; it never makes the projection authoritative. |
| `HarnessProjectionGenerationResolutionResult` | Closed resolved or rejected result; only `resolved` contains one validated immutable generation, while `rejected` contains identified failures and no artifacts. |
| `HarnessProjectionRecoveryResult` | Records quarantine or recovery-marker handling without changing source authority or conferring deletion authority. |
| `ComparisonResult` | Candidate and resolved-generation identities plus missing, unexpected, byte-different, semantically different, or represented blocked/invalid outcome. |

A result records an operation outcome. It does not repeat or continue the operation.

### Validator protocol

Validator composition is a demonstrated polymorphic requirement because `HarnessStateValidator` applies multiple validators with different domain-rule owners through one deterministic interface. The protocol is domain-specific:

```python
class HarnessDomainValidator(Protocol):
    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]: ...

    def execute(self, state: HarnessState) -> ValidationResult: ...
```

Each concrete domain validator returns the normative leaf `ValidationResult`
defined by [Development validation](validation.md). A leaf result does not contain
a modified `HarnessState`; private intermediate findings do not cross the public
boundary.

Concrete implementations include:

| Validator | Principal domain | Responsibility |
|---|---|---|
| `DevelopmentTaskSelectionValidator` | `DevelopmentTaskSelection` | Selected-Task existence and activation consistency |
| `HarnessTaskGraphValidator` | canonical Task inputs | Task identity uniqueness, parent and prerequisite references, cycles, and graph closure before registry use |
| `HarnessCapabilityCatalogValidator` | `HarnessCapabilityCatalog` | Capability identities and declared relationships |
| `HarnessResourceCatalogValidator` | `HarnessResourceCatalog` | Resource dependencies, closure, and layering |
| `HarnessEvidenceCatalogValidator` | `HarnessEvidenceCatalog` | Evidence identities, ownership, and claim boundaries |

Each implementation may inspect the complete `HarnessState` when its rule needs an explicitly declared cross-reference, but it owns only its named domain rules. The protocol supplies no default rules, registration, discovery, mutation, repair, or authorization.

### ActionObjects

| ActionObject | Transformation |
|---|---|
| `HarnessRepositoryLoader` | explicit source contract → `HarnessSourceLoadResult` |
| `HarnessCompiler` | `HarnessSourceSnapshot` → `HarnessCompilationResult` |
| Concrete `HarnessDomainValidator` | `HarnessState` → leaf `ValidationResult` |
| `HarnessStateValidator` | `HarnessState` plus an explicit ordered validator tuple → `ValidationResult` |
| `DevelopmentTaskSignatureRequirementResolver` | exact Task record, expected configured-Task revision, and optional signature configuration → `DevelopmentTaskSignatureRequirementResult` |
| `DevelopmentAuthorityContextResolver` | protected configuration pin, exact trust/source configuration, and bounded signed authority-ledger snapshots → `DevelopmentAuthorityContextResolutionResult` |
| `DevelopmentOperationAuthorizer` | exact state and operation identities plus requirement result and optional successful authority-context resolution → `DevelopmentOperationAuthorizationResult` |
| `HarnessProjector` | state, exact applicable passing `ValidationResult`, exact affirmative projection authorization, and explicit projection inputs → `HarnessProjectionResult` |
| `HarnessArtifactSetValidator` | complete `HarnessArtifactSet` plus explicit validation policy/context → candidate `ValidationResult` |
| `HarnessSynchronizer` | complete candidate plus its applicable passing candidate `ValidationResult`, exact affirmative synchronization authorization, and publication policy/context → `SynchronizationResult` |
| `HarnessProjectionGenerationResolver` | explicit target plus resolver policy/context → `HarnessProjectionGenerationResolutionResult` |
| `HarnessStateComparator` | complete candidate plus its applicable passing candidate `ValidationResult`, exact affirmative comparison authorization, and resolved immutable generation → `ComparisonResult` |

`DevelopmentDecision` owns the intrinsic field and unresolved/resolved variant invariants of one value. Compilation normalization and `HarnessStateValidator` own cross-record decision-identity uniqueness, predecessor/supersession references, other declared references, and canonical sequence ordering directly over `HarnessState`; no decision catalog or decision-specific public validator exists. `HarnessStateValidator` otherwise owns composition rather than domain rules. It records the explicit validator order, applies every validator deterministically, evaluates cross-domain closure, aggregates ordered findings, and returns one `ValidationResult`. It does not discover validators, alter state, repair findings, or authorize actions.

Each ActionObject receives its dependencies explicitly, leaves its inputs unchanged, and returns an immutable object or result. It must not use ambient current-directory discovery, mutable global registries, or hidden fallback sources.

Neither `HarnessState` nor its domain objects perform I/O, validation, projection, publication, or comparison. Those operations belong to the named ActionObjects.

## Authoritative inputs

An operation begins with an explicit source contract. The contract identifies:

- the repository root;
- every permitted source family;
- expected schema or format versions;
- explicit external inputs, if any;
- path and symlink policy;
- required versus optional sources; and
- the ordering rule used when a source family contains multiple records.

The loader may read only sources selected by that contract. Repository scans may implement an explicitly declared source-family rule, but they may not discover new kinds of authority.

Generated projections are never source inputs merely because they are present. If a generated file disagrees with authoritative input, checking reports drift; the loader does not merge the two values or choose the generated value as a fallback.

## Repository loading

`HarnessRepositoryLoader` owns repository I/O and source-format decoding. It performs the following bounded steps:

1. validate the explicit repository root;
2. resolve each declared source beneath that root;
3. enforce path, exact-case, file-type, and symlink rules;
4. read each selected file once into the operation snapshot;
5. decode it according to its declared format version;
6. record its content identity and source provenance; and
7. close every file and parser resource before returning.

`HarnessSourceSnapshot` contains no open files, database connections, parser objects with mutable state, temporary paths, process handles, or credentials. `HarnessSourceLoadResult` is closed: `loaded` contains exactly one snapshot and no blocking loading diagnostic; `failed` contains no snapshot and at least one identified blocking loading diagnostic. A source that changes during loading causes a failed result rather than a mixed-revision snapshot.

## Compilation

`HarnessCompiler` performs the pure transformation

```text
HarnessSourceSnapshot → HarnessCompilationResult
```

The compiler receives no development-authority context, requested operation, permitted-path scope, or authority-ledger identity. Its success and state identities depend only on the closed source snapshot and identified compiler, model, and normalization versions.

`DevelopmentTaskSelection` remains repository-derived requested/selected work state and supplies no authority. After compilation and validation, `DevelopmentTaskSignatureRequirementResolver` binds the exact configured-Task revision and defaults absent configuration to `not_required`. `DevelopmentOperationAuthorizer` then receives the exact state and operation identities plus that requirement result. It returns `signature_not_required` without cryptographic work when the optional gate is disabled. Required mode additionally consumes an independently resolved candidate-independent authority context, rechecks its signed-head payload binding, and returns `authorized`, `denied`, or `error`. `signature_not_required` is not an authority grant, and a `HarnessTask`, selection, candidate decision, validation result, or target operation cannot authorize itself.

Compilation owns structural normalization, including:

- canonical identifier representation;
- deterministic record and relationship ordering, including the canonical `DevelopmentDecision` sequence;
- resolution of declared aliases;
- construction of typed relationships;
- normalization of equivalent source encodings;
- attachment of source provenance to normalized values; and
- calculation of the normalized-state identity.

Compilation does **not**:

- read files or invoke command-line programs;
- load, authenticate, or interpret the protected authority ledger;
- apply publication or rollback policy;
- authorize development work;
- infer approval or resolve a human decision;
- silently repair contradictory sources;
- import maintained projections as missing source state; or
- interpret scientific results.

Normalization may remove representation-only variation, such as irrelevant input ordering when the owning contract defines a canonical order. It must not erase a meaningful distinction, invent a missing value, or convert a conflict into an arbitrary winner.

## Provenance and diagnostics

Every normalized record and relationship retains enough provenance to identify its source. A diagnostic can therefore report:

- compiler phase;
- stable finding code;
- source identity and repository-relative path;
- record or field location;
- normalized object identity, when available;
- concise expected and observed conditions; and
- severity and claim boundary.

Diagnostics use deterministic ordering. They must not expose credentials, private payloads, environment secrets, or unrestricted source contents.

## Outcome retention and reconstruction

Each loader, compiler, validator, authority-context resolver, authorizer, and target operation returns its own immutable identity-bearing result to explicit application composition. No generic harness-operation report, quarantine aggregate, or second `HarnessState` repository is selected. When an applicable coding-standards adapter profile requires durable evidence, the derived report references the exact result and immutable source identities; its reporting and future serializer boundary own that retained representation. Otherwise, Architecture v2 does not require durable persistence of every read-only failed attempt merely because it is represented in memory.

Replay or reconstruction requires the same immutable source-snapshot, authority-ledger-snapshot, trust-configuration, policy, operation-input, and implementation-version identities applicable to the result. Changed inputs define a new operation rather than reconstruction of the prior result. Durable synchronization authority-to-outcome linkage is retained by the identity-bound `SynchronizationResult` referenced from the successful generation manifest or applicable recovery record.

## Validation

Validation occurs after compilation so every validator sees the same normalized model. Domain validators own rules for their domains, such as:

- development Task records and active selection;
- Task prerequisites and dependency relationships;
- aggregate-level `DevelopmentDecision` identity uniqueness, predecessor/supersession and other declared references, and canonical sequence ordering, owned directly by `HarnessStateValidator`; intrinsic field and unresolved/resolved variant invariants remain owned by each `DevelopmentDecision`;
- capability and resource closure;
- evidence identities and ownership; and
- source-owned destination policy and normalized-state destination invariants.

A validation coordinator may order validators and evaluate cross-domain closure, but it must not become a fallback owner for domain rules.

Validators are read-only. They return the single normative `ValidationResult` contract and do not repair `HarnessState`, rewrite sources, publish artifacts, or grant authority. Trusted in-process state validation may inspect the normalized candidate state before operation authorization; candidate-controlled coding-standards adapters use the explicit bounded invocation boundary defined by coding-standards conformance, with no custom sandbox implied. `PromotionEligibilityEvaluator` remains the sole mechanical promotion gate.

A structural pass establishes only conformance to those rules. It does not establish software-test success, numerical verification, scientific validation, uncertainty quantification, protected-execution authority, or human acceptance.

## Projection consumption

[Development projections](projections.md) owns candidate artifact contracts,
post-projection validation, immutable-generation publication, synchronization,
resolution, comparison, and recovery. The compiler produces the validated
`HarnessState` consumed by that boundary; it does not publish or compare derived
views. Human-authored files under `docs/` are never projections.

## Determinism

Compiler and projector determinism is defined over:

- the complete source identities;
- source schema and format versions;
- compiler and normalization-rule versions;
- validator and rule-set versions;
- projector and output-format versions; and
- explicit operation configuration.

Equivalent inputs under those versions produce equivalent `HarnessState` and candidate artifacts. Sources of incidental variation—filesystem enumeration order, locale, timezone, process ID, temporary paths, timestamps, random values, and host-specific SQLite state—must not enter deterministic outputs unless an owning contract represents them explicitly.

A normalized semantic digest identifies represented state, not arbitrary file layout. A raw artifact digest identifies exact bytes. The architecture keeps those identities separate.

## Concurrency and consistency

One compilation observes one closed source snapshot. Concurrent source mutation must be detected before publication. Synchronization verifies that its source snapshot is still applicable at the publication boundary; if not, it fails and requires a new load-and-compile operation.

Only one synchronizer may own a projection target at a time. On a supported filesystem, atomic replacement of the small regular pointer file selects either the previous complete closed generation or the new complete closed generation. Each reader reads that pointer once through `HarnessProjectionGenerationResolver` and remains bound to the selected immutable generation; it never rediscovers individual files. Comparison may run concurrently only against that resolved immutable generation.

## Failure model

| Phase | Example failure | Required outcome |
|---|---|---|
| Loading | Missing source, invalid path, changing file | No snapshot returned |
| Compilation | Duplicate canonical identity, ambiguous alias, or another unrepresentable normalization | Failed `HarnessCompilationResult`; no normalized state |
| Validation | Broken prerequisite, graph cycle, selection inconsistency, or resource closure | Findings returned with normalized state retained; target operations reject non-passing validation |
| Projection | Unsupported format, nondeterministic output, or failed projection precondition | Blocked `HarnessProjectionResult`; no `HarnessArtifactSet` returned |
| Candidate validation | Manifest mismatch, unsupported version, open mutable resource, or SQLite sidecar | Identified candidate `ValidationResult`; no publication or comparison |
| Authorization | Missing, stale, exhausted, revoked, erroneous, or mismatched exact operation authorization | Target operation returns its represented blocked result; no target effect |
| Publication preflight | Unsupported/network filesystem or unavailable durability guarantee | Represented failure; no staging or pointer replacement |
| Generation staging | Incomplete write, close/fsync failure, or corrupt closure | Old pointer remains current; orphan is marked or quarantined; exact state reported |
| Pointer replacement | Failure or ambiguous acknowledgement | Reconcile by rereading pointer and exact generation identity; never multi-file rollback |
| Generation resolution | Missing/malformed pointer, non-closed generation, unsupported version, or identity/closure mismatch | Fail-closed resolution result; no fallback or mixed read |
| Comparison | Missing or divergent artifact in the resolved generation | Read-only drift result returned |

A failure in any phase grants no authority and activates no recovery workflow by itself. Retry is an explicit caller decision using a new operation context.

## Security and path safety

All repository and destination paths are explicit, repository-relative, and root-confined. Loaders and synchronizers reject traversal, unexpected symlinks, unsupported file types, and destinations outside their declared ownership. Compiler state and diagnostics contain no credentials. External data transmission is not part of this architecture.

## Extension rules

A new source family requires an explicit source contract, format identity, loader support, normalized owner, validation rules, and provenance mapping. A new projection format requires a format identity, deterministic projection contract, candidate validation, comparison semantics, and publication ownership.

Neither extension may introduce a parallel compiler path, hidden registry, ambient discovery, or independent interpretation of development authority.

## Authority limits

This compiler architecture belongs exclusively to the development harness. It may represent development Tasks, decisions, capabilities, evidence, and derived control views. It does not:

- load or advance a scientific `WorkflowRun`;
- compile a Workflow into calculator work;
- execute a calculator;
- interpret numerical observations;
- create `ScientificAnalysis`; or
- record scientific acceptance.

Any scientific workflow compiler requires a separate contract under the scientific workflow architecture. It may reuse generic deterministic techniques, but it cannot inherit development-harness state authority implicitly.

## Deferred implementation details

- Exact public field contracts for source snapshots, normalized state, and artifact sets.
- Compiler and normalization-rule version identities.
- Source-snapshot consistency mechanism under concurrent repository mutation.
- Whether format-specific projectors are public ActionObjects or private strategies.
- Concrete supported-local-filesystem matrix and durability adapter tests.
- Retention and garbage-collection policy for immutable projection generations.
- Canonical semantic-digest representation.

## Compilation result discriminant

`HarnessCompilationResult` is a closed discriminated union. Both variants carry source-snapshot identity, compiler and normalization-version identities, and deterministically ordered diagnostics. Neither variant carries development-authority-context, authority-ledger, authorization, requested-operation, or permitted-path identity.

- `succeeded` contains exactly one `HarnessState` and contains no blocking compilation diagnostic.
- `failed` contains no `HarnessState` and contains at least one blocking compilation diagnostic.

The variants cannot represent partial, contradictory, or nullable success. Authority-ledger and authorization identities affect only their own results and the exact target-operation provenance that consumes them. They do not affect compilation-result or `HarnessState` identity, and authority records are not copied into `HarnessState` as repository-derived domain data.
