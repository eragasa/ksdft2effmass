# `Periodic1DIsolatedBandEncodedDocuments`

## Responsibility

This frozen, slotted DataObject owns exactly two ordered fields:

1. nonempty exact built-in `bytes` for the version-one isolated campaign input; and
2. nonempty exact built-in `bytes` for the retained isolated campaign result.

It preserves caller-supplied byte objects without decoding, normalization, canonical
re-encoding, coercion, or copying. Byte subclasses, strings, mutable byte arrays, and
empty values fail closed. A short `__post_init__` delegates the same exact payload check
for both fields.

## Scientific and provenance boundary

The record is an encoded-document owner, not a physical model, finite Hamiltonian,
retained space, frame, retained or represented operator, hopping representation,
effective model, decoded result, provenance record, convergence result, uncertainty
result, or acceptance decision. SHA-256 establishes exact content identity only.
Campaign correlation, schema-specific decoding, numerical reconstruction, and
scientific adoption are separate Actions.

## Code and public routes

| Surface | Mapping |
|---|---|
| Definition | `python/src/ksdft2effmass/periodic1d/campaign/isolated/encoded_documents.py` |
| Qualified class | `ksdft2effmass.periodic1d.campaign.isolated.encoded_documents.Periodic1DIsolatedBandEncodedDocuments` |
| Leaf facade | `ksdft2effmass.periodic1d.campaign.isolated.Periodic1DIsolatedBandEncodedDocuments` |
| Campaign facade | `ksdft2effmass.periodic1d.campaign.Periodic1DIsolatedBandEncodedDocuments` |
| Transitional aliases | None |

## Retained identities

The maintained compact files remain unchanged:

| Artifact | SHA-256 |
|---|---|
| `calculations/research-monograph/periodic-1d/input.json` | `ae17de790380dee76693e984b96fbb22773a40440e267d3e77b4543cafaad6fb` |
| `calculations/research-monograph/periodic-1d/result.json` | `37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c` |

These values are also bound to the maintained `SHA256SUMS` catalog. They do not
identify authorship or prove that any particular software execution produced the files.

## Evidence

Routine class-owned evidence:

- `TestPeriodic1DIsolatedBandEncodedDocuments::test_contract__owns_exact_fields_and_preserves_synthetic_bytes`;
- `TestPeriodic1DIsolatedBandEncodedDocuments::test_construction__rejects_wrong_and_empty_payload_representations`;
- `TestPeriodic1DIsolatedBandEncodedDocuments::test_construction__is_frozen_and_slotted`.

Artifact-owned integration evidence:

- `TestPeriodic1DIsolatedBandEncodedDocumentArtifacts::test_retained_artifacts__preserve_exact_bytes_and_catalog_identities`;
- `TestPeriodic1DIsolatedBandEncodedDocumentArtifacts::test_public_routes__share_implementation_without_transitional_aliases`; and
- `TestPeriodic1DIsolatedBandEncodedDocumentArtifacts::test_public_import__does_not_initialize_transitional_campaign_package`.

Both modules are under
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/isolated/` and
are registered in the colocated ownership metadata. A pass establishes only the
specified structural, route, and content-identity behavior. It does not establish
decoded correctness, execution provenance, convergence, physical adequacy, scientific
validation, uncertainty quantification, or acceptance.

Original local work under the repository license.
