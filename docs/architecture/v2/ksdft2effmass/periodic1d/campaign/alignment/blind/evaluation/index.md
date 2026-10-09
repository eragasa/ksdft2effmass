# `periodic1d.campaign.alignment.blind.evaluation`

## Responsibility

Post hoc comparison of successful inference with truth withheld from the inference Action.

The defining source is
`python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/evaluation.py`.
This module preserves the distinction among encoded bytes, decoded controls,
represented finite operators, inference-visible observations, withheld truth,
numerical outcomes, campaign evidence, and scientific conclusions.

## Class hierarchy

| Class | Responsibility | Architecture page |
|---|---|---|
| `BlindAlignmentEvaluationRequest` | Request post hoc evaluation of one successful inference. | [`BlindAlignmentEvaluationRequest`](BlindAlignmentEvaluationRequest/index.md) |
| `BlindAlignmentEvaluationResult` | Record distinct post hoc map, shift, extraction, model, and spectral errors. | [`BlindAlignmentEvaluationResult`](BlindAlignmentEvaluationResult/index.md) |
| `BlindAlignmentInferenceEvaluator` | Evaluate inferred outputs against truth withheld during inference. | [`BlindAlignmentInferenceEvaluator`](BlindAlignmentInferenceEvaluator/index.md) |

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
