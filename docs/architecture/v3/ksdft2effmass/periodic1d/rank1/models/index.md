# `ksdft2effmass.periodic1d.rank1.models`

Implemented periodic-1D rank-one nominal model ownership.
`Periodic1DRank1Model` inherits `Periodic1DModel` and fixes
`band_subspace_rank == 1`. The maintained rank-one Bloch-hopping model is a concrete
specialization under [`blochhopping`](blochhopping/index.md).
