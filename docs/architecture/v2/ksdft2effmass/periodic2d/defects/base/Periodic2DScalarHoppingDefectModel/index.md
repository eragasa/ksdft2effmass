# `Periodic2DScalarHoppingDefectModel`

## Purpose and status

`Periodic2DScalarHoppingDefectModel` is the implemented row-012 controlled defect
scientific model. It composes one translation-invariant 2D scalar hopping parent with
one finite ordered localized perturbation while preserving their separate identities.

## Public contract

Supported import:
`from ksdft2effmass.periodic2d import Periodic2DScalarHoppingDefectModel`.

Constructor fields are:

- `identifier: str` — exact nonempty configured defect identity;
- `bulk: ScalarHoppingModel` — pristine translation-invariant parent; and
- `perturbation: LocalizedPerturbation` — finite ordered onsite and/or directed-bond
  changes.

The model exposes `model_id == identifier`, `parent_model_id == bulk.identifier`, exact
role `PeriodicModelRole.TOY`, nominal dimension `2`, and
`represents_onsite_potential` when every perturbation term is exactly onsite.

## Scientific state and conventions

The scientific composition distinguishes `H_0`, `Delta H`, and their later finite
represented sum. The model itself stores no finite shape, twist, matrix, or compatibility
finding. Both components must declare `LatticeDimension.TWO`. Unit, basis, geometry,
and energy-reference compatibility is enforced only when a representation is requested.

An onsite-only perturbation can be described as a scalar potential in the declared
lattice basis. A bond term changes off-diagonal hopping and remains a general operator
perturbation rather than being relabeled as a potential.

## Invariants and failure behavior

Wrong identity or component types raise `TypeError`; empty identity or non-2D components
raise `ValueError`. A short `__post_init__` delegates identity, exact component type, and
dimension invariant families. No material-reference role can be supplied by callers.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic2d/defects/base.py:Periodic2DScalarHoppingDefectModel` | Scientific composition and nominal identity |
| Test | `TestPeriodic2DDefect::test_model__has_explicit_nominal_identity_parent_and_role` | Configured/pristine identities, role, dimension, retired name |
| Test | `TestPeriodic2DDefect::test_property__represents_onsite_potential__distinguishes_bond_change` | Potential/operator distinction |
| Test | `TestPeriodic2DDefect::test_method__represent__adds_finite_onsite_potential_to_bulk` | Separate compatible finite representation and sum |
| Sphinx | `doc/sphinx/concepts/periodic2d-finite-extent-defects.rst` | Equations, representation flow, locality, and exclusions |

The tests use authored synthetic scalar hopping and localized perturbations under
`python/tests/software_verification/ksdft2effmass/periodic2d/defects/`.

## Dependencies, provenance, and evidence

The model composes `solid_state.ScalarHoppingModel` and `LocalizedPerturbation` and
inherits the nominal general 2D defect branch. Original local work under the repository
license. Tests establish software behavior only; represented compatibility is separate
evidence. No material validation, convergence, uncertainty quantification, or
acceptance is established.

## Limitations

The model is scalar and controlled. It supplies no electronic-structure provenance,
spinor structure, fitted impurity parameters, or authenticated material parent.
