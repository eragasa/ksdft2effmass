# `Periodic1DIsolatedBandCampaignResult`

## Responsibility

This frozen, slotted result retains three explicit owners:

1. the complete `Periodic1DEncodedResultDocument` and its exact isolated-band wire
   identity;
2. typed parent-representation verification diagnostics; and
3. typed isolated-band reduction diagnostics.

Its intrinsic checks require exact nested result types and the explicit
`ISOLATED_BAND` wire kind. It does not replay an Action or infer origin from shapes,
names, paths, spectra, or digests.

Parent-model, finite-discretization, common-space comparison, retained-band,
Fourier-reconstruction, hopping truncation, least-squares fitting, localization, and
observable diagnostics remain separate fields. The aggregate is not a physical model,
retained space, represented operator, effective model, provenance record, convergence
claim, uncertainty result, or acceptance decision.

## Code and public route

| Surface | Mapping |
|---|---|
| Definition | `python/src/ksdft2effmass/periodic1d/campaign/isolated/results.py` |
| Qualified class | `ksdft2effmass.periodic1d.campaign.isolated.results.Periodic1DIsolatedBandCampaignResult` |
| Public facade | `ksdft2effmass.periodic1d.campaign.Periodic1DIsolatedBandCampaignResult` |
| Transitional aliases | None |

## Evidence and retained identity

`TestPeriodic1DIsolatedBandResultJsonSerializer::test_method__decode_encode__extracts_correlated_domain_results`
in
`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/isolated/test__Periodic1DIsolatedBandResultJsonSerializer.py`
binds the defining module, source document, typed inventories, scalar representation,
and canonical reconstruction. The maintained `result.json` SHA-256 is
`37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c`.

Exact content identity and passing software tests do not establish historical execution,
provenance, convergence, physical validity, scientific validation, uncertainty
quantification, or acceptance. Original local work under the repository license.
