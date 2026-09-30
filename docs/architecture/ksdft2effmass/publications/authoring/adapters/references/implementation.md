# `references` adapter implementation

```mermaid
flowchart TD
    CanonicalImport["projectkoios.references.citation_identity"] --> Adapter["references.py"]
    Adapter --> Status["CitationKeyStatus"]
    Adapter --> Snapshot["ProjectedCitationIdentity"]
```

`project` requires exactly one item correlated to the requested bibliographic work.
The result, source projection, and item identities are retained. All five owner
statuses map explicitly. Only `accepted-active-canonical` copies
`canonical_citekey`; there is deliberately no proposed-citekey field in the local
record.
