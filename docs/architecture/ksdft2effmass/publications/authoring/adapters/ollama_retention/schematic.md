# `ollama_retention` schematic

```mermaid
flowchart LR
    HTTP["exact bounded response bytes"] --> Raw["raw-&lt;request-id&gt;.json<br/>0600; no replace"]
    Raw --> Decode["strict outer JSON decode"]
    Decode -->|"outer contract rejected"| Outer["decoded-rejection-&lt;request-id&gt;.json<br/>outer_response_validation"]
    Decode --> Generated["generated JSON decode and validation"]
    Generated -->|"generated contract rejected"| GeneratedReject["decoded-rejection-&lt;request-id&gt;.json<br/>generated_response_validation"]
    Generated -->|"typed contract rejected"| Typed["decoded-rejection-&lt;request-id&gt;.json<br/>typed_response_construction"]
    Generated -->|"typed contract accepted"| Parsed["parsed-&lt;request-id&gt;.json<br/>IDs + warnings + digests"]
    Parsed --> Compose["canonical authoring composition"]
    Compose --> Terminal["terminal-&lt;request-id&gt;.json<br/>outcome + issues + proposal ID"]
    Outer --> Exceptional["exceptional-terminal-&lt;request-id&gt;.json<br/>no response/result ID"]
    GeneratedReject --> Exceptional
    Typed --> Exceptional
```

Raw bytes are published before parsing. Rejection metadata preserves only bounded safe
structure, hashes, counts, types, and stable failure information without replacement,
target, or evidence excerpts. Exceptional terminal metadata records the failed run
without fabricating a typed response or authoring result.
