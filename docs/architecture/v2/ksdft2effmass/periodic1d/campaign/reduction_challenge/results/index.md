# `periodic1d.campaign.reduction_challenge.results`

## Responsibility

This module owns immutable typed observations for five distinct challenge channels:

1. potential-amplitude observations;
2. reciprocal-mesh, band, and isolation observations;
3. potential-shape observations;
4. gauge-covariance observations; and
5. route-assumption observations.

`Periodic1DReductionChallengeCampaignResult` preserves these channels, version-one
evidence-status text, and one complete `Periodic1DEncodedResultDocument` with explicit
historical `STRESS` wire kind. The result validates intrinsic immutable structure and
source-document agreement. It does not prove Action execution or historical
provenance.

`Periodic1DReductionChallengeResultJsonSerializer` strictly decodes the retained
result and emits canonical JSON using unchanged historical field names. It has no
`encode()` or `decode()` forwarding aliases.

## Key class

- [Periodic1DReductionChallengeCampaignResult](Periodic1DReductionChallengeCampaignResult/index.md)
