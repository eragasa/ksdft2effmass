# Development validation

## Purpose

Development validation evaluates one normalized `HarnessState` without changing it. Domain rules remain with concrete domain validators; composition belongs to `HarnessStateValidator`.

This page describes validation of the development-control aggregate itself. The broader evaluation of proposed changes across source, workflow, calculator, scientific-domain, test, documentation, and harness paths is defined by [Development conformance](conformance.md). A passing `HarnessStateValidator` result is one input to that broader process, not a repository-wide promotion decision.

## Protocol

```python
class HarnessDomainValidator(Protocol):
    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]: ...

    def execute(self, state: HarnessState) -> ValidationResult: ...
```

The protocol provides structural polymorphism only. Every concrete domain validator constructs the complete normative `ValidationResult` for its own leaf invocation; private intermediate findings do not constitute a second public result type. The protocol supplies no registry, discovery, default rules, mutation, repair, or authorization.

## Normalized-state validators

| Validator | Rule ownership |
|---|---|
| `HarnessTaskCatalogValidator` | Task identities and catalog invariants |
| `DevelopmentTaskSelectionValidator` | Selection eligibility and consistency |
| `HarnessTaskGraphValidator` | Parent/prerequisite references, cycles, and closure |
| `HarnessCapabilityCatalogValidator` | Capability identity and relationships |
| `HarnessResourceCatalogValidator` | Resource dependencies, closure, and layering |
| `HarnessEvidenceCatalogValidator` | Evidence identity, ownership, and claim boundaries |
| Applicable destination-policy validator | Source-owned destination policy and normalized-state destination invariants before projection |

## Composition

`DevelopmentDecision` itself owns the intrinsic field and unresolved/resolved variant invariants of one immutable value. `HarnessStateValidator` directly validates cross-record decision-identity uniqueness, predecessor/supersession and other declared references, and canonical ordering of the immutable canonically ordered decision sequence in `HarnessState`; no decision catalog or decision-specific public validator exists.

`HarnessStateValidator` receives an explicit ordered tuple of the remaining `HarnessDomainValidator` objects. It applies them deterministically, evaluates cross-domain closure including those aggregate-level decision rules, and returns the same normative `ValidationResult` used by every leaf or composite invocation.

Every result contains result identity; validator identity; requirement, rule, and version identities; summary; applicability and not-applicable reason; subject identity; execution-completed indicator; closed status (`pass`, `fail`, `error`, `not_run`, or `not_applicable`); ordered identified findings; error diagnostic; blocking; tool, configuration, and environment identities; evidence references; affected paths; child-result identities for composites; and exact claim boundary. Composite findings remain ordered and explicit rather than introducing a second result type.

| Status | Required invariant |
|---|---|
| `not_applicable` | If and only if applicability is not applicable, the requirement/profile permits it, and a nonempty not-applicable reason is recorded; other statuses require applicable and no not-applicable reason. |
| `pass` | Execution completed; no applicable requirement failed; no error diagnostic or blocking finding exists. |
| `fail` | Execution completed and at least one identified applicable requirement failed. |
| `error` | Validation could not establish pass or fail and carries a nonempty error diagnostic. |
| `not_run` | The invocation did not execute or complete and carries no fabricated success evidence. |

`blocking` is derived, never chosen independently, from identified requirement/profile criticality and findings. A required `error`, `not_run`, or `fail` blocks the gate. A composite preserves child identities and findings and derives its status over all applicable child invocations with precedence `error`, then `not_run`, then `fail`, then `pass`; child requirement criticality affects `blocking`, not whether the child's outcome contributes to composite status. Composite `not_applicable` is permitted only when the composite requirement permits it and no child invocation is applicable. Contradictory combinations are invalid.

A structural pass establishes only the rules represented by that result. It does not establish test success, repository-wide conformance, mechanical promotion eligibility, numerical verification, scientific validation, protected authority, or human acceptance.

## Candidate artifact-set validation

`HarnessArtifactSetValidator` is a separate target-first ActionObject. It consumes one already complete immutable `HarnessArtifactSet` plus applicable explicit `HarnessArtifactValidationPolicy` and `HarnessArtifactValidationContext`. It returns the same normative `ValidationResult`, bound to the exact candidate-set, manifest, policy, context, validator, and rule-version identities.

It owns only invariants whose subject exists after projection:

- root confinement and destination uniqueness;
- complete manifest closure;
- supported projection and format versions;
- declared-versus-observed content identity;
- structured-projection relational integrity;
- deterministic SQL where applicable;
- closure of mutable resources;
- absence of forbidden SQLite WAL, SHM, and journal sidecars; and
- agreement of candidate, manifest, artifacts, and generating `HarnessStateIdentity`.

`HarnessStateValidator` and its domain owners retain source-owned destination policy and normalized-state invariants. Candidate validation neither reinterprets source authority nor repairs the candidate. `HarnessSynchronizer` and `HarnessStateComparator` require an applicable `pass` for the exact complete candidate and explicit policy/context plus exact affirmative authorization for their respective operation. They verify result bindings but never validate silently or reinterpret authority policy. An incomplete candidate, identity mismatch, denied or erroneous authorization, failed target precondition, or `fail`, `error`, `not_run`, or `not_applicable` validation result produces the target operation's represented blocked outcome and no write or comparison.

## Unresolved issues

- Exact `ValidationResult` and `ValidationFinding` wire formats.
- Whether normalized-state cross-domain rules are owned by dedicated validators or a narrow closure phase in `HarnessStateValidator`.
- Severity vocabulary and fail/continue policy.
- Validator rule-version compatibility policy.

## Target-operation and promotion ownership

`HarnessProjector`, `HarnessStateComparator`, and `HarnessSynchronizer` each own their target-specific preconditions and verify exact validation and authorization bindings without rerunning validation or resolving authority. No public harness-operation eligibility evaluator or result exists. A private domain helper may remove demonstrated implementation duplication but owns no policy, authority, public result, or retained state.

`PromotionEligibilityEvaluator` remains the sole mechanical promotion gate because promotion aggregates required conformance results for downstream repository governance. `HarnessArtifactSetValidator` owns post-projection candidate facts but grants neither operation authorization nor promotion authority.
