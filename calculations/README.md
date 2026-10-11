# Calculation and experiment inventory

This directory contains retained calculation packages, controlled numerical
experiments, external-reference records, and unexecuted calculation plans. This
page is the repository-level index of those records.

The inventory is a navigation aid, not an acceptance record or execution
authorization. The linked protocol, result, report, verification, provenance,
and checksum files define each package's actual status and claim boundary.
Passing software or numerical checks does not by itself establish scientific
validation.

## Status terms

- **Calculated**: retained numerical outputs exist. This does not imply human
  acceptance, scientific validation, material validity, or exact replay.
- **Reference data**: retained data were obtained from an identified external
  source rather than calculated by this project.
- **Extraction**: compact records were copied or derived from an identified
  existing package without executing a new scientific calculator.
- **Planned**: a design or protocol exists, but the proposed calculation has not
  been executed.

## Bulk silicon

These records range from tutorial smoke tests to provisional production-setting
studies. They do not collectively constitute an accepted bulk-silicon parent.

| Package | Status | Scope and primary record |
|---|---|---|
| [`materials-project/`](bulk-silicon/materials-project/README.md) | Reference data | Materials Project `mp-149` silicon structure snapshot and catalog correlation; not a project calculation or production input. |
| [`qe-example01-si-scf-davidson/`](bulk-silicon/qe-example01-si-scf-davidson/result.md) | Calculated; human-accepted tutorial reproduction | One Quantum ESPRESSO 7.2 silicon Davidson SCF smoke test with compact provenance and externally retained native artifacts. |
| [`qe-example01-si-bands-davidson/`](bulk-silicon/qe-example01-si-bands-davidson/result.md) | Calculated; awaiting human review | One QE 7.2 tutorial band-path calculation; not an effective-mass, Wannier, tight-binding, or production dataset. |
| [`qe-7.5-si-scf-smoke-comparison/`](bulk-silicon/qe-7.5-si-scf-smoke-comparison/execution-comparison.json) | Calculated; not human-accepted | One QE 7.5 tutorial SCF smoke test and bounded mechanical comparison with the QE 7.2 record. |
| [`production-convergence-preflight/`](bulk-silicon/production-convergence-preflight/execution-result.md) | Calculated; provisional | Direct bootstrap study containing nine SCFs and nine linked NSCFs. It reports finite-setting observations but selects no production cutoff or mesh and is not accepted production convergence. |

The scientific preparation and gate structure for production work are maintained
under [`docs/computational/`](../docs/computational/index.md).

## ICMSEP 2026 Conference Paper 1

The parent and M1--M3 packages are controlled synthetic calculations. The
material-facing preview has a different evidence class, stated below. Draft
successors remain unexecuted.

| Package | Status | Scope and primary record |
|---|---|---|
| [`paper_1/`](ICMSEP2026/conference/paper_1/README.md) | Calculated | Direct one-dimensional scalar admissible-set demonstration with an exact common witness and a certified separated case. |
| [`isolated-band/`](ICMSEP2026/conference/paper_1/isolated-band/README.md) | Calculated; retained M1 | Controlled one-dimensional isolated-band reconstruction, truncation, fitting-route, and withheld-mesh study. |
| [`multiband-alignment/`](ICMSEP2026/conference/paper_1/multiband-alignment/README.md) | Calculated; retained M2 | Rank-two synthetic gauge alignment, matrix-valued hopping, locality, and withheld diagnostics. |
| [`constrained-admissible-sets/`](ICMSEP2026/conference/paper_1/constrained-admissible-sets/README.md) | Calculated; retained M3 | Finite parameter-and-alignment family with a complete witness and geometric separation certificate under frozen thresholds. |
| [`constrained-admissible-sets-threshold-sensitivity/`](ICMSEP2026/conference/paper_1/constrained-admissible-sets-threshold-sensitivity/README.md) | Calculated post-hoc analysis | Operator-threshold sensitivity reconstructed from the sealed M3 result; not prospective threshold calibration or uncertainty analysis. |
| [`two-dimensional-common-space/`](ICMSEP2026/conference/paper_1/two-dimensional-common-space/README.md) | Planned; draft M4 | Unfrozen and unexecuted protocol for transporting two-dimensional plane-wave and finite-difference Hamiltonians to a common finite state space. |
| [`hopping-shell-hierarchy/`](ICMSEP2026/conference/paper_1/hopping-shell-hierarchy/README.md) | Planned; draft HSH-1 | Unfrozen and unexecuted two-dimensional nested hopping-shell adequacy study. No result or certificate exists. |
| [`silicon-wannier-kinetic-preview/`](ICMSEP2026/conference/paper_1/silicon-wannier-kinetic-preview/README.md) | Extraction | Preliminary publication extraction from an external read-only analysis of the official Wannier90 silicon tutorial setting; not a production silicon calculation or validation result. |

## Research monograph

These packages provide illustrative calculations and synthetic software or
numerical-verification evidence for the monograph. Unless a package says
otherwise, they are not material calculations, scientific validation, or
uncertainty quantification.

| Package | Status | Included experiments and primary record |
|---|---|---|
| [`harmonic-oscillator/`](research-monograph/harmonic-oscillator/README.md) | Calculated | Finite common-space comparison of analytical, finite-difference, and ladder-operator harmonic-oscillator representations. |
| [`particle-in-box/`](research-monograph/particle-in-box/README.md) | Calculated | Core residual comparison plus grid convergence, higher-eigenpair, norm, and identifiability studies. |
| [`periodic-1d/`](research-monograph/periodic-1d/README.md) | Calculated | Isolated-band nominal and stress studies, composite-band gauge/locality study, and retained Wannier90 attempts and comparison. |
| [`periodic-2d/`](research-monograph/periodic-2d/README.md) | Calculated; human-accepted controlled exercise | Scalar and composite reductions, topology controls and phase sweeps, and bounded Wannier90 comparisons and parameter study. |
| [`periodic-2d-optimizer-basin/`](research-monograph/periodic-2d-optimizer-basin/README.md) | Calculated | Synthetic non-DFT optimizer-basin, convergence, continuation, common-estimator, and post-hoc censored-regression studies. |
| [`impurity-spin-spaces/`](research-monograph/impurity-spin-spaces/README.md) | Calculated; human-accepted bounded exercise | Explicit mappings and compatibility checks among spinless, spin-degenerate, collinear, and spinor finite state spaces. |
| [`impurity-defect-1d/`](research-monograph/impurity-defect-1d/README.md) | Calculated | Matched pristine--defect extraction with planted coordinate and energy-reference perturbations. |
| [`impurity-defect-1d-independent-route/`](research-monograph/impurity-defect-1d-independent-route/README.md) | Calculated | Direct real-space versus independently implemented Bloch-fiber defect-extraction routes and adverse controls. |
| [`impurity-defect-1d-blind-alignment/`](research-monograph/impurity-defect-1d-blind-alignment/README.md) | Calculated; human-accepted bounded exercise | Blind recovery of alignment and energy reference followed by post-hoc comparison with hidden authored values. |
| [`impurity-defect-1d-analytical-oracle/`](research-monograph/impurity-defect-1d-analytical-oracle/README.md) | Calculated | Finite-rank Bloch-resolvent oracle compared with an independently assembled site-space eigensolve. |
| [`impurity-defect-1d-continuum-refinement/`](research-monograph/impurity-defect-1d-continuum-refinement/README.md) | Calculated | Separate continuum-mesh, domain, lattice-supercell, lattice-scale, and defect-width refinement axes. |
| [`impurity-defect-2d/`](research-monograph/impurity-defect-2d/README.md) | Mixed staged record | Human-accepted calculated Stage A, Stage B, and accepted-parent Stage C synthetic packages; retained negative attempts and execution-free designs; later stages remain undesigned and unauthorized. |

The operational log under
[`research-monograph/campaigns/piab1d/`](research-monograph/campaigns/piab1d/)
is retained campaign-run material, not a separate self-contained experiment
package.

## How to use this inventory

1. Open the package `README.md` or linked primary record for its current status.
2. Read `protocol.md` before interpreting a numerical result.
3. Use `report.md` for the bounded human-readable findings where present.
4. Inspect provenance, source manifests, verification records, and
   `SHA256SUMS` before making reproducibility claims.
5. Treat proposed calculations as nonexistent results until they are separately
   frozen, authorized where required, executed, retained, and independently
   verified.

New calculation packages should be added here when their directory is created.
Changing this index must not rewrite or relabel sealed calculation artifacts.
