# Provenance and artifacts

Use `ksdft2effmass.provenance` to represent portable sealed-artifact identity,
deployment metadata, manifests, provenance, lineage, and strict version-1 JSON.
The package records values supplied by controlled boundaries; it does not find,
read, write, transfer, or delete artifacts.

## Construct a portable reference

```python
from ksdft2effmass.provenance import (
    ArtifactIdentity,
    ArtifactReference,
    ArtifactSpecification,
)

reference = ArtifactReference(
    identity=ArtifactIdentity(
        artifact_id="qe-output-001",
        sha256="0" * 64,
        byte_size=128,
    ),
    specification=ArtifactSpecification(
        logical_path="outputs/qe.out",
        format="text",
        semantic_role="execution-log",
        retention_policy="campaign-source",
    ),
    producer_manifest_id="manifest-001",
)
```

The digest and size are stable expected byte identity. `byte_size` is a built-in
integer from 0 through $2^{64}-1$; booleans and numeric strings are rejected.
The logical path is NFC, root-relative, POSIX, and lexical. It is not resolved
against the current directory and does not prove that a file exists.

## Record deployment separately

```python
from ksdft2effmass.provenance import ArtifactLocation, ArtifactLocationKind

location = ArtifactLocation(
    artifact_id=reference.artifact_id,
    kind=ArtifactLocationKind.ROOT_RELATIVE,
    root_id="campaign-root-01",
    path="run-001/outputs/qe.out",
)
```

A root-relative location requires an explicit approved root. An external
location instead uses `EXTERNAL_DESCRIPTOR` and an opaque approved
`external_descriptor_id`; it has no `root_id` or `path`. Neither representation
contains credentials or implies local presence, accessibility, authorization,
or verified content. Obtain observations and authorization at their owning
boundaries, then use `ArtifactIdentityVerifier` to compare already computed
SHA-256 and size values.

Paths reject absolute/drive syntax, backslashes, repeated/trailing separators,
`.`/`..`, Windows device names, non-NFC text, and control characters. Symbolic
links and filesystem state are never consulted.

## Preserve attempt history and relationships

`RunManifest` records one attempt—identified by `manifest_id`—and distinguishes
`DECLARED`, `COMPLETE`, and `FAILED`. A terminal manifest has `finished_at`; a
declared one does not. Timestamps must name real UTC calendar seconds, and finish
must not precede start. Completion is process history, not solver convergence or
scientific acceptance. An external retry uses new request and `attempt_id`
values, may name the distinct prior request with `retry_parent_request_id`,
requires separate authorization, and retains the failed attempt.

`ProvenanceRecord` joins a manifest to covered artifact IDs and direct parent
provenance IDs. `LineageRelation` records a directed `DERIVED`,
`REPRESENTATION`, or `RETRY` edge. Identifier tuples must be lexically sorted and
unique. These records do not by themselves establish representation,
basis/gauge, energy-reference, unit, geometry, or physical compatibility.

## Serialize strict version-1 JSON

```python
from ksdft2effmass.provenance import ProvenanceJsonSerializer

serializer = ProvenanceJsonSerializer()
text = serializer.serialize(reference)
assert text.endswith("\n")
assert serializer.deserialize(text) == reference
```

Output is compact sorted-key UTF-8 JSON with exactly one trailing LF. Input is
strict: duplicate/unknown/missing keys, BOMs, malformed JSON or Unicode,
surrogates, floating-point and non-finite numbers, wrong versions/types/enums,
and object-invariant failures raise `ProvenanceJsonError`. Arrays that represent
deterministic sets remain sorted and duplicate-free. The schema checks wire
structure; the Python boundary additionally owns intrinsic and relational rules
including NFC, lexical ordering, actual calendar validity, timestamp ordering,
non-self relations, location alternatives, and derived statuses. Schema
acceptance alone is not a valid Python record. See the [public API contract on the development
branch](https://github.com/eragasa/ksdft2effmass/blob/dev/docs/api/provenance.md)
and `specification/provenance/v1/provenance-v1.schema.json`.

Large densities, wavefunctions, QE `.save` trees, restart state, FFT grids, and
Wannier bridge files remain external immutable artifacts. Retention metadata
does not authorize deletion. Durable records must not contain credentials, open
files, subprocess/scheduler handles, mutable clients, closures, live library
instances, or SNAKES objects. P2 exposes no generic raw argument,
environment-value, verification-detail, or failure-message field. Because
lexical validation cannot detect a secret hidden in an opaque identifier,
version, or path, callers must never encode credentials, tokens, private keys,
or other secrets in those fields or referenced records.

The implemented checks are software verification only. They make no numerical-
verification, scientific-validation, or uncertainty-quantification claim.
