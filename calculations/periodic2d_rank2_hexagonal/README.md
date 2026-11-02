# Periodic-2D rank-two hexagonal-metric context

**Status: implemented replaceable calculation actions; no retained execution**

This calculation context owns the static nonorthogonal periodic-2D rank-two controls
built from the triangular Bravais metric. Its controlled inventory includes a matched
square-Bravais comparison, a triangular-Bravais case, and a triangular two-basis metric
case. The two-basis case is not a graphene or material model.

The context separates its scientific operations:

- [`gauge_alignment/`](gauge_alignment/README.md);
- [`frame_transport/`](frame_transport/README.md);
- [`band_equivalence/`](band_equivalence/README.md);
- [`hopping_locality/`](hopping_locality/README.md);
- [`support_truncation/`](support_truncation/README.md); and
- [`band_equivalence_hopping_locality/`](band_equivalence_hopping_locality/README.md), which owns thin aggregate composition and the nominal, refinement, and analysis actions.

The aggregate calculation owner contains the authoritative
[research protocol](band_equivalence_hopping_locality/protocol/README.md), bibliography,
actions, migration record, and technical report. The former experiment-tree location is
a legacy forward pointer only. This organization performs no calculation, retention,
sealing, promotion, or publication.
