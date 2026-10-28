# `Periodic1DFourierLocalityEvaluationResult`

## Responsibility

Implemented immutable section owning the common withheld evaluation coordinates and the
lowest two ordered parent eigenvalue fields sampled there. It stores no interpolated,
truncated, or directly fitted candidates.

## Local invariants

- Coordinates are a nonempty strictly increasing `VectorQuantity` in reference units.
- Lowest and adjacent energy vectors have the same shape and unit.
- Adjacent values are no smaller than lowest values pointwise.
- All arrays are finite and operationally immutable.

The calculation-result constructor correlates the coordinates with the configured exact
rational stagger.

```python
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityEvaluationResult,
)
```

## Pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning result module](../index.md)
