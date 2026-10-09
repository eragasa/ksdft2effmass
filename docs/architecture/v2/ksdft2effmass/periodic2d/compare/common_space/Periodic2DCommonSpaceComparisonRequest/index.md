# `Periodic2DCommonSpaceComparisonRequest`

## Purpose and status

Implemented immutable RequestObject for one comparison between complete cosine-model
plane-wave and finite-difference represented results.

## Public contract

Construction accepts `plane_wave`, `finite_difference`, and a nonempty
`comparison_identifier`. The `common_dimension` property returns `(2*M+1)**2`. The
supported import routes are `ksdft2effmass.periodic2d` and
`ksdft2effmass.periodic2d.compare`.

## State and identity

The two Results retain the exact configured toy parent, reduced Bloch momentum, finite
basis definitions, matrices, geometry conventions, dimensionless energy scale, and
model energy zero. `comparison_identifier` identifies the comparison convention; it
does not replace parent or represented-space identities.

## Invariants and failure behavior

Fields require exact semantic classes. Parent values and both momentum components must
match exactly. `2*M+1 <= N` prevents reciprocal-index aliasing on the coordinate grid.
Wrong types raise `TypeError`; empty identity or incompatible represented inputs raise
`ValueError`. Matrix dimension or spectrum is never used to infer compatibility.

## Dependencies and collaborators

The Request composes `Periodic2DPlaneWaveHamiltonianResult` and
`Periodic2DFiniteDifferenceHamiltonianResult`. Their defining constructors remain
responsible for matrix validity and representation metadata.

## Data and action flow

Represented constructors produce independently valid inputs; this Request binds one
compatible pair; `Periodic2DCommonSpaceOperatorComparator.execute` derives the map and
comparison Result.

## Serialization and compatibility

No serializer or wire compatibility contract is provided.

## Scientific and numerical boundary

The alias condition makes the finite sampling columns distinct; it does not establish
grid convergence. Compatibility is specific to the fixed dimensionless cosine adapter
family and is not a generic operator-alignment proof.

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic2d/compare/common_space.py` | Class | `ksdft2effmass.periodic2d.compare.common_space.Periodic2DCommonSpaceComparisonRequest` | Comparison identity and prerequisites |
| `python/src/ksdft2effmass/periodic2d/compare/common_space.py` | Property | `Periodic2DCommonSpaceComparisonRequest.common_dimension` | Plane-wave common-space dimension |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonRequest.py` | `TestPeriodic2DCommonSpaceComparisonRequest::test_construction__compatible_results__retains_common_dimension` | Software verification | Compatible pair and dimension |
| same | `TestPeriodic2DCommonSpaceComparisonRequest::test_construction__different_model__raises_value_error` | Software verification | Parent mismatch rejection |
| same | `TestPeriodic2DCommonSpaceComparisonRequest::test_construction__different_momentum__raises_value_error` | Software verification | Bloch-fiber mismatch rejection |
| same | `TestPeriodic2DCommonSpaceComparisonRequest::test_construction__aliased_basis__raises_value_error` | Software verification | Alias-precondition rejection |

## Sphinx mapping

`doc/sphinx/api/ksdft2effmass/periodic2d/common_space.rst` documents the supported
request and common-space prerequisites.

## Provenance

Original local work under the repository license. The governing contract is
`specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md`.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Positive and incompatibility tests | Mapped Request module | Exact values and expected exceptions | Python/NumPy | Synthetic cosine represented inputs | Not applicable |
| Numerical verification | Not applicable | Request construction performs no numerical comparison | Source contract | Exact prerequisites | Python/NumPy | Request fields | Not applicable |
| Scientific validation | Not evaluated | No physical adequacy protocol | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Separate decision required | Decision record when available | Not applicable | Not applicable | Row 036 request | Named human authority required |

## Limitations and deviations

Only equal configured cosine parents and exact equal binary64 momentum values are
supported. No tolerance-based identity matching or implicit alignment is performed.

## Detail navigation

No separate detail page is required; construction and compatibility are fully stated
here and in the module/Sphinx pages.
