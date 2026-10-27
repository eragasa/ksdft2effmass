# Nested channel crosswalk

## Scope

This document assigns each maintained scientific or derived channel to its
calculation-local path, typed classes, wire/schema surface, effect adapter, and current
artifact inventory. It is an ownership crosswalk, not a claim that every channel already
has a retained direct lifecycle.

All paths are relative to this calculation owner. The implementation under `workflow/`
is calculation-local and is not an installed public API.

## Channel inventory

| Channel | Definition and producer ownership | Result and independent-check ownership | Wire and schema | Effect adapter and artifacts | Current limitation |
|---|---|---|---|---|---|
| Flat analytic point evaluation | `workflow/definition.py`: `SmoothBlochContinuumDefinition`; `workflow/experiment.py`: `SmoothBlochContinuumExperiment` | `workflow/results.py`: `SmoothBlochContinuumResult`, point and hopping-block records; `workflow/verify.py`: `SmoothBlochContinuumVerifier` and verification result | `SmoothBlochContinuumInputSerializer`, `SmoothBlochContinuumResultSerializer`, `SmoothBlochContinuumVerificationSerializer`; `workflow/schema_documents/smooth-continuum-{input,result,verification}.schema.json` | `run_flat_development.py`; `simulations/development/results/{hopping-power-map,selected-hopping-tails}.csv`; flat figure pair | Development entrypoint still combines calculation and tabulation; no retained execution identity. |
| Flat momentum refinement and analytic-amplitude diagnostic | `SmoothBlochContinuumConvergenceDefinition`, thresholds, and `SmoothBlochContinuumConvergenceExperiment` | `SmoothBlochContinuumConvergenceResult`, refinement records, disposition, and `SmoothBlochContinuumConvergenceVerifier` | Same strict flat serializers and schemas encode the aggregate definition/result/verification | `run_flat_development.py`; `momentum-refinement.csv`, `amplitude-resolution.csv`, and `band-equivalence-versus-hopping-locality.{pdf,png}` | The amplitude CSV records a rejected interpolant diagnostic; the active flat law is evaluated directly. |
| Nonflat pointwise four-state realization | `workflow/nonflat/definition.py`: `SmoothFourStateDefinition`; `workflow/nonflat/experiment.py`: `SmoothFourStateExperiment` | `workflow/nonflat/results.py`: `SmoothFourStateResult`, point and hopping-block records; `workflow/nonflat/verify.py`: `SmoothFourStateVerifier` and verification result | `SmoothFourStateInputSerializer`, `SmoothFourStateResultSerializer`, `SmoothFourStateVerificationSerializer`; `workflow/schema_documents/nonflat-{input,result,verification}.schema.json` | `run_nonflat_development.py`; `nonflat-continuum.csv`, hopping-power map, selected tails, and nonflat figure pair | Claims are pointwise at declared amplitudes; no continuous-amplitude reconstruction is claimed. |
| Nonflat momentum refinement | `SmoothFourStateConvergenceDefinition`, thresholds, and `SmoothFourStateConvergenceExperiment` | `SmoothFourStateConvergenceResult`, refinement records, and disposition; the entrypoint applies `SmoothFourStateVerifier` to produced mesh results | No separate aggregate convergence wire/schema beyond the strict point-result surfaces | `run_nonflat_development.py`; `nonflat-momentum-refinement.csv` | A retained lifecycle requires an explicit aggregate verification value and byte-owning wire admission. |
| Nonflat adaptive amplitude exploration | `SmoothFourStateAdaptiveAmplitudeDefinition`, amplitude thresholds, and `SmoothFourStateAdaptiveAmplitudeExperiment` | Adaptive result, level, and validation records in `workflow/nonflat/results.py` | No standalone adaptive wire or schema | `run_nonflat_development.py`; `nonflat-amplitude-resolution.csv` | Reserved for a future between-node claim; no such claim or frozen cap exists. |
| Parent-hopping homotopy | `SmoothFourStateParentFamilyDefinition` and `SmoothFourStateParentFamilyExperiment` | `SmoothFourStateParentFamilyResult` and `SmoothFourStateParentFamilyVerifier` | No dedicated parent-family wire/schema | `run_parent_family_development.py`; `parent-family-{continuum,summary}.csv`; parent-family and scientific-story figure pairs | Five sampled parent scales do not establish a continuous-parent certificate. |
| Dense ordinary-lattice truncation | `workflow/truncation/definition.py`: `SmoothFourStateTruncationDefinition`; `workflow/truncation/experiment.py`: `SmoothFourStateTruncationExperiment` | Truncation result, point, and range records; `SmoothFourStateTruncationVerifier`, verification result, and range-decision records | Strict truncation input/result/verification serializers; `workflow/schema_documents/truncation-{input,result,verification}.schema.json` | `run_truncation_development.py`; `truncation-{consequences,summary}.csv`; truncation and error-channel figure pairs | Development cutoff cap and tolerances are not a frozen protocol or retained result. |
| Threshold-adjacent truncation refinement | Reuses the nonflat definition and dense truncation definition/producer at three construction meshes | Reuses `SmoothFourStateTruncationVerifier` and independently checks each first-passing cutoff and its predecessor | No separate refinement aggregate wire/schema | `run_truncation_refinement_development.py`; `truncation-refinement.csv` | The CSV is a development diagnostic, not an uncertainty estimate or convergence rate. |
| Diagnostic-table admission and sampled decisions | `workflow/analysis.py`: `DiagnosticTable`, `DiagnosticTableContract`, metric metadata, and `DiagnosticBundle` | Schema/product-grid/canonical-order checks and defensive table access; no production analyzer is invoked | CSV contracts are calculation-local; derived tables have no independent retained wire | `run_diagnostic_packaging_development.py`; `diagnostic-catalog.csv`, `sampled-range-decisions.csv` | This is analysis integrity, not a second provenance system. |
| Overview figure composition | `workflow/analysis_plot.py` owns figure construction and saving for three diagnostic views; explicit development plot scripts own the remaining figures | Reproduction compares pixel arrays and rasterized PDFs against predecessor bytes | No authenticated verified-projection record | Ten figure pairs under `analysis/development/figures/` | Direct authenticated render admission remains open before retained use. |
| Prospective protocol and migration boundary | `protocol/experimental-protocol.tex` owns the complete buildable scientific design snapshot; `protocol.md` owns the concise current calculation/lifecycle boundary | Review snapshot is `protocol/experimental-protocol.pdf`; migration evidence is documentary | No immutable versioned configuration wire is frozen | Scratch build recipe in `protocol/README.md`; separate `technical-report/` summary | Authority and conflict rules are defined in `protocol-authority-and-historical-donors.md`; neither surface authorizes execution. |

## Artifact ownership rules

- Producer-owned CSVs remain under `simulations/development/results/`; diagnostic
  packaging does not replace their values.
- `analysis/development/figures/` contains replaceable development renderings. The five
  formerly missing Ragasa2026a inputs have explicit predecessor identities in
  `publication-input-recovery-audit.md`.
- The maintained scientific-story PDF and PNG retain the pre-recovery calculation
  identities `191d8fff...` and `b323ab00...`; the distinct presentation copy
  `9e88e334...` is not promoted into this calculation owner.
- Exact source/destination and supersession dispositions for the remaining experiment
  files are machine-readable in `experiment-removal-manifest.json`.
- Passing checks establish software behavior and bounded reproduction only. They do not
  establish retained evidence, continuum convergence, uncertainty quantification,
  scientific validation, publication acceptance, sealing, or release.
