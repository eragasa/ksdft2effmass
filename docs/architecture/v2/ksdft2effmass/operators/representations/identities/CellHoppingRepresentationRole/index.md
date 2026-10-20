# `CellHoppingRepresentationRole`

## Status and role

`CellHoppingRepresentationRole` is the implemented Phase 1 semantic `Enum` for a
cell-hopping coefficient field `H_hat: Gamma -> End(V)`.

## Public contract

```python
from ksdft2effmass.operators.representations.identities import (
    CellHoppingRepresentationRole,
)

role = CellHoppingRepresentationRole.complete_declared_inventory
```

Its complete member inventory is:

- `CellHoppingRepresentationRole.complete_declared_inventory`;
- `CellHoppingRepresentationRole.support_truncated`.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)
