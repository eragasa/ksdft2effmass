# P1 independent tests/schema/VVUQ review

## Verdict: FAIL

Focused pytest, Ruff, mypy, public import, JSON Schema checks, and Sphinx all pass, but the maintained evidence audit fails on every new P1 test module and material contract/evidence gaps remain. This review does not accept or close P1.

## Findings

1. **HIGH — P1 evidence is not registered with the maintained VVUQ marker required by the repository audit.**  `.pi/skills/audit_evidence_identifiers.py --strict` reports all ten new P1 modules as errors because each lacks the exact executable module marker `pytestmark = pytest.mark.software_verification`. The affected module starts are:
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnToken__contract.py:1`
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__DeclarativeExpressions.py:1`
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnDefinitionAndMarking.py:1`
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__TransitionExecution.py:1`
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__RetryRecoveryIteration.py:1`
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnStructuredErrorsAndImports.py:1`
   - `python/tests/software_verification/ksdft2effmass/integration/test__CpnJsonSchemas.py:1`
   - `python/tests/software_verification/ksdft2effmass/integration/test__CpnJsonFixtures.py:1`
   - `python/tests/software_verification/ksdft2effmass/integration/test__CpnDependencyDirection.py:1`
   - `python/tests/software_verification/ksdft2effmass/integration/test__CpnSnakesIsolation.py:1`
   This is an acceptance-gate failure even though pytest collects the tests by path.

2. **HIGH — two exported validation enum states are unreachable from valid public objects.** `CpnIssueCode.WRONG_ARC_INSCRIPTION` and `CpnIssueCode.EXPRESSION_TYPE_MISMATCH` are publicly declared at `python/src/ksdft2effmass/workflows/cpn/validation.py:24` and `:29`, but neither is emitted anywhere by either public validator. `ArcDefinition` prevents a wrong direction/inscription combination during valid construction, while `CpnDefinitionValidator` performs no expression-type analysis. This conflicts with the repository rule that public enum and structured-error states be reachable from independently valid public objects. No P1 test covers either state.

3. **HIGH — the language-neutral schema omits exported structured validation/result contracts.** Python publicly exports `CpnIssueCode`, `CpnValidationIssue`, and `CpnValidationResult` at `python/src/ksdft2effmass/workflows/cpn/__init__.py:84-91`, but `specification/workflow-cpn/v1/cpn-contract.schema.json:1061-1125` ends with only operational `errorDetail`; it defines no validation issue code, issue, or result representation. `GuardEvaluationResult` and `TransitionEnablementResult` are likewise public but absent. Consequently the gate that public Python types, language-neutral schemas, documentation, and intended Rust mappings agree is not fully evidenced. The current schema tests only prove that the schemas which exist are metaschema-valid.

4. **MEDIUM — relational invalid fixtures are never checked against their claimed ActionObject rejection oracle.** `python/tests/software_verification/ksdft2effmass/integration/test__CpnJsonFixtures.py:74-86` merely asserts that `unknown-color`, `duplicate-token-id`, `wrong-place-set`, `unbound-guard-variable`, and `output-id-collision` pass structural schemas. Its stated oracle is the hand-written invalid-fixture classification (`:3-6`), but it never constructs the corresponding public objects or invokes `CpnDefinitionValidator`, `CpnMarkingValidator`, or `TransitionFirer`. Thus the fixtures' relational expected categories are self-classified rather than independently executable evidence.

5. **MEDIUM — the “complete supported namespace” public-import evidence checks only three symbols.** `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnStructuredErrorsAndImports.py:16-21` calls the namespace complete but checks `CpnNetDefinition`, `TransitionEnabler`, and `TransitionFirer` only; the package exports 49 names. This leaves public import/export inventory and enum/exception exposure weakly covered.

6. **MEDIUM — `CPN-SV-P1-010` does not test its documented requirement.** `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__DeclarativeExpressions.py:75-91` says bindings expose enumerated token fields and identities, but only checks that a missing variable raises `KeyError`; `executable_net` is otherwise unused. There is no positive bound-field oracle and no `BOUND_TOKEN_IDS` assertion.

7. **MEDIUM — repeated iteration is represented as data but not tested as repeated deterministic execution.** `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__RetryRecoveryIteration.py:56-148` performs one retry-style firing and checks a copied `iteration_index == 1`; `:184-207` performs one recovery firing. Neither test executes two or more iteration cycles or verifies deterministic successor markings across repeated firings. The valid `retry-recovery-iteration.json` fixture is schema-only state. This is a coverage gap against the requested deterministic repeated-iteration case, though basic representability is shown.

8. **MEDIUM — P1 identifiers do not follow the documented repository identifier shape.** `docs/verification/testing-and-evidence.rst:39-45` specifies evidence-class prefix + subsystem abbreviation + three-digit sequence (for example `SV-ORA-001`). P1 instead uses `CPN-SV-P1-001` through `CPN-SV-P1-033`, documented at `docs/verification/cpn-contract.rst:7-13`. The 33 P1 IDs are internally unique, but their syntax is inconsistent with the maintained standard and embeds the implementation phase in the stable ID.

## Positive coverage

- 33 P1 test-owner identifiers are internally unique (one owning test function each).
- Multiset multiplicity/canonical token order, synchronization, deterministic binding choice, read/consume/output behavior, one-step retry/recovery, terminal-token retention, output collision/count errors, and immutable frozen token state have focused passing cases.
- Structural schema fixtures exercise Boolean-as-integer, unsupported version, invalid terminality, lambda-like expression, and strict rejection of nonfinite JSON constants.
- Operational error schema enum values agree with `CpnErrorCode`.
- No P1 source imports SNAKES; dependency-direction AST test passes.
- Documentation and tests consistently state that P1 is software verification only and do not claim numerical verification, scientific validation, or uncertainty quantification.

## Commands run

- `cd python && uv run pytest -q tests/software_verification/ksdft2effmass/workflows/cpn tests/software_verification/ksdft2effmass/integration/test__CpnJsonSchemas.py tests/software_verification/ksdft2effmass/integration/test__CpnJsonFixtures.py tests/software_verification/ksdft2effmass/integration/test__CpnDependencyDirection.py tests/software_verification/ksdft2effmass/integration/test__CpnSnakesIsolation.py` — **passed**, 36 tests.
- `cd python && uv run ruff check src/ksdft2effmass/workflows tests/software_verification/ksdft2effmass/workflows/cpn tests/software_verification/ksdft2effmass/integration/test__CpnJsonSchemas.py tests/software_verification/ksdft2effmass/integration/test__CpnJsonFixtures.py tests/software_verification/ksdft2effmass/integration/test__CpnDependencyDirection.py tests/software_verification/ksdft2effmass/integration/test__CpnSnakesIsolation.py` — **passed**.
- `cd python && uv run mypy src/ksdft2effmass/workflows` — **passed**, 9 source files.
- `cd python && uv run sphinx-build -W -b html ../docs ../docs/_build/html` — **passed**.
- `cd python && uv run python ../.pi/skills/audit_evidence_identifiers.py --strict` — **failed**: 10 P1 marker errors; it also reported 22 pre-existing/unrelated unowned operator-difference test warnings.
- Public import/introspection smoke check — **passed**: all 49 names in `ksdft2effmass.workflows.cpn.__all__` exist.

## Residual risks

- Passing focused tests does not establish a Rust implementation, Python/Rust conformance, persistence, SNAKES adaptation, concrete workflow execution, scientific execution, numerical verification, scientific validation, or uncertainty quantification.
- Most of the 49 public objects/enums lack direct construction, invariant, exact-value, and frozen/slotted semantics evidence; the focused suite is scenario-oriented rather than a complete public-object contract inventory.
- Schema/Python agreement is checked manually and partially by fixtures; there is no exhaustive generated comparison of public fields/enums against schema definitions.
- Sphinx output was generated under `docs/_build/` by the requested validation command; no source files were edited or staged by this reviewer.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Eight severity-ranked findings include exact source/test/schema/documentation file and line references; residual risks and command outcomes are recorded."
    }
  ],
  "changedFiles": [
    ".pi-subagents/artifacts/outputs/5ffb4733/.pi/evidence/backend-neutral-cpn-P1-contract/review-tests.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "focused P1 pytest (workflow/cpn plus four CPN integration modules)",
      "result": "passed",
      "summary": "36 passed in 0.11s"
    },
    {
      "command": "focused Ruff check",
      "result": "passed",
      "summary": "All checks passed"
    },
    {
      "command": "uv run mypy src/ksdft2effmass/workflows",
      "result": "passed",
      "summary": "Success: no issues found in 9 source files"
    },
    {
      "command": "uv run sphinx-build -W -b html ../docs ../docs/_build/html",
      "result": "passed",
      "summary": "Sphinx warnings-as-errors build succeeded"
    },
    {
      "command": "uv run python ../.pi/skills/audit_evidence_identifiers.py --strict",
      "result": "failed",
      "summary": "10 P1 modules lack required software_verification module markers; 22 unrelated legacy warnings also reported"
    }
  ],
  "validationOutput": [
    "Focused runtime, lint, type, schema-fixture, import-isolation, and Sphinx checks pass.",
    "Maintained strict evidence audit fails for all ten new P1 test modules.",
    "P1 result is FAIL pending material evidence/schema corrections and re-review."
  ],
  "residualRisks": [
    "No Rust/cross-language, persistence, SNAKES, concrete workflow, numerical-verification, scientific-validation, or UQ evidence exists.",
    "Most public objects and enum/error states lack exhaustive direct public-contract evidence.",
    "Relational invalid fixtures are not executed through their claimed public ActionObject owners."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only independent review; only the required review artifact was written. No production, test, schema, fixture, or documentation source was edited.",
  "reviewFindings": [
    "high: python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnToken__contract.py:1 (and nine peer P1 modules) - strict evidence audit rejects missing software_verification module markers",
    "high: python/src/ksdft2effmass/workflows/cpn/validation.py:24,29 - two public CpnIssueCode members have no reachable public emission path",
    "high: specification/workflow-cpn/v1/cpn-contract.schema.json:1061-1125 - public validation issue/result contracts exported by Python are absent from language-neutral schema",
    "medium: python/tests/software_verification/ksdft2effmass/integration/test__CpnJsonFixtures.py:74-86 - relational invalid fixtures are only shown schema-valid, not rejected by their claimed ActionObjects",
    "medium: python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnStructuredErrorsAndImports.py:16-21 - complete public namespace claim checks only three of 49 exports",
    "medium: python/tests/software_verification/ksdft2effmass/workflows/cpn/test__DeclarativeExpressions.py:75-91 - evidence does not exercise positive bound fields or bound-token IDs",
    "medium: python/tests/software_verification/ksdft2effmass/workflows/cpn/test__RetryRecoveryIteration.py:56-207 - no repeated multi-cycle deterministic iteration case",
    "medium: docs/verification/cpn-contract.rst:7-13 - evidence-ID form conflicts with docs/verification/testing-and-evidence.rst:39-45"
  ],
  "manualNotes": "Review verdict is FAIL. No task acceptance was performed."
}
```
