# `Periodic1DOrthogonalSpectralRetainedSubspace`

## Purpose and status

This implemented row-021 DataObject binds one parent-qualified one-dimensional
mathematical retained space to immutable eigenvalues and an orthonormal column
embedding.

## Public contract and invariants

Supported import:
`from ksdft2effmass.periodic1d import Periodic1DOrthogonalSpectralRetainedSubspace`.
The two fields require exact `PeriodicRetainedSubspace` and
`OrthogonalSpectralSubspace` types. Parent dimensionality must be one; scientific rank
and ambient dimension must equal the numerical retained and full dimensions.

## Scientific boundary

The numerical embedding represents but does not define the mathematical retained
space. Matching dimensions are necessary, not proof of parent alignment. Gauge/basis
coordinates, represented operators, projection error, and parent-model error remain
separate.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/retention.py:Periodic1DOrthogonalSpectralRetainedSubspace` | Mathematical/numerical space binding |
| Test | `TestPeriodic1DOrthogonalSpectralRetainedSubspace::test_construction__dimensions__binds_matching_scientific_and_numerical_spaces` | Exact retained and ambient dimension correlation |
| Test | `TestPeriodic1DOrthogonalSpectralRetainedSubspace::test_construction__ambient_dimension__rejects_mismatch` | Fail-closed incompatible embedding |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/retention.rst` | Public API and representation boundary |

## Provenance and limitations

Original local work under the repository license. Synthetic tests establish software
correlation only. They do not establish source authenticity, parent alignment,
eigensolver convergence, physical adequacy, scientific validation, uncertainty, or
acceptance.
