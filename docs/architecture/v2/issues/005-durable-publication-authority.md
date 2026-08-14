# V2-ISSUE-005: Durable publication authority and outcome

**Severity:** High

**Scope:** Development projection publication and recovery

## Conflict

Harness Task decisions, selection authority, evidence, review, closure, and acceptance have durable conceptual owners. Projection synchronization does not yet have an equivalent durable record linking an exact authority grant, artifact-set identity, prior maintained revision, publication policy, resulting revision, and recovery outcome. `SynchronizationResult` records an operation outcome but does not itself supply authority.

## Affected contracts

- `harness/compiler-architecture.md` — *Synchronization*
- `harness/persistence.md`
- `harness/tasks/decisions-and-authority.md`
- `harness/tasks/persistence-and-projections.md`
- `harness/conformance.md`

## Required resolution

Define immutable publication request/grant and publication record contracts and identify their authoritative repository. Keep mechanical eligibility, protected-action authority, synchronization outcome, and human acceptance separate.

## Acceptance condition

A restarted process can reconstruct why one exact candidate set was publishable, what prior state it expected, what became observable, and what recovery remains required.
