# `Periodic3DRank2BlockHoppingModel`

## Status and responsibility

Implemented frozen, slotted scientific-model value in
`python/src/ksdft2effmass/periodic/periodic3d/rank2/models/block_hopping.py`.

The class combines `Periodic3DRank2Model` and `PeriodicBlockHoppingModel`.
`Periodic3DRank2Model` refines the three-dimensional finite-rank owner to exact retained
rank two; `PeriodicBlockHoppingModel` contributes dimension-neutral represented-operator
behavior and admissibility. The concrete class correlates those contracts with exact
three-dimensional geometry, structured basis identity, model identity, role, and one
composed PhysKit dense or sparse representation.

## Construction boundary

Construction requires:

- a nonempty built-in string identity;
- one exact `PeriodicModelRole`;
- an immutable `Periodic3DLatticeGeometry` containing the ordered primitive-basis
  matrix and an explicit physical length unit;
- one exact `Periodic3DBasisIdentity` with two ordered coordinates;
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
