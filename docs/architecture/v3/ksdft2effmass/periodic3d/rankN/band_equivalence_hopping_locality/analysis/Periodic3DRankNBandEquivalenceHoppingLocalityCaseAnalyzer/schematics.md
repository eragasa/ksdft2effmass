# `Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer` schematic

```mermaid
flowchart LR
    B[PhysKit block-hopping parent] --> C[synthetic-case field sampler]
    G[independent Givens attack] --> C
    C --> X[immutable reference/comparison field samples]
    W[in-memory Wannier field producer] --> X
    N[parent-independent numerical policy] --> A[represented-field analyzer]
    M[physical-metric geometry] --> A
    X --> A
    A --> U[gauge alignment routes]
    U --> F[Fourier series]
    F --> P[typed block powers]
    P --> Q[direct shell sums and support decisions]
    P --> L[locality summary]
    L --> R[total minus onsite, clipped at zero]
    Q --> Y[generic field analysis]
    R --> Y
    Y --> V[v1 synthetic case adapter]
    B --> V
    G --> V
    V --> O[v1 synthetic case analysis]
```

The `R` branch is the deferred `TD-BEL-003` limitation. It is a reporting branch and
does not feed the direct shell-sum decision branch. See
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).
