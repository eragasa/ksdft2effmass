# Frozen portable-verification contract

## Purpose

This page freezes the row-054 field-by-field responsibility of
`Periodic2DOptimizerRegressionCampaignVerifier`. A new field check, changed tolerance,
or expanded scientific interpretation is a reviewed contract change, not routine code
hygiene.

The verifier authenticates three exact compact repository files and reconstructs the
retained finite diagnostics without importing or executing the retained analyzer. It
does not authenticate external native files or recursively traverse provenance.

## Exact source authentication

| Source | Verification |
|---|---|
| Encapsulated `standalone-result.json` | Exact equality with the confined maintained file and SHA-256 equality with `source_result_sha256` |
| Encapsulated analyzer source | Exact equality with the confined maintained file and frozen SHA-256 `e80c16ab7fd11d86e6c51a344e01790306982f1a628b962611dfd0291d16fe46` |
| Encapsulated regression result | Exact equality with the confined maintained file |
| Repository root | Exact `pathlib.Path`, absolute, resolved before reads |
| Maintained paths | Fixed campaign-relative paths resolved under the explicit root; escape is rejected |

Digest agreement establishes content identity only. It does not establish historical
execution, author identity, provenance, semantics, validity, or acceptance.

## Historical source document

The exact source wire contains historical bare `Infinity` values in fields outside this
row's contract. The bounded adapter rejects duplicate keys and invalid UTF-8/JSON,
recognizes only the three Python-JSON nonfinite tokens in its temporary parse tree, and
adapts only the fields below. Any consumed nonfinite value is rejected.

| Field | Disposition |
|---|---|
| root `schema_version` | Exact integer `1` |
| `endpoints` | Exact array; required count 256 |
| each endpoint `configuration_id` | Nonempty exact string; used in group identity |
| each endpoint `arm` | Nonempty exact string; used in group identity |
| each endpoint `start_index` | Exact integer; exactly indices 0–15 |
| each endpoint `start_id` | Nonempty exact string; one-to-one with `start_index` |
| each endpoint `effective_total_iterations` | Finite positive binary64 value; logarithm enters likelihood |
| each endpoint `effective_native_converged` | Exact Boolean; event/right-censor indicator |
| all other source fields | Parsed only to locate the owned fields; unexposed and outside row-054 semantic verification |

Endpoint quadruples `(configuration_id, arm, start_index, start_id)` must be unique.
Every declared category group must contain every one of the 16 explicit starts.

## Strict regression document

The regression payload uses shared strict JSON decoding: invalid UTF-8, duplicate keys,
nonstandard nonfinite constants, non-object roots, wrong primitive representations, and
unrepresentable/nonfinite consumed reals fail closed. Schema version is selected before
version-one fields are accessed.

| Field | Disposition |
|---|---|
| `schema_version` | Exact integer `1` |
| `evidence_status` | Exact frozen exploratory/synthetic/non-DFT statement |
| `source_result_path` | Required nonempty string, preserved as historical report content; not used to locate or authenticate the source |
| `source_result_sha256` | Strict lowercase SHA-256 and exact digest of encapsulated source bytes |
| `model.family` | Exact `log-normal accelerated-failure-time` declaration |
| `model.response` | Exact retained response declaration |
| `model.censoring` | Exact retained right-censoring declaration |
| `model.category_effects` | Exact retained group-effect declaration |
| `model.start_adjustment` | Exact retained deterministic-start fixed-effect declaration |
| `model.reference_group` | Exact `fixed_c31_p4_n23:baseline_preconditioned` |
| `model.reference_start` | Exact `identity` |
| `model.intervals` | Exact retained deterministic-start-clustered limitation statement |
| `model.interpretation` | Exact retained descriptive/noncausal interpretation |
| `observation_count` | Exact integer 256 and endpoint-derived equality |
| `converged_count` | Exact integer 196 and endpoint-derived equality |
| `right_censored_count` | Exact integer 60 and endpoint-derived equality |
| `parameter_count` | Exact integer 32 and parameter-length equality |
| `parameters[].name` | Unique exact ordered design identity: intercept, declared nonreference categories, nonreference starts, log scale |
| `parameters[].value` | Finite binary64; used in independent reconstruction |
| `negative_log_likelihood` | Reconstructed to absolute tolerance `1e-9` |
| `gradient_infinity_norm` | Reconstructed to absolute tolerance `1e-9` and required not to exceed `2e-4` |
| `hessian_condition_number` | Reconstructed to absolute tolerance `1e-7` |
| `log_time_scale` | Equal to final fitted parameter within `1e-12` |
| `time_scale` | Equal to exponential of log scale within `1e-12` |
| `claim_boundary` | Exact frozen noncausal/nonconvergence/non-DFT statement |

Negative counts, nonpositive effective iteration counts, duplicate identities,
incomplete start coverage, and nonfinite reconstructed quantities fail closed.

## Category estimates

Category order is the explicit retained design order. Category keys must be unique and
match exactly the source-derived group set. No category identity is inferred from a
label, filename, coefficient magnitude, or endpoint order.

| Field | Disposition |
|---|---|
| `group_key` | Exact design identity; complete unique set match |
| `label` | Required nonempty display text; preserved but not assigned scientific identity |
| `converged_count` | Exact source-derived group event count |
| `right_censored_count` | Exact source-derived group censor count |
| `log_time_ratio` | Reconstructed group coefficient within `1e-12` |
| `clustered_standard_error` | Reconstructed covariance diagonal within `1e-9` |
| `time_ratio` | Reconstructed exponential within `1e-12` |
| `time_ratio_95_percent_interval` | Exact length two; reconstructed endpoints within `1e-9` |
| `adjusted_median_iterations` | Reconstructed within `1e-9` |
| `predicted_convergence_probability[].iterations` | Exact ordered checkpoints `(500, 1000, 2500, 5000, 10000, 20000)` |
| `predicted_convergence_probability[].probability` | Finite value in `[0,1]`; reconstructed within `1e-12` |

The interval and probability checks reproduce the retained model only. They do not
qualify the model as a numerical oracle for another evidence class.

## Numerical implementation

The independent route reconstructs analytic observation scores and the censored
negative log likelihood, uses centered finite differences of the gradient with relative
step `1e-5`, symmetrizes the Hessian, uses pseudoinverse relative cutoff `1e-12`, groups
scores by explicit deterministic-start identity, and applies the retained finite-cluster
correction. It shares only typed decoded source values, not the analyzer's computational
implementation.

## Result boundary

The immutable Result validates exact built-in Boolean flags, exact nonnegative integer
counts, and strict lowercase SHA-256 syntax. `passes` is only the conjunction of source
authentication and numerical reconstruction indicators. Direct Result construction does
not prove that the verifier ran or that an artifact is accepted.

## Explicitly unsupported conclusions

Passing this contract does not:

- rerun Wannier90 or authenticate unavailable native files;
- prove convergence, global optimality, causal effects, or population generalization;
- treat deterministic starts as random samples;
- quantify physical or scientific uncertainty;
- validate the log-normal family or extrapolation beyond retained checkpoints;
- combine optimizer behavior with parent-model, discretization, retention, gauge,
  localization, interpolation, truncation, or comparison errors;
- reverse row 052's negative finite-design disposition;
- establish scientific validation, physical adequacy, or acceptance.
