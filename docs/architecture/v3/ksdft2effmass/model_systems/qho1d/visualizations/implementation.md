# Implementation

`Qho1dVisualizationData` moves unchanged to `data.py`, and
`Qho1dVisualizationPlotEnum` moves unchanged to `inventory.py`.
`Qho1dVisualizer` remains constructor-bound to the projection and
`Qho1dVerification`; authentication occurs before any figure action is created.

Figure ownership is grouped by output meaning:

| Figure module | Responsibility |
|---|---|
| `eigenstates.py` | Common-coordinate analytical and finite state presentation. |
| `distortion.py` | State-shape and ordered-energy distortion presentation. |
| `diagnostics.py` | Spatial refinement, Gram defects, discrepancy components, and residual diagnostics. |

Private plot and subplot actions remain beside the cohesive figures that consume them.
The aggregate visualizer composes exactly one renderer for every enum member and rejects
missing or additional output.

The family root continues to export supported visualization types deliberately. The old
singular source module is removed; it does not become a forwarding layer.
