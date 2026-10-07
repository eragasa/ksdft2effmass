# `Periodic2DCommonSpaceOperatorComparator`

## Purpose and status

`Periodic2DCommonSpaceOperatorComparator` is the implemented ActionObject for the
operation in `PERIODIC-XWALK-036`. Its purpose is to make two independently valid but
non-subtractable finite representations comparable without pretending that they
already act in the same state space.

The finite-difference matrix acts on ordered coordinate-grid values in
`C**(N**2)`. The plane-wave matrix acts on ordered reciprocal coefficients in
`C**((2*M+1)**2)`. The Action therefore constructs an explicit map from the
plane-wave coefficient space into the coordinate-grid space, pulls the grid operator
back through that map, and only then forms a signed matrix difference in the
plane-wave common space. Retaining the map and transported operator makes this
alignment inspectable instead of hiding it behind equal matrix sizes or a norm.

The operation is deliberately threshold-free. It reports finite-representation
disagreement and does not decide whether the disagreement is sufficiently small,
converged, physically adequate, or scientifically acceptable.

## Public contract

`execute(request)` accepts exactly `Periodic2DCommonSpaceComparisonRequest` and returns
`Periodic2DCommonSpaceComparisonResult`. The supported imports are
`ksdft2effmass.periodic2d` and `ksdft2effmass.periodic2d.compare`.

## State and identity

The Action has no fields or hidden mutable state. All scientific and represented-space
identity enters through the Request and is retained unchanged by the Result.

## Invariants and failure behavior

The Action constructs the normalized period-`2*pi` plane-wave sampling map in declared
row/column order, performs `T.conj().T @ H_fd @ T`, subtracts `H_pw`, and computes the
Frobenius/max diagnostics. Wrong Request type raises `TypeError`; nonrepresentable
transport, subtraction, or diagnostics raise `OverflowError`; allocation failure may
raise `MemoryError`.

## Dependencies and collaborators

The Action uses NumPy dense complex128 operations and composes the Request and Result
owners. It does not call calculators, eigensolvers, serializers, registries, plugins,
or external execution.

## Data and action flow

1. Read the two complete represented Results from the validated comparison Request.
   Their exact adapter types fix the common cosine parent, period-`2*pi` geometry,
   dimensionless energy convention, model energy zero, scalar-spin convention, basis
   normalization, and basis orderings.
2. Enumerate the half-open coordinate points and the retained reciprocal indices. The
   alias prerequisite `2*M+1 <= N` has already ensured that distinct retained indices
   remain distinct on the grid; it has not asserted convergence.
3. Build one normalized one-dimensional sampling matrix in each coordinate direction.
   Each entry evaluates the declared Bloch plane wave at one grid point, including the
   reduced momentum rather than silently comparing periodic parts at a different
   fiber.
4. Take the Kronecker product in the fixed first-index-outer convention. Its rows are
   `(x, y)` grid sites and its columns are `(p, q)` plane waves; no transpose,
   flattening guess, or post-hoc permutation is permitted.
5. Pull the coordinate-grid operator into the plane-wave common space by
   `T.conj().T @ H_fd @ T`. This is a finite representation transform, not a retained-
   space projection, disentanglement, downfolding, or continuum limit.
6. Form the signed difference `H_fd_tilde - H_pw`. Reversing the sign would define a
   different reported comparison and is not treated as a storage convention.
7. Evaluate the map-isometry defect and two operator-difference norms. These values are
   observations; the Action has no pass/fail tolerance.
8. Construct the immutable Result. The Result rechecks algebra available from its
   retained values, including the transport relation, but does not reconstruct the
   request-dependent map or claim that manual Result construction proves Action
   execution.

## Serialization and compatibility

The Action produces no wire format and provides no compatibility alias.

## Scientific and numerical boundary

The Action evaluates finite dense matrices only. It applies no threshold and provides
no continuum extrapolation, parent-model assessment, effective-model reduction,
scientific validation, uncertainty quantification, or acceptance status.

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic2d/compare/common_space.py` | Class | `ksdft2effmass.periodic2d.compare.common_space.Periodic2DCommonSpaceOperatorComparator` | Directional comparison Action |
| same | Method | `Periodic2DCommonSpaceOperatorComparator.execute` | Request-to-Result derivation |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator.py` | `TestPeriodic2DCommonSpaceOperatorComparator::test_execute__equal_basis_and_grid_sides__map_is_unitary` | Provisional numerical verification | Candidate DFT-orthogonality consumer: at `M=2,N=5`, both map products equal identity to absolute tolerance `6e-15`; not accepted until qualification |
| same | `TestPeriodic2DCommonSpaceOperatorComparator::test_execute__free_operator__matches_discrete_fourier_dispersion` | Provisional numerical verification | Candidate dispersion consumer: free centered-difference relation after transport, absolute tolerance `4e-15`; not accepted until qualification |
| same | `TestPeriodic2DCommonSpaceOperatorComparator::test_execute__cosine_operator__isolates_discrete_kinetic_error` | Provisional numerical verification | Candidate dispersion consumer: resolved cosine Fourier blocks cancel, absolute tolerance `6e-15`; not accepted until qualification |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonResult.py` | `TestPeriodic2DCommonSpaceComparisonResult::test_construction__valid_result__retains_immutable_correlated_outputs` | Software verification | Representative Action-to-Result route |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator__execute.py` | `TestPeriodic2DCommonSpaceOperatorComparatorExecute::test_execute__transport_overflow__raises_overflow_error` | Software verification | Nonfinite transport fails closed as `OverflowError` |

## Sphinx mapping

`doc/sphinx/api/ksdft2effmass/periodic2d/common_space.rst` documents the algorithm,
formula, units, complexity, failures, and limitations.

## Provenance

Original local work under the repository license. The governing convention is
`specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md`.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Representative valid route and fail-closed range stress | Mapped Result and Action tests | Exact structural assertions and expected `OverflowError` | Python/NumPy | Cutoff one, five grid points; synthetic maximum-range stress | Not applicable |
| Numerical verification | Not evaluated | Consumer nodes exist, but the two analytic references remain candidate oracles pending separate qualification | Mapped numerical tests and [testing strategy](implementation/testing/index.md) | Entrywise absolute `4e-15` and `6e-15` after qualification | complex128/binary64 | Proposed: `M=2,N=5` square map; free five-point and cosine seven-point grids at `M=1` | Not applicable |
| Scientific validation | Not evaluated | No physical adequacy or convergence reference | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Separate decision required | Decision record when available | Not applicable | Not applicable | Row 036 | Named human authority required |

## Limitations and deviations

Dense storage for the map scales as `N**2 * (2*M+1)**2`; matrix products add dense
working storage and may exhaust memory. No sparse fallback, arbitrary cap, or general
lattice adapter is provided.

## Detail navigation

- [Implementation and data flow](implementation/index.md)
- [Mathematics and physics](implementation/mathematics/index.md)
- [References and provenance](implementation/references/index.md)
- [Verification strategy](implementation/testing/index.md)
