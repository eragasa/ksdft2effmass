# `Periodic2DPlaneWaveHamiltonianRequest`

## Purpose and status

This implemented row-034 adapter request binds the cosine toy parent, reduced reciprocal
momentum, symmetric integer cutoff, and duality tolerance for one finite plane-wave
fiber.

The request exposes the exact `Periodic2DPlaneWaveBasis`, represented dimension, and
`p`-outer, `q`-inner ordering. Momentum components and tolerance are finite built-in
floats; cutoff is validated by the finite-basis definition. The default tolerance covers
binary64 reconstruction of the fixed square lattice and is not a scientific acceptance
threshold.

The request contains no retained-space selection, gauge, eigensolver, convergence, or
acceptance policy.
