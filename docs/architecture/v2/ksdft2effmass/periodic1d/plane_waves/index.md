# `ksdft2effmass.periodic1d.plane_waves`

## Responsibility

Own the finite plane-wave representation of a parent-qualified periodic-1D Fourier
Hamiltonian. Reciprocal-index order is preserved exactly; the represented matrix is not
conflated with the untruncated parent operator.

## Public classes

- [`PlaneWaveFiberHamiltonian1DConstructor`](PlaneWaveFiberHamiltonian1DConstructor/index.md)
- [`PlaneWaveFiberHamiltonian1DResult`](PlaneWaveFiberHamiltonian1DResult/index.md)

## Numerical boundary

For basis dimension `N` and `M` potential harmonics, construction uses dense
`O(N^2)` storage and `O(N^2 + N min(M,N))` time. No arbitrary cap is imposed.
Binary64/complex128 overflow fails closed. Software evidence checks transfer and
ordering but does not establish basis convergence or physical adequacy.
