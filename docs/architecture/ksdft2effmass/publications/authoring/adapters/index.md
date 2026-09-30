# `ksdft2effmass.publications.authoring.adapters`

This package owns the exact outward adapters from pinned Project Koios owner results
to the local manuscript-authoring evidence projection. It does not run ingestion,
retrieval, citation resolution, inference, or writes.

## Defining modules

- [`references`](references/index.md) — citation-identity projection.
- [`ingestion`](ingestion/index.md) — transcript selection and exact block pairing.
- [`search`](search/index.md) — rank-preserving final evidence projection.

## Contents

- [`schematic.md`](schematic.md) — owner-result composition.
- [`implementation.md`](implementation.md) — dependency and failure boundaries.

```{toctree}
:hidden:

schematic
implementation
references/index
ingestion/index
search/index
```
