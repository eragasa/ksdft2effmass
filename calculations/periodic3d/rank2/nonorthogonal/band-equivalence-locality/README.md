# Periodic 3-D rank-two nonorthogonal band-equivalence/locality calculation

This calculation owns the FCC-Bravais/diamond-basis controlled-model execution used by the Paper B development study. The retained subspace has rank two; this is not a bulk-silicon material calculation.

- Root `run_*_development.py` files are the bounded calculation-workflow entrypoints.
- Root `plot_development.py` is the calculation-owned plotting entrypoint.
- `simulations/development/results/` is the replaceable output location.
- `analysis/development/` documents derived diagnostics and owns generated figures.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The experiment protocol remains at [`experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/`](../../../../../experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/). Current outputs are development evidence, not a retained production package or external silicon validation.
