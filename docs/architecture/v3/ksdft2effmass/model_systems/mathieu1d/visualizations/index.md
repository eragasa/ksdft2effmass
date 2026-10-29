# `ksdft2effmass.model_systems.mathieu1d.visualizations`

## Purpose and status

This target package owns the authenticated Mathieu1D finite-reduction projection and
closed two-PNG inventory. It replaces the current monolithic `mathieu1d.visualization`
module without changing projection bytes, plot names, finite numerical values, or
rendering policy.

## Target source map

```text
model_systems/mathieu1d/visualizations/
├── __init__.py
├── data.py
├── inventory.py
├── visualizer.py
└── figures/
    ├── __init__.py
    ├── finite_reduction.py
    └── publication_summary.py
```

## Public classes

- [`Mathieu1dVisualizationData`](Mathieu1dVisualizationData/index.md)
- [`Mathieu1dVisualizationPlotEnum`](Mathieu1dVisualizationPlotEnum/index.md)
- [`Mathieu1dVisualizer`](Mathieu1dVisualizer/index.md)

The family root continues to expose these supported public types deliberately. The old
singular module is deleted rather than retained as a compatibility shim.

## Closed figures

1. `mathieu1d-finite-reduction.png` presents the authenticated finite parent,
   transform, and range diagnostics.
2. `mathieu1d-publication-summary.png` presents the compact authenticated range-error
   and omitted-block summary.

## Detailed pages

- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
- [Parent Mathieu1D architecture](../index.md)
- [Shared visualization architecture](../../../visualizations/index.md)
