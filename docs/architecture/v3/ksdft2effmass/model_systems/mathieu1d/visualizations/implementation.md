# Implementation

`Mathieu1dVisualizationData` moves unchanged to `data.py`; its typed field inventory,
validation, canonical JSON bytes, and verifier-derived digest remain stable.
`Mathieu1dVisualizationPlotEnum` moves unchanged to `inventory.py`.

The existing plot and subplot actions are grouped with the two cohesive output figures:

- `finite_reduction.py` owns refinement, band, hopping, and range panels and their
  complete finite-reduction layout;
- `publication_summary.py` owns the compact range-error and omitted-block layout.

`Mathieu1dVisualizer` moves to `visualizer.py`. It binds the projection and
`Mathieu1dVerification`, authenticates them before Matplotlib construction, composes the
two root PNG renderers, and requires exact enum coverage.

No figure module calls `Mathieu1dAnalyzer`, reconstructs a transform, truncates a hopping
model, fits a range, or selects a scientific conclusion. Atomic publication remains in
the direct render script.
