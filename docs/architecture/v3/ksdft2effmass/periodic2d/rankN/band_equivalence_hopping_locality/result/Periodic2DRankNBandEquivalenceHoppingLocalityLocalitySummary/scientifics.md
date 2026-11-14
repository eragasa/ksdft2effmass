# `Periodic2DRankNBandEquivalenceHoppingLocalityLocalitySummary` scientific interpretation

This value reports finite normalized hopping-power diagnostics. It is not a support
selection, decay law, convergence result, or certificate of exact finite range.

In particular, `nononsite_power == 0.0` currently means that the producer reported zero
under its binary64 subtraction-and-clipping policy. It does not establish an exactly
onsite-only Hamiltonian. Strict absence of nonzero-displacement blocks would require
direct inventory evidence after resolving
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).
