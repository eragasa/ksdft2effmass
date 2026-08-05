H2-HC01 decision: Option A.

Authorize the bounded upstream H1/H3 correction that moves manifest relational validity from strict record construction/deserialization to `ValidateResourceManifest`.

Preserve this response verbatim.

# Required boundary recovery

The H2 pending checkpoint and current coherent conflict state were not committed or pushed before waiting. Recover the required durable boundary before changing the checkpoint or implementing the resolution.

1. Preserve all current H2 implementation, tests, documentation, evidence, and pending checkpoint exactly as they currently stand.
2. Verify the pending checkpoint schema, ownership scope, unrelated-work preservation, and `git diff --check`.
3. Commit only the authorized H2 conflict boundary, including the pending `H2-HC01` record.
4. Push it to `origin/dev` and verify the remote identity.
5. Do not include unrelated files.
6. Do not rewrite or amend this recovered checkpoint commit afterward.

After that boundary is durable:

1. record Option A and this response verbatim;
2. update the authorized correction scope;
3. commit and push the checkpoint-resolution boundary separately;
4. only then implement the authorized correction.

# Accepted semantic boundary

Version-1 record construction and deserialization own:

- field presence;
- exact semantic types;
- enum membership;
- scalar bounds;
- lexical path validity;
- immutable tuple storage;
- field-local uniqueness where it does not require comparing distinct records;
- deterministic canonical ordering;
- structural generic/local layer shape.

`ValidateResourceManifest` owns relational manifest validity, including:

- duplicate resource IDs across manifest entries;
- duplicate resource paths across manifest entries;
- a resource depending on itself;
- missing dependency identities;
- dependency cycles;
- generic-to-local dependency edges;
- incompatible resource kind or format version;
- generic/local manifest mismatch;
- forbidden local replacement of a generic ID or path.

A structurally valid candidate manifest may therefore be constructed and deserialized even when it is not a valid usable manifest.

Construction does not imply manifest acceptance, authorization, resolvability, or capability validity.

# Exact corrections

Apply the smallest consistent H1/H3/H2 correction.

## ResourceReference

Retain intrinsic validation of:

- field types;
- identifier syntax;
- resource kind;
- format version;
- `ResourcePath`;
- content identity;
- tuple storage;
- dependency-ID uniqueness and canonical ordering.

Move this cross-field rule out of construction/deserialization:

```text
resource_id must not occur in dependency_ids
```

`ValidateResourceManifest` must diagnose that self-edge using the accepted capability-specific resource issue semantics, normally the dependency-cycle issue unless the accepted issue registry already defines a more specific resource code.

Do not introduce a new issue code without a separate demonstrated need.

## ResourceManifest

Retain intrinsic validation of:

- field types;
- manifest identity and version;
- layer;
- generic/local `extends_manifest_id` structural relationship;
- nonempty immutable resource tuple;
- canonical resource ordering.

Move these cross-entry rules to `ValidateResourceManifest`:

```text
resource IDs are unique
resource paths are unique
```

Canonicalization may sort entries while preserving duplicates so the validator can report them deterministically.

## Deserialization

`DeserializeJsonRecord` must:

- continue rejecting malformed JSON, duplicate JSON object keys, unknown fields, wrong field types, invalid scalar values, and intrinsic record violations;
- successfully deserialize structurally valid manifest candidates containing relational defects;
- not claim that successful deserialization establishes manifest validity.

## Manifest validation

`ValidateResourceManifest` must accept the candidate records and emit the existing deterministic `PIH.RESOURCE.*` findings with the accepted precedence and ordering.

Downstream actions such as `ResolveResource` and `ValidateSkillResources` must first propagate manifest-validation failure and must not use an invalid manifest.

# H1 correction

Update only the directly conflicting accepted H1 contract material:

- `ResourceReference` invariant ownership;
- `ResourceManifest` invariant ownership;
- `DeserializeJsonRecord` semantics;
- `ValidateResourceManifest` semantics;
- affected interface/field traceability;
- affected issue precedence and action descriptions;
- H2 test obligations.

Record this as a bounded version-1 pre-acceptance correction discovered during H2 implementation. Do not reopen unrelated H1 interfaces or create a new contract version because no accepted H2 implementation or released harness package yet exists.

# H3 correction

Update only affected H3 resources:

- schema descriptions;
- semantic-invariant fixtures and oracle entries;
- resource-resolution fixtures and oracle entries;
- canonical vectors if their expected behavior changes;
- resource manifests and byte identities;
- H3-to-H2 handoff identities;
- H3 validator expectations;
- affected documentation;
- checksum catalog.

In particular, change the self-dependency fixture from:

```text
DeserializeJsonRecord → PIH.WIRE.INVALID_VALUE
```

to:

```text
DeserializeJsonRecord → success
ValidateResourceManifest → relational PIH.RESOURCE.* failure
```

Ensure duplicate-ID and duplicate-path fixtures likewise deserialize successfully before manifest validation reports their capability-specific issues.

Do not alter unrelated accepted H3 resources.

# H2 correction and completion

Update implementation and independent tests to enforce the corrected boundary.

The test writer must demonstrate:

1. structurally valid relationally invalid candidates can be constructed;
2. they round-trip through accepted serialization where applicable;
3. successful construction/deserialization does not imply manifest validity;
4. `ValidateResourceManifest` reports duplicate ID;
5. `ValidateResourceManifest` reports duplicate path;
6. `ValidateResourceManifest` reports self-dependency/cycle;
7. downstream resource actions short-circuit after manifest failure;
8. issue precedence and deterministic ordering match H1;
9. accepted H3 fixtures agree with Python behavior.

Also complete the remaining deterministic H2 hygiene:

- format the remaining H2 test;
- resolve the eight H2 test typing errors without weakening typing;
- rerun the focused and full suites;
- ensure all previously identified review findings remain corrected.

# Review boundary

This resolution authorizes one focused upstream-contract correction and integrated re-review. It does not authorize another open-ended review cycle.

The existing independent reviewers must inspect the final corrected boundary for:

- intrinsic versus relational ownership;
- H1/H3/H2 agreement;
- public construction semantics;
- validator diagnostics;
- downstream short-circuit behavior;
- test independence and completeness;
- generic/local dependency direction.

If a uniquely determined defect remains, correct it within this bounded resolution. If another genuine protected design choice appears, stop at a new checkpoint.

# Validation

Run:

- H2 focused software-verification suite;
- H2 completion validator;
- H3 resource validator;
- canonical-vector agreement;
- schema and fixture agreement;
- Ruff format and lint;
- source-and-test mypy;
- full Python suite;
- public import audit;
- package build and clean-install/import checks;
- Sphinx warnings-as-errors;
- ownership validation;
- checkpoint validation;
- H1/H3/H2 checksum and handoff verification;
- dependency and lockfile nonmutation;
- unrelated-work preservation;
- `git diff --check`.

The sdist README warning should be corrected only if uniquely attributable to H2 packaging and within an already authorized path. Otherwise record it as a nonblocking existing packaging limitation.

# Scope fence

Do not:

- add public interfaces;
- create project-local H4 Python;
- implement SQLite;
- activate H4, H5, or P2;
- retire or cut over live skills;
- add dependencies or modify lockfiles;
- modify CPN or scientific code;
- run external, numerical, or scientific calculations;
- touch unrelated work.

# Completion

After the corrected H1/H3/H2 boundary passes validation and final independent review:

1. update the H2 task and harness chain;
2. create the single final H2 acceptance checkpoint;
3. commit and push the validated boundary;
4. verify the remote identity;
5. stop for human acceptance without activating H4.

Report the recovered checkpoint commit, resolution commit, corrected semantic boundary, affected H1/H3/H2 files, validation results, final review results, remaining limitations, final checkpoint, and remote commit identity.
