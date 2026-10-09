# `periodic1d.campaign.alignment.blind.result_serialization`

## Responsibility

Closed version-one result decoding with exact primitive, finite-range, and inventory checks.

The defining source is
`python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/result_serialization.py`.
This module preserves the distinction among encoded bytes, decoded controls,
represented finite operators, inference-visible observations, withheld truth,
numerical outcomes, campaign evidence, and scientific conclusions.

## Class hierarchy

| Class | Responsibility | Architecture page |
|---|---|---|
| `BlindAlignmentResultDeserializer` | Decode only the closed semantic version-one result contract. | [`BlindAlignmentResultDeserializer`](BlindAlignmentResultDeserializer/index.md) |

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
