# `ReciprocalOperatorSamples1D`

## Purpose and status

This implemented row-026 DataObject retains homogeneous square matrices at ordered
one-dimensional reciprocal coordinates without assigning an operator role.

## Contract

The record requires a `VectorQuantity` coordinate sequence, positive compatible
`ScalarQuantity` reciprocal period, and a nonempty tuple containing one
`ComplexMatrixQuantity` per coordinate. Coordinates are canonicalized to the reciprocal
period unit. Every matrix is nonempty, square, equal in dimension, and equal in unit.

## Role boundary

Matrix rank, file origin, variable name, or downstream usage cannot identify parent,
projected, retained, or reconstructed meaning. `BandProjectedOperatorPathConstructor1D`
assigns input/output roles only for its operation. A
`Periodic1DRetainedOperatorReciprocalRepresentation` supplies exact retained-operator,
mesh, basis, gauge, energy-reference, map, provenance, and content identities when that
scientific claim is available.

## Evidence and limitations

`TestReciprocalOperatorSamples1D` checks intrinsic shape/unit behavior; projection and
Fourier tests check operation-specific roles. Composite adoption tests check explicit
retained interpretation and fail on ambiguous metadata. This software evidence does
not establish parent correctness, convergence, validation, UQ, or acceptance.
