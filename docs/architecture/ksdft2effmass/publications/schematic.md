# `ksdft2effmass.publications` schematic

```mermaid
flowchart LR
    Facade["ksdft2effmass.publications facade"] --> Authoring["authoring package"]
    Ingestion["Project Koios Ingestion result"] --> Adapters["exact owner adapters"]
    Retrieval["Project Koios Search result"] --> Adapters
    References["Project Koios References result"] --> Adapters
    Adapters --> Projection["EvidenceRetrievalProjection"]
    Projection --> Authoring
    Inference["LocalManuscriptInferencePort"] -. "injected" .-> Authoring
    Authoring --> Proposal["immutable proposal"]
    Proposal -. "no automatic write" .-> Target["read-only target"]
```

The package facade preserves defining-module class identities. External retrieval and
local inference are collaborators, not package-owned implementations.
