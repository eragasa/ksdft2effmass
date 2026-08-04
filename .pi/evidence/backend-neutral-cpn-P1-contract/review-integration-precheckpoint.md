# P1 final pre-checkpoint evidence/integration re-review

## Verdict

**PASS for deterministic corrections.** No unresolved deterministic implementation, test, schema, fixture, documentation, Sphinx, marker, audit, import, dependency-direction, or scope finding remains in the reviewed P1 tree.

**BLOCKED on protected public-contract choices.** The only remaining material technical blockers are (1) REAL wire canonicalization and (2) fixed integer widths/overflow behavior. Human authority must select those cross-language/public serialization semantics. This review does not accept or close P1 and does not authorize a successor.

## Module-by-module evidence inventory

- **Control plane — PASS:** `.pi/tasks/backend-neutral-cpn-P1-contract.md:1-10,28-56,66-90,104-110` and `.pi/chains/backend-neutral-kohn-sham-qe.chain.json:4-16,23-35,45-49,77-81` consistently keep P1 active pending review/verification/human acceptance, keep P2-P11 blocked, and prohibit SNAKES adaptation, persistence, concrete workflow/external/scientific execution, and successor launch.
- **`tokens.py` — PASS subject to protected numeric choices:** immutable, slotted project-owned routing values expose payload references, authorization, provenance, parent-run/token lineage, retries, iterations, and scope-explicit outcomes without owning scientific payloads or persistence. Exact Python REAL admission and the unresolved wire choice are explicit at `python/src/ksdft2effmass/workflows/cpn/tokens.py:190-215,232-249`; portable integer width remains explicit at `:345-354,419-449`.
- **`markings.py` — PASS subject to protected integer choice:** tuple-backed complete markings preserve token multiplicity and canonical order rather than Boolean completion; revision width is explicitly unresolved at `python/src/ksdft2effmass/workflows/cpn/markings.py:75-107,124-140`.
- **`expressions.py` — PASS:** closed tagged values/guards/inscriptions use no callable, lambda, source-text evaluation, I/O, or scientific tolerance. Guards are pure and exact; retry and join semantics inspect immutable bound-token state.
- **`model.py` — PASS:** the executable neutral model owns places, transitions, arcs, colors, guards, inscriptions, and initial marking. No scientific-workflow DAG claim, engine object, persistence object, or dangling generic helper was found.
- **`validation.py` — PASS:** definition and marking ActionObjects own cross-object validation and return immutable structured issues. Validation remains distinct from firing and from acceptance/scientific-validation policy.
- **`execution.py` — PASS:** enablement performs deterministic multiset binding and pure guard evaluation; firing performs in-memory read/consume/output state transition, terminal-history retention, collision checks, and revision advance. It is not external execution and correctly does not implement the later two-phase external request/result adapter. Wrong-type validation occurs before dereference at `python/src/ksdft2effmass/workflows/cpn/execution.py:505-533`.
- **`errors.py` — PASS:** operational failures retain structured immutable codes/details; no unreachable obsolete issue member or dangling error helper was found.
- **Public API and topology — PASS:** `python/src/ksdft2effmass/workflows/cpn/__init__.py:1-84` exposes the sorted 49-name neutral API. Static import topology is maintained by `python/tests/software_verification/ksdft2effmass/integration/test__CpnDependencyDirection.py:28-54`; this is static acyclicity evidence, not a scientific-workflow DAG claim. SNAKES/deferred-module isolation is maintained by `test__CpnSnakesIsolation.py:19-45`.
- **Schemas and fixtures — PASS subject to protected numeric choices:** seven Draft 2020-12 schemas and valid/invalid fixtures cover contract, net, marking, firing, results, validation, errors, structural rejection, and public relational ActionObject rejection. `specification/workflow-cpn/v1/README.md:1-29` accurately separates schema and runtime relational ownership. Its corrected limitation wording at `:31-40` now says REAL canonicalization and integer width/overflow are unresolved protected choices, without the former “accepted ... unresolved” contradiction.
- **Test evidence — PASS:** AST/manual review found exactly 34 unique identifiers `SV-CPN-001` through `SV-CPN-034`, with the exact `pytest.mark.software_verification` marker in all ten owning modules. Every test docstring now states a case-specific requirement, public path/method, selected oracle, concrete acceptance criterion, failure interpretation, and limitation; no duplicate docstrings or generic boilerplate remain. Representative corrected evidence is at `test__DeclarativeExpressions.py:37-230`, `test__TransitionExecution.py:32-394`, `test__RetryRecoveryIteration.py:159-424`, and `test__CpnJsonSchemas.py:42-176`.
- **SV-CPN-020 — PASS:** `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__RetryRecoveryIteration.py:159-194` explicitly owns deterministic two-cycle iteration. The executable case at `:289-335` runs the same two authorized cycles twice, proves equal final markings, revision 2, attempt `attempt-2`, retry parent `attempt-1`, and iteration index 2.
- **SV-CPN-034 — PASS:** `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__TransitionExecution.py:344-394` injects only wrong public argument types (no invariant bypass or monkeypatch), checks net/marking/request separately and together, and requires first-invalid-argument `TypeError`. This matches the implementation at `execution.py:526-533`.
- **VVUQ boundaries — PASS:** all evidence is correctly classified as software verification/contract conformance. `docs/verification/cpn-contract.rst:5-22,35-43` accurately records the 34 identifiers, case-specific evidence fields, gates, and explicit exclusion of numerical verification, scientific validation, and UQ.
- **Documentation/MyST/dependencies — PASS:** Markdown-first user-guide navigation and the implemented-but-unaccepted P1 status are accurate at `docs/user-guide/index.md:20-24` and `docs/user-guide/installation.md:9-19`. MyST is configured in `docs/conf.py:6-27`; Sphinx collected 33 sources including all 13 user-guide pages. The optional SNAKES boundary and dependency facts are explicit at `docs/user-guide/external-dependencies.md:78-99,162-182`; `cpnpy` and SimPN remain comparative non-dependencies at `docs/user-guide/colored-petri-nets.md:64-68` and `external-dependencies.md:122-156`.
- **Scope/ownership — PASS:** scans found no production SNAKES/cpnpy/SimPN import, adapter/engine directory, persistence repository, pickle, subprocess/scheduler, QE/ABINIT/Wannier integration, concrete scientific payload/workflow, or external execution. No tracked/staged generated HTML/doctree output was found. Generic CPN synchronization and lineage can represent common-parent joins and accepted scoped gate evidence; P1 correctly does not assert a concrete scientific common-parent workflow or implement an accepted-marking gate policy belonging to later tasks.
- **Source documentation — PASS:** all eight production modules have module docstrings and every class/function/private method has a docstring. Public/private ownership, local canonical ordering, multiset choices, binding indexes, output order, successor construction, and exclusions are documented; no cross-object private-method call or obsolete module was found.

## Protected blockers

1. **BLOCKER / HUMAN-OWNED — REAL wire canonicalization.** Python accepts only exact built-in `float` for `ContractValueKind.REAL` (`python/src/ksdft2effmass/workflows/cpn/tokens.py:205-210,232-249`), whereas JSON Schema `number` accepts integer-valued JSON numbers (`specification/workflow-cpn/v1/cpn-contract.schema.json:97-109`). The diagnostic probe confirmed schema acceptance of `{"kind":"real","value":1}` while Python raises `TypeError`. Choosing canonical decode/serialization semantics changes the public cross-language contract.
2. **BLOCKER / HUMAN-OWNED — fixed integer width and overflow taxonomy.** Python and schemas currently accept unbounded integer values for tagged integers, iteration/revision/schema fields (`tokens.py:205-210,419-449`; `markings.py:75-84,124-135`; `cpn-contract.schema.json:80-93,497-529,1052-1055`). The probe accepted both `2**200` and `-(2**200)` where field sign permits. Selecting Rust widths and overflow errors changes public typing/serialization compatibility.

No other material integration blocker was found. Human final acceptance remains a required later authority gate after protected choices and parent verification; it is not granted by this review.

## Validation evidence

- `cd python && uv run pytest -q` — **PASS**, 958 tests.
- `cd python && uv run ruff check . && uv run ruff format --check . && uv run mypy src` — **PASS**, lint clean, 90 files formatted, no type errors in 18 source files.
- `cd docs && ../python/.venv/bin/sphinx-build -W -b html . /tmp/ksdft2effmass-p1-precheckpoint-sphinx` — **PASS**, 33 sources; MyST 5.1.0; no warnings.
- `cd python && uv run python ../.pi/skills/audit_evidence_identifiers.py --strict` — process exit **FAIL** only because of 22 already cataloged non-P1 operator-difference owner warnings; maintained/P1 evidence reports `audit_errors=0`, 69 evidence modules, 366 tests, and 349 owned identifiers. Standing policy assigns those warnings to a separate migration, so they are not a P1 finding.
- AST test-documentation audit — **PASS**, 34 tests, 34 unique IDs, complete contiguous range, all ten exact markers, all required evidence sections, no duplicate docstrings.
- Source-docstring audit — **PASS**, eight module docstrings and no undocumented class/function/private method.
- REAL/integer diagnostic probe — **PASS as diagnostic evidence**, reproducing the two disclosed protected choices.
- `git diff --check`, staged-file check, prohibited-import/deferred-path/generated-output scans — **PASS**; no staged files, whitespace errors, prohibited P1 implementation/import, or generated documentation output in reviewed project paths.

## Residual risks

- Protected REAL canonicalization and integer width/overflow semantics prevent attested Python/schema/Rust agreement until human resolution.
- Parent verification must bound the intended P1 changes in the broadly dirty shared worktree.
- Passing gates establish neither Rust conformance nor SNAKES-adapter, authoritative-persistence, external-execution, numerical-verification, scientific-validation, UQ, or scientific-workflow evidence.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "The report provides a module-by-module inventory, exact file/line evidence for deterministic PASS areas, and two separately identified human-owned blockers with reproduced diagnostics and residual risks."
    }
  ],
  "changedFiles": [
    ".pi-subagents/artifacts/outputs/c3a35ff8/.pi/evidence/backend-neutral-cpn-P1-contract/review-integration-precheckpoint.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "cd python && uv run pytest -q",
      "result": "passed",
      "summary": "958 tests passed."
    },
    {
      "command": "cd python && uv run ruff check . && uv run ruff format --check . && uv run mypy src",
      "result": "passed",
      "summary": "Ruff lint/format passed; mypy found no issues in 18 source files."
    },
    {
      "command": "cd docs && ../python/.venv/bin/sphinx-build -W -b html . /tmp/ksdft2effmass-p1-precheckpoint-sphinx",
      "result": "passed",
      "summary": "33 sources built with MyST 5.1.0 and warnings treated as errors."
    },
    {
      "command": "cd python && uv run python ../.pi/skills/audit_evidence_identifiers.py --strict",
      "result": "failed",
      "summary": "Exit 1 solely for 22 separately cataloged non-P1 operator warnings; audit_errors=0 and P1 IDs/markers are clean."
    },
    {
      "command": "AST audits of 34 P1 test docstrings/markers/IDs and eight production-module docstrings",
      "result": "passed",
      "summary": "34 unique contiguous IDs, case-specific evidence sections, all ten markers, no duplicate test docstrings, and no undocumented production class/function/private method."
    },
    {
      "command": "Local JSON Schema/runtime REAL and large-integer diagnostic probe",
      "result": "passed",
      "summary": "Reproduced only the disclosed REAL integer-valued-number mismatch and unbounded integer behavior."
    },
    {
      "command": "git diff --check; staged, forbidden-import, deferred-path, and generated-output scans",
      "result": "passed",
      "summary": "No staged files, whitespace errors, prohibited P1 implementation/import, or generated HTML/doctree output in reviewed paths."
    }
  ],
  "validationOutput": [
    "Deterministic correction verdict: PASS.",
    "All 34 P1 test docstrings are case-specific; SV-CPN-020 owns and executes deterministic two-cycle iteration; SV-CPN-034 verifies early wrong-type firing rejection.",
    "Only protected REAL canonicalization and integer width/overflow choices remain material technical blockers.",
    "P1 remains active and unaccepted; P2-P11 and production/scientific execution remain blocked."
  ],
  "residualRisks": [
    "Human-owned REAL wire canonicalization remains unresolved.",
    "Human-owned fixed integer widths and overflow taxonomy remain unresolved.",
    "No Rust, SNAKES-adapter, persistence, external-execution, numerical-verification, scientific-validation, or UQ evidence is established.",
    "The shared worktree is broadly dirty and requires parent diff bounding."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only integration review; only the required review artifact was written, with no production, test, schema, fixture, or documentation edits.",
  "reviewFindings": [
    "no deterministic blockers: all reviewed P1 corrections and validation gates pass",
    "blocker/human-owned: python/src/ksdft2effmass/workflows/cpn/tokens.py:205-249 versus specification/workflow-cpn/v1/cpn-contract.schema.json:97-109 - integer-valued JSON number handling for tagged REAL lacks selected canonical wire semantics",
    "blocker/human-owned: python/src/ksdft2effmass/workflows/cpn/tokens.py:419-449, python/src/ksdft2effmass/workflows/cpn/markings.py:75-135, and specification/workflow-cpn/v1/cpn-contract.schema.json:80-93,497-529,1052-1055 - fixed integer widths and overflow behavior remain unspecified"
  ],
  "manualNotes": "PASS for deterministic corrections, BLOCKED only on the two protected public-contract decisions. No acceptance, closure, checkpoint creation, source edit, or successor launch was performed."
}
```
