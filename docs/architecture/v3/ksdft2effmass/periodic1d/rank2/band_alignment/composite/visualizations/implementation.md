# Implementation

`Periodic1DCompositeBandAlignmentVisualizationData` lives in `data.py`, and
`Periodic1DCompositeBandAlignmentVisualizationPlotEnum` lives in `inventory.py`. The
verified data mapping and canonical bytes remain stable while the closed filename
inventory contains six report figures.

`figures.py` owns six cohesive figure actions:

- retained-spectrum and alignment diagnostics;
- paired frame and represented-operator recovery controls;
- hopping-tail diagnostics from unchanged coefficients;
- complete hopping-block locality and retained-support consequences;
- cyclic-conversion and attacked-channel error accounting; and
- all-channel support-truncation error trajectories.

`Periodic1DCompositeBandAlignmentVisualizer` lives in `visualizer.py`. It binds verified
visualization data and `Periodic1DCompositeBandAlignmentVerification`, checks the data
digest before Matplotlib construction, composes one root `PngFigureRenderer` per enum
member, and requires exact inventory equality.

No figure action constructs the parent model, aligns a frame, performs Procrustes
selection, transforms a represented operator, truncates a hopping model, or calculates
an error. Public family exports remain deliberate, and the old singular module remains
removed without a compatibility shim.
