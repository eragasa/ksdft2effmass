# Development decisions and authority migration plan

## Status and identity

**Proposed work; blocked at two human-owned boundaries.** The canonical Task is
`migration.v2.harness.decisions-authority`, contained by
`migration.v2.harness`. Its declared prerequisites,
`migration.v2.identity-contracts` and `migration.v2.harness.task-model`, are
human-accepted and closed. The current human instruction selected this Task and
authorized planning; implementation was authorized only if planning exposed no
issue. Planning exposed two material unresolved public-contract and protected-trust
choices, so implementation has not begun.

The v2 owner is `ksdft2effmass.harness`. This plan authorizes no protected
execution, dependency change, automatic succession, publication, or release.

## V1 source responsibilities

The implemented compatibility baseline is distributed across these surfaces:

| Surface | Current responsibility | Migration significance |
|---|---|---|
| `harness/pi/checkpoints.py` | Narrow immutable `CheckpointRecord`, pure resolution request/result, resolver, and set validator | Represents only part of the project-local durable checkpoint contract |
| `harness/pi/wire/checkpoints.py` | Explicit narrow checkpoint field mapping | Cannot encode all current `.pi/checkpoints/*.json` fields |
| `harness/pi/local/control_record_adapters.py` | Adapts selected project checkpoint bytes into narrow records | Drops `recommendation`, `blocked_scope`, `safe_scope`, and `authoritative_files`, and derives resumption state |
| `harness/pi/human_review.py` | Review preparation and caller-supplied decision representation | Remains review evidence; it grants no authority and is not a second development-decision aggregate |
| `.pi/checkpoints/*.json` | Durable project-local decision history | Must remain immutable and losslessly accounted for during migration |
| `harness/task-selection.json` | Current selected work and activation-reference identifiers | Selection is an authorizer input, never authority |
| Generated SQL and SQLite | Derived control projection | Cannot become an authority source or protected ledger |

The current checkpoint adapter is therefore not a sufficient migration source.
Migration must consume exact legacy bytes or an explicitly lossless legacy model.
Historical `authorized_scope` text is decision evidence; it is not a
`TaskAuthorization` and cannot be reinterpreted as one.

## Target concern and exclusions

Accepted architecture fixes the following decomposition:

- one immutable `DevelopmentDecision` model is contained directly in the complete
  repository-derived `HarnessState`;
- unresolved and resolved/revised decisions preserve exact human inputs and use
  append-only predecessor/supersession history;
- `HarnessStateValidator` owns cross-record identity uniqueness, reference closure,
  and canonical decision ordering;
- protected `DevelopmentAuthorityLedger` state remains outside `HarnessState`;
- `DevelopmentAuthorityContextResolver` reconstructs a candidate-independent
  context from one explicitly selected protected source;
- `DevelopmentOperationAuthorizer` evaluates one exact selected Task, operation,
  revision set, path scope, and requirement set against that context; and
- only an exact affirmative `DevelopmentOperationAuthorizationResult` may be
  consumed by the target operation, which must verify all bindings.

No Task, selection, decision, review, validation result, generated projection,
candidate state, or successful check authorizes itself. This Task does not own target
repository effects, scientific Workflow decisions, calculator execution, shared
revision-store implementation, or Pi transport adaptation.

## Ownership decomposition

### DataObjects

`DevelopmentDecision` owns intrinsic field and unresolved/resolved-variant
invariants only. The pending cutover decision selects its source and migration
topology, not its exact fields or encoding. Those require a subsequent bounded public-
contract review derived from the selected topology.

Protected authority-plane values comprise `DevelopmentTrustConfiguration`, immutable
ledger snapshot and record values including `TaskAuthorization` and revocation facts,
`DevelopmentAuthorityReconstructionReceipt`, and
`DevelopmentAuthorityContext`. They never enter `HarnessState` or its identity.

The exact operation input represents repository root, source, selection and Task
revisions, starting and candidate revisions, operation identity, permitted paths, and
operation requirements. It is not itself a grant.

### ResultObjects

`DevelopmentAuthorityContextResolutionResult` is a closed `resolved`/`failed`
outcome. Only `resolved` contains a usable context; failure retains deterministic
identified diagnostics.

`DevelopmentOperationAuthorizationResult` is a closed
`authorized`/`denied`/`error` outcome. Only `authorized` identifies the exact
matching, unrevoked authorization and complete operation bindings.

### ActionObjects

The repository loader and compiler decode accepted decision sources and normalize
one canonical sequence without interpreting a response or reconstructing authority.
`HarnessStateValidator` validates aggregate decision relationships.

`DevelopmentAuthorityContextResolver` authenticates the explicitly selected source,
verifies identity and predecessor/revocation closure, and returns the context result
and receipt. It does not authorize an operation. `DevelopmentOperationAuthorizer`
performs exact matching against an already resolved context and neither reconstructs
that context nor executes the target operation.

The dependency direction is:

```text
repository decision sources -> loader/compiler -> HarnessState -> HarnessStateValidator
protected trust configuration + selected ledger source -> context resolver -> authority context
HarnessState + selection + exact operation + authority context -> authorizer -> target operation
```

## Unresolved human decisions

### DevelopmentDecision wire and legacy cutover

Checkpoint
`.pi/checkpoints/migration.v2.harness.decisions-authority.decision-cutover.json`
asks whether to retain dual-format compiler ingress during a measured migration or
create separately identified v2 successor records and cut canonical consumers to the
new source family. Both preserve legacy bytes and forbid in-place history rewrites,
but they differ materially in public wire support, persistence, compatibility life,
and rollback.

### Protected ledger trust source

Checkpoint
`.pi/checkpoints/migration.v2.harness.decisions-authority.ledger-trust.json`
asks whether authoritative reconstruction is based on explicitly selected protected
signed snapshot artifacts or an authenticated protected CI/service source with an
identity-bound export for local reconstruction. The choice affects trust roots,
credentials, availability, storage, transport, verification, and failure recovery.
Ordinary repository SQLite is not an eligible authority source.

These checkpoints select conceptual topologies only. They do not silently decide
exact public fields, canonical encodings, signing algorithms, trust-anchor operation,
credentials, or transport protocols. After both are resolved, one bounded exact-
contract planning pass must derive those details from the selected topologies and
return any remaining material public, dependency, or protected-mechanism choice for
human review. Implementation remains blocked until that exact contract is accepted.

## Implementation approach after exact-contract acceptance

1. Inventory every retained checkpoint shape and reader from exact bytes; record an
   explicit preserve/map/source-provenance disposition for every legacy field and
   lifecycle variant.
2. Implement the accepted `DevelopmentDecision` field and source contract under the
   v2 public owner, with one-way legacy adaptation and no invented authority facts.
3. Integrate decision normalization into the future complete `HarnessState` compiler
   and aggregate validation owner; do not introduce a decision catalog or
   decision-specific public resolver.
4. Implement the selected protected trust source, immutable ledger records, context
   resolver, receipt, and closed resolution result independently of repository-derived
   state.
5. Implement exact operation inputs, authorizer, and closed authorization result.
   Every varied binding must fail closed; denied or error outcomes cause no target
   effect.
6. Run shadow decision compilation and authority reconstruction before consumer
   cutover. New code imports v2 owners; no new domain code imports transitional local
   adapters.
7. Retire v1 resolver and wire routes only after every retained consumer has an exact
   disposition and rollback gates pass.

This is one serial implementation because the decision representation, protected
context, and exact authorizer meet at public operation bindings. Separate concurrent
writers are not required.

## Prerequisite results

Implementation requires retained identities for the accepted identity-contract and
Task-model results, not only their Task status text. It also requires both pending
architecture decisions, an accepted resulting exact public-wire and protected-
mechanism contract, exact source and trust-configuration identities, exact selection
and Task revisions, requested operation, permitted paths, and applicable starting and
candidate revisions.

A producer Task status, planning prose, review agreement, passing test, activation
reference, checkpoint scope, or generated projection is not a prerequisite result or
operation grant.

## Verification

The applicable evidence class is software verification. After the architecture and
exact-contract decisions are resolved, focused evidence must cover:

- intrinsic unresolved/resolved decision variants, exact response preservation,
  ambiguous or conflicting response behavior, immutability, and append-only
  correction;
- aggregate identity uniqueness, predecessor/supersession closure, canonical ordering,
  source provenance, and exclusion of authority context from `HarnessStateIdentity`;
- lossless compatibility fixtures for every retained legacy checkpoint shape and
  field, with no invented authorization;
- resolver matrices for missing, stale, corrupt, unauthenticated, content-mismatched,
  incomplete, revoked, and wrong-trust-source snapshots, all yielding no context;
- authorizer matrices varying Task and selection revisions, state revisions,
  operation, path scope, authorization state, exhaustion, and revocation independently;
- target-operation non-effect for denied, error, or mismatched results; and
- migration shadow, cutover, stale-consumer, rollback, public-import, Ruff, mypy,
  Sphinx, Harness projection, and maintained Python-conformance checks.

These checks establish only the documented software and security-boundary contracts.
They do not establish protected authority for a real operation, numerical
verification, scientific validation, uncertainty quantification, or human acceptance.

## Cutover, retirement, and rollback

Original checkpoint bytes and decision history are never rewritten. Cutover proceeds
from v2 source introduction, through shadow compilation and exact compatibility
comparison, to consumer migration and finally explicit legacy-route retirement.
Rollback restores the last accepted consumer/import and authority-composition
revision; it does not modify decision history, ledger history, Tasks, selection, or
legacy checkpoint bytes.

The protected ledger source, trust configuration, and reconstruction receipts remain
separate from `HarnessState` persistence and generated projections throughout cutover
and rollback.

## Residual limitations

- The checkpoint-source and cutover topology awaits the decision-cutover checkpoint;
  exact public decision fields, canonical encoding, and legacy-ingress lifetime then
  require bounded public-contract review.
- The protected trust-source topology awaits the ledger-trust checkpoint; exact trust
  anchors, authentication, ledger storage, signing, credential handling, and transport
  then require bounded protected-mechanism and any applicable dependency review.
- Exact shared `HarnessState`, compiler, validator, and repository fields remain with
  their separately declared Tasks and may add prerequisite results without changing
  the ownership fixed here.
- No implementation, protected execution, dependency change, successor activation,
  publication, or release has occurred.
