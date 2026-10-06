# `Periodic2DDefectModel`

## Purpose and status

`Periodic2DDefectModel` is the implemented nominal branch for a two-dimensional defect
model with an explicit pristine-parent identity.

## Public contract

Supported import: `from ksdft2effmass.periodic import Periodic2DDefectModel`.
The abstract `parent_model_id: str` property supplements the inherited model identity,
role, and exact dimension `2`.

## Scientific boundary and invariants

Parent identity does not establish that parent and defect operators share a state
space, basis, gauge, geometry, normalization, or energy reference. Concrete owners must
document and enforce those prerequisites before extraction, subtraction, or comparison.
The class stores no hopping inventory, perturbation, represented operator, or campaign
policy.

The class remains abstract until all inherited identity properties and
`parent_model_id` are implemented.

## Code, tests, and Sphinx

| Kind | Path or node | Evidence |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic/model.py:Periodic2DDefectModel` | Nominal 2D defect category |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_inheritance__defect_models__remain_dimension_specific` | Defect/dimension inheritance |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic/model.rst` | Public parent-identity boundary |

## Dependencies, provenance, and evidence

The class depends only on `Periodic2DModel`. The concrete scalar-hopping defect has its
own `periodic2d` owner and does not redefine this base. Original local work under the
repository license. The mapped test is software verification; numerical verification is
not applicable and no scientific validation, uncertainty quantification, or acceptance
is established.

## Limitations

Nominal membership does not establish graphene identity, topological meaning, or
material realism.
