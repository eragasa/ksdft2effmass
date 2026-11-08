# `ksdft2effmass.periodic.periodic3d.rank2.models`

Implemented periodic-3D rank-two model ownership.

`Periodic3DRank2Model` refines `Periodic3DRankNModel` and fixes
`band_subspace_rank == 2`. It retains the inherited requirement for an explicit
`Periodic3DBasisIdentity` containing exactly two ordered coordinates.

`Periodic3DRank2BlockHoppingModel` combines `Periodic3DRank2Model` with
`PeriodicBlockHoppingModel`. It binds exact ordered unit-bearing three-dimensional
lattice geometry, the structured rank-two basis, and a PhysKit dense or sparse
block-hopping representation with exact `2 x 2` blocks and conjugate-displacement
support. The direct metric is derived from complete geometry rather than substituted for
it.

Source owners:

- `python/src/ksdft2effmass/periodic/periodic3d/rank2/models/base.py`
- `python/src/ksdft2effmass/periodic/periodic3d/rank2/models/block_hopping.py`

Detailed architecture:

- [`Periodic3DRank2BlockHoppingModel`](Periodic3DRank2BlockHoppingModel/index.md)
- [Dimension-neutral block-hopping capability](../../../models/PeriodicBlockHoppingModel/index.md)
