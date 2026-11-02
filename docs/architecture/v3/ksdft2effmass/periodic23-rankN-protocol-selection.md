# Periodic-2D and periodic-3D rank-N protocol-selection boundary

## Status and claim boundary

This document defines the decisions required before periodic-2D or periodic-3D
arbitrary-finite-rank software can be installed. It is not a selected scientific
protocol, implementation plan, calculated result, numerical verification, retained
execution, sealing decision, or publication claim.

The two dimensional protocols are separate. A decision made for periodic-2D does not
select the corresponding periodic-3D decision, and neither protocol may be inferred by
copying the periodic-1D implementation.

## Existing authority

The prospective Ragasa2026c program supplies only the following common constraints:

- the study is a topologically trivial synthetic baseline; an obstructed or topological
  family belongs to a separately reviewed study;
- the shared cross-dimensional retained-rank subset is `3`, `4`, and `8`;
- the shared cross-dimensional circuit-depth subset is `1`, `2`, and `4`;
- cross-rank matrix quantities retain raw values and the declared
  \(\sqrt{r}E_{\mathrm{norm}}\) or \(rE_{\mathrm{norm}}^2\) normalization as applicable;
- ordered-spectrum errors use the declared common energy scale and aligned represented
  state space; and
- projection, disentanglement, basis transformation, gauge restriction, Fourier
  interpolation, support truncation, and total error remain separate operations.

These constraints do **not** select a higher-dimensional parent Hamiltonian, gauge
attack, reciprocal mesh, transport topology, metric-shell inventory, tolerance, or
evidence lifecycle. Rank four is one admitted value of a rank-N request; it does not
create a `rank4` namespace.

## Rank-two-derived realization recommendation

“Rank-N” should realize the same **scientific role decomposition and lifecycle shape** as
the corresponding rank-two family, with rank-dependent mathematics generalized
explicitly. It does not mean subclassing rank-two classes or changing a shape check from
`2` to `r` without review.

For each dimension, the recommended realization is:

- retain the rank-two family partition and exact PhysKit lattice/metric identities;
- retain separate aggregate request, analysis, result, independent reference,
  verification, visualization-data, visualizer, execution, execution-verification, and
  rendering owners;
- retain separate global gauge alignment, pointwise Procrustes, frame transport,
  hopping locality, and irreversible support-truncation capabilities;
- add `retained_rank` as an explicit invariant and admit the selected study values
  `3`, `4`, and `8`, while reusable lower-level actions may admit any reviewed finite
  rank greater than two;
- replace every rank-two matrix-shape, normalization, rank-threshold, closure-spectrum,
  and serialization assumption with an explicit rank-dependent contract;
- retain the rank-two lattice cases, bond inventories, metric-shell definitions, and
  lifecycle ordering as prospective controls, subject to rank-N refinement and resource
  qualification before execution; and
- preserve independent periodic-2D and periodic-3D evidence identities even when their
  public class-role inventories mirror one another.

The rank-two restricted real-rotation action is not mechanically promoted to rank-N.
Its rank-N counterpart must be an explicitly selected global alignment family. The
recommended baseline is complete global unitary Procrustes, pointwise unitary
Procrustes, and a separately labelled known-inverse construction oracle when the chosen
gauge circuit provides one. Restricted-circuit fitting remains absent until an optimizer
and certificate policy are selected.

The aggregate synthetic parent requires a reviewed rank-dependent definition. The
recommended structural generalization is an ambient `2 * retained_rank` parent with an
explicit rank-dimensional retained seed and separated retained/exterior sectors. Exact
analytic candidates for the parent, gauge circuit, case inventories, meshes, and shell
controls are calculation-owned in
`calculations/periodic2d/rankN/recommended-baseline.md` and
`calculations/periodic3d/rankN/recommended-baseline.md`; the hard-coded four-state
rank-two definition is not widened in place.

The calculation-owned periodic-2D and periodic-3D protocols now select one common
Procrustes software policy: the Project Koios `MAXIMUM` numerical-rank cutoff rule,
rank components `1e-12` absolute and `1e-10` relative, and backend-validation components
`1e-12` absolute and `1e-10` relative. This explicit cross-dimensional selection does
not transfer periodic-1D qualification evidence and does not establish convergence or a
scientific overlap threshold.

## Decisions required independently for each dimension

Each dimension must obtain scientific review of one closed protocol that selects all of
the following.

| Decision | Required declaration | Forbidden inference |
|---|---|---|
| Study identity | Exact calculation family, case identifiers, retained ranks, depths, and claim boundary | Relabeling periodic-1D or rank-two cases |
| Parent model | Analytic operator, ambient and retained spaces, isolation assumptions, units, basis, energy zero, and `norm_energy_scale` | Reusing one-dimensional coefficients or a material interpretation |
| Lattice geometry | Exact PhysKit direct lattice, reciprocal convention, metric, and basis offsets when present | Treating integer translations as physical distances |
| Gauge class | Exact `SO(r)` or `U(r)` family, right/left action, inner product, generator inventory, depth semantics, and known inverse if an oracle is retained | Assuming the periodic-1D real circuit or rank-two restricted rotation |
| Representation alignment | State-space identification, global and pointwise alignment applicability, numerical-rank policy, degeneracy policy, and failure outcomes | Treating SVD singular vectors as canonical or physical |
| Reciprocal sampling | Construction meshes, offsets, endpoint sewing, withheld evaluation inventory, and refinement relation | Copying odd one-dimensional meshes or scalar Nyquist rules |
| Frame transport | Neighbor graph, primitive cycles, closure observables, plaquette or cell observables, topology applicability, and rank-deficient behavior | Mechanical extension of one-dimensional closed-loop transport |
| Fourier conversion | Tensor transform convention, displacement inventory, Hermitian pairing, self-inverse mode handling, and Parseval diagnostics | Assuming one-dimensional support or Nyquist disposition |
| Locality diagnostics | Raw and normalized block powers, onsite/nononsite partition, physical-metric classification, and diagnostic range inventory | Conflating unchanged hopping diagnostics with truncation |
| Support truncation | Complete conjugate-closed metric shells, shell cap or complete ladder, irreversible removal rule, and unresolved outcomes | Splitting equal-metric shells or using translation-index distance |
| Error channels | Interpolation, truncation, total, operator, ordered-spectrum, parent-model, and numerical errors with explicit operands | Combining errors without a selected relation |
| Independent references | Analytic or direct-sum routes for parent, alignment, transport, Fourier, locality, and support decisions | Calling producer recomputation independent |
| Numerical gates | Absolute/relative tolerances, strict versus inclusive comparisons, overflow behavior, refinement gates, and effect-resolution floor | Importing periodic-1D or rank-two tolerances post hoc |
| Lifecycle | Typed request/result schemas, provenance inventory, verification admission, rendering inventory, evidence status, resource bounds, and no-overwrite execution identity | Treating passing software tests as scientific validation |

## Dimension-specific topology declarations

The periodic-2D protocol must explicitly select two primitive neighbor directions,
primitive-cycle closure handling, and the disposition of the single primitive-axis-pair
plaquette family. The periodic-3D protocol must explicitly select three primitive
neighbor directions, closure handling for each primitive direction, the disposition of
all three primitive-axis-pair plaquette families, and whether an additional cell-level
consistency diagnostic is scientifically required. This document does not select those
dispositions.

## Admission gates before source implementation

No public periodic-2D or periodic-3D rank-N class or direct entrypoint is admitted until:

1. the applicable calculation-owned protocol selects every decision above;
2. its parent, gauge, topology, mesh, support, tolerance, and claim conventions are
   internally consistent and use authoritative PhysKit and Project Koios owners;
3. independent-reference routes and typed failure outcomes are specified;
4. the architecture review identifies which arithmetic remains common and which public
   contracts are dimension-owned;
5. tests can name exact behavior without synthetic expected values being presented as
   scientific evidence; and
6. any execution request separately satisfies clean-revision, no-overwrite, provenance,
   resource-reporting, and explicit human-authorization requirements.

The authorized implementation tranche installs dimension-qualified rank-N analytic
parent/gauge models, global and pointwise Procrustes, frame transport, hopping locality,
support truncation, typed aggregate requests, complete case-expansion owners, thin
aggregate analyzers, immutable per-case/per-alignment aggregate results, and bounded
producer-independent parent, alignment, transport, Fourier, shell-power, and
support-selection references and typed aggregate verification. Visualization and
lifecycle owners remain absent until their applicable gates pass. In particular, neither
dimension has selected the exact rank/depth/case/alignment visualization operands,
invariant reductions, authenticated plot inventory, or bounded rendering resource
envelope; these choices must not be inferred from rank two. The calculation roots remain
documentation-only and contain no direct entrypoints or evidence.
