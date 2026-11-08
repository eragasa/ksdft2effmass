# `ksdft2effmass.periodic.periodic3d.rankN.models`

Implemented periodic-3D finite-rank nominal model ownership.

`Periodic3DRankNModel` inherits `Periodic3DModel` and requires every concrete family to
provide a positive built-in `band_subspace_rank` and an exact
`Periodic3DBasisIdentity` with the same ordered coordinate count. Spatial dimension
three and retained rank remain independent values.

The contract does not infer basis identity from provider labels, model names, lattice
geometry, or support inventories. Fixed-rank owners refine this contract;
`Periodic3DRank2Model` fixes the inherited rank to two. Existing aggregate case values
and provider hopping parents remain separate migration targets.
