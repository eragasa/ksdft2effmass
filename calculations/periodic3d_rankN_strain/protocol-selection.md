# Periodic-3D rank-N synthetic-strain protocol-selection record

**Status: GEOMETRY, M0, AND M1N SELECTED — FULL SCIENTIFIC PROTOCOL UNSELECTED; EXECUTION AND RETAINED OUTPUT PROHIBITED**

## Determination

The repository does not contain one closed scientific protocol for this dedicated
periodic-3D rank-N synthetic-strain package's selected Bain path.

Three authoritative surfaces cover different, noncomposable scopes:

1. [`calculations/periodic3d/rankN/recommended-baseline.md`](../periodic3d/rankN/recommended-baseline.md)
   selects a fixed-geometry analytic parent and gauge circuit for ranks `3`, `4`, and
   `8`, but no continuous strain coordinate or M0/M1N/M2 response law.
2. [`calculations/periodic3d_rank2_bain_path/band_equivalence_hopping_locality/protocol.md`](../periodic3d_rank2_bain_path/band_equivalence_hopping_locality/protocol.md)
   selects a continuous unit-volume Bain path and bounded rank-two M0/M1/M2 controls,
   but its parent, correlation formulas, meshes, tolerances, and response definitions
   are rank-two contracts.
3. [`calculations/periodic/multiband/gauge-locality-under-synthetic-strain.md`](../periodic/multiband/gauge-locality-under-synthetic-strain.md)
   preserves the shared rank-two synthetic-strain donor and explicitly leaves
   dimension-specific authority to the rhombic and Bain contexts.

The physical and numerical specifications under `specification/` govern material-facing
silicon work and do not authorize this synthetic family. Their separation of physical,
numerical/discretization, and model-reduction errors remains applicable as a scientific
integrity rule, but their silicon parent, meshes, tolerances, and material conventions
are not donors.

Consequently this context now owns one exact
[geometry/common-state-space subprotocol](geometry-common-state-space.md), the
[M0 geometry-only control](m0-geometry-only-control.md), and the M1N response boundary,
while retaining the remaining decisions and blockers below. It does
not define a request that software may execute. The calculation-owned
[`research-protocol.tex`](research-protocol.tex) composes these selected Markdown
contracts for typesetting and introduces no additional authority.

## Selected context boundaries

The current task authority selects only these boundaries:

- the geometry is the exact closed `s in [0, 1]` unit-primitive-volume synthetic Bain
  path, unit identity, orientation, direct/reciprocal basis convention, FCC/BCC endpoint
  identity, integer common-cell map, basis-offset map, and oriented bond inventory in
  [`geometry-common-state-space.md`](geometry-common-state-space.md);
- the study is not material strain, elasticity, phase stability, a martensitic
  transition, silicon, or material validation;
- the selected M0 shared-`2r` flat `lambda=0` geometry-only response, the selected M1N
  frozen `2r`-state analytic-parent response, and the unselected M2 prescribed radial
  response are distinct channels and may not be averaged or merged;
- rank-two M1 remains a four-state donor control and is not renamed, widened, or included
  in a rank-N outcome;
- gauge alignment, frame transport, band equivalence, hopping locality, irreversible
  support truncation, withheld interpolation, truncation-only consequence, and total
  consequence remain distinct operations;
- rank-two parameters, outcomes, tolerances, meshes, and evidence do not transfer;
- no cross-rank outcome, threshold, support, convergence, or evidence transfer is
  permitted; and
- failed or absent qualification must remain explicitly `unresolved` or `inapplicable`,
  never fabricated as zero or silently repaired after observing an outcome.

These boundaries select the M0 and M1N parent/gauge semantics and geometry identities
but do not select the M2 parent/response, admitted rank/depth/attack inventories, a
finite sample, tolerance, or lifecycle.

## Dimension and rank vocabulary

Every future request and result must keep the following quantities separate:

| Quantity | Meaning in this prospective context | Current disposition |
|---|---|---|
| Lattice dimension | Three primitive periodic directions defining the Bain metric and reciprocal torus | SELECTED: `3` |
| Ambient parent dimension | Dimension of the parent fiber on which the full synthetic operator acts | SELECTED FOR M0 AND M1N: `2r`; M2 remains unselected |
| Band-subspace rank | Dimension `r` of the represented band subspace at each reciprocal point | CANDIDATE INVENTORY: `(3, 4, 8)`; not yet adopted for this path |
| Numerical rank | Tolerance-dependent rank of an overlap/link matrix used by Procrustes or transport | SOFTWARE POLICY EXISTS for the fixed-geometry baseline; path applicability is unselected |
| Model-reduction retained rank | Rank retained by a genuine parent-to-reduced-model approximation | NOT PRESENT unless a future protocol introduces a distinct reduction; it must not be inferred from `r` |
| Circuit depth | Number of ordered gauge-circuit layers, not a lattice, ambient, numerical, or retained rank | CANDIDATE INVENTORY: `(1, 2, 4)`; not yet adopted for this path |

Rank four remains a value of rank-N and does not create a `rank4` namespace.

## Blocking scientific contract audit

Every row below must be closed by one reviewed protocol before calculation software,
writers, schemas, or outputs are added.

| Contract | Existing or selected information | Disposition or remaining rank-N Bain selection |
|---|---|---|
| Study identity | This filesystem locator names a prospective context | Permanent campaign-family identity, version boundary, case identifiers, and exact claim inventory |
| Strained parent and common state space | M0 and M1N select the same ordered retained/exterior `2r` direct sum, retained seed, dimensionless energy zero, `norm_energy_scale=1`, and common cell/state map; M0 fixes the flat `lambda=0` specialization and exact `2.3` isolation certificate | SELECTED FOR M0/M1N in `geometry-common-state-space.md` and `m0-geometry-only-control.md`; the exact M2 parent and whether it shares these conventions remain open |
| Geometry and metric path | Exact closed path, unit-bearing `DirectLattice3D` orientation, reciprocal/reduced-coordinate convention, determinant and endpoint certificates, integer FCC/Bain map, two reduced basis offsets, oriented six-bond inventory, and the reviewed projectkoios-formal finite-quotient criterion `N2 = N3` with `N1` dividing `N2` | SELECTED in `geometry-common-state-space.md`; quotient applicability is closed, but the actual period triple, mesh authentication, execution correctness, convergence, and evidence admission remain unselected |
| Rank and depth inventory | Fixed-geometry rank-N admits ranks `(3, 4, 8)` and depths `(1, 2, 4)` | Whether the path adopts all or a reviewed subset; whether every rank/depth is evaluated on identical path samples; whether depth is held fixed under strain |
| Gauge/depth action | M0 and M1N select the fixed-geometry right-acting alternating real Givens `SO(r)` circuit, bond-RMS normalization, known inverse, layer ordering, action side, inner product, and oriented common-coordinate bond inventory to remain fixed along the path | Exact admitted rank/depth/amplitude inventory and M2 gauge law; fitted same-strain and cross-strain alignment applicability remain open |
| Alignment inventory | Fixed-geometry rank-N supplies identity, complete global-unitary Procrustes, pointwise-unitary Procrustes, and known-inverse oracle | Which alignments answer same-strain representation equivalence; which align different strain points; whether a single path-consistent alignment is required; applicability and rank-deficient outcomes. Rank-two global-real correlation formulas are not rank-N definitions |
| M0 definition | Operator-selected shared `2r` flat `lambda=0` specialization with simple retained/exterior ladders, fixed energy conventions, exact `2.3` gap, frozen rank-N gauge formula, same/cross-strain operands, Fourier invariance, analytic references, and typed outcomes | SELECTED in `m0-geometry-only-control.md`; admitted rank/depth/attack values and all numerical/reporting policies remain open |
| M1N definition | Human selection chooses a frozen `2r`-state rank-N response based on the fixed-geometry analytic parent | SELECTED below and bound to `geometry-common-state-space.md`: the parent, retained seed, reduced-coordinate gauge circuit, onsite/hopping coefficients, energy zero, normalization, oriented bond inventory, and reduced offsets are independent of path parameter; only the selected Bain metric and derived physical support classification may vary. Admitted parameter inventories remain open |
| M2 definition | Rank two changes selected inter-sublattice amplitudes with a prescribed radial law and `beta=1` | Parent/bond entries affected in the rank-N state space, reference lengths, exponent and coefficient inventory, onsite disposition, normalization, rank/depth dependence, and independent response oracle. `beta=1` is not transferred |
| Path sampling | Rank two uses nine bounded fractions and a separate 201-point development scan | Base path grid, endpoint rule, adaptive/transition rule, between-sample claim boundary, interior-extremum handling, and prohibition on outcome-driven reselection |
| Construction meshes | Fixed-geometry rank-N selects `8^3`; rank-two M0 uses `24^3` and response uses `8^3` | Exact mesh for each rank, depth, and M channel; offsets; refinement relation; maximum size; endpoint sewing; and whether one mesh inventory is common across the path |
| Withheld evaluation | Both donors use shifted finite evaluation controls in some channels | Exact disjoint evaluation mesh, shift, withheld inventory, path/rank/depth binding, and rule forbidding evaluation-driven parameter reselection |
| Frame transport | Fixed-geometry rank-N installs three reciprocal neighbor directions, closures, and three plaquette orientations | Per-path-point link operands; whether transport in the strain direction is also required; primitive closures; all plaquette dispositions; optional cell invariant; path sewing; numerical-rank policy; typed rank-deficient inapplicability |
| Fourier convention | Fixed-geometry rank-N installs a centered finite-periodic Fourier reference for fixed cases | Exact tensor transform along each path metric, displacement inventory, mesh-origin convention, endpoint/self-inverse handling, ordinary versus centered-Nyquist separation, Hermitian pairing, Parseval normalization, and strain-comparison identity |
| Hopping locality | The geometry subprotocol selects the unit-bearing basis-resolved physical-displacement rule; both donors separate descriptive hopping power from support removal | Exact onsite/nononsite partition, raw and rank/energy-normalized powers, physical-radius diagnostics, and treatment of shell degeneracy changes along the path |
| Support ladder | Rank two uses complete physical-radius shells; fixed-geometry rank-N uses family shell caps | Complete conjugate-closed metric-shell inventory at every path point, common versus pointwise supports, shell cap or complete ladder, equal-radius ties, irreversible removal rule, retained-block count, and unresolved outcome |
| Error operands | Installed rank-N arithmetic separates operator and ordered-spectrum errors; rank two separates interpolation, truncation, and total channels | Exact same-space operands after alignment, common basis/gauge/energy reference, raw and normalized functionals, withheld interpolation, truncation-only reference, total direct-field reference, path-difference `Delta H_s`, and prohibition on adding separately maximized channels |
| Independent references | Fixed-geometry rank-N has bounded parent, alignment, transport, Fourier, shell-power, and support-selection references; the path subprotocols select independent geometry/common-map/state-space, M0 parent/gauge/equivalence/invariance, and M1N invariance obligations | Implementation of those selected geometry/M0/M1N references plus an independent M2 response route, scan/transition reconstruction, and independence from the eventual producer |
| Numerical gates | Fixed-geometry rank-N has software rank thresholds and provisional `1e-3`/`1e-5` controls; rank two has its own bounded gates | Scientific tolerances, strict/inclusive comparisons, Hermiticity/Parseval/sewing/gap/transport thresholds, effect-resolution floor, overflow policy, refinement gates, and typed `unresolved`/`inapplicable` reasons. Existing controls are not transferred convergence tolerances |
| Resource envelope | No periodic-3D rank-N lifecycle resource envelope is selected | Maximum rank/depth/path/case counts, memory model, dense-matrix prohibition or bound, batching, expected wall time, local/external resource boundary, scratch and retained-byte budgets, and preflight failure behavior |
| Visualization projection | Rank-N visualization is explicitly unselected | Exact rank/depth/path/channel/alignment operands, invariant scalar reductions, uncertainty/applicability marks, plot inventory, authenticated projection, and rule preventing rendering from calculating new science |
| Lifecycle and authentication | Fixed-geometry rank-N has typed in-memory aggregate verification but no lifecycle; rank two has unrelated replaceable actions | Exact request/result/schema inventory, provenance and environment identity, producer-independent admission, visualization authentication, stage ordering, evidence statuses, and migration policy |
| No-overwrite identity | No rank-N Bain execution identity exists | Stable identity containing protocol revision and all scientifically identity-bearing rank/depth/path/channel/mesh/support choices; incomplete-directory behavior; atomic finalization; refusal to overwrite; recovery and collision policy |

## Selected M0 response contract

The operator selected **Option A: shared `2r` flat specialization**. The exact contract is
[`m0-geometry-only-control.md`](m0-geometry-only-control.md). For every later admitted
finite rank `r > 1`, M0 uses the fixed analytic parent's parameter-free `lambda=0`
specialization on

\[
 \mathbb C^{2r}=\mathbb C^r_{\mathrm{ret}}\oplus
 \mathbb C^r_{\mathrm{ext}},
 \qquad F_0=[I_r\;0]^\mathsf T.
\]

Its retained energies `0.4 xi_j` and exterior energies `3.0 + 0.3 xi_j` are simple,
independent of `q` and `s`, use the fixed dimensionless energy zero and
`norm_energy_scale=1`, and have exact analytic retained-to-exterior gap `2.3`. The M0
right-acting alternating Givens circuit uses the selected oriented Bain bonds and
bond-RMS normalization and remains fixed in common reduced coordinates for all
`s in [0, 1]`. The full and retained represented operators and every reduced-coordinate
Fourier coefficient are therefore independent of `s`; only metric-derived physical
lengths, shell classifications, and radii may change.

M0 shares state-space and energy conventions with M1N but remains a separately named
flat-parent geometry channel. This selection does not adopt a rank, depth, attack,
sample, mesh, fitted alignment, tolerance, support, resource, visualization, lifecycle,
or execution inventory. The exact `2.3` gap is an analytic certificate, not a calculated
or material result.

## Selected M1N response contract

The human selection closes the former M1 state-space conflict by defining and renaming
the rank-N channel:

> **M1N — frozen `2r`-state analytic-parent response control**

For any later admitted rank `r`, depth `L`, parent scale `lambda`, and attack coefficient
`A`, M1N uses the fixed-geometry analytic parent from
`calculations/periodic3d/rankN/recommended-baseline.md` with the selected oriented
common-coordinate bond inventory \(\mathcal B_B\) on

\[
 \mathbb C^{2r}=\mathbb C^r_{\mathrm{ret}}\oplus
 \mathbb C^r_{\mathrm{ext}},
 \qquad F_0=[I_r\;0]^\mathsf T.
\]

Using the selected common Bain coordinate map and oriented bond inventory from
[`geometry-common-state-space.md`](geometry-common-state-space.md), the M1N fields are
frozen in those reduced coordinates for every path parameter `s`:

\[
 H^{\mathrm{M1N}}_{r,\mathcal B_B}(q,s;\lambda)
 =H_{r,\mathcal B_B}(q;\lambda),
 \qquad
 G^{\mathrm{M1N}}_{r,L,\mathcal B_B}(q,s;A)
 =G_{r,L,\mathcal B_B}(q;A).
\]

Thus the parent onsite and hopping coefficient matrices, retained/exterior basis,
retained seed, circuit ordering and depth, energy zero, dimensionless energy unit,
`norm_energy_scale=1`, and known-inverse construction oracle are independent of `s`.
Only the selected unit-volume Bain metric and quantities derived from that
metric—physical bond lengths, metric-shell membership, physical support radius, and
basis-aware distances—may vary with `s`. The analytic external-gap lower bound `1.9`
therefore remains the selected M1N parent bound; this is an analytic property, not a
calculated result.

For the attacked retained operator

\[
 \widetilde D^{\mathrm{M1N}}_{r,L,\mathcal B_B}(q,s)
 =G_{r,L,\mathcal B_B}(q)^\dagger
 D_{r,\mathcal B_B}(q)G_{r,L,\mathcal B_B}(q),
\]

the exact common-coordinate strain response is zero after the selected state-space map.
Any nonzero aligned M1N `Delta H_s` is a numerical/state-identification diagnostic and
must not be interpreted as physical response. Descriptive physical-radius locality may
still change because the metric changes; that geometry effect is not an operator
response.

`M1N` is the scientific channel label; a future wire identifier should use the explicit
form `m1n-frozen-2r-state-analytic-parent` only after schema review. Rank-two M1 retains
its four-state identity and is neither an M1N case nor cross-rank evidence. This selection
does not adopt the candidate ranks, depths, `lambda`, `A`, meshes, path samples,
tolerances, resources, visualization, or lifecycle.

## Operation boundaries

A future aggregate may sequence capabilities but must not collapse them:

- **Gauge alignment** chooses or assesses right actions in one declared state space.
- **Frame transport** diagnoses links, closures, and plaquettes; it does not construct a
  unique global gauge.
- **Band equivalence** compares aligned represented operators and ordered spectra.
- **Hopping locality** reports unchanged Fourier-block powers and physical ranges.
- **Support truncation** irreversibly removes complete support and returns minimum-support
  or unresolved outcomes.
- **Withheld interpolation** compares the complete finite interpolant with the direct
  withheld field before support removal.
- **Truncation-only consequence** compares a truncated interpolant with its complete
  interpolant.
- **Total consequence** compares that truncated model with the direct withheld field.

Parent-model, finite-sampling, and model-reduction errors remain separate unless a future
protocol defines a justified relationship.

## Admission gates

This context remains documentation-only until all of the following are satisfied:

1. one calculation-owned protocol closes every blocking row above;
2. the exact M2 rank-N definition is resolved and the already geometry-bound M0/M1N
   contracts are bound to admitted parameter inventories;
3. every compared operator has an explicit common state space, basis, gauge, energy
   unit, energy reference, geometry, and reciprocal-sample identity;
4. independent references, typed failure outcomes, and a bounded resource preflight are
   specified before observing protocol outcomes;
5. the visualization projection and authentication boundary are selected;
6. tests can name exact documentation and scientific behavior without invented expected
   values; and
7. a later execution request reports executable, input system, expected scale and
   outputs, anticipated runtime/resources, clean source identity, and receives separate
   human authorization.

Until then this root must contain no calculation, verification, rendering, scan, or
lifecycle script; no schema; no `analysis/`, `simulations/`, or `executions/` output tree;
and no generated JSON, figure, report result, or retained artifact.
