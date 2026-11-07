# `ksdft2effmass.operators.representations`

## Implemented purpose

This package owns intrinsic descriptions of finite operator representations:

- ordered finite carrier domains;
- represented-space metadata;
- representation-node identities and carrier-local roles; and
- immutable domain-correlated matrix fields.

The package does not own directed transformation history or numerical transformation
execution. Those belong to the sibling `operators.transformations` package, which may
depend on representations.

## Source inventory

| Source | Implemented responsibility |
|---|---|
| [`__init__.py`](__init__/index.md) | package documentation only; no re-exports |
| [`domains.py`](domains/index.md) | finite-domain ABC, momentum sample roles, momentum meshes, translation inventories |
| [`spaces.py`](spaces/index.md) | composition of represented-space metadata |
| [`identities.py`](identities/index.md) | Bloch and cell-hopping roles, representation identity, identity factory |
| [`fields.py`](fields/index.md) | matrix-field ABC hierarchy and immutable NumPy-backed leaves |

Source root:
`python/src/ksdft2effmass/operators/representations/`.

## Documentation bundle

- [Scientific interpretation](scientific.md)
- [Numerical representation](numerics.md)
- [Implementation and ownership](implementation.md)
- [Schematics](schematics.md)

## Status

The listed modules were introduced at commit
`ed9522dd25c33f2473b2a8320f5fafeeb56ece60`; the explicitly typed field-comparison
correction is currently an uncommitted Phase 1 amendment. A generic node that binds one identity to one
field is not part of this implemented surface.
