# V2-ISSUE-032: Durable harness-publication authority and outcome

**Severity:** High
**Scope:** Development-harness projection publication, durable authority linkage, synchronization outcome, and recovery
**Status:** Open

## Current conflict

The current prospective architecture defines candidate artifacts, target-specific synchronization preconditions, immutable projection generations, pointer manifests, recovery records, and `SynchronizationResult`. It separately defines candidate-independent development authority through `TaskAuthorization` and `DevelopmentAuthorityContext`. The durable publication outcome does not yet bind those boundaries into one reconstructible account of why one exact candidate was authorized for publication under one exact policy and what state became observable.

`SynchronizationResult` and generation manifests identify candidate, generation, predecessor, pointer, lifecycle, and recovery outcomes, but their stated contracts do not include the exact authorization, authority-context, validation, publication-policy, publication-context, or verified target-precondition identities consumed by synchronization.

## Affected contracts

- [`docs/architecture/v2/ksdft2effmass/harness/compiler-architecture.md`](../ksdft2effmass/harness/compiler-architecture.md) — synchronization inputs include exact candidate validation, authorization, and publication policy/context, while durable result and generation identities omit their linkage.
- [`docs/architecture/v2/ksdft2effmass/harness/projections.md`](../ksdft2effmass/harness/projections.md) — publication and recovery define mechanical behavior without a complete durable authority-to-outcome record.
- [`docs/architecture/v2/ksdft2effmass/harness/persistence.md`](../ksdft2effmass/harness/persistence.md) — projection generations remain outside lossless `HarnessState` persistence.
- [`docs/architecture/v2/ksdft2effmass/harness/control-plane.md`](../ksdft2effmass/harness/control-plane.md) — development authority is reconstructible separately but is not connected to the publication outcome contract.
- [`docs/architecture/v2/ksdft2effmass/harness/conformance.md`](../ksdft2effmass/harness/conformance.md) — promotion eligibility remains separate from target-operation validation, authorization, and precondition checks.

## Missing contract

The architecture lacks one durable, reconstructible linkage among the exact candidate and predecessor, applicable validation, authorization and authority-context identities, verified synchronization preconditions, publication policy/context, synchronization attempt, resulting generation and pointer observation, and any recovery or reconciliation state. The owner and persistence boundary for that linkage, its retry and supersession semantics, and its distinction from mechanical promotion eligibility, repository promotion, protected-action authority, synchronization outcome, and human acceptance remain unspecified.

## Exclusions and claim boundary

This record does not select a persistence design, authorize publication, activate implementation, grant protected authority, or establish software verification, scientific validation, uncertainty quantification, or human acceptance.
