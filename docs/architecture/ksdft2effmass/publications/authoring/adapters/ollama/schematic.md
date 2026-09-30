# `ollama` schematic

```mermaid
flowchart LR
    Request["ManuscriptInferenceRequest<br/>owner-owned lineage"] --> Bound["UTF-8 byte bound"]
    Bound --> Tags["GET 127.0.0.1 /api/tags"]
    Tags --> Identity["exact model name + digest"]
    Identity --> Chat["POST 127.0.0.1 /api/chat<br/>text + warnings only; no tools"]
    Chat --> Raw["retain exact raw bytes"]
    Raw --> Decode["strict bounded JSON decode"]
    Decode --> Response["ManuscriptInferenceResponse<br/>request lineage + candidate text"]
    Decode -->|"typed rejection"| Rejection["decoded-rejection metadata"]
    Identity -->|"mismatch"| Stop["fail closed"]
    Decode -->|"malformed / tools / overflow"| Stop
```

The host is not configurable and no path reaches a remote service, manuscript, or
bibliography boundary. The model never supplies citation/evidence/marker identities.
