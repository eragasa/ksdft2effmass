# Scientific objects and interpretation

## Mathematical objects

The representations package distinguishes:

1. a finite ordered carrier domain;
2. a represented finite state space with explicit basis, geometry, energy reference,
   scalar field, and coordinate convention;
3. an intrinsic representation-node identity; and
4. finite matrix values correlated with the domain.

A finite representation is not the basis-independent mathematical operator it represents
and is not its derivation history. Directed transformations are separate objects owned by
`ksdft2effmass.operators.transformations`.

## State spaces and bases

`RepresentationSpaceIdentity` composes existing `StateSpace` and ordered `Basis`
identities. Their dimensions must agree. Equal matrix shape does not establish a common
state space or basis; subtraction and entrywise comparison require explicit alignment of
those identities or a declared transformation.

## Geometry, carriers, and coordinates

`Geometry` retains cell, boundary-condition, coordinate-convention, and length-unit
metadata. The representation space separately identifies its field-coordinate
convention. These identities are not silently equated or converted.

Momentum domains compose Numerics-owned centered reduced meshes. Translation domains own
ordered integer-cell inventories. Phase 1 assigns no reciprocal scale, metric, shell,
support radius, or hopping interpretation.

## Roles, storage, and units

Bloch nodes use `BlochSpaceRole.ambient` or `BlochSpaceRole.retained`. Cell-hopping nodes
use `CellHoppingRepresentationRole.complete_declared_inventory` or
`CellHoppingRepresentationRole.support_truncated`. Separate enums prevent roles from
crossing carrier families. “Complete” means complete only on the declared finite
inventory.

The mathematical scalar-field identity is distinct from NumPy dtype. Concrete leaves use
`complex128`; this does not assert exact complex arithmetic. Energy-reference metadata
identifies the zero and unit, but Phase 1 performs no unit conversion or energy alignment.

## Scientific assumptions and exclusions

Phase 1 does not establish isolation, constant rank, Hermiticity, projector identities,
isometry, unitarity, periodicity, sewing, topological triviality, correctness of an
operator construction, transformation correctness, material provenance, model adequacy,
or scientific validation. Those claims require their explicit scientific and evidence
owners.
