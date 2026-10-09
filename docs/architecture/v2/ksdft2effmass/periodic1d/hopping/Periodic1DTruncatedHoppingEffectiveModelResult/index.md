# `Periodic1DTruncatedHoppingEffectiveModelResult`

## Purpose and status

This implemented row-014 immutable ResultObject identifies an approximate finite-range
hopping model produced by explicit symmetric truncation of a complete coefficient
family.

## Public contract

Supported import:
`from ksdft2effmass.periodic1d import Periodic1DTruncatedHoppingEffectiveModelResult`.

- `effective_model_id` is an exact nonempty identity.
- `retained_operator` is the exact operator being approximated.
- `truncation` is a `BlockHoppingTruncationResult1D` retaining complete source
  coefficients, selected symmetric range, truncated coefficients, and omitted norm.
- `model` returns exactly `truncation.truncated`.

The truncated model dimension must equal retained-space rank.

## Scientific and numerical boundary

Truncation changes the model class by discarding coefficient blocks outside the declared
range. The result therefore represents an effective model rather than another exact
representation. The omitted norm is route evidence; this object does not decide whether
the approximation is acceptable on training or withheld observables.

## Failure behavior

Wrong semantic types raise `TypeError`; empty identity or retained-rank mismatch raises
`ValueError`. Construction does not infer a cutoff from coefficient magnitudes.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/hopping.py:Periodic1DTruncatedHoppingEffectiveModelResult` | Effective-model identity and route binding |
| Test | `python/tests/software_verification/ksdft2effmass/periodic1d/test__hopping_construction_routes.py::TestPeriodic1DHoppingConstructionRoutes::test_artifact__truncation__constructs_effective_model` | Separate identity and exact truncated model exposure |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/hopping.rst` | Route distinction and exclusions |

## Provenance and evidence

Original local work under the repository license. The synthetic test establishes
software classification only. Approximation accuracy, convergence, scientific
validation, uncertainty quantification, and human acceptance are not established.

## Limitations

The result is not a scientific acceptance decision and does not combine truncation error
with parent discretization or other model-reduction errors.
