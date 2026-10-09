# `periodic1d.campaign.alignment.blind.case_execution`

## Responsibility

Composition of observation-only inference and separately authorized post hoc synthetic evaluation.

The defining source is
`python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/case_execution.py`.
This module preserves the distinction among encoded bytes, decoded controls,
represented finite operators, inference-visible observations, withheld truth,
numerical outcomes, campaign evidence, and scientific conclusions.

## Class hierarchy

| Class | Responsibility | Architecture page |
|---|---|---|
| `BlindAlignmentCaseExecutionRequest` | Request inference and conditionally separate post hoc evaluation. | [`BlindAlignmentCaseExecutionRequest`](BlindAlignmentCaseExecutionRequest/index.md) |
| `BlindAlignmentCaseExecutionResult` | Return represented inference separately from flattened campaign outcome. | [`BlindAlignmentCaseExecutionResult`](BlindAlignmentCaseExecutionResult/index.md) |
| `BlindAlignmentCaseExecutor` | Infer from observation-only data, then evaluate successful output post hoc. | [`BlindAlignmentCaseExecutor`](BlindAlignmentCaseExecutor/index.md) |

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
