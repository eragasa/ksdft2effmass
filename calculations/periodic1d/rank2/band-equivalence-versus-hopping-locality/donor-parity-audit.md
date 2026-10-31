# Calculation-local donor parity audit

## Scope and decision boundary

This read-only audit compares the calculation-local historical `workflow/` donors with
installed owners under
`ksdft2effmass.periodic1d.band_equivalence_locality` and with the immutable unsealed
`direct-embedded-rank2-controlled-v2` calculation record. It asks only whether the
tracked donor tree is ready for reviewed retirement.

The audit is bound to repository revision
`5e53559ca0586393b13b60ad213913216cfd149e`. At that revision:

- the 31-file `workflow/` Git tree is
  `9ba77fc1fea2ee4957678c70baaa00a7a08d3d46`;
- the installed owner Git tree is
  `9d16a41233b0470795b328afadd1348e142ffbcf`;
- the direct-v2 calculation SHA-256 is
  `29c1a2bdd7ec85b721cb9c9248ba0961cd1472278cf79a33f641eaa9e657dd01`;
  and
- no donor, development-result, `v1`, `v2`, figure, report, or protocol byte was changed
  by this audit.

SHA-256 and Git identities establish byte identity and recovery, not scientific
validity. Numerical agreement below establishes bounded software-route agreement only.
It does not establish convergence, sealing, material validation, publication
acceptance, or release readiness.

## Method

The audit did not rerun either retained execution and did not activate
`workflow/analysis.py` or `workflow/analysis_plot.py`, the pandas-dependent diagnostic
surface. A repository test admits the canonical direct-v2 typed calculation bytes and
compares them with the immutable workflow-produced development CSVs using only Python's
standard `csv` module:

`python/tests/ksdft2effmass/periodic1d/band_equivalence_locality/embedded_subspace/rank2/test__Periodic1DRank2DonorParity.py`

The test binds all compared input digests, compares every mapped scalar, and records
semantic differences rather than relaxing tolerances. Its comparison tolerance is
`1.0e-13`; this is an audit-comparison tolerance and does not alter the installed
`1.0e-10` independent-verification tolerance.

## Named source parity

| Donor surface | Installed successor | Audit disposition |
|---|---|---|
| `_validation.py` and scientific definitions | Exact typed request validation in the flat and `embedded_subspace/rank2` owners | Behavior represented; installed owners additionally reject booleans at numeric boundaries. |
| Flat `definition.py`, `experiment.py`, `results.py`, and `verify.py` | Flat-parent request, analyzer, records, independent reference, verifier, and visualizer | Scientific core represented and independently tested, but the cohesive direct-v2 aggregate does not retain the flat channel and no immutable donor-to-direct artifact comparison exists. |
| Flat `serialization.py` and flat schema documents | Canonical typed record and verification bytes | Deliberate replacement, not wire compatibility. Historical schema decoding is not promised. |
| `nonflat/definition.py`, `experiment.py`, and `results.py` | Embedded rank-two request, parent, transport, analysis, family, momentum-refinement, and adaptive-amplitude owners | Pointwise and family outcome channels agree within the bounded comparison below. The installed momentum parent-diagnostic semantics are intentionally broader. |
| `nonflat/verify.py` | Independent single-parent, family, momentum, amplitude, and aggregate verification owners | Independent reconstruction is installed. Exact verifier-record compatibility is deliberately not retained. |
| `nonflat/serialization.py` and nonflat schema documents | Canonical single-parent, family, and cohesive aggregate typed bytes | Deliberate replacement, not wire compatibility. |
| `truncation/definition.py`, `experiment.py`, `results.py`, and `verify.py` | Embedded rank-two truncation request, analyzer, results, independent reference, and verification | All 561 direct-v2 rows at parent scale `1.0` agree; the donor's other four parent-scale slices are not retained in direct v2. |
| `truncation/serialization.py` and truncation schema documents | Cohesive aggregate typed bytes | Deliberate replacement, not wire compatibility. |
| `analysis.py` | No installed equivalent of the pandas `DiagnosticBundle` table API | Not dynamically activated in this audit; still consumed by a maintained development entrypoint and test. |
| `analysis_plot.py` | Authenticated installed visualizers for the closed direct-lifecycle inventory | Not full behavioral parity. The donor still owns additional development-only diagnostic compositions and is still imported by maintained files. |
| `__init__.py` export surfaces | Deliberate installed public exports from cohesive owners | Names and package layout are not compatibility contracts. |

## Immutable numerical comparison

| Compared channel | Scalar comparisons | Maximum absolute difference | Disposition |
|---|---:|---:|---|
| Parent-family continuum, five scales and 33 amplitudes | 2,145 | `9.6173069508154185e-15` | Agrees. |
| Nonflat final-mesh point channels | 455 | `3.0878077872387166e-15` | Agrees. |
| Nonflat hopping-power map | 1,690 | `2.3314683517128287e-15` | Agrees. |
| Nonflat selected hopping tails | 126 | `8.3266726846886741e-17` | Agrees. |
| Adaptive-amplitude levels | 24 | `6.661338147750939e-16` | Values and four failed level dispositions agree; installed disjoint quarter-point validation remains additional evidence. |
| Momentum refinement excluding the expanded parent diagnostic | 48 | `1.887379141862766e-15` | Agrees. |
| Parent-scale `1.0` truncation consequences | 14,025 | `4.6185277824406512e-14` | Agrees. |

The mapped comparison contains 18,513 scalar checks. The maximum observed difference is
below `1.0e-13`.

### Momentum-disposition difference

The donor defines `maximum_parent_diagnostic_change` from the parent quantities it then
owned. Its four values are at roundoff scale, from
`2.993730229760529e-16` through `7.764221573563186e-16`, and all four donor refinement
rows say `within_draft_tolerances=true`.

The installed owner includes the primitive-link Frobenius residual in the parent
qualification diagnostic. Its adjacent-mesh changes are:

- `32 -> 64`: `0.00729834199405332`;
- `64 -> 128`: `0.0036586456823999524`;
- `128 -> 256`: `0.0018305094665233494`; and
- `256 -> 512`: `0.0009154031332538671`.

These values decrease but exceed `1.01e-8`. The installed outcome is therefore
`MomentumRefinementUnresolved`, whereas the donor reports convergence. This is not a
floating-point parity defect and must not be hidden by tolerance widening or by dropping
the installed diagnostic.

### Truncation-family coverage difference

The donor truncation table contains 2,805 rows: 561 rows at each parent hopping scale
`0.0`, `0.25`, `0.5`, `0.75`, and `1.0`. Direct v2 retains 561 truncation rows only at
scale `1.0`. The installed truncation owner accepts other parent scales, but capability
alone is not retained numerical parity for the missing 2,244 rows. Direct v2 must not be
rerun or relabeled to fill this gap.

The donor parent-family summary also retains adjacent-mesh convergence summaries for all
five parent scales. The direct-v2 family channel retains each final mesh member, while
its separate momentum-refinement channel evaluates only scale `1.0`. Those summaries
therefore do not have a one-to-one retained successor.

## Remaining live consumers

At the audited revision, the workflow tree was not dormant. Six maintained development
entrypoints imported it:

- `run_10_flat_control.py`;
- `run_11_nonflat_control.py`;
- `run_12_parent_family_control.py`;
- `run_13_truncation_control.py`;
- `run_14_truncation_mesh_stability.py`;
- `run_15_five_scale_evidence_assessment.py`; and
- `run_16_diagnostic_packaging.py`.

At the audited revision, four calculation-local test modules also imported it. The
diagnostic entrypoint and its test consumed the pandas-dependent `analysis.py` and
`analysis_plot.py` surfaces. Removing `workflow/` then would have broken these maintained
routes even though the direct calculate, verify, and render scripts were independent of
it.

## Subsequent consumer-migration status

After this immutable audit baseline, five scientific producer entrypoints and three
producer-composition tests were migrated to `rank2_control_analysis.py` and installed
`ksdft2effmass.periodic1d` request, analyzer, canonical-record, and independent-verifier
owners. The diagnostic-packaging entrypoint and test were subsequently migrated to
`development_diagnostics.py`, which validates immutable standard-library CSV projections,
uses canonical typed records for the catalog and separate range-decision channels, and
renders without recomputing scientific analyses. The migration preserved historical CSV
column contracts but did not execute the full development producers or alter any
development or retained artifact. No extracted JSON schema, pandas compatibility layer,
or parallel wire format was introduced; installed canonical serialization continues to
own byte representations.

No maintained Python consumer now imports `workflow/`. A subsequent byte-bound
[`five-scale-consistency.md`](five-scale-consistency.md) assessment covers
the complete stored five-scale grids, summaries, and cutoff-decision projections without
rerunning their scientific analyses. This progress does not amend the 18,513-value
direct-v2 comparison, authenticate missing retained coverage, establish momentum
semantic equivalence, or authorize donor retirement.

## Findings and retirement disposition

1. **Retained numerical overlap is strong but incomplete.** The mapped parent-family,
   nonflat, adaptive, and scale-one truncation values agree to less than `1.0e-13`.
2. **Momentum outcome semantics are not equivalent.** The installed, broader parent
   diagnostic correctly leaves refinement unresolved under the declared threshold,
   while the donor reports convergence.
3. **Four truncation-family slices and five-scale refinement summaries lack retained
   direct successors.** Installed capability is not the same as an authenticated
   retained result.
4. **Source successors do not create missing retained evidence.** The flat scientific
   core has an installed successor, and the diagnostic bundle now has a typed
   calculation-local successor, but neither fact adds authenticated direct-v2 family
   coverage or amends this immutable audit baseline.
5. **The donor still had maintained consumers at the audited revision.** Retirement
   would have broken six development entrypoints and four tests.

**Retirement disposition: not ready.** Keep `workflow/` tracked and unchanged. This
conclusion does not identify a defect in the passing unsealed direct-v2 lifecycle
evidence; it limits only the donor-retirement claim.

The read-only [`scientific-claim-use-audit.md`](scientific-claim-use-audit.md) traces
those five-scale surfaces into the active Ragasa2026a v3 claim and figure graph.
Scientific authority then selected maintenance in
[`five-scale-maintenance-disposition.md`](five-scale-maintenance-disposition.md). The
maintained source consumers now use installed scientific owners or the typed
calculation-local diagnostic boundary, without changing direct v2. The donor's pandas
implementation and dataframe API need no successor. Keep the donor tracked until named
maintained-scope parity evidence and a new retirement review dispose the unresolved
semantic and retained-evidence gaps. Do not describe the donor and installed momentum
dispositions as equivalent.
