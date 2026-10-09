# `Periodic1DDefectModel`

## Purpose and status

`Periodic1DDefectModel` is the implemented nominal branch for a one-dimensional defect
model with an explicit pristine-parent identity.

## Public contract

Supported import: `from ksdft2effmass.periodic import Periodic1DDefectModel`.
The abstract `parent_model_id: str` property supplements the inherited model identity,
role, and exact dimension `1`.

## Scientific boundary and invariants

Parent identity states which pristine model the defect claims to modify. It does not
establish common state space, basis, gauge, geometry, normalization, or energy reference
between parent and defect operators. A concrete owner validates that its parent identity
is nonempty and supplies the defect definition and compatibility prerequisites.

The class remains abstract until `model_id`, `model_role`, and `parent_model_id` are
implemented. It stores no perturbation or represented matrix.

## Code, tests, and Sphinx

| Kind | Path or node | Evidence |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic/model.py:Periodic1DDefectModel` | Nominal 1D defect category |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_inheritance__defect_models__remain_dimension_specific` | Defect/dimension inheritance |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic/model.rst` | Public parent-identity boundary |

## Dependencies, provenance, and evidence

The class depends only on `Periodic1DModel`. Campaign-specific defect construction and
operator subtraction remain outside this owner. Original local work under the repository
license. The mapped test is software verification; numerical verification is not
applicable and no scientific validation, uncertainty quantification, or acceptance is
established.

## Limitations

No complete nominal 1D Gaussian defect is supplied by this abstract branch; the current
Gaussian onsite record remains a perturbation definition until composed with an
identified compatible parent.
