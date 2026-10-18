# Non-orthogonal periodic 2-D model-adequacy experiments

## Purpose

This subpackage mirrors experiment families with a non-orthogonal two-dimensional
primitive basis. It is deliberately separate from [`periodic2d`](../periodic2d/index.md)
so geometry, shell semantics, protocols, versions, and evidence cannot be inherited
implicitly from orthogonal families.

## Architecture bundle

- [Science](science.md)
- [Numerics](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Child map

- [Graphene-inspired band equivalence versus hopping locality](band-equivalence-versus-hopping-locality/index.md)

The child has a substantive protocol plus bounded, independently verified three-level
matrix-free tensor actions with replaceable records. It has no immutable version, retained run, or
qualified result. Selection of one triangular lattice does not establish a general 2-D
lattice API.
