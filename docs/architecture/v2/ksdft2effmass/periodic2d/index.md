# `ksdft2effmass.periodic2d`

## Purpose and status

`ksdft2effmass.periodic2d` owns canonical two-dimensional scientific definitions,
represented-space comparisons, controlled defects, and campaign surfaces. The package
and assigned crosswalk rows are implemented. Scientific-model adoption remains bounded
by authenticated evidence; unavailable frame/projector coordinates are not inferred.

The package now owns a parent-qualified selected-band retention definition. That
DataObject declares a selection contract only; it does not claim that preserved
periodic2d campaign results contain a retained subspace or exact retained operator.

## Public contract

The package root deliberately exports supported two-dimensional campaign records,
comparison Actions and results, defect records and Actions, encoded-document owners,
and `Periodic2DSelectedBandRetentionDefinition`. Exact supported names are declared by
`ksdft2effmass.periodic2d.__all__`.

| Child owner | Public responsibility | Canonical page |
|---|---|---|
| `periodic2d.retention` | Parent-qualified two-dimensional selected-band retention definitions | [Retention definitions](retention/index.md) |
| `periodic2d.campaign` | Independent two-dimensional campaign composition, encoded documents, and typed one-band operations | [Campaigns](campaign/index.md) |
| `periodic2d.compare` | Explicit represented-operator transport and threshold-free comparison | [Common-space comparison](compare/index.md) |
| `periodic2d.defects` | Controlled finite-extent scalar-hopping defect definitions and represented analyses | [Defect models and analyses](defects/index.md) |
| `periodic2d.model` | Two-dimensional toy-model and representation-specific definitions | [Controlled models](model/index.md) |
| `periodic2d.run` | Preserved executable campaign families and encoded-document owners | [Run families](run/index.md) |

Family topic pages map the defining modules, reviewed facades, exact tests, provenance,
evidence, and scientific limitations for the migrated campaign rows.

## Ownership boundary

This package may specialize the general contracts from `ksdft2effmass.periodic` for
exactly two periodic dimensions. It owns project-specific identity, provenance,
retention, comparison, and campaign policy. Reusable direct and reciprocal lattice
primitives remain owned by PhysKit. Generic finite represented operators remain owned
by `ksdft2effmass.operators`.

A selected-band interval does not supply parent-model, parent-operator, ambient-space,
reciprocal-domain, projector, frame, gauge, or provenance identity. Equal dimensions,
rank, spectra, or route names do not establish those meanings.

## Dependency rules

Permitted direct dependencies include the general `ksdft2effmass.periodic` contracts,
reusable analysis and operator records, and pinned PhysKit lattice primitives. Campaign
and filesystem behavior must not flow into scientific retention DataObjects. PhysKit
must not depend on this package.

## Child map

- [Retention definitions](retention/index.md)
  - [`Periodic2DSelectedBandRetentionDefinition`](retention/Periodic2DSelectedBandRetentionDefinition/index.md)
- [Common-space comparison](compare/index.md)
  - [`Periodic2DCommonSpaceComparisonRequest`](compare/common_space/Periodic2DCommonSpaceComparisonRequest/index.md)
  - [`Periodic2DCommonSpaceComparisonResult`](compare/common_space/Periodic2DCommonSpaceComparisonResult/index.md)
  - [`Periodic2DCommonSpaceOperatorComparator`](compare/common_space/Periodic2DCommonSpaceOperatorComparator/index.md)
- [Controlled models](model/index.md)
  - [Cosine toy model](model/toy_models/cosine/index.md)
- [Defect models and analyses](defects/index.md)
  - [`Periodic2DScalarHoppingDefectModel`](defects/base/Periodic2DScalarHoppingDefectModel/index.md)
- [Campaigns](campaign/index.md)
  - [One-band isolated campaign](campaign/nbands_1/index.md)
  - [`Periodic2DIsolatedBandEncodedDocuments`](campaign/nbands_1/encoded_documents/Periodic2DIsolatedBandEncodedDocuments/index.md)
- [Periodic2d migration boundary](../periodic/periodic2d/index.md)
- [Run families](run/index.md)
  - [Composite campaign](run/composite/index.md)
  - [`Periodic2DCompositeEncodedDocuments`](run/composite/encoded_documents/Periodic2DCompositeEncodedDocuments/index.md)
  - [Topological campaign](run/topological/index.md)
  - [`Periodic2DTopologicalEncodedDocuments`](run/topological/encoded_documents/Periodic2DTopologicalEncodedDocuments/index.md)
  - [Topological phase sweep](run/topological/phase_sweep/index.md)
  - [`Periodic2DTopologicalPhaseSweepEncodedDocuments`](run/topological/phase_sweep/encoded_documents/Periodic2DTopologicalPhaseSweepEncodedDocuments/index.md)
  - [Wannier90 campaign families](run/wannier90/index.md)
  - [Balanced Wannier90 campaign](run/wannier90/balanced/index.md)
  - [`Periodic2DWannier90BalancedEncodedDocuments`](run/wannier90/balanced/encoded_documents/Periodic2DWannier90BalancedEncodedDocuments/index.md)
  - [Wannier90 bounded sensitivity study](run/wannier90/study/index.md)
  - [`Periodic2DWannier90StudyEncodedDocuments`](run/wannier90/study/encoded_documents/Periodic2DWannier90StudyEncodedDocuments/index.md)
  - [Wannier90 optimizer-basin family](run/wannier90/optimizer_basin/index.md)
  - [`Periodic2DOptimizerBasinEncodedDocuments`](run/wannier90/optimizer_basin/encoded_documents/Periodic2DOptimizerBasinEncodedDocuments/index.md)
- [Periodic2d capability-parity gate](../periodic2d-capability-parity.md)

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic2d/__init__.py` | Package | `ksdft2effmass.periodic2d` | Deliberate public two-dimensional API |
| `python/src/ksdft2effmass/periodic2d/retention.py` | Module | `ksdft2effmass.periodic2d.retention` | Parent-qualified two-dimensional retention definitions |
| `python/src/ksdft2effmass/periodic2d/retention.py` | Class | `ksdft2effmass.periodic2d.retention.Periodic2DSelectedBandRetentionDefinition` | Defining selected-band retention class |
| `python/src/ksdft2effmass/periodic2d/compare/common_space.py` | Module | `ksdft2effmass.periodic2d.compare.common_space` | Directional common-space comparison owner |
| `python/src/ksdft2effmass/periodic2d/compare/common_space.py` | Class | `ksdft2effmass.periodic2d.Periodic2DCommonSpaceComparisonResult` | Supported root route to the defining comparison Result |
| `python/src/ksdft2effmass/periodic2d/model/toy_models/cosine.py` | Class | `ksdft2effmass.periodic2d.Periodic2DCosinePotentialToyModel` | Controlled dimensionless cosine scientific parent |
| `python/src/ksdft2effmass/periodic2d/defects/base.py` | Class | `ksdft2effmass.periodic2d.Periodic2DScalarHoppingDefectModel` | Controlled scalar-hopping defect scientific model |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | Class | `ksdft2effmass.periodic2d.Periodic2DSelectedBandRetentionDefinition` | Supported package-root re-export of the defining class |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py` | `TestPeriodic2DSelectedBandRetentionDefinition::test_public_api__package__exports_supported_definition` | Software verification | The package deliberately exports the two-dimensional retention definition |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonRequest.py` | `TestPeriodic2DCommonSpaceComparisonRequest` | Software verification | Common-parent, fiber, identity, and alias prerequisites |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonResult.py` | `TestPeriodic2DCommonSpaceComparisonResult` | Software verification | Immutable transport, signed difference, and diagnostic correlation |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator__execute.py` | `TestPeriodic2DCommonSpaceOperatorComparatorExecute` | Software verification | Explicit transport-overflow failure |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__common_space_oracle_records.py` | `TestPeriodic2DCommonSpaceOracleRecords` | Software verification | Closed row-036 oracle-resource structure and dependency direction |
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/test__common_space_oracle_qualification.py` | `TestPeriodic2DCommonSpaceOracleQualification` | Qualification evidence | Independent finite-algebra checks for all three records, bound to reviewed revision `f37e5d722f8c9007d8ea55c06e808c9c73bf775d` |
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator.py` | `TestPeriodic2DCommonSpaceOperatorComparator` | Bounded numerical verification after proposal acceptance | Consumers of three qualified oracles: DFT orthogonality, centered-difference dispersion, and resolved cosine Fourier transfer |
| `python/tests/ksdft2effmass/periodic2d/model/toy_models/test__Periodic2DCosinePotentialToyModel.py` | `TestPeriodic2DCosinePotentialToyModel` | Software verification | Cosine parent identity, coefficients, lattice convention, and scalar boundary |
| `python/tests/software_verification/ksdft2effmass/periodic2d/defects/test__Periodic2DDefect.py` | `TestPeriodic2DDefect` | Software verification | Defect identity/parentage and represented composition, extraction, and locality |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Exact export and invariant tests | Mapped pytest class | Exact assertions | Supported Python environment | New retention definition | Not applicable |
| Numerical verification | Not applicable | Definition performs no numerical construction | Source contract | Not applicable | Not applicable | Selection metadata | Not applicable |
| Scientific validation | Not evaluated | No model-adequacy claim | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Review and merge remain separate | Review record when available | Not applicable | Not applicable | Changed contract | Named human authority required |

## Limitations and deviations

The canonical comparison package, module, and class pages map row 036. Its production
and software-verification contracts are complete. Its numerical evidence is `Supported`
only for the recorded fixed domains after the three analytic oracles' reviewed-revision
dispositions pass the exact proposal acceptance gate.
Untouched legacy modules do not yet have complete canonical module/class mirrors and are
not silently declared complete here. Existing migration and capability pages remain the
authoritative status records for those owners.
