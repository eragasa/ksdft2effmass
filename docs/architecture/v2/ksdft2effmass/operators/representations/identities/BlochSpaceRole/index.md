# `BlochSpaceRole`

## Status and role

`BlochSpaceRole` is the implemented Phase 1 semantic `Enum` for the represented-space
role of a Bloch operator field `H: K -> End(V)`.

## Public contract

```python
from ksdft2effmass.operators.representations.identities import BlochSpaceRole

role = BlochSpaceRole.retained
```

Its complete member inventory is:

- `BlochSpaceRole.ambient`;
- `BlochSpaceRole.retained`.

These are enum members, not strings and not derivation-stage labels.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Limitation

The enum member does not prove the node's momentum domain, space, basis, rank, or source.
