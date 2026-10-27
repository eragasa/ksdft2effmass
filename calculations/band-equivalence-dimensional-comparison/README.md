# Band-equivalence dimensional comparison calculation

This calculation owns the Paper B cross-family comparison across four rank-two controlled families:

1. periodic 2-D orthogonal;
2. periodic 2-D nonorthogonal;
3. periodic 3-D orthogonal; and
4. periodic 3-D nonorthogonal.

[`band_equivalence_workflow/`](band_equivalence_workflow/) owns the shared canonical schemas, serialization, artifact composition, and verification-document construction for the aggregated experiment family. It is calculation-owned and is not an installed `ksdft2effmass` library API.

Root `plot_development.py` and `plot_shell_scale_decision_landscapes.py` are the aggregation-analysis workflow entrypoints. They load explicit family definitions from their calculation owners and write replaceable comparison artifacts under `analysis/development/generated/`. `simulations/` remains intentionally empty of stage entrypoints because this root compares family calculations rather than defining another physical model. The comparison protocol remains under [`experiments/model-adequacy/band-equivalence-dimensional-comparison/`](../../experiments/model-adequacy/band-equivalence-dimensional-comparison/).

The current comparison is development evidence, not a retained production package or a material-model validation.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Four family dependencies | Periodic 2-D/3-D orthogonal/nonorthogonal results and refinements; each remains independently owned and authenticated. |
| Family request/result/refinement/verification schemas | Sixteen calculation-local schema documents currently duplicate family wire concerns. |
| Shell--scale decision landscape | Separate request, result, verification, and plotting surface. |
| Synthetic strain aggregation | Separate M0, M1, M2, witness, scan request/result/verification, response plotting, and scan plotting surfaces. |
| Frame-transport diagnostics | Cross-family diagnostic surface with its own tests; not a family result. |
| `band_equivalence_workflow/` | Calculation-local application, schemas, serializers, and document construction to reconcile with canonical typed owners. |
| Experiment migration source | Six tracked files under the dimensional-comparison experiment path contain the protocol, plotting scripts, analysis path contract, and ignore contract; all must move here or receive a provenance-only disposition. |
