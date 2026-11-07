# `ksdft2effmass.operators.representations.domains`

## Source

`python/src/ksdft2effmass/operators/representations/domains.py`

## Responsibility

The module owns finite ordered carrier domains used by represented fields. Momentum
samples compose the Numerics-owned centered mesh. Translation samples retain an explicit
ordered integer-vector inventory.

## Symbols

- [`FiniteDomainABC`](FiniteDomainABC/index.md)
- [`MomentumSampleRole`](MomentumSampleRole/index.md)
- [`_require_nonempty_exact_string`](_require_nonempty_exact_string/index.md)
- [`FiniteMomentumMeshDomain`](FiniteMomentumMeshDomain/index.md)
- [`FiniteTranslationDomain`](FiniteTranslationDomain/index.md)

Only the four names listed in `__all__` are public; the string validator is documented as
a private module invariant.

## Pages

- [Scientific interpretation](scientific.md)
- [Numerical behavior](numerics.md)
- [Implementation](implementation.md)
- [Schematic](schematics.md)
