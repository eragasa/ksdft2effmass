# `Periodic2DCompositeEncodedDocuments`

## Purpose and migration status

This implemented immutable DataObject is the row-047 replacement for the retired
`Periodic2DCompositeCampaignModel`. It owns exact encoded input and result documents
for the retained periodic-2D composite campaign. The former class name and
retained-model source module are absent rather than preserved as aliases or forwarding
routes.

The class resides under `ksdft2effmass.periodic2d.run.composite`. Row 068 owns later
composite-campaign decomposition and explicit typed scientific results; that work must
not alter these retained bytes or reinterpret this container as a model, retained band
group, frame, or represented operator.

## Public contract and reviewed routes

The constructor accepts `input_payload` and `result_payload` and returns one frozen,
slotted DataObject. It has no decoding, filesystem, correlation, verification,
calculation, retained-space adoption, or scientific interpretation method.

Supported reviewed import routes are:

- `ksdft2effmass.periodic2d.run.composite.Periodic2DCompositeEncodedDocuments`; and
- `ksdft2effmass.periodic2d.Periodic2DCompositeEncodedDocuments`.

Both routes expose the defining class object and neither exposes the retired name.
`ksdft2effmass.periodic2d.run` is a namespace boundary, not an additional flattening
facade.

## State and invariants

| Field | Representation | Meaning |
|---|---|---|
| `input_payload` | Exact nonempty built-in `bytes` | Encoded composite campaign definition |
| `result_payload` | Exact nonempty built-in `bytes` | Encoded retained composite campaign result |

Field order is stable as listed. Construction rejects non-`bytes` values, including
`bytes` subclasses, with `TypeError`, and empty exact bytes with `ValueError`. Each
supplied byte object is retained without decoding, re-encoding, normalization,
coercion, or copying.

## Dependencies and data flow

The class depends only on built-in bytes and dataclass immutability. It imports no
scientific-model, retention, frame, operator, serializer, verifier, repository, or
calculator owner.

```text
caller-owned exact bytes -> composite encoded-document DataObject -> explicit consumer
```

The class does not select schemas or infer identity, compatibility, frame, gauge,
normalization, symmetry, provenance, or meaning from filenames, paths, hashes, shapes,
dimensions, spectra, or group identifiers.

## Retained artifact identity

Artifact-owned integration evidence reads the maintained directory
`calculations/research-monograph/periodic-2d/` and checks:

| Artifact | SHA-256 |
|---|---|
| `composite-input.json` | `4abe583a5198537703f3a9e4937fd93c4c7cd6f46a3eefd302a551b1f0ae7e90` |
| `composite-result.json` | `2bd97c1138e501e0b26f19dd43b3bb1718dc6e4655804f6bc96e853c7fd87792` |

Both identities are bound to maintained `SHA256SUMS` entries. A digest establishes
content identity only; it does not establish source provenance, execution, decoded
correctness, scientific validity, uncertainty, or acceptance.

## Scientific and numerical boundary

The DataObject does not define a physical parent, retained space, selected band group,
frame, gauge, geometry, units, energy reference, projector, represented operator,
effective model, comparison, or tolerance. It performs no numerical operation and
invokes no calculator. Scientific meaning remains with authenticated decoders,
correlators, retained-space owners, and explicit campaign Actions.

## Code mapping

| Code path | Qualified owner | Responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic2d/run/composite/encoded_documents.py` | `ksdft2effmass.periodic2d.run.composite.encoded_documents.Periodic2DCompositeEncodedDocuments` | Defining exact immutable byte container |
| `python/src/ksdft2effmass/periodic2d/run/composite/__init__.py` | `ksdft2effmass.periodic2d.run.composite.Periodic2DCompositeEncodedDocuments` | Reviewed composite-run facade |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | `ksdft2effmass.periodic2d.Periodic2DCompositeEncodedDocuments` | Reviewed package facade |

## Test mapping

| Test path | Exact pytest node | Evidence ownership | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/composite/test__Periodic2DCompositeEncodedDocuments.py` | `TestPeriodic2DCompositeEncodedDocuments::test_contract__owns_exact_ordered_payload_fields` | Class-owned routine software verification | Exact fields, defining owner, and no-copy synthetic bytes |
| same | `TestPeriodic2DCompositeEncodedDocuments::test_construction__rejects_wrong_and_empty_payloads` | Class-owned routine software verification | Wrong, subtyped, and empty payloads fail closed |
| same | `TestPeriodic2DCompositeEncodedDocuments::test_construction__is_frozen_and_slotted` | Class-owned routine software verification | Maintained state is frozen and slotted |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/composite/test__integration__periodic_2d_composite_encoded_document_artifacts.py` | `TestPeriodic2DCompositeEncodedDocumentArtifacts::test_retained_artifacts__preserve_bytes_and_catalog_identities` | Artifact-owned claim-bearing integration evidence | Exact retained bytes and checksum-catalog identities |
| same | `TestPeriodic2DCompositeEncodedDocumentArtifacts::test_public_routes__share_implementation_without_retired_name` | Artifact-owned integration evidence | Reviewed facades share one class and omit retired name/module routes |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/run/composite.rst` | `ksdft2effmass.periodic2d.run.composite.Periodic2DCompositeEncodedDocuments` | User-facing ownership narrative and autodoc |

## Evidence and claim boundary

| Evidence question | Status | Evidence or limitation |
|---|---|---|
| Exact field ownership and immutable representation | Supported | Routine class-owned tests |
| Exact retained bytes and SHA-256 identities | Supported | Artifact-owned integration test and maintained `SHA256SUMS` |
| Reviewed facades and retired-route absence | Supported | Exact class-identity and source-path absence assertions |
| Decoded schema and campaign semantics | Not claimed | Owned by serializer, correlator, verifier, and campaign Actions |
| Retained-space, frame, or represented-operator identity | Not claimed | Encoded bytes do not establish scientific identity or compatibility |
| Execution provenance | Not claimed | Content identity is not execution provenance |
| Numerical or scientific validation | Not claimed | No numerical or physical claim is evaluated |
| Uncertainty quantification or acceptance | Not claimed | No uncertainty model, decision, or authority is owned |

## Provenance and limitations

Original local work under the repository license. Retained files and checksums are
repository-maintained content-identity evidence. Row 068 owns broader composite
campaign decomposition and must keep retention, frame selection, represented operators,
and campaign evidence distinct. Passing the mapped checks establishes bounded software
behavior only.
