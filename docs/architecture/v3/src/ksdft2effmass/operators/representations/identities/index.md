# `ksdft2effmass.operators.representations.identities`

## Source

`python/src/ksdft2effmass/operators/representations/identities.py`

## Responsibility

The module identifies representation nodes independently of their derivation history. It
owns separate role enums for Bloch-space and cell-hopping carriers, one immutable node
identity, and an identity-only factory.

## Symbols

- [`BlochSpaceRole`](BlochSpaceRole/index.md)
- [`CellHoppingRepresentationRole`](CellHoppingRepresentationRole/index.md)
- [`_require_nonempty_exact_string`](_require_nonempty_exact_string/index.md)
- [`RepresentationIdentity`](RepresentationIdentity/index.md)
- [`RepresentationIdentityFactory`](RepresentationIdentityFactory/index.md)

The private string validator is not part of `__all__`.

## Pages

- [Scientific interpretation](scientific.md)
- [Numerical behavior](numerics.md)
- [Implementation](implementation.md)
- [Schematic](schematics.md)
