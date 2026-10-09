# `periodic1d.campaign.alignment.blind.input_records`

## Responsibility

Closed immutable version-one campaign controls and source content identities.

The defining source is
`python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/input_records.py`.
This module preserves the distinction among encoded bytes, decoded controls,
represented finite operators, inference-visible observations, withheld truth,
numerical outcomes, campaign evidence, and scientific conclusions.

## Class hierarchy

| Class | Responsibility | Architecture page |
|---|---|---|
| `BlindAlignmentSourceIdentity` | Identify one immutable baseline artifact. | [`BlindAlignmentSourceIdentity`](BlindAlignmentSourceIdentity/index.md) |
| `BlindAlignmentObservationInformationContract` | Declare the exact information exposed to inference. | [`BlindAlignmentObservationInformationContract`](BlindAlignmentObservationInformationContract/index.md) |
| `BlindAlignmentExactCase` | Represent one exact full-rank campaign case. | [`BlindAlignmentExactCase`](BlindAlignmentExactCase/index.md) |
| `BlindAlignmentNoiseSweep` | Represent the well-conditioned anchor-noise sequence. | [`BlindAlignmentNoiseSweep`](BlindAlignmentNoiseSweep/index.md) |
| `BlindAlignmentGaugeCase` | Represent the undercomplete identified-sector control. | [`BlindAlignmentGaugeCase`](BlindAlignmentGaugeCase/index.md) |
| `BlindAlignmentStoppingCase` | Represent one authored structured-stop observation. | [`BlindAlignmentStoppingCase`](BlindAlignmentStoppingCase/index.md) |
| `BlindAlignmentDiagnosticControls` | Represent neighboring probes for structured stopping boundaries. | [`BlindAlignmentDiagnosticControls`](BlindAlignmentDiagnosticControls/index.md) |
| `BlindAlignmentCampaignInput` | Represent the complete immutable version-one campaign input. | [`BlindAlignmentCampaignInput`](BlindAlignmentCampaignInput/index.md) |

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
