# `RepresentationIdentityFactory`

## Status and role

`RepresentationIdentityFactory` is the implemented Phase 1 operational constructor for
carrier-compatible immutable representation identities.

## Public contract

```python
from ksdft2effmass.operators.representations.identities import (
    BlochSpaceRole,
    RepresentationIdentityFactory,
)

identity = RepresentationIdentityFactory().create_bloch(
    representation_id="retained-reference",
    domain=momentum_domain,
    space=represented_space,
    role=BlochSpaceRole.retained,
    source_artifact_id="analytic-parent-law.v1",
)
```

The factory provides `create_bloch` and `create_cell_hopping`; neither accepts parallel
rank or domain-ID inputs.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Tests

- `test__RepresentationIdentityFactory.py`
