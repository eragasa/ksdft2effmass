# `Mathieu1dVisualizationPlotEnum`

Implemented closed two-member artifact inventory:

- `finite_reduction` → `mathieu1d-finite-reduction.png`;
- `publication_summary` → `mathieu1d-publication-summary.png`.

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dVisualizationPlotEnum
```

`Mathieu1dVisualizer` requires exact equality between rendered members and this enum.
Adding or omitting a figure therefore requires an explicit public-contract change.
