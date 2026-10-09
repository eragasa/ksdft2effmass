# `periodic1d.campaign.composite.correlation_workflow`

The immutable request owns exact input/result bytes. The Workflow strictly decodes each
wire, calculates its SHA-256 content identity, requires experiment/source/group/control
correlations, and returns typed records plus both identities. It creates no repository
root and performs no implicit scientific transformation.

`correlation.Periodic1DCompositeCampaignCorrelator` is the request-to-value Action
facade and creates a fresh Workflow per invocation.

Claim-bearing evidence:
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeCampaignWorkflow.py::TestPeriodic1DCompositeCampaignWorkflow`.
A pass establishes represented cross-document consistency only, not provenance,
execution, convergence, validation, UQ, or acceptance.
