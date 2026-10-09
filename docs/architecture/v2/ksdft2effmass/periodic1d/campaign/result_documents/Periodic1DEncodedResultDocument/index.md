# `Periodic1DEncodedResultDocument`

## Purpose and owner

`Periodic1DEncodedResultDocument` is the row-045 immutable supporting record for one
complete periodic-1D encoded result wire. Its defining implementation is
`python/src/ksdft2effmass/periodic1d/campaign/result_documents.py`; the reviewed
facade import is:

```python
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DEncodedResultDocument,
    Periodic1DEncodedResultJsonSerializer,
    Periodic1DEncodedResultKind,
)
```

The former underscored campaign and research-monograph facades do not re-export these
owners. The former `Periodic1DRetainedResultDocument`,
`Periodic1DRetainedResultJsonSerializer`, and `Periodic1DRetainedResultKind` names are
retired rather than aliased. Periodic-specific `Periodic1DJsonArray`,
`Periodic1DJsonObject`, `Periodic1DJsonScalar`, and `Periodic1DJsonValue` names are also
retired; reusable immutable JSON ownership is
[`ksdft2effmass.serialization.json.immutable`](../../../../serialization/json/immutable/index.md).
The serializer's former `decode` and `encode` forwarding methods are absent;
`deserialize` and `serialize` are the sole reviewed methods.

## Immutable contract

The record owns, in order:

1. one exact `Periodic1DEncodedResultKind`;
2. schema version, record identity, evidence-status text, and optional calculation
   status decoded from the top-level object;
3. the complete shared immutable `ImmutableJsonObject` tree;
4. the exact nonempty built-in `bytes` supplied to the decoder; and
5. the lowercase SHA-256 digest derived from those exact source bytes.

Construction rejects a nonexact byte representation, empty bytes, malformed digest,
digest/source mismatch, unsupported version, empty identity or evidence status, root
field mismatch, or an unsupported calculation-status representation. The frozen,
slotted record owns no repository path and performs no filesystem access.

`ImmutableJsonArray`, `ImmutableJsonObject`, and `ImmutableJsonCodec` recursively admit
only JSON null, exact Boolean, exact integer, finite float, string, immutable array, and
immutable object values. They preserve JSON meaning; they do not coerce numeric strings
or assign scientific metadata. `StrictJsonDecoder` owns duplicate-key and nonfinite
extension rejection, so periodic result code does not reproduce generic parser
mechanics.

## Wire kinds

The explicit stable wire values are:

| enum member | wire value | bounded interpretation |
|---|---|---|
| `ISOLATED_BAND` | `isolated_band` | isolated-band result JSON |
| `STRESS` | `stress` | historical reduction-challenge/stress result JSON |
| `COMPOSITE` | `composite` | composite result JSON |
| `WANNIER90` | `wannier90` | Wannier90 result JSON |
| `WANNIER90_PRECONDITIONED` | `wannier90_preconditioned` | preconditioned Wannier90 result JSON |
| `WANNIER90_CONVERGENCE_ATTEMPT` | `wannier90_convergence_attempt` | stopped convergence-attempt JSON |

The kind is caller-supplied and checked at serialization. It is not inferred from the
filename, path, record identity, decoded fields, dimensions, or any scientific
property.

## Source bytes and canonical bytes

For source bytes \(b\), deserialization retains \(b\) exactly and binds

\[
  d = \operatorname{SHA256}(b).
\]

The digest establishes content identity only. It does not establish authorship,
execution provenance, correctness, native artifact presence, convergence,
qualification, or acceptance.

`serialize` emits a deterministic compact JSON encoding with sorted keys. These
canonical bytes may differ from the retained source bytes because insignificant source
formatting is not part of the decoded tree. Deserializing the canonical bytes must
recover the same immutable tree and top-level identity, while its source bytes and
source digest correctly identify the canonical wire itself.

## Retained evidence

Artifact-owned evidence binds these maintained files under
`calculations/research-monograph/periodic-1d/`:

| file | SHA-256 |
|---|---|
| `result.json` | `37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c` |
| `stress-result.json` | `5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394` |
| `composite-result.json` | `9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f` |
| `wannier90-result.json` | `d167294da9ebb53173b91fa69f089900f11e03917969bc028b9c0e69db951535` |
| `wannier90-preconditioned-result.json` | `c4d6d32f8a52e93c447424b49b649e63fa036117bf88a4f8af6ed4e1d270316c` |
| `wannier90-convergence-attempt.json` | `54dc87a1f341a4f57116dcdf456a060e8d7b482b92d9596c6022cbe647347b3a` |

The maintained `SHA256SUMS` catalog independently lists all six identities. This row
reads the retained bytes but does not execute Quantum ESPRESSO, Wannier90, or a campaign
runner.

## Verification mapping

Shared immutable JSON evidence:

- `SV-SERIALIZATION-IMMUTABLE-JSON-001` through
  `SV-SERIALIZATION-IMMUTABLE-JSON-004` verify exact recursive immutable containers,
  strict wire rejection, canonical round trips, defensive conversion, and explicit
  binary64 overflow at
  `python/tests/software_verification/ksdft2effmass/serialization/test__ImmutableJsonCodec.py`.

Row-specific routine class-owned evidence:

- `SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-001` — explicit enum values, ordered fields, and
  removal of retired result names, periodic JSON names, and forwarding methods;
- `SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-002` — exact source-byte retention and distinct
  canonical JSON semantics;
- `SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-003` — fail-closed source/digest correlation and
  operational immutability; and
- `SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-004` — exact explicit kind and cross-kind
  rejection.

Exact pytest nodes:

```text
python/tests/software_verification/ksdft2effmass/periodic1d/campaign/test__Periodic1DEncodedResultJsonSerializer.py::TestPeriodic1DEncodedResultJsonSerializer::test_contract__defines_explicit_wire_kinds_and_document_fields
python/tests/software_verification/ksdft2effmass/periodic1d/campaign/test__Periodic1DEncodedResultJsonSerializer.py::TestPeriodic1DEncodedResultJsonSerializer::test_methods__preserve_source_bytes_and_emit_canonical_json
python/tests/software_verification/ksdft2effmass/periodic1d/campaign/test__Periodic1DEncodedResultJsonSerializer.py::TestPeriodic1DEncodedResultJsonSerializer::test_construction__rejects_unbound_or_mutable_source_identity
python/tests/software_verification/ksdft2effmass/periodic1d/campaign/test__Periodic1DEncodedResultJsonSerializer.py::TestPeriodic1DEncodedResultJsonSerializer::test_methods__reject_wrong_or_mismatched_wire_kinds
```

Artifact-owned integration evidence:

- `SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-ARTIFACT-001` — all six exact source files,
  digests, catalog entries, kinds, record identities, nested shapes, and canonical
  semantic reconstruction; and
- `SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-ROUTE-001` — canonical facade identity and absence
  of retired result names and compatibility methods.

Exact pytest nodes:

```text
python/tests/software_verification/ksdft2effmass/periodic1d/campaign/test__integration__periodic_1d_encoded_result_document_artifacts.py::TestPeriodic1DEncodedResultDocumentArtifacts::test_retained_artifacts__preserve_exact_sources_and_catalog_identities
python/tests/software_verification/ksdft2effmass/periodic1d/campaign/test__integration__periodic_1d_encoded_result_document_artifacts.py::TestPeriodic1DEncodedResultDocumentArtifacts::test_public_routes__share_defining_classes_without_retired_names
```

The first integration node is parameterized once per named wire.

## Claim boundary

This record and its tests establish immutable JSON-level persistence compatibility and
content identity. They do not decode campaign-specific scientific objects, authenticate
input/result correlation, prove a calculation ran, demonstrate that a native Wannier90
file exists, establish localization or numerical convergence, validate a physical
model, quantify uncertainty, or approve evidence. Those responsibilities remain with
the campaign-specific correlation, verification, qualification, and decision owners.
