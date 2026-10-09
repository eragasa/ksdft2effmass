# `periodic1d.campaign.alignment.blind.construction`

## Responsibility

Construction of inference-visible represented observations and separately typed hidden truth.

The defining source is
`python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/construction.py`.
This module preserves the distinction among encoded bytes, decoded controls,
represented finite operators, inference-visible observations, withheld truth,
numerical outcomes, campaign evidence, and scientific conclusions.

## Class hierarchy

| Class | Responsibility | Architecture page |
|---|---|---|
| `BlindAlignmentHiddenTruth` | Store construction-only values withheld from inference. | [`BlindAlignmentHiddenTruth`](BlindAlignmentHiddenTruth/index.md) |
| `BlindAlignmentObservationConstructionRequest` | Request one full-dimensional synthetic blind observation. | [`BlindAlignmentObservationConstructionRequest`](BlindAlignmentObservationConstructionRequest/index.md) |
| `BlindAlignmentObservationConstructionResult` | Return inference-visible observation separately from hidden truth. | [`BlindAlignmentObservationConstructionResult`](BlindAlignmentObservationConstructionResult/index.md) |
| `BlindAlignmentObservationConstructor` | Construct a synthetic observation while preserving the inference boundary. | [`BlindAlignmentObservationConstructor`](BlindAlignmentObservationConstructor/index.md) |

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
