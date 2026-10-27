# Periodic 3-D rank-two orthogonal band-equivalence/locality calculation

This calculation owns the simple-cubic controlled-model execution used by the Paper B development study. The retained subspace has rank two; three-dimensional space does not imply retained rank three.

- Root `run_*_development.py` files are the bounded calculation-workflow entrypoints.
- Root `plot_development.py` is the calculation-owned plotting entrypoint.
- `simulations/development/results/` is the replaceable output location.
- `analysis/development/` documents derived diagnostics and owns generated figures.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The experiment protocol remains at [`experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/`](../../../../../experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/). Current outputs are development evidence, not a retained production package or material calculation.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Simple-cubic nominal development calculation | Present; spatial dimension three does not change retained rank two. |
| First and second mesh refinements | Present as separate entry points and replaceable results; no convergence claim. |
| Independent verification and schemas | Distributed across experiment/calculation and comparison-local surfaces; canonical typed ownership is unresolved. |
| Plotting and technical report | Development products exist but are not authenticated execution artifacts. |
| Experiment migration source | 11 tracked files under the periodic-3D orthogonal experiment path contain protocol, bibliography, producer/refinement/plot scripts, analysis records, and ignore contract; all must move here or receive a provenance-only disposition. |
| Cross-dimensional comparison | Downstream consumer only; it cannot transfer identity, normalization, or tolerance policy. |
