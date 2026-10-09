# `Periodic1DCompositeEncodedDocuments`

## Purpose and migration status

This implemented immutable DataObject is the row-038 replacement for the retired
`Periodic1DCompositeCampaignModel`. Its name states its complete responsibility: it
owns exact encoded input and result documents for the version-one composite campaign.
The retired class, source module, imports, exports, aliases, and forwarding routes are
absent.

Row 059 moved the implementation with the complete composite family to
`ksdft2effmass.periodic1d.campaign.composite.encoded_documents` while preserving the
retained bytes and wire identities. The former underscored and publication routes are
absent; the document remains a wire container rather than a scientific model or
retained object.

## Public contract and supported routes

The public constructor accepts `input_payload` and `result_payload` and returns one
frozen slotted DataObject. It exposes only those two read-only fields and inherited
object behavior; it has no public decoding, filesystem, correlation, verification, or
adoption method.

Supported reviewed import routes are:

- `ksdft2effmass.periodic1d.campaign.Periodic1DCompositeEncodedDocuments`; and
- `ksdft2effmass.periodic1d.campaign.composite.Periodic1DCompositeEncodedDocuments`.

Both routes expose the defining class object; neither exposes the retired name.

## State, identity, invariants, and failures

| Field | Representation | Meaning |
|---|---|---|
| `input_payload` | Exact nonempty built-in `bytes` | Encoded composite campaign definition |
| `result_payload` | Exact nonempty built-in `bytes` | Encoded retained composite campaign result |

Field order is stable as listed. Object identity is ordinary Python instance identity;
the class does not synthesize a scientific identity. Construction rejects non-`bytes`
values, including `bytes` subclasses, with `TypeError`, and rejects empty exact bytes
with `ValueError`. The DataObject preserves each supplied byte object without decoding,
re-encoding, normalization, coercion, or copying.

## Dependencies, collaborators, and data flow

The DataObject depends only on built-in byte values and dataclass immutability. It must
not import scientific-model, retention, operator, verifier, repository, or calculator
owners. Consumers receive it explicitly. Serializers may decode each payload;
correlators may bind input and result meaning; verifiers may reconstruct declared
channels; scientific-adoption Actions may construct separately typed retained spaces
and operators from explicitly authenticated evidence. This DataObject performs none of
those operations.

Data flow is therefore:

```text
caller-owned bytes -> encoded-document DataObject -> explicit serializer/correlator/
verifier/adoption consumer
```

No reverse dependency from scientific model or reusable operator packages is allowed.

## Serialization and compatibility

The class stores already encoded documents and is not a serializer. It preserves the
version-one payload bytes exactly. There is no compatibility alias, automatic schema
upgrade, decoding fallback, normalization, or re-encoding route. Canonical source
ownership preserves the current wire identities.

## Scientific-category boundary

The result document contains historical composite-campaign evidence, but possession of
its bytes does not itself define or authenticate:

- a physical parent or finite representation;
- a retained band group or retained mathematical subspace;
- a smooth or rough frame, projector, or gauge transformation;
- a retained or represented operator;
- a hopping truncation or fitted effective model; or
- a scientific verification or acceptance decision.

Unavailable frame/projector coordinates, attacked gauges, rough reciprocal matrices,
and withheld reciprocal matrices remain unavailable. The encoded-document owner must
not infer them from ranks, names, spectra, or hashes.

## Retained artifact identity

The artifact-owned integration evidence reads the maintained directory
`calculations/research-monograph/periodic-1d/` and checks:

| Artifact | SHA-256 |
|---|---|
| `composite-input.json` | `2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20` |
| `composite-result.json` | `9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f` |

The integration test verifies identity-preserving construction and binds both computed
digests to the maintained `SHA256SUMS` entries. A digest establishes content identity
only. It does not establish where, when, how, or by whom a calculation ran; it does not
establish that decoded content is scientifically correct.

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic1d/campaign/composite/encoded_documents.py` | Class | `ksdft2effmass.periodic1d.campaign.composite.encoded_documents.Periodic1DCompositeEncodedDocuments` | Defines the exact immutable row-038 byte container |
| `python/src/ksdft2effmass/periodic1d/campaign/__init__.py` | Package | `ksdft2effmass.periodic1d.campaign.Periodic1DCompositeEncodedDocuments` | Reviewed campaign facade |
| `python/src/ksdft2effmass/periodic1d/campaign/composite/__init__.py` | Package | `ksdft2effmass.periodic1d.campaign.composite.Periodic1DCompositeEncodedDocuments` | Reviewed leaf facade |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeEncodedDocuments.py` | `TestPeriodic1DCompositeEncodedDocuments::test_contract__owns_exact_fields_and_preserves_synthetic_bytes` | Software verification, class-owned | Exact fields, defining owner, and no-copy synthetic-byte storage |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeEncodedDocuments.py` | `TestPeriodic1DCompositeEncodedDocuments::test_construction__rejects_wrong_and_empty_payload_representations` | Software verification, class-owned | Wrong types, byte subclasses, and empty payloads fail closed |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeEncodedDocuments.py` | `TestPeriodic1DCompositeEncodedDocuments::test_construction__is_frozen_and_slotted` | Software verification, class-owned | Field mutation and undeclared state are rejected |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__integration__composite_encoded_document_artifacts.py` | `TestPeriodic1DCompositeEncodedDocumentArtifacts::test_retained_artifacts__preserve_exact_bytes_and_catalog_identities` | Software verification, artifact-owned integration | Exact retained bytes and checksum-catalog identities |
| `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__integration__composite_encoded_document_artifacts.py` | `TestPeriodic1DCompositeEncodedDocumentArtifacts::test_public_routes__share_implementation_without_retired_route` | Software verification, artifact-owned integration | Two supported facades share the implementation and retired routes remain absent |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/research-monograph-campaigns.rst` | `ksdft2effmass.periodic1d.campaign.Periodic1DCompositeEncodedDocuments` | Canonical user-facing narrative and autodoc |

## Evidence and claim boundary

| Evidence question | Status | Evidence or limitation |
|---|---|---|
| Exact field ownership and immutable representation | Supported | Routine class-owned software tests listed above |
| Exact retained byte and digest preservation | Supported | Claim-bearing artifact-owned integration test against maintained files and `SHA256SUMS` |
| Reviewed facade and retired-route behavior | Supported | Artifact-owned integration route test |
| Decoded schema and semantic correctness | Not claimed here | Owned by serializers, correlators, and verifiers |
| Retained-space, frame, projector, or operator identity | Not claimed here | Requires explicit scientific metadata and separate typed adoption |
| Source provenance or authenticity | Not claimed | Bytes and SHA-256 values are content identities, not provenance evidence |
| Scientific validation, convergence, or physical adequacy | Not claimed | No model adequacy or convergence calculation is performed |
| Uncertainty quantification or acceptance | Not claimed | No uncertainty model, tolerance decision, or acceptance authority is owned here |

## Provenance

Original local work under the repository license. Retained files and checksum entries
are repository-maintained content-identity evidence, not scientific or execution
provenance.

## Limitations and deviations

The class has no separate implementation, mathematics, references, or testing child
page because its complete
contract is the bounded encoded-container behavior mapped here. Passing mapped checks
is not numerical-oracle qualification, scientific validation, uncertainty
quantification, or human acceptance.
