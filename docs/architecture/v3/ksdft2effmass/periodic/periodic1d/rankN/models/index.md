# `ksdft2effmass.periodic.periodic1d.rankN.models`

Implemented periodic-1D arbitrary-finite-rank nominal model ownership.
`Periodic1DRankNModel` inherits `Periodic1DModel` and requires each concrete family to
report its finite `band_subspace_rank`. It does not admit or enumerate ranks globally.
The Bloch-hopping specialization remains abstract under
[`blochhopping`](blochhopping/index.md).
