# `ksdft2effmass.periodic.periodic2d.rank2.models`

Implemented periodic-2D rank-two model ownership.

`Periodic2DRank2Model` refines `Periodic2DRankNModel` and fixes
`band_subspace_rank == 2`. It retains the inherited requirement for an explicit
`Periodic2DBasisIdentity` containing exactly two ordered coordinates.

`Periodic2DRank2BlockHoppingModel` combines `Periodic2DRank2Model` with
`PeriodicBlockHoppingModel`. It binds exact ordered unit-bearing two-dimensional lattice
geometry, the structured rank-two basis, and a PhysKit dense or sparse block-hopping
representation with exact `2 x 2` blocks and conjugate-displacement support. The direct
metric is derived from complete geometry rather than substituted for it.

Source owners:

- `python/src/ksdft2effmass/periodic/periodic2d/rank2/models/base.py`
- `python/src/ksdft2effmass/periodic/periodic2d/rank2/models/block_hopping.py`

Detailed architecture:

- [`Periodic2DRank2BlockHoppingModel`](Periodic2DRank2BlockHoppingModel/index.md)
- [Dimension-neutral block-hopping capability](../../../models/PeriodicBlockHoppingModel/index.md)
