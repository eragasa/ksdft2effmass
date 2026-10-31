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

`python/tests/ksdft2effmass/periodic1d/band_equivalence_locality/embedded_subspace/rank2/test__Periodic1DEmbeddedSubspaceRank2DonorParity.py`

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

The workflow tree is not dormant. Six maintained development entrypoints import it:

- `run_flat_development.py`;
- `run_nonflat_development.py`;
- `run_parent_family_development.py`;
- `run_truncation_development.py`;
- `run_truncation_refinement_development.py`; and
- `run_diagnostic_packaging_development.py`.

Four calculation-local test modules also import it. The diagnostic entrypoint and its
test consume the pandas-dependent `analysis.py` and `analysis_plot.py` surfaces.
Removing `workflow/` now would break these maintained routes even though the direct
calculate, verify, and render scripts are independent of it.

## Findings and retirement disposition

1. **Retained numerical overlap is strong but incomplete.** The mapped parent-family,
   nonflat, adaptive, and scale-one truncation values agree to less than `1.0e-13`.
2. **Momentum outcome semantics are not equivalent.** The installed, broader parent
   diagnostic correctly leaves refinement unresolved under the declared threshold,
   while the donor reports convergence.
3. **Four truncation-family slices and five-scale refinement summaries lack retained
   direct successors.** Installed capability is not the same as an authenticated
   retained result.
4. **Flat and pandas diagnostic surfaces do not have named immutable full-donor parity.**
   The flat scientific core has an installed successor, but it is outside direct v2;
   the diagnostic bundle remains calculation-local and was not activated here.
5. **The donor still has maintained consumers.** Retirement would currently break six
   development entrypoints and four tests.

**Retirement disposition: not ready.** Keep `workflow/` tracked and unchanged. This
conclusion does not identify a defect in the passing unsealed direct-v2 lifecycle
evidence; it limits only the donor-retirement claim.

Before another retirement review, scientific authority must choose whether the donor's
five-scale convergence and truncation studies remain maintained capabilities or become
Git-recoverable historical development surfaces. If they remain maintained, port their
effect adapters and diagnostic packaging to installed owners and add named parity tests
without changing direct v2. If they become historical, bind exact source and consumer
recovery identities and separately authorize removal. In either case, do not describe
the donor and installed momentum dispositions as equivalent.
