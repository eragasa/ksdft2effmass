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

## Analysis order

This family follows the nonorthogonal/basis-aware rank-two stage of the shared
[periodic analysis order](../periodic/multiband/analysis-order.md). Analyze:

1. geometry, units, common retained state space, parent, and qualification;
2. the matched square-Bravais control;
3. the triangular-Bravais case;
4. the triangular two-basis metric case, using basis-aware distances;
5. gauge alignment and frame transport;
6. band equivalence, complete Fourier interpolation, and descriptive locality;
7. complete-shell support truncation and separate interpolation/truncation/total
   consequences;
8. nominal verification, then each bounded refinement as a distinct calculation; and
9. authenticated or explicitly development-only rendering, followed later by the
   cross-family comparison.

The case order isolates Bravais-metric and basis-offset effects. It does not make the
two-basis control a material model, and refinements do not establish convergence.

The nominal composition explicitly supplies two reciprocal-axis maps in lattice-axis
order. Both are named identity sewing with `ambient_dimension = 4`, so
$Q_{\mathbf{G}_a}=I_4$ acts on the parent ambient basis of each $4\times2$ retained
frame. Retained rank two does not change the identity-map order, and the projected
closure is not required to be identity.

The aggregate calculation owner contains the authoritative
[research protocol](band_equivalence_hopping_locality/protocol/README.md), bibliography,
actions, migration record, and technical report. The former experiment-tree location is
a legacy forward pointer only. This organization performs no calculation, retention,
sealing, promotion, or publication.
