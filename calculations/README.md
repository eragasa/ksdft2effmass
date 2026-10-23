# Calculation and experiment inventory

This directory contains retained and development calculation packages, controlled
numerical studies, external-reference records, and unexecuted calculation plans. This
page is the repository-level index of those records.

The inventory is a navigation aid, not an acceptance record or execution
authorization. The linked protocol, result, report, verification, provenance,
and checksum files define each package's actual status and claim boundary.
Passing software or numerical checks does not by itself establish scientific
validation.

## Code-ownership boundary

This tree is not a second Python library. Hash-bound producers, verifiers, and adapters
inside retained packages are preserved evidence bytes and must not be reformatted or
rewritten solely to follow the current package layout. New and unsealed work places
reusable implementation in `python/src/ksdft2effmass/`; filesystem entry points contain
only calculation-specific inputs, explicit composition, effects, verification,
artifact writing, and reports. Controlled model-system calculations such as PIAB1D and
QHO1D are consolidated here even when their outputs remain mutable development bytes.
Scientific experiment identities and protocols may remain under `experiments/`, while
active calculation composition, outputs, and technical reports live here.

A migration must distinguish byte-preserved retained evidence from an unsealed script.
For an unsealed script, callers move directly to the canonical library owner without a
compatibility facade. For retained evidence, the original bytes and their provenance
remain intact even when the current library has a cleaner implementation.

## Execution-package lifecycle

The repository-wide [calculation-package implementation
contract](../docs/architecture/v3/calculations/implementation.md) defines the target
package layout and the separate calculation, independent
verification, rendering, sealing, and read-only package-verification stages. New
pre-publication records use calculation-family and execution identities, not `.vN`
identities. A scientific publication version is assigned only when a publication-owned
manifest binds an exact sealed execution and evidence-package digest to a posted arXiv
revision.

Existing flat packages and historical `.vN` identities remain provenance. They are not
rewritten merely to adopt the target layout. Migration proceeds non-destructively until
historical calculation-data removal is explicitly authorized.

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

The canonical forward-looking calculation owner is [`Si/bulk/`](Si/bulk/README.md).
The older `bulk-silicon/` records retain their historical paths because embedded
provenance and checksum contracts are not rewritten by the ownership organization.
Neither location currently establishes an accepted bulk-silicon parent.

| Package | Status | Scope and primary record |
|---|---|---|
| [`Si/bulk/`](Si/bulk/README.md) | Planning and evidence aggregation | Publication-independent owner for bulk-parent qualification, prospective Wannier bridging, joint spectral/operator reduction, verified-input analysis, and the calculation-facing technical report; no production execution or result. |
| [`materials-project/`](bulk-silicon/materials-project/README.md) | Historical reference data | Materials Project `mp-149` silicon structure snapshot and catalog correlation; not a project calculation or production input. |
| [`qe-example01-si-scf-davidson/`](bulk-silicon/qe-example01-si-scf-davidson/result.md) | Historical calculated record; human-accepted tutorial reproduction | One Quantum ESPRESSO 7.2 silicon Davidson SCF smoke test with compact provenance and externally retained native artifacts. |
| [`qe-example01-si-bands-davidson/`](bulk-silicon/qe-example01-si-bands-davidson/result.md) | Historical calculated record; awaiting human review | One QE 7.2 tutorial band-path calculation; not an effective-mass, Wannier, tight-binding, or production dataset. |
| [`qe-7.5-si-scf-smoke-comparison/`](bulk-silicon/qe-7.5-si-scf-smoke-comparison/execution-comparison.json) | Historical calculated record; not human-accepted | One QE 7.5 tutorial SCF smoke test and bounded mechanical comparison with the QE 7.2 record. |
| [`production-convergence-preflight/`](bulk-silicon/production-convergence-preflight/execution-result.md) | Historical calculated record; provisional | Direct bootstrap study containing nine SCFs and nine linked NSCFs. It reports finite-setting observations but selects no production cutoff or mesh and is not accepted production convergence. |

The detailed scientific preparation and source audit remain under
[`docs/computational/`](../docs/computational/index.md) and are cross-linked from the
canonical calculation owner.

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

## Periodic model systems

These publication-independent packages retain controlled finite calculations organized
by dimension, model, and calculation type. Their stable family, version, run, and
evidence identities are not renamed by filesystem consolidation.

| Package | Status | Scope and primary record |
|---|---|---|
| [`periodic/multiband/`](periodic/multiband/README.md) | Planning and aggregation layer | Cross-dimensional and cross-rank map of periodic multiband calculation owners, salient source-linked results, comparability limits, and staged development gates; not an execution or evidence owner. |
| [`mathieu1d/`](mathieu1d/README.md) | Retained version | Immutable Mathieu1D single-band Fourier-reduction version `v1`, strict schemas, producer-independent verification, exact predecessor provenance, and content-addressed synthetic evidence; not material validation. |
| [`periodic1d/rank1/fourier-locality/`](periodic1d/rank1/fourier-locality/README.md) | Pre-execution design | Model-family-compatible scalar Fourier/locality null control for the periodic multiband rank ladder; no implemented model, run, or result. |
| [`periodic1d/rank2/band-equivalence-locality/`](periodic1d/rank2/band-equivalence-locality/README.md) | Migration-in-progress development calculation | Active synthetic four-state periodic parent, rank-two retained representation, smooth band-equivalent rotation, and hopping-locality analysis intended for the Ragasa2026a v3 calculation; no retained successor run exists. |
| [`periodic1d/rankN/composite-band-alignment-locality/`](periodic1d/rankN/composite-band-alignment-locality/README.md) | Schema-free development calculation | Finite retained-rank ladder `3, 4, 8, 16`, rotation-depth ladder, alignment controls, analytic qualification, and replaceable summary; no strict full-result verifier or retained run. |
| [`periodic2d/rank2/orthogonal/band-equivalence-locality/`](periodic2d/rank2/orthogonal/band-equivalence-locality/README.md) | Development calculation | Square-lattice rank-two band-equivalence, locality, and bounded mesh-refinement controls for Ragasa2026b. |
| [`periodic2d/rank2/nonorthogonal/band-equivalence-locality/`](periodic2d/rank2/nonorthogonal/band-equivalence-locality/README.md) | Development calculation | Triangular-Bravais/honeycomb-basis rank-two controlled family; not graphene validation. |
| [`periodic3d/rank2/orthogonal/band-equivalence-locality/`](periodic3d/rank2/orthogonal/band-equivalence-locality/README.md) | Development calculation | Simple-cubic rank-two band-equivalence, locality, and bounded mesh-refinement controls. |
| [`periodic3d/rank2/nonorthogonal/band-equivalence-locality/`](periodic3d/rank2/nonorthogonal/band-equivalence-locality/README.md) | Development calculation | FCC-Bravais/diamond-basis rank-two controlled family; not a silicon calculation. |
| [`periodic2d/rank2/strain-locality/`](periodic2d/rank2/strain-locality/README.md) | Development calculation | Area-preserving rhombic synthetic-strain M0/M1/M2 and scan controls. |
| [`periodic3d/rank2/strain-locality/`](periodic3d/rank2/strain-locality/README.md) | Development calculation | Volume-preserving Bain-path synthetic-strain M0/M1/M2 and scan controls. |
| [`band-equivalence-dimensional-comparison/`](band-equivalence-dimensional-comparison/README.md) | Development analysis | Cross-family tolerance and shell--scale comparison without transferring family identity. |

## Research monograph

These packages provide illustrative calculations and synthetic software or
numerical-verification evidence for the monograph. Unless a package says
otherwise, they are not material calculations, scientific validation, or
uncertainty quantification.

| Package | Status | Included experiments and primary record |
|---|---|---|
| [`harmonic-oscillator/`](research-monograph/harmonic-oscillator/README.md) | Calculated historical record | Original finite common-space comparison of analytical, finite-difference, and ladder-operator harmonic-oscillator representations; preserved with its historical provenance. |
| [`qho1d/`](qho1d/README.md) | Mutable development calculation | Canonical QHO1D spatial-truncation calculation, replaceable outputs, and calculation-owned technical report; not retained evidence. |
| [`piab1d/`](piab1d/README.md) | Calculated | Canonical PIAB1D spectral-reduction calculation: core residual comparison plus grid convergence, higher-eigenpair, norm, decomposition-identifiability studies, and technical report. |
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

The research monograph references the canonical top-level `calculations/piab1d/`
record rather than owning a duplicate particle-in-box calculation directory.

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
