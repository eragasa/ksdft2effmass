# `ksdft2effmass.periodic.periodic1d.rank2.models`

Implemented periodic-1D rank-two nominal model ownership.
`Periodic1DRank2Model` inherits `Periodic1DModel` and fixes
`band_subspace_rank == 2`. Rank two is a sibling of rank N. The Bloch-hopping
specialization remains abstract under [`blochhopping`](blochhopping/index.md).

`Periodic1DRank2BlockHoppingModel` directly inherits the shared
`PeriodicRank2BlockHoppingModel`, binds immutable physical one-dimensional geometry,
and composes a PhysKit dense or sparse block-hopping representation with exact `2 x 2`
blocks and conjugate displacement support.

The existing legacy `BlockHoppingModel1D` and cyclic-to-ordinary conversion values remain
separate representation and historical-study owners during migration. They are not added
to this inheritance hierarchy. No shared admission class or compatibility model is
approved; study composition uses the existing values and the existing concrete model
constructor explicitly.

Source owners:

- `python/src/ksdft2effmass/periodic/periodic1d/rank2/models/base.py`
- `python/src/ksdft2effmass/periodic/periodic1d/rank2/models/block_hopping.py`

Detailed architecture:

- [`Periodic1DRank2BlockHoppingModel`](Periodic1DRank2BlockHoppingModel/index.md)
- [Shared rank-two block-hopping parent](../../../models/PeriodicRank2BlockHoppingModel/index.md)
