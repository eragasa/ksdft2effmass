# `Periodic1DFittedHoppingEffectiveModelResult`

## Purpose and status

This implemented row-014 immutable ResultObject identifies an approximate finite-range
hopping model produced by an explicit weighted least-squares fit.

## Public contract

Supported import:
`from ksdft2effmass.periodic1d import Periodic1DFittedHoppingEffectiveModelResult`.

- `effective_model_id` is an exact nonempty identity.
- `retained_operator` is the exact operator being approximated.
- `fit` is a `BlockHoppingLeastSquaresFitResult1D` retaining source samples,
  representatives, weights, fitted coefficients, rank, conditioning, and training
  residuals.
- `model` returns exactly `fit.fitted_model`.

The fitted model dimension must equal retained-space rank.

## Scientific and numerical boundary

Weighted fitting estimates coefficients in a declared restricted model class and is not
a representation-only change. Training residuals and conditioning remain fit evidence;
they do not establish identifiability, withheld-domain accuracy, scientific validation,
or uncertainty quantification. The fitted route remains distinct from direct
truncation even when both produce the same coefficient range.

## Failure behavior

Wrong semantic types raise `TypeError`; empty identity or retained-rank mismatch raises
`ValueError`. The result does not select representatives, weights, or tolerances.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/hopping.py:Periodic1DFittedHoppingEffectiveModelResult` | Effective-model identity and fit binding |
| Test | `python/tests/software_verification/ksdft2effmass/periodic1d/test__hopping_construction_routes.py::TestPeriodic1DHoppingConstructionRoutes::test_artifact__weighted_fit__constructs_effective_model` | Separate route type and exact fitted model exposure |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/hopping.rst` | Route distinction and exclusions |

## Provenance and evidence

Original local work under the repository license. The synthetic test establishes
software classification only. Numerical verification of the least-squares algorithm
belongs to its Action owner. No approximation acceptance, scientific validation,
uncertainty quantification, or human acceptance is established.

## Limitations

The result does not merge fitting error with parent-model, discretization, interpolation,
or truncation errors and does not claim transfer outside the fit domain.
