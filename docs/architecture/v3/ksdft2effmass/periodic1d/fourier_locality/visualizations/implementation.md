# Implementation

`Periodic1DFourierLocalityVisualizationData` moves unchanged to `data.py`, and the
closed `Periodic1DFourierLocalityVisualizationPlotEnum` moves unchanged to
`inventory.py`. Their field inventory, validation, canonical projection bytes, enum
members, and filenames remain stable.

`figures.py` owns the two cohesive figure actions:

- `Periodic1DFourierLocalityFigure`; and
- `Periodic1DFourierRouteAgreementFigure`.

`Periodic1DFourierLocalityVisualizer` moves to `visualizer.py`. It binds authenticated
projection data and `Periodic1DFourierLocalityVerification`, authenticates their exact
digest before Matplotlib construction, composes one root `PngFigureRenderer` per enum
member, and requires exact inventory equality.

The package performs no parent-band calculation, Fourier transform, route
reconstruction, fitting, threshold search, or nondominated-set calculation. Public
family exports remain deliberate; the old singular module is deleted without a
compatibility shim.
