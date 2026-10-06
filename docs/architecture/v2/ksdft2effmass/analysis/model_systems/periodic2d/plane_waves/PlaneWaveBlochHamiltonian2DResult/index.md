# `PlaneWaveBlochHamiltonian2DResult`

## Purpose and status

This implemented row-033 ResultObject retains one general two-dimensional continuum
plane-wave represented operator, its complete construction request, and checked
lattice-duality residual.

## Contract

The energy-valued `ComplexMatrixQuantity` is square in the request's exact `p`-outer,
`q`-inner basis dimension and uses the representation definition's kinetic energy unit.
The finite nonnegative residual cannot exceed the request tolerance. The nested request
preserves PhysKit direct/reciprocal geometry, reduced momentum, cutoff, ordering,
state-space/basis/energy identities, spin convention, Fourier inventory, and tolerance.

## Scientific boundary and evidence

This is finite represented-space output—not a nominal scientific model, retained
operator, eigensystem, or campaign acceptance result. Parent-model, discretization, and
later reduction errors remain separate. Result tests check shape, units, and fail-closed
residual correlation; constructor numerical tests use analytic lattice/Fourier cases.
Passing does not establish continuum convergence or material validation.
