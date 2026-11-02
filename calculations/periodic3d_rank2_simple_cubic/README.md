# Periodic-3D rank-two simple-cubic context

**Status: implemented replaceable calculation actions; no retained execution**

This calculation context owns the orthogonal simple-cubic rank-two controlled model. Its
family is `simple_cubic`, its nominal construction/evaluation sizes are `8/17`, and its
support inventory uses complete physical-metric shells. It is a synthetic control, not a
material calculation.

The context separates its scientific operations:

- [`gauge_alignment/`](gauge_alignment/README.md);
- [`frame_transport/`](frame_transport/README.md);
- [`band_equivalence/`](band_equivalence/README.md);
- [`hopping_locality/`](hopping_locality/README.md);
- [`support_truncation/`](support_truncation/README.md); and
- [`band_equivalence_hopping_locality/`](band_equivalence_hopping_locality/README.md),
  which owns the authoritative protocol, thin aggregate composition, nominal and
  refinement calculations, replaceable analysis, migration record, and technical report.

The former experiment-tree location is a legacy forward pointer only. This organization
performs no calculation, retention, sealing, promotion, or publication.
