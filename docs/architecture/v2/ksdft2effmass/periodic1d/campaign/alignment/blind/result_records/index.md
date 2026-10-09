# `periodic1d.campaign.alignment.blind.result_records`

## Responsibility

Immutable typed hierarchy for every retained blind-alignment result channel.

The defining source is
`python/src/ksdft2effmass/periodic1d/campaign/alignment/blind/result_records.py`.
This module preserves the distinction among encoded bytes, decoded controls,
represented finite operators, inference-visible observations, withheld truth,
numerical outcomes, campaign evidence, and scientific conclusions.

## Class hierarchy

| Class | Responsibility | Architecture page |
|---|---|---|
| `BlindAlignmentSuccessfulCaseResult` | Represent one flattened successful version-one case. | [`BlindAlignmentSuccessfulCaseResult`](BlindAlignmentSuccessfulCaseResult/index.md) |
| `BlindAlignmentStoppedCaseResult` | Represent one structured stop without aligned outputs. | [`BlindAlignmentStoppedCaseResult`](BlindAlignmentStoppedCaseResult/index.md) |
| `BlindAlignmentNoiseCaseResult` | Bind one successful case to its authored unitary anchor-noise amplitude. | [`BlindAlignmentNoiseCaseResult`](BlindAlignmentNoiseCaseResult/index.md) |
| `BlindAlignmentGaugeCaseResult` | Represent identified-sector recovery and completion nonuniqueness. | [`BlindAlignmentGaugeCaseResult`](BlindAlignmentGaugeCaseResult/index.md) |
| `BlindAlignmentStoppingControlResult` | Bind one structured stop to its authored negative-control kind. | [`BlindAlignmentStoppingControlResult`](BlindAlignmentStoppingControlResult/index.md) |
| `BlindAlignmentConditioningDiagnosticResult` | Bind an outcome to a conditioning-boundary probe. | [`BlindAlignmentConditioningDiagnosticResult`](BlindAlignmentConditioningDiagnosticResult/index.md) |
| `BlindAlignmentPrincipalAngleDiagnosticResult` | Bind an outcome to a retained-subspace angle probe. | [`BlindAlignmentPrincipalAngleDiagnosticResult`](BlindAlignmentPrincipalAngleDiagnosticResult/index.md) |
| `BlindAlignmentEnergyAnchorDiagnosticResult` | Bind an outcome to one requested exterior energy-anchor rank. | [`BlindAlignmentEnergyAnchorDiagnosticResult`](BlindAlignmentEnergyAnchorDiagnosticResult/index.md) |
| `BlindAlignmentRankReconciliationResult` | Represent explicit rectangular partial-isometry reconciliation. | [`BlindAlignmentRankReconciliationResult`](BlindAlignmentRankReconciliationResult/index.md) |
| `BlindAlignmentSpinReconciliationResult` | Represent direct spin mismatch and explicit spin-lift reconciliation. | [`BlindAlignmentSpinReconciliationResult`](BlindAlignmentSpinReconciliationResult/index.md) |
| `BlindAlignmentDiagnosticSuiteResult` | Store all retained neighboring stopping-boundary diagnostics. | [`BlindAlignmentDiagnosticSuiteResult`](BlindAlignmentDiagnosticSuiteResult/index.md) |
| `BlindAlignmentInformationBoundary` | Represent the declared inference information boundary. | [`BlindAlignmentInformationBoundary`](BlindAlignmentInformationBoundary/index.md) |
| `BlindAlignmentProvenance` | Represent retained version-one execution provenance. | [`BlindAlignmentProvenance`](BlindAlignmentProvenance/index.md) |
| `BlindAlignmentCampaignResult` | Represent the complete semantic version-one blind-alignment result. | [`BlindAlignmentCampaignResult`](BlindAlignmentCampaignResult/index.md) |
| `BlindAlignmentResultCorrelationRequest` | Request semantic and canonical correlation with one retained result. | [`BlindAlignmentResultCorrelationRequest`](BlindAlignmentResultCorrelationRequest/index.md) |
| `BlindAlignmentResultCorrelation` | Report identity-only correlation without a verification claim. | [`BlindAlignmentResultCorrelation`](BlindAlignmentResultCorrelation/index.md) |

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
