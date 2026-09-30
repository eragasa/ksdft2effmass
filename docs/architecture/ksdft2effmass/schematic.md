# `ksdft2effmass` implementation schematic

```mermaid
flowchart TB
    Root["ksdft2effmass"] --> Publications["ksdft2effmass.publications"]
    Publications --> Authoring["publications.authoring"]
    Authoring --> Adapters["authoring.adapters"]
    Ingestion["Project Koios Ingestion"] --> Adapters
    Search["Project Koios Search"] --> Adapters
    References["Project Koios References"] --> Adapters
    Abstracts["authorized APS abstracts<br/>ad-hoc scope"] --> Adapters
    Ollama["fixed-model Ollama<br/>127.0.0.1 only"] --> Adapters
    Adapters --> Cache["0600 ignored-cache<br/>response observability"]
    Adapters -. "bounded inference port" .-> Authoring
    Authoring -. "proposal only; no write" .-> Manuscript["read-only manuscript target"]
```

Solid arrows include documented Python ownership and direct typed adapter imports.
The dotted arrows are injected composition boundaries rather than package-owned
effects.
