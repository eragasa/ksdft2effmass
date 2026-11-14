# `PeriodicBasisFamily`

## Contract and identity

Closed `StrWireEnum` vocabulary identifying the four coordinate record families, not
project-specific basis instances.

## Invariants

Members are exact strings: `labeled_component`, `plane_wave`, `wannier_orbital`, and
`slater_koster_orbital`. No aliases or normalization exist.

## Dependencies and flow

The enum is consumed by coordinate wires and `PeriodicBasisIdentity.family`.

## Serialization

Owners explicitly call `to_wire()` and `from_wire()` through repository-native record
mappings.

## Scientific boundary

A family identifies coordinate structure only; it establishes no basis compatibility
without the complete ordered coordinates.

## Mappings

Source: `python/src/ksdft2effmass/periodic/operators/basis.py`; tests:
`python/tests/ksdft2effmass/periodic/operators/test__PeriodicBasisIdentity.py`; Sphinx:
`doc/sphinx/api/periodic-basis.rst`.

## Provenance and evidence

The vocabulary follows the selected basis audit. Tests are software verification.

## Limitations

Adding a coordinate family requires a reviewed source, wire, and admission contract.

## Navigation

- [Module](../index.md)
- [`PeriodicBasisIdentity`](../PeriodicBasisIdentity/index.md)
