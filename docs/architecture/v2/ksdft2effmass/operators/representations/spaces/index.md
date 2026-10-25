# `ksdft2effmass.operators.representations.spaces` module

## Purpose and status

This implemented Phase 1 module composes existing represented-operator metadata into one
finite-space identity. It does not introduce competing state-space, basis, geometry, or
energy-reference types.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerics](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Contract inventory

| Symbol | Role |
|---|---|
| [`RepresentationSpaceIdentity`](RepresentationSpaceIdentity/index.md) | immutable composition of interpreting space metadata |

Supported provisional import route:

```python
from ksdft2effmass.operators.representations.spaces import (
    RepresentationSpaceIdentity,
)
```

## Represented object

One `RepresentationSpaceIdentity` contains:

- a stable space identifier;
- the existing `operators.records.StateSpace`;
- the existing ordered `operators.records.Basis`;
- the existing `operators.records.Geometry`;
- the existing textual `operators.records.EnergyReference`;
- a mathematical scalar-field identity; and
- a field-coordinate convention identity.

The mathematical scalar-field identity is distinct from NumPy storage dtype. For
example, an identity for complex-number scalars does not assert that every possible
representation uses binary128 or exact complex arithmetic; concrete Phase 1 NumPy fields
separately require `complex128` storage.

## Invariants and failure behavior

- textual identities are exact nonempty built-in strings;
- composed records use the existing exact nominal record classes;
- basis ordering length equals state-space dimension; and
- `dimension` is derived from `StateSpace.dimension`.

Wrong nominal types raise `TypeError`. Empty identifiers or basis/state-space dimension
mismatch raise `ValueError`.

Construction does not infer basis orthonormality, completeness, physical equivalence,
unit compatibility, coordinate compatibility, Hermiticity, or scientific validity.
Those properties require their existing owner or later explicit evidence.

## Dependencies and collaborators

The module imports metadata directly from `operators.records`, not through the
`operators` package initializer. It has no dependency on NumPy, analysis, campaigns,
schemas, serialization, or formal code.

## Code mapping

- Source: `python/src/ksdft2effmass/operators/representations/spaces.py`
- Existing metadata owner: `python/src/ksdft2effmass/operators/records.py`
- Package page: [`../index.md`](../index.md)

## Test mapping

- `python/tests/software_verification/ksdft2effmass/operators/representations/test__RepresentationSpaceIdentity.py`
- existing `StateSpace`, `Basis`, `Geometry`, and `EnergyReference` owner tests under
  `python/tests/software_verification/ksdft2effmass/operators/`

The Phase 1 tests cover composition, exact nominal boundaries, noncoercion, and the
basis/state-space dimension relation. They do not retest generic frozen-dataclass
behavior.

## Sphinx mapping

No Sphinx API page or supported root export is selected in Phase 1.

## Evidence and limitations

Passing tests establish only metadata composition and dimension consistency. They do not
prove that labels describe a physical Hilbert space, that a basis is complete or
orthonormal, that units are compatible, or that two spaces are mathematically or
physically equivalent.
