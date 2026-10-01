# `inference` implementation

```mermaid
flowchart LR
    Contracts["contracts.py"] --> Inference["inference.py"]
    ProposedCitation["proposal.ProposedCitation"] --> Inference
    Inference --> Author["author.py"]
    Ollama["adapters.ollama"] --> Inference
```

The protocol exposes only `infer(ManuscriptInferenceRequest) ->
ManuscriptInferenceResponse`. Records impose hard size, identity, uniqueness, and
ordering bounds. The request owns the exact citations, complete evidence identities,
and required evidence markers derived from admitted owner evidence. Concrete inference
supplies only candidate text and warnings; the adapter copies request-owned structure
into the typed response. The protocol remains runtime-neutral. The concrete
[`OllamaLoopbackManuscriptInferenceAdapter`](../adapters/ollama/index.md) fixes model
identity, loopback transport, timeout, generation bounds, no-tools policy, and
structured-output parsing; service launch and admitted-evidence selection remain
outside this module.
