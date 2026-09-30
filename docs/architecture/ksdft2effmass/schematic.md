# `ksdft2effmass` implementation schematic

```mermaid
flowchart TB
    Root["ksdft2effmass"] --> Publications["ksdft2effmass.publications"]
    Publications --> Authoring["publications.authoring"]
    Authoring --> Adapters["authoring.adapters"]
    Ingestion["Project Koios Ingestion"] --> Adapters
    Search["Project Koios Search"] --> Adapters
    References["Project Koios References"] --> Adapters
    LocalInference["injected local inference"] -. "bounded port" .-> Authoring
    Authoring -. "proposal only; no write" .-> Manuscript["read-only manuscript target"]
```

Solid arrows include documented Python ownership and direct typed adapter imports.
The dotted arrows are injected composition boundaries rather than package-owned
effects.
