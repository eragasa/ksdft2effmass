# `ksdft2effmass.periodic.periodic2d.rankN.models`

Implemented periodic-2D finite-rank nominal model ownership.

`Periodic2DRankNModel` inherits `Periodic2DModel` and requires every concrete family to
provide a positive built-in `band_subspace_rank` and an exact
`Periodic2DBasisIdentity` with the same ordered coordinate count. Spatial dimension two
and retained rank remain independent values.

The contract does not infer basis identity from provider labels, model names, lattice
geometry, or support inventories. Fixed-rank owners refine this contract;
`Periodic2DRank2Model` fixes the inherited rank to two.

`Periodic2DRankNParentModel` is the reusable parent-field contract. Concrete analytic,
provider-backed, and calculation-owned families supply their own separated spectra,
ambient embedding, harmonic support, declared isolation-gap lower bound, stable model identity, and
explicit `Periodic2DBasisIdentity`. Reusable alignment and locality source consumes those
values without owning a concrete formula.

The independent `Periodic2DRankNGivensGaugeTransformation` remains with periodic-2D rank-N
gauge transformation. `Periodic2DRankNParentGaugeCase` is a transient study input that
correlates one supplied parent with one compatible transformation; it is not itself a
scientific model. Historical analytic formulas and request cross-product construction now
live only in test verification support. The concrete ranks 3, 4, and 8 and their explicitly
enumerated basis values remain calculation-owned in
`calculations/periodic2d/rankN/control_basis.py`; reusable source neither imports that
inventory nor synthesizes coordinates from rank.
