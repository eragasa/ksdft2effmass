# Frozen portable-verification contract

## Purpose

This document freezes the row-052 responsibility of
`Periodic2DOptimizerBasinCampaignVerifier`. It prevents later “hygiene” work from
silently expanding a compact structural verifier into a native-artifact verifier,
numerical reanalysis, optimizer implementation, or scientific acceptance engine.

Every value in both encoded documents first passes strict UTF-8 JSON decoding,
duplicate-key rejection, closed primitive validation, and nonfinite-real rejection.
That wire-level check does **not** by itself assign scientific meaning.

The field dispositions below are exhaustive for the retained schema and use four terms:

- **Validated** — the portable verifier checks an intrinsic representation, range,
  cardinality, digest, Boolean disposition, or reconstructed arithmetic invariant.
- **Correlated** — the verifier checks equality or an explicit relationship between two
  retained structures. Correlation does not authenticate historical execution.
- **Preserved but uninterpreted** — exact bytes retain the field and strict JSON checks
  its wire representation, but the portable verifier makes no field-specific claim.
- **Explicitly out of scope** — the field points to native/external evidence or requires
  independent numerical reconstruction. The portable route neither reads nor validates
  it. Exact-byte and checksum evidence remain separate.

A field not listed as Validated or Correlated must not be described as verified by this
route. Changes to this matrix reopen row-052 review.

## Study-input fields

| Field or field family | Disposition | Portable-verifier responsibility |
|---|---|---|
| `schema_version` | Validated | Exact integer equal to `1`. |
| `experiment_id` | Correlated | Exact string equality with the result. |
| `evidence_status` | Validated | Exact campaign-owned authoritative-input status. |
| `authorization_checkpoint` | Correlated | Exact string equality with the result; this does not independently authenticate the historical authorization event. |
| `claim_boundary` | Correlated | Exact string equality with the result. |
| `parent_input_path` | Explicitly out of scope | Parent input is not opened or authenticated by the portable route. |
| `executable.name`, `executable.version` | Preserved but uninterpreted | No executable identity or capability is inferred. |
| `executable.path`, `executable.sha256` | Explicitly out of scope | No executable is opened, hashed, or invoked. |
| `external_output_root` | Explicitly out of scope | The external native tree is never accessed. |
| `configurations` cardinality | Validated | Exactly nine entries with unique `configuration_id` values. |
| `configurations[].configuration_id` | Correlated | Exact identity set equals the unique result-configuration identity set. |
| `configurations[].study_axes` | Correlated | Exact recursive JSON representation equals the corresponding result field; axes also select declared finest-pair and embedding-summary identities. |
| `configurations[].plane_wave_cutoff` | Correlated | Exact integer equals the corresponding result control and participates in cutoff-pair selection. |
| `configurations[].reciprocal_mesh_size` | Correlated | Exact integer equals the corresponding result control and participates in mesh-pair selection. |
| `configurations[].transverse_lattice_length` | Correlated | Finite binary64 value equals the corresponding result value with zero absolute tolerance. This does not make the auxiliary coordinate physical. |
| `initial_gauges` cardinality | Validated | Exactly eight entries with unique `gauge_id` values. |
| `initial_gauges[].gauge_id` | Correlated | Every result configuration has exactly one endpoint for each declared identity. |
| `initial_gauges[].ordered_generator_terms` | Preserved but uninterpreted | The portable route does not reconstruct smooth unitary gauges. |
| `gauge_definition.formula`, `multiplication_order`, `generators.*`, `invariants` | Preserved but uninterpreted | Gauge mathematics is retained text/data, not executed or independently checked here. |
| `convergence_method.minimum_repeated_best_basin_occupancy` | Validated | Exact integer used to reconstruct both occupancy-pass flags. |
| `convergence_method.mesh_finest_pair` | Validated and correlated | Exactly two unique integer controls; ordered configuration identities are selected by explicit `mesh` axes and reciprocal-mesh controls. |
| `convergence_method.cutoff_finest_pair` | Validated and correlated | Exactly two unique integer controls; ordered configuration identities are selected by explicit `cutoff` axes and plane-wave controls. |
| `convergence_method.require_both_best_and_median_stability` | Validated | Exact Boolean required to remain true. The portable route does not recompute the best/median metric gates. |
| `convergence_method.common_finite_supercell_grid_size` | Preserved but uninterpreted | No common-grid reconstruction occurs. |
| `convergence_method.basin_spread_absolute_tolerance`, `basin_center_set_periodic_tolerance` | Preserved but uninterpreted | Basin numerical distances are not independently recomputed. |
| `convergence_method.finest_pair_relative_spread_tolerance`, `finest_pair_center_set_periodic_tolerance`, `finest_pair_relative_hopping_tail_tolerance` | Preserved but uninterpreted | Difference metrics and metric-pass flags are not independently recomputed. |
| `convergence_method.classification` | Preserved but uninterpreted | Retained explanatory text is not parsed as executable policy. |
| `execution_limits.*` | Preserved but uninterpreted | The portable route does not authenticate historical resource monitoring or execution-policy enforcement. |

## Result fields

| Field or field family | Disposition | Portable-verifier responsibility |
|---|---|---|
| `schema_version` | Validated | Exact integer equal to `1`. |
| `experiment_id`, `authorization_checkpoint`, `claim_boundary` | Correlated | Exact string equality with study input. |
| `evidence_status` | Validated | Exact campaign-owned calculated-result status, distinct from input authority. |
| `configurations` cardinality and identities | Validated and correlated | Exactly nine unique identities equal to study declarations before any lookup dictionary is built. |
| `configurations[].study_axes`, `plane_wave_cutoff`, `reciprocal_mesh_size`, `transverse_lattice_length` | Correlated | Match explicit study declarations as described above. |
| `configurations[].starts` cardinality and `starts[].gauge_id` | Validated and correlated | Exactly eight unique declared gauge identities per configuration. |
| `configurations[].starts[].completed` | Validated | Every endpoint must carry exact Boolean true. Process completion remains distinct from native convergence. |
| `configurations[].starts[].convergence_criterion_satisfied` | Validated | Exact Boolean partitions endpoints into converged and nonconverged groups. The native criterion itself is not independently recomputed. |
| `configurations[].starts[].native_total_spread_cell_squared` | Validated for finite representation and structurally used | Finite binary64 values select the minimum reported spread among retained converged endpoints. Values are not independently reconstructed from native files. |
| Other `configurations[].starts[]` fields: `analysis_result_path`, `analysis_result_sha256`, common/native centers, common/direct spreads, elapsed time, defects, iterations, resident bytes, and radius-50 tail | Explicitly out of scope | Native files and numerical diagnostics are not authenticated or recomputed by the portable route. Strict JSON still rejects nonfinite decoded reals. |
| `configurations[].converged_start_count` | Correlated | Equals the partition reconstructed from endpoint convergence flags. |
| `configurations[].nonconverged_gauge_ids` | Validated and correlated | Duplicate-free and exactly equals the reconstructed nonconverged identity set. |
| `configurations[].observed_converged_basin_count` | Correlated | Equals the number of retained basin records. |
| `configurations[].observed_converged_basins[].gauge_ids` and `occupancy` | Validated and correlated | Duplicate-free across the complete basin partition; occupancy equals membership count; members partition converged endpoint identities exactly once. |
| `configurations[].observed_converged_basins[].representative_gauge_id` | Correlated | Must be a member of its retained basin. |
| `configurations[].observed_converged_basins[].basin_id`, representative centers, and representative native spread | Preserved but uninterpreted | Basin distances, labels, and representative numerical values are not recomputed. |
| `configurations[].best_is_observed_not_proven_global` | Validated | Exact Boolean required to remain true. |
| `configurations[].best_observed_converged` and all descendants | Correlated | Complete recursive exact-representation equality with the minimum-reported-native-spread converged endpoint. This is copy correlation, not numerical authentication or proof of global optimality. |
| `configurations[].median_across_converged_starts` and descendants | Preserved but uninterpreted | Median and medoid values are not recomputed. They are correlated only where copied into embedding summaries. |
| `configurations[].analysis_input_path`, `analysis_input_sha256` | Explicitly out of scope | Analysis inputs are not opened or authenticated. |
| `convergence_assessment.supports_declared_convergence` | Validated | Exact Boolean required to remain false. |
| `convergence_assessment.not_a_global_or_general_claim` | Validated | Exact Boolean required to remain true. |
| `convergence_assessment.disposition` | Validated | Exact retained negative disposition text. |
| Mesh/cutoff `lower_configuration_id`, `upper_configuration_id` | Correlated | Exact ordered identities derived from study axes and declared controls, never from names. |
| Mesh/cutoff `minimum_endpoint_best_basin_occupancy` | Correlated | Equals the minimum reconstructed occupancy of the two best-observed basins. |
| Mesh/cutoff `occupancy_pass` | Correlated | Equals comparison of reconstructed occupancy with the declared minimum. |
| Mesh/cutoff `supporting` | Validated | Exact Boolean required to remain false. |
| Mesh/cutoff `best_observed_differences.*`, `median_across_converged_starts_differences.*`, and `metrics_pass` | Preserved but uninterpreted | Difference metrics and metric gates require independent numerical reconstruction and are not recomputed here. |
| `convergence_assessment.embedding_sensitivity` identities | Validated and correlated | Unique identity set equals declarations carrying `embedding` or `embedding_reference` axes. |
| Each embedding summary's `best_observed_converged`, `median_across_converged_starts`, `observed_converged_basin_count`, and `transverse_lattice_length` | Correlated | Exact recursive representation equals the corresponding selected fields in the full configuration. No physical meaning is assigned to embedding. |
| `execution_summary.configuration_count`, `localization_count`, `converged_localization_count`, `nonconverged_localization_count` | Correlated | Equal reconstructed configuration and endpoint counts. |
| `execution_summary.all_localization_processes_completed` | Validated and correlated | Exact Boolean true, consistent with individually checked endpoint completion flags. |
| `execution_summary.elapsed_seconds`, `external_output_bytes_at_execution_end`, `maximum_localization_resident_bytes`, `maximum_localization_seconds` | Preserved but uninterpreted | Historical timing, memory, and output accounting are not authenticated. |
| `generated_at_utc` | Preserved but uninterpreted | Timestamp syntax and historical time are not authenticated. |
| `provenance.study_input_sha256` | Validated | Strict lowercase SHA-256 and content identity of encapsulated input bytes. |
| `provenance.extractor_path`, `base_extractor_path` | Validated | Resolve beneath explicit repository root before reads, including symlink resolution. |
| `provenance.extractor_sha256`, `base_extractor_sha256` | Validated | Strict lowercase SHA-256 and content identity of confined compact source bytes. |
| `provenance.study_input_path` | Preserved but uninterpreted | Location is not used to select or authenticate the encapsulated input. |
| `provenance.execution_result_path`, `execution_result_sha256` | Explicitly out of scope | External execution result is not opened or authenticated by this route. |

## Result-DataObject boundary

`Periodic2DOptimizerBasinCampaignVerificationResult` validates exact Boolean flags,
nonnegative exact integer counts, lowercase SHA-256 syntax, immutability, and aggregate
pass conjunction. Direct construction proves only those intrinsic invariants. It does
not prove that `Periodic2DOptimizerBasinCampaignVerifier.execute` ran.

`Periodic2DOptimizerBasinCampaign` owns only exact encoded documents. Each `verify`
request creates a fresh verifier Action; no shared or replaceable verifier collaborator
is retained on the immutable campaign.

## Explicitly excluded conclusions

A passing portable result does not establish:

- execution provenance or native-file availability;
- correctness of paths or digests classified as out of scope;
- Wannier90 execution, native convergence, or basin-distance recomputation;
- correctness of median, medoid, difference-metric, or metric-pass values;
- optimizer global optimality or exhaustive initialization coverage;
- asymptotic mesh/cutoff convergence or physical embedding meaning;
- material or production-Wannierization validity;
- uncertainty quantification, scientific validation, or acceptance.

The historical independent scripts described by `protocol.md` have broader retained
native checks. Row 052 does not rerun them and does not substitute this portable
structural route for their evidence.

## Freeze rule

After this matrix is synchronized with source, tests, the canonical dossier, Sphinx, and
the migration ledger, row 052 is frozen for final independent rereview. A proposed new
field check is a contract change, not “hygiene”; it requires an explicit justification,
updated evidence, and a new review disposition.
