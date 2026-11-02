# Periodic-3D rank-two FCC/diamond context

**Status: implemented replaceable calculation actions; no retained execution**

This calculation context owns the FCC-Bravais and diamond-basis rank-two controlled
models, including the matched simple-cubic Bravais control. The two-basis case is a
synthetic connectivity and geometry control. It is explicitly **not a silicon material
calculation**, parameterization, validation, or effective-mass result.

The context separates its scientific operations:

- [`gauge_alignment/`](gauge_alignment/README.md);
- [`frame_transport/`](frame_transport/README.md);
- [`band_equivalence/`](band_equivalence/README.md);
- [`hopping_locality/`](hopping_locality/README.md);
- [`support_truncation/`](support_truncation/README.md); and
- [`band_equivalence_hopping_locality/`](band_equivalence_hopping_locality/README.md),
  which owns the authoritative protocol and bibliography, thin aggregate composition,
  nominal and refinement calculations, replaceable analysis, migration record, and
  technical report.

The former experiment-tree location is a legacy forward pointer only. This organization
performs no calculation, retention, sealing, promotion, or publication.
