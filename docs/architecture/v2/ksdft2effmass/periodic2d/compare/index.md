# `ksdft2effmass.periodic2d.compare`

## Purpose and status

This implemented subpackage owns explicit comparison of the cosine-model plane-wave
and finite-difference represented operators after directional transport into one finite
common space. It owns no scientific acceptance policy.

## Public contract

The package initializer deliberately exports
`Periodic2DCommonSpaceComparisonRequest`,
`Periodic2DCommonSpaceComparisonResult`, and
`Periodic2DCommonSpaceOperatorComparator`. Their defining module is
[`common_space`](common_space/index.md).

## Ownership boundary

This package owns represented-input compatibility, the project-specific normalized
sampling convention, grid-to-plane-wave transport, signed subtraction, and
threshold-free diagnostics. Represented matrices remain owned by the plane-wave and
finite-difference constructors. PhysKit owns lattice primitives. Parent selection,
retention, reduction, convergence protocols, scientific validation, and acceptance are
outside this package.

## Dependency rules

The package may depend on exact periodic2d cosine adapter results and immutable operator
quantities. Campaign execution, persistence, calculator integration, dynamic discovery,
and reverse dependencies from PhysKit are prohibited.

## Child map

- [Common-space comparison module](common_space/index.md)
  - [`Periodic2DCommonSpaceComparisonRequest`](common_space/Periodic2DCommonSpaceComparisonRequest/index.md)
  - [`Periodic2DCommonSpaceComparisonResult`](common_space/Periodic2DCommonSpaceComparisonResult/index.md)
  - [`Periodic2DCommonSpaceOperatorComparator`](common_space/Periodic2DCommonSpaceOperatorComparator/index.md)

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic2d/compare/__init__.py` | Package | `ksdft2effmass.periodic2d.compare` | Deliberate comparison facade |
| `python/src/ksdft2effmass/periodic2d/compare/common_space.py` | Module | `ksdft2effmass.periodic2d.compare.common_space` | Defining comparison implementation |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonRequest.py` | `TestPeriodic2DCommonSpaceComparisonRequest` | Software verification | Compatibility and alias preconditions |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonResult.py` | `TestPeriodic2DCommonSpaceComparisonResult` | Software verification | Immutable structure and intrinsic algebra |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator__execute.py` | `TestPeriodic2DCommonSpaceOperatorComparatorExecute` | Software verification | Fail-closed complex128 transport range |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__common_space_oracle_records.py` | `TestPeriodic2DCommonSpaceOracleRecords` | Software verification | Bounded candidate-record, exact-node, dependency-direction, and empty-ledger structure |
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/test__common_space_oracle_qualification.py` | `TestPeriodic2DCommonSpaceOracleQualification` | Candidate qualification evidence | Independent finite DFT, stencil-action, cosine-transfer, and alias-boundary checks |
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator.py` | `TestPeriodic2DCommonSpaceOperatorComparator` | Provisional numerical verification | Consumers of candidate DFT isometry/unitarity, finite-difference dispersion, and resolved cosine-transfer records; not accepted until reviewed-revision dispositions and the acceptance gate |

## Provenance

Original local work under the repository license. The mathematical contract is
`specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md`.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Exact positive and mutation tests | Mapped software modules | Exact types, arrays, units, shapes, and exceptions | Supported Python/NumPy environment | Synthetic cutoff-one five-point case and negative prerequisites | Not applicable |
| Numerical verification | Not evaluated | Candidate records and independent qualification checks exist, but the disposition ledger is empty and no acceptance gate has passed | Mapped numerical modules and [oracle dossiers](common_space/oracles/index.md) | Entrywise absolute tolerances `4e-15` and `6e-15` after qualification | complex128/binary64 | `M=2,N=5` map boundary and fixed synthetic free/cosine cases | Not applicable |
| Scientific validation | Not evaluated | No material or continuum-adequacy protocol | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Commit, merge, and scientific acceptance remain separate | Human decision when available | Not applicable | Not applicable | Changed row-036 contract | Named human authority required |

## Limitations and deviations

The package is specialized to the dimensionless period-`2*pi` cosine adapters, dense
square grids, and symmetric square plane-wave cutoffs. It does not serialize Results,
compare arbitrary `OperatorRecord` instances, or infer missing scientific identity.
