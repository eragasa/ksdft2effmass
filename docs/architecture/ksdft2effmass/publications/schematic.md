# `ksdft2effmass.publications` schematic

```mermaid
flowchart LR
    Facade["ksdft2effmass.publications facade"] --> Authoring["authoring package"]
    Ingestion["Project Koios Ingestion result"] --> Adapters["exact owner adapters"]
    Retrieval["Project Koios Search result"] --> Adapters
    References["Project Koios References result"] --> Adapters
    Abstracts["authorized APS abstracts"] --> AdHoc["ad-hoc abstract adapter"]
    AdHoc --> AdHocProjection["AdHocEvidenceRetrievalProjection"]
    Adapters --> Projection["EvidenceRetrievalProjection"]
    Projection --> Authoring
    AdHocProjection --> Authoring
    Ollama["fixed-model loopback Ollama"] --> InferenceAdapter["OllamaLoopbackManuscriptInferenceAdapter"]
    InferenceAdapter -. "LocalManuscriptInferencePort" .-> Authoring
    InferenceAdapter --> Cache["0600 ignored-cache observability"]
    Authoring --> Proposal["immutable proposal"]
    Proposal -. "no automatic write" .-> Target["read-only target"]
```

The package facade preserves defining-module class identities. External retrieval is
a collaborator; the package-owned inference adapter is injected through the neutral
port and has only bounded literal-loopback transport.
