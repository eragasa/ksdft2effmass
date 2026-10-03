# `AbstractDirichletIntervalRepresentation`

## Status

**Accepted nominal-ABC migration contract; implementation pending.**

## Responsibility

`AbstractDirichletIntervalRepresentation(ABC)` declares one read-only
`AbstractUniformGrid1DRepresentation` and one
`AbstractDirichletBoundaryConditionRepresentation`. Concrete interval construction and
cross-object geometry remain owned by the concrete DataObject.

`analysis.model_systems.DirichletInterval` inherits explicitly. The ABC introduces no
operator matrix, boundary forcing, convergence, or scientific-validation claim.

## Related architecture

- [Schematic](schematic.md)
- [Repository-wide migration](../../protocol-to-abc-migration.md)
