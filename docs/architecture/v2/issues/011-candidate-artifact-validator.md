# V2-ISSUE-011: Candidate artifact validation owner

**Severity:** Medium

**Scope:** Harness projection and publication

## Conflict

Candidate artifact checks are specified after projection and appear as a distinct failure phase, but no named ActionObject owns that phase. Normalized-state validation also mentions generated-artifact path and manifest closure before `HarnessArtifactSet` exists.

## Affected contracts

- `harness/compiler-architecture.md` — *Validation*, *Candidate validation*, and *ActionObjects*
- `harness/validation.md`

## Required resolution

Keep source-owned destination-policy invariants in snapshot validation. Assign post-projection artifact-set invariants to a named action such as:

```text
HarnessArtifactSetValidator
    HarnessArtifactSet + projection policy
    → ArtifactSetValidationResult
```

## Acceptance condition

Every invariant is evaluated only after its subject exists, and comparison or synchronization accepts only an explicitly validated complete candidate set.
