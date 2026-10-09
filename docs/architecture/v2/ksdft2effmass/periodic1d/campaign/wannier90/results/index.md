# `periodic1d.campaign.wannier90.results`

## Responsibility

Owns the closed version-one retained-result schema and typed Wilson-phase, center, artifact-identity, localization-status, and convergence-status observations. Circular center comparison is reconstructed by an Action during deserialization; retained status is never inferred.

## Implemented classes

- [`Periodic1DWannier90WilsonGroupResult`](Periodic1DWannier90WilsonGroupResult/index.md)
- [`Periodic1DWannier90CampaignResult`](Periodic1DWannier90CampaignResult/index.md)
- [`Periodic1DWannier90ResultJsonSerializer`](Periodic1DWannier90ResultJsonSerializer/index.md)

## Boundaries and evidence

The defining source is `python/src/ksdft2effmass/periodic1d/campaign/wannier90/results.py`. Canonical tests are under `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/wannier90/`; the [family dossier](../index.md) lists exact pytest owners, supported imports, Sphinx mapping, retained identities, and claim limitations. Passing evidence establishes software behavior only, not execution provenance, physical adequacy, scientific validation, UQ, or acceptance.
