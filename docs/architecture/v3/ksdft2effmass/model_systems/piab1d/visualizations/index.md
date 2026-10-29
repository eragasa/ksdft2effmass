# `ksdft2effmass.model_systems.piab1d.visualizations`

## Purpose and status

This implemented package owns the authenticated PIAB1D projection and closed
thirteen-PNG presentation inventory. It replaces the removed monolithic
`piab1d.visualization` module without changing projection bytes, figure names,
scientific values, or rendering policy.

## Source map

```text
model_systems/piab1d/visualizations/
├── __init__.py
├── data.py
├── inventory.py
├── visualizer.py
└── figures/
    ├── __init__.py
    ├── convergence.py
    ├── decomposition.py
    ├── diagnostics.py
    ├── ladders.py
    └── spectrum.py
```

`data.py` owns `Piab1dVisualizationData`. `inventory.py` owns the closed
`Piab1dVisualizationPlotEnum`. The figure modules are grouped by scientific figure
family rather than one file per class. `visualizer.py` owns only authentication and
exact inventory composition.

## Closed inventory

The package retains exactly thirteen existing plot-enum members and filenames. The move
does not add, remove, rename, merge, or split a figure. Any later inventory change is a
separate public-contract change requiring corresponding verifier projection and direct
render-script review.

## Boundaries

- The byte-owning PIAB1D verifier derives and authenticates every projection field.
- Figure actions calculate no new spectrum, state, norm, convergence result, selection,
  residual, algebraic diagnostic, or decomposition.
- Shared PNG encoding comes from `ksdft2effmass.visualizations`.
- Atomic directory publication and execution-specific hashes remain in
  `calculations/piab1d/run_03_render.py`.
- Historical execution figures and rendering records are not rewritten.

## Detailed pages

- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
- [Parent PIAB1D architecture](../index.md)
- [Shared visualization architecture](../../../visualizations/index.md)
