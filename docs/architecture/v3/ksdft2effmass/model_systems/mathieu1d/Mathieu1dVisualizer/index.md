# `Mathieu1dVisualizer`

Implemented authenticated renderer for the closed Mathieu1D figure inventory.

```python
figures = Mathieu1dVisualizer(
    data=visualization_data,
    verification=verification,
).visualize()
```

Authentication occurs before Matplotlib objects are created. The verification must pass
and its projection digest must match the supplied typed data. Figure actions may choose
layout, axes, and styling but calculate no new scientific values. The shared
`ModelAnalysisPngFigureRenderer` encodes both figures. `visualize()` returns exactly the
two validated immutable PNG values declared by `Mathieu1dVisualizationPlotEnum`.

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dVisualizer
```
