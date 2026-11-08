# Certification schematics

```mermaid
flowchart LR
    A[Scientific calculation identity] --> R[Certification request]
    V[Numerical-verification artifact] --> R
    S[Source and dependency hashes] --> R
    R --> P[Outward-enclosure producer]
    P --> E[Enclosure artifact]
    E --> I[Independent containment verifier]
    I --> C[Certification result]
    R --> C
    C --> D{Exact disposition}
    D -->|decided pass| AC[Accepted proposition]
    D -->|decided failure| RE[Rejected proposition]
    D -->|overlap or missing decision| UN[Unresolved proposition]
```

The implemented tranche covers the request, result, canonical wire, structural
correlation, and exact disposition nodes. Producer and independent containment-verifier
nodes remain unimplemented in the maintained audit tree.
