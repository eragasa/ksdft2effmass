# `ksdft2effmass.periodic1d.finite_differences`

## Responsibility

Own the ordered half-open periodic grid and sparse second-order finite-difference
representation of a parent-qualified periodic-1D Fourier Hamiltonian.

## Public classes

- [`PeriodicUniformGrid1D`](PeriodicUniformGrid1D/index.md)
- [`PeriodicFiniteDifferenceFiberHamiltonian1DConstructor`](PeriodicFiniteDifferenceFiberHamiltonian1DConstructor/index.md)
- [`PeriodicFiniteDifferenceFiberHamiltonian1DResult`](PeriodicFiniteDifferenceFiberHamiltonian1DResult/index.md)

## Numerical boundary

For `N` grid points and `M` Fourier harmonics, construction uses `O(N)` sparse storage
and `O(NM)` sampling time. The half-open order and conjugate Bloch seam are semantic
representation conventions. Passing software checks does not establish mesh
convergence or scientific validation.
