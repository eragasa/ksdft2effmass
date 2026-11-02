# `Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer` schematic

```mermaid
flowchart LR
    R[bound request and case] --> A[gauge alignment routes]
    A --> F[Fourier series]
    F --> P[typed block powers]
    P --> S[direct shell sums and support decisions]
    P --> L[locality summary]
    L --> D[total minus onsite, clipped at zero]
    S --> C[case analysis]
    D --> C
```

The `D` branch is the deferred `TD-BEL-003` limitation. It is a reporting branch and
does not feed the direct shell-sum decision branch. See
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).
