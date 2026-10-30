# Periodic 2-D rank-two orthogonal band-equivalence/locality calculation

This calculation owns the square-lattice controlled-model execution used by the Paper B development study. The retained subspace has rank two; the spatial dimension is two.

- `run_01_calculation.py`, `run_02_verification.py`, and `run_03_render.py`
  own the nominal typed direct lifecycle.
- `executions/direct-square-rank2-n16/` is the retained **CALCULATED RESULT —
  UNSEALED** execution. Its `producers/` directory preserves the exact historical
  script bytes authenticated by the retained lifecycle records; calculation-root scripts
  are the current source surface and are not substituted into that hash chain.
- Root `run_*_development.py` files remain bounded development and refinement
  entrypoints outside the nominal direct lifecycle.
- Root `plot_development.py` is the calculation-owned development plotting entrypoint.
- `simulations/development/results/` is the replaceable output location.
- `analysis/development/` documents derived diagnostics and owns generated figures.
- `technical-report/technical-report.md` records the calculation-facing scope and evidence boundary.

The experiment protocol remains at [`experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/`](../../../../../experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/). The nominal identity is `direct-square-rank2-n16`, with construction size 16, evaluation size 33, shift $1/3$, and shell cap 25. Its retained direct execution is unsealed calculated output, not a production package, convergence result, material calculation, publication acceptance, or sealed evidence.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Square-lattice nominal calculation | Retained as the unsealed typed direct execution `direct-square-rank2-n16`. |
| First and second mesh refinements | Present as separate entry points and replaceable refinement outputs; no convergence claim. |
| Independent verification and schemas | Domain-owned typed request, result, verification, projection, execution, and rendering records authenticate the nominal direct execution, including independent finite-sum shell-power checks. Refinement records remain separate. |
| Plotting and technical report | The direct figure is authenticated from retained execution, result, verification, and projection bytes. Historical development rendering remains separate. |
| Experiment migration source | 11 tracked files under the periodic-2D orthogonal experiment path: protocol, bibliography, development/refinement/plot scripts, analysis records, and ignore contract; all must move here or receive a provenance-only disposition. |
| Cross-dimensional comparison | Downstream consumer only; it must authenticate this family's own result and cannot own its tolerances. |
