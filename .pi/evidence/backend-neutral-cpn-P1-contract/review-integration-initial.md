# P1 independent integration/documentation/scope review

## Result: FAIL

Material documentation, VVUQ-classification, source-documentation, and schema/runtime synchronization findings remain. This review does **not** accept or close P1 and did not launch a successor.

## Evidence inventory

- **Control plane:** `.pi/tasks/backend-neutral-cpn-P1-contract.md` says implementation complete but review/verification/human acceptance pending. `.pi/chains/backend-neutral-kohn-sham-qe.chain.json:4-6,23-35` correctly keeps P1 active, P2-P11 blocked, and production execution unauthorized (`:16`).
- **Production package/public imports:** `python/src/ksdft2effmass/workflows/cpn/` contains concrete immutable contract objects and stateless validation/expression/enablement/firing ActionObjects. `ksdft2effmass.workflows.cpn` imports 49 public names successfully. The parent `workflows` package intentionally does not flatten them.
- **Architecture/scope:** module imports follow the tested neutral layers `tokens/errors -> markings -> expressions -> model -> validation -> execution`; scans found no SNAKES, subprocess, pickle, QE, Wannier, provenance-subsystem, persistence-repository, engine-adapter, or external-execution production import. The implementation models stateful multiset CPN behavior rather than claiming a scientific-workflow DAG. It represents pure guards, read/consume firing, synchronization, retries/recovery/iterations, lineage/correlation/authorization references, and scoped accepted/rejected/failed/blocked outcomes. External execution and authoritative persistence remain absent as required.
- **Schemas/fixtures/tests:** version-1 schemas and synthetic valid/invalid fixtures exist. The full suite passed (957 tests), as did public import, Ruff, formatting, mypy, and schema tests. Stable P1 IDs `CPN-SV-P1-001` through `-033` are present, but their executable evidence-class markings and detailed per-test documentation are incomplete (findings below).
- **Sphinx/navigation:** MyST is configured in `docs/conf.py:8,20-27`; P1 concept/API/verification pages are collected in `docs/index.rst:7-28`; the Markdown-first user guide is collected explicitly at `docs/index.rst:47-69`. Sphinx 9.1.0 with `-W` built 33 pages successfully to `/tmp/ksdft2effmass-p1-sphinx`. No `_build` output is tracked or staged. cpnpy and SimPN remain truthfully labelled comparative, non-dependencies in `docs/user-guide/colored-petri-nets.md:66-68`.
- **Ownership/Rust boundary:** production objects are frozen/slotted, fields are fixed, scalar checks reject Boolean-as-integer, collection ordering is deterministic, and schemas expose language-neutral names. No generic helper/obsolete production module was found. The package remains backend-neutral and Rust-translatable in structure.

## Findings

1. **HIGH — MyST-rendered user-guide status contradicts the active control plane and implemented P1 production contract.**
   - `docs/user-guide/index.md:22` says P0A is the only active task and P1 remains unauthorized.
   - `docs/user-guide/installation.md:13` says P1 and P2-P11 remain blocked and refers to the project-owned contract as future code.
   - `docs/user-guide/external-dependencies.md:80-81` says no project CPN runtime is implemented and calls it future.
   - These contradict `.pi/chains/backend-neutral-kohn-sham-qe.chain.json:4-6,23-26`, `.pi/tasks/backend-neutral-cpn-P1-contract.md` (implementation-complete status), the executable package, and the synchronized architecture status at `docs/architecture/colored-petri-net-workflows.md:367-380`. Sphinx succeeds because this is semantic staleness, not a syntax error. User-facing status/navigation therefore is not synchronized.

2. **HIGH — all ten new P1 test modules lack executable software-verification classification markers.**
   - Representative evidence: `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnToken__contract.py:11-22` imports pytest but defines no `pytestmark = pytest.mark.software_verification`; `python/tests/software_verification/ksdft2effmass/integration/test__CpnDependencyDirection.py:9-24` likewise has no classification marker.
   - `python .pi/skills/audit_evidence_identifiers.py --strict` reported exactly 10 P1 audit errors, covering all six `workflows/cpn/test__*.py` modules and all four `integration/test__Cpn*.py` modules. Directory placement and narrative claims do not replace maintained executable classification.
   - The same modules' individual test docstrings are generally one-line restatements (for example `test__TransitionExecution.py:91-113`) rather than recording method, oracle, acceptance, failure interpretation, and limitations per evidence item as required by `docs/verification/testing-and-evidence.rst:59-66`. Module docstrings provide some shared context, but not the required complete per-test evidence record. Thus `docs/verification/cpn-contract.rst:7-19` overstates the maintained evidence surface.

3. **HIGH — maintained public source documentation is incomplete under the repository's NumPy-style source standard.**
   - `python/src/ksdft2effmass/workflows/cpn/model.py:35-190` exposes `ColorDefinition`, `PlaceDefinition`, `TokenPattern`, both inscription types, `TransitionDefinition`, `ArcDefinition`, and `CpnNetDefinition`, but their docstrings omit individual NumPy `Parameters` field documentation (types, allowed values, canonicalization, relationships); `CpnNetDefinition` refers collectively to “Parameters” without documenting any field.
   - `python/src/ksdft2effmass/workflows/cpn/execution.py:42-99` similarly exposes three Result/DataObjects with undocumented public fields. Public ActionObject methods also omit complete `Parameters`/`Returns` documentation; for example `TransitionFirer.execute` at `execution.py:280-292` documents only selected raised-error behavior.
   - Comparable abbreviated public dataclass/enum documentation occurs in `markings.py`, `validation.py`, and `errors.py`. Sphinx autodoc renders these omissions without warning, so the passing build does not satisfy source-docstring completeness or source/Sphinx semantic completeness.

4. **MEDIUM — the Python `FiringRequest` and the language-neutral schema disagree about duplicate output-token identities.**
   - `python/src/ksdft2effmass/workflows/cpn/execution.py:61-86` accepts `FiringRequest(..., output_token_ids=("x", "x"))`; duplicate detection is deferred to `TransitionFirer` as structured `OUTPUT_ID_COLLISION` policy.
   - `specification/workflow-cpn/v1/cpn-contract.schema.json:1016-1018` references `$defs/ids`, whose `uniqueItems: true` is defined at `:27-33`, so the same request is structurally rejected before firing.
   - A direct probe confirmed Python construction succeeds while Draft 2020-12 validation rejects the equivalent JSON. Existing `CPN-SV-P1-018` at `test__TransitionExecution.py:91-113` checks count and collision with an existing marking ID, but not duplicate request IDs or cross-surface agreement. Choosing whether uniqueness is an intrinsic request invariant or a structured firing error affects the public API/schema contract and requires parent/human classification rather than reviewer repair.

## Passing checks and negative evidence

- Full pytest: 957 passed.
- Ruff lint and format check: passed.
- mypy over `python/src`: passed with no issues in 18 source files.
- Sphinx HTML build with `-W`: passed, 33 sources, temporary output only.
- Public import smoke: passed, 49 supported CPN names.
- Static dependency and excluded-import scans: passed; no SNAKES production import or later-task production dependency found.
- `git diff --check`: passed; no staged files. P1 files are currently untracked/modified in the shared worktree, and this reviewer made no repository-source changes.
- No scientific calculation, external tool, network access, generated graph, authoritative persistence operation, or SNAKES runtime execution was performed.

## Residual risks

- Passing unit/schema tests do not establish cross-language Rust conformance, SNAKES-adapter behavior, persistence behavior, scientific validation, numerical verification, or uncertainty quantification; these remain correctly excluded.
- The broad shared worktree contains many unrelated modified/untracked files. Review conclusions are bounded to the inspected P1/control/docs surfaces; final parent verification must assess the intended combined-tree diff.
- Ignored `__pycache__` files exist from test execution, but no generated build output is staged/tracked and Sphinx output was directed to `/tmp`.
- Human authority remains required for the schema/runtime uniqueness boundary and final acceptance. P2-P11 and all production/scientific execution remain blocked.

## Commands run

- `cd python && uv run python ...` public-import smoke — passed (49 exports).
- `cd python && uv run pytest -q` — passed (957 tests).
- `cd python && uv run ruff check . && uv run ruff format --check .` — passed.
- `cd python && uv run mypy src` — passed (18 source files).
- `cd docs && ../python/.venv/bin/sphinx-build -W -b html . /tmp/ksdft2effmass-p1-sphinx` — passed.
- `python .pi/skills/audit_evidence_identifiers.py --strict` — failed: 10 P1 missing-marker errors plus 22 previously catalogued non-P1 unowned-test warnings.
- AST/import, forbidden-scope, generated-output, `git status`, `git diff --check`, and staged-file scans — passed for the reviewed assertions; no staged files.
- Direct Python/JSON-Schema duplicate-output-ID probe — demonstrated the mismatch described in finding 4.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Four concrete findings with severity and exact file:line evidence are reported, together with residual risks and command results."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "cd python && uv run pytest -q",
      "result": "passed",
      "summary": "957 tests passed"
    },
    {
      "command": "cd python && uv run ruff check . && uv run ruff format --check .",
      "result": "passed",
      "summary": "Lint passed; 90 files already formatted"
    },
    {
      "command": "cd python && uv run mypy src",
      "result": "passed",
      "summary": "No issues in 18 source files"
    },
    {
      "command": "cd docs && ../python/.venv/bin/sphinx-build -W -b html . /tmp/ksdft2effmass-p1-sphinx",
      "result": "passed",
      "summary": "Sphinx 9.1.0 built 33 pages with warnings treated as errors"
    },
    {
      "command": "python .pi/skills/audit_evidence_identifiers.py --strict",
      "result": "failed",
      "summary": "10 P1 modules lack required software_verification markers; 22 known non-P1 unowned-test warnings also reported"
    },
    {
      "command": "public import, schema/runtime duplicate-ID probe, dependency/forbidden-import/generated-output/git scans",
      "result": "passed",
      "summary": "Import and negative scans passed; probe reproducibly exposed schema/runtime mismatch"
    }
  ],
  "validationOutput": [
    "FAIL: material review findings remain despite deterministic gates passing",
    "P1 active; P2-P11 and production/scientific execution remain blocked",
    "No SNAKES production import, adapter, persistence implementation, or external execution found"
  ],
  "residualRisks": [
    "No Rust, SNAKES-adapter, persistence, numerical-verification, scientific-validation, or UQ evidence was established.",
    "Shared worktree contains broad unrelated changes; parent verification must review the intended combined-tree diff.",
    "Public API/schema uniqueness policy requires protected-decision classification before correction."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only review; no source/test/documentation edits. P1 source, schemas, fixtures, tests, and pages are untracked in the shared worktree while docs/conf.py and docs/index.rst are modified.",
  "reviewFindings": [
    "high: docs/user-guide/index.md:22, installation.md:13, external-dependencies.md:80-81 - stale status contradicts active/implemented P1",
    "high: python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnToken__contract.py:11-25 and integration/test__CpnDependencyDirection.py:9-24 - missing executable software-verification markers across all 10 P1 modules and incomplete per-test evidence documentation",
    "high: python/src/ksdft2effmass/workflows/cpn/model.py:35-190 and execution.py:42-99 - public fields lack required complete NumPy-style source documentation",
    "medium: specification/workflow-cpn/v1/cpn-contract.schema.json:27-33,1016-1018 versus python/src/ksdft2effmass/workflows/cpn/execution.py:61-86 - duplicate output IDs rejected by schema but accepted by FiringRequest"
  ],
  "manualNotes": "Overall independent review result is FAIL. No task acceptance, closure, edit, or successor launch was performed."
}
```
