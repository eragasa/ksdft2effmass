# Implementation

`Periodic1DCompositeBandAlignmentVisualizationData` moves unchanged to `data.py`, and
`Periodic1DCompositeBandAlignmentVisualizationPlotEnum` moves unchanged to
`inventory.py`. Their typed mapping, validation, canonical bytes, enum members, and
filenames remain stable.

`figures.py` owns the three cohesive figure actions:

- alignment and transport diagnostics;
- hopping locality and range consequences; and
- interpolation, cyclic-conversion, deliberate-truncation, and total error channels.

`Periodic1DCompositeBandAlignmentVisualizer` moves to `visualizer.py`. It binds the
authenticated projection and `Periodic1DCompositeBandAlignmentVerification`, checks the
projection digest before Matplotlib construction, composes one root `PngFigureRenderer`
per enum member, and requires exact inventory equality.

No figure action constructs the parent model, aligns a frame, performs Procrustes
selection, transforms a represented operator, truncates a hopping model, or calculates
an error. Public family exports remain deliberate, and the old singular module is
removed without a compatibility shim.
