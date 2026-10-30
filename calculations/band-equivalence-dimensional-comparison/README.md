# Band-equivalence dimensional comparison calculation

This calculation owns the Paper B cross-family comparison across four rank-two controlled families:

1. periodic 2-D orthogonal;
2. periodic 2-D nonorthogonal;
3. periodic 3-D orthogonal; and
4. periodic 3-D nonorthogonal.

The former calculation-local workflow, custom schemas, serializers, artifact constructors,
and aggregation entrypoints have been removed. They are not successors to the canonical
typed owners under `python/src/ksdft2effmass/analysis/model_adequacy/`. Historical
calculation records remain development records; removing the workflow does not promote
or revalidate them. `simulations/` remains intentionally empty of stage entrypoints.
The comparison protocol remains under
[`experiments/model-adequacy/band-equivalence-dimensional-comparison/`](../../experiments/model-adequacy/band-equivalence-dimensional-comparison/).
The calculation root owns the two maintained plotting compositions and their replaceable
outputs under `analysis/development/generated/`.

The current comparison is development evidence, not a retained production package or a material-model validation.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Four family dependencies | Periodic 2-D/3-D orthogonal/nonorthogonal results and refinements; each remains independently owned and authenticated. |
| Former family schemas and serializers | Removed; canonical typed records own current wire bytes. |
| Shell--scale decision landscape | Historical development output only; its custom workflow surface was removed. |
| Synthetic strain studies | Experiment identities remain under `experiments/model-adequacy/`; executable composition is calculation-owned under `periodic2d/rank2/strain-locality/` and `periodic3d/rank2/strain-locality/`. They remain outside this nominal lifecycle. |
| Frame-transport diagnostics | Reusable behavior remains with the installed analysis owner. |
| Experiment migration source | Duplicate plotting entrypoints and analysis-path contracts are retired. The experiment path retains its identity README and comparison protocol. |
