# V2-ISSUE-003: Compiler handling of contradictory authority

**Severity:** Implementation blocker

**Scope:** Harness compilation and diagnostics

## Conflict

`harness/compiler-architecture.md` says conflicting sources remain explicit findings in `HarnessStateSnapshot`, but its failure model says contradictory authority returns no compiled snapshot. Validators and findings otherwise refer to snapshot objects and provenance.

## Required resolution

Distinguish at least:

- unrepresentable source or identity ambiguity, which produces compilation failure and no snapshot; and
- representable cross-record authority conflict, which produces a snapshot plus validation findings while prohibiting downstream publication.

Neither path may select an arbitrary winner.

## Acceptance condition

Compiler return types, diagnostic provenance, validation entry conditions, and projection gates describe one consistent lifecycle for contradictory authoritative inputs.
