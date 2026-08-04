# P1 correction integration re-review

## Result: FAIL

The corrected combined tree resolves the initial user-guide status, executable marker, source-docstring, and duplicate-output-ID findings. However, the initial finding about per-test evidence documentation is not resolved: all 33 P1 test docstrings use the same non-specific method/oracle/acceptance boilerplate rather than documenting the actual public method, case-specific oracle, and acceptance condition. The protected REAL wire-canonicalization and integer width/overflow decisions also remain blocked. Therefore protected choices are **not** the sole remaining blockers.

This review is read-only with respect to project source. It does not accept or close P1 and does not authorize or launch a successor.

## Module-by-module evidence inventory

- **Control plane — PASS:** `.pi/tasks/backend-neutral-cpn-P1-contract.md:1-5,56-77` and `.pi/chains/backend-neutral-kohn-sham-qe.chain.json:4-6,15-16,23-35` consistently keep P1 active/pending review and human acceptance, P2-P11 blocked, and production/scientific execution unauthorized.
- **User guide/MyST/dependency catalog — PASS:** `docs/user-guide/index.md:20-24`, `installation.md:9-19`, and `external-dependencies.md:78-99` now identify the implemented-but-unaccepted P1 neutral contract and distinguish the deferred SNAKES adapter, persistence, concrete workflows, and execution. MyST 5.1.0 loaded and Sphinx collected the 13 Markdown user-guide pages. `docs/user-guide/colored-petri-nets.md:66-68` retains cpnpy/SimPN as comparative non-dependencies.
- **`tokens.py` — PASS subject to protected wire choices:** immutable, slotted routing/outcome objects; exact built-in scalar typing; Boolean rejection; finite Python REAL values; explicit lineage, authorization, provenance, iteration, and scoped terminality. Public and private source documentation is materially complete. `tokens.py:209-211,353-354` correctly exposes unresolved REAL/integer portability limits.
- **`markings.py` — PASS subject to integer choice:** complete tuple-backed multiset markings preserve independently identified tokens and deterministic order; markings are not Boolean completion. Field and private constructor documentation is present. `markings.py:83-84` discloses unresolved portable integer width.
- **`expressions.py` — PASS:** closed enum/tagged declarative expressions, pure evaluation, no callable/lambda/eval/I/O surface, documented public/private methods, and meaningful binding/field state. Exact like-tag comparison owns no scientific tolerance or unit conversion.
- **`model.py` — PASS subject to integer choice:** immutable net definition covers places, transitions, arcs, colors, guards, inscriptions, and initial marking. Cross-object validation is routed outward. Every public field and both module-private mechanical functions are documented; no dangling helper or obsolete module was found.
- **`validation.py` — PASS:** stateless ActionObjects own cross-object definition/marking validation and return structured immutable issues. Local comments explain complete-place, global-token-identity, and transition-local binding state. No cross-object private calls were found.
- **`execution.py` — PASS:** deterministic binding enumeration, multiple-input synchronization, read/consume semantics, output production, revision advance, retained terminal history, recovery, retry, and repeated iteration are executable. Guards remain pure; no external operation is executed. Firing is an in-memory contract action, not a scientific workflow DAG or two-phase external executor. Public/private methods and meaningful local state are documented.
- **`errors.py` — PASS:** reachable structured errors retain immutable authoritative codes/details. Public exceptions, enum members, constructor, and `detail` attribute are documented.
- **Public imports/dependency direction/SNAKES isolation — PASS:** `ksdft2effmass.workflows.cpn` imports 49 public names without SNAKES. Maintained topology evidence remains in `python/tests/software_verification/ksdft2effmass/integration/test__CpnDependencyDirection.py:1-45`; isolation remains in `test__CpnSnakesIsolation.py:1-45`. Production imports follow `tokens/errors -> markings -> expressions -> model -> validation -> execution`. Static import acyclicity is correctly distinct from stateful CPN semantics; no scientific-workflow DAG claim was found.
- **Schemas/fixtures/runtime — PASS except protected numeric choices:** duplicate `FiringRequest.output_token_ids` are now intrinsic constructor/schema errors (`execution.py:104-164`; `cpn-contract.schema.json:1013-1030`), while collision against a current marking remains structured firing policy (`execution.py:608-629`). Tests at `test__TransitionExecution.py:167-217,293-304` and `test__CpnJsonSchemas.py:123-176` synchronize the boundary. Versioned schemas/fixtures cover net, marking, firing, results, validation, and errors without implementing serialization/persistence.
- **VVUQ classification/markers — PARTIAL:** all ten P1 modules now carry `pytest.mark.software_verification`; all 33 stable IDs are unique and the audit reports `audit_errors=0`. Evidence remains software verification/contract conformance, not numerical verification, scientific validation, or UQ. Detailed per-test evidence documentation still fails the maintained standard (finding 1).
- **Sphinx/concept/API/verification consistency — PARTIAL:** Sphinx `-W` succeeds and source/API/concept behavior agrees on output-ID uniqueness and exclusions. `docs/verification/cpn-contract.rst:15-22` overstates the per-test documentation quality (finding 1). The schema README contains one contradictory protected-choice phrase (finding 3).
- **Scope/exclusions/generated output — PASS:** scans found no production SNAKES import, adapter, repository/persistence/pickle, subprocess/scheduler, QE/ABINIT/Wannier integration, scientific payload, or external execution. No generated output is tracked or staged. Existing ignored `graphify-out/` is outside P1 and was not generated by this review; Sphinx output went only to `/tmp`.

## Findings

1. **HIGH — the 33 P1 test docstrings remain generic, non-case-specific evidence records, contrary to the maintained VVUQ documentation standard.**
   - Representative examples are `python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnToken__contract.py:27-51,72-96,104-128` and `python/tests/software_verification/ksdft2effmass/integration/test__CpnJsonSchemas.py:42-68`.
   - Every test repeats the same method text (“constructor, ResultObject, schema, or ActionObject path”), the same disjunctive oracle list, and “Every assertion must pass.” It does not name the actual public method/constructor exercised, identify the case-specific independent oracle, or state the concrete acceptance criterion. For example, `SV-CPN-003` does not document `CpnToken` construction plus expected `TypeError` for `iteration_index=True`; that information exists only in code.
   - The repeated “Requirement: Verify <test title>” restates the test rather than connecting it to a separately stated contract requirement. Identical boilerplate occurs 33 times across all ten P1 modules.
   - This contradicts `docs/verification/cpn-contract.rst:15-22`, which claims each docstring records its public method, oracle, and acceptance, and does not satisfy `AGENTS.md`'s non-tautological per-evidence requirement. This is deterministic documentation correction, not a protected scientific/API choice.

2. **BLOCKER / HUMAN-OWNED — REAL wire canonicalization and fixed integer width/overflow remain unresolved public cross-language contract choices.**
   - Python requires exact built-in `float` for `ContractValueKind.REAL` (`python/src/ksdft2effmass/workflows/cpn/tokens.py:205-246`), while JSON Schema admits an integer-valued JSON number for tagged `real` (`specification/workflow-cpn/v1/cpn-contract.schema.json:97-109`). A direct probe showed schema acceptance of `{"kind":"real","value":1}` and Python `TypeError`.
   - Python and schemas currently admit unbounded integers (`tokens.py:205-210,419-449`; `markings.py:83-84,125-136`; schema `:89-93,497-500,521-529,1052-1055`), but the intended fixed Rust width and overflow taxonomy are not selected.
   - The limitation is truthfully disclosed in `docs/api/workflows-cpn.md:14-18`, `docs/verification/cpn-contract.rst:33-43`, and `specification/workflow-cpn/v1/README.md:35-40`. Choosing these semantics affects the public wire contract and Rust mapping and remains human-owned.

3. **LOW — the schema README uses self-contradictory protected-choice wording.**
   - `specification/workflow-cpn/v1/README.md:38-40` says “The accepted `real` wire-value canonicalization ... remain unresolved.” No canonicalization is accepted. The surrounding source and docs correctly call it protected and unresolved. This is a nonblocking wording defect but should not remain in acceptance evidence.

## Validation evidence

- `cd python && uv run pytest -q` — **PASS**, 957 tests.
- `cd python && uv run ruff check . && uv run ruff format --check . && uv run mypy src` — **PASS**, lint clean, 90 files formatted, no type issues in 18 source files.
- `cd docs && ../python/.venv/bin/sphinx-build -W -b html . /tmp/ksdft2effmass-p1-correction-sphinx` — **PASS**, 33 sources; MyST 5.1.0; no warnings.
- `python .pi/skills/audit_evidence_identifiers.py --strict` — process **FAIL** because 22 already cataloged non-P1 operator warnings remain; P1 itself is clean (`audit_errors=0`, 33 owned P1 IDs, all ten P1 markers present). Those 22 warnings are separately deferred by standing repository policy and are not a P1 finding.
- Public numeric/schema and duplicate-output-ID probes — **PASS as diagnostic evidence**: duplicate-ID runtime/schema agreement confirmed; unresolved REAL mismatch reproduced.
- `git diff --check`, staged-file scan, forbidden-import scan — **PASS**; no staged files and no prohibited P1 implementation/import found.

## Residual risks and parent-owned follow-up

- Correct the case-specific evidence documentation and synchronize `docs/verification/cpn-contract.rst`; this is not human-protected policy.
- Human authority must select REAL wire canonicalization and fixed integer width/overflow semantics before attested cross-language contract agreement can be claimed.
- Parent verification must review the intended combined-tree diff in the broadly dirty shared worktree.
- Passing gates do not establish Rust conformance, SNAKES-adapter behavior, persistence, external execution, numerical verification, scientific validation, or UQ. P2-P11 and production/scientific execution remain blocked.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Three concrete findings include severity and exact file/line evidence; residual risks and validated corrected areas are inventoried module by module."
    }
  ],
  "changedFiles": [
    "/Users/eugene/repos/ksdft2effmass/.pi-subagents/artifacts/outputs/e6505e86/.pi/evidence/backend-neutral-cpn-P1-contract/review-integration-correction.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "cd python && uv run pytest -q",
      "result": "passed",
      "summary": "957 tests passed"
    },
    {
      "command": "cd python && uv run ruff check . && uv run ruff format --check . && uv run mypy src",
      "result": "passed",
      "summary": "Lint and format checks passed; mypy found no issues in 18 source files"
    },
    {
      "command": "cd docs && ../python/.venv/bin/sphinx-build -W -b html . /tmp/ksdft2effmass-p1-correction-sphinx",
      "result": "passed",
      "summary": "Sphinx built 33 sources with MyST 5.1.0 and warnings treated as errors"
    },
    {
      "command": "python .pi/skills/audit_evidence_identifiers.py --strict",
      "result": "failed",
      "summary": "P1 audit_errors=0 and all markers/IDs are owned; process exits 1 for 22 separately cataloged non-P1 operator warnings"
    },
    {
      "command": "public schema/runtime numeric and duplicate-output-ID probes",
      "result": "passed",
      "summary": "Duplicate IDs agree as intrinsic ValueError/schema rejection; protected tagged-REAL integer mismatch reproduced"
    },
    {
      "command": "git diff --check; staged/generated/forbidden-import scans",
      "result": "passed",
      "summary": "No whitespace errors, staged files, tracked generated output, or prohibited P1 implementation/import"
    }
  ],
  "validationOutput": [
    "FAIL: per-test evidence documentation remains materially non-specific across all 33 P1 tests",
    "Initial user-guide, source-docstring, marker, and duplicate-output-ID findings are otherwise corrected",
    "Protected REAL/integer choices remain blocked but are not the sole blockers",
    "P1 remains active; P2-P11 and production/scientific execution remain blocked"
  ],
  "residualRisks": [
    "Human-owned REAL wire canonicalization and integer width/overflow choices block public cross-language agreement.",
    "Per-test evidence documentation and its Sphinx status claim require deterministic correction.",
    "No Rust, SNAKES-adapter, persistence, external-execution, numerical-verification, scientific-validation, or UQ evidence was established.",
    "The shared worktree is broadly dirty; parent verification must bound the intended P1 diff."
  ],
  "noStagedFiles": true,
  "diffSummary": "Review report artifact written; no project source, test, schema, fixture, or documentation files changed by the reviewer.",
  "reviewFindings": [
    "high: python/tests/software_verification/ksdft2effmass/workflows/cpn/test__CpnToken__contract.py:27-51 and all 33 P1 tests - generic boilerplate does not record the case-specific public method, oracle, or concrete acceptance criterion",
    "blocker/human-owned: python/src/ksdft2effmass/workflows/cpn/tokens.py:205-246 versus specification/workflow-cpn/v1/cpn-contract.schema.json:97-109 - tagged REAL integer-valued JSON semantics and fixed integer width/overflow remain unresolved",
    "low: specification/workflow-cpn/v1/README.md:38-40 - calls REAL canonicalization accepted and unresolved in the same sentence"
  ],
  "manualNotes": "Overall correction re-review is FAIL. Protected REAL/integer choices are not the sole remaining blockers because deterministic evidence-documentation correction remains. No acceptance, closure, edit to project source, or successor launch was performed."
}
```
