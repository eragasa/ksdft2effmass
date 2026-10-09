# `Periodic2DWannier90BalancedEncodedDocuments`

## Purpose and migration status

This implemented immutable DataObject is the row-050 replacement for the retired
`Periodic2DWannier90BalancedCampaignModel`. It owns the exact encoded result for one
retained periodic-2D balanced Wannier90 comparison. The former class name and source
module `python/src/ksdft2effmass/periodic2d/model/retained/wannier90_balanced.py` are
absent rather than preserved as aliases or forwarding routes.

The historical crosswalk contract contains only `result_payload`. This migration does
not invent an input payload, native-file inventory, execution provenance, convergence
status, or scientific interpretation. Rows 051–055 independently audit other Wannier90
study and optimizer-family document owners.

## Public contract and reviewed routes

The constructor accepts `result_payload` and returns one frozen, slotted DataObject. It
has no decoding, filesystem, native-artifact discovery, correlation, verification,
calculation, oracle-qualification, localization-assessment, or acceptance method.

Supported reviewed import routes are:

- `ksdft2effmass.periodic2d.run.wannier90.balanced.Periodic2DWannier90BalancedEncodedDocuments`;
- `ksdft2effmass.periodic2d.run.wannier90.Periodic2DWannier90BalancedEncodedDocuments`;
  and
- `ksdft2effmass.periodic2d.Periodic2DWannier90BalancedEncodedDocuments`.

All three routes expose the defining class object and none exposes the retired name.

## State and invariants

| Field | Representation | Meaning |
|---|---|---|
| `result_payload` | Exact nonempty built-in `bytes` | Encoded retained balanced-comparison result |

This is the complete state. Construction rejects non-`bytes` values, including `bytes`
subclasses, with `TypeError`, and empty exact bytes with `ValueError`. The supplied byte
object is retained without decoding, re-encoding, normalization, coercion, or copying.
There is deliberately no `input_payload` field.

## Dependencies and data flow

The class depends only on built-in bytes and dataclass immutability. It imports no
Wannier90 native-artifact, scientific-model, retained-space, operator, serializer,
verifier, oracle, repository, optimizer, or calculator owner.

```text
caller-owned exact result bytes -> balanced encoded-result DataObject -> explicit consumer
```

The class does not select a schema or infer input availability, native files, execution,
localization convergence, normalization, symmetry, frame, gauge, provenance, or
scientific meaning from filenames, paths, hashes, shapes, dimensions, spectra, labels,
or campaign names.

## Retained artifact identity

Artifact-owned integration evidence reads the maintained directory
`calculations/research-monograph/periodic-2d/` and checks:

| Artifact | SHA-256 |
|---|---|
| `wannier90-balanced-result.json` | `422e53b012fb824164e3f03e67eeef6f5a013ce6f17da942ddc3f2d477b06e93` |

The identity is also bound to the corresponding maintained `SHA256SUMS` entry. This is
content-identity evidence only. No separately retained
`wannier90-balanced-input.json` is claimed because it is not part of the reviewed
crosswalk contract or checksum catalog.

## Scientific, native-artifact, and numerical boundary

The DataObject does not define a physical parent, Hamiltonian, retained space, frame,
gauge, geometry, units, energy reference, projector, represented operator, localization
functional, optimizer, convergence threshold, comparison tolerance, or acceptance
criterion. It performs no numerical operation and invokes neither Wannier90 nor another
calculator.

An encoded result does not imply the availability or authenticity of native `.win`,
`.wout`, `.chk`, `_hr.dat`, `.amn`, `.mmn`, `.eig`, or other files. It also does not
establish that localization converged, that any optimizer was valid, that a decoded
observation is correct, or that a scientific conclusion is accepted.

## Code mapping

| Code path | Qualified owner | Responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic2d/run/wannier90/balanced/encoded_documents.py` | `ksdft2effmass.periodic2d.run.wannier90.balanced.encoded_documents.Periodic2DWannier90BalancedEncodedDocuments` | Defining exact immutable result-byte container |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/balanced/__init__.py` | `ksdft2effmass.periodic2d.run.wannier90.balanced.Periodic2DWannier90BalancedEncodedDocuments` | Reviewed balanced-run facade |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/__init__.py` | `ksdft2effmass.periodic2d.run.wannier90.Periodic2DWannier90BalancedEncodedDocuments` | Reviewed Wannier90-run facade |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | `ksdft2effmass.periodic2d.Periodic2DWannier90BalancedEncodedDocuments` | Reviewed package facade |

## Test mapping

| Test path | Exact pytest node | Evidence ownership | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/balanced/test__Periodic2DWannier90BalancedEncodedDocuments.py` | `TestPeriodic2DWannier90BalancedEncodedDocuments::test_contract__owns_one_exact_result_payload` | Class-owned routine software verification | One exact field, defining owner, no-copy bytes, and no invented input field |
| same | `TestPeriodic2DWannier90BalancedEncodedDocuments::test_construction__rejects_wrong_and_empty_payloads` | Class-owned routine software verification | Wrong, subtyped, and empty payloads fail closed |
| same | `TestPeriodic2DWannier90BalancedEncodedDocuments::test_construction__is_frozen_and_slotted` | Class-owned routine software verification | Maintained state is frozen and slotted |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/balanced/test__integration__periodic_2d_wannier90_balanced_encoded_document_artifact.py` | `TestPeriodic2DWannier90BalancedEncodedDocumentArtifact::test_retained_artifact__preserves_bytes_and_catalog_identity` | Artifact-owned claim-bearing integration evidence | Exact retained bytes and checksum-catalog identity, not scientific validation |
| same | `TestPeriodic2DWannier90BalancedEncodedDocumentArtifact::test_public_routes__share_implementation_without_retired_name` | Artifact-owned integration evidence | Three reviewed facades share one class and omit retired name/module routes |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/run/wannier90-balanced.rst` | `ksdft2effmass.periodic2d.run.wannier90.balanced.Periodic2DWannier90BalancedEncodedDocuments` | User-facing ownership narrative and autodoc |

## Evidence and claim boundary

| Evidence question | Status | Evidence or limitation |
|---|---|---|
| Exact field ownership and immutable representation | Supported | Routine class-owned tests |
| Exact retained result bytes and SHA-256 identity | Supported | Artifact-owned integration test and maintained `SHA256SUMS` |
| Reviewed facades and retired-route absence | Supported | Exact class-identity and source-path absence assertions |
| Separately retained encoded input | Not claimed | The reviewed contract owns only `result_payload` |
| Native Wannier90 artifact presence | Not established | No native-file owner or authenticated inventory is involved |
| Execution provenance | Not claimed | Content identity is not execution provenance |
| Localization or optimizer convergence | Not claimed | No convergence contract is owned by this DataObject |
| Decoded numerical correctness | Not claimed | Owned by explicit decoder and independent verifier boundaries |
| Scientific validation, UQ, or acceptance | Not claimed | No scientific decision or authority is owned |

## Provenance and limitations

Original local work under the repository license. The retained file and checksum are
repository-maintained content-identity evidence. The compact result cannot reconstruct
missing input or native execution artifacts and cannot establish historical execution.
Passing the mapped checks establishes bounded software behavior only.
