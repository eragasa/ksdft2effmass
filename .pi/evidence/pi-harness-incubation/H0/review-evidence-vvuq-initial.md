# H0 evidence/VVUQ/skill-overlap review

**Verdict: FAIL**

The evidence/VVUQ recommendations are substantively sound, but the H0 completion validator has an out-of-scope nonmutation allowlist that makes its protected-path claim unsound.

## Review

- **Correct:** The accepted evidence grammar has a clear single source of truth. `.pi/skills/document-research-python/references/test-evidence-documentation.md:6-27` separates software verification, numerical verification, scientific validation, and UQ; `:30-86` owns exact headings and fields; `:111-183` owns class/artifact ownership and filename semantics; and `:206-232` explicitly separates structural checks from semantic review. `.pi/skills/develop-operator-records/SKILL.md:9-15` correctly imports that shared grammar and limits itself to operator-specific scientific/architectural constraints. The durable acceptance is confirmed by `.pi/tasks/class-owned-evidence-documentation-convention.md` and `.pi/checkpoints/EVIDENCE-DOC-1-HC03-final-acceptance.json`.

- **Correct:** The artifact-versus-boundary recommendation is coherent with accepted P1 evidence. `.pi/evidence/pi-harness-incubation/H0/open-finding-resolutions.md` §1 keeps `class_owned` and `artifact_owned` as generic primary kinds, models agreement/direction as artifact relation metadata, and preserves P1 `boundary_owned` only through local compatibility. That matches the accepted grammar and the executable P1 surface: `.pi/evidence/backend-neutral-cpn-P1-contract/test-ownership-manifest.json:1529-1618` contains one legacy `boundary_owned` entry but all ten integration tests retain `test_artifact__...`; `.pi/evidence/class-owned-evidence-convention/validate.py` enforces this structural compatibility. A genuine production Workflow remains class-owned, while a technical integration boundary is artifact-owned; no artificial Workflow owner is introduced.

- **Correct:** H0 properly treats `docs/harness/ksdft2effmass.harness.04.md` through `.06.md` as prospective/advisory rather than implemented authority. Their proposed independent `write-research-evidence-tests`, peer `boundary` surface, and `boundary_owned` vocabulary conflict with the accepted grammar, but `.pi/evidence/pi-harness-incubation/H0/duplication-and-overlap-analysis.md` and `open-finding-resolutions.md` explicitly reconcile those conflicts instead of following the pages. `.pi/evidence/pi-harness-incubation/H0/source-of-truth-map.json` assigns the future grammar to one generic resource capability, local marker/prefix/profile policy to the local layer, domain rules to existing project sources, and leaves `docs/harness/` explanatory only.

- **Correct:** Generic/local decomposition and structural/semantic separation are appropriately bounded. `.pi/evidence/pi-harness-incubation/H0/proposed-H1-contract.md` makes AST range/duplicate mechanics and structured results generic, while roots, `SV`/`NV` prefixes, pytest marker names, filename policy, migration state, P1 inventories, and the legacy `boundary_owned` mapping remain explicit local/profile inputs. It also states that validator PASS does not grant semantic, scientific, or human acceptance.

- **Correct:** Current marker and evidence-audit behavior matches the retained account. `python/pyproject.toml:55-70` declares the four distinct VVUQ markers with strict marker handling. Independent AST inspection found exactly 96 audited `test__*.py` modules: 92 with the sole executable `software_verification` marker and 4 with the sole `numerical_verification` marker. `.pi/skills/audit_evidence_identifiers.py:44-57` limits the current local audit to those two maintained hierarchies, while `:93-133` supports one fielded ID or one normalized inclusive range plus historical first-line declarations. Warning mode found 420 test functions, 403 unique owned IDs, 22 unowned functions, and zero audit errors. Strict mode returned 1, as it must; H0 correctly reports that as known debt rather than a pass or waiver.

- **Correct:** The 22-test debt is exactly localized to protected operator software-verification tests: fourteen functions in the three `OperatorRecordDifferenceResult` facet modules and eight in `test__OperatorRecordDifferencer.py`. `.pi/evidence/pi-harness-incubation/H0/component-inventory.json:7091-7139` inventories that debt locally; `.pi/evidence/class-owned-evidence-convention/migration-inventory.json` preserves the closed operator surface; and the proposed H1 audit profile supports migrated/protected/warning states rather than weakening strictness globally.

- **Correct:** H0 VVUQ applicability is stated correctly. `.pi/tasks/pi-harness-incubation-H0-inventory.md` limits H0 to control-plane/software-inventory evidence. Structural inventory, marker, schema, ownership, and replay checks are software verification. No harness numerical algorithm was implemented or discovered, so numerical verification is not applicable; no physical-model comparison or uncertainty propagation exists, so scientific validation and UQ are not applicable. The report does not use passing software gates as scientific evidence.

- **Blocker (high):** `.pi/evidence/pi-harness-incubation/H0/validate_h0.py:44-50` permits H0 changes to `.pi/evidence/backend-neutral-cpn-P1-contract/checksums.sha256` and `.pi/evidence/class-owned-evidence-convention/checksums.sha256`. That contradicts the authorized write boundary in `.pi/tasks/pi-harness-incubation-H0-inventory.md`, which permits only H0 task/checkpoint/control records and retained evidence under `.pi/evidence/pi-harness-incubation/H0/`. Both permitted checksum paths are closed historical P1/EVIDENCE-DOC-1 evidence, not H0 control records. Although `git status --short --branch` showed no current modification to either catalog, `validate_nonmutation()` would accept such an unauthorized historical-evidence mutation and therefore cannot substantiate the report's protected-path/nonmutation claim. Remove those two paths from `ALLOWED_CHANGES` (or obtain and durably record an explicit scope authorization) before treating the H0 completion validator as passing evidence.

- **Note:** The requested `/Users/eugene/repos/ksdft2effmass/plan.md` and `progress.md` were absent (`ENOENT`), so they could not inform this review. The retained H0 task, report, structured artifacts, accepted grammar/decision records, and current repository state were reviewed directly instead.

- **Note:** The H0 directory does not yet contain a final checksum catalog. That may be sequenced after all four review artifacts exist, but the task's required checksum output and final `--require-reviews`/checkpoint gates remain outstanding and must be completed before H0 checkpoint presentation.

## Commands

- `git status --short --branch && git branch --show-current` — passed; branch `dev`, H0 evidence is untracked, and no staged entries were shown. One unrelated untracked paper file was present and left untouched.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py` — passed: 149 components; 12 `DEFER`, 110 `KEEP_PROJECT_LOCAL`, 27 `SPLIT_GENERIC_AND_LOCAL`; this pass is insufficient because of the allowlist defect above.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/skills/audit_evidence_identifiers.py --self-test` — passed: self-test 0 failures, 96 modules, 420 functions, 403 owned IDs, 22 warnings, 0 errors.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/skills/audit_evidence_identifiers.py --self-test --strict` — failed with exit 1 as expected: the same 22 unowned protected functions; no audit errors.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/backend-neutral-cpn-P1-contract/validate_test_ownership.py` — passed: 32 class modules, 5 artifact modules, 49 exports, 88 IDs, 8 restored pytest gates.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/class-owned-evidence-convention/validate.py` — passed: 32 CPN modules, 78 tests/IDs, 11 helpers, 78 mappings, 5 artifact modules, 10 artifact tests, 96 inventoried modules; structural evidence only.
- `cd python && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q ../.pi/task-ownership/tests/test_validate_task_ownership.py` — passed: 36 tests.
- Independent AST marker-count script — passed: 96 modules/420 functions; 92 exact software-verification markers and 4 exact numerical-verification markers.

## Residual risks

1. The nonmutation validator currently permits unauthorized edits to two closed historical checksum catalogs; this is the blocking risk.
2. Strict repository-wide evidence-ID audit remains intentionally red until the 22 protected operator tests receive separate migration authorization.
3. Final H0 review/checksum/checkpoint gates were not available or invoked in this review; H1 remains blocked.
4. No full Python suite or Sphinx build was rerun by this reviewer; retained results report them as passed, while this review independently replayed the focused evidence/ownership gates.
5. H1 must positively bind artifact relation-side/directionality metadata into the accepted grammar/profile resource; merely excluding a third generic `boundary_owned` kind would be incomplete.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete high-severity validator finding at .pi/evidence/pi-harness-incubation/H0/validate_h0.py:44-50, plus verified correct behavior and residual risks with file paths."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py",
      "result": "passed",
      "summary": "149-component structural inventory passed, but its nonmutation allowlist is unsound."
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/skills/audit_evidence_identifiers.py --self-test",
      "result": "passed",
      "summary": "96 modules, 420 tests, 403 owned IDs, 22 warnings, 0 errors."
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/skills/audit_evidence_identifiers.py --self-test --strict",
      "result": "failed",
      "summary": "Expected exit 1 for 22 known protected unowned operator tests; no audit errors."
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/backend-neutral-cpn-P1-contract/validate_test_ownership.py && PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/class-owned-evidence-convention/validate.py",
      "result": "passed",
      "summary": "P1 ownership and accepted evidence-grammar structural replay passed."
    },
    {
      "command": "cd python && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q ../.pi/task-ownership/tests/test_validate_task_ownership.py",
      "result": "passed",
      "summary": "36 task-ownership validator tests passed."
    },
    {
      "command": "independent Python AST marker inventory",
      "result": "passed",
      "summary": "92 software-verification and 4 numerical-verification modules each had exactly the expected executable marker."
    }
  ],
  "validationOutput": [
    "Overall review verdict: FAIL due to an unsound protected-path allowlist.",
    "Evidence grammar/source-of-truth, artifact-boundary recommendation, workflow ownership, marker/profile split, strict-debt reporting, and H0 VVUQ applicability otherwise reviewed as correct."
  ],
  "residualRisks": [
    "H0 validator permits edits to two closed historical checksum catalogs outside authorized H0 write scope.",
    "Strict evidence-ID mode remains blocked by 22 protected operator tests.",
    "Final H0 reviews, checksum catalog, and checkpoint-required validation remain outstanding.",
    "Full suite and Sphinx were not independently rerun in this focused review."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only review; no project source, tests, documentation, or control records were modified.",
  "reviewFindings": [
    "blocker: .pi/evidence/pi-harness-incubation/H0/validate_h0.py:44-50 - ALLOWED_CHANGES includes two closed historical checksum catalogs outside the H0 authorized write boundary, so validate_nonmutation can accept unauthorized mutation.",
    "correct: accepted grammar and operator extension retain one evidence source of truth and separate structural tooling from semantic/VVUQ review.",
    "correct: warning and strict audit modes accurately expose the known 22-test protected debt without waiving it."
  ],
  "manualNotes": "plan.md and progress.md were requested but absent. H1-H5 and P2-P11 must remain blocked."
}
```
