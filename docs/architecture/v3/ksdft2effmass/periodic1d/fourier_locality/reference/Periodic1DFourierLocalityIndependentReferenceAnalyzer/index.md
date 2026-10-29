# `Periodic1DFourierLocalityIndependentReferenceAnalyzer`

## Responsibility

Request-bound direct reference action whose
`Periodic1DFourierLocalityIndependentReferenceRequest` admits one
constructor-validated `Periodic1DFourierLocalityCalculationResult` and the
verifier-owned `Periodic1DFourierLocalityVisualizationData`. Its zero-argument
`execute()` returns `Periodic1DFourierLocalityIndependentReference`. Its scientific
operations are cohesive instance methods reading the bound request.

The action independently recomputes declared scientific values with direct NumPy formulas
and does not invoke `Periodic1DFourierLocalityAnalyzer`, production transform actions, or
the production least-squares fitter. Projection checks correlate each rendering field
with its admitted-result source; they do not claim a separately implemented projection.

## Public import

```python
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityIndependentReferenceAnalyzer,
    Periodic1DFourierLocalityIndependentReferenceRequest,
)
```

## Pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning module](../index.md)
