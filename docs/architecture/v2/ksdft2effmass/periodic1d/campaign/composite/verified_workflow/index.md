# `periodic1d.campaign.composite.verified_workflow`

This module owns immutable request/result records and
`Periodic1DCompositeVerifiedWorkflow`. Execution correlates the retained bytes first,
then independently verifies the already correlated typed result. Fresh Action owners
are constructed for each invocation.

The Workflow is deterministic in-process orchestration. It neither invokes the original
calculation nor turns a passing tolerance comparison into a scientific acceptance
claim.

Claim-bearing evidence:
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeVerifiedWorkflow.py::TestPeriodic1DCompositeVerifiedWorkflow`.
