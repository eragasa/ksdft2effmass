# Band equivalence and hopping locality in the FCC/diamond context

This aggregate owns the FCC-Bravais/diamond-basis rank-two controlled-model composition,
including matched simple-cubic and FCC Bravais controls. The retained subspace has rank
two. The diamond-basis case is explicitly **not a bulk-silicon calculation**, silicon
parameterization, material validation, or effective-mass result.

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

The reserved nominal identity is `direct-fcc-diamond-rank2-n8`, with construction size
`8`, evaluation size `17`, shift `1/3`, and shell cap `7`. No execution directory is
retained. Current outputs are replaceable development evidence, not convergence,
production, silicon, or publication evidence. The former experiment-tree location is a
legacy forward pointer only.

## Migration inventory

This README owns the local inventory; [`migration.md`](migration.md) owns the distributed
checklist.

| Surface | Current disposition |
|---|---|
| FCC-Bravais/diamond-basis nominal calculation | Bounded synthetic calculation action; explicitly not silicon. |
| First and second refinements | Separate bounded checks; no convergence claim. |
| Basis, geometry, and frame transport | Context-specific operands and outcomes rather than inherited simple-cubic conclusions. |
| Plotting and technical report | Replaceable nominal analysis and a calculation-owned technical report. |
| Legacy experiment donor | The calculation owner holds identity, protocol, bibliography, actions, and reports; the legacy path points forward. |
| Cross-dimensional comparison | Downstream consumer only; it owns neither this context's identity nor thresholds. |
