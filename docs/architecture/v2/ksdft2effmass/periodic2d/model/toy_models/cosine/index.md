# `periodic2d.model.toy_models.cosine`

## Purpose and status

This implemented module owns the dimensionless cosine scientific parent and two finite
representation routes used by controlled periodic2d studies.

## Public contract inventory

| Symbol family | Category | Responsibility |
|---|---|---|
| `Periodic2DCosinePotentialToyModel` | Scientific model | Period-`2*pi` spinless dimensionless cosine parent |
| `Periodic2DPlaneWaveBasis`, `Periodic2DUniformCellGrid` | Representation definitions | Ordered reciprocal and coordinate bases |
| Plane-wave request/result/constructor | Represented-operator route | Delegated finite continuum plane-wave construction |
| Finite-difference request/result/constructor | Represented-operator route | Centered finite-difference construction with Bloch seams |
| `Periodic2DHamiltonianResult` | Supporting result base | Immutable square exactly Hermitian matrix storage |

Row 010 owns the scientific parent. Rows 034 and 035 separately own migration of the
represented routes.

## Scientific model equation and conventions

The parent potential is

$$
V(x,y)=\lambda_x\cos x+\lambda_y\cos y+\lambda_{xy}\cos x\cos y
$$

on the dimensionless square cell with direct lattice `A = 2*pi*I` and reciprocal
lattice `B = I`, satisfying `A^T B = 2*pi*I`. Couplings are exact finite built-in
floats. Energies use the reciprocal kinetic scale and the model's fixed energy zero.

Finite plane-wave and finite-difference matrices are not the parent itself. Their
basis/grid ordering, reduced momentum, seams, units, and provenance belong to their
requests and results.

## Class navigation

- [`Periodic2DCosinePotentialToyModel`](Periodic2DCosinePotentialToyModel/index.md)
- [`Periodic2DPlaneWaveHamiltonianRequest`](Periodic2DPlaneWaveHamiltonianRequest/index.md)
- [`Periodic2DPlaneWaveHamiltonianResult`](Periodic2DPlaneWaveHamiltonianResult/index.md)
- [`Periodic2DPlaneWaveHamiltonianConstructor`](Periodic2DPlaneWaveHamiltonianConstructor/index.md)
- [`Periodic2DFiniteDifferenceHamiltonianRequest`](Periodic2DFiniteDifferenceHamiltonianRequest/index.md)
- [`Periodic2DFiniteDifferenceHamiltonianResult`](Periodic2DFiniteDifferenceHamiltonianResult/index.md)
- [`Periodic2DFiniteDifferenceHamiltonianConstructor`](Periodic2DFiniteDifferenceHamiltonianConstructor/index.md)

Rows 034 and 035 are reconciled adapter routes. Each preserves its exact campaign
request while delegating matrix assembly to a reusable represented-operator Action.
The finite-difference adapter explicitly supplies Euclidean coordinate-basis,
dimensionless energy, model-zero, source/operator/state-space, and provenance metadata
without changing grid order or Bloch-seam direction.

## Code, tests, and Sphinx

| Kind | Path or node | Responsibility |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic2d/model/toy_models/cosine.py` | Parent and finite routes |
| Test | `python/tests/ksdft2effmass/periodic2d/model/toy_models/test__Periodic2DCosinePotentialToyModel.py::TestPeriodic2DCosinePotentialToyModel` | Couplings, identity, role, lattice, strict scalar boundary |
| Sphinx | `doc/sphinx/concepts/periodic2d-controlled-reduction.rst` | Model/representation distinction |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` | Current public classes |

## Provenance and evidence

Original local work under the repository license. Analytic lattice identities and
constructor tests establish software or bounded numerical behavior as individually
marked. They do not establish material adequacy, continuum convergence, scientific
validation, uncertainty quantification, or acceptance.

## Limitations

The model is dimensionless and spinless. It is not graphene or another material-
reference model. The reusable finite-difference route remains intentionally bounded to
a square dimensionless cell and centered second-order stencil; completing row 035 does
not establish continuum convergence or material adequacy.
