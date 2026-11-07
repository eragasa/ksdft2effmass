# Phase 2 — representation nodes

## Status

Phase 2 is a proposed checkpoint, not implemented source. Its scope remains subject to an
operator decision. Creating these documents does not authorize source changes.

## Recommended purpose

Bind one Phase 1 `RepresentationIdentity` to one compatible immutable matrix field. The
node becomes the invariant boundary at which carrier family, complete domain, and
represented rank must agree.

The recommended checkpoint is nodes-only. It introduces no numerical transformation,
representation graph, evidence attachment, campaign adapter, serializer, or schema.

## Proposed public surface

- `OperatorRepresentationABC`: read-only `identity` and `field` interface;
- `BlochOperatorRepresentation`: Bloch identity plus operator field;
- `CellHoppingRepresentation`: cell-hopping identity plus Fourier-block field.

Carrier-specific ABCs are not proposed while each carrier has only one concrete node
leaf.

## Decisions still required

1. Accept or reject a nodes-only Phase 2.
2. Retain the current narrow KSD transformation-role transitions without generalizing
   them during this phase, recommended.
3. Accept fields through the Phase 1 ABC contracts and validate observable invariants,
   rather than requiring exact NumPy leaves, recommended.

## Phase-level views

- [Scientific scope](scientific.md)
- [Numerical scope](numerics.md)
- [Proposed implementation boundary](implementation.md)
- [Schematics](schematics.md)

No `src/` page exists for a Phase 2 node module because that source module has not been
implemented.
