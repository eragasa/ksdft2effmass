# `SquareMatrixFieldABC`

## Status and role

`SquareMatrixFieldABC` is the implemented Phase 1 refinement for matrix fields whose
source and target dimensions coincide.

## Public contract

```python
from ksdft2effmass.operators.representations.fields import SquareMatrixFieldABC
```

It adds the derived `dimension` property to `MatrixFieldABC`.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)
