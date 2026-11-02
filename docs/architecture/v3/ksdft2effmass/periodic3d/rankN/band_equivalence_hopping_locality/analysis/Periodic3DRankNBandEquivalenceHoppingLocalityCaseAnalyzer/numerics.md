# `Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer` numerics

The analyzer uses binary64 complex Fourier coefficients and nonnegative normalized
squared Frobenius powers. The current summary computes

```text
P_nononsite = max(0, P_total - P_onsite).
```

Because `P_total` and `P_onsite` are separately rounded, subtraction can return zero
when a smaller directly representable non-onsite component exists. The selected
analytic family has retained energies bounded in magnitude by `0.7`; unitary gauge
action preserves Frobenius power, so normalized total power is at most approximately
`0.49`. The unresolved loss is therefore roundoff-scale for this baseline.

Support decisions do not consume this summary scalar. They use direct
`normalized_power_beyond_shell(...)` sums and shell reconstruction-error channels.
The future replacement must directly sum disjoint, exhaustive zero- and
nonzero-displacement inventories and retain the total as an independent diagnostic.

This limitation and its regression requirements are recorded in
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).
