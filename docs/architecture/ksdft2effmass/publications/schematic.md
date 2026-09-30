# `ksdft2effmass.publications` schematic

```mermaid
flowchart LR
    Facade["ksdft2effmass.publications facade"] --> Authoring["authoring module"]
    Ingestion["external transcript selection"] -. "future exact adapter" .-> Projection["EvidenceRetrievalProjection"]
    Retrieval["external retrieval result"] -. "future exact adapter" .-> Projection
    References["external citation identity"] -. "future exact adapter" .-> Projection
    Projection --> Authoring
    Inference["LocalManuscriptInferencePort"] -. "injected" .-> Authoring
    Authoring --> Proposal["immutable proposal"]
    Proposal -. "no automatic write" .-> Target["read-only target"]
```

The package facade preserves defining-module class identities. External retrieval and
local inference are collaborators, not package-owned implementations.
