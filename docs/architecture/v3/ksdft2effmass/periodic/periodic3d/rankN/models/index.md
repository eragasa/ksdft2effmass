# `ksdft2effmass.periodic.periodic3d.rankN.models`

Implemented periodic-3D finite-rank nominal model ownership.

`Periodic3DRankNModel` inherits `Periodic3DModel` and requires every concrete family to
provide a positive built-in `band_subspace_rank` and an exact
`Periodic3DBasisIdentity` with the same ordered coordinate count. Spatial dimension
three and retained rank remain independent values.

The contract does not infer basis identity from provider labels, model names, lattice
geometry, or support inventories. Fixed-rank owners refine this contract;
`Periodic3DRank2Model` fixes the inherited rank to two.

`Periodic3DRankNParentModel` defines the reusable parent-field boundary. Concrete
analytic, provider-backed, and calculation-owned families supply their own spectra,
ambient embedding, harmonic support, isolation-gap lower bound, stable model identity,
and exact `Periodic3DBasisIdentity`. Reusable alignment and locality source consumes
those values without owning a formula or provider representation.

`Periodic3DRankNParentGaugeCase` is a transient study input correlating one supplied
parent with one independent transformation. The associated field sampler uses the
parent's structured basis display identity rather than constructing a label from a model
family string. Historical analytic formulas, PhysKit block-hopping construction, and
request cross-product expansion live only in verification support until a calculation
owns an admitted composition.
