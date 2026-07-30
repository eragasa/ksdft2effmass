---
name: design-data-action-objects
description: Applies the repository DataObject/ActionObject architecture. Use for new scientific object models, substantial refactors, object ownership questions, and Python designs that must remain portable to Rust.
---

# Design DataObject/ActionObject Models

Use this skill before changing public scientific object boundaries or adding nontrivial behavior to a data model.

## Load first

Read `references/data-action-architecture.md` for the authoritative rules and checklist.

## Quick routing

- Intrinsic data invariant: method or constructor validation on the owning DataObject.
- Numerical or analysis policy: ActionObject.
- Serialization or wire-format rule: serializer ActionObject.
- Operation output: explicit immutable ResultObject.
- Domain-independent mathematics: free function only when no domain owner exists.
- Workflow: concrete ActionObject only for a reusable scientifically or computationally meaningful sequence with explicit DataObject/ResultObject inputs, outputs, and dependencies.

Do not create a production Workflow merely to own a technical integration test.

## Examples

Positive:

```python
@dataclass(frozen=True, slots=True)
class SpectrumWindow:
    emin: float
    emax: float


@dataclass(frozen=True, slots=True)
class WindowProjector:
    tolerance: float

    def execute(self, bands: BandSet, window: SpectrumWindow) -> ProjectionResult: ...
```

Negative:

```python
class OperatorRecord:
    def to_dict(self): ...  # serialization belongs to a serializer ActionObject
    def require_hermitian(self): ...  # tolerance policy belongs to an analyzer
```

Avoid new abstract base classes until several real implementations require the same interface.

## Corrective operator-record policy

DataObjects and ResultObjects are operationally immutable: public arrays and
nested metadata must not be mutable through ordinary public APIs such as
``setflags(write=True)``.  Intrinsic validation belongs to the owning object,
relational compatibility belongs to a named ActionObject, and policy validation
with units belongs to the ActionObject that owns the policy.  Public enum and
error states must be reachable from independently valid public objects; tests
must not manufacture invalid states with ``object.__setattr__`` or monkey
patching.  Public Python, documented Rust mapping, runtime acceptance, tests,
schemas, and Sphinx documentation must agree on stored types and structured
errors.  Module-level field validators and generic helper modules remain
prohibited; limited owner-local duplication is preferred.  Numerical norms and
residual computations must be scale-safe and must surface structured numerical
errors rather than silent ``inf`` or ``nan`` results.  Reviews must report file
evidence, commands, findings, and a PASS or FAIL conclusion.
