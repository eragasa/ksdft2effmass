# C6-B20-W21 hopping-first Pareto synthesis contract

**Status: V2 LATEST EXECUTION; FORMATTING-ONLY V3 LIVE AND UNEXECUTED**

This calculation-owned contract defines a characterization-only, no-calculator synthesis
of the existing complete-shell evidence. Its goal is to expose channel-specific support
tradeoff spaces. It adopts fixed-gauge finite enumeration: it neither modifies, wraps,
reruns, nor reimplements Wannier90 optimization. It does not select a new support,
calibrate an operational diagnostic to parent error, predict hidden error, fit a
Slater--Koster model, or observe confirmation parent values.

## Bound authorities

An implementation must authenticate these exact retained inputs before computing any
new value:

| Authority | Role | SHA-256 |
|---|---|---|
| [`../c6-b20-w21-untruncated-characterization/characterization-result.json`](../c6-b20-w21-untruncated-characterization/characterization-result.json) | S30 full untruncated rank-10 source and structural reconstruction | `37f654ae31bc21e43b768bf2b9da5edabd88c195e3f6e1c87708eaa1c4773c18` |
| [`../c6-b20-w21-spatial-truncation-design/truncation-design.json`](../c6-b20-w21-spatial-truncation-design/truncation-design.json) | S90 complete-shell candidate family and diagnostic definitions | `6b9863271ba8241881d62435a7c8307d3431ffe59bfdcce5d96525fe86fcb531` |
| [`../c6-b20-w21-spatial-truncation-evaluation/truncation-evaluation.json`](../c6-b20-w21-spatial-truncation-evaluation/truncation-evaluation.json) | S100 existing complete-family evaluation on its retained domains | `1ac8bb59137e8dc7217df52f89c18a84e8599bcf82ec59f40a361929d4322a52` |
| [`../c6-b20-w21-spatial-truncation-disposition/spatial-truncation-disposition.json`](../c6-b20-w21-spatial-truncation-disposition/spatial-truncation-disposition.json) | S105 selected full-support disposition | `519adfcf1101f7caa7916e04f3bf37879f4ad82b0f30e4ef38adc39770224f68` |
| [`../construction-mesh-adequacy-recommendation/construction-mesh-candidates.json`](../construction-mesh-adequacy-recommendation/construction-mesh-candidates.json) | exact C6 construction mesh | `1e5ebb9dffa6a97a2f2445cfd6290aff4cd3d6c06c15e4e0e7d6bbde7826c803` |
| [`../withheld-parent-validation-preflight/withheld-kpoint-manifest.json`](../withheld-parent-validation-preflight/withheld-kpoint-manifest.json) | exact 408-point development evaluation inventory | `754bce5030ef0e34eb092406b27d9094287b4f749e358ef36404040f44b8d2b4` |
| [`../c6-b20-w21-revealed-408-development/development-result.json`](../c6-b20-w21-revealed-408-development/development-result.json) | revealed-parent evaluation overlay only | `bb1a6d0fab5d08fecaa0d86cbfe00e8670e7f089e289c6fabc59c32c6f76991d` |
| [`../construction-mesh-adequacy-recommendation/successor-confirmation-holdout.json`](../construction-mesh-adequacy-recommendation/successor-confirmation-holdout.json) | confirmation-only geometry and non-consumption boundary | `51427c7389ae293566d865d42a3a8a8217b0fed4607ac65c5a97199ce6a383c8` |

The candidate set is exactly the 18 nested complete physical-radius shells
`H-shell-00` through `H-shell-17`, containing the already authenticated 383 effective
WS representatives at full support. No candidate may be added, removed, split, or
pruned. The onsite shell remains admitted even when a named observable is undefined.

## Reciprocal-space roles

The roles are fixed and noninterchangeable:

1. The Gamma-origin `6 x 6 x 6` C6 construction mesh has 216 points. It establishes
   finite-transform source reconstruction only. It is not the Pareto evaluation
   inventory.
2. The revealed 408-point geometry is the development evaluation inventory. Internal
   shell errors are measured there against the full `H_W` in the same rank-10 Wannier
   gauge. Revealed direct-parent comparisons may be displayed afterward as a separate
   evaluation overlay; they do not define candidates, metrics, frontiers, support
   selection, fitting objectives, or thresholds.
3. The frozen 402-point geometry is confirmation-only. Neither its geometry nor future
   parent values may define or tune a diagnostic, candidate, Pareto frontier,
   truncation, fit, threshold, or numerical comparison policy.
4. The balanced 108/108 construction-grid split remains reserved for a future,
   separately authorized Slater--Koster study. It has no role in this hopping synthesis.

## Bound numerical controls

The synthesis inherits rather than weakens the retained structural controls:

- complete shells use S90's Cartesian-radius grouping after rounding radii to nine
  decimal places in angstrom;
- every candidate must preserve exact recorded representative inclusion and
  `R`/`-R` closure;
- pair-Hermiticity uses S30's `1e-8 eV` maximum residual tolerance;
- source reconstruction remains bounded by S30's authenticated native serialization:
  six HR decimals, ten `u`/`u_dis` decimals, twelve EIG decimals, exact degeneracy
  weights, and the retained derived bounds (`0.0001528384214328397 eV` matrix-element,
  `0.001527454004059488 eV` matrix-Frobenius and ordered-spectrum);
- the 408-point coordinates and equal weights `1/408` are taken byte-for-byte from the
  bound manifest; and
- no numerical-convergence, parent-fidelity, tail, or Slater--Koster tolerance becomes a
  support-acceptance threshold.

The selected policy is **conservative interval Pareto dominance**:

- retained support cost is the exact integer included-representative count;
- every numerical objective is a closed uncertainty interval;
- candidate A robustly dominates B on one channel-specific frontier only when A has no
  greater exact cost, A's upper objective bound is no greater than B's lower bound, and
  at least one of those two coordinates is strictly better; and
- intervals with positive overlap remain `UNRESOLVED_INTERVAL_OVERLAP` rather than being
  forced into an order.

Touching closed intervals are ordered only when the upper bound of one is no greater
than the lower bound of the other. No absolute/relative tolerance, scalar score, or
cross-channel aggregation is introduced. The interval-construction method for the
currently unavailable 408-point per-shell metrics must be declared by their future
producer; the classifier does not invent intervals from point estimates.

## Channel-specific Pareto definitions

For shell candidate `s`, retain both exact support descriptors:

- `N(s)`: included effective-representative count; and
- `r(s)`: complete-shell radius in angstrom.

`N(s)` is the retained-support cost coordinate; `r(s)` is reported alongside it. Both
increase in the same order for this nested family. This definition is not a runtime or
parameter-count model for a future Slater--Koster Hamiltonian.

For every scalar error metric `E_j`, construct a separate two-coordinate descriptive
frontier `(N(s), E_j(s))`. Candidate `s` is dominated in channel `j` only when another
applicable candidate has no greater retained count and no greater channel error, with at
least one strict comparison under the selected numerical policy. Do not scalarize
channels, average frontier ranks, combine errors into one loss, or select a compromise
shell.

The required frontiers are separate for each retained metric:

- **operator:** maximum pointwise spectral norm and weighted-RMS Frobenius norm of
  `H_W(k) - H_s(k)` on the 408-point inventory;
- **ordered spectrum:** maximum absolute and weighted-RMS ordered-eigenvalue differences
  across all ten bands on the same inventory;
- **gap:** absolute indirect-gap change relative to full `H_W`;
- **valley:** maximum periodic Cartesian valley displacement and maximum valley-energy
  change relative to full `H_W`, with identity failure retained separately; and
- **curvature/mass:** each S100-named primary-curvature, direction-matched effective-mass,
  and stencil-stability scalar relative to full `H_W`, each with its own frontier.

The 408-point manifest, its role labels, and the existing S40 matching conventions bind
the development evaluation. If an inventory does not resolve a shell's valley or
curvature observable, retain a typed unresolved outcome; do not assign zero, infinity,
or a favorable rank. The onsite-only flat-band control therefore remains a candidate but
has inapplicable valley and mass channels.

Tail Frobenius norms, excluded-block spectral norms, spectral triangle bounds,
Hermiticity residuals, and larger-shell envelopes remain reported diagnostics. They are
not substitutes for measured operator, spectral, gap, valley, curvature, or mass errors
and do not define Pareto dominance in those channels.

## Required output contract

A future separately authorized no-calculator implementation must produce one immutable,
typed result containing:

1. authenticated identities for every bound authority and the implementation itself;
2. `calculator_invocations = 0`;
3. all 18 candidates in original order, with radius, included/excluded counts, pair
   closure, Hermiticity, and full-support equality;
4. per-candidate 408-point operator, ordered-spectrum, gap, valley, curvature, and mass
   uncertainty intervals relative to full `H_W`, each with its declared availability;
5. per-metric frontier membership with explicit dominator identities for dominated
   candidates;
6. unresolved/inapplicable reasons without numeric sentinels;
7. S100 tail diagnostics displayed separately from measured channel errors;
8. a separate 408-parent evaluation overlay that cannot affect frontier membership;
9. the frozen 402 identity and `parent_values_consumed = false` boundary;
10. the reserved 108/108 Slater--Koster role with `consumed = false`; and
11. the unchanged selected disposition: `H-shell-17`, 383 representatives,
    `H_T = H_W`, zero selected spatial-truncation error, and no newly accepted support.

Allowed top-level dispositions are:

- `COMPLETED_CHARACTERIZATION_ONLY`: every required identity and applicable interval is
  present, all frontiers are classified, no new support is selected, and no forbidden
  inventory is consumed;
- `UNRESOLVED_DEVELOPMENT_EVALUATION`: the required authenticated 408-point interval
  bundle is absent; and
- `UNRESOLVED_CHANNEL_METRIC`: an otherwise authenticated bundle explicitly records an
  applicable unresolved channel.

`INAPPLICABLE_OBSERVABLE_IDENTITY` is a candidate/objective membership only, never a
whole-result disposition. A byte-identity, producer-identity, policy-identity, source-
binding, candidate-order, or support-cost failure is fail-closed: the action raises an
error and writes **no output**, rather than emitting a result that could be mistaken for
an authenticated record.

`COMPLETED_CHARACTERIZATION_ONLY` is not scientific validation, support acceptance,
Slater--Koster readiness, or execution authority.

## Installed action and current readiness

[`run_analysis.py`](run_analysis.py) implements:

- fail-closed authentication of every bound retained identity and runtime computation of
  its own implementation SHA-256;
- exact ordered `H-shell-00` through `H-shell-17` identity, radius, strictly increasing
  integer support-cost, closure, Hermiticity, and full-support checks;
- composition of all 18 candidate records with S100 tail/envelope diagnostics and typed
  408-point objective intervals;
- a separate revealed-408 parent overlay that is never a frontier input;
- an `UNRESOLVED_DEVELOPMENT_EVALUATION` record containing all available retained fields
  and explicit per-objective gaps when no interval bundle is supplied;
- conservative interval-frontier classification only after authenticating the declared
  producer file, interval-policy file, exact ordered source bindings, and bundle bytes;
- typed candidate-level inapplicable/unresolved handling; and
- deterministic no-overwrite JSON output.

The live formatting-only v3 action SHA-256 is
`76321e9fa38b789dadd4d6b771ac57283deadf95e0c3249569af05287ad76a86`.
V3 has **not** been executed and has no result. The latest execution remains v2, whose
exact producer bytes are immutable at
[`executions/identity-gap-v2/producer-source.py.txt`](executions/identity-gap-v2/producer-source.py.txt).
The executed v1 producer bytes likewise remain immutable at
[`executions/identity-gap-v1/producer-source.py.txt`](executions/identity-gap-v1/producer-source.py.txt).

Its explicit `--software-test-input` route consumes synthetic metrics only, marks output
`SYNTHETIC_SOFTWARE_TEST_ONLY`, and never reads retained silicon inputs.

The retained authorities uniquely supply the shell inventory, all source identities,
structural tolerances, existing S100 metrics on its `21^3` and valley/stencil domains,
and the S105 full-support disposition. They do **not** contain the required per-shell
interval metrics evaluated on the 408-point development inventory. The installed action
therefore cannot produce silicon frontier memberships from current retained JSON alone.
It does not reconstruct HR/WS data, wrap or modify Wannier90, or fabricate missing
intervals.

## Authorized identity/gap executions

### Preserved v1

The operator authorized the first no-calculator identity/gap route with the direct
instruction `so let's run it on what we have`. It executed at
`2026-11-02T12:40:19Z` without a metrics bundle. The original no-overwrite result remains
at [`replaceable/hopping-pareto-synthesis-result.json`](replaceable/hopping-pareto-synthesis-result.json).
Exact producer and result copies plus the execution record are retained under
[`executions/identity-gap-v1/`](executions/identity-gap-v1/manifest.json):

- producer SHA-256: `d745b753d9d608cbcbf9dacb12b5a9159727d66ba97fc9c13840eb07d00962cf`;
- result SHA-256: `4dd7ae9842a2b33784f6c9ec19b0353e8959c8d25fa3682603f509852146ad3c`,
  230900 bytes;
- manifest SHA-256: `49d723bbcbe45ecbdf1d3a9bc39fbfcc04884e271dea074acaf894e0b0791076`; and
- resources: 0.07 seconds wall, 0.05 seconds user, 0.01 seconds system, and
  31,473,664 bytes maximum resident set size.

V1 records an absolute workstation `implementation.path`. It is
`superseded_for_portability_only`; its `UNRESOLVED_DEVELOPMENT_EVALUATION` scientific
disposition is unchanged, and neither its producer nor result bytes were rewritten.

### Portable v2

The operator separately authorized the provenance-preserving migration and one corrected
rerun. The then-installed v2 action executed exactly once at `2026-11-02T12:45:20Z`:

```text
PYTHONDONTWRITEBYTECODE=1 python/.venv/bin/python \
  calculations/Si/bulk/analysis/c6-b20-w21-hopping-pareto-synthesis/run_analysis.py \
  --bulk-root calculations/Si/bulk \
  --output calculations/Si/bulk/analysis/c6-b20-w21-hopping-pareto-synthesis/executions/identity-gap-v2/hopping-pareto-synthesis-result.json
```

The immutable v2 record is retained under
[`executions/identity-gap-v2/`](executions/identity-gap-v2/manifest.json):

- producer SHA-256: `c156d413ef11cc37aae5b93f2f239b9d23344d8f6ad194f2bef781188065aeb1`;
- result SHA-256: `1af973546b6e1a9687a51433b0ba61227b9f2d13b711d89e789a3ba7c29e6b50`,
  230821 bytes;
- manifest SHA-256: `84b3170a59f24d730f8f5a41d37042c820917b711471f1b92c19be831b243284`; and
- resources: 0.06 seconds wall, 0.05 seconds user, 0.01 seconds system, and
  31,588,352 bytes maximum resident set size.

V2 records the repository-relative implementation path and derives unresolved costs from
the authenticated retained candidate inventory. Its result's repository-relative live
path plus producer SHA-256 resolves immutably to the retained v2 producer copy even though
the live path now contains v3. After normalizing the implementation identity object, the
v1 and v2 JSON values are identical. Both record
`UNRESOLVED_DEVELOPMENT_EVALUATION`, all eight inputs, 18 ordered candidates, the separate
parent overlay, and missing 408-point intervals.

### Live formatting-only v3

Independent validation found one 89-character exception-message source line in v2. V3
wraps only that string literal; Python concatenation preserves the runtime message. V3
has SHA-256 `76321e9fa38b789dadd4d6b771ac57283deadf95e0c3249569af05287ad76a86`.
No v3 result, manifest, execution identity, or scientific disposition exists. V2 remains
the latest execution and the authoritative retained identity/gap result.

## Future interval-bundle execution plan

With a separately reviewed 408-point interval-metrics bundle, add all three authenticated
arguments:

```text
  --metrics /absolute/path/to/authorized-408-shell-interval-metrics.json \
  --metrics-producer /absolute/path/to/authorized-producer-action.py \
  --interval-policy /absolute/path/to/reviewed-interval-construction-policy
```

The bundle must declare identities and SHA-256 values matching the latter two files and
must carry the exact ordered S30/S90/S100/S105, C6, and 408-inventory source-binding
records. Missing or mismatched provenance produces no output.

The action requires one local Python process, no MPI, no network, no Quantum ESPRESSO or
Wannier90 executable, and no accelerator. Identity/gap inspection and interval
classification are expected to remain below 60 seconds wall time and 256 MiB resident
memory; these are resource ceilings for authorization, not measured runtimes. The output
is one deterministic JSON file at the requested no-overwrite path. No PDF, image,
wavefunction, density, restart, or dense-matrix output is produced.

A separate future action or reviewed extension would still be required to reconstruct
all 18 shell operators on the 408-point inventory and produce their uncertainty
intervals. That work must bind the existing HR/WS identities and interval-propagation
rule before execution; it is not authorized here.

The completed v1 and v2 identity/gap runs invoked no Quantum ESPRESSO or Wannier90
executable, network service, or 402-point parent calculation and supplied no invented
intervals. No additional retained-evidence execution, result creation, or output
replacement is implied by those bounded authorizations.
