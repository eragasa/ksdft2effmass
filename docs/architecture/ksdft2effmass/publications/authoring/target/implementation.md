# `target` implementation

```mermaid
flowchart LR
    Caller["externally observed source state"] --> Context["ManuscriptTargetContext"]
    Context --> Hashes["canonical JSON + SHA-256"]
    Hashes --> Ids["revision_id<br/>target_id<br/>span_id"]
```

`ManuscriptTargetContext` is frozen, slotted, and keyword-only. Construction validates
bounded root-relative identity fields and requires the selected text to occur exactly
once in the complete section context. It performs no file or Git access.
