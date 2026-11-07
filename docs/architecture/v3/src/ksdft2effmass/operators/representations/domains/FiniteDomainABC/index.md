# `FiniteDomainABC`

**Defined in:** `operators.representations.domains`

`FiniteDomainABC` is the nominal interface shared by finite ordered carriers. It requires
read-only `identity: str` and `cardinality: int` properties and stores no state.

Concrete Phase 1 leaves are `FiniteMomentumMeshDomain` and `FiniteTranslationDomain`.

- [Scientific meaning](scientific.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematic](schematics.md)
