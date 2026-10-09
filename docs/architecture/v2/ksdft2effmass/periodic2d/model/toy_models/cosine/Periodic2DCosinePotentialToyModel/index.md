# `Periodic2DCosinePotentialToyModel`

## Purpose and status

`Periodic2DCosinePotentialToyModel` is the implemented row-010 dimensionless spinless
scientific toy parent. It has nominal 2D membership and the stable family identity
`periodic2d.cosine-potential-toy`.

## Public contract

Defining import:
`ksdft2effmass.periodic2d.model.toy_models.Periodic2DCosinePotentialToyModel`.
The package-root route is also deliberately exported by `ksdft2effmass.periodic2d`.

Constructor fields `lambda_x`, `lambda_y`, and `lambda_xy` are exact finite built-in
floats multiplying `cos(x)`, `cos(y)`, and `cos(x)cos(y)`, respectively. The object
exposes exact `PeriodicModelRole.TOY`, dimension `2`, and PhysKit-owned immutable direct
and reciprocal lattices.

## Mathematics, state, and conventions

$$
V(x,y)=\lambda_x\cos x+\lambda_y\cos y+\lambda_{xy}\cos x\cos y,
\qquad A=2\pi I,\quad B=I.
$$

Coordinates, couplings, and energies are dimensionless under the model's reciprocal
kinetic scale. The configured coupling tuple identifies an instance while `model_id`
identifies the maintained family. No finite basis, gauge, or matrix is stored.

## Invariants and failure behavior

Boolean, integer, NumPy-scalar, and numeric-string substitutes are rejected with
`TypeError`; nonfinite built-in floats raise `ValueError`. A short `__post_init__`
delegates the coupling invariant. The lattice properties preserve the exact fixed cell
convention rather than accepting caller geometry.

## Scientific boundary

Nominal membership and successful construction do not establish material realism.
Plane-wave and finite-difference matrices are distinct represented operators produced
by separate requests and constructors.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic2d/model/toy_models/cosine.py:Periodic2DCosinePotentialToyModel` | Parent state and conventions |
| Test | `TestPeriodic2DCosinePotentialToyModel::test_init_retains_finite_dimensionless_couplings` | Couplings, identity, role, dimension |
| Test | `TestPeriodic2DCosinePotentialToyModel::test_lattices_form_the_two_pi_dual_square_cell` | Analytic direct/reciprocal convention |
| Test | `TestPeriodic2DCosinePotentialToyModel::test_init_rejects_boolean_and_nonfinite_couplings` | Strict scalar and finite-value boundary |
| Sphinx | `doc/sphinx/concepts/periodic2d-controlled-reduction.rst` | Scientist-facing model distinction |

The test nodes reside in
`python/tests/ksdft2effmass/periodic2d/model/toy_models/test__Periodic2DCosinePotentialToyModel.py`.

## Provenance and evidence

Original local work under the repository license. Exact authored inputs and analytic
lattice arrays support software verification. No discretization convergence, material
validation, uncertainty quantification, or acceptance is established.

## Limitations

The class supplies no spin, orbital, material, pseudopotential, or calculator model. It
is a controlled mathematical parent only.
