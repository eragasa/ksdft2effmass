# Band equivalence and hopping locality in the simple-cubic context

This aggregate owns the orthogonal simple-cubic rank-two controlled-model composition.
The retained subspace has rank two; three-dimensional space does not imply retained rank
three. The parent context keeps gauge alignment, frame transport, band equivalence,
hopping locality, and support truncation distinct.

- `run_nominal_calculation.py` calculates and independently verifies the bounded nominal
  request.
- `run_refinement_01.py` and `run_refinement_02.py` own the two bounded mesh-refinement
  actions; refinement remains a separate expensive test gate.
- `render_nominal_analysis.py` writes replaceable nominal analysis figures.
- `simulations/replaceable/` owns replaceable typed outputs.
- `analysis/replaceable/` documents derived diagnostics and generated figures.
- [`protocol/`](protocol/README.md) owns the authoritative research protocol and
  bibliography.
- `technical-report/technical-report.md` records scope and evidence boundaries.

The nominal request uses an `8 x 8 x 8` construction mesh, shifted `17 x 17 x 17`
evaluation mesh, parent scales `0` and `1`, amplitudes `0`, `pi/8`, and `pi/4`, and
complete cubic metric shells through squared radius `9`. No execution directory is
retained. Current outputs are replaceable development evidence, not a convergence result,
production package, material calculation, or publication evidence. The former
experiment-tree location is a legacy forward pointer only.

## Migration inventory

This README owns the local inventory; [`migration.md`](migration.md) owns the distributed
checklist.

| Surface | Current disposition |
|---|---|
| Simple-cubic nominal calculation | Calculation-owned typed nominal action with independent verification; no execution retained. |
| Mesh refinement | Two separate bounded actions; no convergence claim. |
| Frame and geometry diagnostics | Context-specific operands and outcomes remain distinct from the FCC/diamond family. |
| Plotting and technical report | Replaceable nominal analysis and a calculation-owned technical report. |
| Legacy experiment donor | The calculation owner holds identity, protocol, bibliography, actions, and reports; the legacy path points forward. |
| Cross-dimensional comparison | Downstream consumer only; it cannot transfer identity, normalization, tolerance policy, or evidence status. |
