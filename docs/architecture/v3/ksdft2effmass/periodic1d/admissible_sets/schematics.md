# Schematics

## Calculation and admission

```mermaid
graph TD
    B[Exact composite result bytes] --> R[Immutable M3 request]
    C[Frozen M3 controls and upstream digest] --> R
    V[Explicit composite byte-owning verifier] --> A[M3 analyzer]
    R --> A
    A --> Q[Spectral and angle-resolved quadratics]
    Q --> W[Compatible witness]
    Q --> S[Separated or unresolved certificate]
    A --> L[Cyclic conversion and ordinary-tail locality]
    W --> O[Canonical typed M3 result bytes]
    S --> O
    L --> O
```

## Independent verification and visualization

```mermaid
graph TD
    O[Exact M3 result bytes] --> M[M3 byte-owning verifier]
    M --> U[Authenticate embedded composite bytes]
    M --> I[Direct-formula independent reconstruction]
    I --> P[Verifier-derived typed projection]
    U --> G[Aggregate verification]
    I --> G
    P --> G
    G --> Z[Authenticated visualizer]
    P --> Z
    Z --> F1[Confirmatory witness and diagnostics PNG]
    Z --> F2[Separate locality-channel PNG]
```

The verifier and renderer do not invoke the production analyzer. The M3 analyzer does
not invoke a composite producer.
