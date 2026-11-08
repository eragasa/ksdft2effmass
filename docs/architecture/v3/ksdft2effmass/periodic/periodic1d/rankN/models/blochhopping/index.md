# `ksdft2effmass.periodic.periodic1d.rankN.models.blochhopping`

Abstract periodic-1D Bloch-hopping owner for a declared finite retained-space dimension.
Concrete families must supply the inherited exact `Periodic1DBasisIdentity` and enforce
their reviewed retained-rank inventories.

`Periodic1DRank2BlochHoppingModel` refines this owner and fixes the retained rank to two.
The finite-rank owner introduces no calculation, durable wire, or retained result.
