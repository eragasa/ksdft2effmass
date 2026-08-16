# V2-ISSUE-033: Target-operation identity binding without policy reinterpretation

**Severity:** High
**Scope:** Harness projector, comparator, synchronizer, supplied validation and authorization outcomes, and target-specific blocked results
**Status:** Open

## Current conflict

Architecture v2 assigns validation to validators and exact development-operation authorization to `DevelopmentOperationAuthorizer`, while `HarnessProjector`, `HarnessStateComparator`, and `HarnessSynchronizer` consume those outcomes before acting. The target operations must reject missing, stale, mismatched, denied, erroneous, or non-passing inputs, but they must not rerun validation rules, reconstruct the authority ledger, reinterpret policy, broaden permitted scope, or silently manufacture replacement outcomes.

The architecture states this separation but does not yet define one exact compatibility and identity-binding contract shared by the three target operations. Without that contract, implementations could duplicate policy under the name of defensive checking or accept results produced for another state, candidate, operation, revision, authority context, path closure, validation policy, or attempt.

## Affected contracts

- [`docs/architecture/v2/ksdft2effmass/harness/compiler-architecture.md`](../ksdft2effmass/harness/compiler-architecture.md) — target operations consume exact validation and authorization outcomes.
- [`docs/architecture/v2/ksdft2effmass/harness/projections.md`](../ksdft2effmass/harness/projections.md) — projector, comparator, and synchronizer own distinct target preconditions and blocked outcomes.
- [`docs/architecture/v2/ksdft2effmass/harness/validation.md`](../ksdft2effmass/harness/validation.md) — validators own validation policy and findings.
- [`docs/architecture/v2/ksdft2effmass/harness/control-plane.md`](../ksdft2effmass/harness/control-plane.md) — the authority resolver and operation authorizer own trust reconstruction and authorization policy.
- [`docs/architecture/v2/issues/032-harness-publication-authority-outcome.md`](032-harness-publication-authority-outcome.md) — synchronization must durably link the exact consumed outcomes without taking over their policy.

## Missing contract

The public target-operation boundary lacks an exact account of:

1. which state, candidate, manifest, operation, revision, authority-context, authorization, validation-policy, path-closure, and attempt identities each target must compare;
2. which equality, closure, freshness, and applicability relationships are mechanical binding checks rather than validation or authorization policy;
3. how `denied`, `error`, non-passing, missing, stale, superseded, and mismatched inputs map to each operation-specific blocked result;
4. whether and how a private shared binding helper may remove demonstrated duplication without owning public policy, authority, or retained state; and
5. how tests prove that targets reject mismatched outcomes and never reinterpret findings, ledger records, or permitted scope.

## Exclusions and claim boundary

This record does not reintroduce a public operation-eligibility evaluator or result, select wire spelling, grant authority, or authorize projection, comparison, synchronization, implementation, promotion, or another protected action. It establishes no software verification, scientific validation, uncertainty quantification, or human acceptance.
