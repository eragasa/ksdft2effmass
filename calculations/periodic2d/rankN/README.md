# Periodic-2D finite-rank calculations

**Status: PROSPECTIVE — NO CALCULATION OR EVIDENCE**

This root is reserved for separately reviewed periodic-2D retained-rank-\(N\)
calculations governed by the dimension-indexed arbitrary-finite-rank construction in
Ragasa2026c. It is not an alias for the installed Ragasa2026b rank-two calculations and
does not change their requests, results, verification records, or retained bytes.

The reusable finite-rank operator and ordered-spectrum loss definition is
`BandEquivalenceHoppingLocalityLossDefinition`; `BandEquivalenceHoppingLocalityLoss` composes that
definition with calculated values. The definition uses the Ragasa2026c cross-rank
quadratic normalization \(rE_{\mathrm{norm}}^2\), with `norm_energy_scale` declaring
\(E_{\mathrm{norm}}>0\); its rank-two specialization is exactly the Ragasa2026a loss.
Its typed identity separately retains the reciprocal-sample inventory, retained space,
basis, gauge, geometry, energy unit, and common energy-zero/alignment convention. Those
software values alone are not a periodic-2D rank-\(N\) calculation.

Any installed calculation below this root must compose the common scientific bases rather
than create calculation-local substitutes:

- `SubspaceReduction` for the declared parent-to-retained-space map;
- `RepresentationEquivalence` for aligned represented-operator comparisons;
- `RealSpaceSupportTruncation` for complete metric-shell support removal and
  minimum-tolerance support selection; and
- `NumericalConsistency` for reciprocal-mesh and independent-route assessments.

`BaseTypedRecord` remains a serialization boundary only. SHA-256 establishes byte
identity, not scientific validity.

The source hierarchy is capability-first: dimension-neutral periodic finite-rank owners
are refined by periodic-2D rank-N owners, and applicable periodic-2D rank-two operation
owners refine those rank-N owners while fixing rank two. This does not admit rank two to
the calculation-owned `3`, `4`, and `8` study inventory or transfer any rank-two
calculation result, threshold, lifecycle, or evidence identity.

## Analysis order

This prospective family follows the higher-rank admission order in the shared
[periodic analysis order](../../periodic/multiband/analysis-order.md):

1. select the parent/common state space and keep lattice dimension, ambient dimension,
   band rank, numerical rank, retained rank, and circuit depth distinct;
2. select direct geometry, basis offsets, reciprocal convention, and units;
3. select the gauge group, generators, action side, depth meaning, and oracle boundary;
4. select alignment applicability and numerical-rank failure semantics;
5. select meshes and two-direction transport/plaquette topology;
6. select Fourier, locality, complete-shell support, and error operands;
7. freeze independent references, gates, and resource bounds;
8. select authenticated visualization and lifecycle/no-overwrite identity; and only then
9. request separate implementation, calculation, verification, and execution authority.

The current root remains prospective; software loss values alone do not advance this
scientific sequence. `control_basis.py` composes the explicitly enumerated structured
basis values for the selected ranks 3, 4, and 8. Importing that module performs no
calculation and creates no evidence; reusable source owns only the generic immutable
inventory contract and dimensional basis identities.

## Open protocol decisions

The calculation-owned decision register is
[`protocol-selection.md`](protocol-selection.md), with an exact analytic recommendation
in [`recommended-baseline.md`](recommended-baseline.md). The prospective fixed-geometry family boundary is
[`composite-band-alignment-locality/`](composite-band-alignment-locality/README.md).
A continuous deformation study is a separate calculation identity under
[`calculations/periodic2d_rankN_strain/`](../../periodic2d_rankN_strain/README.md);
this fixed-geometry root does not select that package's path or response laws.

Ragasa2026c selects a later cross-dimensional rank/depth subset but explicitly does not
select the periodic-2D harmonic coefficients, tensor meshes, support inventory, family
identity, or evidence status. Those decisions remain scientifically open and will not be
inferred from the periodic-1D higher-rank protocol or the periodic-2D rank-two controls.
Consequently, this root contains no calculation, verification, or rendering entrypoint.

Production execution, retained-result creation, sealing, promotion, and publication
require separate explicit authorization after the periodic-2D protocol and implementation
have been reviewed.
