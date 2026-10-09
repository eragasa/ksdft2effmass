# `Periodic1DFiniteHoppingToyModel`

## Purpose and status

`Periodic1DFiniteHoppingToyModel` is the implemented row-011 scientific toy parent. It
combines an explicit configured identity, ordered finite directed hopping blocks, an
energy-unit identity, and an absolute Hermiticity tolerance under nominal 1D membership.

## Public contract

Supported import:
`from ksdft2effmass.periodic1d import Periodic1DFiniteHoppingToyModel`.

```text
Periodic1DFiniteHoppingToyModel(
    model_id,
    blocks,
    energy_unit,
    hermiticity_tolerance,
)
```

The model exposes exact `model_id`, `PeriodicModelRole.TOY`, dimension `1`, ordered
`blocks`, `energy_unit`, `hermiticity_tolerance`, and common `orbital_count`.

## State, ordering, and mathematical contract

For every stored displacement `R`, the tuple contains `-R` and satisfies

$$
H_R = H_{-R}^{\dagger}
$$

using zero relative tolerance and the configured inclusive absolute tolerance. Tuple
order is increasing cell displacement, displacements are unique and contiguous, and
zero is present. All matrices have the same nonzero square orbital dimension.

## Failure behavior

Wrong semantic scalar, tuple, block, or unit types raise `TypeError`. Empty identity or
unit, nonpositive/nonfinite tolerance, invalid displacement coverage, inconsistent
orbital dimensions, or failed pairwise Hermiticity raise `ValueError`. Validation order
is retained through cohesive `_check_args_*` methods called by a short `__post_init__`.

## Scientific boundary

The object identifies a controlled parent model, not a material Hamiltonian, a Bloch
fiber matrix, a retained operator, or an effective model. Its blocks are complete for
the configured finite-range toy family. Later truncation or fitting routes produce
separately identified effective-model results.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/hopping.py:Periodic1DFiniteHoppingToyModel` | Configured nominal parent and invariant checks |
| Test | `TestPeriodic1DFiniteHoppingToyModel::test_construction__identity__has_nominal_dimension_and_toy_role` | Identity, role, dimension, catalog membership |
| Test | `TestPeriodic1DFiniteHoppingToyModel::test_construction__blocks__owns_ordered_nonwriteable_complex_matrices` | Ordered immutable block storage |
| Test | `TestPeriodic1DFiniteHoppingToyModel::test_construction__model_id__rejects_empty_identity` | Identity failure |
| Test | `TestPeriodic1DFiniteHoppingToyModel::test_construction__hermiticity__rejects_unpaired_hopping` | Pairwise Hermiticity failure |
| Test | `TestPeriodic1DFiniteHoppingToyModel::test_public_api__campaign_route__does_not_export_migrated_model` | Canonical owner and retired aliases |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/hopping.rst` | Public model equation and exclusions |

The tests use authored synthetic dimensionless matrices and establish software
verification only.

## Provenance and evidence

Original local work under the repository license. Numerical verification of downstream
fiber constructors is separate. No material adequacy, scientific validation,
uncertainty quantification, or human acceptance is established.

## Limitations

`energy_unit` is an exact identity string and is not converted. The Hermiticity
tolerance is software input policy, not uncertainty or a scientific acceptance
threshold.
