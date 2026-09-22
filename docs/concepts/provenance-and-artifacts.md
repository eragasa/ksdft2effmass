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

## Represented external-tool lifecycle layers

The lifecycle records represent adjacent but different claims. A tool identity
and specification are declarations, not observations. An installation
observation stores metadata acquired elsewhere, not a capability-verification
result. A verification observation stores the represented capability outcome
and evidence-artifact identities, but grants no execution authorization. An
execution request refers to a separate authorization and performs no work. A
result or failure stores an already-observed boundary outcome; completion,
failure classification, and request/outcome correlation are separate facts.
Later adapter interpretation of sealed artifacts is outside this lifecycle
record seam.

Internally, `external_tools.py` owns declarations, `tool_observations.py` owns
observations, and `external_execution.py` owns requests and outcomes. These are
implementation ownership boundaries, not supported direct-import paths. The
only supported public import path remains `ksdft2effmass.provenance`; there was
no supported `ksdft2effmass.provenance.tools` module-path contract before
`tools.py` was removed.

## DataObject/ActionObject boundary

All records and results are frozen, slotted value objects. Each decomposed
record class validates its intrinsic represented invariants directly in its own
`__post_init__`, without shared or private validator helpers. An action validates
its direct scalar inputs in `execute`. Cross-record constructor dispatch is not
part of the contract.

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

Declaration, observation, request, result, and failure fields are stored
represented state. Verification and correlation result statuses are instead
derived properties of exact represented state, not stored constructor or wire
fields. `ExternalExecutionOutcome` is only an internal typing alias over result
and failure; it adds no wrapper or stored state.
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

The internal dependency direction is acyclic: the new record modules do not
import `actions` or `serialization`; `actions` imports only the exact record
families it consumes, and `serialization` imports the exact public record and
result types it maps. This direction prevents validation or wire policy from
becoming hidden ownership of the record layers.

Durable values categorically exclude credentials, open files,
process/scheduler handles, mutable clients, closures, live external-library
instances, and SNAKES runtime objects. The P2 records expose no generic raw
argument, environment-value, verification-detail, or failure-message channel.
Opaque identifiers, lexical versions, and paths cannot be semantically proven
secret-free, so callers must not encode credentials, tokens, private keys, or
other secrets in them or in referenced records.

## Workflow-owned v2 artifact records

The public `ksdft2effmass.workflows` package now also owns the initial v2
artifact-manifest and closed producer-provenance records documented in
[`workflow-artifacts.rst`](workflow-artifacts.rst). Those records are distinct
from the transitional v1 records described on this page. Equal-looking
identities are not aliases or interchangeable values; migration requires an
explicit adapter and separate compatibility authority.

## Evidence boundary

Exact digest/size agreement establishes represented-byte identity only; it is
not evidence that this action observed a file. Lifecycle verification
establishes a declared software capability only. Correlation establishes
request/result-or-failure identity agreement only, independently of completion.
These claims exclude file observation, format validity, provenance truth,
numerical acceptance, scientific validation, uncertainty quantification,
physical correctness, human acceptance, and external-execution validity. P2
evidence is software verification only.
