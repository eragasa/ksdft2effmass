# `Periodic3DRank2BlockHoppingModel`

## Status and responsibility

Implemented frozen, slotted scientific-model value in
`python/src/ksdft2effmass/periodic/periodic3d/rank2/models/block_hopping.py`.

The class directly inherits `PeriodicRank2BlockHoppingModel`. It completes the shared
contract with exact three-dimensional geometry, identity, role, and one composed PhysKit
dense or sparse block-hopping representation.

## Construction boundary

Construction requires:

- a nonempty built-in string identity;
- one exact `PeriodicModelRole`;
- an immutable `Periodic3DLatticeGeometry` containing the ordered primitive-basis
  matrix and an explicit physical length unit;
- provider dimension three;
- exact `2 x 2` coefficient blocks; and
- complete exactly Hermitian ordinary-lattice support.

The model reconstructs `DirectLattice3D` and derives `DirectLatticeMetric` from the
geometry. The metric is therefore a derived intrinsic value, not a replacement for the
ordered coordinate map or its unit convention.

The public value is operationally immutable. It contains no mesh, tolerance, gauge
analysis, truncation policy, campaign, persistence, or execution identity.

## Locality integration

`Periodic3DRank2HoppingLocalityAnalysisRequest` accepts this exact model rather than a
bare Fourier series. Shell labels remain explicit positional metadata over immutable
provider term order. The installed raw-power route currently requires dense storage and
does not densify sparse models implicitly.

## Detailed documents

- [Numerics](numerics.md)
- [Schematic](schematics.md)
- [Scientific interpretation](scientifics.md)
