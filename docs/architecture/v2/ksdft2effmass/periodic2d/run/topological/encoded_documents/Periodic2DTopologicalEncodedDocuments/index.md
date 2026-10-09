# `Periodic2DTopologicalEncodedDocuments`

## Purpose and migration status

This implemented immutable DataObject is the row-048 replacement for the retired
`Periodic2DTopologicalCampaignModel`. It owns exact encoded input and result documents
for the retained periodic-2D topological campaign. The former class name and source
module `python/src/ksdft2effmass/periodic2d/model/retained/topological.py` are absent
rather than preserved as aliases or forwarding routes.

The class resides under `ksdft2effmass.periodic2d.run.topological`. Row 049 separately
owns the phase-sweep pair, while row 069 completes topological-observation operation
decomposition. Neither row reinterprets encoded expected observations as qualified
numerical oracles.

## Public contract and reviewed routes

The constructor accepts `input_payload` and `result_payload` and returns one frozen,
slotted DataObject. It has no decoding, filesystem, correlation, verification,
calculation, oracle-qualification, or scientific-interpretation method.

Supported reviewed import routes are:

- `ksdft2effmass.periodic2d.run.topological.Periodic2DTopologicalEncodedDocuments`; and
- `ksdft2effmass.periodic2d.Periodic2DTopologicalEncodedDocuments`.

Both routes expose the defining class object and neither exposes the retired name.
`ksdft2effmass.periodic2d.run` remains a namespace boundary rather than an additional
flattening facade.

## State and invariants

| Field | Representation | Meaning |
|---|---|---|
| `input_payload` | Exact nonempty built-in `bytes` | Encoded topological campaign definition |
| `result_payload` | Exact nonempty built-in `bytes` | Encoded retained topological campaign result |

Field order is stable as listed. Construction rejects non-`bytes` values, including
`bytes` subclasses, with `TypeError`, and empty exact bytes with `ValueError`. Each
supplied byte object is retained without decoding, re-encoding, normalization,
coercion, or copying.

## Dependencies and data flow

The class depends only on built-in bytes and dataclass immutability. It imports no
scientific-model, topology, operator, serializer, verifier, oracle, repository, or
calculator owner.

```text
caller-owned exact bytes -> topological encoded-document DataObject -> explicit consumer
```

The class does not select schemas or infer physical phase, topology, normalization,
symmetry, provenance, or meaning from filenames, paths, hashes, shapes, dimensions,
spectra, labels, or expected values.

## Retained artifact identity

Artifact-owned integration evidence reads the maintained directory
`calculations/research-monograph/periodic-2d/` and checks:

| Artifact | SHA-256 |
|---|---|
| `topological-input.json` | `b4372d84ba80e84a1bf9a12d25750618bf276baa8999d298031e3ac6e0c18436` |
| `topological-result.json` | `bd94c40a3b12f4f7ecb41009e86c936e456d09738176256f4e0d27ab9fdd959a` |

Both identities are bound to maintained `SHA256SUMS` entries. These values are content
identities, not numerical oracles or evidence of provenance, topology, convergence,
scientific validation, uncertainty, or acceptance.

## Scientific and numerical boundary

The DataObject does not define a physical parent, Hamiltonian, retained space, frame,
gauge, geometry, units, energy reference, projector, represented operator, topological
invariant, comparison, or tolerance. It performs no numerical operation and invokes no
calculator. Encoded expected observations cannot supply accepted evidence without
qualification for the exact evidence class and validity domain.

## Code mapping

| Code path | Qualified owner | Responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic2d/run/topological/encoded_documents.py` | `ksdft2effmass.periodic2d.run.topological.encoded_documents.Periodic2DTopologicalEncodedDocuments` | Defining exact immutable byte container |
| `python/src/ksdft2effmass/periodic2d/run/topological/__init__.py` | `ksdft2effmass.periodic2d.run.topological.Periodic2DTopologicalEncodedDocuments` | Reviewed topological-run facade |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | `ksdft2effmass.periodic2d.Periodic2DTopologicalEncodedDocuments` | Reviewed package facade |

## Test mapping

| Test path | Exact pytest node | Evidence ownership | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/topological/test__Periodic2DTopologicalEncodedDocuments.py` | `TestPeriodic2DTopologicalEncodedDocuments::test_contract__owns_exact_ordered_payload_fields` | Class-owned routine software verification | Exact fields, defining owner, and no-copy synthetic bytes |
| same | `TestPeriodic2DTopologicalEncodedDocuments::test_construction__rejects_wrong_and_empty_payloads` | Class-owned routine software verification | Wrong, subtyped, and empty payloads fail closed |
| same | `TestPeriodic2DTopologicalEncodedDocuments::test_construction__is_frozen_and_slotted` | Class-owned routine software verification | Maintained state is frozen and slotted |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/topological/test__integration__periodic_2d_topological_encoded_document_artifacts.py` | `TestPeriodic2DTopologicalEncodedDocumentArtifacts::test_retained_artifacts__preserve_bytes_and_catalog_identities` | Artifact-owned claim-bearing integration evidence | Exact retained bytes and checksum-catalog identities, not oracle qualification |
| same | `TestPeriodic2DTopologicalEncodedDocumentArtifacts::test_public_routes__share_implementation_without_retired_name` | Artifact-owned integration evidence | Reviewed facades share one class and omit retired name/module routes |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/run/topological.rst` | `ksdft2effmass.periodic2d.run.topological.Periodic2DTopologicalEncodedDocuments` | User-facing ownership narrative and autodoc |

## Evidence and claim boundary

| Evidence question | Status | Evidence or limitation |
|---|---|---|
| Exact field ownership and immutable representation | Supported | Routine class-owned tests |
| Exact retained bytes and SHA-256 identities | Supported | Artifact-owned integration test and maintained `SHA256SUMS` |
| Reviewed facades and retired-route absence | Supported | Exact class-identity and source-path absence assertions |
| Decoded schema and campaign semantics | Not claimed | Owned by serializer, correlator, verifier, and campaign Actions |
| Numerical-oracle qualification | Not established | Encoded expected observations are retained content only |
| Topological phase or invariant correctness | Not claimed | No topological quantity is computed by this owner |
| Execution provenance | Not claimed | Content identity is not execution provenance |
| Scientific validation, UQ, or acceptance | Not claimed | No scientific decision or authority is owned |

## Provenance and limitations

Original local work under the repository license. Retained files and checksums are
repository-maintained content-identity evidence. Row 069 owns broader topological
campaign decomposition and must preserve distinctions among encoded observations,
independent verification, qualified oracles, and scientific conclusions. Passing the
mapped checks establishes bounded software behavior only.
