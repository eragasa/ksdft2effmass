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

## Analysis order

This family is the orthogonal periodic-3D rank-two stage in the shared
[periodic analysis order](../periodic/multiband/analysis-order.md). Analyze:

1. simple-cubic geometry, parent, retained state space, units, meshes, and qualification;
2. prescribed gauge and three-direction frame transport;
3. same-space band equivalence and ordered spectra;
4. complete Fourier conversion and withheld interpolation;
5. descriptive hopping locality before complete-shell support truncation;
6. separate interpolation, truncation-only, and total consequences;
7. nominal independent verification;
8. each bounded refinement as a distinct calculation; and
9. authenticated or explicitly development-only rendering, followed later by
   cross-family comparison.

Refinement does not establish convergence, and the synthetic control does not establish
material behavior.

The nominal composition explicitly supplies three reciprocal-axis maps in lattice-axis
order. Each is named identity sewing with `ambient_dimension = 4`, so
$Q_{\mathbf{G}_a}=I_4$ acts on the parent ambient basis of the $4\times2$ retained
frame. The retained rank does not reduce the ambient identity to $I_2$, and projected
closure may remain nonidentity.

The former experiment-tree location is a legacy forward pointer only. This organization
performs no calculation, retention, sealing, promotion, or publication.
