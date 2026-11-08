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

The dependency-free core covers request, result, canonical wire, structural correlation,
and exact disposition. The optional Arb leaf implements only parent and mediated pieces
inside the producer node. The complete producer artifact, direct objective, independent
containment verifier, and retained certification composition remain unimplemented. The
diagram does not imply persistence, scientific validation, or human acceptance.
