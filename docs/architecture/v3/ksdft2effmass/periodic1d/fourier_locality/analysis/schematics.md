# Analysis schematics

## Calculation composition

```mermaid
flowchart TB
    C[Validated configuration] --> P[Exact parent fibers]
    P --> E[Ordered eigenvalues]
    E --> V[Common evaluation result]
    E --> M[Construction-mesh results]
    M --> T[Complete transforms]
    T --> R[Range truncations]
    M --> F[Equal-weight direct fits]
    R --> D[Three-channel diagnostics]
    F --> D
    D --> X[Error--complexity and passage]
    M --> Q[Refinement qualification]
    V --> G[Sampled-gap qualification]
    X --> Z[Calculation result]
    Q --> Z
    G --> Z
```

## Reusable-owner boundary

```mermaid
flowchart LR
    A[Family analyzer]
    PW[Exact parent composition] --> A
    PK[PhysKit eigensystem] --> A
    ST[solidstate transforms and truncation] --> A
    AN[analysis fit and diagnostics] --> A
    A --> R[Family-owned typed records]
```

Delegation preserves scientific meanings; it does not transfer family thresholds,
decisions, or provenance to reusable owners.

## Effect exclusion

```mermaid
flowchart LR
    A[Analyzer] --> R[In-memory immutable result]
    F[Filesystem] -. forbidden .-> A
    W[Workflow engine] -. forbidden .-> A
    V[Verifier] -. not invoked .-> A
    P[Plot renderer] -. not invoked .-> A
```
