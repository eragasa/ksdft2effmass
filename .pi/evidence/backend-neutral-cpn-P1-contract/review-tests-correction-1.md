# P1 correction re-review — tests, schemas, fixtures, and VVUQ evidence

## Verdict: FAIL

The executable corrections resolve the eight concrete initial findings at the runtime/schema level, and all focused P1 checks pass. However, the newly expanded per-test documentation is generic boilerplate rather than non-tautological evidence documentation, and the new two-cycle iteration assertions are not described by their owning evidence requirement. These remain material evidence-gate failures. This review is read-only and does not accept or close P1.

## Findings

1. **HIGH — all 33 P1 test docstrings fail the maintained non-tautological per-test documentation standard.** In all ten P1 modules, the `Method`, `Oracle and acceptance`, and `Failure interpretation and limitations` sections are identical boilerplate. For example, `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__DeclarativeExpressions.py:38-64` says only to “exercise” an unspecified constructor/result/schema/ActionObject, lists a menu of possible oracles, and defines acceptance as “Every assertion must pass.” It does not state that this test constructs a string in place of `ValueExpressionKind`, constructs an incomplete token-field expression, or expects `TypeError` and `ValueError`. The same text is repeated for every test, including schema, AST, import, firing, and iteration cases, so it cannot identify the actual method, selected independent oracle, concrete acceptance criterion, or case-specific failure meaning. This conflicts with `docs/verification/testing-and-evidence.rst:48-57`, especially “Documentation must explain the evidence rather than repeat the function name,” and with the P1 test-owner instruction requiring non-tautological requirement/method/oracle/acceptance/interpretation/limitations documentation. Affected modules are:
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnToken__contract.py`
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__DeclarativeExpressions.py`
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnDefinitionAndMarking.py`
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__TransitionExecution.py`
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__RetryRecoveryIteration.py`
   - `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnStructuredErrorsAndImports.py`
   - `python/tests/software_verification/ksdft2effmass/integration/test__CpnJsonSchemas.py`
   - `python/tests/software_verification/ksdft2effmass/integration/test__CpnJsonFixtures.py`
   - `python/tests/software_verification/ksdft2effmass/integration/test__CpnDependencyDirection.py`
   - `python/tests/software_verification/ksdft2effmass/integration/test__CpnSnakesIsolation.py`

2. **MEDIUM — the added multi-cycle iteration assertions are executable but not documented by their owning stable evidence item.** `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__RetryRecoveryIteration.py:281-327` now executes two cycles twice and checks deterministic equality, revision 2, attempt lineage, and iteration index 2. But its owning `SV-CPN-020` docstring at `:162-188` states only the one-step requirement “retry-style read emits a new attempt without erasing failure”; it never identifies the two-cycle method or its exact successor-marking oracle. Consequently the requested multi-cycle behavior exists as an assertion but is not auditable from the stable evidence documentation. This is also a concrete instance of finding 1.

## Initial finding disposition

1. **Markers:** resolved for P1. All ten modules contain exact `pytestmark = pytest.mark.software_verification`; the strict audit reports `audit_errors=0` for maintained identifiers/markers.
2. **Unreachable validation issue members:** resolved. `WRONG_ARC_INSCRIPTION` and `EXPRESSION_TYPE_MISMATCH` were removed from `CpnIssueCode`; the remaining validation issue set is represented in source and schema. Operational `CpnErrorCode.EXPRESSION_TYPE_MISMATCH` remains reachable through firing/enablement translation in `python/src/ksdft2effmass/workflows/cpn/execution.py:384`.
3. **Missing exported result schemas:** resolved. `cpn-contract.schema.json` now includes `validationIssueCode`, `validationIssue`, `validationResult`, `guardEvaluationResult`, and `transitionEnablementResult`; `cpn-validation.schema.json` and `cpn-results.schema.json` provide narrow entry points. Tests compare both issue/error enums with schema enums.
4. **Relational fixtures:** resolved for the five initially named fixtures. `test__CpnJsonFixtures.py:327-423` validates their structural classification and invokes `CpnDefinitionValidator`, `CpnMarkingValidator`, or `TransitionFirer` for exact public issue/error codes.
5. **Complete export check:** resolved. `test__CpnStructuredErrorsAndImports.py:19-50` checks sorted unique `__all__`, exact count 49, and resolves every exported name.
6. **Bound token fields/IDs:** resolved. `test__DeclarativeExpressions.py:177-239` checks `RUN_ID`, ordered duplicate `BOUND_TOKEN_IDS`, invalid empty sequence entries, and an unbound variable.
7. **Repeated iteration execution:** executable behavior resolved at `test__RetryRecoveryIteration.py:281-327`, subject to finding 2 about evidence ownership/documentation.
8. **Evidence identifier shape:** resolved. The suite owns exactly 33 unique `SV-CPN-001` through `SV-CPN-033` identifiers, matching `docs/verification/testing-and-evidence.rst:31-43` and `docs/verification/cpn-contract.rst:8-14`.

## Validation results

- Focused P1 pytest: **passed**, 36 tests.
- Ruff and mypy: **passed**.
- Public import introspection: **passed**, all 49 exports resolved.
- JSON Schema metaschema check: **passed**, seven schemas.
- Sphinx warnings-as-errors: **passed**.
- Strict maintained evidence audit: command exits **failed** because it intentionally treats 22 pre-existing operator-difference tests without evidence owners as warnings/nonzero; importantly it reports `audit_errors=0`, 69 evidence modules, 365 test functions, and 348 owned identifiers. The repository policy already records those 22 tests as a separate bounded migration, so they are not a new P1 finding.

## Residual risks and exclusions

- The two protected wire choices named in the task remain unresolved: real-number canonicalization and fixed integer width/overflow behavior. They remain human-authority blockers and are not resolved by these tests.
- Passing P1 checks does not establish Rust conformance, authoritative persistence, SNAKES adaptation, concrete workflow/scientific execution, numerical verification, scientific validation, or uncertainty quantification.
- This review did not attempt exhaustive direct invariant/value-semantics tests for every one of the 49 exports; it re-reviewed the corrected surfaces against the initial findings and P1 gates.
- The worktree contains extensive pre-existing unstaged/untracked changes. `git diff --cached --quiet` confirms no staged files; this reviewer edited no production, test, schema, fixture, or documentation source.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Two severity-ranked residual findings cite exact test and documentation paths/line ranges; all eight initial findings have explicit correction dispositions and residual risks are listed."
    }
  ],
  "changedFiles": [
    ".pi-subagents/artifacts/outputs/e6505e86/.pi/evidence/backend-neutral-cpn-P1-contract/review-tests-correction.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "cd python && uv run python ../.pi/skills/audit_evidence_identifiers.py --strict",
      "result": "failed",
      "summary": "Nonzero from 22 known unrelated operator-difference owner warnings; P1/maintained audit_errors=0, 348 owned identifiers."
    },
    {
      "command": "cd python && uv run pytest -q tests/software_verification/ksdft2effmass/workflows/cpn tests/software_verification/ksdft2effmass/integration/test__CpnJsonSchemas.py tests/software_verification/ksdft2effmass/integration/test__CpnJsonFixtures.py tests/software_verification/ksdft2effmass/integration/test__CpnDependencyDirection.py tests/software_verification/ksdft2effmass/integration/test__CpnSnakesIsolation.py",
      "result": "passed",
      "summary": "36 passed in 0.11s."
    },
    {
      "command": "cd python && uv run ruff check <focused P1 source/tests> && uv run mypy src/ksdft2effmass/workflows",
      "result": "passed",
      "summary": "Ruff all checks passed; mypy found no issues in 9 source files."
    },
    {
      "command": "cd python && uv run python <49-name public __all__ introspection smoke check>",
      "result": "passed",
      "summary": "All 49 unique sorted exports resolved to the expected public object name."
    },
    {
      "command": "cd python && uv run python <local draft-2020-12 metaschema/registry check>",
      "result": "passed",
      "summary": "All 7 schemas are metaschema-valid and locally registrable."
    },
    {
      "command": "cd python && uv run sphinx-build -W -b html ../docs /tmp/ksdft2effmass-cpn-review-html",
      "result": "passed",
      "summary": "Sphinx build succeeded with warnings treated as errors."
    },
    {
      "command": "AST structural audit of the ten P1 modules",
      "result": "passed",
      "summary": "33 tests, 33 unique first-line SV-CPN identifiers, and all required section headings present; manual semantic review found the headings contain generic boilerplate."
    }
  ],
  "validationOutput": [
    "Executable runtime, schema, fixture, export, lint, type, and documentation-build checks pass.",
    "All eight initial findings are corrected at the structural/executable level.",
    "Final re-review verdict is FAIL because per-test evidence prose remains non-tautological and the multi-cycle assertions lack an accurate owning requirement/oracle."
  ],
  "residualRisks": [
    "Protected real-number canonicalization and integer width/overflow choices remain unresolved human-authority blockers.",
    "No Rust, persistence, SNAKES, concrete workflow, scientific execution, numerical-verification, scientific-validation, or UQ evidence is established.",
    "Strict audit remains globally nonzero because of 22 documented unrelated operator-difference tests awaiting a separate evidence-ID migration."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only correction review; only the required review artifact was written. No source, test, schema, fixture, or documentation files were edited.",
  "reviewFindings": [
    "high: python/tests/software_verification/ksdft2effmass/workflows/cpn/test__DeclarativeExpressions.py:38-64 and all 33 P1 test docstrings across ten modules - identical generic method/oracle/acceptance prose does not explain each test's actual evidence and violates the maintained non-tautological documentation requirement",
    "medium: python/tests/software_verification/ksdft2effmass/workflows/cpn/test__RetryRecoveryIteration.py:162-188,281-327 - two-cycle deterministic iteration is asserted but omitted from the owning SV-CPN-020 requirement, method, and oracle"
  ],
  "manualNotes": "Verdict is FAIL. No P1 acceptance or closeout was performed."
}
```
