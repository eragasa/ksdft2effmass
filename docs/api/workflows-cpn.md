# CPN public API

The supported import surface is:

```python
from ksdft2effmass.workflows.cpn import CpnNetDefinition, TransitionEnabler
```

All DataObjects and ResultObjects are frozen, slotted dataclasses. Collection
fields are immutable tuples. Set-like identity tuples are unique and canonical;
ordered `string_sequence` values preserve duplicates. ResultObjects validate
matching transition identity, successor revision, and unique nonempty audit IDs.
ActionObjects are concrete, stateless classes with explicit verbs. The contract
is designed to translate structurally to Rust as validated immutable structs,
exhaustive enums, owned vectors, `Option` fields, immutable borrows during
evaluation, and `Result` with exhaustive structured error state. The intended
numeric scalar mappings are Python built-in binary64 `float` to Rust `f64` and
signed-i64 Python `int` to Rust `i64`; no Rust implementation or attested
cross-language conformance is provided by P1.

`ContractValue(ContractValueKind.REAL, value)` accepts only exact built-in
Python `int` or `float` values except `bool` and stores a finite IEEE-754
binary64 built-in `float`. Integer conversion uses round-to-nearest,
ties-to-even. If $M=(2-2^{-52})2^{1023}=2^{1024}-2^{971}$ is the maximum finite
binary64 value, general noninteger number values are bounded inclusively by
$\pm M$. Built-in Python `int` values and integer-valued JSON `real` inputs are
instead admitted through the exact inclusive endpoints
$\pm L$, where $L=2^{1024}-2^{970}-1$. Consequently, integers above $M$ can
remain valid: $M+1$ is admitted and rounds to $M$, while $\pm(L+1)$ overflows
and is rejected. Conversion overflow or a nonfinite input/result raises
`ValueError`. The tagged-`real` JSON Schema expresses the separate integer and
general-number domains. Strict JSON wire input excludes `NaN`, `Infinity`, and
`-Infinity`; an in-memory Python `nan` supplied directly to `jsonschema` is not
a permitted wire value, regardless of that validator's ordered-bound behavior.
`ContractValueKind.INTEGER` accepts only exact built-in `int` values except
`bool` in $[-2^{63},2^{63}-1]$ and preserves them exactly. There is no unsigned
`ContractValue` kind.

## Routing tokens

- `ContractValueKind`, `ContractValue`
- `OutcomeStatus`, `OutcomeScope`, `OutcomeTerminality`, `TokenOutcome`
- `TokenField`, `CpnToken`

## Declarative expressions

- `ValueExpressionKind`, `ValueExpression`
- `GuardOperator`, `GuardExpression`, `GuardEvaluationResult`
- `TokenFieldAssignment`, `TokenTemplate`
- `CpnExpressionEvaluator.evaluate_value()` and `.evaluate_guard()`

The version-1 expression API selects literals, token fields, or bound-token IDs;
it has no arithmetic operator and does not compute
`iteration_index = current + 1`. Repeated or cyclic execution consists of
successive enabled firings. Each output `iteration_index` is supplied explicitly
or copied by a `TokenFieldAssignment`, and repeated values are permitted. Any
future automatic advancement requires a future ActionObject or a separately
authorized expression revision.

Every expression-visible nonnegative P1 version-1 control is in
$[0,2^{63}-1]$. This includes `CpnMarking.revision`,
`FiringResult.previous_revision`, `CpnToken.iteration_index`, and
`CpnToken.payload_schema_version` when present. They therefore pass through
`ContractValueKind.INTEGER` and remain representable by Rust `i64`. At the upper
revision endpoint, `TransitionFirer.execute()` raises `CpnFiringError` whose
`detail.code` is `CpnErrorCode.REVISION_OVERFLOW`; it does so before evaluating
outputs or constructing a successor.

## Markings and model

- `PlaceMarking`, `CpnMarking`
- `TokenBinding`, `TransitionBinding`
- `ArcDirection`, `InputArcMode`
- `ColorDefinition`, `PlaceDefinition`, `TransitionDefinition`
- `TokenPattern`, `InputInscription`, `OutputInscription`, `ArcDefinition`
- `CpnNetDefinition`

## Validation and execution

- `CpnIssueCode`, `CpnValidationIssue`, `CpnValidationResult` (also represented
  by the version-1 language-neutral validation schema)
- `CpnDefinitionValidator.execute()`, `CpnMarkingValidator.execute()`
- `TransitionEnablementResult`, `TransitionEnabler.execute()`
- `FiringRequest`, `FiringResult`, `TransitionFirer.execute()`

## Structured exceptions

Every exception retains `CpnErrorDetail` with stable `CpnErrorCode`, explanatory
message, and optional model, transition, place, and token identities:

- `CpnContractError`
- `CpnDefinitionError`, `CpnMarkingError`, `CpnBindingError`
- `CpnGuardEvaluationError`, `TransitionNotEnabledError`, `CpnFiringError`

```{automodule} ksdft2effmass.workflows.cpn.tokens
:members:
```

```{automodule} ksdft2effmass.workflows.cpn.expressions
:members:
```

```{automodule} ksdft2effmass.workflows.cpn.markings
:members:
```

```{automodule} ksdft2effmass.workflows.cpn.model
:members:
```

```{automodule} ksdft2effmass.workflows.cpn.validation
:members:
```

```{automodule} ksdft2effmass.workflows.cpn.execution
:members:
```

```{automodule} ksdft2effmass.workflows.cpn.errors
:members:
```

This API is control-flow software. True u64 artifact sizes and counters are
deferred P2 fields that would require their own explicit types; P1 implements
neither those fields nor an unsigned expression-value tag. `P1-HC01` Option A and `P1-HC02` Option B are resolved. Final P1 acceptance
was granted as Option A through `P1-HC03` on 2026-08-04, after reviews and
parent verification; P1 is closed as human-accepted `PASS`. No successor was
selected or launched, and P2--P11 and production or scientific execution
remain blocked and unauthorized. The API reports no physical units or
scientific acceptance criterion and supplies no numerical verification,
scientific validation, or uncertainty quantification.
