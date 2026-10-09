# `periodic1d.campaign.composite.results`

## Responsibility

This module owns the immutable decoded composite result hierarchy and
`Periodic1DCompositeResultJsonSerializer`. It separates Wilson, sampled isolation,
gauge-comparison, complete represented hopping, finite-range, direct-route, artifact
identity, provenance, and source-document channels rather than collapsing them into one
scientific claim.

The aggregate `Periodic1DCompositeCampaignResult` retains its exact
`Periodic1DEncodedResultDocument`, ordered group results, and provenance. A group result
is documented in the
[Periodic1DCompositeBandGroupResult dossier](Periodic1DCompositeBandGroupResult/index.md).

## Boundaries and evidence

Results validate intrinsic immutable structure and retained algebraic correlations. They
do not prove that an Action executed, authenticate authorship, reconstruct unavailable
frames/projectors, establish parent convergence, or apply scientific acceptance.

Claim-bearing serializer evidence is
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeResultJsonSerializer.py::TestPeriodic1DCompositeResultJsonSerializer`.
Independent numerical evidence is owned separately by
`python/tests/numerical_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeResultVerifier.py::TestPeriodic1DCompositeResultVerifier`.
