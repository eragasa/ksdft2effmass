# `Periodic2DPlaneWaveHamiltonianConstructor`

## Purpose and status

This implemented row-034 Action adapts the cosine toy model and exact adapter request to
the reusable `PlaneWaveBlochHamiltonian2DConstructor`.

## Delegation route

The Action maps the three cosine couplings to the eight nonzero Fourier transfers with
the exact transfer signs and factors, composes the PhysKit lattices, cutoff, unitless
kinetic scale, and explicit represented identities, and delegates general matrix
assembly. It then returns the original adapter request, represented matrix, and duality
residual. No second plane-wave assembly algorithm is maintained.

The separable zero-mixed-coupling test uses an analytic Kronecker-sum oracle, checks
Hermiticity and immutable storage, and compares with an explicit absolute numerical
tolerance. Result tests cover contradictory dimensions and residuals. These establish
bounded software/numerical behavior only—not continuum convergence or scientific
validation.
