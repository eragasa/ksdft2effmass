# `periodic1d.campaign.composite.definition`

## Responsibility

This module owns `Periodic1DCompositeCampaignDefinition` and
`Periodic1DCompositeCampaignJsonSerializer`. The definition is a frozen, slotted
schema-one control record. It binds a finite plane-wave cutoff, reciprocal sample
counts, explicit parent-qualified retained-band group definitions, hopping ranges,
gap threshold, direct-route range, and deterministic gauge-perturbation amplitudes.

[Class dossier](Periodic1DCompositeCampaignDefinition/index.md)

The serializer uses strict UTF-8/JSON mechanics, rejects duplicate keys and nonfinite
ordinary JSON values, performs schema selection before adaptation, and exposes only
`serialize()` and `deserialize()`. It does not infer scientific identity or expose
retired `encode()`/`decode()` forwarding methods.

## Boundaries

Definition validity establishes intrinsic structure and finite-parent executability
only. It does not establish historical execution, parent convergence, spectral
isolation, retention adequacy, provenance, scientific validation, UQ, or acceptance.

Routine class-owned evidence is
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeCampaignDefinition.py::TestPeriodic1DCompositeCampaignDefinition`.
