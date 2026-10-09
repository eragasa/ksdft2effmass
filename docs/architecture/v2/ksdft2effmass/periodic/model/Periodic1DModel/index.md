# `Periodic1DModel`

## Purpose and status

`Periodic1DModel` is the implemented nominal branch for scientific models with exactly
one periodic spatial direction.

## Public contract

Supported import: `from ksdft2effmass.periodic import Periodic1DModel`.
It inherits the abstract `model_id` and `model_role` requirements and supplies a final
read-only `spatial_dimension` property returning the exact built-in integer `1`.

## Invariants and failure behavior

A subclass that defines `spatial_dimension` is rejected with `TypeError` during class
creation. This prevents a concrete model from claiming 1D nominal membership while
reporting another dimension. The class owns no geometry, lattice convention, boundary
condition, operator, units, basis, or gauge.

## Dependencies and collaborators

`Periodic1DDefectModel` extends this branch with pristine-parent identity. Concrete 1D
models live under the applicable domain owner, such as `periodic1d`, and document their
complete physical and numerical conventions there.

## Code, tests, and Sphinx

| Kind | Path or node | Evidence |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic/model.py:Periodic1DModel` | Exact nominal 1D branch |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_property__spatial_dimension__returns_exact_built_in_identity` | Exact built-in dimension |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_class_definition__dimension_override__is_rejected` | Override rejection |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic/model.rst` | Supported API |

## Provenance, evidence, and limitations

Original local work under the repository license. Tests provide software verification
only. No numerical verification is applicable to nominal membership, and no scientific
validation, uncertainty quantification, or human acceptance is established. One
periodic direction does not by itself define the embedding dimension or a specific
Hamiltonian.
