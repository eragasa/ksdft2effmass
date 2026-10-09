# `Periodic2DOptimizerBasinEncodedDocuments`

## Purpose and migration status

This implemented immutable DataObject is the row-052 replacement for the retired
`Periodic2DOptimizerBasinCampaignModel`. It owns exact encoded input and result
documents for the retained periodic-2D Wannier90 optimizer-basin study. The former class
name and source module
`python/src/ksdft2effmass/periodic2d/model/retained/optimizer_basin.py` are absent rather
than preserved as aliases or forwarding routes.

The retained input describes nine mesh, cutoff, and auxiliary-embedding configurations,
eight smooth reciprocal-periodic unitary initial gauges, bounded execution limits, and
frozen convergence criteria. The retained result records 72 localization attempts and a
negative disposition: the observations do not support the frozen finite-parameter
convergence criteria. These are descriptions of encoded content. The byte owner neither
authenticates nor scientifically adopts those statements.

## Public contract and reviewed routes

The constructor accepts `input_payload` and `result_payload` and returns one frozen,
slotted DataObject. It has no decoding, filesystem, native-artifact discovery, gauge
construction, endpoint correlation, basin classification, verification, calculation,
convergence-assessment, oracle-qualification, or acceptance method.

Supported reviewed import routes are:

- `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.Periodic2DOptimizerBasinEncodedDocuments`;
- `ksdft2effmass.periodic2d.run.wannier90.Periodic2DOptimizerBasinEncodedDocuments`; and
- `ksdft2effmass.periodic2d.Periodic2DOptimizerBasinEncodedDocuments`.

All three routes expose the defining class object and none exposes the retired name.

## State and invariants

| Field | Representation | Meaning |
|---|---|---|
| `input_payload` | Exact nonempty built-in `bytes` | Encoded optimizer-basin study definition |
| `result_payload` | Exact nonempty built-in `bytes` | Encoded retained optimizer-basin result |

Field order is stable as listed. Construction rejects non-`bytes` values, including
`bytes` subclasses, with `TypeError`, and empty exact bytes with `ValueError`. Each
supplied byte object is retained without decoding, re-encoding, normalization,
coercion, or copying.

## Dependencies and data flow

The encoded-document class depends only on built-in bytes and dataclass immutability. It
imports no gauge, Wannier90 native-artifact, scientific-model, retained-space, operator,
serializer, verifier, basin classifier, oracle, repository, optimizer, or calculator
owner. The separate portable verifier consumes these wires through the shared
`StrictJsonDecoder`, which rejects invalid UTF-8, duplicate keys, nonstandard nonfinite
constants, and non-object document roots before campaign fields influence verification.
It also correlates identity, authority, bounded claim text, and distinct input/result
evidence-status roles; requires nine unique declaration and result configuration
identities before building lookup dictionaries; requires exactly eight unique endpoint
gauge identities per configuration; and requires duplicate-free nonconverged identities,
an exact-representation
recursive copy of the minimum-native-spread best endpoint, and confinement of every
directly declared compact source to the resolved repository root before reading it.
Declared provenance identities use the shared strict lowercase SHA-256 contract. The
verifier preserves per-configuration observed-only-best flags, the aggregate
non-global/non-general flag, aggregate process completion, the exact negative disposition,
and the joint best-and-median requirement. It correlates study axes, derives finest-pair
identities from axes and declared numerical controls rather than names, and requires
the four selected fields in each embedding-sensitivity summary to match the
corresponding fields in its identified configuration.

```text
caller-owned exact bytes -> optimizer-basin encoded-document DataObject -> explicit consumer
```

The class does not select schemas or infer initial-gauge semantics, endpoint completion,
basin identity, native-file availability, execution success, localization convergence,
global optimality, frame, provenance, or scientific meaning from filenames, paths,
hashes, shapes, dimensions, status labels, spectra, or reported trends.

## Retained artifact identity

Artifact-owned integration evidence reads the maintained directory
`calculations/research-monograph/periodic-2d-optimizer-basin/` and checks:

| Artifact | SHA-256 |
|---|---|
| `study-input.json` | `c2e0f601198be51d56da1ccacd03251491480e6602eb5a32633b7be6efd3fa6f` |
| `result.json` | `d3074c086f6d8071bb608cde25b5605b6898b55b749b27c32ae735256299ff85` |

Both identities are bound to maintained `SHA256SUMS` entries. These values establish
content identity only; they do not authenticate execution, native artifacts, completed
localizations, basin classifications, convergence, numerical correctness, or scientific
acceptance.

## Scientific, optimizer, and numerical boundary

The DataObject does not define a physical parent, Hamiltonian, initial-gauge action,
optimization functional, basin-equivalence relation, convergence sequence, retained
space, frame, geometry, units, energy reference, projector, represented operator,
convergence tolerance, uncertainty model, or acceptance criterion. It performs no
numerical operation and invokes neither Wannier90 nor another calculator.

The retained input states that its smooth reciprocal-periodic unitary gauges leave the
rank-three retained subspace unchanged. This separates initialization sensitivity from
subspace selection. The study then considers spread, periodic center sets, hopping
tails, basin occupancy, and endpoint convergence across mesh, cutoff, and embedding
variations. Those quantities remain distinct:

- different converged endpoints may represent different observed optimizer basins;
- a local convergence flag does not prove a global optimum;
- repeated basin occupancy is an empirical bounded diagnostic, not a theorem;
- mesh, cutoff, and embedding sensitivity are separate error sources; and
- a negative frozen convergence disposition must not be rewritten into a positive
  convergence claim.

The retained result reports that the frozen criteria were not supported. Row 052
preserves this result without independently validating it; dedicated verification owns
that responsibility. The companion [numerical-techniques and scientific-reasoning note](../../numerical-techniques-and-scientific-reasoning.md)
documents the gauge construction, parameter design, localization estimators, operational
basin quotient, frozen gates, numerical tolerance choices, portable-verification scope,
and limitations in detail. The [frozen portable-verification contract](../../verification-contract.md)
classifies every retained field as validated, correlated, preserved but uninterpreted,
or explicitly out of scope. Adding a new check is a reviewed contract change rather
than hygiene.

## Code mapping

| Code path | Qualified owner | Responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/encoded_documents.py` | `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.encoded_documents.Periodic2DOptimizerBasinEncodedDocuments` | Defining exact immutable byte container |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/__init__.py` | `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.Periodic2DOptimizerBasinEncodedDocuments` | Reviewed optimizer-basin facade |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/__init__.py` | `ksdft2effmass.periodic2d.run.wannier90.Periodic2DOptimizerBasinEncodedDocuments` | Reviewed Wannier90-run facade |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | `ksdft2effmass.periodic2d.Periodic2DOptimizerBasinEncodedDocuments` | Reviewed package facade |

## Test mapping

| Test path | Exact pytest node | Evidence ownership | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/test__Periodic2DOptimizerBasinEncodedDocuments.py` | `TestPeriodic2DOptimizerBasinEncodedDocuments::test_contract__owns_exact_ordered_payload_fields` | Class-owned routine software verification | Exact fields, defining owner, and no-copy synthetic bytes |
| same | `TestPeriodic2DOptimizerBasinEncodedDocuments::test_construction__rejects_wrong_and_empty_payloads` | Class-owned routine software verification | Wrong, subtyped, and empty payloads fail closed |
| same | `TestPeriodic2DOptimizerBasinEncodedDocuments::test_construction__is_frozen_and_slotted` | Class-owned routine software verification | Maintained state is frozen and slotted |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/test__Periodic2DOptimizerBasinCampaign__ownership.py` | `TestPeriodic2DOptimizerBasinCampaign` | Class-owned routine software verification | Exact document ownership, immutability, and request-scoped verifier composition |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/test__Periodic2DOptimizerBasinCampaignVerificationResult.py` | `TestPeriodic2DOptimizerBasinCampaignVerificationResult` | Class-owned routine software verification | Exact flags, nonnegative counts, digest syntax, immutability, and aggregate pass logic |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/test__Periodic2DOptimizerBasinCampaignVerifier__strict_decoding.py` | `TestPeriodic2DOptimizerBasinCampaignVerifierStrictDecoding::test_execute__rejects_ambiguous_or_nonstandard_input_wires` | Class-owned routine software verification | Shared strict decoding rejects duplicate keys, nonfinite constants, invalid UTF-8, and non-object roots |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/test__integration__periodic_2d_optimizer_basin_verifier_fail_closed.py` | `TestPeriodic2DOptimizerBasinCampaignVerifierFailClosed` | Artifact-owned adversarial integration evidence | Endpoint/nonconverged multiplicity, repository-source confinement, and missing-field boundaries fail closed |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/test__integration__periodic_2d_optimizer_basin_encoded_document_artifacts.py` | `TestPeriodic2DOptimizerBasinEncodedDocumentArtifacts::test_retained_artifacts__preserve_bytes_and_catalog_identities` | Artifact-owned claim-bearing integration evidence | Exact retained bytes and checksum-catalog identities, not optimizer or convergence evidence |
| same | `TestPeriodic2DOptimizerBasinEncodedDocumentArtifacts::test_public_routes__share_implementation_without_retired_name` | Artifact-owned integration evidence | Three reviewed facades share one class and omit retired name/module routes |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/run/optimizer-basin.rst` | `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.Periodic2DOptimizerBasinEncodedDocuments` | User-facing ownership narrative and autodoc |

## Evidence and claim boundary

| Evidence question | Status | Evidence or limitation |
|---|---|---|
| Exact field ownership and immutable representation | Supported | Routine class-owned tests |
| Exact retained bytes and SHA-256 identities | Supported | Artifact-owned integration test and maintained `SHA256SUMS` |
| Strict unambiguous verifier wire decoding | Supported | Shared decoder plus malformed-wire regressions |
| Intrinsic verification-result integrity | Supported | Exact scalar, range, digest, immutability, and pass-logic tests |
| Campaign metadata and evidence-role boundaries | Supported | Promotional-claim and evidence-status substitution regressions |
| Scientific non-global claim boundaries | Supported | Per-configuration and aggregate boundary-flag regressions |
| Aggregate process-completion consistency | Supported | Contradictory completion-summary regression |
| Configuration study-axis correlation | Supported | Axis-substitution regression |
| Finest-pair identity derivation | Supported | Valid-but-undeclared endpoint substitution regression |
| Frozen method and negative text | Supported | Joint-stability and disposition-promotion regressions |
| Embedding-summary correlation | Supported | Copied basin-count mutation regression |
| Strict provenance-digest representation | Supported | Shared SHA-256 validator and uppercase-digest regression |
| Unique configuration identities | Supported | Joint declaration/result duplicate regression before map construction |
| Exact endpoint and nonconverged multiplicity | Supported | Adversarial duplicate-entry regressions |
| Complete best-observed endpoint correlation | Supported | Gauge-preserving spread mutation and Boolean-to-integer substitution regressions |
| Repository-source confinement | Supported | Resolved containment plus absolute/traversal escape regressions |
| Reviewed facades and retired-route absence | Supported | Exact class-identity and source-path absence assertions |
| Encoded study design and negative disposition | Preserved, not adopted | Exact wires retain the declarations without interpreting them |
| Native Wannier90 artifact presence | Not established | No native-file owner or authenticated inventory is involved |
| Execution provenance or completion | Not claimed | Content identity and status fields are not execution evidence |
| Valid basin classification | Not established by this row | Requires explicit endpoint correlation and numerical verification |
| Global optimum | Not claimed | Multistart local optimization cannot imply global optimality |
| Finite-parameter convergence | Encoded disposition is negative | The retained result says the frozen criteria are not supported |
| Scientific validation, UQ, or acceptance | Not claimed | No scientific decision or authority is owned |

## Provenance and limitations

Original local work under the repository license. Retained files and checksums are
repository-maintained content-identity evidence. The compact documents cannot establish
historical execution or reconstruct missing native files. This is synthetic non-DFT
numerical study content, not material validation, production Wannierization, proof of a
global optimum, or a general localization-convergence theorem. Passing the mapped
checks establishes bounded software behavior only.
