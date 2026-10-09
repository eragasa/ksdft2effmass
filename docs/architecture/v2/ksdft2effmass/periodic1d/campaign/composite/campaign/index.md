# `periodic1d.campaign.composite.campaign`

## `Periodic1DCompositeCampaign`

This frozen, slotted operation owner encapsulates one
`Periodic1DCompositeEncodedDocuments` value and exposes `correlate()` and `verify()`.
Each invocation constructs fresh request-scoped Action owners; the campaign retains no
mutable operation or result state.

Correlation binds strict decoded values and exact wire identities. Verification then
uses a separate numerical implementation for reconstructable retained channels. Neither
operation discovers repository files, invokes calculators, authenticates historical
execution, or makes a scientific acceptance decision.

Implementation:
`python/src/ksdft2effmass/periodic1d/campaign/composite/campaign.py`.
Claim-bearing evidence:
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeCampaign.py::TestPeriodic1DCompositeCampaign`.
