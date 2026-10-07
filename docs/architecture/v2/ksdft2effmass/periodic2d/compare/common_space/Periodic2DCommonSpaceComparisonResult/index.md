# `Periodic2DCommonSpaceComparisonResult`

## Purpose and status

Implemented immutable ResultObject for row `PERIODIC-XWALK-036`. It records one
directional finite-representation comparison after the finite-difference operator has
been transported into the plane-wave common space. It is not a represented operator or
acceptance result.

## Public contract

Construction accepts the exact comparison Request, unitless `ComplexMatrixQuantity`
records for the sampling map, transported finite-difference operator, and signed
difference, plus unitless `ScalarQuantity` records for three diagnostics. There are no
mutating methods. Supported imports are `ksdft2effmass.periodic2d` and
`ksdft2effmass.periodic2d.compare`.

## State and identity

`plane_wave_to_grid` has shape `N**2` by `(2*M+1)**2` and maps ordered plane-wave
coefficients to ordered grid samples. `transported_finite_difference` and
`operator_difference` are square matrices in the plane-wave common space. The request
retains parent, Bloch fiber, geometry, energy zero, basis order, and comparison
identity. Every array is copied into immutable complex128 storage.

## Invariants and failure behavior

The Result requires exact quantity classes and `Unitless` units. It validates, by exact
complex128 array equality,

`transported_finite_difference == T.conj().T @ H_fd @ T`

and

`operator_difference == transported_finite_difference - H_pw`.

It recomputes the Frobenius isometry defect, difference Frobenius norm, and maximum
absolute difference. Type errors raise `TypeError`; unit, shape, algebra, and diagnostic
mismatches raise `ValueError`; nonfinite intrinsic arithmetic raises `OverflowError`.

## Dependencies and collaborators

The Result composes immutable quantities, a comparison Request, and the represented
matrices retained by that Request. It does not call the comparator's sampling-map
builder or depend on a private Action evaluation kernel.

## Data and action flow

The comparator derives request-dependent values for the returned outcome. Result
construction validates relations available from retained values. It does not
reconstruct the sampling map from momentum and indices, but it deliberately repeats
the dense congruence from retained `T` and `H_fd` to prevent forged transport. A valid
manually constructed Result still does not prove comparator execution or provenance.

## Serialization and compatibility

No serialized form or compatibility alias exists.

## Scientific and numerical boundary

The difference is dimensionless finite-representation disagreement. No diagnostic
threshold, continuum convergence claim, material interpretation, scientific
validation, or uncertainty model is attached. Parent-model, retention, reduction,
interpolation, and comparison errors remain separate.

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic2d/compare/common_space.py` | Class | `ksdft2effmass.periodic2d.compare.common_space.Periodic2DCommonSpaceComparisonResult` | Immutable comparison outcome and intrinsic algebra |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonResult.py` | `TestPeriodic2DCommonSpaceComparisonResult::test_construction__valid_result__retains_immutable_correlated_outputs` | Software verification | Shapes, immutability, and nonnegative diagnostics |
| same | `TestPeriodic2DCommonSpaceComparisonResult::test_construction__forged_transport__raises_value_error` | Software verification | Transport cannot be forged behind self-consistent downstream values |
| same | `TestPeriodic2DCommonSpaceComparisonResult::test_construction__forged_difference__raises_value_error` | Software verification | Signed subtraction correlation |
| same | `TestPeriodic2DCommonSpaceComparisonResult::test_construction__forged_isometry_defect__raises_value_error` | Software verification | Sampling-map diagnostic correlation |
| same | `TestPeriodic2DCommonSpaceComparisonResult::test_construction__forged_operator_norms__raise_value_error` | Software verification | Both difference diagnostics remain correlated |

## Sphinx mapping

`doc/sphinx/api/ksdft2effmass/periodic2d/common_space.rst` documents fields, equations,
error classes, construction boundaries, and excluded claims.

## Provenance

Original local work under the repository license. The authoritative finite mathematics
is `specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md`.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Positive and field-by-field mutation tests | Mapped Result module | Exact equality and expected exceptions | Python/NumPy | Synthetic cutoff-one five-point Result | Not applicable |
| Numerical verification | Not applicable | Result validation owns intrinsic algebra, not an independent numerical algorithm claim | Source contract | Exact retained-value equality | complex128 | Structurally valid values | Not applicable |
| Scientific validation | Not evaluated | No material or convergence protocol | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Separate decision required | Decision record when available | Not applicable | Not applicable | Row 036 | Named human authority required |

## Limitations and deviations

Exact algebra checks intentionally detect any bitwise change in one retained outcome.
Transport correlation adds one dense congruence evaluation and may raise `MemoryError`.
The Result does not authenticate that its map is the comparator-derived map; Action
execution and retained provenance require evidence outside manual Result construction.

## Detail navigation

No separate detail page is required; nontrivial mathematics and evidence are maintained
in the specification, module page, and Sphinx API page.
