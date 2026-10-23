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
