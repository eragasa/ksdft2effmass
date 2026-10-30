# Periodic 3-D rank-two nonorthogonal band-equivalence/locality calculation

This calculation owns the FCC-Bravais/diamond-basis controlled-model execution used by the Paper B development study. The retained subspace has rank two; this is not a bulk-silicon material calculation.

- `run_01_calculation.py`, `run_02_verification.py`, and `run_03_render.py`
  install the nominal typed direct lifecycle without retaining an execution.
- Root `run_*_development.py` files remain bounded development and refinement
  entrypoints outside the nominal direct lifecycle.
- Root `plot_development.py` is the calculation-owned development plotting entrypoint.
- `simulations/development/results/` is the replaceable output location.
- `analysis/development/` documents derived diagnostics and owns generated figures.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The experiment protocol remains at [`experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/`](../../../../../experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/). The reserved nominal identity is `direct-fcc-diamond-rank2-n8`, with construction size 8, evaluation size 17, shift $1/3$, and shell cap 7. No execution directory is retained. Current outputs are development evidence, not a retained production package, silicon calculation, or external material validation.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| FCC-Bravais/diamond-basis nominal calculation | Present as bounded synthetic development work; not silicon. |
| First and second mesh refinements | Present separately and remain bounded numerical checks rather than convergence evidence. |
| Basis/geometry and frame-transport diagnostics | Family-specific surfaces to preserve rather than inherit from the simple-cubic family. |
| Independent verification and schemas | The nominal direct composition uses domain-owned typed request, result, verification, projection, execution, and rendering records plus independent finite-sum shell-power checks. Refinement records remain separate. |
| Plotting and technical report | Authenticated nominal rendering is installed and tested in temporary execution roots; no direct execution is retained. Historical development rendering remains separate. |
| Experiment migration source and dimensional comparison | 12 tracked files under the periodic-3D nonorthogonal container/family path must move here or receive a provenance-only disposition. The downstream aggregate owns neither this family's identity nor thresholds. |
