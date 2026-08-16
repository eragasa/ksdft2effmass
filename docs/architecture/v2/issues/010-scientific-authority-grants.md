# V2-ISSUE-010: Enforceable execution and disposition authority grants

**Severity:** Critical
**Scope:** Protected execution and scientific-disposition authority
**Status:** Open

## Current conflict

Protected execution and scientific disposition require independent, fail-closed checks against exact immutable grants and trusted authority snapshots, but neither grant family has a closed validity, trust, revocation, verification-result, reservation/use, or append/supersession protocol.

## Affected contracts

- [`docs/architecture/v2/separation-of-harness-and-workflow.md`](../separation-of-harness-and-workflow.md) — protected execution requires an immutable grant and authority snapshot without closing their verification semantics.
- [`docs/architecture/v2/ksdft2effmass/workflows/control-plane.md`](../ksdft2effmass/workflows/control-plane.md) — dispatch reservation and repeated checks lack an authoritative grant-state protocol; disposition grants are explicitly separate.
- [`docs/architecture/v2/ksdft2effmass/workflows/service-model.md`](../ksdft2effmass/workflows/service-model.md) — service operations depend on grant verification and one-dispatch use without a closed result contract.
- [`docs/architecture/v2/ksdft2effmass/calculators/quantum-espresso.md`](../ksdft2effmass/calculators/quantum-espresso.md) — the executor must independently reject stale, revoked, consumed, or unverifiable authority without sufficient represented inputs.
- [`docs/architecture/v2/ksdft2effmass/analysis/analysis-and-disposition.md`](../ksdft2effmass/analysis/analysis-and-disposition.md) — disposition recording, supersession, and withdrawal require a trusted grant and snapshot whose lifecycle is undefined.

## Missing contract

Separate execution-grant and disposition-grant contracts are missing for trusted issuer/source snapshots, exact subject and operation scope, validity, revocation or supersession, closed verification results, and retry or indeterminate treatment. Execution also lacks authoritative reservation and one-dispatch use; disposition lacks append, supersession, and withdrawal authority semantics.

## Exclusions and claim boundary

A shared nominal grant class, exact fields, and wire encoding are excluded. This record grants no execution or disposition authority and establishes no implementation, verification, scientific validation, uncertainty quantification, or human acceptance.
