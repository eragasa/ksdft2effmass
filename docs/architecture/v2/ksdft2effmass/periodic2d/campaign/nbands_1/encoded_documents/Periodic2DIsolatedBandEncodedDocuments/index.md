# `Periodic2DIsolatedBandEncodedDocuments`

## Purpose and migration status

This implemented immutable DataObject is the row-046 replacement for the retired
`Periodic2DIsolatedBandCampaignModel`. Its name states its bounded responsibility: it
owns exact encoded input and result documents for the retained version-one isolated
periodic-2D campaign. The former class name and source module
`python/src/ksdft2effmass/periodic2d/campaign/nbands_1/retained.py` are absent rather
than retained as aliases or forwarding routes.

The class already resides under the canonical
`ksdft2effmass.periodic2d.campaign.nbands_1` campaign family. Row 067 owns later
campaign decomposition and must not change these bytes or reinterpret this container as
a scientific model.

## Public contract and reviewed routes

The constructor accepts `input_payload` and `result_payload` and returns one frozen,
slotted DataObject. It has no decoding, filesystem, correlation, verification,
calculation, or scientific-adoption method.

Supported reviewed import routes are:

- `ksdft2effmass.periodic2d.campaign.nbands_1.Periodic2DIsolatedBandEncodedDocuments`;
- `ksdft2effmass.periodic2d.campaign.Periodic2DIsolatedBandEncodedDocuments`; and
- `ksdft2effmass.periodic2d.Periodic2DIsolatedBandEncodedDocuments`.

All routes expose the defining class object and none exposes the retired name.

## State and invariants

| Field | Representation | Meaning |
|---|---|---|
| `input_payload` | Exact nonempty built-in `bytes` | Encoded isolated-band campaign definition |
| `result_payload` | Exact nonempty built-in `bytes` | Encoded retained isolated-band campaign result |

Field order is stable as listed. Construction rejects non-`bytes` values, including
`bytes` subclasses, with `TypeError`, and empty exact bytes with `ValueError`. Each
supplied byte object is retained without decoding, re-encoding, normalization,
coercion, or copying.

## Dependencies and data flow

The class depends only on built-in bytes and dataclass immutability. It imports no
scientific-model, retention, operator, serializer, verifier, repository, or calculator
owner.

```text
caller-owned exact bytes -> encoded-document DataObject -> explicit campaign consumer
```

The class does not select schemas or infer identity from filenames, paths, digests,
shapes, dimensions, spectra, or group identifiers.

## Retained artifact identity

Artifact-owned integration evidence reads the maintained directory
`calculations/research-monograph/periodic-2d/` and checks:

| Artifact | SHA-256 |
|---|---|
| `input.json` | `82e9915101e755f7cc77cb8901478f88d878ffaa808732036631b7ae5cfd78ec` |
| `result.json` | `4eb55bde9d456d86bad1d65c8ac60267c07873c6936f8af876b07fd3e1d27be6` |

Both identities are also bound to their maintained `SHA256SUMS` entries. A digest
establishes content identity only; it does not establish source provenance, execution,
decoded correctness, scientific validity, uncertainty, or acceptance.

## Scientific and numerical boundary

The DataObject does not define a physical parent, retained space, basis, gauge,
geometry, units, energy reference, represented operator, effective model, comparison,
or tolerance. It performs no numerical operation and invokes no calculator. Scientific
meaning remains with authenticated decoders and explicit campaign owners.

## Code mapping

| Code path | Qualified owner | Responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic2d/campaign/nbands_1/encoded_documents.py` | `ksdft2effmass.periodic2d.campaign.nbands_1.encoded_documents.Periodic2DIsolatedBandEncodedDocuments` | Defining exact immutable byte container |
| `python/src/ksdft2effmass/periodic2d/campaign/nbands_1/__init__.py` | `ksdft2effmass.periodic2d.campaign.nbands_1.Periodic2DIsolatedBandEncodedDocuments` | Canonical campaign-family facade |
| `python/src/ksdft2effmass/periodic2d/campaign/__init__.py` | `ksdft2effmass.periodic2d.campaign.Periodic2DIsolatedBandEncodedDocuments` | Reviewed campaign facade |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | `ksdft2effmass.periodic2d.Periodic2DIsolatedBandEncodedDocuments` | Reviewed package facade |

## Test mapping

| Test path | Exact pytest node | Evidence ownership | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/campaign/nbands_1/test__Periodic2DIsolatedBandEncodedDocuments.py` | `TestPeriodic2DIsolatedBandEncodedDocuments::test_contract__owns_exact_ordered_payload_fields` | Class-owned routine software verification | Exact fields, defining owner, and no-copy synthetic bytes |
| same | `TestPeriodic2DIsolatedBandEncodedDocuments::test_construction__rejects_wrong_and_empty_payloads` | Class-owned routine software verification | Wrong, subtyped, and empty payloads fail closed |
| same | `TestPeriodic2DIsolatedBandEncodedDocuments::test_construction__is_frozen_and_slotted` | Class-owned routine software verification | Maintained state is frozen and slotted |
| `python/tests/software_verification/ksdft2effmass/periodic2d/campaign/nbands_1/test__integration__periodic_2d_isolated_band_encoded_document_artifacts.py` | `TestPeriodic2DIsolatedBandEncodedDocumentArtifacts::test_retained_artifacts__preserve_bytes_and_catalog_identities` | Artifact-owned claim-bearing integration evidence | Exact retained bytes and checksum-catalog identities |
| same | `TestPeriodic2DIsolatedBandEncodedDocumentArtifacts::test_public_routes__share_the_defining_class_without_retired_name` | Artifact-owned integration evidence | Reviewed facades share one class and omit the retired name and source module |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/campaign/nbands_1/serialization.rst` | `ksdft2effmass.periodic2d.campaign.nbands_1.Periodic2DIsolatedBandEncodedDocuments` | User-facing ownership narrative and autodoc |

## Evidence and claim boundary

| Evidence question | Status | Evidence or limitation |
|---|---|---|
| Exact field ownership and immutable representation | Supported | Routine class-owned tests |
| Exact retained bytes and SHA-256 identities | Supported | Artifact-owned integration test and maintained `SHA256SUMS` |
| Reviewed facades and retired-name absence | Supported | Exact class-identity and absence assertions |
| Decoded schema and campaign semantics | Not claimed | Owned by serializer, correlator, verifier, and campaign Actions |
| Execution provenance | Not claimed | Content identity is not execution provenance |
| Numerical or scientific validation | Not claimed | No numerical or physical claim is evaluated |
| Uncertainty quantification or acceptance | Not claimed | No uncertainty model, decision, or authority is owned |

## Provenance and limitations

Original local work under the repository license. Retained files and checksums are
repository-maintained content-identity evidence. Row 056 separately reconciles
`Periodic2DIsolatedBandResultDocument` under its
[`result_documents`](../../result_documents/index.md) owner; row 067 owns broader
campaign decomposition.
Passing the mapped checks establishes bounded software behavior only.
