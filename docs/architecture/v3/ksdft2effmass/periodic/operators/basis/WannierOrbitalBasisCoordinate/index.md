# `WannierOrbitalBasisCoordinate`

## Contract and identity

Frozen coordinate keyed by a zero-based provider-native ordinal and an exact
scientifically qualified orbital label.

## Invariants

`native_ordinal` is a nonnegative built-in integer. `qualified_orbital_label` is
nonempty. An ordinal-only or automatically generated label is insufficient admission
evidence.

## Dependencies and flow

A future reviewed provider adapter must preserve native order, qualify orbital labels,
and fail closed before constructing this record and a `PeriodicBasisIdentity`.

## Serialization

The record stores `kind = wannier_orbital`, `native_ordinal`, and
`qualified_orbital_label` through `BaseTypedRecord`.

## Scientific boundary

Artifact identity, Wannier center, spread, frame, gauge, embedding, and localization
provenance remain separate.

## Mappings

Source: `python/src/ksdft2effmass/periodic/operators/basis.py`; tests:
`python/tests/ksdft2effmass/periodic/operators/test__PeriodicBasisIdentity.py`; Sphinx:
`doc/sphinx/api/periodic-basis.rst`.

## Provenance and evidence

The fail-closed rule follows the provider inventory in the basis audit. Tests establish
record behavior only.

## Limitations

No QE/Wannier90 adapter is implemented by this class.

## Navigation

- [Module](../index.md)
- [Basis audit](../../../basis_embedding/basis-identity-audit.md)
