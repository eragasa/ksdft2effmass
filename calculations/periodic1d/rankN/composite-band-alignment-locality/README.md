# Higher-rank basis rotations and hopping range in one dimension

**Status:** development calculation with no stable result format, independently checked result, or permanent checksum-bound run.

This synthetic calculation asks a concrete question: if a momentum-dependent change of
basis preserves the represented energy bands, how much can it lengthen the real-space
hopping matrices, and how much locality can different alignment choices recover? It
compares `3`, `4`, `8`, and `16` retained states; rotation depths `1`, `2`, `4`, and `8`;
and four controls: no alignment, one constant alignment, a separate complete alignment
at each momentum, and the known inverse rotation.

- [`workflow/`](workflow/) contains the code for constructing the synthetic model,
  applying the four alignment choices, calculating hopping matrices, and recording the
  current development results.
- [`run_development.py`](run_development.py) runs the current development calculation.
- [`verify_analytic_controls.py`](verify_analytic_controls.py) checks two formulas on a
  finite grid. It is a sanity check, not an independent verification of the full result.
- [`protocol/`](protocol/README.md) contains the detailed plan for a future fully
  recorded and independently checked calculation.
- [`technical-report/technical_report.tex`](technical-report/technical_report.tex) is the
  calculation-facing report.

The current script writes only a replaceable development summary. The project has not
yet defined the stable JSON result format, implemented an independent full-result
checker, authenticated plotted values, or created a retained run. Proposed two- and
three-dimensional studies are separate future work.

Migration records:

- [`experiment-migration-crosswalk.md`](experiment-migration-crosswalk.md) explains where
  each of the five old experiment files belongs.
- [`experiment-removal-manifest.json`](experiment-removal-manifest.json) records their
  exact hashes and current destinations.
- [`experiment-removal-readiness.md`](experiment-removal-readiness.md) records the
  review and the later separately authorized five-file removal.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Part | What exists now |
|---|---|
| One-dimensional fixed-subspace model and 16 rank/depth cases | Implemented under `workflow/`; outputs are replaceable development summaries. |
| Four alignment choices | No alignment, one constant alignment, separate alignment at each momentum, and the known inverse are implemented and kept distinct. |
| Model construction and numerical operations | Split across calculation-local modules and tests. Reusable behavior still needs reviewed source ownership. |
| Formula checks | A bounded finite-grid sanity check exists; it does not independently verify the full calculation. |
| Historical experiment files | The protocol, README, development runner, formula-check runner, and ignore file were removed from the old experiment path after exact-hash review and separate authorization. Their calculation destinations and recovery revision are recorded in [`experiment-migration-crosswalk.md`](experiment-migration-crosswalk.md). |
| Future variants | Moving-subspace, complex-rotation, restricted-optimizer, two-dimensional, and three-dimensional variants are absent and cannot inherit this result. |
