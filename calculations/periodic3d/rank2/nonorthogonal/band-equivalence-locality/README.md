# Periodic 3-D rank-two nonorthogonal band-equivalence/locality calculation

This calculation owns the FCC-Bravais/diamond-basis controlled-model execution used by the Paper B development study. The retained subspace has rank two; this is not a bulk-silicon material calculation.

- Root `run_*_development.py` files are the bounded calculation-workflow entrypoints.
- Root `plot_development.py` is the calculation-owned plotting entrypoint.
- `simulations/development/results/` is the replaceable output location.
- `analysis/development/` documents derived diagnostics and owns generated figures.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The experiment protocol remains at [`experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/`](../../../../../experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/). Current outputs are development evidence, not a retained production package or external silicon validation.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| FCC-Bravais/diamond-basis nominal calculation | Present as bounded synthetic development work; not silicon. |
| First and second mesh refinements | Present separately and remain bounded numerical checks rather than convergence evidence. |
| Basis/geometry and frame-transport diagnostics | Family-specific surfaces to preserve rather than inherit from the simple-cubic family. |
| Independent verification and schemas | Distributed across experiment/calculation and comparison-local surfaces; canonical typed ownership is unresolved. |
| Plotting and technical report | Development products exist but are not authenticated execution artifacts. |
| Experiment migration source and dimensional comparison | 12 tracked files under the periodic-3D nonorthogonal container/family path must move here or receive a provenance-only disposition. The downstream aggregate owns neither this family's identity nor thresholds. |
