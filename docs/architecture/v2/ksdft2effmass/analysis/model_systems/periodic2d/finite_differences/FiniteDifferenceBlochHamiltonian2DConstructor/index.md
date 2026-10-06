# `FiniteDifferenceBlochHamiltonian2DConstructor`

## Purpose and public contract

This implemented row-035 Action owns the only centered finite-difference matrix
assembly algorithm used by the reusable route and cosine campaign adapter. It is
supported from `ksdft2effmass.analysis.model_systems`.

For spacing `h=L/N`, it constructs one-dimensional negative-Laplacian blocks with
`2*c` diagonal, `-c` nearest-neighbor entries, `c=E_K/h**2`, and the request's directed
Bloch seams. Their Kronecker sum preserves `x_outer_y_inner` order. Immutable sampled
potential values are added diagonally in the same order.

## Failures and resource behavior

- Wrong request semantics raise `TypeError`.
- Model/request construction rejects unrepresentable spacing, coefficient, diagonal,
  and phase values before execution.
- A defensive final nonfinite check raises `OverflowError`.
- The dense matrix dimension is `N**2` and storage scales as `O(N**4)`; allocation
  failure propagates as `MemoryError`. No arbitrary grid cap is imposed.

The Action performs no eigensolve, continuum extrapolation, common-space transport,
error acceptance, or scientific validation.

## Code, Sphinx, and tests

| Surface | Mapping |
|---|---|
| Class | `python/src/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.py::FiniteDifferenceBlochHamiltonian2DConstructor` |
| Sphinx | `doc/sphinx/api/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.rst` |
| Canonical test source | [`tests.py`](tests.py) |

| Pytest node | Evidence class | Oracle and comparator |
|---|---|---|
| `TestFiniteDifferenceBlochHamiltonian2DConstructor::test_execute_matches_declared_stencil_and_directed_bloch_seams` | Numerical verification | Analytic selected entries; exact structural assertions and complex absolute tolerance `2e-15` |

The synthetic case uses a five-by-five Euclidean grid, unitless scale `1.7`, explicit
real potential samples, and two nonzero seam phases. It checks diagonal and neighbor
coefficients, both directed seam pairs, one structural zero, exact Hermiticity, request
identity, and immutable storage. The validity domain is this declared finite
representation; it does not establish continuum convergence.

`tests.py` is a relative symlink to the single runnable numerical-verification module.

## Evidence and limitations

Numerical verification supports the bounded analytic-entry claim. Scientific
validation, uncertainty quantification, and human acceptance are not evaluated.
Original local work under the repository license.
