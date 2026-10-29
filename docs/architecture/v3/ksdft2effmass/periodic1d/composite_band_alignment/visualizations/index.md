# `ksdft2effmass.periodic1d.composite_band_alignment.visualizations`

## Purpose and status

This implemented package owns
[`Periodic1DCompositeBandAlignmentVisualizationData`](Periodic1DCompositeBandAlignmentVisualizationData/index.md),
the closed
[`Periodic1DCompositeBandAlignmentVisualizationPlotEnum`](Periodic1DCompositeBandAlignmentVisualizationPlotEnum/index.md),
and
[`Periodic1DCompositeBandAlignmentVisualizer`](Periodic1DCompositeBandAlignmentVisualizer/index.md).
It replaces the removed singular source module without changing projection bytes,
filenames, scientific values, or rendering policy.

```text
periodic1d/composite_band_alignment/visualizations/
├── __init__.py
├── data.py
├── figures.py
├── inventory.py
└── visualizer.py
```

The root `ksdft2effmass.visualizations.PngFigureRenderer` owns PNG encoding only.

## Closed inventory

The existing three-member inventory remains:

1. `rank2-composite-alignment.png`;
2. `rank2-composite-locality.png`; and
3. `rank2-composite-error-channels.png`.

## Detailed pages

- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
- [Parent package](../index.md)
- [Shared visualization architecture](../../../visualizations/index.md)
