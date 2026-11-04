# Periodic-1D rank-one support truncation

**Status:** implemented rank-owned capability; tested in memory; not yet serialized as a separate execution result

This operation owns deliberate finite-support removal from the rank-one Fourier
representation. It binds an explicit periodic-1D lattice geometry and preserves the exact
source calculation, source mesh, and source range by identity.

For every declared support it exposes the retained coefficients and the corresponding
evaluation candidate. Interpolation, truncation-only, and total errors remain separate;
a support-truncated result is not relabelled as a complete Fourier representation.

Source ownership resides in
`ksdft2effmass.periodic1d.rank1.support_truncation`. The aggregate protocol, independent
verification, rendering, and current unsealed execution live under
[`../band_equivalence_hopping_locality/`](../band_equivalence_hopping_locality/).
