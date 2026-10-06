# `Periodic3DModel`

## Purpose and status

`Periodic3DModel` is the implemented nominal branch for scientific models with exactly
three periodic spatial directions.

## Public contract

Supported import: `from ksdft2effmass.periodic import Periodic3DModel`.
It inherits the abstract `model_id` and `model_role` requirements and supplies a final
read-only `spatial_dimension` property returning the exact built-in integer `3`.

## Invariants and failure behavior

A subclass that defines `spatial_dimension` is rejected with `TypeError` during class
creation. The branch supplies no crystal structure, reciprocal cell, spin convention,
operator, basis, gauge, energy reference, or calculator settings.

## Dependencies and collaborators

`Periodic3DDefectModel` adds pristine-parent identity. Bulk-silicon and substitutional-
defect scientific definitions require their own specifications and concrete model
owners; this nominal branch does not create them.

## Code, tests, and Sphinx

| Kind | Path or node | Evidence |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic/model.py:Periodic3DModel` | Exact nominal 3D branch |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_inheritance__dimensions__uses_nominal_branches` | Nominal membership separation |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_property__spatial_dimension__returns_exact_built_in_identity` | Exact built-in dimension |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic/model.rst` | Supported API |

## Provenance, evidence, and limitations

Original local work under the repository license. Tests provide software verification
only. No numerical verification is applicable to nominal membership, and no scientific
validation, uncertainty quantification, or human acceptance is established. Nominal 3D
membership does not imply silicon identity or validate a materials calculation.
