# `Periodic2DRankNBandEquivalenceHoppingLocalityLocalitySummary` numerics

The three fields are dimensionless normalized binary64 powers:

- `total_power` covers the complete Fourier coefficient inventory;
- `onsite_power` covers zero displacement;
- `nononsite_power` is intended to cover every nonzero displacement.

Construction rejects non-built-in, negative, or nonfinite values and currently checks
`abs(total - onsite - nononsite) <= 1.0e-12`. That scalar relation cannot recover a
small partition contribution lost before construction when the producer subtracts two
separately rounded larger values.

For the selected baseline, normalized total power is at most approximately `0.49`, so
the unresolved false-zero magnitude is roundoff-scale. Future correction must bind each
reported partition to a direct inventory sum and use only a bounded ULP allowance above
the existing absolute floor. See
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).
