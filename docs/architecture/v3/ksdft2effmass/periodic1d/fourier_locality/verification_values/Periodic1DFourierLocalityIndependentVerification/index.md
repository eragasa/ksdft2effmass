# `Periodic1DFourierLocalityIndependentVerification`

## Responsibility

Immutable value containing the named comparisons produced by the direct reference
verifier for one admitted calculation result and verifier-owned visualization projection.

The class is an internal scientific value exposed deliberately for typed verification
composition. It stores comparison values only; it is not a reconstructed result,
projection, aggregate verification, or evidence package.

## Invariants

- The comparison mapping is nonempty and immutable.
- Comparison names are nonempty strings and unique by mapping construction.
- Every value is a `MaximumAbsoluteErrorComparison` with explicit typed operands and
  tolerances.
- Scientific and `visualization_...` names remain separable for aggregate composition.
- No producer object, result object, projection object, or filesystem path is retained.

## Public import

```python
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityIndependentVerification,
)
```

## Pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning module](../index.md)
