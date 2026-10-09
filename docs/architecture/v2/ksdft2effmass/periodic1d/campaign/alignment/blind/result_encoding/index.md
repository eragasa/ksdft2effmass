# `periodic1d.campaign.alignment.blind.result_encoding`

## Responsibility

Canonical result JSON encoding and exact retained-result correlation.

The defining source is
`python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/result_encoding.py`.
This module preserves the distinction among encoded bytes, decoded controls,
represented finite operators, inference-visible observations, withheld truth,
numerical outcomes, campaign evidence, and scientific conclusions.

## Class hierarchy

| Class | Responsibility | Architecture page |
|---|---|---|
| `BlindAlignmentResultSerializer` | Encode a typed result as canonical version-one UTF-8 JSON bytes. | [`BlindAlignmentResultSerializer`](BlindAlignmentResultSerializer/index.md) |
| `BlindAlignmentRetainedResultCorrelator` | Correlate typed and retained identity without numerical verification. | [`BlindAlignmentRetainedResultCorrelator`](BlindAlignmentRetainedResultCorrelator/index.md) |

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
