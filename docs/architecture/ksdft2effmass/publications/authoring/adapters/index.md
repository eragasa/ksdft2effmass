# `ksdft2effmass.publications.authoring.adapters`

This package owns exact outward adapters from pinned Project Koios owner results to
the local manuscript-authoring evidence projection and one bounded fixed-model Ollama
inference adapter. It does not run ingestion, retrieval, citation resolution, remote
inference, or writes.

## Defining modules

- [`ad_hoc`](ad_hoc/index.md) — explicit author-supplied APS abstract projection.
- [`references`](references/index.md) — citation-identity projection.
- [`ingestion`](ingestion/index.md) — transcript selection and exact block pairing.
- [`search`](search/index.md) — rank-preserving final evidence projection.
- [`ollama`](ollama/index.md) — loopback-only fixed-model structured inference.
- [`ollama_retention`](ollama_retention/index.md) — atomic accepted/rejected and
  ordinary/exceptional observability.

## Contents

- [`schematic.md`](schematic.md) — owner-result composition.
- [`implementation.md`](implementation.md) — dependency and failure boundaries.

```{toctree}
:hidden:

schematic
implementation
ad_hoc/index
references/index
ingestion/index
search/index
ollama/index
ollama_retention/index
```
