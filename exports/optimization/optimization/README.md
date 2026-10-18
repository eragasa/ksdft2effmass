# Affine quadratic and diagonal metric candidate

## Status and destination

This directory records the contracts for active non-runtime source candidates staged at
`exports/optimization/affine.py` and `exports/optimization/metric.py`. They were prepared
against exact clean Optimization owner commit
`ec3d2907097a659aef4be2b3384bd1922a9cb4dc` and KSD donor base
`08a3211f0748bdbb1d45bfc12f2ca8f8205007d3`.

The flattened source files map to:

| Export file | Intended owner path |
|---|---|
| `../affine.py` | `src/python/projectkoios/optimization/affine.py` |
| `../metric.py` | `src/python/projectkoios/optimization/metric.py` |

Mapped tests are staged under `exports/optimization/tests/`. Exact relative-source,
destination, and SHA-256 mappings are recorded in [`transfer.toml`](transfer.toml).
The owner repository remains authoritative for final naming, public imports,
integration, review, versioning, and release.

## Weighted affine residuals

`WeightedAffineResidualTerm` represents one unit-free residual
`coefficients @ x - target` with a strictly positive weight.
`WeightedAffineResidualDefinition` owns unique ordered coordinate names and a nonempty
common-dimensional term tuple. Its direct `squared_loss()` uses deterministic scalar
summation and scaled fallback products to avoid premature underflow or overflow when the
weighted result is representable; nonfinite results fail closed.

`WeightedAffineResidualQuadraticConstructor.execute()` forms the exactly symmetric
normal matrix, solves for the represented center with NumPy, evaluates the minimum from
the original residual definition, and delegates final positive-definiteness acceptance,
storage, and evaluation to the existing
`projectkoios.optimization.adapters.PositiveDefiniteQuadraticLoss`. `sparse=True`
selects its existing SciPy backend. Rank-deficient systems fail rather than being
silently regularized.

Weights are used exactly as supplied. Mean-square normalization, units, sample meaning,
and scientific policy remain caller-owned.

## Positive diagonal metric

`PositiveDiagonalMetric` owns unique ordered coordinate names and finite strictly
positive unit-free diagonal entries. It evaluates squared distance, distance, squared
dual norm, and dual norm using checked, scale-aware scalar arithmetic. It accepts the
zero covector;
a scientific caller that requires a nonzero separating direction must impose that
policy outside the generic metric.

Physical callers must nondimensionalize coordinates and metric entries before crossing
this boundary.

## Candidate validation

In a disposable overlay of the exact owner base, 16 focused candidate tests and all 111
overlay tests pass. Ruff check/format, strict mypy over all 29 owner-plus-candidate source
files, sdist/wheel builds, wheel-content inspection, and installed-wheel imports pass.
These are software checks of staged bytes, not owner acceptance or scientific
validation.

## Exclusions

The candidate does not implement box-constrained quadratic minimization, nonemptiness or
infeasibility certificates, common-witness search, support optimization, set distance,
directed rounding, interval arithmetic, HSH thresholds, certificate interpretation, or
scientific dispositions. Existing exploratory optimizers remain non-certifying.
