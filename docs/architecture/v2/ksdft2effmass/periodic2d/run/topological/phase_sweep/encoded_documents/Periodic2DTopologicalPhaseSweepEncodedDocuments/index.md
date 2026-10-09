# `Periodic2DTopologicalPhaseSweepEncodedDocuments`

## Purpose and migration status

This implemented immutable DataObject is the row-049 replacement for the retired
`Periodic2DTopologicalPhaseSweepCampaignModel`. It owns exact encoded input and result
documents for the retained periodic-2D topological phase sweep. The former class name
and source module
`python/src/ksdft2effmass/periodic2d/model/retained/topological_phase_sweep.py` are
absent rather than preserved as aliases or forwarding routes.

The class resides under `ksdft2effmass.periodic2d.run.topological.phase_sweep`. Row 048
owns the nonsweep topological document pair, while row 070 completes phase-sweep
operation decomposition. Neither row reinterprets encoded axes or expected observations
as qualified scientific evidence.

## Public contract and reviewed routes

The constructor accepts `input_payload` and `result_payload` and returns one frozen,
slotted DataObject. It has no decoding, filesystem, correlation, verification,
calculation, missing-sample resolution, oracle-qualification, or
scientific-interpretation method.

Supported reviewed import routes are:

- `ksdft2effmass.periodic2d.run.topological.phase_sweep.Periodic2DTopologicalPhaseSweepEncodedDocuments`; and
- `ksdft2effmass.periodic2d.Periodic2DTopologicalPhaseSweepEncodedDocuments`.

Both routes expose the defining class object and neither exposes the retired name.
Intermediate run packages remain namespace boundaries rather than additional flattening
facades.

## State and invariants

| Field | Representation | Meaning |
|---|---|---|
| `input_payload` | Exact nonempty built-in `bytes` | Encoded topological phase-sweep definition |
| `result_payload` | Exact nonempty built-in `bytes` | Encoded retained phase-sweep result |

Field order is stable as listed. Construction rejects non-`bytes` values, including
`bytes` subclasses, with `TypeError`, and empty exact bytes with `ValueError`. Each
supplied byte object is retained without decoding, re-encoding, normalization,
coercion, or copying.

## Dependencies and data flow

The class depends only on built-in bytes and dataclass immutability. It imports no
parameter-space, scientific-model, topology, operator, serializer, verifier, oracle,
repository, or calculator owner.

```text
caller-owned exact bytes -> phase-sweep encoded-document DataObject -> explicit consumer
```

The class does not select schemas or infer axis meaning, sample availability, physical
phase, topology, normalization, symmetry, provenance, or meaning from filenames, paths,
hashes, shapes, dimensions, spectra, labels, or expected values. In particular, the
presence of an encoded parameter point is not proof that a corresponding scientific
outcome is available or accepted.

## Retained artifact identity

Artifact-owned integration evidence reads the maintained directory
`calculations/research-monograph/periodic-2d/` and checks:

| Artifact | SHA-256 |
|---|---|
| `topological-phase-sweep-input.json` | `f8b535250ede7efc79b96682979b72472791172d0662d41a490f8bad2a0a553c` |
| `topological-phase-sweep-result.json` | `298532cba30f56518c6578feb187704ad8f031eabdeae468b7ad067d0b286b11` |

Both identities are bound to maintained `SHA256SUMS` entries. These values are content
identities, not numerical oracles or evidence of sample completeness, provenance,
topology, convergence, scientific validation, uncertainty, or acceptance.

## Scientific and numerical boundary

The DataObject does not define a physical parent, Hamiltonian, parameter axis, sampled
outcome, retained space, frame, gauge, geometry, units, energy reference, projector,
represented operator, topological invariant, comparison, or tolerance. It performs no
numerical operation and invokes no calculator. Encoded expected observations cannot
supply accepted evidence without qualification for the exact evidence class and
validity domain. Unavailable outcomes remain unavailable and are not reconstructed from
neighboring parameter points, names, dimensions, or expected trends.

## Code mapping

| Code path | Qualified owner | Responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic2d/run/topological/phase_sweep/encoded_documents.py` | `ksdft2effmass.periodic2d.run.topological.phase_sweep.encoded_documents.Periodic2DTopologicalPhaseSweepEncodedDocuments` | Defining exact immutable byte container |
| `python/src/ksdft2effmass/periodic2d/run/topological/phase_sweep/__init__.py` | `ksdft2effmass.periodic2d.run.topological.phase_sweep.Periodic2DTopologicalPhaseSweepEncodedDocuments` | Reviewed phase-sweep facade |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | `ksdft2effmass.periodic2d.Periodic2DTopologicalPhaseSweepEncodedDocuments` | Reviewed package facade |

## Test mapping

| Test path | Exact pytest node | Evidence ownership | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/topological/phase_sweep/test__Periodic2DTopologicalPhaseSweepEncodedDocuments.py` | `TestPeriodic2DTopologicalPhaseSweepEncodedDocuments::test_contract__owns_exact_ordered_payload_fields` | Class-owned routine software verification | Exact fields, defining owner, and no-copy synthetic bytes |
| same | `TestPeriodic2DTopologicalPhaseSweepEncodedDocuments::test_construction__rejects_wrong_and_empty_payloads` | Class-owned routine software verification | Wrong, subtyped, and empty payloads fail closed |
| same | `TestPeriodic2DTopologicalPhaseSweepEncodedDocuments::test_construction__is_frozen_and_slotted` | Class-owned routine software verification | Maintained state is frozen and slotted |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/topological/phase_sweep/test__integration__periodic_2d_topological_phase_sweep_encoded_document_artifacts.py` | `TestPeriodic2DTopologicalPhaseSweepEncodedDocumentArtifacts::test_retained_artifacts__preserve_bytes_and_catalog_identities` | Artifact-owned claim-bearing integration evidence | Exact retained bytes and checksum-catalog identities, not oracle qualification |
| same | `TestPeriodic2DTopologicalPhaseSweepEncodedDocumentArtifacts::test_public_routes__share_implementation_without_retired_name` | Artifact-owned integration evidence | Reviewed facades share one class and omit retired name/module routes |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/run/topological-phase-sweep.rst` | `ksdft2effmass.periodic2d.run.topological.phase_sweep.Periodic2DTopologicalPhaseSweepEncodedDocuments` | User-facing ownership narrative and autodoc |

## Evidence and claim boundary

| Evidence question | Status | Evidence or limitation |
|---|---|---|
| Exact field ownership and immutable representation | Supported | Routine class-owned tests |
| Exact retained bytes and SHA-256 identities | Supported | Artifact-owned integration test and maintained `SHA256SUMS` |
| Reviewed facades and retired-route absence | Supported | Exact class-identity and source-path absence assertions |
| Decoded schema and parameter-axis semantics | Not claimed | Owned by serializer, correlator, verifier, and campaign Actions |
| Availability of every parameter outcome | Not established | Encoded points do not prove complete or accepted outcomes |
| Numerical-oracle qualification | Not established | Encoded expected observations are retained content only |
| Topological phase or invariant correctness | Not claimed | No topological quantity is computed by this owner |
| Execution provenance | Not claimed | Content identity is not execution provenance |
| Scientific validation, UQ, or acceptance | Not claimed | No scientific decision or authority is owned |

## Provenance and limitations

Original local work under the repository license. Retained files and checksums are
repository-maintained content-identity evidence. Row 069 owns broader topological
campaign decomposition and must preserve distinctions among requested axes, available
and unavailable outcomes, encoded observations, independent verification, qualified
oracles, and scientific conclusions. Passing the mapped checks establishes bounded
software behavior only.
