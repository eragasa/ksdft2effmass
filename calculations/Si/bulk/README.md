# Bulk-silicon parent qualification and reduction

This is the canonical publication-independent calculation owner for the prospective
bulk-silicon parent, Wannier bridge, and joint spectral/operator reduction used by
Paper D (`Ragasa2026d`). Paper D consumes this calculation; it does not own or rename
the calculation evidence.

## Status

**Planning and evidence aggregation; no accepted production parent.** A previously
executed direct bootstrap matrix contains nine SCF and nine linked diagnostic NSCF
invocations. Its compact records were audited successfully. Human disposition selected
C48/K8 (48/192 Ry and a shifted $8\times8\times8$ mesh) as provisional finite-setting
parameters, not as accepted production or infinite-setting values. The result does not
locate the conduction valley, establish effective-mass convergence, or validate a
silicon Hamiltonian.

The IEEE diagnosis classifies an external OpenCL-startup trap and a separate
cross-BLAS, cross-MPI `ZHEGVX` divide-by-zero during initial-wavefunction
subspace diagonalization. Its effect on retained observables and the origins of the
remaining reported IEEE classes are unresolved. The successor
[provisional-use disposition](provisional-use-disposition.md) permits explicitly
labelled downstream development and exploratory analysis while retaining these limits.
Production and publication-grade acceptance remain pending, and this directory
authorizes no additional Quantum ESPRESSO or Wannier90 execution.

## Ownership boundary

This root owns the forward-looking scientific plan, source crosswalk, verified-input
analysis boundary, and calculation-facing technical report. It does not copy or mutate
historical records. Those remain at their provenance-bound locations:

- [`calculations/bulk-silicon/`](../../bulk-silicon/) — reference snapshots, tutorial
  reproductions, smoke comparisons, and the provisional direct convergence bootstrap;
- [`calculations/ICMSEP2026/conference/paper_1/silicon-wannier-kinetic-preview/`](../../ICMSEP2026/conference/paper_1/silicon-wannier-kinetic-preview/)
  — tutorial-scale Wannier90 extraction, excluded from production admissible sets.

Reusable calculator, unit, operator, and analysis contracts remain with their installed
library owners. Workflow integration is intentionally outside this extraction.

## Contents

- [`development-plan.md`](development-plan.md) — gated calculation sequence from the
  audited bootstrap through a retained joint-fidelity result.
- [`provisional-use-disposition.md`](provisional-use-disposition.md) — successor
  decision permitting labelled downstream development without accepting a production
  parent or authorizing new calculator execution.
- [`evidence-crosswalk.md`](evidence-crosswalk.md) — exact predecessor locations,
  evidence classes, permitted uses, and non-transfer rules.
- [`simulations/`](simulations/) — future simulation and experiment-verification
  boundary; currently contains no runnable production stage.
- [`analysis/`](analysis/) — verified-input analysis boundary, current supportable
  conclusions, and the calculation-local
  [Vogl 1983 LCAO `sp3s*` control](analysis/controls/vogl-sp3s-star/).
- [`technical-report/`](technical-report/) — calculation-facing synthesis and links to
  the detailed design and retained audits.

## Nonclaims

This root does not establish production convergence, an infinite-basis result,
experimental agreement, pseudopotential transferability, a qualified Wannier model,
an adequate tight-binding model, or scientific validation. It authorizes no protected
execution, evidence promotion, publication, or release.
