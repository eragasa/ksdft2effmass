# Analysis

Analysis under this calculation root consumes authenticated simulation records. Most
publication-facing routes require independent verification; explicitly labeled
development analyses may instead retain authenticated producer checks without an
independent reconstruction. Analysis does not execute Quantum ESPRESSO or Wannier90 and
does not infer acceptance from successful process exit.

## Current admissible inputs

The only material-facing calculated predecessor is the audited direct bootstrap:

- [`direct-results-audit.md`](../../../bulk-silicon/production-convergence-preflight/direct-results-audit.md)
- [`finite-setting-analysis.json`](../../../bulk-silicon/production-convergence-preflight/finite-setting-analysis.json)
- [`direct-results-decision-packet.json`](../../../bulk-silicon/production-convergence-preflight/direct-results-decision-packet.json)
- [`direct-results-setting-disposition.json`](../../../bulk-silicon/production-convergence-preflight/direct-results-setting-disposition.json)

The audit found the compact primary matrix complete and internally consistent. Human
disposition selected C48/K8 (48/192 Ry and a shifted $8\times8\times8$ mesh) as a
provisional finite-setting parameter pair. The active
[provisional-use disposition](../provisional-use-disposition.md) permits labelled
downstream development and exploratory analysis. This is not an accepted production or
infinite-setting result; a cross-toolchain observable comparison and mixed cutoff--mesh
interaction check remain production-acceptance gates.

## Development controls

The [Vogl 1983 LCAO `sp3s*` control](controls/vogl-sp3s-star/) contains the accepted
16-compound, 13-parameter Table 1 transcription and an independently implemented
spinless ten-band Bloch Hamiltonian. Its calculation-local package is
`vogl1983_lcao_sp3sstar`.

This external empirical control tests basis ordering, phase conventions, Hermiticity,
reciprocal periodicity, band ordering, and later reduction machinery. It does not
qualify the production parent, a Wannier bridge, or the planned local-model hierarchy.

## Current supportable conclusions

- The no-calculator
  [construction-mesh adequacy recommendation](construction-mesh-adequacy-recommendation/)
  records the protocol-first `C6` successor: change only the Gamma-origin construction
  mesh from `4x4x4` to `6x6x6`, retain all other scientific and optimizer coordinates,
  and treat `C8` as conditional rather than automatic. `C12` is reserved as a bounded
  upper diagnostic after `C8`, not presumed mesh convergence. The package also freezes a
  disjoint 402-point, parent-informed but parent-value-unobserved confirmation geometry.
  Later exact authorizations produced the eligible 216-point, 20-band interface and
  provider-eligible rank-10 `C6-B20-W21` operator. The disjoint 402-point parent values
  remain unobserved.
- The no-calculator
  [`C6-B20-W21` full untruncated characterization](c6-b20-w21-untruncated-characterization/)
  verifies pair closure, real-space Hermiticity, format-aware source reconstruction,
  spectra, six Delta-family minima, curvature masses, and the complete locality curve.
  No spatial truncation was applied. The result is structurally verified and
  scientifically unassessed by S30 alone.
- The authorized post-hoc
  [`C6-B20-W21` two-tolerance Wannier-shell exploration](c6-b20-w21-tau1-tau2-posthoc-exploration/)
  maps uniform-408-point RMS and maximum spectral/operator threshold pairs directly
  over the 17 proper native Wigner--Seitz shell reductions. The full 383-representative
  source remains a zero-loss control and is excluded from reduced-family feasibility.
  H-shell-16 minimizes both primary losses with requirements approximately
  `(4.46e-4, 1.52e-3)` while retaining 371 representatives, so this literal truncation
  family shows no global spectral--operator conflict at its tightest proper reduction.
  The map is explicitly post hoc and does not establish prospective acceptance, parent
  fidelity, or Slater--Koster expressivity.
- The authorized post-hoc
  [`C6-B20-W21` refitted native-shell witness follow-on](c6-b20-w21-refitted-ws-shell-witness-posthoc/)
  adds one bounded nonnegative scale per retained complete Wigner--Seitz shell in the
  same rank-10 Wannier basis. The converged constructive witnesses form distinct
  spectral/operator tradeoff arcs rather than the literal deletion line. Refitting
  reduces the minimum observed support at several illustrative threshold pairs, for
  example from 135 to 79 representatives at `(0.1, 0.15)`. The bounded multistart search
  provides witnesses but no global infeasibility certificate, prospective threshold,
  parent-fidelity claim, or independent reconstruction.
- The authorized no-calculator
  [`C6-B20-W21` Wannier-only fidelity ladder](c6-b20-w21-wannier-only-fidelity-ladder/)
  freezes H-shell-05, H-shell-10, and H-shell-16 without refitting. Exact Parseval
  operator losses and independent `12^3`, `20^3`, and `32^3` interpolation meshes show
  that the fitted 408-point spectral/operator RMS values understate broader errors by
  factors of approximately `(2.51, 2.03)`, `(2.11, 1.84)`, and `(1.62, 1.25)`,
  respectively. Source-relative curvature remains especially demanding: the maximum
  principal-mass changes are approximately 67.7%, 53.2%, and 2.54%. This is a
  Wannier-source compression result, not DFT or silicon validation.
- The authorized no-calculator
  [`C6-B20-W21` comprehensive non-SOC band-edge analysis](c6-b20-w21-wannier-only-comprehensive-band-edge/)
  extends the same frozen models to full electron mass tensors, derived six-valley mass
  conventions, Gamma-valence cluster projectors and splittings, direct-gap symmetry
  checks, ordered-band bandwidths, and a degeneracy-aware three-band quadratic valence
  Hamiltonian. H-shell-05 and H-shell-10 split the source's approximately `0.02495 meV`
  Gamma cluster to about `102.2` and `54.8 meV`; H-shell-16 yields about `2.50 meV`.
  Their aligned valence-quadratic coefficient errors are approximately `9.54%`, `5.88%`,
  and `0.279%`, and maximum non-SOC curvature-channel mass changes are approximately
  `38.9%`, `19.7%`, and `4.53%`. Independently ordered hole-band Hessians are rejected
  as unstable at the degeneracy. These are source-relative scalar-relativistic
  multiband diagnostics, not physical SOC heavy-hole, light-hole, split-off, acceptor,
  transport, DFT-parent, or silicon-validation results.
- The independent no-calculator
  [`C6-B20-W21` numerical-convention audit](c6-b20-w21-independent-convention-audit/)
  recomputes the single- and six-valley DOS and equal-population conductivity-mass
  conventions from retained tensors without importing the silicon producers. The
  maximum formula-level difference is `6.22e-15`. It also retains a complete 216-record
  cyclic-to-ordinary ledger: 91 modes touching the negative Nyquist boundary are
  removed and the remaining 125 map identically, with FCC radii reproduced to
  `3.56e-15 angstrom`. This audit does not reconstruct the Hamiltonian fields, removed
  cyclic coefficients, valleys, Hessians, support errors, or band-edge results.
- The authorized producer-checked
  [`C6-B20-W21` gauge-alignment/locality analysis](c6-b20-w21-gauge-alignment-locality/)
  applies the Hamiltonian-only periodic-3D rank-N represented-field framework to that
  authenticated source. It retains a frozen internal gauge attack, four alignment
  channels, finite-cyclic conversion, complete physical-support curves, equal-attained-
  error projections, the revealed direct-parent overlay, and nine report figures. The
  maximum complete-spectrum attack difference is approximately `3.20e-14 eV`. The
  result is explicitly not independently reconstructed and is development evidence,
  not publication-qualified silicon validation.
- The authorized no-calculator
  [`C6-B20-W21` revealed-408 development comparison](c6-b20-w21-revealed-408-development/)
  applies the unchanged 5% gap, 3% valley-position, and 8% per-mass targets. All six
  valley positions pass, but the indirect gap, all six longitudinal masses, and eleven
  of twelve transverse masses fail. These revealed-parent values are development-oracle
  labels that limit physical-fidelity claims; they do not block controlled reduction
  from the structurally eligible S30 operator. They remain a separate evaluation overlay
  and may not calibrate diagnostics, select support, define frontiers, or tune fits.
- The authorized no-calculator
  [`C6-B20-W21` spatial-truncation design](c6-b20-w21-spatial-truncation-design/)
  freezes all 18 complete physical-radius shells from the onsite-only control through
  the 383-representative full-support control. It predeclares pair closure, tail bounds,
  full-to-truncated operator and spectrum differences, valley and mass changes relative
  to the full source, and monotone larger-shell envelopes. It selects no radius and
  consumes no 402-point parent values.
- The separately authorized no-calculator
  [`C6-B20-W21` spatial-truncation evaluation](c6-b20-w21-spatial-truncation-evaluation/)
  reports every frozen shell against the full source. Pair closure and Hermiticity pass
  for all masks; the full-support control is exact; and direct, spectral, valley,
  gap, curvature, and mass changes are retained without accepting a radius. The first
  three dispersive masks do not preserve all Delta identities, and the onsite-only
  control has explicitly undefined valley/mass observables.
- The separately authorized no-calculator
  [`C6-B20-W21` spatial-truncation disposition](c6-b20-w21-spatial-truncation-disposition/)
  retains the 383-representative full-support shell, so `H_T = H_W` and the selected
  spatial-truncation error is identically zero. No post-observation numeric threshold is
  created to accept a nontrivial shell, and parent numerical-convergence tolerances are
  not repurposed as reduction tolerances.
- The protocol-only
  [`C6-B20-W21` hopping-first Pareto synthesis contract](c6-b20-w21-hopping-pareto-synthesis/)
  binds S30/S90/S100/S105 and defines separate retained-cost frontiers for operator,
  ordered-spectrum, gap, valley, curvature, and mass metrics on the 408-point development
  inventory. Its calculation-owned action installs conservative interval classification
  and exact identity inspection. The original authorized identity/gap run is preserved,
  and one authorized portable v2 rerun retained
  `UNRESOLVED_DEVELOPMENT_EVALUATION`. It selects no support, preserves
  `H_T = H_W`, consumed no 402-point parent values, and reserves 108/108 for future
  Slater--Koster work. Required 408-point per-shell intervals remain unavailable.
- The separately authorized no-calculator
  [`C6-B20-W21` Slater--Koster definition and fit](c6-b20-w21-slater-koster-definition-fit/)
  stopped at its mandatory common-space gate. The projected ten-orbital `sp3s*` frame
  has resolved rank 9 at Gamma and one additional C6 point under the native-format
  singular-value bound. No fit ran and no parameter vector or Slater--Koster model was
  produced. The unretained CSD0/CSD1 producer is now incubated under
  [`../common_space/diagnostics/`](../common_space/diagnostics/); it is not an independent
  verification result. S50 remains blocked pending a separate scientific decision.
  Stopping is the default; the current
  [hopping-first post-S110 protocol](../research-protocol/controlled-reduction-protocol-hopping-first.tex)
  preserves the blocked result and requires the characterization-only Pareto synthesis
  before any separately authorized continuation fit.
- The
  [withheld-parent validation package](withheld-parent-validation-preflight/)
  froze 408 candidate-conditioned, construction-disjoint QE coordinates and exact
  intended-use criteria before one separately authorized NSCF invocation. The direct
  comparison completed: all valley-position targets were met, but the indirect-gap
  error, two longitudinal-mass errors, and all transverse-mass errors establish that the
  provider-eligible candidate is not adequate for the declared SSSP-pilot intended use.
- The execution-free
  [provider-eligible operator characterization](provider-eligible-operator-qualification/)
  verifies source reconstruction and records 1000-to-1290-step spectral sensitivity,
  valley predictions, curvature diagnostics, and the locality curve. Those candidate-only
  observations were not themselves failures; the later prospective direct-parent
  comparison supplies the intended-use disposition while leaving provider eligibility
  and structural validity unchanged.
- The execution-free
  [conduction-frozen gauge-sensitivity diagnostic](conduction-frozen-gauge-sensitivity/)
  finds that the blocked 500- and 1000-iteration operators agree at source points but
  differ substantially in between-mesh interpolation, conduction-edge location,
  curvature, and locality diagnostics. Neither operator is accepted, and further
  iteration-only extension is unsupported.
- The retained 9-SCF/9-NSCF direct matrix does not require rerun merely to reproduce it
  through a workflow harness.
- The observations are finite-setting numerical evidence only.
- The nominal `Delta_0.85` point is a reproducible diagnostic probe, not a located
  conduction minimum.
- Fixed-point band and gap changes do not establish effective-mass convergence.
- The IEEE diagnosis separates an external OpenCL-startup event from a later
  cross-BLAS, cross-MPI `ZHEGVX` divide-by-zero; observable effect and the remaining
  reported flag classes are unresolved.
- The provisional C48/K8 selection identifies the relevant mixed cutoff--mesh corner,
  but that successor calculation has neither been frozen nor authorized here.

## Future analysis stages

After verified successors exist, analysis may perform:

1. finite-setting selection and mixed-corner interaction assessment;
2. valley identity and projector/cluster tracking;
3. effective-mass stencil or fit analysis with conditioning diagnostics;
4. direct-parent/Wannier interpolation and aligned operator comparison where a common
   state space exists;
5. complete Fourier/hopping reconstruction before support removal, using C6 only for
   source reconstruction;
6. channel-specific descriptive Pareto analysis on the 408-point development inventory
   without scalarization or support selection;
7. complete-shell support-removal consequences while preserving S105's selected
   full-support disposition;
8. separate 408-parent evaluation overlays that cannot define or tune the internal
   analysis;
9. only then, a separately admitted Slater--Koster parameterization using its reserved
   108/108 split; and
10. confirmation-only 402-point comparison without frontier revision or refitting.

Each derived result requires its own schema, source bindings, declared producer-check
or verification status, and nonclaim statement before plotting or publication use.
