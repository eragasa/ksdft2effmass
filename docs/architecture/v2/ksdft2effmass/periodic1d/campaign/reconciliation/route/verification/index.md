# `ksdft2effmass.periodic1d.campaign.reconciliation.route.verification`

## Responsibility

Owns request-scoped independent reconstruction and bounded verification results. Every
declared input, runner, implementation, and baseline-source path is resolved beneath the
caller-supplied absolute repository root before bytes are read; absolute, parent
traversal, and symlink escapes fail closed. Exact source hashes remain byte identities;
numerical records use reviewed tolerances. Generation-time matrix fingerprints are
validated as lowercase SHA-256 values but are not compared across libm or BLAS/LAPACK
runtimes. Both retained and reconstructed near-zero eigenspace-projector defects must
satisfy the unchanged authored eigenspace bound; their machine-noise magnitudes need not
match below that bound.

## Classes

- [`RouteReconciliationVerificationRequest`](RouteReconciliationVerificationRequest/index.md)
- [`RouteReconciliationVerificationResult`](RouteReconciliationVerificationResult/index.md)
- [`RouteReconciliationCampaignVerifier`](RouteReconciliationCampaignVerifier/index.md)

## Claim boundary

This module contributes bounded route-reconciliation software or numerical evidence. It does not establish material validity, general convergence, transferability, uncertainty quantification, or acceptance.
