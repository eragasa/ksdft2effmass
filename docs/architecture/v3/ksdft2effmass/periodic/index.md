# `ksdft2effmass.periodic`

## Purpose

The package owns dimension-neutral periodic scientific-model vocabulary and explicit
supporting catalogs. The v3 nominal hierarchy is documented under
[`models`](models/index.md).

Dimension-specific model ownership belongs to:

- [`periodic.periodic1d.models`](periodic1d/models/index.md),
- [`periodic.periodic2d.models`](periodic2d/models/index.md), and
- [`periodic.periodic3d.models`](periodic3d/models/index.md).

Finite-rank and rank-two specializations remain nested below each dimensional package.
Each dimensional rank-two model refines its finite-rank owner rather than duplicating a
sibling rank contract. The package root does not re-export model classes. Import the
dimension-neutral contracts
from `ksdft2effmass.periodic.models` and dimensional contracts from their exact nested
owners. The control-model catalog remains explicit at
`ksdft2effmass.periodic.catalog`.

## Basis identity and prospective prerequisites

- [`ksdft2effmass.periodic.operators.basis`](operators/basis/index.md) owns the implemented immutable
  ordered basis identity and its labeled-component, plane-wave, qualified
  Wannier-orbital, and Slater--Koster coordinate families.
- [`basis_embedding`](basis_embedding/index.md) specifies the still-prospective periodic
  basis embedding, Bloch convention, reciprocal-shift sewing map, reciprocal-loop
  ownership, and Wilson-loop boundary. Its
  [`basis-identity audit`](basis_embedding/basis-identity-audit.md) records the selected
  exact compatibility contract and the remaining migration and provider-admission
  boundaries.
