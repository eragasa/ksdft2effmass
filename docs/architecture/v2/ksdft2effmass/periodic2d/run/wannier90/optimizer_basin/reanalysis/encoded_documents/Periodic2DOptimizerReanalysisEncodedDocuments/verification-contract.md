# Optimizer reanalysis portable-verification contract

## Status

This document freezes the verifier-owned semantic boundary for
`PERIODIC-XWALK-053`. A new field check or a change in field interpretation is a
reviewed contract change, not routine code hygiene.

The portable verifier authenticates compact repository evidence and reconstructs
bounded offline diagnostics. It does not authenticate the unavailable external
native tree, rerun Wannier90, prove optimizer completeness or global optimality,
establish scientific validation, quantify uncertainty, or record acceptance.

## Contract classes

Each retained field is assigned exactly one class:

- **validated** — checked intrinsically or against a fixed row-053 rule;
- **correlated** — checked against another authenticated retained field or source;
- **preserved but uninterpreted** — retained as exact result content but assigned no
  portable scientific meaning;
- **out of scope** — deliberately not authenticated or replayed by this verifier.

## Source optimizer-basin result

| Field | Class | Portable responsibility |
|---|---|---|
| `schema_version` | validated | Exact integer `1`. |
| `configurations` | validated | Array of records with unique `configuration_id` values. |
| `configurations[].configuration_id` | correlated | Exact identity set equals the reanalysis configuration set. |
| `configurations[].plane_wave_cutoff` | correlated | Exact integer equals the corresponding reanalysis value. |
| `configurations[].reciprocal_mesh_size` | correlated | Exact integer equals the corresponding reanalysis value. |
| `configurations[].transverse_lattice_length` | correlated | Finite real equals the corresponding reanalysis value exactly. |
| `configurations[].starts` | validated | Array with unique `gauge_id` values. |
| `configurations[].starts[].gauge_id` | correlated | Exact identity set equals the corresponding reanalysis start set. |
| `configurations[].starts[].convergence_criterion_satisfied` | correlated | Exact Boolean equals the reanalysis endpoint value. |
| `configurations[].starts[].native_total_spread_cell_squared` | correlated | Finite value agrees with reconstructed reanalysis total spread within `2e-8`. |
| all other source fields | preserved but uninterpreted | Available to the strict decoder but assigned no row-053 responsibility. |

## Reanalysis result root

| Field | Class | Portable responsibility |
|---|---|---|
| `schema_version` | validated | Exact integer `1`. |
| `campaign`, `generated_at`, `authorization`, `authority`, `evidence_status`, `claim_boundary` | preserved but uninterpreted | Retained wire content; no identity, chronology, authority, acceptance, or scientific conclusion is inferred. |
| `provenance.source_result_path` | out of scope | Not opened and not used to locate source bytes. |
| `provenance.source_result_sha256` | correlated | Strict lowercase digest authenticates encapsulated `source_result_payload`. |
| `provenance.reanalyzer_path` | validated | Resolves inside explicit `repository_root`. |
| `provenance.reanalyzer_sha256` | correlated | Strict lowercase digest authenticates the confined repository bytes. |
| `provenance.base_extractor_path` | validated | Resolves inside explicit `repository_root`. |
| `provenance.base_extractor_sha256` | correlated | Strict lowercase digest authenticates the confined repository bytes. |
| `provenance.source_analysis_result_path` | out of scope | External native-tree path is not opened or authenticated. |
| `provenance.source_analysis_result_sha256` | preserved but uninterpreted | Digest text is retained but does not authenticate an external file. |

## Method

| Field | Class | Portable responsibility |
|---|---|---|
| `method.common_estimator_fft_sizes` | validated | Exact integer sequence `[256, 512, 1024]`. |
| `method.basin_spread_absolute_tolerance` | validated | Finite real used in retained basin reconstruction. |
| `method.basin_center_set_periodic_tolerance` | validated | Finite real used in retained basin reconstruction. |
| `method.symmetry_aware_basin_classifier` | preserved but uninterpreted | Text is not used to select code or infer a classifier implementation. |
| `method.common_estimator_note` | preserved but uninterpreted | Narrative remains claim-boundary content. |

## Configurations and endpoints

| Field | Class | Portable responsibility |
|---|---|---|
| `configurations` | validated | Array with unique `configuration_id` values and the exact source identity set. |
| `configurations[].configuration_id` | correlated | Exact source configuration identity. |
| `configurations[].plane_wave_cutoff` | correlated | Exact source integer. |
| `configurations[].reciprocal_mesh_size` | correlated | Exact source integer. |
| `configurations[].transverse_lattice_length` | correlated | Exact finite source value. |
| `configurations[].starts` | validated | Array with unique `gauge_id` values and the exact source gauge set. |
| `configurations[].starts[].configuration_id` | correlated | Exact enclosing configuration identity. |
| `configurations[].starts[].gauge_id` | correlated | Exact corresponding source endpoint identity. |
| `configurations[].starts[].convergence_criterion_satisfied` | correlated | Exact source Boolean. |
| `configurations[].starts[].spread_components.omega_i_cell_squared` | validated | Finite real; participates in total-spread reconstruction. |
| `configurations[].starts[].spread_components.omega_d_cell_squared` | validated | Finite real; participates in gauge-dependent and total-spread reconstruction. |
| `configurations[].starts[].spread_components.omega_od_cell_squared` | validated | Finite real; participates in gauge-dependent and total-spread reconstruction. |
| `configurations[].starts[].spread_components.omega_tilde_cell_squared` | correlated | Equals `omega_d + omega_od` within `2e-8`. |
| `configurations[].starts[].spread_components.omega_total_cell_squared` | correlated | Equals `omega_i + omega_d + omega_od` within `2e-8` and correlates with source native total spread. |
| four terminal trace metrics | validated | Finite values used by the fixed descriptive classifier. |
| `spread_components.diagnostic_classification` | correlated | Exact fixed classification reconstructed from convergence and terminal metrics. |
| `native_centers_modulo_cell` | validated | Nonempty arrays of finite two-coordinate centers used in periodic matching. |
| `iteration_trace_tail` | preserved but uninterpreted | Trace samples are not replayed; only already-derived terminal metrics are classified. |
| `best_observed_converged_by_omega_tilde` | correlated | Exact recursive JSON copy of the complete minimum reported converged endpoint. |
| `symmetry_aware_observed_basins[].gauge_ids` | correlated | Exact bounded representative partition reconstructed with the retained tolerances and eight square-lattice coordinate operations. |
| all other basin fields | preserved but uninterpreted | Labels, representative summaries, and descriptive fields are retained without additional interpretation. |
| `symmetry_aware_observed_basin_count` | correlated | Exact number of retained basin records. |

## Aggregate classification counts

| Field | Class | Portable responsibility |
|---|---|---|
| `diagnostic_classification_counts` | correlated | Exact object of reconstructed class-to-count pairs; no missing or additional class is accepted. |

The classification is descriptive and post hoc. It is not a native Wannier90
convergence decision and does not change the row-052 negative convergence disposition.

## Common-estimator refinement

| Field | Class | Portable responsibility |
|---|---|---|
| `common_estimator_refinement` | validated | Array with unique `case_id` values. |
| `[].case_id` | validated | Exact unique string identity. |
| `[].configuration_id`, `[].gauge_id` | correlated | Pair identifies an existing reanalysis endpoint. |
| `[].convergence_criterion_satisfied` | correlated | Exact endpoint Boolean. |
| `[].sizes` | validated | Exact ordered FFT sizes `[256, 512, 1024]`. |
| `[].sizes[].input_path` | validated | Must have a logical basename. The external path itself is not authenticated. |
| maintained estimator fixture selected by basename | correlated | Resolved beneath the maintained fixture directory and authenticated by `input_sha256`. |
| `[].sizes[].input_sha256` | validated/correlated | Strict lowercase SHA-256 syntax and exact maintained-fixture identity. |
| `[].sizes[].common_total_spread_cell_squared` | validated | Finite real. |
| `[].sizes[].common_centers_modulo_cell` | validated | Nonempty arrays of finite two-coordinate centers. |
| `[].refinement_512_to_1024.relative_total_spread_difference` | correlated | Reconstructed from the 512 and 1024 spread values within `1e-15`. |
| `[].refinement_512_to_1024.center_set_periodic_distance` | correlated | Reconstructed by permutation-minimized periodic center matching without point-group operations, within `1e-15`. |
| all other refinement fields | preserved but uninterpreted | No additional scientific meaning is assigned. |

## Complexity and failure boundary

Strict JSON decoding is linear in the wire size apart from parser recursion. Center-set
matching enumerates all orbital permutations and therefore scales factorially with
retained rank; the retained campaign rank is three. The verifier imposes no arbitrary
size cap and documents possible `MemoryError` and `RecursionError`.

A successful result establishes only consistency with this frozen contract and exact
compact-byte identities. SHA-256 identities establish content identity, not provenance,
scientific meaning, correctness, convergence, validation, uncertainty quantification,
or acceptance.
