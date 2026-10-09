# `ksdft2effmass.periodic1d.campaign.reconciliation.route.verification`

## Responsibility

Owns request-scoped independent reconstruction and bounded verification results. Every
declared input, runner, implementation, and baseline-source path is resolved beneath the
caller-supplied absolute repository root before bytes are read; absolute, parent
traversal, and symlink escapes fail closed.

## Classes

- [`RouteReconciliationVerificationRequest`](RouteReconciliationVerificationRequest/index.md)
- [`RouteReconciliationVerificationResult`](RouteReconciliationVerificationResult/index.md)
- [`RouteReconciliationCampaignVerifier`](RouteReconciliationCampaignVerifier/index.md)

## Claim boundary

This module contributes bounded route-reconciliation software or numerical evidence. It does not establish material validity, general convergence, transferability, uncertainty quantification, or acceptance.
