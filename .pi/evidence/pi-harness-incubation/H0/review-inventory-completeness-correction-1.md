# Corrected H0 inventory-completeness review

**Checkpoint technical-adequacy verdict: FAIL**

The leakage, dependency, source-map ID coverage, command-manifest, Graphify, and nonmutation corrections are present and reproducible. However, the original atomic-granularity defect is not fully corrected: the 341 inventory rows describe only 316 unique paths, and several physical artifacts receive contradictory classifications and future owners. The passing validator does not check path uniqueness.

## Review

- **Correct:** `validate_h0.py` runs successfully and reports 341 rows: 38 `SPLIT_GENERIC_AND_LOCAL`, 289 `KEEP_PROJECT_LOCAL`, and 14 `DEFER`. H0 remains the sole active harness task; H1--H5 and P2--P11 remain blocked, and all four prospective roots remain absent.
- **Correct:** The leakage correction is complete for the current candidate set. `leakage-audit.json#/candidate_files_scanned` lists all 38 split/extractable candidate IDs; 33 have matches and the other five are explicitly listed under `summary.generic_candidates_with_no_reported_match`. The validator now reads every candidate file without suffix filtering (`validate_h0.py:263-318`) and reproduces exactly 527 occurrences: 293 path/discovery, 135 task/evidence-identity, and 99 domain-coupling occurrences. No generic-to-local edge is approved.
- **Correct:** Direct dependencies are reconciled. The inventory declares 21 `(component, dependency)` pairs, and `dependency-map.json` contains exactly the same 21 `declared_direct_dependency` edges; `validate_h0.py:222-260` now compares both sets.
- **Correct:** `source-of-truth-map.json` assigns all 341 component IDs exactly once, and `validate_h0.py:176-219` enforces full ID coverage and uniqueness. This corrects the former 108/149 ID-coverage defect, subject to the physical-path blocker below.
- **Correct:** Graphify is now consistently deferred: the complete `SKL-001`--`SKL-011` closure is retained under `graphify_optional_integration`, owned by existing project-domain source, and excluded from minimum H1.
- **Correct:** The nonmutation corrections address both initial review defects. `ALLOWED_CHANGES` contains only the H0 chain/task/checkpoint control records (`validate_h0.py:44-50`), and `validate_nonmutation()` now accounts for untracked files and verifies each concurrent unrelated path by SHA-256 (`validate_h0.py:385-434`). `concurrent-unrelated-worktree.json` records all three current unrelated paths, including both conference files and the empty paper file, and the validator passed with those paths present.
- **Correct:** `command-environment-manifest.json#/validation_commands` now provides argv arrays, environment, working directory where needed, inputs, outputs, purpose, and side effects for all retained gates, including warning/strict evidence audits, P1 replays, Sphinx, Ruff, checksum validation, and `git diff --check`. The temporary Sphinx destination is intentionally symbolic rather than a stable output path.
- **Correct:** The absent final H0 `checksums.sha256` is not treated as a standalone failure in this review. The manifest defines its validation command and the report records the intended ordering: stabilize the final reviews, generate the catalog, then validate it before checkpoint creation. Its eventual content and result remain a closeout condition.
- **Blocker:** The claimed atomic inventory remains overlapping. `component-inventory.json#/granularity_policy` says every present component record names one file and independently owned files are not collapsed, but the 341 rows contain only **316 unique `current_path` values** (312 present files plus four absent prospective roots). Twenty-five present paths are each inventoried twice. Examples include `EVD-001` and `FIL-012` for `.pi/evidence/backend-neutral-cpn-P0-preflight/preflight.py`, `EVD-015` and `FIL-030` for `.pi/evidence/backend-neutral-cpn-P1-contract/contract_gates.py`, and `EVD-024` and `FIL-066` for `.pi/evidence/class-owned-evidence-convention/validate.py`. Most importantly, the same checksum artifacts receive contradictory classifications: `EVD-007` versus `FIL-004`, `EVD-013` versus `FIL-015`, `EVD-022` versus `FIL-029`, and `EVD-029` versus `EVD-028` classify each identical physical catalog as both `SPLIT_GENERIC_AND_LOCAL` and `KEEP_PROJECT_LOCAL`. The corresponding source-map rows consequently assign one physical file both to generic artifact-integrity ownership and to historical evidence. Thus “341 components” is still a count of rows, not an exact non-overlapping atomic-file/prospective inventory with one classification and one future authority per component.
- **Blocker:** The deterministic gate does not detect that defect. `validate_inventory()` checks component-ID uniqueness, counts, existence, enum values, and array ordering, but never requires `current_path` uniqueness or requires every non-prospective path to be a file (`validate_h0.py:117-156`). `validate_source_map()` proves uniqueness only over duplicated component IDs, not physical paths (`validate_h0.py:176-219`). This is why `validate_h0.py` returns PASS despite the unresolved original granularity finding. Checkpoint adequacy requires deduplicating the physical artifacts and adding a deterministic path-level granularity assertion.
- **Note:** Repository-root `plan.md` and `progress.md` were requested but do not exist, so no evidence could be read from them. The original H0 task, chains, all 17 current H0 artifacts, initial reviews, correction record, and current repository state were inspected instead.

## Initial finding disposition

1. **H0 checksum catalog absent:** conditionally acceptable at this review stage; final catalog generation and validation remain required after review text stabilizes.
2. **Incomplete leakage audit:** corrected; 38/38 readable candidates and 527 reproducible occurrences are covered.
3. **Mixed/overlapping granularity:** **not corrected**; directory families were expanded, but 25 previously named files were retained as duplicate rows.
4. **Incomplete source map:** ID coverage corrected, but unique physical ownership remains invalid because duplicate paths cross authority rows.
5. **Unreconciled direct dependencies:** corrected; exact 21-pair equality is validated.
6. **Incomplete command manifest:** corrected to structured argv/environment/input/output/side-effect records.
7. **Graphify contradiction:** corrected by consistent deferral.
8. **Untracked-file/nonmutation blind spot and historical allowlist:** corrected with pinned concurrent paths and a narrowed allowlist.

## Commands

- `PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py` — **PASS**: 341 rows; checkpoint/review requirements false.
- Read-only Python accounting over inventory, source map, dependency map, and leakage audit — completed: 341 rows, 316 unique paths, 25 duplicate paths, 341/341 source-map ID assignments, 21/21 direct-dependency equality, and 527 leakage occurrences.
- Read-only candidate/source-family coverage inspection — completed: all files under the expanded historical evidence, ownership fixtures, maintained CPN/operator evidence, and CPN specification families are represented; the defect is duplicate representation, not an omitted file in those expanded families.
- `git status --short --branch` — completed: no staged files; H0 evidence and three pinned concurrent unrelated paths are untracked.

## Residual risks

- The final H0 checksum catalog cannot be validated until the corrected final review set and catalog are stable; this sequencing is acceptable, but checkpoint creation must remain blocked until the catalog passes.
- The repository-wide strict evidence-ID audit still has 22 known protected operator-test gaps. This is explicitly retained debt, not an H0 inventory failure or scientific waiver.
- `--require-reviews` and `--require-checkpoint` were not invoked because the corrected final review set and `H0-HC01` do not yet exist in the reviewed H0 directory.
- The validator's leakage reconstruction is complete for current readable candidates, but it does not independently validate the informational `candidate_files_scanned` and zero-match metadata fields. Their current values were manually reconciled and are correct.
- No scientific validation, UQ, numerical verification, external execution, or implementation validation is implied or applicable to H0.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete blocker findings identify duplicate component IDs/paths in component-inventory.json and the missing path-uniqueness assertions in validate_h0.py:117-156 and :176-219; corrected findings and residual risks are separately enumerated."
    }
  ],
  "changedFiles": [
    ".pi-subagents/artifacts/outputs/74dd7a29/.pi/evidence/pi-harness-incubation/H0/review-inventory-completeness.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py",
      "result": "passed",
      "summary": "Reported 341 rows and passed all current default gates; this is a false positive for atomic path uniqueness."
    },
    {
      "command": "Read-only Python inventory/source/dependency/leakage accounting",
      "result": "passed",
      "summary": "Found 341 rows but only 316 unique paths and 25 duplicated present paths; confirmed 341/341 source-map ID coverage, exact 21-pair dependency reconciliation, and 527 audit occurrences."
    },
    {
      "command": "git status --short --branch and expanded-family file coverage inspection",
      "result": "passed",
      "summary": "Confirmed no staged files, all three unrelated untracked paths are recorded, and expanded family files are represented."
    }
  ],
  "validationOutput": [
    "h0_inventory_validation=passed; components=341; classifications={DEFER:14, KEEP_PROJECT_LOCAL:289, SPLIT_GENERIC_AND_LOCAL:38}",
    "Independent path accounting: 341 rows, 316 unique paths, 25 duplicated present paths.",
    "Checkpoint technical-adequacy verdict: FAIL because one physical artifact can have multiple component IDs, classifications, and future owners."
  ],
  "residualRisks": [
    "Final H0 checksum catalog and closeout-mode review/checkpoint gates remain pending by design.",
    "22 protected operator tests remain known strict evidence-ID debt.",
    "Leakage candidate-list metadata is manually correct but not itself asserted by validate_h0.py."
  ],
  "noStagedFiles": true,
  "diffSummary": "No reviewed repository files were edited; only the required external review artifact was written.",
  "reviewFindings": [
    "blocker: .pi/evidence/pi-harness-incubation/H0/component-inventory.json - 341 rows contain only 316 unique paths; 25 physical files are duplicated, and four checksum catalogs receive contradictory SPLIT_GENERIC_AND_LOCAL/KEEP_PROJECT_LOCAL classifications and future owners.",
    "blocker: .pi/evidence/pi-harness-incubation/H0/validate_h0.py:117-156 and :176-219 - validation enforces unique IDs but not unique atomic current_path values, allowing the unresolved granularity defect to pass.",
    "correct: leakage-audit.json and validate_h0.py:263-318 - all 38 readable candidates and exactly 527 semantically disposed occurrences are covered.",
    "correct: dependency-map.json and validate_h0.py:222-260 - all 21 declared direct dependencies are exactly reconciled.",
    "correct: concurrent-unrelated-worktree.json and validate_h0.py:385-434 - untracked protected paths are pinned and checked, and closed historical catalogs are no longer allowlisted."
  ],
  "manualNotes": "FAIL is for H0-HC01 technical adequacy only. The final checksum's intentional post-review generation is not the reason for failure; deduplicating atomic paths and enforcing that invariant is required before checkpoint presentation."
}
```
