# `ksdft2effmass.periodic.periodic1d.rank2.models.blochhopping`

Abstract periodic-1D Bloch-hopping owner with retained-space dimension exactly two.
It refines `Periodic1DRankNBlochHoppingModel` through the fixed-rank
`Periodic1DRank2Model` branch and therefore retains the explicit structured-basis
contract of the finite-rank owner.

This owner does not manufacture a concrete scientific model, calculation, durable wire,
or retained result. Concrete descendants remain responsible for coefficient and
scientific admissibility.
