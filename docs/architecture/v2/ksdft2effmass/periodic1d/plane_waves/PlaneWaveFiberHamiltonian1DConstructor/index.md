# `PlaneWaveFiberHamiltonian1DConstructor`

**Defined in:** `ksdft2effmass.periodic1d.plane_waves`

## Role

Action that constructs one finite Galerkin matrix from an exact
`Periodic1DFiberHamiltonianRequest`, ordered `PlaneWaveBasis1D`, and explicit duality
tolerance. It reads the potential and recoil scale from the qualified parent rather
than accepting uncorrelated duplicates.

## Mathematics and ordering

Diagonal entries are `E_G (k+n)^2 + V_0`; positive and negative Fourier harmonics
populate conjugate matrix diagonals. Matrix index order is exactly
`basis.reciprocal_indices` and is never sorted or inferred.

## Evidence

`test__PlaneWaveFiberHamiltonian1DConstructor.py` checks a complex multiharmonic
analytic matrix, Hermiticity for the real synthetic potential, exact basis order, and
period/reciprocal-vector rejection. It does not establish discretization convergence.
