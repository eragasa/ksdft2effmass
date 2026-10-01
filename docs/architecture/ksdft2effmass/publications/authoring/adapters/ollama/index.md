# `ksdft2effmass.publications.authoring.adapters.ollama`

This module owns the concrete, bounded `LocalManuscriptInferencePort` implementation
for the fixed `qwen3.5:9b` Ollama model and exact SHA-256 digest. It can contact only
an Ollama HTTP service on literal IPv4 loopback, sends no tools, follows no redirects,
uses no proxy, and has no remote fallback. Its sole filesystem capability is required
bounded response observability through [`ollama_retention`](../ollama_retention/index.md).

## Public class

- [`OllamaLoopbackManuscriptInferenceAdapter`](OllamaLoopbackManuscriptInferenceAdapter/index.md)

## Contents

- [`schematic.md`](schematic.md) — fixed loopback request and response flow.
- [`implementation.md`](implementation.md) — bounds, identity, parsing, and runtime gate.

```{toctree}
:hidden:

schematic
implementation
OllamaLoopbackManuscriptInferenceAdapter/index
```
