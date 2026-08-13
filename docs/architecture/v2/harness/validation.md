# Development validation

## Purpose

Development validation evaluates one normalized `HarnessState` without changing it. Domain rules remain with concrete domain validators; composition belongs to `HarnessStateValidator`.

## Protocol

```python
class HarnessDomainValidator(Protocol):
    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]: ...

    def execute(self, state: HarnessState) -> DomainValidationResult: ...
```

The protocol provides structural polymorphism only. It supplies no registry, discovery, default rules, mutation, repair, or authorization.

## Concrete validators

| Validator | Rule ownership |
|---|---|
| `HarnessTaskCatalogValidator` | Task identities and catalog invariants |
| `DevelopmentTaskSelectionValidator` | Selection eligibility and consistency |
| `HarnessTaskGraphValidator` | Parent/prerequisite references, cycles, and closure |
| `HarnessDecisionCatalogValidator` | Decision identity and resolution consistency |
| `HarnessCapabilityCatalogValidator` | Capability identity and relationships |
| `HarnessResourceCatalogValidator` | Resource dependencies, closure, and layering |
| `HarnessEvidenceCatalogValidator` | Evidence identity, ownership, and claim boundaries |

## Composition

`HarnessStateValidator` receives an explicit ordered tuple of `HarnessDomainValidator` objects. It applies them deterministically, evaluates cross-domain closure, and returns one `ValidationResult` containing state identity, rule identities and versions, ordered findings, and claim boundary.

A structural pass establishes only the rules represented by that result. It does not establish test success, numerical verification, scientific validation, protected authority, or human acceptance.

## Unresolved issues

- Exact `DomainValidationResult` and `ValidationFinding` wire formats.
- Whether cross-domain rules are owned by dedicated validators or a narrow closure phase in `HarnessStateValidator`.
- Severity vocabulary and fail/continue policy.
- Validator rule-version compatibility policy.
