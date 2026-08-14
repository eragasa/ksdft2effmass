# V2-ISSUE-004: Validation and publication gate

**Severity:** Implementation blocker

**Scope:** Harness validation, projection, comparison, and synchronization

## Conflict

`HarnessArtifactSet` is described as “permitted by” `ValidationResult`, although validators grant no authority. Severity and fail/continue policy remain unresolved, and no closed predicate states when a validated snapshot may be projected, compared, or synchronized. The repository-wide conformance target introduced alongside these issue records defines distinct `ConformanceCheckResult` and `PromotionEligibilityResult` contracts, so state validation must retain a narrower, explicit role.

## Affected contracts

- `harness/compiler-architecture.md` — *Validation model*, *Projection model*, and *Validation*
- `harness/validation.md`
- `harness/conformance.md`

## Required resolution

Define an immutable fail-closed state-validation outcome and replace authority-bearing wording such as “permitted by” with “validated under.” Specify which result is required for projection and comparison. Publication must separately consume exact authority and publication-policy inputs.

## Acceptance condition

Every consumer can determine from identified results whether its mechanical preconditions pass, without treating validation as human or protected-action authority.
