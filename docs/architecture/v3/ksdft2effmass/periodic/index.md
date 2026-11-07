# `ksdft2effmass.periodic`

## Purpose

The package owns dimension-neutral periodic scientific-model vocabulary and explicit
supporting catalogs. The v3 nominal hierarchy is documented under
[`models`](models/index.md).

Dimension-specific model ownership belongs to:

- [`periodic.periodic1d.models`](periodic1d/models/index.md),
- [`periodic.periodic2d.models`](periodic2d/models/index.md), and
- [`periodic.periodic3d.models`](periodic3d/models/index.md).

Rank-two and rank-N specializations remain nested below each dimensional package. The
package root does not re-export model classes. Import the dimension-neutral contracts
from `ksdft2effmass.periodic.models` and dimensional contracts from their exact nested
owners. The control-model catalog remains explicit at
`ksdft2effmass.periodic.catalog`.

## Prospective prerequisites

- [`basis_embedding`](basis_embedding/index.md) specifies the proposed periodic basis
  embedding, Bloch convention, reciprocal-shift sewing map, reciprocal-loop ownership,
  Wilson-loop boundary, and the unresolved `basis_identifier` composition gate.
