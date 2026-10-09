# Frozen portable-verification contract

## Purpose

This page freezes the row-055 field-by-field responsibility of
`Periodic2DOptimizerStandaloneCampaignVerifier`. A new field check, changed tolerance,
or expanded interpretation is a reviewed contract change, not routine code hygiene.

The verifier authenticates compact repository files and reconstructs retained endpoint,
summary, basin, sensitivity, control, and claim-boundary relationships. It does not open
the external native execution tree, execute calculation scripts, or recursively traverse
provenance.

## Exact source authentication

| Source | Verification |
|---|---|
| Encapsulated `standalone-study-proposal.json` | Exact equality with confined maintained file and frozen SHA-256 `d260475252b420d151ebfd7e276e170c1d069e4bbc7ad974d21e911dd6db3485` |
| Encapsulated `standalone-initial-gauges.json` | Exact equality with confined maintained file and frozen SHA-256 `34ebdb57dbcdb3cb72bb3fbc602a12b3c05b58534d1c028047578afceb1a8f4b` |
| Encapsulated `standalone-result.json` | Exact equality with confined maintained file and frozen SHA-256 `add349df1cccd95fc35c1984a21f58d4d5b49b62ba528377ea0f4245e5d5ce9a` |
| Maintained `extract_standalone_results.py` | Fixed campaign-relative file with frozen SHA-256 `c30612ccd886f140fe429f04233b6312601859d8a09328c71312e1fc204fe5c3`, equal to the result declaration |
| Repository root | `pathlib.Path`, absolute, resolved before reads |
| Maintained paths | Fixed campaign-relative paths resolved under the explicit root; escape is rejected |

The retained absolute `proposal_path` and `extractor_path` strings are preserved report
content, not filesystem authority. The external `execution_result_path` and
`execution_result_sha256` are outside portable authentication. Digest agreement proves
content identity only, not historical execution, authorship, semantics, provenance,
validity, or acceptance.

## Proposal document

The proposal and initial-gauge wires use shared strict JSON decoding. Invalid UTF-8,
duplicate keys, nonstandard nonfinite constants, non-object roots, wrong exact primitive
representations, and unrepresentable/nonfinite consumed reals fail closed. Schema
selection precedes schema-specific adaptation.

| Field | Disposition |
|---|---|
| root `schema_version` | Exact integer `1` |
| `basin_method.spread_absolute_tolerance_cell_squared` | Finite binary64; selects earlier representatives eligible for a density-aware comparison |
| `basin_method.center_set_periodic_tolerance_cell` | Finite binary64; threshold for member/rejected comparisons, sensitivity, and controls |
| `basin_method.maximum_matched_density_l2_mismatch` | Finite binary64; frozen density threshold |
| `basin_method.best_basin_minimum_occupancy` | Exact integer; used with both-start-block flag |
| all other proposal fields | Strict-decoded but preserved outside row-055 semantic verification |

## Initial-gauge document

| Field | Disposition |
|---|---|
| root `schema_version` | Exact integer `1` |
| `proposal_sha256` | Strict lowercase SHA-256; exact proposal identity |
| `start_count` | Exact integer equal to start-array length and exactly 16 |
| `starts[].start_id` | Nonempty exact strings; unique retained order defines `start_index` correlation |
| start generator terms and numerical design details | Strict-decoded but outside portable reconstruction; gauge construction is not replayed |

Start identity and order are explicit metadata. Neither is inferred from endpoint order,
coefficients, paths, or names.

## Historical result wire

The exact result uses bare positive `Infinity` in only the complete seven-part paths
`groups[int].observed_density_d4_basins[int].rejected_equivalence_candidates[int].center_set_periodic_distance`
and
`groups[int].observed_density_d4_basins[int].rejected_equivalence_candidates[int].maximum_density_l2_mismatch`.
The bounded adapter requires those exact field names and integer array positions and
rejects duplicate keys, invalid UTF-8/JSON, `NaN`, `-Infinity`, and positive infinity at
every other path. Mutable parser containers remain inside schema adaptation; only closed
frozen records reach authentication and correlation.

### Root and provenance

| Field | Disposition |
|---|---|
| root `schema_version` | Exact integer `1` |
| `provenance.proposal_sha256` | Strict lowercase SHA-256; exact proposal identity |
| `provenance.extractor_sha256` | Strict lowercase SHA-256; exact maintained extractor identity |
| `provenance.extractor_path` | Required nonempty historical string; preserved, not filesystem authority |
| other provenance fields | Outside direct portable authentication |

### Endpoint transitions

Exactly 256 unique `(configuration_id, arm, start_id)` records are required.

| Field | Disposition |
|---|---|
| `configuration_id`, `arm`, `start_id` | Nonempty exact strings; group/start correlation identities |
| `start_index` | Exact integer equal to the explicit gauge-design position |
| `initial_process_completed` | Exact Boolean and required true |
| `initial_native_converged` | Exact Boolean controlling continuation selection |
| `continuation_applied` | Exact Boolean; logical negation of initial native convergence |
| `continuation_native_endpoint`, `continuation_native_converged` | Both absent (`null`) for initial selection or both present for continuation selection |
| `effective_native_endpoint` | Exact typed equality with selected complete initial or continuation endpoint |
| `effective_native_converged` | Exact Boolean; equal to continuation status when continuation applies |
| `effective_total_iterations` | Exact integer; initial iterations or initial-plus-continuation iterations |
| external `effective_run_root` | Not read or authenticated |
| represented endpoint fields | Preserved in exact result bytes but outside row-055 portable reconstruction |

Each initial, present continuation, and effective native endpoint adapts every retained
field: three center records and their two active-coordinate pairs and orbital indices;
classification strings; iteration, terminal-window, and trace counts; five spread
components; orbital spreads; and six terminal spread/gradient diagnostics. Every
consumed real except the two declared rejected-candidate extended reals must be finite
binary64. The verifier checks

\[
\widetilde\Omega=\Omega_D+\Omega_{OD},\qquad
\Omega=\Omega_I+\Omega_D+\Omega_{OD}
\]

with absolute tolerance `2e-8` in squared-cell units. It reconstructs the retained
terminal diagnostic decision sequence and requires exact classification agreement.

### Execution summary

The seven initial, continuation, effective-convergence, and effective-nonconvergence
counts must equal independently accumulated endpoint values. Diagnostic labels must be
unique and their exact integer counts must equal reconstructed stopped-endpoint classes.
Execution time and byte-volume fields are preserved but not interpreted.

### Group and basin correlation

Exactly 16 unique `(configuration_id, arm)` groups are required. Each group must contain
all 16 explicit start identities exactly once.

| Field | Disposition |
|---|---|
| initial/effective converged counts and effective fraction | Exact endpoint-derived equality |
| nonconverged start IDs | Unique exact set equality with stopped effective endpoints |
| best observed start ID | Minimum effective native `omega_tilde_cell_squared`, then explicit start-ID tie-break |
| declared basin count | Exact basin-array length; nonempty |
| basin IDs and order | Exact sequential IDs; order reconstructed from converged endpoint `(omega_tilde_cell_squared, start_id)` order |
| basin representative ID and spread | Representative is the first ordered member; retained spread equals its effective native endpoint |
| basin start IDs | Unique complete partition of group converged endpoints; representative is first |
| basin occupancy | Exact membership length |
| member-equivalence diagnostics | Exact IDs for every nonrepresentative member; both center and density mismatches pass the frozen thresholds |
| start blocks and both-block flag | Derived from explicit gauge-design positions, then compared exactly |
| rejected candidate identities | Exact earlier-representative sequence selected by the frozen spread tolerance |
| rejected candidate center/density mismatches | Nonnegative finite or positive-infinite binary64; no rejected candidate may pass both frozen thresholds |
| best-basin pass | Occupancy threshold and independently derived both-start-block flag |
| density sensitivity records | Direct pair count, current candidate identities matching the rejected best representative, and occupancy reconstructed at each retained density threshold |
| post-hoc control records | Nonempty count, exact maxima, and frozen-threshold flags reconstructed |
| other basin geometry and symmetry labels | Preserved but outside row-055 reconstruction |

### Claim boundary

The control-status text must exactly preserve that the planned pre-execution control
lacks a retained record and post-hoc controls do not establish retroactive compliance.
`supports_declared_convergence` must be false; both non-global/non-general limitation
flags must be true; and `disposition` must exactly remain `does not support the frozen
standalone finite-sequence criteria`.

## Result boundary

The immutable verification Result validates exact built-in Boolean flags, exact
nonnegative integer counts, and strict lowercase SHA-256 syntax. `passes` is only the
conjunction of compact-source authentication and structural-reconstruction indicators.
Direct Result construction does not prove Action execution or artifact acceptance.

## Explicitly unsupported conclusions

Passing this contract does not:

- authenticate or read external native execution files;
- rerun Quantum ESPRESSO or Wannier90;
- prove basin equivalence as a mathematical or scientific oracle;
- prove local, global, asymptotic, or general optimizer convergence;
- treat deterministic starts as population samples or quantify physical uncertainty;
- combine initialization, localization, parent-model, discretization, retention,
  embedding, interpolation, truncation, or comparison errors;
- reverse the retained negative finite-design disposition;
- establish physical adequacy, scientific validation, or acceptance.
