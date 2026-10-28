# `Periodic1DFourierLocalityAnalyzer`

## Status and responsibility

Implemented stateless action object in
`ksdft2effmass.periodic1d.fourier_locality.analysis`.

Its public calculation method accepts one
`Periodic1DFourierLocalityConfiguration` and returns one fully correlated
`Periodic1DFourierLocalityCalculationResult`.

## Guarantees

- Every configured mesh and support is evaluated exactly once.
- Reusable operations are called through canonical owners.
- Parent, transform, fit, diagnostic, refinement, and decision values are composed into
  their domain records without filesystem effects.
- No passing result is manufactured when a gate fails; failure dispositions remain data
  in the complete result where the contract permits calculation to finish.
- No verification value, digest, figure, or execution metadata is invented by analysis.

## Public import

```python
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityAnalyzer,
)
```

## Related pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning module](../index.md)
