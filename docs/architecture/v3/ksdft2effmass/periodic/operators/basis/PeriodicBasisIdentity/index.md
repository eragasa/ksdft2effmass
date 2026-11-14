# `PeriodicBasisIdentity`

## Contract and identity

Abstract frozen, slotted record for the dimension-neutral invariants of one ordered
periodic-basis coordinate inventory. Its `display_identifier` is descriptive; equality
and hashing use the dimensional concrete type and `coordinates`.

## Invariants

Coordinates are a nonempty tuple, unique, and all have the same exact supported type.
Tuple position is represented matrix order. `dimension`, `family`, and
`spatial_dimension` are derived. Plane-wave reciprocal-index rank must equal the
concrete basis spatial dimension.

## Dependencies and flow

It consumes family-specific coordinate records and exposes no analysis or adapter
behavior. Later models, frames, operators, and sewing records may correlate to it.

## Serialization

The version-2 `BaseTypedRecord` wire stores `schema_version`, `spatial_dimension`,
`display_identifier`, `family`, and typed tuple `coordinates`. Reconstruction dispatches
by exact family through a dimensional concrete subclass and rejects dimension mismatch.

## Scientific boundary

Equality is basis-coordinate compatibility only. It is not state-space, gauge,
embedding, geometry, energy, sewing, provenance, or physical-equivalence evidence.

## Mappings

Source: `python/src/ksdft2effmass/periodic/operators/basis.py`. Direct tests:
`python/tests/ksdft2effmass/periodic/operators/test__PeriodicBasisIdentity.py`. Sphinx:
`doc/sphinx/api/periodic-basis.rst`.

## Provenance and evidence

Selected by the [basis-identity decision](../../../basis_embedding/basis-identity-audit.md).
Tests provide software-verification evidence only.

## Limitations

No provider admission or historical-string migration is automatic.

## Navigation

- [Module](../index.md)
- [Embedding boundary](../../../basis_embedding/index.md)
