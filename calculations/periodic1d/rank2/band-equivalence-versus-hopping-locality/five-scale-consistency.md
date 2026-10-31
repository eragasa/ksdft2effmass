# Five-scale artifact consistency

## Scope

This assessment binds the complete maintained five-scale development artifacts without
rerunning a scientific calculation. It covers source-byte integrity, complete product
grids, internally reproduced summaries, minimum tolerance-satisfying support decisions,
retained-evidence coverage, and the distinct donor and installed momentum dispositions.

The executable owners are in
[`five_scale_consistency.py`](five_scale_consistency.py). The aggregate
`FiveScaleConsistencyAssessor` only composes five focused actions:

1. `FiveScaleSourceIntegrityAssessor`;
2. `FiveScaleTableConsistencyAssessor`;
3. `FiveScaleCutoffConsistencyAssessor`;
4. `FiveScaleEvidenceCoverageAssessor`; and
5. `FiveScaleMomentumDispositionAssessor`.

Each action has a conventionally named `test__ClassName__assess.py` module under
[`tests/`](tests/); aggregate composition is covered by
[`test__FiveScaleConsistencyAssessor__assess.py`](tests/test__FiveScaleConsistencyAssessor__assess.py).
The actions compose the immutable CSV loader in `development_diagnostics.py` and
canonical typed admission of the direct-v2 calculation. They do not call a production
analyzer or independent scientific verifier.

The aggregate result has five explicit immutable components:

1. source-artifact integrity;
2. table-reproduction consistency;
3. cutoff-decision consistency;
4. retained-evidence coverage; and
5. momentum disposition.

No component represents scientific validation or numerical parity.

## Bound inputs

| Source | SHA-256 |
|---|---|
| `parent-family-continuum.csv` | `1ab9a26544f70f2f53ad798f6ab61aa9f72b7f065f5dc3fa67ff84f8b5557597` |
| `parent-family-summary.csv` | `aa249ec7b19b8126e906f10ee657e79998c81980e6531440d2da2c0359c1aeb9` |
| `truncation-consequences.csv` | `84c1769c98d737f2e65e53c1ea105cca9c01e7f36c39713112c6649a2f92c40c` |
| `truncation-refinement.csv` | `bf3b3c80cc7b9ee37da00ad02735368a9b1b5b281d5af56098f77a2cc0d09b20` |
| `truncation-summary.csv` | `5c18c4d8506f0a4e54b921cb7d508862c9ed8067bf879a1fe5e403a8a15a7575` |
| direct-v2 `calculation.json` | `29c1a2bdd7ec85b721cb9c9248ba0961cd1472278cf79a33f641eaa9e657dd01` |

These identities establish the bytes assessed, not scientific validity.

## Complete-grid and table-reproduction checks

The assessment admits exactly:

- five parent hopping scales: `0.0`, `0.25`, `0.5`, `0.75`, and `1.0`;
- 33 amplitudes from zero through $\pi/4$;
- all 17 integer cutoffs $R_c=0,\ldots,16$; and
- construction meshes 128, 256, and 512 with disjoint evaluation meshes
  $4N+1$.

It checks the following complete inventories:

| Table | Rows | Internal reproduction |
|---|---:|---|
| Parent-family continuum | 165 | Complete five-by-33 product grid. |
| Parent-family summary | 5 | Ten endpoint values reproduce the continuum exactly. |
| Truncation consequences | 2,805 | Complete five-by-33-by-17 product grid. |
| Truncation summary | 5 | 45 maxima and endpoint values reproduce the consequence table exactly. |
| Truncation refinement | 495 | Complete five-by-three-by-33 product grid. |

At construction mesh 256, the assessment independently reapplies the declared minimum
tolerance-satisfying support rule to every parent scale, amplitude, and distinct
spectral/Hamiltonian channel. All 660 selected ranges agree with the historical
`*_first_passing_range` fields in `truncation-refinement.csv`; all 1,252 applicable
satisfying and preceding error values agree exactly. Every stored satisfying value is at
or below `1.0e-8`, and every applicable preceding value is above it. The four channel
decisions have zero changes from 128 to 256 and zero changes from 256 to 512.

These are table-reproduction and decision-consistency checks over existing bytes. They
do not reproduce the Hamiltonian analyses that originally generated those bytes.

## Evidence and semantic boundaries

The assessment deliberately preserves two gaps:

1. All five historical summary rows say `converged` under the donor's narrower momentum
   diagnostic. Canonical direct v2 retains
   `Periodic1DEmbeddedSubspaceRank2MomentumRefinementUnresolved` under the installed
   broader diagnostic. The assessment therefore leaves
   `FiveScaleMomentumDisposition.semantic_equivalence_established` false.
2. Direct v2 contains 561 scale-one truncation rows. The development table contains
   2,805 rows, leaving 2,244 rows outside direct-v2 retained coverage.
   `FiveScaleEvidenceCoverage.complete_retained_coverage` is therefore false.

The assessment establishes complete maintained source integrity and internal table and
decision consistency. It does **not** establish complete retained numerical parity,
scientific validity, or donor-retirement readiness. A new execution must reproduce and
independently verify the five-scale scope before the missing retained-evidence gap can be
reconsidered. The required execution design is recorded in
[`complete-five-scale-execution-plan.md`](complete-five-scale-execution-plan.md).
