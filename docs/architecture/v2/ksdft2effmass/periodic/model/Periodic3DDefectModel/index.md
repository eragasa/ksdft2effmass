# `Periodic3DDefectModel`

## Purpose and status

`Periodic3DDefectModel` is the implemented nominal branch for a three-dimensional defect
model with an explicit pristine-parent identity.

## Public contract

Supported import: `from ksdft2effmass.periodic import Periodic3DDefectModel`.
The abstract `parent_model_id: str` property supplements the inherited model identity,
role, and exact dimension `3`.

## Scientific boundary and invariants

Parent identity alone does not establish aligned state spaces, bases, gauges,
normalization, geometry, spin convention, or energy reference. A concrete defect model
must own and validate those meanings before any parent/defect operator difference is
constructed. The abstract branch stores no defect species, crystal site, perturbation,
or represented operator.

The class remains abstract until all model and parent identity properties are
implemented.

## Code, tests, and Sphinx

| Kind | Path or node | Evidence |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic/model.py:Periodic3DDefectModel` | Nominal 3D defect category |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_inheritance__defect_models__remain_dimension_specific` | Defect/dimension inheritance and synthetic parent identity |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic/model.rst` | Public parent-identity boundary |

## Dependencies, provenance, and evidence

The class depends only on `Periodic3DModel`. Original local work under the repository
license. The synthetic mapped test provides software verification only; numerical
verification is not applicable and no scientific validation, uncertainty quantification,
or acceptance is established.

## Limitations

The branch does not implement silicon, phosphorus, boron, spin-orbit policy, or any
production electronic-structure calculation.
