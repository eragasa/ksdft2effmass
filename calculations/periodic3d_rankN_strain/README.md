# Prospective periodic-3D rank-N synthetic strain

**Status: GEOMETRY, M0, AND M1N SELECTED — FULL SCIENTIFIC PROTOCOL, CALCULATION, AND EVIDENCE UNSELECTED**

This dedicated strain calculation package records the decisions required for a
continuous, unit-primitive-volume synthetic Bain-path study at arbitrary finite
band-subspace rank. It is separate from the fixed-geometry periodic-3D rank-N package.
It is not an elastic, phase-stability, martensitic-transition, silicon, or other material
calculation.

The exact geometry and common-state-space subprotocol is selected in
[`geometry-common-state-space.md`](geometry-common-state-space.md). It fixes the closed
path, unit-bearing `DirectLattice3D` basis, reciprocal/reduced-coordinate conventions,
volume and endpoint certificates, integer common-cell map, basis offsets, oriented bond
inventory, common `2r` fiber, M1N frozen/metric-varying boundary, independent reference,
and typed geometry failures. The selected
[`m0-geometry-only-control.md`](m0-geometry-only-control.md) binds M0 to the shared `2r`
flat `lambda=0` analytic-parent specialization, exact `2.3` isolation certificate,
frozen rank-N gauge formula, common-space operands, and zero-response identity.

The installed [periodic-3D rank-N analytic baseline](../periodic3d/rankN/recommended-baseline.md)
selects the fixed-geometry parent and gauge controls used by M1N. The
[periodic-3D rank-two Bain protocol](../periodic3d_rank2_bain_path/band_equivalence_hopping_locality/protocol.md)
and [shared synthetic-strain donor](../periodic/multiband/gauge-locality-under-synthetic-strain.md)
supply geometry vocabulary only. Rank two is not parameter, outcome, threshold, or
evidence authority.

The full-protocol decision register is [`protocol-selection.md`](protocol-selection.md).
[`research-protocol.tex`](research-protocol.tex) is the calculation-owned TeX
composition of the selected geometry, M0, and M1N Markdown authorities. It introduces no
additional scientific selection; if a discrepancy appears, the scoped Markdown owner
must be corrected before the TeX document is used.
Capability boundaries are reserved separately for:

- [`gauge_alignment/`](gauge_alignment/README.md);
- [`frame_transport/`](frame_transport/README.md);
- [`band_equivalence/`](band_equivalence/README.md);
- [`hopping_locality/`](hopping_locality/README.md);
- [`support_truncation/`](support_truncation/README.md); and
- [`band_equivalence_hopping_locality/`](band_equivalence_hopping_locality/README.md),
  which may eventually compose the separate channels after the protocol closes.

**M0 geometry-only/frozen response**, **M1N frozen `2r`-state analytic-parent response**,
and M2 prescribed radial response remain separate channels. M0 and M1N share the common
`2r` state space and fixed energy conventions but remain scientifically distinct: M0 is
the flat `lambda=0` geometry control, while M1N retains an admitted fixed analytic parent
case. Both have exact zero common-coordinate path response while metric-derived physical
locality may change. Rank-two M0/M1 remain donors only. Exact M2, admitted
rank/depth/attack inventories, meshes, tolerances, resources, visualization, and
lifecycle contracts remain open.

The candidate rank inventory `(3, 4, 8)` and circuit-depth inventory `(1, 2, 4)` are not
adopted for this path merely because they are selected for the fixed-geometry rank-N
baseline.

## Analysis order

This context follows the continuous higher-rank path order in the shared
[periodic analysis order](../periodic/multiband/analysis-order.md):

1. selected path geometry, units, determinant/endpoints, common-cell map, offsets,
   oriented bonds, and common `2r` state space;
2. selected M0 shared-`2r` flat geometry-only control;
3. selected M1N frozen-parent null-response control;
4. exact M2 parent and response law;
5. admitted rank, depth, parent, attack, sampling, and mesh inventories;
6. same-strain/cross-strain alignment and transport applicability;
7. Fourier/interpolation, descriptive locality, and complete-shell support policy;
8. separate error operands, independent references, numerical gates, and resource bounds;
9. sampled scan/transition policy and independent verification;
10. authenticated visualization, lifecycle, no-overwrite identity, and separate execution
    authorization.

The current protocol stops after step 3. Steps 4--10 remain blocked and must not be
filled from rank-two or fixed-geometry outcomes. The reviewed projectkoios-formal
finite-quotient result is now bound as an applicability gate: positive period triples are
admitted exactly when `N2 = N3` and `N1` divides `N2`. This does not select or
authenticate a mesh, authorize execution, establish convergence, or admit evidence.

There are intentionally no Python actions, output directories, schemas, lifecycle
writers, renderers, execution identities, or retained artifacts here. Adding any of
those before the blocking scientific, resource, visualization, and authentication
contracts are selected would overstate capability.
