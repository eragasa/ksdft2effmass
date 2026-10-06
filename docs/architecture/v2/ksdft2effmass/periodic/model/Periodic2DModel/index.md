# `Periodic2DModel`

## Purpose and status

`Periodic2DModel` is the implemented nominal branch for scientific models with exactly
two periodic spatial directions.

## Public contract

Supported import: `from ksdft2effmass.periodic import Periodic2DModel`.
It inherits the abstract `model_id` and `model_role` requirements and supplies a final
read-only `spatial_dimension` property returning the exact built-in integer `2`.

## Invariants and failure behavior

A subclass that defines `spatial_dimension` is rejected with `TypeError` during class
creation. The branch does not define a direct/reciprocal lattice pair, plane-wave or
finite-difference representation, gauge, energy reference, or topology.

## Dependencies and collaborators

`Periodic2DDefectModel` adds pristine-parent identity. Concrete models such as the
controlled cosine-potential toy belong to their `periodic2d` owner and remain separate
from their finite represented Hamiltonians and campaigns.

## Code, tests, and Sphinx

| Kind | Path or node | Evidence |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic/model.py:Periodic2DModel` | Exact nominal 2D branch |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_inheritance__dimensions__uses_nominal_branches` | Nominal membership separation |
| Test | `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py::TestPeriodicModel::test_property__spatial_dimension__returns_exact_built_in_identity` | Exact built-in dimension |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic/model.rst` | Supported API |

## Provenance, evidence, and limitations

Original local work under the repository license. Tests provide software verification
only. No numerical verification is applicable to nominal membership, and no scientific
validation, uncertainty quantification, or human acceptance is established. Nominal 2D
membership does not imply graphene identity or material realism.
