# `FiniteMomentumMeshDomain`

**Defined in:** `operators.representations.domains`

A final immutable carrier for one centered uniform finite momentum mesh.

```python
FiniteMomentumMeshDomain(
    identifier: str,
    mesh: CenteredUniformMesh,
    coordinate_convention_id: str,
    sample_role: MomentumSampleRole,
)
```

Derived properties are `identity`, `cardinality`, and `dimension`.

- [Scientific meaning](scientific.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematic](schematics.md)
