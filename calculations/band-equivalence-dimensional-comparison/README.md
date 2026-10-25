# Band-equivalence dimensional comparison calculation

This calculation owns the Paper B cross-family comparison across four rank-two controlled families:

1. periodic 2-D orthogonal;
2. periodic 2-D nonorthogonal;
3. periodic 3-D orthogonal; and
4. periodic 3-D nonorthogonal.

[`band_equivalence_workflow/`](band_equivalence_workflow/) owns the shared canonical schemas, serialization, artifact composition, and verification-document construction for the aggregated experiment family. It is calculation-owned and is not an installed `ksdft2effmass` library API.

Root `plot_development.py` and `plot_shell_scale_decision_landscapes.py` are the aggregation-analysis workflow entrypoints. They load explicit family definitions from their calculation owners and write replaceable comparison artifacts under `analysis/development/generated/`. `simulations/` remains intentionally empty of stage entrypoints because this root compares family calculations rather than defining another physical model. The comparison protocol remains under [`experiments/model-adequacy/band-equivalence-dimensional-comparison/`](../../experiments/model-adequacy/band-equivalence-dimensional-comparison/).

The current comparison is development evidence, not a retained production package or a material-model validation.
