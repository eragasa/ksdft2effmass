# `ksdft2effmass.publications.authoring.adapters.ollama_retention`

This module owns atomic, bounded, no-replace local retention for Ollama response
observability. Raw response bytes, parsed metadata, and terminal authoring metadata are
separate mode-`0600` artifacts.

## Public classes

- [`OllamaRawResponseArtifact`](OllamaRawResponseArtifact/index.md)
- [`OllamaResponseRetention`](OllamaResponseRetention/index.md)

## Contents

- [`schematic.md`](schematic.md) — raw, parsed, and terminal artifact order.
- [`implementation.md`](implementation.md) — atomicity, bounds, permissions, and exclusions.

```{toctree}
:hidden:

schematic
implementation
OllamaRawResponseArtifact/index
OllamaResponseRetention/index
```
