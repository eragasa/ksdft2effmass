# `ksdft2effmass.periodic.periodic1d.rank2.models`

Implemented periodic-1D rank-two model ownership.

`Periodic1DRank2Model` refines `Periodic1DRankNModel` and fixes
`band_subspace_rank == 2`. It inherits the requirement for an explicit
`Periodic1DBasisIdentity`; concrete descendants must supply exactly two ordered basis
coordinates.

`Periodic1DRank2BlockHoppingModel` combines `Periodic1DRank2Model` with the
representation capability `PeriodicBlockHoppingModel`. It binds immutable unit-bearing
one-dimensional geometry, the structured rank-two basis, and a PhysKit dense or sparse
block-hopping representation with exact `2 x 2` blocks and conjugate-displacement
support.

The historical `BlockHoppingModel1D` and cyclic-to-ordinary conversion values remain
separate representation and historical-study owners. Conversion does not construct a
scientific model. The concrete constructor must receive geometry, role, model identity,
and structured basis explicitly.

Source owners:

- `python/src/ksdft2effmass/periodic/periodic1d/rank2/models/base.py`
- `python/src/ksdft2effmass/periodic/periodic1d/rank2/models/block_hopping.py`

Detailed architecture:

- [`Periodic1DRank2BlockHoppingModel`](Periodic1DRank2BlockHoppingModel/index.md)
- [Dimension-neutral block-hopping capability](../../../models/PeriodicBlockHoppingModel/index.md)
