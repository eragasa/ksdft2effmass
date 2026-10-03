# `AbstractUniformGrid1DRepresentation`

## Status

**Accepted nominal-ABC migration contract; implementation pending.**

## Responsibility

`AbstractUniformGrid1DRepresentation(ABC)` declares the read-only coordinate unit,
positive spacing, and interior-point count required by one-dimensional represented
operators. Its properties are abstract; concrete grid invariants remain owned by the
concrete DataObject.

`analysis.model_systems.UniformCartesianGrid1D` inherits this ABC explicitly. Matching
properties without inheritance are rejected. The ABC adds no discretization,
convergence, geometry, or scientific-adequacy claim.

## Related architecture

- [Schematic](schematic.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
