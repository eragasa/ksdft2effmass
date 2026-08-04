# Corrected independent H0 architecture and extraction review

## Review

**Result: FAIL**

- **Correct:** The deterministic validator passes the current structural checks: `341` component IDs, classifications `DEFER=14`, `KEEP_PROJECT_LOCAL=289`, and `SPLIT_GENERIC_AND_LOCAL=38`. The source map accounts for all 341 component IDs exactly once, and the validator now reads untracked paths, compares the three concurrent unrelated paths against recorded SHA-256 values, and rejects unaccounted paths (`.pi/evidence/pi-harness-incubation/H0/validate_h0.py:405-432`; `.pi/evidence/pi-harness-incubation/H0/concurrent-unrelated-worktree.json:5-25`). Live hashes matched the record.
- **Correct:** The generic/local boundary is appropriately narrow: generic code owns structural integrity while local configuration owns `.pi`, task/checkpoint identities, Git policy, evidence profiles, and scientific/domain semantics (`.pi/evidence/pi-harness-incubation/H0/proposed-H1-contract.md:53-57`). The minimum H1 contract is immutable, explicit-root, versioned, deterministic, Rust-portable, and restricted to demonstrated consumers (`proposed-H1-contract.md:3-5`); Graphify, implicit discovery, scientific validation/UQ, and numerical APIs without an algorithm are excluded (`proposed-H1-contract.md:59-73`).
- **Correct:** The retained schedule and ownership recommendations are sound and protected rather than implemented: H3 precedes H2 sequentially, and future work uses harness-specific roles plus version-2 exact-path manifests (`.pi/evidence/pi-harness-incubation/H0/H0-report.md:96-103`; `open-finding-resolutions.md:41-63`).
- **Blocker (high) — atomic inventory and unique source ownership remain false at the file level:** `component-inventory.json` contains 341 component IDs but only 316 distinct current paths; 25 present files are represented twice. Four checksum catalogs receive contradictory classifications and future owners. For example, the same P0 checksum file is `EVD-007` (`SPLIT_GENERIC_AND_LOCAL`, lines 2018-2020) and `FIL-004` (`KEEP_PROJECT_LOCAL`, lines 3397-3399); the same pattern occurs for `EVD-013`/`FIL-015` (lines 2313-2315 and 3947-3949), `EVD-022`/`FIL-029` (lines 2755-2757 and 4647-4649), and `EVD-028`/`EVD-029` (lines 3050-3052 and 3100-3102). The source map assigns the split IDs to future generic `artifact_integrity_validation` (`source-of-truth-map.json:20-29`) while assigning the duplicate IDs to `historical evidence` (`source-of-truth-map.json:202-260`). `validate_source_map()` checks component-ID uniqueness only (`validate_h0.py:215-220`), not current-path uniqueness, so it cannot support the report's claim of one future authoritative owner (`H0-report.md:94`). This violates atomic granularity and leaves the concrete source owner ambiguous.
- **Blocker (high) — direct-dependency reconciliation is mechanically circular rather than complete:** the inventory declares only 21 direct dependencies, while the dependency map itself contains 39 additional direct relationships under other edge kinds that are absent from `direct_dependencies`. Examples include the checkpoint validator using its fixture/schema (`dependency-map.json:1474-1483` versus `component-inventory.json:924-943`), the ownership validator using three schemas (`dependency-map.json:1780-1795` versus `component-inventory.json:13478-13498`), the Graphify entry referencing its ten-resource closure (`dependency-map.json:1840-1897` versus `component-inventory.json:14065-14095`), and the checkpoint-resolution skill consuming the schema/validator (`dependency-map.json:1900-1909` versus `component-inventory.json:14545-14564`). The validator compares `direct_dependencies` only to edges pre-labelled `declared_direct_dependency` (`validate_h0.py:238-249`), so both sides can agree while known direct edges remain omitted. The requested complete direct-dependency reconciliation is therefore not established.
- **Blocker (high) — Graphify is excluded from H1 but its retained classification/destination is not fully consistent:** the source map correctly groups `SKL-001`–`SKL-011` under `graphify_optional_integration`, assigns the closure to `existing project-domain source`, and says not to copy it into harness resources (`source-of-truth-map.json:183-198`). Most closure records are `DEFER`, and H1 excludes Graphify (`proposed-H1-contract.md:68`). However, `SKL-001` still proposes a `harness/pi` manifest destination (`component-inventory.json:14053-14060`), while `SKL-008` is `KEEP_PROJECT_LOCAL` but proposes movement to `harness/local/` (`component-inventory.json:14389-14396`). Those destinations contradict the closure-level existing-source owner and the claim that the complete closure was consistently deferred/kept existing. Either all closure destinations must remain the existing source while deferred, or the exception and later migration boundary must be made explicit and consistent in the source map/report.
- **Note:** The H0 checksum catalog is absent, which matches the stated sequencing that it is generated only after final reviews stabilize. The final checksum cannot attest this failing review state yet.
- **Note:** Requested repository-root `plan.md` and `progress.md` were absent (`ENOENT`); the active H0 task, chain, structured evidence, initial architecture review, and resolution report were available.

## Residual risks

- Public names, serialized fields, compatibility rules, stable issue-code ordering, and checkpoint durability/replay fields remain protected H1 decisions.
- The three unrelated untracked paths are now detected and hash-pinned, but provenance for the empty `docs/papers/ksdft2efffmas.P03.md` remains unresolved as recorded.
- Strict evidence-ID mode still has 22 protected historical operator-test warnings; this is retained debt, not H0 scientific evidence.
- Current chain/task prose still permits H2/H3 sibling concurrency until human acceptance durably changes the schedule; H3-before-H2 is presently a recommendation only.
- No numerical verification, scientific validation, UQ, external execution, or extraction was performed; these are not applicable to this H0 review.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete high-severity findings cite component-inventory.json, source-of-truth-map.json, dependency-map.json, validate_h0.py, H0-report.md, and proposed-H1-contract.md with line ranges; residual risks are separately listed."
    }
  ],
  "changedFiles": [
    ".pi-subagents/artifacts/outputs/74dd7a29/.pi/evidence/pi-harness-incubation/H0/review-architecture-classification.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py",
      "result": "passed",
      "summary": "Reported h0_inventory_validation=passed with 341 components; checkpoint/review requirements were false."
    },
    {
      "command": "git diff --check; git diff --name-only BASE_COMMIT; git ls-files --others --exclude-standard; shasum -a 256 <three concurrent paths>",
      "result": "passed",
      "summary": "No whitespace/tracked unauthorized diff was reported; all unrelated untracked paths were accounted for and hashes matched."
    },
    {
      "command": "test ! -e .pi/evidence/pi-harness-incubation/H0/checksums.sha256",
      "result": "passed",
      "summary": "Confirmed the H0 checksum is intentionally not generated before final reviews stabilize."
    },
    {
      "command": "Python structured cross-checks of inventory paths, source owners, classifications, direct_dependencies, and dependency edges",
      "result": "failed",
      "summary": "Found 341 IDs but 316 unique paths (25 duplicate paths), four checksum files with conflicting classifications/owners, and 39 dependency-map relationship edges absent from inventory direct_dependencies."
    }
  ],
  "validationOutput": [
    "Deterministic validator: PASS (341 components).",
    "Independent architecture/extraction verdict: FAIL.",
    "Atomic/source-owner check: 25 duplicate current paths; four checksum paths have conflicting classifications/future owners.",
    "Dependency reconciliation check: 39 known relationship edges omitted from inventory direct_dependencies.",
    "Graphify remains excluded from H1, but SKL-001/SKL-008 candidate destinations conflict with closure-level existing-source ownership."
  ],
  "residualRisks": [
    "Protected H1 API, wire, compatibility, issue-code, and durability details remain undecided.",
    "22 known strict evidence-ID warnings remain in protected historical tests.",
    "H3-before-H2 remains a recommendation until human acceptance updates authoritative scheduling.",
    "Concurrent paper-path provenance remains unresolved although path/hash accounting now passes."
  ],
  "noStagedFiles": true,
  "diffSummary": "Wrote only the required external review artifact; no reviewed H0 evidence, source, tests, docs, chain, task, or checkpoint file was edited.",
  "reviewFindings": [
    "blocker: .pi/evidence/pi-harness-incubation/H0/component-inventory.json and source-of-truth-map.json - 25 duplicate current paths defeat atomic file granularity; four checksum files have conflicting classifications and future owners",
    "blocker: .pi/evidence/pi-harness-incubation/H0/validate_h0.py:238-249 and dependency-map.json - validator reconciles only pre-labelled declared edges while 39 known direct relationship edges are absent from inventory direct_dependencies",
    "blocker: component-inventory.json SKL-001/SKL-008 and source-of-truth-map.json graphify_optional_integration - Graphify is excluded from H1 but candidate destinations conflict with keeping the full closure at its existing source"
  ],
  "manualNotes": "The validator pass is narrower than the requested corrected architecture review. Root plan.md and progress.md were absent."
}
```
