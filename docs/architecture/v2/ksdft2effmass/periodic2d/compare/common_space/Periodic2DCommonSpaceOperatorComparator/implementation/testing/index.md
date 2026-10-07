# `Periodic2DCommonSpaceOperatorComparator` verification strategy

## Evidence separation

Row 036 has software-verification and bounded numerical-verification evidence. No test
is classified as scientific validation or uncertainty quantification. Synthetic
fixtures are not retained production calculations, and passing tests do not authorize
scientific use.

## Software fixtures and mutation oracle

The software Result fixture uses the dimensionless cosine parent with
`(lambda_x, lambda_y, lambda_xy) = (0.4, 0.7, 0.2)`, reduced momentum
`(0.1, -0.2)`, cutoff `M=1`, and `N=5` grid points per direction. The resulting map
has shape `25 by 9`; transported and difference matrices have shape `9 by 9`.

The positive test establishes immutable storage and directional shape. Negative tests
mutate one contract at a time:

- the transported matrix is changed, while the signed difference and its two norms are
  recomputed consistently from that forgery; rejection therefore specifically
  establishes `T^dagger H_fd T` correlation;
- the signed difference is replaced independently to establish subtraction
  correlation;
- the isometry defect is changed to establish correlation to retained `T`; and
- each operator norm is changed to establish correlation to retained `Delta H`.

These are exact structural or algebraic contracts, so their acceptance rule is exact
complex128/binary64 equality along the retained evaluation route. Introducing an
approximate tolerance would weaken the immutable Result contract and blur it with a
caller-owned numerical acceptance policy.

The Action-specific range test uses an exactly Hermitian synthetic grid matrix whose
entries equal the largest finite binary64 value. Dense transport must overflow for the
declared map, and the required behavior is an explicit `OverflowError`; accepted
nonfinite quantities or an incidental downstream `ValueError` would fail the contract.
This fixture has no physical interpretation.

## Independent numerical oracles

The equality-boundary case uses `M=2,N=5`, so the map is `25 by 25`. Discrete Fourier
orthogonality requires both `T.conj().T @ T` and `T @ T.conj().T` to equal identity.
The test checks both products with zero relative tolerance and `6e-15` absolute
tolerance. This explicitly covers the full-space unitary-similarity branch rather than
extrapolating from proper rectangular cutoff-one cases.

The remaining numerical tests do not reconstruct the production matrix-product
algorithm. They evaluate the centered-difference mode dispersion independently:

$$
\epsilon^{\mathrm{FD}}_{pq}
=\frac{4}{h^2}\left[
\sin^2\frac{(\kappa_x+p)h}{2}
+\sin^2\frac{(\kappa_y+q)h}{2}
\right].
$$

The free case uses `N=5`, `M=1`, and reduced momentum `(0.13, -0.21)`. The expected
transported matrix is the diagonal analytic dispersion; the expected difference is
that diagonal minus the continuum kinetic diagonal. Entrywise absolute tolerance is
`4e-15`, appropriate to the small complex128 transforms and unit-scale values in this
fixed case.

The cosine case uses `N=7`, `M=1`, reduced momentum `(-0.17, 0.09)`, and couplings
`(0.4, 0.7, 0.2)`. In this alias-free test domain, the resolved sampled potential
blocks agree with the plane-wave Fourier blocks, leaving the independently calculated
kinetic dispersion difference. The entrywise absolute tolerance is `6e-15`.

Neither tolerance is a production convergence criterion. Both are forward-error
bounds for fixed small binary64 examples.

## Compatibility evidence

Request tests independently establish that different configured parents, different
Bloch momenta, and a grid too small to distinguish retained reciprocal indices are
rejected. They do not infer compatibility from matrix shape, spectrum, or descriptive
names.

## Test mapping

| Test path | Owner | Evidence class | Validity domain |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonRequest.py` | `Periodic2DCommonSpaceComparisonRequest` | Software verification | Exact synthetic compatibility partitions |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceComparisonResult.py` | `Periodic2DCommonSpaceComparisonResult` | Software verification | Intrinsic cutoff-one five-point Result |
| `python/tests/software_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator__execute.py` | `Periodic2DCommonSpaceOperatorComparator` | Software verification | Synthetic complex128 overflow stress |
| `python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/test__Periodic2DCommonSpaceOperatorComparator.py` | `Periodic2DCommonSpaceOperatorComparator` | Numerical verification | Square-unitary boundary and declared free/cosine small-grid cases |

## Missing evidence and prohibited conclusions

The suite does not provide:

- an $N$-refinement or $M$-refinement convergence study;
- high-cutoff conditioning or resource benchmarks;
- general potential-aliasing coverage;
- arbitrary lattice or physical-unit coverage;
- comparison with a trusted material calculation;
- uncertainty propagation; or
- human scientific acceptance.

These omissions remain explicit rather than being filled by the green software and
numerical checks.

## Navigation

- [Comparator contract](../../index.md)
- [Implementation](../index.md)
- [Mathematics and physics](../mathematics/index.md)
- [References and provenance](../references/index.md)
