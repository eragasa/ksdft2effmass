# `Periodic3DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer` schematic

```mermaid
flowchart LR
    C[explicit coefficient sums] --> T[total power]
    C --> O[onsite power]
    T --> N[subtract onsite and clip]
    O --> N
    N --> Q[non-onsite comparison]
    C --> S[direct shell sums]
    S --> D[support comparisons]
```

The `N` route repeats the producer mechanism and is the deferred `TD-BEL-003`
independence gap. The direct shell route remains separate. See
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).
