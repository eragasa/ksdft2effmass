# `ksdft2effmass.periodic.periodic2d.models`

## Ownership

This package owns periodic-2D scientific models and their cohesive represented-operator
construction. `Periodic2DModel` fixes `spatial_dimension == 2`;
`Periodic2DDefectModel` additionally requires a stable pristine parent identity. A
model's evidentiary role is the `PeriodicModelRole` value returned by `model_role`, not a
`control_models` namespace or a `ControlModel` class-name suffix.

`Periodic2DCosinePotentialModel` is a `Periodic2DModel` with an explicitly supplied
`PeriodicModelRole`; the class does not infer control, material-reference, or reduced
status. Its plane-wave and finite-difference operations build finite representations
without becoming separate scientific models.

The reusable plane-wave Bloch model, Fourier coefficients, reciprocal meshes, and
finite-cutoff sewing mechanics are also owned here. PhysKit retains primitive lattice,
quantity, and generic numerical ownership.

## Representation flow

```text
Periodic2DCosinePotentialModel + representation request
  -> Periodic2DPlaneWaveHamiltonian or Periodic2DFiniteDifferenceHamiltonian
  -> immutable represented matrix result
```

The represented-Hamiltonian operations retain exact requests and represented matrices.
They do not select campaign meshes, convergence criteria, comparison policy, or
scientific acceptance.

## Navigation

- [`Periodic2DPlaneWaveBlochHamiltonianModel`](Periodic2DPlaneWaveBlochHamiltonianModel/index.md)
- [`Periodic2DPlaneWaveBasis`](Periodic2DPlaneWaveBasis/index.md)
- [`Periodic2DPlaneWaveHamiltonian`](Periodic2DPlaneWaveHamiltonian/index.md)
- [`Periodic2DFiniteDifferenceHamiltonian`](Periodic2DFiniteDifferenceHamiltonian/index.md)
- [Periodic-2D basis identity](../../operators/basis/index.md)
