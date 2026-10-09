# `Periodic2DOptimizerReanalysisEncodedDocuments`

## Purpose and migration status

`Periodic2DOptimizerReanalysisEncodedDocuments` is the implemented row-053 replacement
for the retired `Periodic2DOptimizerReanalysisCampaignModel`. It is a frozen, slotted
DataObject that owns two exact encoded wires:

1. the retained row-052 optimizer-basin result consumed by offline reanalysis; and
2. the retained offline reanalysis result.

The former symbol and
`python/src/ksdft2effmass/periodic2d/model/retained/optimizer_reanalysis.py` are absent.
No compatibility alias or forwarding module is retained.

## Defining owner and reviewed routes

The defining owner is:

`ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis.encoded_documents.Periodic2DOptimizerReanalysisEncodedDocuments`

Reviewed facades expose that same class object through:

- `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis`;
- `ksdft2effmass.periodic2d.run.wannier90`; and
- `ksdft2effmass.periodic2d`.

The class has no decoding, filesystem, native-artifact discovery, classification,
verification, calculation, optimization, convergence-assessment, uncertainty, or
acceptance method.

## State and intrinsic invariants

| Field | Exact representation | Owned meaning |
|---|---|---|
| `source_result_payload` | Nonempty exact built-in `bytes` | Encoded source optimizer-basin result wire |
| `result_payload` | Nonempty exact built-in `bytes` | Encoded offline-reanalysis result wire |

Field order is stable as listed. The constructor rejects strings, mutable byte buffers,
`bytes` subclasses, and every other nonexact representation with `TypeError`. Empty exact
bytes raise `ValueError`. Valid objects retain caller-supplied byte objects without
copying, decoding, normalization, or re-encoding.

The encoded-document DataObject owns no repository root. Repository location and source
authentication belong to the verifier request and Action boundary.

## Composition and data flow

`Periodic2DOptimizerReanalysisCampaign` composes the encoded documents with a fresh
`Periodic2DOptimizerReanalysisCampaignVerifier` for each `verify()` request. The
campaign exposes no shared or replaceable verifier collaborator.

```text
exact source-result bytes + exact reanalysis-result bytes
    -> Periodic2DOptimizerReanalysisEncodedDocuments
    -> explicit verification request with repository_root
    -> request-scoped portable verifier Action
    -> immutable bounded verification Result
```

The verifier uses shared `StrictJsonDecoder` mechanics for strict UTF-8 object decoding,
duplicate-key rejection, nonstandard-nonfinite rejection, exact primitive checks, finite
binary64 conversion, and lowercase SHA-256 syntax. Campaign-specific schema,
correlation, classification, basin, and refinement responsibilities remain local to the
row-053 verifier.

## Retained artifact identities

Artifact-owned integration evidence binds the exact repository files:

| Role | Artifact | SHA-256 |
|---|---|---|
| Source optimizer-basin result | `calculations/research-monograph/periodic-2d-optimizer-basin/result.json` | `d3074c086f6d8071bb608cde25b5605b6898b55b749b27c32ae735256299ff85` |
| Offline reanalysis result | `calculations/research-monograph/periodic-2d-optimizer-basin/reanalysis-result.json` | `89780db50cb367f429a7947894805a89fbfc757f571a55f82936507ef397f38b` |

Both digests must equal the maintained `SHA256SUMS` entries. These identities establish
content identity only. They do not prove historical execution, provenance, scientific
meaning, numerical correctness, convergence, validation, uncertainty quantification, or
acceptance.

## Portable-verification boundary

The portable verifier authenticates:

- the encapsulated source-result bytes against the declared source digest;
- the maintained reanalysis and base-extractor source files after resolving them beneath
  the explicit repository root; and
- maintained common-estimator fixtures selected by logical basename and confined to the
  estimator-fixture directory.

It reconstructs only the frozen row-053 responsibilities:

- unique configuration, endpoint, and refinement identities;
- source/reanalysis configuration and endpoint correlation;
- gauge-dependent and total spread-component sums;
- the retained descriptive terminal-trace classification;
- aggregate classification counts;
- the bounded representative square-lattice basin partition;
- the complete best-observed converged endpoint copy; and
- the reported 512-to-1024 common-estimator refinement differences.

The exact field matrix is frozen in the companion
[portable-verification contract](verification-contract.md). Adding a field check or
changing a field interpretation is a reviewed semantic change, not code hygiene.

## Scientific and numerical limitations

The retained result describes offline post-hoc diagnostics for the bounded row-052
optimizer-basin observations. It does not change the row-052 negative disposition that
the observations do not support the frozen finite-parameter convergence criteria.

In particular:

- a native convergence flag does not prove a global optimum;
- a descriptive trace class is not a native convergence decision;
- a bounded basin partition is not proof of distinct mathematical stationary points;
- common-grid estimator agreement is separate from optimization convergence;
- mesh, plane-wave cutoff, auxiliary embedding, initialization, localization,
  truncation, and sampling errors remain distinct;
- the unavailable external native tree is not authenticated by portable verification;
  and
- passing software checks does not establish physical adequacy, scientific validation,
  uncertainty quantification, or acceptance.

Center-set comparison enumerates all orbital permutations and scales factorially with
retained rank. The retained campaign rank is three. No arbitrary rank cap is imposed;
large caller-supplied documents may raise `MemoryError`, and deeply nested JSON may raise
`RecursionError`.

## Code mapping

| Code path | Qualified owner | Responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/encoded_documents.py` | defining class above | Exact immutable wire ownership |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/decode.py` | `Periodic2DOptimizerReanalysisDocumentDecoder` | Strict schema adaptation to closed immutable records |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/records.py` | decoder-owned records | Immutable verifier-owned values and complete endpoint snapshots |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/authentication.py` | source-authentication Actions | Encapsulated-byte identity and confined direct-source authentication |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/numerics.py` | trace, spread, center, and basin Actions | Bounded numerical policies with explicit instantiated owners |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/correlation.py` | `Periodic2DOptimizerReanalysisCorrelator` | Source, endpoint, complete-best-copy, count, and basin correlation |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/refinement.py` | `OptimizerReanalysisRefinementVerifier` | Maintained-fixture authentication and refinement reconstruction |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/verify.py` | request, orchestration verifier, and Result owners | Request validation, cohesive Action composition, and bounded outcome |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/data.py` | `Periodic2DOptimizerReanalysisCampaign` | Immutable campaign composition and request-scoped verifier creation |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/__init__.py` | reviewed reanalysis facade | Explicit local public surface |
| `python/src/ksdft2effmass/periodic2d/run/wannier90/__init__.py` | reviewed Wannier90-run facade | Explicit parent public surface |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | reviewed periodic-2D facade | Explicit package public surface |

## Exact test mapping

| Test module | Exact pytest node | Ownership | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/test__Periodic2DOptimizerReanalysisEncodedDocuments.py` | `TestPeriodic2DOptimizerReanalysisEncodedDocuments::test_contract__owns_exact_ordered_payload_fields` | Class-owned routine | Field order, exact identities, and no repository root |
| same | `TestPeriodic2DOptimizerReanalysisEncodedDocuments::test_construction__rejects_wrong_and_empty_payloads` | Class-owned routine | Wrong, subtyped, mutable, and empty payloads fail closed |
| same | `TestPeriodic2DOptimizerReanalysisEncodedDocuments::test_construction__is_frozen_and_slotted` | Class-owned routine | Frozen, slotted maintained state |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/test__Periodic2DOptimizerReanalysisCampaignContracts.py` | `TestPeriodic2DOptimizerReanalysisCampaignContracts::test_campaign__owns_documents_without_shared_verifier` | Class-owned routine | Exact campaign ownership and request-scoped verifier composition |
| same | `TestPeriodic2DOptimizerReanalysisCampaignContracts::test_result__validates_state_and_pass_conjunction` | Class-owned routine | Exact flags, count ranges, digest syntax, immutability, and conjunction-only pass logic |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/test__Periodic2DOptimizerReanalysisActionOwnership.py` | `TestPeriodic2DOptimizerReanalysisActionOwnership::test_actions__use_instantiated_owners_without_static_namespaces` | Class-owned routine | Cohesive Actions use instances and expose no static/class-method utility namespaces |
| same | `TestPeriodic2DOptimizerReanalysisActionOwnership::test_verifier__composes_cohesive_request_scoped_actions` | Class-owned routine | Top-level verifier owns orchestration only and exposes no private computational kernel |
| same | `TestPeriodic2DOptimizerReanalysisActionOwnership::test_action_requests__reject_implicit_numeric_and_path_coercion` | Class-owned routine | Numeric and repository request boundaries reject Boolean/integer substitution and relative roots |
| same | `TestPeriodic2DOptimizerReanalysisActionOwnership::test_reviewed_modules__have_no_module_functions` | Class-owned routine | Row-053 and changed shared immutable-JSON ownership contain no module-level function namespace |
| same | `TestPeriodic2DOptimizerReanalysisActionOwnership::test_public_methods__retain_numpy_style_contract_sections` | Class-owned routine | Public-by-name reviewed methods retain NumPy-style parameter and return contracts |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/test__Periodic2DOptimizerReanalysisCampaignVerifier__strict_decoding.py` | `TestPeriodic2DOptimizerReanalysisCampaignVerifierStrictDecoding::test_execute__rejects_ambiguous_or_nonstandard_source_wires` | Class-owned routine | Duplicate keys, nonstandard nonfinite constants, invalid UTF-8, and non-object roots fail closed |
| same | `TestPeriodic2DOptimizerReanalysisCampaignVerifierStrictDecoding::test_execute__rejects_schema_before_schema_specific_field_access` | Class-owned routine | Schema selection precedes version-one field adaptation |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/test__integration__periodic_2d_optimizer_reanalysis_artifacts.py` | `TestPeriodic2DOptimizerReanalysisArtifacts::test_retained_artifacts__preserve_bytes_and_catalog_identities` | Artifact-owned claim-bearing | Exact retained bytes and checksum-catalog identities |
| same | `TestPeriodic2DOptimizerReanalysisArtifacts::test_retained_documents__decode_to_closed_immutable_records` | Artifact-owned claim-bearing | Retained wires adapt to closed frozen records with tuple-owned nested collections |
| same | `TestPeriodic2DOptimizerReanalysisArtifacts::test_retained_campaign__passes_bounded_portable_verification` | Artifact-owned claim-bearing | Compact-source authentication and bounded 72-endpoint/four-refinement reconstruction |
| same | `TestPeriodic2DOptimizerReanalysisArtifacts::test_public_routes__share_identity_and_retired_model_is_absent` | Artifact-owned integration | Three reviewed routes share one class; retired name and module are absent |
| `python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/test__integration__periodic_2d_optimizer_reanalysis_verifier_fail_closed.py` | `TestPeriodic2DOptimizerReanalysisVerifierFailClosed` | Artifact-owned adversarial integration | Identity multiplicity, confinement, digest, best-copy, and refinement boundaries fail closed |

Test ownership metadata is maintained at:

`python/tests/software_verification/ksdft2effmass/periodic2d/run/wannier90/optimizer_basin/reanalysis/resources/implementation-verification-ownership.json`

## Sphinx mapping

| Sphinx path | Public route | Role |
|---|---|---|
| `doc/sphinx/api/research-monograph-campaigns.rst` | `ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.reanalysis` | User-facing narrative and explicit encoded-document, campaign, request, and Result autodoc |
| `doc/sphinx/concepts/periodic2d-controlled-reduction.rst` | campaign concept narrative | Scientific distinction between original observations and offline diagnostics |

## Evidence status

| Question | Status |
|---|---|
| Exact immutable wire ownership | Supported by routine class-owned tests |
| Exact retained bytes and checksum identities | Supported by artifact-owned integration evidence |
| Strict unambiguous JSON decoding | Supported by shared decoder and malformed-wire evidence |
| Compact repository-source confinement and authentication | Supported by retained and adversarial evidence |
| Bounded spread, classification, basin, and refinement reconstruction | Supported within the frozen field contract |
| External native-file authenticity | Not established |
| Historical execution provenance | Not established by content hashes |
| Global optimality or general optimizer convergence | Not claimed |
| Scientific validation, uncertainty quantification, or acceptance | Not claimed |

Original local work is retained under the repository license. No Quantum ESPRESSO or
Wannier90 execution is required or performed by this capability.
