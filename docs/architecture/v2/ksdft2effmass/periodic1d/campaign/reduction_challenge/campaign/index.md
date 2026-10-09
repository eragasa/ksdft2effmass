# `periodic1d.campaign.reduction_challenge.campaign`

## Responsibility

`Periodic1DReductionChallengeCampaign` is the cohesive DataObject facade around one
`Periodic1DReductionChallengeEncodedDocuments` value. `correlate()` constructs a fresh
correlation Action. `verify(absolute_tolerance)` constructs a fresh campaign-verifier
Action. The facade owns no filesystem root, discovery, calculator, mutable Action, or
scientific-acceptance policy.

The verification tolerance is an explicit nonnegative finite unitless scalar. Dense
verification can propagate `MemoryError`, `OverflowError`, and
`numpy.linalg.LinAlgError`; see the verifier contract. Passing remains bounded
software/numerical consistency rather than scientific validation.
