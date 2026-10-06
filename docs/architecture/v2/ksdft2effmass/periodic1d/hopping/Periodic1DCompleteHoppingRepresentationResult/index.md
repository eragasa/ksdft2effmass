# `Periodic1DCompleteHoppingRepresentationResult`

## Purpose and status

This implemented row-014 immutable ResultObject binds a complete centered finite-mesh
Fourier transform to one exact identified retained operator. It classifies the output as
an operator representation, not an effective model.

## Public contract

Supported import:
`from ksdft2effmass.periodic1d import Periodic1DCompleteHoppingRepresentationResult`.

- `retained_operator` is an exact `PeriodicRetainedOperator`.
- `transform` is an exact `ReciprocalOperatorFourierTransformResult1D` containing all
  mesh representatives and reconstruction diagnostics.

The transform's hopping matrix dimension must equal retained-space rank.

## Scientific and numerical boundary

On a complete centered Born--von Karman mesh, the transform changes representation while
retaining all finite-mesh information. It does not truncate displacement blocks, fit a
restricted model class, or assert that reconstruction diagnostics satisfy scientific
acceptance criteria. Exactness is relative to the identified finite sampled parent.

## Failure behavior

Wrong exact field types raise `TypeError`; rank mismatch raises `ValueError`. The class
uses identity-preserving composition and does not copy or reinterpret the retained
operator or transform.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/hopping.py:Periodic1DCompleteHoppingRepresentationResult` | Exact route binding and rank check |
| Test | `python/tests/software_verification/ksdft2effmass/periodic1d/test__hopping_construction_routes.py::TestPeriodic1DHoppingConstructionRoutes::test_artifact__complete_transform__is_operator_representation` | Exact operator/transform identity and type distinction |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/hopping.rst` | Complete representation versus effective model |

## Provenance and evidence

Original local work under the repository license. The synthetic rank-one test is
software verification. Transform numerical verification belongs to the transform owner.
No infinite-system convergence, scientific validation, uncertainty quantification, or
acceptance is established.

## Limitations

The result stores no new gauge, basis, or provenance metadata beyond its two composed
owners; a separate represented retained-operator binding supplies those meanings where
required.
