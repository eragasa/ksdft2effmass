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

## Analysis order

This downstream owner runs only after the four contributing rank-two families reach the
cross-family stage of the shared
[periodic analysis order](../periodic/multiband/analysis-order.md). Analyze:

1. authenticate each family-owned nominal result, verification, basis/gauge/energy
   conventions, geometry, and evidence status;
2. establish which operands and normalizations are comparable without changing any
   family threshold or identity;
3. compare frame-transport and band-equivalence diagnostics;
4. compare tolerance behavior using family-owned limits;
5. compare physical shell/radius and shell--scale landscapes without transferring shell
   indices between metrics;
6. retain strain-path channels as separately identified inputs outside the nominal four-
   family lifecycle;
7. independently verify the comparison projection; and
8. render only authenticated derived values.

If any source is absent, unverified, or inapplicable, the dependent comparison remains
unavailable or unresolved rather than being reconstructed from plots or replaced by
zero.

## Migration inventory

This README owns the complete local inventory; [`migration.md`](migration.md) owns its
distributed checklist.

| Surface | Current disposition |
|---|---|
| Four family dependencies | Periodic 2-D/3-D orthogonal/nonorthogonal results and refinements; each remains independently owned and authenticated. |
| Former family schemas and serializers | Removed; canonical typed records own current wire bytes. |
| Shell--scale decision landscape | Historical development output only; its custom workflow surface was removed. |
| Synthetic strain studies | Context identities, protocols, and executable composition are calculation-owned under `periodic2d_rank2_rhombic_path/` and `periodic3d_rank2_bain_path/`; legacy experiment paths are forward pointers. They remain outside this nominal lifecycle. |
| Frame-transport diagnostics | Reusable behavior remains with the installed analysis owner. |
| Experiment migration source | Duplicate plotting entrypoints and analysis-path contracts are retired. The experiment path retains its identity README and comparison protocol. |
