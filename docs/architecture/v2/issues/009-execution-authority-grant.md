# V2-ISSUE-009: Executable scientific authority grant

**Severity:** High

**Scope:** Protected scientific execution

## Conflict

`AuthorityIdentity` identifies a decision or grant, but the enforceable execution-grant contract remains unspecified. Scientific requests and calculator executors are nevertheless required to validate authority before dispatch.

## Required resolution

Define an immutable `ExecutionGrant` containing, as applicable:

- issuer and exact decision provenance;
- permitted workflow, run, simulation, calculator, executable, and effect scope;
- allowed attempt and retry behavior;
- configuration and resource ceilings;
- validity, expiry, revocation, and supersession semantics; and
- use or reuse constraints.

Validate the grant before request reservation and immediately before dispatch.

## Acceptance condition

Missing, stale, mismatched, exhausted, revoked, or superseded authority produces `AuthorizationFailure` without execution.

This issue does not grant protected-execution authority.
