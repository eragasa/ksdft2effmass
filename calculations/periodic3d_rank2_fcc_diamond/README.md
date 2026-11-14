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

## Analysis order

This family follows the nonorthogonal/basis-aware rank-two stage of the shared
[periodic analysis order](../periodic/multiband/analysis-order.md). Analyze:

1. geometry, parent, retained state space, units, meshes, and qualification;
2. the matched simple-cubic Bravais control;
3. the FCC Bravais control;
4. the FCC two-basis metric control with basis-aware distances;
5. prescribed gauge and three-direction frame transport;
6. same-space band equivalence, complete Fourier interpolation, and descriptive locality;
7. complete-shell truncation and separate interpolation/truncation/total consequences;
8. nominal independent verification, then each bounded refinement separately; and
9. authenticated or explicitly development-only rendering, followed later by the
   cross-family comparison.

The case order isolates metric and basis-offset effects. It does not turn the two-basis
control into silicon, and refinement is not convergence evidence.

The nominal composition explicitly supplies three reciprocal-axis maps in lattice-axis
order. Each is named identity sewing with `ambient_dimension = 4`, so
$Q_{\mathbf{G}_a}=I_4$ acts on the parent ambient basis of the $4\times2$ retained
frame. Retained rank two does not imply $I_2$, and projected closure may remain
nonidentity.

The former experiment-tree location is a legacy forward pointer only. This organization
performs no calculation, retention, sealing, promotion, or publication.
