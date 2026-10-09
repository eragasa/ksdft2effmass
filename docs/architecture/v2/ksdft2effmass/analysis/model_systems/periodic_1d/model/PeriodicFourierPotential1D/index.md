# `PeriodicFourierPotential1D`

## Purpose and status

`PeriodicFourierPotential1D` is the implemented row-017 reusable finite real Fourier
potential component. It becomes part of a complete scientific parent only through
explicit composition with a kinetic law and parent identities.

## Public contract

Supported import:
`from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D`.

Fields are a positive `period`, one `constant_coefficient`, and paired
`cosine_coefficients`/`sine_coefficients`. `harmonic_count` reports the paired inventory
length. `evaluate` returns energies at compatible coordinates.
`reciprocal_period_in` returns `2*pi/a` in an explicitly requested positive reciprocal
unit convention.

## Invariants, units, and failure behavior

Period and coefficients use exact scalar/vector quantity types. Cosine and sine
inventories have equal shape, including explicit zeros for absent channels. Every
coefficient unit is compatible with the constant term and is canonicalized to that
unit. Physical periods require physical inverse-length reciprocal units; unitless
periods require unitless reciprocal targets.

Wrong semantic types raise `TypeError`; nonpositive period/target, unequal inventories,
or incompatible units raise `ValueError`. The short `__post_init__` delegates type,
inventory, and unit checks before canonicalization.

## Scientific boundary

The object is a potential component, not a complete Hamiltonian, finite representation,
retained operator, or effective model. Its finite harmonic inventory is exact for this
component record but does not prove physical completeness.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/analysis/model_systems/periodic_1d/model.py:PeriodicFourierPotential1D` | Component state, unit canonicalization, evaluation |
| Test | `TestPeriodicFourierPotential1D::test_constructor__fourier_series__normalizes_and_evaluates` | Unit normalization and analytic series values |
| Test | `TestPeriodicFourierPotential1D::test_constructor__fourier_series__computes_reciprocal_period_in_requested_unit` | Analytic dimensionless reciprocal period |
| Test | `TestPeriodicFourierPotential1D::test_constructor__fourier_series__rejects_unequal_inventories` | Explicit paired harmonic inventory |
| Sphinx | `doc/sphinx/api/model-systems.rst` | Supported public API |

## Provenance and evidence

Original local work under the repository license. The mapped tests use authored analytic
values. They establish software and bounded numerical behavior, not material adequacy,
scientific validation, uncertainty quantification, or acceptance.

## Limitations

No infinite Fourier-series truncation error or coefficient uncertainty is represented.
