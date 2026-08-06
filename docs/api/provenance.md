# Provenance API

The supported import path is `ksdft2effmass.provenance`. The package contains frozen,
slotted DataObjects and ResultObjects plus stateless ActionObjects. It performs no
filesystem, network, process, tool-discovery, workflow-engine, or scientific
calculation.

## Artifact, manifest, and lineage records

| Public object | Fields and owned invariant |
|---|---|
| `ArtifactIdentity` | `artifact_id`; 64-character lowercase hexadecimal `sha256`; built-in integer `byte_size` in $[0,2^{64}-1]$. Boolean and numeric-string sizes are rejected. |
| `ArtifactSpecification` | NFC root-relative POSIX lexical `logical_path`; identifier-valued `format`, `semantic_role`, and `retention_policy`. Retention metadata grants no deletion authority. |
| `ArtifactReference` | `identity`, `specification`, and `producer_manifest_id`. Its `artifact_id`, `logical_path`, `sha256`, and `byte_size` properties are exact views of nested state. It contains no deployment location and does not imply local presence. |
| `ArtifactLocation` | `artifact_id` and `kind`. `ROOT_RELATIVE` requires `root_id` and `path` and forbids `external_descriptor_id`; `EXTERNAL_DESCRIPTOR` requires the opaque approved descriptor and forbids `root_id`/`path`. It records observed or authorized deployment metadata without resolving it or asserting that bytes exist. |
| `RunManifest` | `manifest_id` is the attempt identity; the record also stores specification, sorted unique artifact/dependency IDs, actual UTC calendar timestamps, and `ManifestState`. `output_artifact_ids` are preallocated expected identities, so `DECLARED` may contain them before bytes or a terminal outcome exist. `DECLARED` has no `finished_at`; terminal `COMPLETE`/`FAILED` require it, not before `started_at`. Impossible calendar dates and direct self-dependency are rejected; this local check does not detect graph-wide cycles. Completion is not scientific acceptance. There are no raw argument or environment-value fields. |
| `ProvenanceRecord` | `provenance_id`, `manifest_id`, sorted unique direct `parent_provenance_ids`, and sorted unique `artifact_ids`; self-parenting is forbidden. |
| `LineageRelation` | Directed `parent_id` to distinct `child_id`, classified by `LineageKind`, and supported by `provenance_id`. |

`ArtifactLocationKind` is exactly `root_relative` or `external_descriptor`.
`ManifestState` is exactly `declared`, `complete`, or `failed`. `LineageKind` is
exactly `derived`, `representation`, or `retry`.

## External-tool records

| Public object | Fields and owned invariant |
|---|---|
| `ExternalToolIdentity` | Stable `tool_id` and `implementation_family`; the family is not a plugin or dynamic-import key. |
| `ExternalToolSpecification` | `specification_id`, `tool_id`, narrow portable lexical `requested_version`, and identifier-valued `executable_or_package_id`. |
| `DeclaredCapability` | `capability_id`, provider `tool_id`, `CapabilityKind`, narrow `name`, and project contract `specification_version`. |
| `InstallationObservation` | Correlated specification/tool identities, observed version and executable/package identifier, optional lowercase SHA-256, separately controlled environment-provenance record identity, and provenance. Observation is neither discovery nor verification. |
| `VerificationObservation` | Installation/capability identities, `VerificationStatus`, sorted unique evidence-artifact IDs, and provenance. Verification is software-capability evidence only; there is no raw detail field. |
| `ExternalExecutionRequest` | Request, correlation, and explicit attempt identities; optional `retry_parent_request_id`; tool/capability/installation identities; **separate** `authorization_id`; sorted unique sealed inputs and expected output roles; and provenance. A retry parent must differ from the new request, records lineage only, and grants no authorization. Recording a request does not execute it. |
| `ExternalExecutionResult` | Result/request/correlation/**attempt** identities, the sole status `COMPLETED`, sorted unique output artifact IDs, manifest, and provenance. Completion is not convergence or acceptance. |
| `ExternalExecutionFailure` | Failure/request/correlation/**attempt** identities, exact stage and code, sorted unique diagnostic paths, and provenance. There is no raw message field. It is a retained outcome, not an exception thrown by an adapter. |

`CapabilityKind` is `execute`, `parse`, `render`, or `transfer`.
`VerificationStatus` is `verified`, `rejected`, or `unavailable`.
`ExternalExecutionStatus` contains only `completed`.
`ExternalFailureStage` is `request_acceptance`, `execution`, or `result_capture`.
`ExternalFailureCode` is `unavailable`, `not_authorized`, `rejected`,
`interrupted`, `malformed_result`, or `internal_error`.

## Verification and correlation actions

| Public object | Contract |
|---|---|
| `ArtifactIdentityVerifier` | Stateless `execute(reference, observed_sha256, observed_byte_size)` compares caller-supplied, already observed values; it validates its direct scalar inputs but never observes bytes, computes a digest, or reads a file. |
| `ArtifactIdentityVerificationResult` | Stores the artifact ID and expected/observed digest and u64 size. It validates those intrinsic fields directly. Its non-constructor, non-wire `status` property derives `VERIFIED` exactly when both represented pairs match and `MISMATCH` otherwise. |
| `ExecutionOutcomeCorrelator` | Stateless `execute(request, outcome)` checks request, correlation, and attempt IDs for either a completed result or a structured failure without mutation or I/O. A correlated failure remains a failure; a completed result with an identity mismatch remains `MISMATCH`. |
| `ExecutionCorrelationResult` | Stores request and outcome IDs plus the issue tuple, and validates those intrinsic fields directly. Its non-constructor, non-wire `status` property derives `CORRELATED` exactly when `issues` is empty. Issues are unique and ordered exactly request-ID, correlation-ID, then attempt-ID mismatch. |

`ArtifactIdentityVerificationStatus` is `verified` or `mismatch`;
`CorrelationStatus` is `correlated` or `mismatch`; `CorrelationIssue` is
`request_id_mismatch`, `correlation_id_mismatch`, or `attempt_id_mismatch` in
that deterministic order, including when only a subset is present. All public
string-valued enums are Python `StrEnum` classes; Python record fields require
enum members rather than arbitrary strings.

These comparisons are pure represented-state operations. They do not establish
file observation, format validity, provenance truth, numerical acceptance,
scientific validation, uncertainty quantification, physical correctness, human
acceptance, or the validity of external execution.

## Strict JSON action and error

`ProvenanceJsonSerializer.serialize(record)` admits the 17 record/result types
listed in the version-1 schema and emits compact, lexicographically sorted-key,
UTF-8 JSON followed by exactly one LF. `deserialize(text)` accepts exactly one
version-1 record and constructs the corresponding immutable public object.
`ProvenanceJsonError`, a `ValueError`, reports strict decoding or contract
failure. It is the package's public error type.

Input rejects malformed JSON, duplicate or unknown keys, a BOM, missing keys,
unsupported versions/types/enums, floating-point lexical forms, non-finite
numbers, Unicode surrogate code points, and Python record-invariant violations.
There are no version-1 floating-point fields. Derived identity-verification and
correlation statuses are deliberately absent from JSON. The JSON Schema is
`specification/provenance/v1/provenance-v1.schema.json`; its golden valid and
invalid fixtures are in the neighboring `fixtures/` directories.

The schema owns wire structure: exact members, required/null forms, primitive
types, enums, identifier/digest/path patterns, numeric bounds, unique arrays,
and its declared conditional shapes. The strict parser additionally rejects
syntax forms JSON Schema does not observe, such as duplicate keys, BOMs, and
floating lexical forms. Each public record owns its intrinsic validation directly in its own constructor;
there is no shared callable field-validator API. Python constructors own NFC,
lexical tuple ordering, real calendar dates and timestamp order, direct non-self
manifest/provenance/lineage/retry relations, location-branch consistency, and
status derivation. Cross-record existence, graph-wide cycle detection, and
other repository-level relational validity require a separate boundary. Schema
conformance alone is therefore not construction of a valid Python record; the
serializer boundary applies both layers.

## Common scalar and collection rules

Portable identifiers match `[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`. Text is
nonempty scalar Unicode in NFC. Every documented deterministic identifier/path
collection is an exact built-in tuple in lexical order with no duplicates; JSON
uses arrays with the same order.

Logical and diagnostic paths, and root-relative location paths, are lexical NFC
POSIX paths relative to an explicitly identified root. They reject absolute and
Windows-drive forms, backslashes, empty/`.`/`..` components, repeated or trailing
slashes, Windows device components, and C0/C1/line controls. Validation does not
query a filesystem, resolve symbolic links, infer a current working directory,
or prove local presence. External descriptors are opaque approved identifiers,
not URIs carrying credentials.

## Scope

The public records provide no generic raw argument, environment-value,
verification-detail, or failure-message channel. Credentials remain
categorically prohibited, as are open files, subprocess or scheduler handles,
mutable clients, closures, SNAKES objects, and live tool instances. Identifier,
version, and path validation is lexical and cannot prove that an opaque value is
not a secret: callers must never encode credentials, tokens, private keys, or
other secrets into those fields or referenced records. Future QE and Wannier90
work owns concrete scientific mappers, parsers, and adapters that
consume requests and return results/failures outside guard evaluation. This seam
is deliberately not a plugin framework, backend registry, resolver framework,
or authorization mechanism.

This API is supported by software verification only. Numerical verification,
scientific validation, and uncertainty quantification are not applicable to this
nonnumerical record/serialization task and no such claims are made.
