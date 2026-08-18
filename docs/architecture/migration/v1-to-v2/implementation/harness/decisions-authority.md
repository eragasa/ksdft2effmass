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
invariants only. The resolved cutover and exact-contract decisions select its source,
migration topology, fields, invariants, and encoding.

Protected authority-plane DataObjects comprise `DevelopmentTrustConfiguration`,
immutable ledger snapshot and record values including `TaskAuthorization` and
revocation facts, and `DevelopmentAuthorityContext`. The derived
`DevelopmentAuthorityReconstructionReceipt` is a ResultObject. They never enter `HarnessState` or its identity.

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

The accepted contract requires this exact wire clarification before implementation.
`DevelopmentDecisionOption` has exactly `option_id: Identifier`, `summary: Text`, and
`consequence: Text | null`. `DevelopmentDecisionSourceProvenance` has exactly:

```text
schema_version: 1
source_family: "legacy_checkpoint" | "development_decision"
source_schema_version: Identifier
source_artifact_identity: Digest
source_path: ResourcePath
source_byte_count: UInt64
adapter_version: Identifier
legacy_checkpoint_id: Identifier | null
legacy_status: Identifier | null
```

Legacy sources require both legacy fields; native v2 sources require both null. The
artifact identity is SHA-256 over exact source bytes. The complete
`DevelopmentDecision` field types are:

| Field | Exact type |
|---|---|
| `schema_version` | integer 1 |
| `decision_id` | `Identifier`, allocated by the explicit migration or native creation input rather than derived from a filename |
| `state` | `"unresolved" \| "resolved"` |
| `decision_class`, `task_id`, `episode_id` | `Identifier \| null` |
| `created_at`, `resolved_at` | RFC 3339 UTC `Text \| null` |
| `question`, `recommendation`, `blocked_scope`, `safe_scope`, `response`, `normalized_outcome`, `declared_scope`, `resumption_status` | `Text \| null` |
| `options` | nonempty tuple of `DevelopmentDecisionOption`; unique option IDs; source order preserved |
| `declared_authoritative_paths`, `record_paths` | tuple of unique `ResourcePath`; source order preserved |
| `response_source_identity`, `authority_identity` | `Identifier \| null` |
| `authority_identity_status` | `"available" \| "unavailable_legacy"` |
| `selected_option_id` | `Identifier \| null` naming one option when present |
| `predecessor_decision_id`, `supersedes_decision_id` | `Identifier \| null` with the paired rules above |
| `source_provenance` | `DevelopmentDecisionSourceProvenance` |

Every key is required and null is explicit. Native resolved decisions require
`authority_identity_status="available"`, non-null response-source and authority
identities, and the resolved fields. Legacy successors require
`unavailable_legacy` and null trusted identities; no availability is fabricated.

Checkpoint
`.pi/checkpoints/migration.v2.harness.decisions-authority.development-decision-contract-amendment.json`
requests acceptance of this exact type, nullability, nested-wire, and source-provenance
clarification to the previously accepted DevelopmentDecision contract.

## Resolved exact-contract and signature decisions

The exact response `“1 A, 2 A.”` accepted the version-1 DevelopmentDecision contract
above and selected Ed25519 verification through the Python `cryptography` package.
The response authorizes exact dependency compatibility and license review, not project
dependency mutation, credential handling, signing, publication, or protected
execution.

Public metadata verified on 2026-08-18 identifies `cryptography` 50.0.0 as supporting
Python 3.14 and providing CPython 3.14 wheels. Its project license permits use under
either Apache-2.0 or BSD-3-Clause terms. A temporary Python-3.14 `uv 0.11.25`
resolution of `cryptography==50.0.0` produced `cryptography==50.0.0`, `cffi==2.1.1`,
and `pycparser==3.0`; it did not mutate project files. CFFI states MIT No Attribution
terms and pycparser states BSD-3-Clause terms. The actual project lock remains the
resolved-version authority after separately authorized dependency mutation.

Verified sources:

- `https://pypi.org/project/cryptography/50.0.0/`;
- `https://cryptography.io/en/50.0.0/hazmat/primitives/asymmetric/ed25519/`;
- `https://github.com/pyca/cryptography/blob/50.0.0/LICENSE`;
- `https://pypi.org/project/cffi/2.1.1/` and its `v2.1.1` license; and
- `https://pypi.org/project/pycparser/3.0/` and its BSD license.

The retained review is
`harness/reports/development-authority-cryptography-dependency-review.md`. The
implementation dependency candidate is exactly `cryptography==50.0.0`; the temporary
lock and its package hashes are recorded there. Exact project lock output and platform
markers must still be reviewed after real project resolution; the probe is
compatibility evidence, not a committed dependency result.

## Exact signed-ledger contract candidate

All values are frozen, slotted, operationally immutable public Harness records. Each
selected concrete wire variant requires exactly the keys declared for that variant;
keys owned by another variant are prohibited rather than emitted as null. Fields
explicitly marked nullable are required keys encoded as JSON `null` when inactive.
Unknown, duplicate, or missing keys are rejected. Every object uses the same sorted-key
compact UTF-8 Harness JSON profile with one trailing line feed as
`DevelopmentDecision`.

The normative wire vocabulary is:

| Name | Exact JSON/runtime contract |
|---|---|
| `Identifier` | JSON string matching `[A-Za-z0-9][A-Za-z0-9._:/-]*`; built-in `str` at runtime |
| `ResourcePath` | JSON string satisfying the accepted version-1 root-relative NFC POSIX path contract; built-in `str` at runtime |
| `Digest` | 64 lowercase hexadecimal SHA-256 characters |
| `Text` | JSON string without unpaired surrogates; nonempty where stated |
| `UInt64` | JSON integer from $0$ through $2^{64}-1$; Boolean rejected |
| `Bytes32` / `Bytes64` | unpadded canonical base64url JSON string decoding to exactly 32 or 64 bytes; runtime `bytes` |
| tuple | JSON array; runtime built-in tuple; fields marked canonical are strictly sorted and duplicate-free |
| diagnostic | JSON object with exactly `code: Identifier`, `subject_identity: Identifier | null`, and `detail: Text` |

Every field ending `_id` or `_identity` is an `Identifier` unless its table explicitly
says `Digest`; every revision field has the exact type stated by its owning table; every `schema_version` is integer 1. Domain-derived
identities use SHA-256 over
`domain_ascii + b"\x00v1\x00" + uint64_big_endian(len(body)) + body`, where `body` is
the exact canonical JSON object with only the identity being computed encoded as null.
Domains are fixed as `ksdft2effmass-development-trust-configuration`,
`ksdft2effmass-development-trust-configuration-pin`,
`ksdft2effmass-development-authority-source`,
`ksdft2effmass-development-authority-record`,
`ksdft2effmass-development-authority-receipt`,
`ksdft2effmass-development-authority-context`,
`ksdft2effmass-development-operation-authorization-input`, and
`ksdft2effmass-development-operation-authorization-result`. This rule defines
configuration, source-descriptor, record-content, receipt, context, and result
identities respectively and prevents self-reference. The receipt body has no context
identity; context identity is derived only after the finalized receipt identity exists.

### Trust and source records

`DevelopmentTrustAnchor` fields are:

```text
schema_version: 1
anchor_id: Identifier
key_id: Digest
mechanism: "ed25519"
public_key_encoding: "raw-base64url"
public_key_bytes: Bytes32
issuer_authority_identity: Identifier
state: "enabled" | "disabled"
```

`key_id` is SHA-256 over
`b"ksdft2effmass-development-authority-key\x00v1\x00" + public_key_bytes`.
Only public verification material is representable.

`DevelopmentIssuerAnchorBinding` fields are
`issuer_authority_identity: Identifier`, canonical nonempty
`allowed_record_kinds: tuple[record-kind enum]`, canonical nonempty
`anchor_ids: tuple[Identifier]`, and `threshold: UInt64` greater than zero and no
greater than the enabled listed-anchor count. For every record, the head envelope's
verified distinct anchor IDs must satisfy the exact binding for that record's issuer
and kind. Missing, duplicate, disabled, wrong-issuer, or insufficient bindings fail
reconstruction. The software's closed record semantics remain authoritative; a policy
record cannot add a new record kind or evaluation language.

`DevelopmentTrustConfiguration` fields and types are:

```text
schema_version: 1
configuration_identity: Digest
configuration_revision: UInt64
predecessor_configuration_identity: Digest | null (null only at revision zero)
trust_domain: Identifier
accepted_payload_schema_version: 1
accepted_envelope_schema_version: 1
accepted_canonicalization_version: "harness-canonical-json-v1"
accepted_source_modes: canonical nonempty tuple["local" | "ci"]
accepted_head_artifact_identity: Digest
required_ancestor_payload_identity: Digest
minimum_snapshot_sequence: UInt64
anchors: canonical nonempty tuple[DevelopmentTrustAnchor] ordered by anchor_id
issuer_anchor_bindings: canonical nonempty tuple[DevelopmentIssuerAnchorBinding]
resolver_policy_version: Identifier
```

`DevelopmentTrustConfigurationPin` is a separately protected trusted-boundary input
with `schema_version=1`, `pin_identity: Digest` derived under the fixed
`ksdft2effmass-development-trust-configuration-pin` domain,
`current_configuration_identity: Digest`, `minimum_configuration_revision: UInt64`,
`source_authority_identity: Identifier`, and
`authentication_receipt_identity: Identifier`. Application composition authenticates
this pin outside candidate-controlled state. The resolver rejects any supplied
configuration whose derived identity differs, whose revision is below the protected
minimum, or whose predecessor rules are inconsistent. Receipt and context bind the
pin identity and configuration revision. Replaying an old valid configuration and its
old signed head therefore fails before ledger reconstruction.

The accepted head artifact identity pins freshness independently of signature
validity. Anchor disablement and head advancement require a new independently
protected configuration and pin; a ledger cannot revoke its own trust root.

`DevelopmentAuthoritySnapshotSource` fields are:

```text
schema_version: 1
source_descriptor_identity: Digest
mode: "local" | "ci"
source_reference_identity: Identifier
expected_head_artifact_identity: Digest
maximum_snapshot_count: UInt64 greater than zero
maximum_aggregate_byte_count: UInt64 greater than zero
```

The resolver receives a nonempty tuple of exact signed-envelope byte strings ordered
from the required ancestor through the accepted head. Each decoded payload after the
first must name the preceding payload identity; the first payload identity must equal
`required_ancestor_payload_identity`; the final envelope identity must equal both
source and configuration head identities. Every envelope is independently canonical,
content-identified, and signature-verified under the configuration. Adjacent snapshots
must retain the same `ledger_id`, increment `snapshot_sequence` by exactly one, name
the immediately preceding payload identity, and preserve the predecessor's complete
record tuple as an exact prefix; every added record then continues the ordinal and
record-content predecessor chain. Any deletion, replacement, reordering, or mutation
of prior authority records fails ancestry. This bounded chain makes both payload
ancestry and append-only semantic continuity provable. The source contains no open file, network client,
path discovery, credential, or payload bytes.

### Ledger records

Every concrete authority record has these exact common fields:

```text
schema_version: 1
record_id: Identifier
record_content_identity: Digest
record_ordinal: UInt64
previous_record_content_identity: Digest | null (null only at ordinal zero)
record_kind: closed enum below
issuer_authority_identity: Identifier
governing_policy_identity: Digest | null (null only for the genesis authority_policy)
```

The generic record-content identity rule above uses the domain
`ksdft2effmass-development-authority-record`. Ordinals begin at zero and increase by
one; predecessor content identities form one complete chain. Every non-genesis
`governing_policy_identity` resolves to an earlier `authority_policy` record's
`record_content_identity`. A policy record additionally carries
`policy_revision: UInt64` and `policy_document_identity: Identifier`; it identifies an
externally accepted policy revision but cannot introduce executable expressions.

`record_kind` is exactly one of `authority_policy`, `task_authorization`,
`review_authorization`, `promotion_authorization`, `eligibility_reference`,
`authorization_use`, or `revocation`.

The named exact operation-binding variants are:

| Public DataObject | `binding_kind` and required fields |
|---|---|
| `DevelopmentTaskOperationBinding` | `binding_kind="task"`; `repository_root_identity`, `source_snapshot_identity`, `harness_state_identity`, `selection_revision`, `task_id`, `task_revision`, `starting_revision`, `candidate_revision`, `operation_id`, `attempt_id`, `idempotency_id`, `operation_kind`, canonical `permitted_paths: tuple[ResourcePath]`, canonical `requirement_ids: tuple[Identifier]`, `architecture_policy_identity`, `validator_profile_identity` |
| `DevelopmentReviewOperationBinding` | every task-binding field; `binding_kind="review"`; `review_subject_identity`, `review_result_identity` |
| `DevelopmentPromotionOperationBinding` | every task-binding field; `binding_kind="promotion"`; `decision_identity`, `candidate_composition_identity`, `predecessor_composition_identity`, `target_identity` |

Every identity-valued binding member is an `Identifier`; revision members are
`Identifier`; tuples are strictly sorted and duplicate-free. Task-binding
`operation_kind` is exactly `planning`, `implementation_planning`, `implementation`,
`verification`, `administrative_closeout`, or `repository_mutation`. Review binding
requires `operation_kind="review"`. Promotion binding requires exactly `promotion`,
`activation`, or `rollback`.

A `DevelopmentTaskAuthorization`,
`DevelopmentReviewAuthorization`, or `DevelopmentPromotionAuthorization` contains the
common record fields, `authorization_id: Identifier`, exactly one corresponding
immutable `operation_binding`, and `use_limit: UInt64` fixed to 1. The authorizer
requires field-for-field equality between the requested binding and the signed grant;
no security-relevant value is inherited from ambient state or derived after issuance.

The remaining concrete variants are:

| Record kind | Additional required fields |
|---|---|
| `authority_policy` | `policy_revision: UInt64`, `policy_document_identity: Identifier` |
| `eligibility_reference` | `eligibility_result_identity: Identifier`, `subject_identity: Identifier` |
| `authorization_use` | `authorization_id: Identifier`, `operation_id: Identifier`, `attempt_id: Identifier`, `idempotency_id: Identifier`, `operation_receipt_identity: Identifier` |
| `revocation` | `target_authorization_record_id: Identifier`, `reason_code: Identifier`, `replacement_authorization_record_id: Identifier | null` |

Each concrete variant requires only its common and listed keys and rejects keys owned
by another variant. Authorization IDs and record IDs are unique. One exact-attempt
authorization is single-use. A use is unique by the complete
`(authorization_id, operation_id, attempt_id, idempotency_id)` tuple and must match its
grant and immutable operation receipt. Revocation targets only an earlier task,
review, or promotion authorization; use and revocation records cannot themselves be
revoked. Replacement authorization, when present, must exist earlier and have the same
binding kind. Exhaustion is derived from one valid use and never stored mutably.

For every record, the verified head-envelope signer set must satisfy its exact
`DevelopmentIssuerAnchorBinding` and the record kind must be allowed by that binding.
The governing policy must exist earlier. Thus a cryptographically valid envelope from
a signer not authorized for a claimed issuer and kind fails closure. A static signed
snapshot still does not provide concurrent reservation; a target effect additionally
uses its owning compare-and-swap/idempotency contract.

### Snapshot and signed envelope

`DevelopmentAuthorityLedgerSnapshot` fields are:

```text
schema_version: 1
ledger_id: Identifier
snapshot_sequence: UInt64
predecessor_payload_identity: Digest | null (null only at sequence zero)
first_record_ordinal: 0
last_record_ordinal: UInt64
governing_policy_identity: Digest
records: nonempty tuple[DevelopmentAuthorityRecord]
```

It contains the complete history from ordinal zero, not a delta. Its
`payload_identity` is a runtime derived value: SHA-256 over exact canonical snapshot
bytes and is not embedded recursively in those bytes. All record predecessors,
policies, authorizations, uses, revocations, replacements, and referenced targets must
close in the snapshot.

`DevelopmentSignatureEntry` fields are `mechanism: "ed25519"`, `key_id: Digest`,
`signature_encoding: "raw-base64url"`, and `signature_bytes: Bytes64`. The signed
preimage is:

```text
b"ksdft2effmass-development-authority-snapshot\x00v1\x00"
+ uint64_big_endian(len(payload_bytes))
+ payload_bytes
```

`DevelopmentSignedAuthoritySnapshot` wire fields are
`schema_version: 1`, `canonicalization_version: "harness-canonical-json-v1"`,
`payload_encoding: "base64url-no-padding"`, `payload_bytes: unpadded base64url of the
exact canonical snapshot bytes`, and `signatures: nonempty tuple[DevelopmentSignatureEntry]`
strictly ordered by unique key ID. Its runtime `artifact_identity` is SHA-256 over the exact
canonical envelope bytes and is not embedded recursively. Re-signing preserves payload
identity but creates a different artifact identity.

### Reconstruction and authorization

`DevelopmentAuthorityReconstructionReceipt` fields are:

```text
schema_version: 1
receipt_identity: Digest
source_descriptor_identity: Digest
mode: "local" | "ci"
trust_configuration_pin_identity: Digest
trust_configuration_identity: Digest
trust_configuration_revision: UInt64
requested_head_artifact_identity: Digest
observed_head_artifact_identity: Digest | null
head_payload_identity: Digest | null
head_snapshot_sequence: UInt64 | null
verified_snapshot_count: UInt64
canonicalization_version: "harness-canonical-json-v1"
resolver_version: Identifier
source_status, configuration_status, content_status, signature_status,
threshold_status, snapshot_chain_status, record_chain_status,
reference_closure_status, issuer_policy_status, accepted_head_status:
    "passed" | "failed" | "not_reached"
verified_key_ids: canonical tuple[Digest]
diagnostics: canonical tuple[diagnostic]
```

`observed_head_artifact_identity`, payload identity, and sequence are null when bytes
were not observed or decoded far enough. Missing, unreadable, oversized, interrupted,
or over-count sources set `source_status="failed"`, every later status to
`not_reached`, observed identities to null when unavailable, no context, and at least
one stable diagnostic. Configuration anti-rollback failure similarly prevents source
and ledger acceptance. `verified_snapshot_count` counts only envelopes that completed
content and signature verification.

The receipt identity uses its domain-derived rule with `receipt_identity` null. It has
no context identity, breaking the receipt/context cycle. Diagnostics are strictly
ordered by `(code, subject_identity or "", detail)`. No secret, unrestricted
environment, or ambient path is retained.

`DevelopmentAuthorityContext` fields are `schema_version: 1`,
`context_identity: Digest`, `trust_configuration_pin_identity: Digest`,
`trust_configuration_identity: Digest`, `trust_configuration_revision: UInt64`,
`source_descriptor_identity: Digest`, `head_artifact_identity: Digest`,
`head_payload_identity: Digest`, `ledger_id: Identifier`,
`snapshot_sequence: UInt64`, `record_head_identity: Digest`,
`governing_policy_identity: Digest`, `receipt_identity: Digest`,
`records: nonempty tuple[DevelopmentAuthorityRecord]`, and
`resolver_version: Identifier`. Context identity uses its domain-derived rule with
`context_identity` null and the finalized receipt identity present. It never enters `HarnessState` or
`HarnessStateIdentity`.

`DevelopmentAuthorityContextResolutionResult` is a ResultObject with fields
`schema_version: 1`, `status: "resolved" | "failed"`,
`receipt: DevelopmentAuthorityReconstructionReceipt`, and
`context: DevelopmentAuthorityContext | null`. Resolved requires one context and every
receipt status passed; failed requires null context, at least one failed status, and at
least one diagnostic.

`DevelopmentOperationAuthorizationInput` fields are `schema_version: 1`,
`input_identity: Digest`, and exactly one `operation_binding` using the task, review,
or promotion variant defined above. Input identity uses the fixed
`ksdft2effmass-development-operation-authorization-input` domain with its own field
null. The requested binding must equal its signed authorization binding field for
field; no wildcard, subset, path prefix, latest revision, or omitted-identity matching
exists.

`DevelopmentOperationAuthorizationResult` fields are:

```text
schema_version: 1
result_identity: Digest
status: "authorized" | "denied" | "error"
input: DevelopmentOperationAuthorizationInput
context_identity: Digest
authorization_id: Identifier | null
authorization_record_content_identity: Digest | null
authorizer_version: Identifier
diagnostics: canonical tuple[diagnostic]
```

Result identity uses its domain-derived rule with `result_identity` null. Authorized
requires both authorization fields non-null, one exact unrevoked and unused matching
authorization, and an empty diagnostic tuple. Denied requires both authorization
fields null, a reliable context, and at least one diagnostic establishing an absent,
stale, used, revoked, or field-mismatched grant. Error requires both authorization
fields null and at least one diagnostic showing authorization or denial could not be
established. Only authorized is usable, and the target operation rechecks the complete
binding.

### Public imports, serializers, and exclusions

The supported import surface is `ksdft2effmass.harness`. It exports
`DevelopmentDecision`, its option and source-provenance records,
`DevelopmentDecisionSerializer`, every named trust/source/record/binding/snapshot/
signature/receipt/context/input/result type above,
`DevelopmentTrustConfigurationSerializer`,
`DevelopmentSignedAuthoritySnapshotSerializer`,
`DevelopmentAuthorityResolutionSerializer`,
`DevelopmentOperationAuthorizationSerializer`,
`DevelopmentAuthorityContextResolver`, and
`DevelopmentOperationAuthorizer`. Transitional v1 checkpoint imports remain one-way
compatibility only and are not aliases for the new nominal types.

`DevelopmentDecisionSerializer` owns only the accepted decision wire.
`DevelopmentTrustConfigurationSerializer` owns anchor, issuer-binding, configuration,
pin, and source-descriptor wires. `DevelopmentSignedAuthoritySnapshotSerializer` owns
record, binding, snapshot, signature-entry, and envelope wires.
`DevelopmentAuthorityResolutionSerializer` owns receipt, context, and closed context-
resolution-result wires. `DevelopmentOperationAuthorizationSerializer` owns operation
input and closed authorization-result wires. No DataObject owns `to_json`, `from_json`,
file access, or persistence.

`DevelopmentSignedAuthoritySnapshotSerializer` owns strict snapshot/envelope wire
mechanics. `DevelopmentAuthorityContextResolver` receives the exact protected configuration pin,
trust configuration, source descriptor, and bounded ordered tuple of envelope bytes; it
verifies configuration anti-rollback, canonical bytes, identities, every envelope's
Ed25519 signatures and issuer bindings, threshold, snapshot ancestry, accepted head,
sequence, and complete record/policy/reference closure. It performs
no discovery, fetching, signing, publication, credential access, or operation
authorization.

`DevelopmentOperationAuthorizer` receives an exact input and resolved context and
returns the closed authorization result. It performs no reconstruction, persistence,
reservation, target effect, or policy broadening. No signer or publisher is introduced
by this Task.

Checkpoint
`.pi/checkpoints/migration.v2.harness.decisions-authority.signed-ledger-contract.json`
requests acceptance, bounded correction, or deferral of this exact contract.

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
resolved topology, DevelopmentDecision, and signature checkpoints; acceptance of the
DevelopmentDecision wire amendment and exact signed-ledger contract; a separate
explicit implementation activation; the authorized and validated dependency and
lockfile mutation; exact source and trust-configuration identities; exact selection
and Task revisions; requested operation; permitted paths; and applicable starting and
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

Original checkpoint bytes and decision history are never rewritten. Cutover is
eligible only when identified results establish all of these exact conditions:

1. one migration result binds the frozen legacy source-snapshot identity, explicit
   migration-manifest identity, every source and successor artifact identity, and a
   zero-missing/zero-extra one-to-one count;
2. field comparison reproduces every legacy key, value, null, string, and array order,
   with only the accepted lifecycle and identity-availability mappings reported as
   intentional transformations;
3. canonical schema/runtime round trips, aggregate closure, public imports, Ruff,
   mypy, Sphinx, maintained conformance, and the focused software-verification suite
   pass for the exact candidate revision;
4. an identified consumer-inventory result reports zero canonical readers of the old
   checkpoint adapter/wire route and zero new imports of transitional local modules;
5. the selected compiler/configuration revision names only the v2 source root and
   rejects mixed legacy/v2 canonical input; and
6. the exact predecessor consumer/import revision, authority-composition revision,
   rollback target, and rollback validator identities are retained before cutover.

Legacy-route retirement additionally requires successful shadow comparison and one
read-only reconstruction of the frozen legacy snapshot. It never deletes legacy bytes.
Rollback before any native-v2 decision restores the exact retained predecessor
consumer/import and configuration revisions. After the first native-v2-only decision,
legacy write rollback is prohibited because it cannot represent the new record;
rollback is recovery/read-only until a separately accepted forward migration exists.
A rollback trigger is any failed cutover condition, incompatible/corrupt successor,
stale consumer, or failed reconstruction; no check chooses a winner or rewrites
history.

The migration result, consumer inventory, cutover candidate, and rollback validation
belong to this Task's implementation and closeout evidence. The exact predecessor and
candidate Git revisions are supplied implementation inputs, not inferred as “last” at
runtime. Protected ledger source, trust configuration, and reconstruction receipts
remain separate from `HarnessState` persistence and generated projections throughout
cutover and rollback.

## Residual limitations

- The DevelopmentDecision nested-wire clarification awaits the contract-amendment
  checkpoint, and the exact signed-ledger fields, canonical encoding, trust,
  reconstruction, and authorization contract awaits the signed-ledger-contract
  checkpoint.
- Project dependency and lockfile mutation remain unauthorized until that contract is
  accepted and implementation resumes. Trust-anchor rotation, protected signing and
  publication, credential handling, and accepted-head advancement remain separately
  protected operations even after implementation.
- Exact shared `HarnessState`, compiler, validator, and repository fields remain with
  their separately declared Tasks and may add prerequisite results without changing
  the ownership fixed here.
- No implementation, protected execution, dependency change, successor activation,
  publication, or release has occurred.
