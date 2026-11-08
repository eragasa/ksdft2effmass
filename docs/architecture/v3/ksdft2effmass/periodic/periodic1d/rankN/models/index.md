# `ksdft2effmass.periodic.periodic1d.rankN.models`

Implemented periodic-1D finite-rank nominal model ownership.

`Periodic1DRankNModel` inherits `Periodic1DModel` and requires every concrete family to
provide:

- a positive built-in `band_subspace_rank`; and
- an exact `Periodic1DBasisIdentity` whose ordered coordinate count equals that rank.

The contract does not infer basis coordinates from provider strings, model names,
geometry, or hopping support. It does not enumerate an approved global rank set.
Fixed-rank owners refine this contract; in particular, `Periodic1DRank2Model` is a
subclass that fixes the inherited rank to two.

The finite-rank Bloch-hopping specialization remains abstract under
[`blochhopping`](blochhopping/index.md). It is refined by the rank-two Bloch-hopping
owner rather than duplicated as a sibling capability.
