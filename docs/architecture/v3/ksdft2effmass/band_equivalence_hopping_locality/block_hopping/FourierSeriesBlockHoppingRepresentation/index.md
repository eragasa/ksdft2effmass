# `FourierSeriesBlockHoppingRepresentation`

## Status and responsibility

Implemented request-bound representation operation in
`python/src/ksdft2effmass/band_equivalence_hopping_locality/block_hopping.py`.

The operation maps one finite Fourier matrix series into one immutable, unitless PhysKit
dense block-hopping representation. The request binds explicit provider identifier,
energy-reference identity, retained-basis identity, and the exact numerical series.

## Representation boundary

`result()`:

- closes dimension two or three onto the PhysKit lattice enum;
- copies every complex128 coefficient block;
- constructs an exact PhysKit integer lattice displacement for every integer mode;
- sorts terms lexicographically by displacement; and
- returns one `DenseBlockHoppingModel`.

The operation preserves coefficients. It does not symmetrize, truncate, align gauges,
infer a physical metric, or assign KSD scientific-model identity.

## Ownership exclusions

The result is provider representation data, not a complete
a dimensional rank-two model that combines `PeriodicBlockHoppingModel` with its
rank-two dimensional owner. Scientific-model admission remains a separate explicit
operation with exact geometry, role, rank, and Hermiticity requirements.

## Detailed documents

- [Numerics](numerics.md)
- [Schematic](schematics.md)
- [Scientific interpretation](scientifics.md)
