# `periodic1d.campaign.alignment.blind.workflow`

## Responsibility

Multi-case synthetic campaign orchestration with hidden truth excluded from inference requests.

The defining source is
`python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/workflow.py`.
This module preserves the distinction among encoded bytes, decoded controls,
represented finite operators, inference-visible observations, withheld truth,
numerical outcomes, campaign evidence, and scientific conclusions.

## Class hierarchy

| Class | Responsibility | Architecture page |
|---|---|---|
| `BlindAlignmentCampaignWorkflowRequest` | Request complete campaign composition from authenticated typed inputs. | [`BlindAlignmentCampaignWorkflowRequest`](BlindAlignmentCampaignWorkflowRequest/index.md) |
| `BlindAlignmentCampaignWorkflow` | Compose all exact, sensitivity, gauge, stop, and boundary-diagnostic cases. | [`BlindAlignmentCampaignWorkflow`](BlindAlignmentCampaignWorkflow/index.md) |

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
