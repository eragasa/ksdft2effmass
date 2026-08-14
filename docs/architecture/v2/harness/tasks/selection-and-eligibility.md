# Harness Task selection and eligibility

## Distinct meanings

Eligibility and selection are separate:

- `HarnessTaskEligibilityResult` reports whether an exact Task revision can be selected under explicit graph, lifecycle, decision, and scope inputs.
- `DevelopmentTaskSelection` records which exact eligible Task revision is authorized as active work in one declared control scope.

Eligibility grants no authority. Selection does not establish completion or acceptance.

```mermaid
flowchart LR
    task["HarnessTask revision"] --> evaluator["HarnessTaskEligibilityEvaluator"]
    graph["HarnessTaskGraph revision"] --> evaluator
    closures["HarnessTaskClosure catalog"] --> evaluator
    decisions["Resolved decision references"] --> evaluator
    scope["Control scope"] --> evaluator
    evaluator --> result["HarnessTaskEligibilityResult"]
    result --> selector["HarnessTaskSelector"]
    authority["Explicit authority"] --> selector
    selector --> selection["DevelopmentTaskSelection"]
```

## Selection invariants

- A selection references an exact Task definition revision.
- A selection identifies its control scope and authority reference.
- At most one active selection exists per control scope unless a later accepted contract permits otherwise.
- The selected Task must be eligible under the recorded input revisions.
- Explicit activation requirements must be satisfied by explicit authority.
- Automatic successor activation is disabled by default.
- A projection, passing check, elapsed time, or reviewer conclusion cannot create selection.

## Operations

| ActionObject | Responsibility |
|---|---|
| `HarnessTaskEligibilityEvaluator` | Evaluate graph, state, decision, and scope conditions |
| `HarnessTaskSelector` | Construct a selection from eligibility and explicit authority |
| `DevelopmentTaskSelectionValidator` | Validate one represented selection against supplied revisions |

Each operation returns an immutable ResultObject with findings and exact input identities. It does not mutate the Task catalog or repository.

## Unresolved issues

- Whether selection expiry or revocation is represented as a new selection revision or transition record.
- Exact control-scope identity contract.
- Whether multiple independent repository scopes may be selected concurrently.
- Required authority fields for routine versus human-owned boundaries.
- Whether selection replacement requires a closure for the prior selection.
