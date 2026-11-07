# `ksdft2effmass.operators.transformations`

## Implemented purpose

This package owns typed identity and nominal computational contracts for directed changes
between representation identities. It does not currently implement a numerical
transformation operation.

## Source inventory

| Source | Implemented responsibility |
|---|---|
| [`__init__.py`](__init__/index.md) | package documentation only; no re-exports |
| [`identities.py`](identities/index.md) | transformation-kind enum, directed edge identity, identity-only factory |
| [`base.py`](base/index.md) | non-generic nominal request, result, and request-bound transformation ABCs plus protected kind validators |

Source root:
`python/src/ksdft2effmass/operators/transformations/`.

## Documentation bundle

- [Scientific interpretation](scientific.md)
- [Numerical representation](numerics.md)
- [Implementation and ownership](implementation.md)
- [Schematics](schematics.md)

## Status

The identity contracts were introduced at commit
`ed9522dd25c33f2473b2a8320f5fafeeb56ece60`; the non-generic request-bound ABC correction
is currently an uncommitted Phase 1 amendment. No operation-specific request, result, or
transformation exists in this package yet. `TransformationIdentityFactory` constructs metadata;
it is not a numerical transformation factory.
