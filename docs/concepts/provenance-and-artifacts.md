# Provenance and artifact concepts

## Identity, specification, and location are different claims

An `ArtifactIdentity` states the expected identity of sealed bytes: stable
`artifact_id`, exact lowercase SHA-256 digest, and exact unsigned-64-bit byte
size. An `ArtifactSpecification` states their portable logical path, format,
semantic role, and retention policy. `ArtifactReference` joins those stable
expected identity/provenance facts to the producer manifest.

`ArtifactLocation` instead states observed or authorized deployment metadata for
that artifact identity. It is either an explicit approved `root_id` plus a
root-relative lexical path, or an opaque approved external descriptor ID. A
location can change while the reference remains unchanged. Conversely, a
reference or location record does **not** assert that bytes are locally present,
accessible, authorized for use, or verified. Resolution, access, observation,
and digest computation occur at separately controlled boundaries.

This separation avoids treating a mutable machine path or storage service as
scientific identity. It also prevents a logical path from being interpreted as
an ambient-current-directory path.

## Manifests, provenance, and lineage

A `RunManifest` records one declared or terminal attempt; its `manifest_id` is
the attempt identity. Inputs, outputs, and dependencies are identities rather
than embedded payloads. Output IDs are preallocated expected identities, so a
`DECLARED` manifest may name expected outputs before their bytes exist or an
attempt reaches a terminal outcome. Timestamps identify actual UTC calendar
seconds, not merely strings matching a numeric shape. The record rejects a
direct dependency on its own `manifest_id`; graph-wide dependency cycles remain
a relational concern outside one manifest. `COMPLETE` means that the represented
execution attempt completed; it does not mean solver convergence,
numerical-protocol acceptance, or scientific acceptance. A failed attempt
remains durable. An `ExternalExecutionRequest` carries its own `attempt_id` and
an optional distinct `retry_parent_request_id`; the parent records lineage only,
never authorization. Every result or failure copies the request, correlation,
and attempt identities.

A `ProvenanceRecord` associates a manifest with covered artifacts and direct
parent provenance records. A `LineageRelation` adds an explicit directed
`DERIVED`, `REPRESENTATION`, or `RETRY` relation supported by a provenance ID.
These records preserve joins without claiming that identifiers alone prove
basis, gauge, energy-zero, unit, geometry, pseudopotential, or physical
compatibility. A future comparison join must establish its separately declared
representation and common-parent requirements.

## DataObject/ActionObject boundary

All records and results are frozen, slotted value objects. Each owning class
validates its intrinsic represented invariants directly in construction or,
for an action's direct scalar inputs, in `execute`; removed module-level helper
callables are not a public validation layer. Cross-record constructor dispatch
is also not part of the contract.

`ArtifactIdentityVerifier` accepts a digest and size that a caller has already
observed elsewhere and compares their represented values against a reference.
The word *observed* identifies the role of those inputs; the action does not
observe bytes, compute a digest, open a path, or perform file I/O.
`ExecutionOutcomeCorrelator` compares request, correlation, and attempt
identities for either a result or a structured failure without interpreting the
outcome. Its issue tuple is the exact mismatching subset in request-ID,
correlation-ID, then attempt-ID order. A matching failure is `CORRELATED`; a
completed result with a mismatching join identity is `MISMATCH`, because
completion and identity correlation are separate claims.

Verification and correlation result statuses are derived properties of exact
represented state, not stored constructor or wire fields.
`ProvenanceJsonSerializer` owns the strict version-1 wire boundary. These
ActionObjects have no fields or retained policy: they are stateless and perform
no I/O, execution, mutation, or hidden deployment or scientific policy. Public
string-valued enum vocabularies use `StrEnum`.

The schema owns structural wire constraints; strict JSON parsing also rejects
syntax-level defects, while Python constructors own intrinsic and record-local
relational checks such as NFC, deterministic ordering, actual calendar validity,
timestamp ordering, direct non-self relations, and derived statuses. Cross-record
existence and graph-wide acyclicity require a separate repository or workflow
boundary. Schema acceptance alone does not establish all runtime relational
validity or Python invariants.

Durable values categorically exclude credentials, open files,
process/scheduler handles, mutable clients, closures, live external-library
instances, and SNAKES runtime objects. The P2 records expose no generic raw
argument, environment-value, verification-detail, or failure-message channel.
Opaque identifiers, lexical versions, and paths cannot be semantically proven
secret-free, so callers must not encode credentials, tokens, private keys, or
other secrets in them or in referenced records.

## Evidence boundary

Exact digest/size agreement establishes represented-byte identity only; it is
not evidence that this action observed a file. Lifecycle verification
establishes a declared software capability only. Correlation establishes
request/result-or-failure identity agreement only, independently of completion.
These claims exclude file observation, format validity, provenance truth,
numerical acceptance, scientific validation, uncertainty quantification,
physical correctness, human acceptance, and external-execution validity. P2
evidence is software verification only.
