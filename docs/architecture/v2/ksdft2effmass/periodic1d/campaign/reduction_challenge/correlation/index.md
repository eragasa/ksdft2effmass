# `periodic1d.campaign.reduction_challenge.correlation`

## Responsibility

This module gives campaign correlation a nominal request/Result/Action boundary.
`Periodic1DReductionChallengeCampaignCorrelator.execute()` accepts an encoded-document
owner, constructs a fresh request-scoped
`Periodic1DReductionChallengeCampaignWorkflow`, and returns a nominal Result containing
the correlated typed campaign result. The encoded documents remain owned by the
request rather than being duplicated in the Result.

The Result proves neither that the Action ran nor that the historical calculation ran;
it validates only its intrinsic exact types. SHA-256 fields establish exact supplied
content identity, not authorship, execution provenance, decoded correctness,
convergence, validation, UQ, or acceptance.
