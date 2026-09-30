# `ollama_retention` schematic

```mermaid
flowchart LR
    HTTP["exact bounded response bytes"] --> Raw["raw-&lt;request-id&gt;.json<br/>0600; no replace"]
    Raw --> Decode["strict JSON decode"]
    Decode -->|"typed contract accepted"| Parsed["parsed-&lt;request-id&gt;.json<br/>IDs + warnings + digests"]
    Decode -->|"typed contract rejected"| Rejection["decoded-rejection-&lt;request-id&gt;.json<br/>structure + digests + stable error"]
    Parsed --> Compose["canonical authoring composition"]
    Compose --> Terminal["terminal-&lt;request-id&gt;.json<br/>outcome + issues + proposal ID"]
    Rejection --> Exceptional["exceptional-terminal-&lt;request-id&gt;.json<br/>no response/result ID"]
```

Raw bytes are published before parsing. Decoded-rejection metadata preserves exact
bounded structure, hashes, counts, warnings, and stable failure information without
replacement, target, or evidence excerpts. Exceptional terminal metadata records the
failed run without fabricating a typed response or authoring result.
