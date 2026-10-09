# `Periodic2DWannier90StudyEncodedDocuments`

## Purpose and migration status

This implemented immutable DataObject is the row-051 replacement for the retired
`Periodic2DWannier90StudyCampaignModel`. It owns exact encoded input and result
documents for the retained bounded periodic-2D Wannier90 sensitivity study. The former
class name and source module
`python/src/ksdft2effmass/periodic2d/model/retained/wannier90_study.py` are absent rather
than preserved as aliases or forwarding routes.

The encoded input declares a reference case and six bounded cases across reciprocal
mesh, plane-wave cutoff, and auxiliary-embedding axes. This statement describes the
retained wire; it does not assert that every case was executed correctly, that native
files remain present, or that any axis is converged. The encoded result and its status
fields remain provisional content until explicit correlation and independent
verification establish their bounded meanings.

## Public contract and reviewed routes

The constructor accepts `input_payload` and `result_payload` and returns one frozen,
slotted DataObject. It has no decoding, filesystem, native-artifact discovery,
correlation, verification, calculation, case-completion, convergence-assessment,
oracle-qualification, or acceptance method.

Supported reviewed import routes are:

- `ksdft2effmass.periodic2d.run.wannier90.study.Periodic2DWannier90StudyEncodedDocuments`;
- `ksdft2effmass.periodic2d.run.wannier90.Periodic2DWannier90StudyEncodedDocuments`; and
- `ksdft2effmass.periodic2d.Periodic2DWannier90StudyEncodedDocuments`.

All three routes expose the defining class object and none exposes the retired name.

## State and invariants

| Field | Representation | Meaning |
|---|---|---|
| `input_payload` | Exact nonempty built-in `bytes` | Encoded bounded Wannier90 study definition |
| `result_payload` | Exact nonempty built-in `bytes` | Encoded retained study result |

Field order is stable as listed. Construction rejects non-`bytes` values, including
`bytes` subclasses, with `TypeError`, and empty exact bytes with `ValueError`. Each
supplied byte object is retained without decoding, re-encoding, normalization,
coercion, or copying.

## Dependencies and data flow

The class depends only on built-in bytes and dataclass immutability. It imports no
parameter-space, Wannier90 native-artifact, scientific-model, retained-space, operator,
serializer, verifier, oracle, repository, optimizer, or calculator owner.

```text
caller-owned exact bytes -> study encoded-document DataObject -> explicit consumer
```

The class does not select schemas or infer study-axis meaning, case completion, native
file availability, execution success, localization convergence, embedding adequacy,
normalization, frame, gauge, provenance, or scientific meaning from filenames, paths,
hashes, shapes, dimensions, status labels, case identifiers, or reported trends.

## Retained artifact identity

Artifact-owned integration evidence reads the maintained directory
`calculations/research-monograph/periodic-2d/` and checks:

| Artifact | SHA-256 |
|---|---|
| `wannier90-study-input.json` | `0092895cf1ff970ab3275b976d365e3c4df8c3c4c2a3ad33f4d0eaf9dbf5517a` |
| `wannier90-study-result.json` | `a4a400f7610520d75f42af991b5b0eacaaaca53ac5dfd0736f072b918d092e11` |

Both identities are bound to maintained `SHA256SUMS` entries. These values establish
content identity only; they do not authenticate case execution, native artifacts,
completion, convergence, numerical correctness, or scientific acceptance.

## Scientific, native-artifact, and numerical boundary

The DataObject does not define a physical parent, Hamiltonian, convergence sequence,
retained space, frame, gauge, geometry, units, energy reference, projector, represented
operator, localization functional, optimizer, convergence tolerance, uncertainty model,
or acceptance criterion. It performs no numerical operation and invokes neither
Wannier90 nor another calculator.

The three encoded sensitivity axes remain distinct:

- reciprocal-mesh variation concerns sampling/discretization;
- plane-wave-cutoff variation concerns finite-basis discretization; and
- auxiliary-embedding variation concerns the finite embedding used by the synthetic
  construction.

The byte owner does not combine these into one error measure or claim that bounded
variation establishes convergence. Parent-model, discretization, embedding,
localization, interpolation, and comparison errors remain separate unless an explicit
scientific owner defines their relationship.

## Code mapping

| Code path | Qualified owner | Responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic2d/run/wannier90/study/encoded_documents.py` | `ksdft2effmass.periodic2d.run.wannier90.study.encoded_documents.Periodic2DWannier90StudyEncodedDocuments` | Defining exact immutable byte container |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/study/__init__.py` | `ksdft2effmass.periodic2d.run.wannier90.study.Periodic2DWannier90StudyEncodedDocuments` | Reviewed study facade |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/__init__.py` | `ksdft2effmass.periodic2d.run.wannier90.Periodic2DWannier90StudyEncodedDocuments` | Reviewed Wannier90-run facade |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | `ksdft2effmass.periodic2d.Periodic2DWannier90StudyEncodedDocuments` | Reviewed package facade |

## Test mapping

| Test path | Exact pytest node | Evidence ownership | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/study/test__Periodic2DWannier90StudyEncodedDocuments.py` | `TestPeriodic2DWannier90StudyEncodedDocuments::test_contract__owns_exact_ordered_payload_fields` | Class-owned routine software verification | Exact fields, defining owner, and no-copy synthetic bytes |
| same | `TestPeriodic2DWannier90StudyEncodedDocuments::test_construction__rejects_wrong_and_empty_payloads` | Class-owned routine software verification | Wrong, subtyped, and empty payloads fail closed |
| same | `TestPeriodic2DWannier90StudyEncodedDocuments::test_construction__is_frozen_and_slotted` | Class-owned routine software verification | Maintained state is frozen and slotted |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/study/test__integration__periodic_2d_wannier90_study_encoded_document_artifacts.py` | `TestPeriodic2DWannier90StudyEncodedDocumentArtifacts::test_retained_artifacts__preserve_bytes_and_catalog_identities` | Artifact-owned claim-bearing integration evidence | Exact retained bytes and checksum-catalog identities, not execution or convergence evidence |
| same | `TestPeriodic2DWannier90StudyEncodedDocumentArtifacts::test_public_routes__share_implementation_without_retired_name` | Artifact-owned integration evidence | Three reviewed facades share one class and omit retired name/module routes |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/run/wannier90-study.rst` | `ksdft2effmass.periodic2d.run.wannier90.study.Periodic2DWannier90StudyEncodedDocuments` | User-facing ownership narrative and autodoc |

## Evidence and claim boundary

| Evidence question | Status | Evidence or limitation |
|---|---|---|
| Exact field ownership and immutable representation | Supported | Routine class-owned tests |
| Exact retained bytes and SHA-256 identities | Supported | Artifact-owned integration test and maintained `SHA256SUMS` |
| Reviewed facades and retired-route absence | Supported | Exact class-identity and source-path absence assertions |
| Encoded bounded axis declarations | Preserved, not adopted | Exact input bytes retain the declarations without interpreting them |
| Native Wannier90 artifact presence | Not established | No native-file owner or authenticated inventory is involved |
| Execution provenance or case completion | Not claimed | Content identity and status fields are not execution evidence |
| Numerical convergence | Not established by this row | Bounded variations are not a convergence proof |
| Localization or embedding validity | Not claimed | No scientific acceptance criterion is owned by the DataObject |
| Scientific validation, UQ, or acceptance | Not claimed | No scientific decision or authority is owned |

## Provenance and limitations

Original local work under the repository license. Retained files and checksums are
repository-maintained content-identity evidence. The compact documents cannot establish
historical execution or reconstruct missing native files. Their six declared cases are
bounded synthetic study content rather than material validation or general convergence
evidence. Passing the mapped checks establishes bounded software behavior only.
