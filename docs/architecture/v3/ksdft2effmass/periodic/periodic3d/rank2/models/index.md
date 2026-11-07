# `ksdft2effmass.periodic.periodic3d.rank2.models`

Implemented periodic-3D rank-two model ownership.

`Periodic3DRank2Model` inherits `Periodic3DModel` and fixes
`band_subspace_rank == 2`. `Periodic3DRank2BlockHoppingModel` directly inherits the
shared `PeriodicRank2BlockHoppingModel`, binds an exact three-dimensional lattice
metric, and composes a PhysKit dense or sparse block-hopping representation with exact
`2 x 2` blocks and conjugate displacement support.

Source owners:

- `python/src/ksdft2effmass/periodic/periodic3d/rank2/models/base.py`
- `python/src/ksdft2effmass/periodic/periodic3d/rank2/models/block_hopping.py`

Detailed architecture:

- [`Periodic3DRank2BlockHoppingModel`](Periodic3DRank2BlockHoppingModel/index.md)
- [Shared rank-two block-hopping parent](../../../models/PeriodicRank2BlockHoppingModel/index.md)
