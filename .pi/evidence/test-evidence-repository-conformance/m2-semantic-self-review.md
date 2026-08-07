# M2 semantic self-review

Status: **PASS for the supplied M2 scope**. Structural PASS is reported separately and does not establish these semantic findings or human acceptance.

## Ownership and surfaces

- Reviewed all 37 inventoried modules: 32 public CPN classes remain class-owned with filename/import/`SUT` agreement; five package/schema/fixture/dependency/engine boundaries remain artifact-owned.
- Constructor, field, action-method, and artifact names identify the exercised public surface. `evaluate_value` and `evaluate_guard` evidence is separated. No equality operation is mislabeled as a property or protocol.
- `conftest.py` constructs only public synthetic inputs, owns no evidence ID, and records complete supporting-ID inventories.

## Cohesion and partitions

- Removed all hidden `for` statement case loops from collected tests and nontrivial helpers.
- Split valid state, wrong semantic types, malformed values, and distinct public method shapes.
- Added explicit semantic `pytest.param` IDs for fixture, enum-agreement, numeric-boundary, outcome, and schema cases.
- Separated schema shape, strict JSON parsing, runtime constructor behavior, relational validation, public error translation, dependency direction, public API, and deferred-engine isolation.

## Oracles and acceptance

- Exact language types, signed-i64 endpoints, binary64 conversion boundaries, strict JSON behavior, fixed schema/fixture classifications, fixed public error codes, and fixed synthetic routing state supply independently inspectable oracles.
- The public API owner now compares against a literal 49-name inventory rather than deriving expected names from `__all__`.
- Schema/Python enum checks are explicitly agreement relations; neither side is claimed as an independent scientific oracle.
- Acceptance remains exact. No approximate tolerance, warning allowance, numerical-verification claim, scientific-validation claim, or UQ claim was introduced.

## Preservation review

- The baseline 91 collected nodes map one-to-one to successors with the same authoritative evidence IDs.
- All baseline assertions, exception expectations, fixtures, synthetic inputs, and public calls remain represented. Semantic splits add 132 nodes and 85 new evidence owners (`SV-CPN-089` through `SV-CPN-173`).
- No production, schema, fixture, dependency, specification, provenance/operator/harness test, historical evidence, or checkpoint path was intentionally modified.

## Pass/fail interpretation and exclusions

Passing supports only the named CPN software contracts and artifact agreements under the synthetic/version-1 cases. Failure can indicate implementation, fixture, schema, oracle transcription, environment, dependency, or public-contract drift according to the owner. M2 does not establish physical correctness, numerical verification, scientific validation, uncertainty quantification, external engine correctness, persistence compatibility beyond the exercised version-1 artifacts, Rust agreement, release readiness, or human acceptance.
