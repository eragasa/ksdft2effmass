# Periodic 2-D rank-two orthogonal band-equivalence/locality calculation

This calculation owns the square-lattice controlled-model execution used by the Paper B development study. The retained subspace has rank two; the spatial dimension is two.

- Root `run_*_development.py` files are the bounded calculation-workflow entrypoints.
- Root `plot_development.py` is the calculation-owned plotting entrypoint.
- `simulations/development/results/` is the replaceable output location.
- `analysis/development/` documents derived diagnostics and owns generated figures.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The experiment protocol remains at [`experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/`](../../../../../experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/). Current outputs are development evidence, not a retained production package or material calculation.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Square-lattice nominal development calculation | Present as a thin entry point over reusable band-equivalence/locality behavior. |
| First and second mesh refinements | Present as separate entry points and replaceable refinement outputs; no convergence claim. |
| Independent verification and schemas | Development contracts exist across experiment/calculation and comparison-local surfaces; canonical typed ownership is unresolved. |
| Plotting and technical report | Development rendering exists; it is not authenticated from a canonical execution package. |
| Experiment migration source | 11 tracked files under the periodic-2D orthogonal experiment path: protocol, bibliography, development/refinement/plot scripts, analysis records, and ignore contract; all must move here or receive a provenance-only disposition. |
| Cross-dimensional comparison | Downstream consumer only; it must authenticate this family's own result and cannot own its tolerances. |
