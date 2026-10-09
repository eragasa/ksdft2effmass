# `Periodic1DIsolatedBandCampaign`

## Responsibility

This frozen, slotted DataObject encapsulates exactly one
`Periodic1DIsolatedBandEncodedDocuments` value and constructs fresh campaign-specific
correlation or verification Actions for each request. Correlation strictly decodes and
binds represented input/result relations. Verification separately reconstructs the
implemented numerical channels with explicit tolerances and unavailable-channel
reporting.

The campaign does not discover files, invoke Quantum ESPRESSO or Wannier90, rerun the
historical calculation, manufacture provenance, or collapse correlation and numerical
verification into scientific acceptance.

## Code and public route

| Surface | Mapping |
|---|---|
| Definition | `python/src/ksdft2effmass/periodic1d/campaign/isolated/campaign.py` |
| Qualified class | `ksdft2effmass.periodic1d.campaign.isolated.campaign.Periodic1DIsolatedBandCampaign` |
| Public facade | `ksdft2effmass.periodic1d.campaign.Periodic1DIsolatedBandCampaign` |
| Transitional aliases | None |

## Evidence

`python/tests/software_verification/ksdft2effmass/periodic1d/campaign/isolated/test__Periodic1DIsolatedBandCampaign.py`
owns the following exact nodes:

- `TestPeriodic1DIsolatedBandCampaign::test_method__correlate__uses_distinct_correlation_action`;
- `TestPeriodic1DIsolatedBandCampaign::test_method__verify__delegates_documents_through_typed_request`.

Artifact-owned route and content evidence resides in
`test__integration__isolated_band_encoded_document_artifacts.py`. Numerical
reconstruction evidence remains separately classified under
`python/tests/numerical_verification/ksdft2effmass/periodic1d/campaign/isolated/`.

A passing campaign result establishes only its documented software and numerical
comparisons. It does not establish discretization or hopping-range convergence,
physical adequacy, scientific validation, uncertainty quantification, or acceptance.
Original local work under the repository license.
