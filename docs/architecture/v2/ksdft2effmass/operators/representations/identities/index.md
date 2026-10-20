# `ksdft2effmass.operators.representations.identities` module

## Purpose and status

This implemented Phase 1 module owns carrier-local representation roles, immutable
intrinsic node identity, and its carrier-specific factory. Directed transformation kinds
and edge identities belong to [`operators.transformations.identities`](../../transformations/identities/index.md).

## Contract inventory

| Symbol | Role |
|---|---|
| [`BlochSpaceRole`](BlochSpaceRole/index.md) | ambient or retained represented-space enum for a Bloch field |
| [`CellHoppingRepresentationRole`](CellHoppingRepresentationRole/index.md) | complete-inventory or support-truncated enum for a cell-hopping field |
| [`RepresentationIdentity`](RepresentationIdentity/index.md) | node identity composing domain, space, role, and source |
| [`RepresentationIdentityFactory`](RepresentationIdentityFactory/index.md) | carrier-specific construction of node identities |

```python
from ksdft2effmass.operators.representations.identities import (
    BlochSpaceRole,
    CellHoppingRepresentationRole,
    RepresentationIdentity,
    RepresentationIdentityFactory,
)
```

Neither package initializer nor `operators.__init__` re-exports these symbols.

## Construction

`RepresentationIdentity` composes an exact momentum or translation domain,
`RepresentationSpaceIdentity`, its family-local enum role, and a source identity.
`domain_id`, `rank`, `space_id`, and `basis_id` are derived. Cross-family role/domain
combinations fail.

`RepresentationIdentityFactory.create_bloch` and `create_cell_hopping` expose the two
carrier-specific paths without parallel rank or domain-ID inputs.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Code and tests

- Source: `python/src/ksdft2effmass/operators/representations/identities.py`
- Tests: class-matched modules under
  `python/tests/software_verification/ksdft2effmass/operators/representations/`

Passing tests establishes nominal construction and intrinsic compatibility validation
only, not correctness of represented values or their provenance.
