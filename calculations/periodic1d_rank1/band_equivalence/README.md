# Periodic-1D rank-one band equivalence

**Status:** implemented through the scalar Fourier-locality producer; one local unsealed aggregate execution

This operation owns the rank-one retained scalar field and its finite complete cyclic
Fourier reconstruction. At rank one, band equivalence is scalar equality on the declared
sample inventories rather than a non-Abelian frame-selection problem.

The maintained `Periodic1DFourierLocalityConfiguration`, result, and analyzer implement
the concrete rank-one band-equivalence request, analysis, and action roles. The operation
retains interpolation error separately from deliberate support-removal error and does not
interpret finite sampled agreement as continuum equality.

The executable protocol and current unsealed result package live under
[`../band_equivalence_hopping_locality/`](../band_equivalence_hopping_locality/). No
separate duplicate band-equivalence execution is produced.
