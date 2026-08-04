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
patching. Public Python, runtime acceptance, tests, applicable schemas, and
Sphinx documentation must agree on stored types and structured errors. A Rust
mapping must also agree only when the contract is explicitly language-independent,
uses a shared wire format, is approved for Rust implementation, or the active
task requires cross-language conformance.  Module-level field validators and generic helper modules remain
prohibited; limited owner-local duplication is preferred.  Numerical norms and
residual computations must be scale-safe and must surface structured numerical
errors rather than silent ``inf`` or ``nan`` results.  Reviews must report file
evidence, commands, findings, and a PASS or FAIL conclusion.

## CPN-compatible review invocation contract

This skill supplies a bounded architecture-review capability; it is not a CPN
guard or transition and it cannot accept architecture. The agent/harness invokes
it outside guard evaluation.

Required immutable inputs:

- task and parent-workflow/attempt identifiers;
- artifact references or exact repository paths to review;
- the requested ownership-review scope;
- authoritative architecture/reference paths;
- permitted mutation scope, which defaults to `none`;
- expected result shape and termination policy.

Allowed side effects are read-only inspection and deterministic read-only
commands unless a separately authorized writer assignment explicitly names
owned files. It must not launch downstream tasks, alter scientific meaning, or
treat reviewer agreement as acceptance.

The result must report:

```text
skill identity and content hash
request, task, parent-workflow, and attempt identities
input artifact identities
files and references inspected
owned task class
PASS | FAIL | BLOCKED
structured findings with severity and file/line evidence
deterministic commands and exact results
mutation summary
warnings and residual risks
human decisions required
```

A missing authoritative reference, contradictory authority, or protected public
contract choice returns `BLOCKED`; it is not silently resolved. A retry requires
an immutable parent authorization identity or a request's pre-authorized retry
policy, uses a new attempt identity, and retains prior findings. Repeating the same read-only
request against the same artifact identities is observationally idempotent.
Stop after the requested review result; do not implement, accept, or launch the
reviewed work.
