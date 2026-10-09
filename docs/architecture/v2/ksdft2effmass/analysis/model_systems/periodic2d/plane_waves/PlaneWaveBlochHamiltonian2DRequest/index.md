# `PlaneWaveBlochHamiltonian2DRequest`

## Purpose and status

This implemented row-033 immutable Action request binds one complete finite plane-wave
representation definition to a reduced-momentum fiber and caller-owned lattice-duality
tolerance.

Reduced momentum is an exact finite pair of built-in floats in reciprocal primitive
coordinates, not Cartesian wave-vector components. The tolerance is a finite
nonnegative built-in float applied to the maximum component of `A^T B - 2*pi*I`.
Booleans, integers, numeric strings, nonfinite values, and semantic substitutes are not
silently converted.

The request chooses no eigensolver, retained bands, gauge, convergence criterion,
scientific validation threshold, or acceptance decision.
