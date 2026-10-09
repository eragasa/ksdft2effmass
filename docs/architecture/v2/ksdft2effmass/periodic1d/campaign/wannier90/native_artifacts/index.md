# `periodic1d.campaign.wannier90.native_artifacts`

## Responsibility

Owns explicit campaign native-artifact inventories and composes generic authentication and parsing with retained group observations. It performs no path discovery or calculator execution.

## Implemented classes

- [`Periodic1DWannier90NativeArtifactGroup`](Periodic1DWannier90NativeArtifactGroup/index.md)
- [`Periodic1DWannier90NativeArtifactWorkflowRequest`](Periodic1DWannier90NativeArtifactWorkflowRequest/index.md)
- [`Periodic1DWannier90NativeArtifactGroupResult`](Periodic1DWannier90NativeArtifactGroupResult/index.md)
- [`Periodic1DWannier90NativeArtifactWorkflowResult`](Periodic1DWannier90NativeArtifactWorkflowResult/index.md)
- [`Periodic1DWannier90NativeArtifactWorkflow`](Periodic1DWannier90NativeArtifactWorkflow/index.md)

## Boundaries and evidence

The defining source is `python/src/ksdft2effmass/periodic1d/campaign/wannier90/native_artifacts.py`. Canonical tests are under `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/`; the [family dossier](../index.md) lists exact pytest owners, supported imports, Sphinx mapping, retained identities, and claim limitations. Passing evidence establishes software behavior only, not execution provenance, physical adequacy, scientific validation, UQ, or acceptance.
