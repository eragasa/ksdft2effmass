# `ksdft2effmass.operators.representations.domains` module

## Purpose and status

This implemented Phase 1 module owns finite ordered domain identity for operator
representations. It composes the Numerics-owned `CenteredUniformMesh` and does not create
a parallel mesh-size or coordinate-array API.

The contracts are provisional direct-module imports. They have no wire format.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerics](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Contract inventory

| Symbol | Role |
|---|---|
| [`FiniteDomainABC`](FiniteDomainABC/index.md) | abstract identity and positive cardinality interface |
| [`MomentumSampleRole`](MomentumSampleRole/index.md) | semantic enum with `general`, `construction`, and `evaluation` members |
| [`FiniteMomentumMeshDomain`](FiniteMomentumMeshDomain/index.md) | identified centered uniform momentum domain |
| [`FiniteTranslationDomain`](FiniteTranslationDomain/index.md) | identified ordered unique integer-translation inventory |

Supported provisional import route:

```python
from ksdft2effmass.operators.representations.domains import (
    FiniteMomentumMeshDomain,
    FiniteTranslationDomain,
    MomentumSampleRole,
)

sample_role = MomentumSampleRole.construction
```

## Represented objects

`FiniteMomentumMeshDomain` identifies a one-, two-, or three-dimensional finite
momentum sample domain. Its `CenteredUniformMesh` owns dimension, common axis size,
offsets, point count, and coordinate origin. Construction and evaluation are roles of the
same mesh type rather than subclasses.

`FiniteTranslationDomain` identifies matrices indexed by an explicitly ordered finite
set of integer lattice translations. It assigns no metric, shell, support, physical
radius, or hopping-range interpretation.

## Invariants and failure behavior

### Momentum domain

- `identifier` and `coordinate_convention_id` are exact nonempty built-in strings;
- `mesh` is an exact `CenteredUniformMesh`;
- `sample_role` is a `MomentumSampleRole`, not a raw string;
- `cardinality` is derived from `mesh.point_count`; and
- `dimension` is derived from `mesh.dimension`.

Wrong nominal types raise `TypeError`; empty identifiers raise `ValueError`. Mesh size,
dimension, offsets, finiteness, and overflow behavior remain owned and documented by
`CenteredUniformMesh`.

### Translation domain

- the inventory and each translation are exact tuples;
- the inventory and each vector are nonempty;
- all vectors have one common positive dimension;
- every component is an exact built-in integer, excluding Boolean and numeric strings;
- translations are unique without reordering; and
- integer magnitude uses Python integer semantics with no fixed-width conversion.

Type failures raise `TypeError`; empty, inconsistent, or duplicate inventories raise
`ValueError`.

## Dependency boundary

The module imports only Python standard-library contracts and
`projectkoios.numerics.finite_periodic.meshes.CenteredUniformMesh`. It owns no NumPy array,
geometry, unit, transformation, analyzer, serializer, or campaign behavior.

## Code mapping

- Source: `python/src/ksdft2effmass/operators/representations/domains.py`
- Package page: [`../index.md`](../index.md)

## Test mapping

- `test__MomentumSampleRole.py`
- `test__FiniteMomentumMeshDomain.py`
- `test__FiniteTranslationDomain.py`
- `test__RepresentationIdentity__dependency_boundary.py`

Tests cover mesh-derived cardinality, role typing, ordered translations, dimension,
uniqueness, Boolean and numeric-string rejection, and dependency direction. They do not
test generic frozen-dataclass behavior.

## Sphinx mapping

No Sphinx API page or supported root export is selected in Phase 1.

## Evidence and limitations

Passing tests establish domain software behavior only. They do not establish reciprocal
lattice correctness, mesh convergence, support completeness, physical units, or
scientific suitability. Coordinate values remain derived by the Numerics mesh owner and
are not redundantly retained here.
