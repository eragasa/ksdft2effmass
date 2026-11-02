# Band equivalence and hopping locality in the hexagonal-metric context

This aggregate owns the triangular-Bravais/two-basis-metric controlled-model
composition used by the Paper B development study. The represented band subspace has
rank two; this is not a graphene material calculation. The parent
[`periodic2d_rank2_hexagonal`](../README.md) context keeps gauge alignment, frame
transport, band equivalence, hopping locality, and support truncation distinct.

- `run_nominal_calculation.py` calculates and independently verifies the bounded
  nominal request.
- `run_refinement_01.py` and `run_refinement_02.py` own the two mesh-refinement
  actions; the complete doubling ladder remains a separate expensive test gate.
- `render_nominal_analysis.py` is the calculation-owned replaceable plotting action.
- `simulations/replaceable/` is the replaceable typed-output location.
- `analysis/replaceable/` documents derived diagnostics and owns generated figures.
- [`protocol/`](protocol/README.md) owns the authoritative research protocol and bibliography.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The reserved nominal identity is `direct-triangular-honeycomb-rank2-n16`, with construction size 16, evaluation size 33, shift $1/3$, and shell cap 21. No execution directory is retained. Current outputs are development evidence, not a retained production package, graphene calculation, or external material validation. The former experiment-tree location is a legacy forward pointer only.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Triangular-Bravais/honeycomb-basis nominal calculation | Present as bounded synthetic development work; not graphene. |
| First and second mesh refinements | Present separately; one first-refinement pointwise shell decision changed and remains part of the record. |
| Basis/geometry and frame-transport diagnostics | Family-specific inputs to preserve rather than inherit from the orthogonal family. |
| Independent verification and schemas | The nominal action uses domain-owned typed request, result, and verification records. Refinement assessment records remain separate. |
| Plotting and technical report | Replaceable nominal analysis is tested in temporary calculation roots; no direct execution is retained. |
| Legacy experiment donor and dimensional comparison | Duplicate family entrypoints and analysis-path contracts are retired. The calculation owner now holds the identity, protocol, and bibliography; the legacy experiment path points forward. A downstream cross-result assessment does not transfer this family's identity or tolerances. |
