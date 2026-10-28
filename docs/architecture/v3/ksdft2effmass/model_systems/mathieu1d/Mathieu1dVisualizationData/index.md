# `Mathieu1dVisualizationData`

Implemented immutable authenticated projection for both Mathieu1D figures.

`from_result()` selects recorded refinement, parent-band, selected-band, complete-hopping,
and range-diagnostic values from an independently reconstructed
`Mathieu1dCalculationResult`. It computes only presentation forms already implied by
those values, such as coefficient magnitudes and stacked range candidates.

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dVisualizationData
```

The projection owns no inferred threshold, interpolation, fit, or accepted range. Its
canonical typed JSON digest is stored in `Mathieu1dVerification`.
