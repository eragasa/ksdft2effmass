# `ksdft2effmass.model_systems.qho1d.visualizations`

## Purpose and status

This implemented package owns the authenticated QHO1D spatial-truncation projection and
closed three-PNG inventory. It replaces the removed monolithic `qho1d.visualization`
module without changing projection bytes, plot names, numerical content, or rendering
policy.

## Source map

```text
model_systems/qho1d/visualizations/
├── __init__.py
├── data.py
├── inventory.py
├── visualizer.py
└── figures/
    ├── __init__.py
    ├── diagnostics.py
    ├── distortion.py
    └── eigenstates.py
```

The closed inventory remains:

- QHO1D eigenstates;
- state/eigenvalue distortion; and
- spatial-refinement and residual diagnostics.

Exact filenames remain owned by `Qho1dVisualizationPlotEnum` and do not change in the
package migration.

## Boundaries

The verifier derives every projected finite-grid, analytical-state, aligned-state,
energy, distortion, Gram-defect, and residual value. Figure actions arrange those values
only. They do not solve the oscillator, select a state, align eigenvectors, calculate a
Gram matrix, or recompute a norm.

Shared authentication and PNG encoding come from `ksdft2effmass.visualizations`.
Filesystem publication remains in `calculations/qho1d/run_03_render.py`.

## Detailed pages

- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
- [Parent QHO1D architecture](../index.md)
- [Shared visualization architecture](../../../visualizations/index.md)
