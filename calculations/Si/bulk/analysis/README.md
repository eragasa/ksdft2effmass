# Analysis

Analysis under this calculation root consumes only authenticated and independently
verified simulation records. It does not execute Quantum ESPRESSO or Wannier90 and does
not infer acceptance from successful process exit.

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
- The authorized no-calculator
  [`C6-B20-W21` revealed-408 development comparison](c6-b20-w21-revealed-408-development/)
  applies the unchanged 5% gap, 3% valley-position, and 8% per-mass targets. All six
  valley positions pass, but the indirect gap, all six longitudinal masses, and eleven
  of twelve transverse masses fail. These revealed-parent values are development-oracle
  labels that limit physical-fidelity claims; they do not block controlled reduction
  from the structurally eligible S30 operator. Reduction and diagnostic predictions
  must be frozen before the 402-point confirmation oracle is revealed.
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
- The separately authorized no-calculator
  [`C6-B20-W21` Slater--Koster definition and fit](c6-b20-w21-slater-koster-definition-fit/)
  stopped at its mandatory common-space gate. The projected ten-orbital `sp3s*` frame
  has resolved rank 9 at Gamma and one additional C6 point under the native-format
  singular-value bound. No fit ran and no parameter vector or Slater--Koster model was
  produced. S50 remains blocked pending a separate scientific decision. Stopping is the
  default; the current
  [post-S110 protocol](../research-protocol/controlled-reduction-protocol-post-s110.tex)
  orders separately authorized continuation levels by increasing implementation
  difficulty.
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
4. direct-parent/Wannier interpolation and operator comparison;
5. support-tail and locality analysis;
6. joint spectral/operator admissibility and minimum-cost selection; and
7. withheld and sensitivity analysis.

Each derived result requires its own schema, source bindings, verification, and
nonclaim statement before plotting or publication use.
