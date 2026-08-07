# Consolidated independent review

**Disposition: FAIL**

Profile: `REVIEW_ONLY`

Mutation summary: none.

## Blocking finding

### B1 — Unauthorized production-source mutation

`python/src/ksdft2effmass/harness/pi/evidence.py:154` changes production behavior from `clean=False` to `clean=True`.

This conflicts with:

- `.pi/tasks/TEST-EVIDENCE-CONVENTIONS-2.md:20-21`, which explicitly leaves production source unauthorized.
- `.pi/evidence/test-evidence-repository-conformance/task-ownership.json:11-33`, whose writer paths exclude `python/src/`.
- The validated manifest, which therefore does not authorize this change.

Moreover, `.pi/evidence/test-evidence-repository-conformance/m4-invocation.json` self-declares that production path permitted, but an invocation record cannot expand the controlling task or manifest.

The parser correction itself is deterministic and has focused evidence, but it requires proper production-source ownership/authority before integration.

## High findings

### H1 — Generated, tautological evidence prose remains widespread

An AST scan of all 182 inventoried modules found **105 functions across 21 modules** containing tautological generated requirements such as:

> `The public <owner> contract must <function-name-derived phrase>.`

or merged placeholder-like prose such as `method and oracle` and `interpretation and limitations`.

Representative examples:

- `python/tests/numerical_verification/ksdft2effmass/operators/test__OperatorRecordResidualAnalyzer__floating_point.py:243-267`
- same file `:274-298`
- same file `:349-376`
- same file `:558-574`
- `python/tests/software_verification/ksdft2effmass/integration/test__operator_record_json_schema.py:47-70`
- same file `:74-98`
- `python/tests/software_verification/ksdft2effmass/integration/test__operator_record_json_fixtures.py:60-83`
- same file `:87-111`

For example, “must binary64 ulp distance” does not state a public requirement, while the generic Method/Oracle/Acceptance text does not document the helper’s actual bit-ordering assumptions. This violates the non-tautological requirement, oracle, acceptance, interpretation, and helper-ownership expectations in the authoritative convention.

Affected files include the numerical residual modules, operator JSON/schema modules, difference/comparison result modules, serializer modules, residual analyzer contract, differencer, and comparator workflow.

### H2 — Equality/frozen recurrence enforcement has semantic holes

The validator recognizes only narrow phrases:

- `harness/pi/validation/validate_python_test_evidence.py:73-78`
- enforcement at `:824-840`

Consequently, synonymous complete-state claims pass without the required inventories or complete exercise.

Concrete example:

- `python/tests/software_verification/ksdft2effmass/operators/test__OperatorRecordDifferenceResult__value_semantics.py:148-175` claims frozen dataclass state but mutates only `energy_unit`.
- The same module at `:229-253` claims “complete public state” equality without an `EQUALITY_FIELDS` inventory.
- No `FROZEN_FIELDS` or `EQUALITY_FIELDS` declaration exists in that module.

Thus the recurrence control does not prevent the exact incomplete frozen/equality defect that this task was activated to eliminate.

### H3 — Numerical tolerance justification is insufficient for the stated evidence class

The floating-point module applies eight ULPs across scalar magnitude, Frobenius, and spectral/SVD paths:

- `python/tests/numerical_verification/ksdft2effmass/operators/test__OperatorRecordResidualAnalyzer__floating_point.py:44-52`
- enforcement at `:300-303`

The prose calls eight ULPs “conservative” while explicitly disclaiming a formal bound. It does not derive why eight ULPs is adequate for each algorithmic path, backend, and tested regime. The 64-epsilon normal-value rule is similarly presented as a regression criterion rather than a derived error bound.

This can support bounded regression evidence, but the current documentation does not adequately justify the acceptance rule for numerical-verification claims as required by the authoritative convention. The exact-zero cases and analytical oracles themselves are otherwise appropriately separated from approximate cases.

## Bounded control-plane correction

The documented preflight command is incomplete for this non-default chain:

- `.pi/task-ownership/README.md:11-13` instructs `--task` only.
- `.pi/task-ownership/validate_task_ownership.py:733-738` silently defaults to another chain.

Observed result:

```text
python .pi/task-ownership/validate_task_ownership.py \
  --task TEST-EVIDENCE-CONVENTIONS-2
→ FAIL: expected exactly one chain task 'TEST-EVIDENCE-CONVENTIONS-2'
```

The task-specific invocation passes:

```text
python .pi/task-ownership/validate_task_ownership.py \
  --chain .pi/chains/test-evidence-repository-conformance.chain.json \
  --task TEST-EVIDENCE-CONVENTIONS-2
→ PASS
```

The README or command routing should prevent this misleading default failure.

## Evidence inventory and favorable observations

The repository completion gate directly established:

- 182 discovered and inventoried modules;
- 155 class-owned modules;
- 27 artifact-owned modules;
- 178 software-verification modules;
- 4 numerical-verification modules;
- 1,021 test functions and unique evidence owners;
- 2,569 collected nodes;
- zero structural findings.

Additional consolidated checks found:

- All seven `test_protocol__str__...` owners exercise genuine `str()`/`StrEnum` protocol behavior; no vague protocol misuse was found.
- No vague `behavior`, `contract`, `general`, or `misc` test surfaces were found.
- M1–M4 migration maps are one-to-one and set-complete:
  - M1: 1,252 mappings
  - M2: 91
  - M3: 920
  - M4: 120
- Artifact/class ownership and the lowercase artifact renames are structurally synchronized with the inventory.
- Schema, fixture, and runtime modules remain separately owned, although their evidence prose needs correction.
- The maintained comparison dependency-direction owner remains
  `python/tests/software_verification/ksdft2effmass/integration/test__operator_comparison_dependency_direction.py`.
- Agent routing distinguishes test writing, read-only VVUQ review, and repository-conformance closure.
- Unrelated Graphify, CPN-audit, research, computational, proof, and control-plane dirty paths were excluded from semantic review.

## Commands and results

```text
ownership preflight with explicit chain
PASS

python harness/local/validation/validate_repository_test_evidence.py
PASS — 182 modules, 2,569 nodes, zero structural findings

maintained inventory pytest
2,567 passed, 2 setup errors
```

The two errors are in `test__package_wheel.py` because the `uv` project environment lacks `pip`; they are environmental setup errors, not assertion failures.

```text
ruff check over all 182 inventoried modules
PASS

migration-map uniqueness/set-equality script
PASS for M1–M4

git diff --check over in-scope paths
PASS
```

No scientific validation, UQ, or human acceptance is established or claimed.