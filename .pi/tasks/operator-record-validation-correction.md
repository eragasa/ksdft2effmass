# Operator-record validation correction

Status: active

## Context

This corrective task records explicit human decisions for a repository-wide architecture, implementation, testing, and documentation pass over the maintained `ksdft2effmass` operator-record package. It is the active authority for this correction and does not rewrite historical E00/E01 or earlier operator-record task evidence.

Historical records including `.pi/tasks/operator-record-refactor.md` and `.pi/tasks/operator-record-comparison.md` are preserved as historical evidence only. Newly discovered defects and corrections are recorded prospectively here.

## Human decisions recorded

1. Current comparison is limited to two already-compatible finite `OperatorRecord` representations. It performs no basis alignment, permutation discovery, gauge alignment, energy-zero alignment, unit conversion, geometry transformation, approximate metadata matching, physical-equivalence determination, or scientific validation. For compatible records, `Delta H = H_candidate - H_reference`. Public metrics are maximum-entry, Frobenius, and spectral norms with the compared matrix energy unit, satisfying `0 <= maximum <= spectral <= Frobenius`; metrics are symmetric although role identifiers are retained.
2. Every public compatibility mismatch code must be reachable by comparing two independently valid public `OperatorRecord` instances. The schema-version-1 orthonormality-convention mismatch is unreachable and must be removed from implementation, tests, task statements, and documentation. Invalid-state fabrication by invariant bypass is prohibited.
3. `OperatorRecordCompatibilityIssue` must use the mismatch code as authoritative state and expose a canonical derived description. No compatibility alias for the old free-form constructor is retained absent released-user evidence.
4. `OperatorRecordCompatibilityResult` has one exact public boundary: tuple `issues`, derived `is_compatible`, derived `rules_applied`, duplicate issue rejection, canonical enum ordering, and agreement among annotations, runtime acceptance, stored types, tests, documentation, and Rust mapping. Lists are not silently accepted.
5. Hermiticity residual has the same energy unit as the represented matrix. `HermiticityAnalyzer(tolerance: float, energy_unit: str)` requires an explicit unit, `HermiticityResult` stores `residual`, `tolerance`, and `energy_unit`, exact unit equality with `record.energy_reference.unit` is required, unit conversion is not authorized, unit mismatch and failed requirements use structured public exceptions, and Hermiticity checking is fixed-representation software verification.
6. Maintained DataObjects and ResultObjects are operationally immutable. `OperatorRecord.matrix` must not be mutable through `record.matrix.setflags(write=True)`. Defensive constructor ownership, immutable provenance, immutable nested metadata, exact structural equality, and unhashability where exact hashing is unsafe are required.
7. Dangling module-level field-validation helpers are prohibited. Validation ownership follows DataObject intrinsic validation, ActionObject policy validation, serializer wire validation, no cross-object private-method calls, limited duplication over ambiguous ownership, named object for shared domain concepts, and ownerless free functions only for independently specified mathematics or external callbacks.
8. Norm implementations must be scale-safe; comparison detects nonfinite subtraction intermediates and numerical failures and reports structured numerical errors instead of returning silent `inf`, `nan`, or avoidable zero.
9. Maintained public APIs reject booleans for numeric semantics, reject numeric strings, define accepted Python and NumPy scalar types, canonicalize to built-in Python scalar types, handle conversion overflow by documented taxonomy, validate nested public object types, avoid public duck typing, eliminate essential `Any`, contain parser dynamics at JSON boundary, and synchronize Python, tests, schemas, docs, and Rust mapping.
10. Maintained source must satisfy the source-documentation standard. Tests use valid ordinary fixtures and exact exception taxonomy. No scientific validation is authorized or claimed.

## Affected files

Authorized scope includes `AGENTS.md`, relevant `.pi/skills/`, `.pi/agents/`, `.pi/chains/`, `.pi/tasks/`, maintained source under `python/src/ksdft2effmass/`, tests under `python/tests/`, required synchronization in `specification/`, and maintained Sphinx documentation under `docs/`.

Graphify integration is excluded unless an active reference is directly broken. Remote processing, hooks, global skills, releases, tags, publication claims, and new scientific capabilities are excluded.

## Deterministic findings and corrections

- D001: Active policy and control-plane artifacts did not yet durably encode the human-approved comparison, compatibility, Hermiticity-unit, immutability, typing, and numerical-robustness corrections. Correction: update this task record, root policy, project skills, agents, and a new corrective chain before production changes.
- Further deterministic findings discovered during execution are to be recorded here or in a subordinate correction log, corrected, and revalidated without a human checkpoint when uniquely resolved by this contract.

## Public API corrections

- Remove the unreachable orthonormality mismatch code.
- Make compatibility issue descriptions canonical and derived from mismatch codes.
- Make compatibility results tuple-only with canonical ordering and duplicate rejection.
- Add unit-bearing Hermiticity result/analyzer and structured Hermiticity errors.
- Add structured comparison numerical errors and scale-safe comparison metrics.
- Preserve public DataObject/ActionObject/ResultObject separation and no compatibility aliases.

## Implementation order

1. Recorded contract.
2. Control-plane update.
3. Architecture review.
4. Production implementation.
5. Object and integration tests.
6. Sphinx documentation.
7. Combined-tree verification.
8. Independent numerical/architecture review.
9. Independent test review.
10. Independent documentation review.
11. Final read-only integration review.
12. Parent verification.
13. Human final acceptance.

## Validation gates

Python 3.14 version check, package metadata validation, dependency check, Ruff format check, Ruff lint check, mypy, maintained-module inventory, public API versus object-test inventory, targeted record/Hermiticity/compatibility/comparison/serializer tests, integration tests, full pytest, schema and fixture validation, public-import smoke test, JSON round trip, deterministic serialization, source/Sphinx synchronization audit, no-`:undoc-members:` scan, no-dangling-helper scan, no-cross-private-call scan, invalid-state-fabrication scan, stale API and terminology scan, and Sphinx warning-as-error build.

## Review roles

Writer agents may not provide independent acceptance of their own work. Separate read-only reviews are required for architecture/numerical/Rust portability, tests/fixtures/exception taxonomy/invalid-state fabrication, source and Sphinx documentation synchronization, and final combined-tree integration.

## Human final acceptance

After verification and independent reviews, stop and report. Human final acceptance remains required before closing this task or selecting any next scientific task.

## Correction log from independent reviews

- D002: Architecture review found Hermiticity residual subtraction overflow could surface as a generic nonfinite-result failure. Correction: added structured `HermiticityNumericalError`, documented it, and added tests for subtraction overflow.
- D003: Test review found missing extreme-scale comparison tests and broad exception tuples. Correction: added `1e200`, `1e-200`, and subtraction-overflow comparison tests; replaced broad exception tuples with exact expected exception types.
- D004: Documentation/integration reviews found incomplete Hermiticity and comparison concept/source documentation, including numerical failure modes, norm inequalities, and private-method rationale. Correction: synchronized Sphinx concept/API pages and expanded source docstrings/comments until final integration review passed.
- D005: Integration review found stale historical comparison-task statements requiring the now-removed orthonormality mismatch. Correction: marked the historical comparison task as superseded by this active corrective task and removed the stale requirement without rewriting historical E00/E01 evidence.

## Review results

Independent architecture/numerical/Rust-portability review: PASS after correction loop.
Independent test/fixture/exception-taxonomy review: PASS after correction loop.
Independent documentation review: PASS after correction loop.
Final read-only integration/source-documentation review: PASS after correction loop.
