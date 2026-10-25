# `MatrixFieldABC`

## Status and role

`MatrixFieldABC` is the implemented Phase 1 abstract contract for finite-domain-correlated
matrix values.

## Public contract

```python
from ksdft2effmass.operators.representations.fields import MatrixFieldABC
```

Implementations expose `domain`, immutable `values`, `source_dimension`, and
`target_dimension`. Exact value equality is defined only between the same concrete leaf.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)
