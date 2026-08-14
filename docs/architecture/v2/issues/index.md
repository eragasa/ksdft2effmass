# Architecture v2 issues

These records preserve findings from a read-only review of Architecture v2 at base revision `4ec9b5650dc4bea8c7da504fec7f5a79e6606b08` plus the repository-wide conformance target introduced in the same change as these records. They describe unresolved contracts and one deterministic documentation correction. They do not activate Harness Tasks, select unresolved architecture alternatives, authorize implementation or protected execution, or record human acceptance.

Architecture v2 remains a prospective target under the [v1-to-v2 migration crosswalk](../../migration/v1-to-v2/index.md).

## Implementation blockers

- [V2-ISSUE-001: Simulation execution request context](001-simulation-execution-request-context.md)
- [V2-ISSUE-002: Scientific dispatch and result-ingress atomicity](002-scientific-dispatch-atomicity.md)
- [V2-ISSUE-003: Compiler handling of contradictory authority](003-compiler-authority-conflict.md)
- [V2-ISSUE-004: Validation and publication gate](004-validation-and-publication-gate.md)

## High-priority architecture issues

- [V2-ISSUE-005: Durable publication authority and outcome](005-durable-publication-authority.md)
- [V2-ISSUE-006: Deterministic CPN transition and binding selection](006-cpn-deterministic-selection.md)
- [V2-ISSUE-009: Executable scientific authority grant](009-execution-authority-grant.md)
- [V2-ISSUE-010: Package dependency graph consistency](010-dependency-graph-consistency.md)
- [V2-ISSUE-012: Projection publication rollback guarantee](012-publication-rollback-guarantee.md)

## Additional contract issues

- [V2-ISSUE-007: Observation normalization composition](007-observation-normalization-composition.md)
- [V2-ISSUE-008: Scientific disposition ActionObject](008-scientific-disposition-action.md)
- [V2-ISSUE-011: Candidate artifact validation owner](011-candidate-artifact-validator.md)
- [V2-ISSUE-013: Producer identity for external input artifacts](013-external-artifact-producer-identity.md)

## Deterministic documentation correction

- [V2-ISSUE-014: Required-failure policy wording](014-required-failure-wording.md)

## Review disposition

The high-level separation among development conformance, Harness Task authority, scientific-workflow control, domain-independent colored-Petri-net semantics, calculator execution, deterministic analysis, and human authority remains a sound target. The blocker records above must be resolved before the complete v2 architecture can be implemented as one coherent public and persistence contract.
