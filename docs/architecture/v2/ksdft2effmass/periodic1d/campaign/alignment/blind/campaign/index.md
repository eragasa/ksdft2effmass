# `periodic1d.campaign.alignment.blind.campaign`

## Responsibility

Operation-owned filesystem roots, campaign calculation, retained correlation, and the narrow supported facade.

The defining source is
`python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/campaign.py`.
This module preserves the distinction among encoded bytes, decoded controls,
represented finite operators, inference-visible observations, withheld truth,
numerical outcomes, campaign evidence, and scientific conclusions.

## Class hierarchy

| Class | Responsibility | Architecture page |
|---|---|---|
| `BlindAlignmentCampaignCalculationRequest` | Request campaign calculation from encapsulated state and explicit provenance. | [`BlindAlignmentCampaignCalculationRequest`](BlindAlignmentCampaignCalculationRequest/index.md) |
| `BlindAlignmentCampaignCalculator` | Decode, authenticate, and calculate one complete blind-alignment campaign. | [`BlindAlignmentCampaignCalculator`](BlindAlignmentCampaignCalculator/index.md) |
| `BlindAlignmentCampaignRetainedCorrelationRequest` | Request retained compatibility reconstruction from encapsulated state. | [`BlindAlignmentCampaignRetainedCorrelationRequest`](BlindAlignmentCampaignRetainedCorrelationRequest/index.md) |
| `BlindAlignmentCampaignRetainedCorrelator` | Reconstruct under retained provenance and report identity-only correlation. | [`BlindAlignmentCampaignRetainedCorrelator`](BlindAlignmentCampaignRetainedCorrelator/index.md) |
| `BlindAlignmentCampaign` | Encapsulate blind-alignment documents behind a small public façade. | [`BlindAlignmentCampaign`](BlindAlignmentCampaign/index.md) |

## Failure and scientific boundaries

Representation errors raise `TypeError`; invalid closed schemas, identities, domains,
or intrinsic invariants raise `ValueError`; unrepresentable finite numeric conversions
raise `OverflowError` where applicable. Dense work may raise `MemoryError`. Structured
rank, spin, subspace-angle, conditioning, and energy-anchor stops remain typed campaign
outcomes rather than exceptions for otherwise valid requests.

Passing tests establishes only the documented synthetic software or numerical contract,
not material validation, convergence, UQ, transferability, or acceptance. See the
[family dossier](../index.md) for exact evidence and retained identities.

Original local work under the repository license.
