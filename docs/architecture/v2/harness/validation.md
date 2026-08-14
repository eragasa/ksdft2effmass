# Development validation

## Purpose

Development validation evaluates one coherent `HarnessStateSnapshot` without changing it. Domain rules remain with concrete domain validators; aggregate composition and cross-domain closure belong to `HarnessStateValidator`.

## Validation layers

1. **Wire validation** is owned by each domain serializer or deserializer.
2. **Domain validation** is owned by the applicable domain ActionObject, such as validators under `harness.tasks`.
3. **Aggregate validation** checks coherence among independently represented domain records in one `HarnessStateSnapshot`.

Compilation does not absorb any of these rule sets.

## Protocol

```python
class HarnessDomainValidator(Protocol):
    @property
    def rule_identities(self) -> tuple[ValidationRuleIdentity, ...]: ...

    def execute(self, state: HarnessStateSnapshot) -> DomainValidationResult: ...
```

The protocol provides structural polymorphism only. It supplies no registry, discovery, default rules, mutation, repair, or authorization.

## Concrete validators

| Validator | Rule ownership |
|---|---|
| `HarnessTaskValidator` | Task-definition rules owned by `harness.tasks` |
| `HarnessTaskClosureValidator` | Closure identity, selection correlation, and disposition rules owned by `harness.tasks` |
| `DevelopmentTaskSelectionValidator` | Selection consistency rules owned by `harness.tasks` |
| `HarnessTaskGraphValidator` | Task relation and graph rules owned by `harness.tasks` |
| `HarnessDecisionCatalogValidator` | Decision identity and resolution consistency |
| `HarnessCapabilityCatalogValidator` | Capability identity and relationships |
| `HarnessResourceCatalogValidator` | Resource dependencies, closure, and layering |
| `HarnessEvidenceCatalogValidator` | Evidence identity, ownership, and claim boundaries |

Eligibility, closure evaluation, and acceptance evaluation are Task-domain operations, not generic aggregate validation.

## Composition

`HarnessStateValidator` receives an explicit ordered tuple of `HarnessDomainValidator` objects. It applies them deterministically, evaluates only declared cross-domain closure, and returns one `ValidationResult` containing snapshot identity, rule identities and versions, ordered findings, and claim boundary.

A structural pass establishes only the rules represented by that result. It does not establish test success, numerical verification, scientific validation, protected authority, or human acceptance.

## Unresolved issues

- Exact `DomainValidationResult` and `ValidationFinding` wire formats.
- Ownership of each cross-domain closure rule.
- Severity vocabulary and fail/continue policy.
- Validator rule-version compatibility policy.
- Whether wire validation results are retained in `HarnessSourceSnapshot`.
