# `periodic1d.campaign.wannier90.verified_workflow`

## Responsibility

Owns the fixed orchestration order from native authentication through independent Wilson verification while preserving the lower-level Results separately.

## Implemented classes

- [`Periodic1DWannier90VerifiedNativeWorkflowRequest`](Periodic1DWannier90VerifiedNativeWorkflowRequest/index.md)
- [`Periodic1DWannier90VerifiedNativeWorkflowResult`](Periodic1DWannier90VerifiedNativeWorkflowResult/index.md)
- [`Periodic1DWannier90VerifiedNativeWorkflow`](Periodic1DWannier90VerifiedNativeWorkflow/index.md)

## Boundaries and evidence

The defining source is `python/src/ksdft2effmass/periodic1d/campaign/wannier90/verified_workflow.py`. Canonical tests are under `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/`; the [family dossier](../index.md) lists exact pytest owners, supported imports, Sphinx mapping, retained identities, and claim limitations. Passing evidence establishes software behavior only, not execution provenance, physical adequacy, scientific validation, UQ, or acceptance.
