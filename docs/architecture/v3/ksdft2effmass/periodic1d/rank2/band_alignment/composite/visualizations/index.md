# `ksdft2effmass.periodic1d.rank2.band_alignment.composite.visualizations`

## Purpose and status

This implemented package owns
[`Periodic1DCompositeBandAlignmentVisualizationData`](Periodic1DCompositeBandAlignmentVisualizationData/index.md),
the closed
[`Periodic1DCompositeBandAlignmentVisualizationPlotEnum`](Periodic1DCompositeBandAlignmentVisualizationPlotEnum/index.md),
and
[`Periodic1DCompositeBandAlignmentVisualizer`](Periodic1DCompositeBandAlignmentVisualizer/index.md).
It replaces the removed singular source module. The verified visualization-data bytes
and scientific values remain unchanged; the closed report inventory now contains six
role-specific figures.

```text
periodic1d/rank2/band_alignment/composite/visualizations/
├── __init__.py
├── data.py
├── figures.py
├── inventory.py
└── visualizer.py
```

The root `ksdft2effmass.visualizations.PngFigureRenderer` owns PNG encoding only.

## Closed inventory

The six-member inventory is:

1. `rank2-composite-alignment.png`;
2. `rank2-composite-recovery-controls.png`;
3. `rank2-composite-hopping-diagnostics.png`;
4. `rank2-composite-locality.png`;
5. `rank2-composite-error-channels.png`; and
6. `rank2-composite-error-trajectories.png`.

The hopping-diagnostic figure measures unchanged coefficients. The locality and error
figures apply or evaluate retained-support policies; identical integer ranges do not
make these operations interchangeable.

## Detailed pages

- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
- [Parent package](../index.md)
- [Shared visualization architecture](../../../../../visualizations/index.md)
