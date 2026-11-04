# Periodic-1D rank-one gauge alignment

**Status:** implemented operator-trivial applicability capability; no separate retained execution

This operation owns the rank-one gauge-alignment applicability boundary. For a scalar
represented Hamiltonian and any phase field \(U(k)\in U(1)\),

\[
U(k)^\dagger H(k)U(k)=H(k).
\]

Consequently, identity, global-unitary, pointwise-unitary, inverse-oracle, and restricted
internal-rotation cases must not be manufactured as distinct operator-locality results.
The maintained source owner records one `operator-trivial` applicability result with an
explicit periodic-1D lattice geometry.

Source ownership:

- `ksdft2effmass.periodic1d.rank1.alignment` owns the applicability action and result;
- `ksdft2effmass.periodic1d.rank1.gauge_alignment` owns rank-one gauge-alignment
  guardrails; and
- [`../band_equivalence_hopping_locality/`](../band_equivalence_hopping_locality/)
  establishes the scalar identity before interpreting locality or truncation channels.

This operation does not authorize a duplicate numerical alignment campaign.
