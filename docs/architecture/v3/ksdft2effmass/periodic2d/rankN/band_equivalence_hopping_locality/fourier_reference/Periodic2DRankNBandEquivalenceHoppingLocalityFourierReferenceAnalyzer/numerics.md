# `Periodic2DRankNBandEquivalenceHoppingLocalityFourierReferenceAnalyzer` numerics

The reference reconstructs Fourier coefficients and normalized coefficient powers with
explicit dense finite sums. Total and onsite powers are separately summed in binary64.
It then derives non-onsite power by subtracting those rounded totals and clipping at
zero, matching the production formula.

Consequently, producer/reference agreement for `nononsite_power` does not exclude a
roundoff-scale false zero. The selected baseline keeps normalized total power at most
approximately `0.49`, so the unresolved discrepancy is roundoff-scale and does not
change direct shell sums or support decisions.

The replacement must classify zero and nonzero displacements independently and directly
sum the nonzero inventory rather than reconstruct it by subtraction. See
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).
