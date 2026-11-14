# Periodic-1D rank-one hopping locality

**Status:** implemented rank-owned capability; tested in memory; not yet serialized as a separate execution result

This operation owns descriptive locality of the complete rank-one Fourier
representation before support removal. It binds an explicit periodic-1D lattice geometry
to the exact source calculation and construction mesh, then exposes one immutable hopping
tail value for every declared range.

The operation preserves the complete coefficient inventory and reports omitted-tail
quantities without constructing a truncated operator. Irreversible coefficient removal
belongs to [`../support_truncation/`](../support_truncation/).

Source ownership resides in
`ksdft2effmass.periodic1d.rank1.hopping_locality`. The aggregate numerical producer and
current unsealed execution live under
[`../band_equivalence_hopping_locality/`](../band_equivalence_hopping_locality/).
