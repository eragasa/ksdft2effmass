# `ksdft2effmass.periodic.periodic2d.rankN.models`

Implemented periodic-2D finite-rank nominal model ownership.

`Periodic2DRankNModel` inherits `Periodic2DModel` and requires every concrete family to
provide a positive built-in `band_subspace_rank` and an exact
`Periodic2DBasisIdentity` with the same ordered coordinate count. Spatial dimension two
and retained rank remain independent values.

The contract does not infer basis identity from provider labels, model names, lattice
geometry, or support inventories. Fixed-rank owners refine this contract;
`Periodic2DRank2Model` fixes the inherited rank to two.

`Periodic2DRankNAnalyticParentModel` is the reusable dimensionless parent selected by the
synthetic software baseline. It owns the separated retained/exterior spectrum, exact
retained embedding, explicit `Periodic2DBasisIdentity`, and contextual
`PeriodicModelRole`. It owns no gauge transformation, geometry case, mesh, or calculation rank
inventory.

The independent `Periodic2DRankNGivensGaugeTransformation` remains with periodic-2D rank-N gauge
alignment. `Periodic2DRankNAnalyticCase` is only the band-equivalence/locality case
composition correlating one parent and one compatible attack. The concrete ranks 3, 4,
and 8 and their explicitly enumerated basis values are composed by
`calculations/periodic2d/rankN/control_basis.py`; reusable source does not import that
calculation-owned instance or synthesize coordinates from rank.
