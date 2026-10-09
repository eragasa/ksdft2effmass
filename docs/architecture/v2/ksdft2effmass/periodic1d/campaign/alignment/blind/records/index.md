# `periodic1d.campaign.alignment.blind.records`

## Responsibility

Inference policy, visible observations, requests, and structured numerical outcomes.

The defining source is
`python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/records.py`.
This module preserves the distinction among encoded bytes, decoded controls,
represented finite operators, inference-visible observations, withheld truth,
numerical outcomes, campaign evidence, and scientific conclusions.

## Class hierarchy

| Class | Responsibility | Architecture page |
|---|---|---|
| `BlindAlignmentInferencePolicy` | Store numerical policy for one blind-alignment inference. | [`BlindAlignmentInferencePolicy`](BlindAlignmentInferencePolicy/index.md) |
| `BlindAlignmentObservation` | Represent only information visible to blind alignment. | [`BlindAlignmentObservation`](BlindAlignmentObservation/index.md) |
| `BlindAlignmentInferenceRequest` | Bind one observation to the explicit inference policy applied to it. | [`BlindAlignmentInferenceRequest`](BlindAlignmentInferenceRequest/index.md) |
| `BlindAlignmentInferenceResult` | Record a full, partial, or stopped blind-alignment outcome. | [`BlindAlignmentInferenceResult`](BlindAlignmentInferenceResult/index.md) |

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
