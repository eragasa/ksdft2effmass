# `FiniteMomentumMeshDomain`

## Status and role

`FiniteMomentumMeshDomain` is the implemented Phase 1 DataObject identifying one
Numerics-owned centered uniform momentum mesh, coordinate convention, and sample role.

## Public contract

```python
from ksdft2effmass.operators.representations.domains import FiniteMomentumMeshDomain
```

Constructor state is `identifier`, `mesh`, `coordinate_convention_id`, and
`sample_role`. Public derived properties are `identity`, `cardinality`, and `dimension`.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Code and tests

- Source: `operators/representations/domains.py`
- Tests: `test__FiniteMomentumMeshDomain.py`
