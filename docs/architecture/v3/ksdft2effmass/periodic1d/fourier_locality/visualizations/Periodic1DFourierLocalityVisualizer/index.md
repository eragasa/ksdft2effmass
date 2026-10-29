# `Periodic1DFourierLocalityVisualizer`

## Responsibility

Authenticated renderer for the complete closed figure inventory.

Its `visualize()` method admits a passing `Periodic1DFourierLocalityVerification` and the exact
`Periodic1DFourierLocalityVisualizationData` whose canonical bytes reproduce the
verification's projection digest. It returns immutable PNG visualization values and
performs no file writes.

## Guarantees

- Failed verification or digest mismatch is rejected.
- Every enum member is rendered exactly once.
- Figure actions consume authenticated values only and expose all declared gap,
  refinement, omitted-norm, decision-mask, passage, and route-diagnostic channels.
- The root `PngFigureRenderer` owns PNG encoding and structural validation.
- No scientific value or decision is calculated during rendering.

## Public import

```python
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityVisualizer,
)
```

## Pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning module](../index.md)
