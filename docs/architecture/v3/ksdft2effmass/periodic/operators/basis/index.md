# `ksdft2effmass.periodic.operators.basis`

## Contract and identity

This module owns the immutable, order-sensitive coordinate identity of a finite periodic
basis. `PeriodicBasisIdentity.coordinates[j]` identifies matrix row and column `j`.
`display_identifier` is descriptive and does not participate in equality or hashing.

Supported coordinate families are labeled components, plane-wave reciprocal indices,
qualified native Wannier orbitals, and Slater--Koster site orbitals.

## Invariants

- the coordinate tuple is nonempty and unique;
- every coordinate has one exact concrete family;
- one identity cannot mix coordinate families;
- coordinate order, spelling, case, indices, ordinals, orbital labels, and explicit
  component/spin absence are semantic;
- no normalization, sorting, alias, permutation, or fallback occurs.

## Dependencies and flow

The module depends only on repository-native serialization records and enums.

```text
analytic definition or qualified provider inventory
  -> family-specific coordinate records
  -> Periodic1DBasisIdentity, Periodic2DBasisIdentity, or Periodic3DBasisIdentity
  -> optional calculation-owned PeriodicBasisInventory composition
  -> model/operator/frame correlation in later reviewed adapters
```

## Serialization

All records use final `BaseTypedRecord` mapping and JSON boundaries. The dimensional
basis wire has schema version 2 and fields `schema_version`, `spatial_dimension`,
`display_identifier`, `family`, and `coordinates`. Coordinate records carry `kind` plus
exact family-specific fields. Deserialization occurs through the intended dimensional
concrete type and rejects a mismatched `spatial_dimension`.

## Scientific boundary

`PeriodicBasisInventoryEntry` and `PeriodicBasisInventory` are generic immutable domain
objects in `periodic.operators.basis_inventory`; they have no dimensional subclasses.
The contained identity supplies the exact spatial dimension. Concrete calculation rank
inventories belong to their calculation composition rather than reusable source.

Basis identity is separate from state-space identity, retained-frame identity, gauge,
embedding, geometry, energy reference, sewing, and artifact provenance. Exact basis
equality alone does not prove physical equivalence, validate provider semantics, or
establish a Wilson-loop claim.

## Mappings

| Source | Tests | Sphinx |
|---|---|---|
| `python/src/ksdft2effmass/periodic/operators/basis.py` | `python/tests/ksdft2effmass/periodic/operators/test__PeriodicBasisIdentity.py` | `doc/sphinx/api/periodic-basis.rst` |
| `python/src/ksdft2effmass/periodic/operators/basis_inventory.py` | `python/tests/ksdft2effmass/periodic/operators/test__PeriodicBasisInventory.py` | `doc/sphinx/api/periodic-basis.rst` |

## Provenance and evidence

The contract follows the repository basis-identity inventory and selected decision in
[`../../basis_embedding/basis-identity-audit.md`](../../basis_embedding/basis-identity-audit.md).
Software-verification tests establish constructor, equality, order, and wire behavior
only. No external calculation or retained scientific evidence is produced.

## Limitations

Provider admission, operator correlation, basis embedding, reciprocal-shift sewing,
and reusable Wilson-loop construction remain separate future work.

## Navigation

- [`PeriodicBasisIdentity`](PeriodicBasisIdentity/index.md)
- [`Periodic1DBasisIdentity`](../../periodic1d/operators/basis/Periodic1DBasisIdentity/index.md)
- [`Periodic2DBasisIdentity`](../../periodic2d/operators/basis/Periodic2DBasisIdentity/index.md)
- [`Periodic3DBasisIdentity`](../../periodic3d/operators/basis/Periodic3DBasisIdentity/index.md)
- [`PeriodicBasisFamily`](PeriodicBasisFamily/index.md)
- [`LabeledComponentBasisCoordinate`](LabeledComponentBasisCoordinate/index.md)
- [`PlaneWaveBasisCoordinate`](PlaneWaveBasisCoordinate/index.md)
- [`WannierOrbitalBasisCoordinate`](WannierOrbitalBasisCoordinate/index.md)
- [`SlaterKosterOrbital`](SlaterKosterOrbital/index.md)
- [`SlaterKosterOrbitalBasisCoordinate`](SlaterKosterOrbitalBasisCoordinate/index.md)
- [Embedding and sewing boundary](../../basis_embedding/index.md)
