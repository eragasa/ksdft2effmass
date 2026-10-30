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
During migration, scientific experiment identities and protocols remain readable under
`experiments/`, while active calculation composition, outputs, and technical reports
live here. The target is complete migration of the tracked experiment tree into
distributed calculation owners under `calculations/`; `experiments/` is not a permanent
second maintained surface.

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
| [`wannier-gauge-locality-comparison/`](bulk-silicon/wannier-gauge-locality-comparison/README.md) | Planned | Prospective fixed-subspace silicon DFT–Wannier gauge/locality comparison with explicit state-space, operator, Nyquist-conversion, verification, and protected-execution boundaries; no admitted artifacts, implementation, execution, or result. |

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
| [`mathieu1d/`](mathieu1d/README.md) | Direct unsealed execution | `executions/direct-finite-reduction-n64/` owns the live typed calculation, byte-owning verification, authenticated two-figure rendering, and buildable technical report. Predecessor code and run artifacts are absent from the live tree. This does not establish material validation. |
| [`periodic1d/rank1/fourier-locality/`](periodic1d/rank1/fourier-locality/README.md) | Implemented direct lifecycle | Compatible scalar null control with exact-parent configuration, four-mesh analysis, immutable typed result, byte-owning independent verification, authenticated two-figure rendering, direct scripts, and a comprehensive upstream provisional technical report; no retained execution exists. |
| [`periodic1d/rank2/band-equivalence-versus-hopping-locality/`](periodic1d/rank2/band-equivalence-versus-hopping-locality/README.md) | Calculation-owned development family | Active synthetic four-state periodic parent, rank-two retained representation, smooth band-equivalent rotation, and hopping-locality analysis intended for the Ragasa2026a v3 calculation. The experiment donor was removed after exact-manifest review; no retained successor run exists. |
| [`periodic1d/rank2/composite-band-alignment-locality/`](periodic1d/rank2/composite-band-alignment-locality/README.md) | Implemented direct lifecycle | Exact-parent rank-two configuration, pure analysis, immutable typed result, byte-owning independent verification, authenticated two-figure rendering, direct scripts, exact M2/monograph donor crosswalks, and a comprehensive upstream provisional technical report; no retained successor execution exists. |
| [`periodic1d/rankN/composite-band-alignment-locality/`](periodic1d/rankN/composite-band-alignment-locality/README.md) | Schema-free development calculation | Finite retained-rank ladder `3, 4, 8, 16`, rotation-depth ladder, alignment controls, analytic qualification, and replaceable summary; no strict full-result verifier or retained run. |
| [`periodic2d/rank2/orthogonal/band-equivalence-locality/`](periodic2d/rank2/orthogonal/band-equivalence-locality/README.md) | Development calculation | Square-lattice rank-two band-equivalence, locality, and bounded mesh-refinement controls for Ragasa2026b. |
| [`periodic2d/rank2/nonorthogonal/band-equivalence-locality/`](periodic2d/rank2/nonorthogonal/band-equivalence-locality/README.md) | Development calculation | Triangular-Bravais/honeycomb-basis rank-two controlled family; not graphene validation. |
| [`periodic3d/rank2/orthogonal/band-equivalence-locality/`](periodic3d/rank2/orthogonal/band-equivalence-locality/README.md) | Development calculation | Simple-cubic rank-two band-equivalence, locality, and bounded mesh-refinement controls. |
| [`periodic3d/rank2/nonorthogonal/band-equivalence-locality/`](periodic3d/rank2/nonorthogonal/band-equivalence-locality/README.md) | Development calculation | FCC-Bravais/diamond-basis rank-two controlled family; not a silicon calculation. |
| [`periodic2d/rank2/strain-locality/`](periodic2d/rank2/strain-locality/README.md) | Development calculation | Area-preserving rhombic synthetic-strain M0/M1/M2 and scan controls. |
| [`periodic2d/rank1/hopping-shell-hierarchy/`](periodic2d/rank1/hopping-shell-hierarchy/README.md) | Prospective calculation design | Complete seven-file experiment design migrated to the calculation owner; no implementation, execution, or result. |
| [`periodic3d/rank2/strain-locality/`](periodic3d/rank2/strain-locality/README.md) | Development calculation | Volume-preserving Bain-path synthetic-strain M0/M1/M2 and scan controls. |
| [`periodic3d/rank1/anisotropic-hopping-support-hierarchy/`](periodic3d/rank1/anisotropic-hopping-support-hierarchy/README.md) | Preserved proposal design | Complete three-file proposal migrated to the calculation owner; implementation remains sequence-gated and absent. |
| [`band-equivalence-dimensional-comparison/`](band-equivalence-dimensional-comparison/README.md) | Development analysis | Cross-family tolerance and shell--scale comparison without transferring family identity. |

### Canonical-infrastructure integration workplan

This subsection is the repository-level roll-up for periodic calculation migration. It
covers every maintained periodic experiment family in
[`experiments/`](../experiments/README.md), the cross-family comparison composition, the
current calculation roots, and the removed historical packages that still contain
scientific or provenance-bearing design input. Migration state is deliberately
distributed: each maintained calculation owner keeps its complete local inventory in
its own `README.md` and its actionable `- [ ]` ledger in a neighboring `migration.md`.
Every tracked file under `experiments/` maps to exactly one family-local calculation
owner or to the shared periodic-program owner; no migration checklist remains
experiment-owned. Aggregation pages link those ledgers; they do not replace them with a
central checklist. This roll-up is a navigation and coverage audit,
not an instruction to combine scientifically distinct families or rewrite retained
bytes.

A migrated calculation will use the direct package lifecycle defined by the
[Architecture v3 calculation contract](../docs/architecture/v3/calculations/implementation.md):
a calculation-family identity; immutable execution identities; typed result bytes;
verification that owns the exact subject bytes and uses an independent reconstruction
route; authenticated rendering; and separate sealing and read-only package
verification. Reusable behavior belongs under `python/src/ksdft2effmass/`; calculation
roots retain only explicit scientific composition, effects, reports, and execution
artifacts. Concrete scientific configurations, results, analyzers, verifier
inventories, and figure inventories remain family-owned. Migration must not add a
generic Workflow, compatibility facade, empty marker base, or universal periodic
layout beyond behavior that is actually identical.

#### Maintained experiment inventory

The table includes architecture-selected families whose source directory does not yet
exist. Those rows are inventory only: no placeholder calculation root or stage script
is to be created before the model, protocol, and input/output contracts exist.

| Experiment or composition | Experiment-tree migration source | Calculation-side owner | Integration disposition |
|---|---|---|---|
| Periodic-1D single-band Fourier reduction | Historical 65-file donor formerly at `experiments/periodic-reduction/single-band-fourier-reduction/`, removed after exact-manifest review and separately authorized; recoverable from `c73aa96077ee03e1f7438ecbb44349b445a3eec8` | [`mathieu1d/`](mathieu1d/README.md), direct typed lifecycle and unsealed execution | The [65-file crosswalk](mathieu1d/experiment-migration-crosswalk.md) is closed. All predecessor run artifacts were subsequently deleted; publication consumers use only the direct execution, and the repository Python project is the sole live dependency authority. |
| Periodic-1D composite-band alignment and locality | Migrated from `experiments/periodic-reduction/composite-band-alignment-and-locality/` | [`periodic1d/rank2/composite-band-alignment-locality/`](periodic1d/rank2/composite-band-alignment-locality/README.md) | The complete three-file protocol now resides with its distinct calculation owner. Reuse reviewed operations without treating the model-adequacy rank-two family as the same experiment. |
| Periodic-1D higher-rank basis rotations and hopping range | Historical five-file donor removed after exact-hash review; migration and recovery details are recorded in the calculation-side [crosswalk](periodic1d/rankN/composite-band-alignment-locality/experiment-migration-crosswalk.md) | [`periodic1d/rankN/composite-band-alignment-locality/`](periodic1d/rankN/composite-band-alignment-locality/README.md) | Move reusable code to reviewed source owners; define stable typed inputs and results; independently check the full result; authenticate plotted values; and add direct calculation, verification, and rendering scripts. Keep moving-subspace, complex-rotation, 2-D, and 3-D studies separate. |
| Periodic-1D band equivalence versus hopping locality | Historical donor removed; exact migration and recovery provenance is recorded in the calculation-side [crosswalk](periodic1d/rank2/band-equivalence-versus-hopping-locality/experiment-migration-crosswalk.md) | [`periodic1d/rank2/band-equivalence-versus-hopping-locality/`](periodic1d/rank2/band-equivalence-versus-hopping-locality/README.md) | Extract reusable behavior from calculation-local `workflow/` into cohesive source owners; complete direct calculate → independently verify → render stages. The flat rule is direct, the nonflat claim is pointwise, adaptive refinement remains reserved, and no retained execution is authorized. |
| Periodic-2D orthogonal band equivalence versus hopping locality | [`experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/`](../experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/) | [`periodic2d/rank2/orthogonal/band-equivalence-locality/`](periodic2d/rank2/orthogonal/band-equivalence-locality/README.md) | Replace development-only scripts and loose artifacts with typed family-owned composition, independent verification, authenticated plots, and execution directories while preserving the three mesh roles and their current non-convergence status. |
| Periodic-2D nonorthogonal band equivalence versus hopping locality | [`experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/`](../experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/) | [`periodic2d/rank2/nonorthogonal/band-equivalence-locality/`](periodic2d/rank2/nonorthogonal/band-equivalence-locality/README.md) | Apply the same lifecycle mechanics as the orthogonal family, but retain its triangular-Bravais/honeycomb-basis conventions, pointwise shell-decision change, and non-material claim boundary. |
| Periodic-3D orthogonal band equivalence versus hopping locality | [`experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/`](../experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/) | [`periodic3d/rank2/orthogonal/band-equivalence-locality/`](periodic3d/rank2/orthogonal/band-equivalence-locality/README.md) | Migrate the simple-cubic rank-two development calculation to the direct lifecycle without conflating spatial dimension with retained rank or promoting bounded refinement to convergence. |
| Periodic-3D nonorthogonal band equivalence versus hopping locality | [`experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/`](../experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/) | [`periodic3d/rank2/nonorthogonal/band-equivalence-locality/`](periodic3d/rank2/nonorthogonal/band-equivalence-locality/README.md) | Migrate the FCC-Bravais/diamond-basis controlled family independently; retain the explicit boundary that it is not a silicon calculation. |
| Periodic-2D gauge locality under synthetic strain | [`experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/`](../experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/) | [`periodic2d/rank2/strain-locality/`](periodic2d/rank2/strain-locality/README.md) | Represent M0, M1, M2, and scan outputs as explicit typed channels with independent checks and authenticated figures. Preserve the unit-area path and do not recast it as elastic or material strain. |
| Periodic-3D gauge locality under synthetic strain | [`experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/`](../experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/) | [`periodic3d/rank2/strain-locality/`](periodic3d/rank2/strain-locality/README.md) | Represent M0, M1, M2, and scan outputs as explicit typed channels while preserving the unit-volume Bain-path and non-material boundary. |
| Periodic-2D hopping-shell hierarchy | Migrated from `experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/` | [`periodic2d/rank1/hopping-shell-hierarchy/`](periodic2d/rank1/hopping-shell-hierarchy/README.md) | Protocol/design bytes now reside with the calculation owner. HSH-1 remains a provenance-design donor; certificate/schema decisions remain open and no result exists. |
| Periodic-3D isotropic hopping-support hierarchy | [Architecture-only owner](../docs/architecture/v2/experiments/model-adequacy/periodic3d/isotropic-hopping-support-hierarchy/index.md) | No source or calculation directory | Keep as an explicit deferred family. Define its parent and exact protocol before any filesystem or implementation work. |
| Periodic-2D anisotropic hopping-support hierarchy | [Architecture-only owner](../docs/architecture/v2/experiments/model-adequacy/periodic2d/anisotropic-hopping-support-hierarchy/index.md) | No source or calculation directory | Keep as an explicit deferred anisotropy-isolation family; it must not inherit results or thresholds from isotropic or 3-D work. |
| Periodic-3D anisotropic hopping-support hierarchy | Migrated from `experiments/model-adequacy/periodic3d/anisotropic-hopping-support-hierarchy/` | [`periodic3d/rank1/anisotropic-hopping-support-hierarchy/`](periodic3d/rank1/anisotropic-hopping-support-hierarchy/README.md) | The complete three-file proposal now resides with the calculation owner as design input only. Implementation remains prerequisite- and threshold-gated. |
| Cross-dimensional band-equivalence comparison | [`experiments/model-adequacy/band-equivalence-dimensional-comparison/`](../experiments/model-adequacy/band-equivalence-dimensional-comparison/) | [`band-equivalence-dimensional-comparison/`](band-equivalence-dimensional-comparison/README.md) | Keep this as a composition over authenticated family results, not a fifth physical family. Replace calculation-local schema/serialization machinery with canonical typed records and independently verify every aggregate projection and source digest. |

#### Historical and legacy donor inventory

Commit `6c17150bce8bf339e9c818453a0ef0572d34e17a` removed superseded
calculation trees. Their last complete parent tree is
`c5d34a93b4710a4a430738c404c775865d418d42`. The paths below are therefore Git
history locators, not live links and not proposed directories to restore wholesale.
Integration means recording an exact path/revision/hash crosswalk and carrying forward
only still-authoritative scientific definitions or independently useful verification
routes. It does not mean copying old files, relabeling old outputs, or presenting
separate historical artifacts as one atomic execution.

| Historical locator at `c5d34a93b4710a4a430738c404c775865d418d42` | Scientific content to account for | Required disposition |
|---|---|---|
| `calculations/ICMSEP2026/conference/paper_1/` | Direct one-dimensional scalar admissible-set demonstration | Crosswalk the exact witness/separation controls to the maintained periodic-1D admissible-set source owner. Preserve the historical package identity; any successor is a separate calculation and execution. |
| `.../isolated-band/` (M1) | Plane-wave and finite-difference refinement, Fourier reconstruction, truncation, direct fitting, and withheld evaluation | Use as a method, verifier, and tolerance donor for a canonical isolated-band calculation; do not merge its identity with Mathieu1D or the compatible rank-one null control. |
| `.../multiband-alignment/` (M2) | Four-state parent, rank-two retained space, gauge attack, alignment channels, matrix hoppings, and withheld diagnostics | Crosswalk to the periodic-1D composite and model-adequacy rank-two successors while retaining which controls and outputs belonged to M2. |
| `.../constrained-admissible-sets/` (M3) | Finite parameter-and-alignment family, complete witness, separation certificate, and amendment chain | Preserve the M2 input dependency and the full amendment/checksum history. Treat constrained admissibility as its own calculation family rather than a verification flag on M2. |
| `.../constrained-admissible-sets-threshold-sensitivity/` | Post-hoc operator-threshold sensitivity derived from M3 | Integrate only as an authenticated derived analysis of one exact M3 result; it remains post hoc and cannot choose prospective thresholds. |
| `.../two-dimensional-common-space/` (M4) | Draft nonorthogonal plane-wave/finite-difference common-space protocol and square regression controls | Retain as an unexecuted design donor. Resolve the nonorthogonal comparator and strict wire contracts before creating a 2-D calculation package. |
| `.../hopping-shell-hierarchy/` (HSH-1) | Draft nested-support experiment and unresolved certificate design | Crosswalk into the maintained periodic-2D hopping-shell protocol without implying protocol freeze, execution, or a result. |
| `.../silicon-wannier-kinetic-preview/` | Read-only Wannier90 silicon-tutorial extraction | Route to the [`Si/bulk/`](Si/bulk/README.md) material-facing program. It is a correlation donor, not controlled-periodic evidence and not production silicon validation. |
| `calculations/research-monograph/periodic-1d/` | Isolated-band nominal and stress studies; rank-two composite alignment/locality; failed, diagnosed, and converged Wannier90 attempts | Split the channels into explicit successor dependencies. Preserve the exact historical result bytes and failed attempts; keep external-code execution separate from synthetic in-process calculations. |
| `calculations/research-monograph/periodic-2d/` | Scalar and rank-three composite reduction, topology controls and phase sweeps, Wannier90 failure/balanced comparison, and a bounded Wannier90 parameter study | Inventory each channel as a distinct typed calculation or derived analysis. Do not collapse topology, localization, common-space reduction, and optimizer behavior into one result wire. |
| `calculations/research-monograph/periodic-2d-optimizer-basin/` | Wannier90 multi-start execution, reanalysis, standalone continuation, common-estimator checks, and censored convergence regression | Preserve execution outcomes, including nonconverged endpoints, as historical evidence. Any successor must retain dependency digests between execution, extraction, reanalysis, and regression and requires separate authorization for external execution. |
| Historical execution-time `experiments/periodic-reduction/periodic1d/single-band-fourier-reduction/` | Removed predecessor source path | No live manifest consumes this path. Recovery is confined to the Mathieu1D migration and retirement ledgers. |

#### Nested channel and donor-surface inventory

The parent rows above are not sufficient migration units. A nested surface is any child
channel or package that owns a distinct scientific role, result wire, verification
route, dependency edge, execution outcome, or provenance contract. Each surface below
requires its own crosswalk row before its parent can be considered integrated.

| Parent surface | Nested surfaces that must remain distinguishable |
|---|---|
| Mathieu1D single-band reduction | The direct `ksdft2effmass.model_systems.mathieu1d` lifecycle; the retained unsealed direct execution with typed result, byte-owning verification, two authenticated figures, and technical report; and compact Git recovery records for removed donor, calculation-local, installed `study/`, run, and schema-v1 predecessors. No predecessor run wire, input, or JSON schema remains in the live tree. |
| Periodic-1D rank-two band equivalence/locality | Flat-parent baseline, nonflat four-state realization, parent-family robustness, truncation consequences, momentum refinement, amplitude resolution, hopping-tail/power diagnostics, scientific-story rendering, and their separate result and verification definitions. |
| Periodic-1D higher-rank alignment/locality | D1 P0/G0 parent construction, rank ladder, rotation-depth ladder, identity/global-unitary/pointwise-unitary/known-inverse-oracle gauge alignments, endpoint sewing, transport, case ledger, failure dispositions, numerical backend, and analytic-control verification. Future P1, G1, restricted-circuit, complex-unitary, moving-subspace, 2-D, and 3-D branches remain separate absent surfaces. |
| Each 2-D/3-D band-equivalence family | Nominal development calculation, first refinement, second refinement, independent family verification, development plotting, and the replaceable result/refinement directories. The four orthogonal/nonorthogonal dimensional families have parallel mechanics but separate scientific identities and thresholds. |
| Each 2-D/3-D strain family | M0 geometry/frozen-response channel, M1 four-state response channel, M2 prescribed radial-response channel, witness/qualification data, parameter scan, response rendering, scan rendering, and each channel's verification record. |
| Cross-dimensional comparison | Four family-specific request/result/refinement/verification schema sets; frame-transport diagnostics; tolerance comparison; shell--scale decision landscape request/result/verification; M0/M1/M2/witness strain documents; strain-scan request/result/verification; and the corresponding plot inventories. |
| Periodic-2D hopping-shell hierarchy | Orbit/support inventory, construction and evaluation sample roles, projection-and-loss definition, threshold design, conservative exclusion/support certificates, execution structure, and future result and verifier schemas. These design documents are not one frozen protocol. |
| Periodic-3D anisotropic hopping-support hierarchy | The preserved parent protocol and its disclosed exploratory threshold design. The threshold surface must not silently become a prospective acceptance rule. |
| ICMSEP parent and M1--M4/HSH packages | Parent scalar witness/separation; M1 parent refinement, Fourier reconstruction, truncation, direct-fit route, and withheld evaluation; M2 gauge/alignment/hopping channels; M3 configuration materialization, M2 correlation, protocol-freeze and amendment chain, producer verification, and standalone verification; M3 post-hoc threshold sensitivity; M4 square regression and prospective skew common-space cases; and HSH-1 design components. |
| Historical periodic-1D monograph package | Nominal isolated-band calculation, stress calculation, composite-band calculation, original Wannier90 preprocessing failure, bounded nonconverged attempts, diagnosis, preconditioned executions, extracted results, independent verification, and their separate figures/reports. |
| Historical periodic-2D monograph package | Scalar calculation, rank-three composite calculation and projected-gauge correction, three topological model controls, topological phase sweeps, initial Wannier90 failure, balanced inactive-embedding retry, bounded Wannier90 mesh/cutoff/embedding study, portable per-case study records, and native-evidence archive verification. |
| Historical periodic-2D optimizer-basin package | Original study input/execution/extraction/verification; offline reanalysis; standalone proposal and generated starts; bounded execution and resume; standalone extraction and verification; common-estimator inputs at three FFT sizes for four declared endpoints; censored convergence regression; two native-evidence archives; and the separate report/figure products. Nonconverged endpoints remain first-class outcomes. |
| Live historical campaign source | `campaigns/periodic_1d/run/{isolated,stress,composite,wannier90}` data, calculate, correlate, verify, native-artifact, and serialization subpackages; none is subsumed merely by naming the parent campaign directory. |
| Live periodic-2D source | `periodic2d/campaign/nbands_1`; `run/composite`; `run/topological` and `run/topological/phase_sweep`; `run/wannier90/balanced`; `run/wannier90/study`; and `run/wannier90/optimizer_basin/{reanalysis,standalone,convergence_regression}` data, calculate, correlate, and verify subpackages. Each channel retains its own dependency and evidence boundary. |
| Live periodic-1D calculation source | The direct `periodic1d/{fourier_locality,composite_band_alignment,admissible_sets}` lifecycles. The retired `isolated_band` and `multiband_alignment` packages are Git-recoverable only. The rank-two split, historical M2 identities, and final source-retirement inventory remain recorded in [`periodic1d/rank2/phase-3-split-audit.md`](periodic1d/rank2/phase-3-split-audit.md) and [`periodic1d/rank2/composite-band-alignment-locality/legacy-retirement.md`](periodic1d/rank2/composite-band-alignment-locality/legacy-retirement.md). |

Nested development outputs are not promoted by enumeration. Nested historical outputs
remain recoverable evidence only at their exact revision and path. A successor may
compose several authenticated child results, but it must record their individual wire
digests and cannot replace them with one digest of a reconstructed aggregate.

#### Implementation surfaces to reconcile

The migration must assign each behavior and every tracked experiment file one
calculation-side owner before changing imports or paths. At baseline, `experiments/`
contains 197 tracked files: 193 map to family calculation owners and four shared files
map to [`periodic/multiband/`](periodic/multiband/README.md). The current implementation
surfaces are:

- reusable periodic primitives and records under `python/src/ksdft2effmass/periodic/`,
  `periodic1d/`, and `periodic2d/`;
- historical monograph campaign composition under
  `python/src/ksdft2effmass/campaigns/periodic_1d/`;
- finite model constructors under `python/src/ksdft2effmass/model_systems/periodic_1d/`
  and `model_systems/periodic2d/`;
- reusable band-equivalence, Fourier, alignment, geometry, support, refinement, and
  strain behavior under
  `python/src/ksdft2effmass/analysis/model_adequacy/band_equivalence_locality/`;
- calculation-local implementations under
  `periodic1d/rank2/band-equivalence-versus-hopping-locality/workflow/`,
  `periodic1d/rankN/composite-band-alignment-locality/workflow/`, and
  `band-equivalence-dimensional-comparison/band_equivalence_workflow/`; and
- mutable composition and plotting scripts under `experiments/` and the dimensioned
  calculation roots.

The intended direction is from calculation composition to one reviewed source owner,
never from the installed package back into `calculations/` or `experiments/`. The former
Mathieu1D calculation-local source copy has been removed; maintained code imports only
the reviewed source owner.

Migration ledgers follow ownership rather than dimension. Each family-local
`migration.md` is authoritative for its checkboxes and must link every nested donor,
dependency, and retained execution named by the neighboring `README.md`. The
repository-level and multiband indexes may summarize status, but a checkbox is changed
only in the owning distributed ledger and only with the evidence named by that item.

#### Migration sequence

1. **Freeze the crosswalk.** For each family and every nested channel above, record
   exact live and historical paths, Git revisions, schemas, result digests,
   verification routes, dependency edges, publication consumers, and whether bytes are
   retained, replaceable development outputs, or design only. Parent-directory coverage
   is not sufficient evidence of nested-channel coverage.
2. **Define shared mechanics only.** Reuse canonical typed serialization, exact-byte
   verifier admission, aggregate verification, authenticated visualization, PNG
   validation, and atomic artifact publication where behavior is identical. Keep lattices,
   gauges, meshes, supports, tolerances, and scientific inventories concrete and
   family-owned.
3. **Close the one-dimensional scalar slice.** Mathieu1D direct replacement is complete;
   implement the compatible rank-one control, M1-related scientific questions, and
   scalar admissible-set study as distinct direct families rather than restoring any
   predecessor runtime.
4. **Close the one-dimensional multiband slice.** The separate rank-two composite-band
   direct lifecycle is implemented without retained execution. Finish the rank-two
   band-equivalence owner, migrate constrained admissibility away from M2, and then
   implement the higher-rank family. Each receives independent reconstruction and
   rendering before evidence retention is considered.
5. **Migrate the four dimensional rank-two families.** Establish typed parity for the
   2-D/3-D orthogonal and nonorthogonal calculations, preserve refinement roles, and
   generate fresh execution identities rather than rewriting development artifacts.
6. **Migrate derived strain and comparison work.** Make M0/M1/M2/scan dependencies
   explicit, then make the dimensional comparison consume only authenticated results
   with compatible units, norms, mesh roles, and evidence status.
7. **Implement support-hierarchy families in dependency order.** Complete periodic-2D
   isotropic hopping-shell work before the deferred 3-D isotropic and anisotropic
   families unless a separately reviewed protocol changes that dependency order.
8. **Separate monograph and external-code successors.** Migrate topological,
   common-space, Wannier90 comparison, optimizer-basin, and regression channels as
   distinct calculation/analysis packages. No production or new Wannier90 execution,
   remote computation, or evidence replacement is authorized by this plan.
9. **Retire duplicate mutable surfaces only after parity.** Require typed-wire parity,
   named numerical tolerances, independent-verifier parity, authenticated figure
   inventory parity, documentation updates, and an exact predecessor-recovery record.
   Deletion or replacement of retained or historical data remains separately
   authorized.

A family is integrated only when its authoritative protocol and owner are unambiguous,
its direct lifecycle can be run without importing a legacy calculation tree, its
verifier reconstructs decisive facts without invoking the producer, its figures consume
only authenticated data, and its documentation states basis, gauge, energy reference,
units, geometry, sampling roles, error classes, and evidence limitations. Software
checks establish these mechanics only; they do not establish convergence, scientific
validation, publication acceptance, sealing, release, or material validity.

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
