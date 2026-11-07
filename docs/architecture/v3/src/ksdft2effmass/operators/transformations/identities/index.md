# `ksdft2effmass.operators.transformations.identities`

## Source

`python/src/ksdft2effmass/operators/transformations/identities.py`

## Responsibility

The module identifies directed derivation edges between representation identities. It
owns the transformation-kind enum, metadata validation, current role-transition policy,
and identity-only construction.

## Symbols

- [`RepresentationTransformationKind`](RepresentationTransformationKind/index.md)
- [`_require_nonempty_exact_string`](_require_nonempty_exact_string/index.md)
- [`_require_compatible_role_transition`](_require_compatible_role_transition/index.md)
- [`TransformationIdentity`](TransformationIdentity/index.md)
- [`TransformationIdentityFactory`](TransformationIdentityFactory/index.md)

The two validators are private and absent from `__all__`.

## Pages

- [Scientific interpretation](scientific.md)
- [Numerical behavior](numerics.md)
- [Implementation](implementation.md)
- [Schematic](schematics.md)
