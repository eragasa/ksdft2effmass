# Development decisions and authority migration plan

## Status and identity

**Exact contract planning; implementation blocked.** The canonical Task is
`migration.v2.harness.decisions-authority`, contained by
`migration.v2.harness`. Its declared prerequisites,
`migration.v2.identity-contracts` and `migration.v2.harness.task-model`, are
human-accepted and closed. The human selected separately identified v2 successor
records for `DevelopmentDecision` and protected signed snapshot artifacts for the
`DevelopmentAuthorityLedger` trust source. Those responses are preserved in the two
resolved Task checkpoints.

Exact planning exposed a public-wire acceptance decision and a dependency/protected-
signature mechanism decision. Implementation was authorized only if planning exposed
no issue, so it has not begun. The v2 owner is `ksdft2effmass.harness`; this plan
authorizes no dependency change, credential handling, protected execution, automatic
succession, publication, or release.

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
invariants only. The resolved cutover decision selects its source and migration
topology, not its exact fields or encoding. The pending exact-contract checkpoint owns
that subsequent bounded public-contract review.

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

## Resolved architecture decisions

The exact response `1. B and 2 A is authorized` selected:

- **Decision cutover B:** separately identified v2 successor records become the
  future canonical decision source; legacy checkpoint bytes remain immutable history
  and are not rewritten in place.
- **Ledger trust A:** explicitly selected protected signed snapshot artifacts provide
  local and CI reconstruction input; ordinary repository SQLite, candidate state, and
  ambient discovery remain ineligible trust sources.

These decisions fix topology but do not themselves accept the exact public wire or a
cryptographic implementation dependency.

## Exact DevelopmentDecision contract candidate

One frozen, slotted `DevelopmentDecision` DataObject has schema version 1 and the
following fields; canonical object-key order is lexical rather than the presentation
order below:

```text
schema_version, decision_id, state, decision_class, task_id, episode_id,
created_at, question, options, recommendation, blocked_scope, safe_scope,
declared_authoritative_paths, response_source_identity,
authority_identity_status, authority_identity, response, normalized_outcome,
selected_option_id, resolved_at, declared_scope, record_paths,
resumption_status, predecessor_decision_id, supersedes_decision_id,
source_provenance
```

Each option is `{option_id, summary, consequence}`. `source_provenance` identifies the
source family and schema version, exact source identity and path, SHA-256 and byte
count of exact source bytes, adapter version, optional legacy checkpoint identity,
and exact legacy status. A digest or declared authoritative path records provenance
only and grants no authority.

`state` is exactly `unresolved` or `resolved`; revision and supersession are orthogonal
to response state. Unresolved decisions encode response, outcome, selected option,
resolution time, and declared scope as JSON `null`. Resolved decisions require the
verbatim response, one normalized outcome, resolution time, and declared scope.
`predecessor_decision_id` and `supersedes_decision_id` are both null for an initial
record and both non-null and equal for a successor revision, whether unresolved or
resolved. Aggregate validation requires the target to exist earlier, closed acyclic
references, no fork, and one effective tip. `selected_option_id` is non-null only when
exact durable evidence establishes one offered option. Migration copies legacy
normalized prose without reinterpreting it.

All wire fields are required and always emitted; inactive optional values are encoded
as JSON `null`, never omitted. Canonical version-1 bytes reuse the implemented Harness
JSON profile: UTF-8, no BOM, keys sorted lexically, compact separators, no NaN or
infinity, duplicate keys rejected, and exactly one trailing line feed. Unknown or
missing fields, unsupported versions, noncanonical bytes, booleans in integer
positions, malformed identifiers, timestamps, paths, digests, or duplicate options
are rejected. This is a narrow named Harness profile, not a claim of complete RFC
8785 support and requires no new dependency.

The exact legacy mapping is:

| Legacy field | Successor field or disposition |
|---|---|
| `checkpoint_id` | retained as `source_provenance.legacy_checkpoint_id`; `decision_id` is allocated by the explicit migration manifest |
| `task_id`, `episode_id`, `decision_class`, `created_at`, `question` | copied exactly |
| `status` | copied to `source_provenance.legacy_status`; `resolved` maps to resolved state and every null-response status maps to unresolved state |
| `options[].id`, `summary`, `consequence` | copied exactly to `options[].option_id`, `summary`, `consequence`, preserving order |
| `recommendation`, `blocked_scope`, `safe_scope` | copied exactly |
| `authoritative_files` | copied exactly to `declared_authoritative_paths`; remains a historical declaration, not reconstructed authority |
| `human_response`, `normalized_decision`, `resolved_at` | copied exactly to `response`, `normalized_outcome`, `resolved_at` |
| `authorized_scope` | copied exactly to `declared_scope`; never a grant |
| `record_paths`, `resumption_status` | copied exactly without normalization |

Legacy records lack separate trusted response-source and authority identities.
`response_source_identity` and `authority_identity` are therefore null and
`authority_identity_status` is `unavailable_legacy`; native v2 records require
`available` plus both exact identities. The source artifact identity is the exact
legacy path, SHA-256, and byte count, not an invented authority identity.

The current adapter is prohibited as a migration source because it drops four fields
and collapses resumption text. The unresolved successor for `P2-HC04` may name and
supersede the unresolved successor for `P2-HC03`, as the durable records cross-reference
that edge. The absent later record named by `P2-HC04` remains an explicit provenance
gap rather than a fabricated successor.

Checkpoint
`.pi/checkpoints/migration.v2.harness.decisions-authority.development-decision-contract.json`
requests acceptance, bounded correction, or deferral of this exact candidate.

## Signed-ledger contract outline

The following outline fixes ownership and required meaning but is not yet an exact
public field or wire contract. A dedicated ledger-contract acceptance boundary will be
prepared after the signature mechanism is selected.

The prospective public immutable values are `DevelopmentTrustAnchor`,
`DevelopmentTrustConfiguration`, tagged `DevelopmentAuthorityRecord` variants,
`DevelopmentAuthorityLedgerSnapshot`, `DevelopmentSignedAuthoritySnapshot`,
`DevelopmentAuthorityReconstructionReceipt`, `DevelopmentAuthorityContext`, and
`DevelopmentOperationAuthorizationInput`. Closed results are
`DevelopmentAuthorityContextResolutionResult` (`resolved`/`failed`) and
`DevelopmentOperationAuthorizationResult` (`authorized`/`denied`/`error`).

A complete ledger snapshot contains a ledger identity, monotonic sequence,
predecessor snapshot payload identity, complete ordered record chain, governing policy
identity, and payload identity. Record variants cover policy, exact Task authorization,
eligibility reference, review or promotion authorization, authorization use, and
revocation. Effective exhaustion is derived from append-only use facts; revocations,
uses, policies, and predecessors must close within the snapshot.

The signed envelope contains canonical payload bytes, mechanism and key identifiers,
signature encoding and bytes, plus a distinct exact-artifact identity. Signatures bind
a versioned domain-separated length-framed preimage of the exact payload. Trust
configuration pins accepted artifact/head or ancestor identity, trust domain, issuer-
to-anchor bindings, accepted versions and modes, enabled public verification anchors,
and threshold policy. Signature validity alone never establishes freshness.

The resolver receives explicit bounded bytes, expected artifact identity, source mode,
and trust configuration. It performs no discovery, fetching, signing, publication, or
credential access. Any malformed, noncanonical, mismatched, untrusted, stale, forked,
revoked, exhausted, incomplete, or indeterminate input yields no context. The
authorizer consumes only a resolved context and exact operation bindings; every
mismatch denies, while an unusable context is an error rather than a denial.

The current dependency contract contains no supported asymmetric signature API.
Hand-written public-key cryptography is prohibited. Checkpoint
`.pi/checkpoints/migration.v2.harness.decisions-authority.signature-mechanism.json`
therefore asks the human to choose an audited asymmetric Python dependency, an
explicit external verifier executable, symmetric HMAC with its loss of verifier/signer
separation, or deferral. Protected signing, key generation, secret handling,
publication, and accepted-head advancement remain later protected operations and are
not implemented by this Task's read-only resolver.

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
Task-model results, not only their Task status text. It also requires the accepted
resolved topology checkpoints, acceptance of the exact DevelopmentDecision contract,
an accepted signature mechanism and any dependency or executable decision, exact
source and trust-configuration identities, exact selection and Task revisions,
requested operation, permitted paths, and applicable starting and candidate revisions.

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

- The exact DevelopmentDecision fields, canonical encoding, migration mapping, and
  rollback policy await the development-decision-contract checkpoint.
- The asymmetric signature implementation, algorithm, key encoding, and dependency or
  external executable await the signature-mechanism checkpoint. Trust-anchor rotation,
  protected signing/publication, credential handling, and accepted-head advancement
  remain separately protected operations even after mechanism selection.
- Exact shared `HarnessState`, compiler, validator, and repository fields remain with
  their separately declared Tasks and may add prerequisite results without changing
  the ownership fixed here.
- No implementation, protected execution, dependency change, successor activation,
  publication, or release has occurred.
