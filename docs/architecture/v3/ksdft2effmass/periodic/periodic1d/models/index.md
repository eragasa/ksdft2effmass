# `ksdft2effmass.periodic.periodic1d.models`

Implemented periodic-1D nominal model ownership. `Periodic1DModel` fixes
`spatial_dimension == 1`; `Periodic1DDefectModel` additionally requires a stable pristine
parent identity. The package also contains the maintained periodic-1D Bloch-hopping
family under [`blochhopping`](blochhopping/index.md).

Rank specializations are owned separately by `periodic1d.rank1.models`,
`periodic1d.rank2.models`, and `periodic1d.rankN.models`.
