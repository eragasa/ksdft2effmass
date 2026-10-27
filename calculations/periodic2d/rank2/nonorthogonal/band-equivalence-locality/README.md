# Periodic 2-D rank-two nonorthogonal band-equivalence/locality calculation

This calculation owns the triangular-Bravais/honeycomb-basis controlled-model execution used by the Paper B development study. The retained subspace has rank two; this is not a graphene material calculation.

- Root `run_*_development.py` files are the bounded calculation-workflow entrypoints.
- Root `plot_development.py` is the calculation-owned plotting entrypoint.
- `simulations/development/results/` is the replaceable output location.
- `analysis/development/` documents derived diagnostics and owns generated figures.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The experiment protocol remains at [`experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/`](../../../../../experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/). Current outputs are development evidence, not a retained production package or external material validation.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Triangular-Bravais/honeycomb-basis nominal calculation | Present as bounded synthetic development work; not graphene. |
| First and second mesh refinements | Present separately; one first-refinement pointwise shell decision changed and remains part of the record. |
| Basis/geometry and frame-transport diagnostics | Family-specific inputs to preserve rather than inherit from the orthogonal family. |
| Independent verification and schemas | Distributed across experiment/calculation and comparison-local surfaces; canonical typed ownership is unresolved. |
| Plotting and technical report | Development rendering exists; it is not authenticated from a canonical execution package. |
| Experiment migration source and dimensional comparison | 12 tracked files under the periodic-2D nonorthogonal container/family path must move here or receive a provenance-only disposition. The downstream aggregate does not transfer this family's identity or tolerances. |
