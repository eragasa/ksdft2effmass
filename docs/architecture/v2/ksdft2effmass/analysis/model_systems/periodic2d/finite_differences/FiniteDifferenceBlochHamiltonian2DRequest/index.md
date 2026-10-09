# `FiniteDifferenceBlochHamiltonian2DRequest`

## Purpose and public contract

This implemented row-035 immutable Action request binds one complete finite-difference
representation definition to a reduced-momentum fiber. It is supported from
`ksdft2effmass.analysis.model_systems`.

The momentum is an exact pair of finite built-in floats in dimensionless reciprocal
coordinates dual to the square period. For direction `d`, the last-to-first positive
seam phase is `exp(+i*kappa_d*L)` and the reverse seam uses its conjugate.

## Invariants and failures

- The model has the exact reusable model type.
- Momentum is a length-two tuple of built-in floats; integers, booleans, lists, and
  numeric strings are not converted.
- Components are finite.
- Each product `kappa_d*L` must remain finite binary64; overflow raises
  `OverflowError` before phase evaluation.

Momentum is not inferred to be a Cartesian physical wave vector. The request selects
no eigensolver, retained space, convergence tolerance, validation threshold, or
acceptance decision.

## Code, Sphinx, and tests

| Surface | Mapping |
|---|---|
| Class | `python/src/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.py::FiniteDifferenceBlochHamiltonian2DRequest` |
| Sphinx | `doc/sphinx/api/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.rst` |
| Canonical test source | [`tests.py`](tests.py) |

| Pytest node | Evidence established |
|---|---|
| `TestFiniteDifferenceBlochHamiltonian2DRequestConstruction::test_construction_exposes_declared_conjugate_seam_phases` | Exact request correlation and phase convention |
| `...::test_construction_rejects_mistyped_or_nonfinite_momentum` | Strict tuple/component and finite-value boundary |
| `...::test_construction_rejects_binary64_seam_argument_overflow` | Fail-closed phase-argument representability |

`tests.py` is a relative symlink to the single runnable software-verification module.

## Evidence and limitations

Synthetic software tests establish request behavior only. They establish no physical
momentum adequacy, convergence, validation, UQ, or acceptance. Original local work
under the repository license.
