# Corrected H0 evidence/VVUQ review

**Verdict: FAIL**

The initial evidence-review blocker is corrected, and the evidence/VVUQ recommendations remain sound. However, the H0 completion validator has a separate false-pass path for required review verdicts, so it should be corrected before final review stabilization and checksum generation.

Skill applied: `document-research-python` (`b1fd3c22bc4e1b798e47796110e4f3f15f2085ac32a6a3c4396b599fb52c5393` as retained in `.pi/skills/skill-capability-inventory.json`). Profile: `REVIEW_ONLY`; task: `H0`; produced artifact: this review; reviewed repository files were not modified.

## Review

- **Correct:** The initial unauthorized historical-checksum allowance was removed. `.pi/evidence/pi-harness-incubation/H0/validate_h0.py:62-66` now allows only the H0 chain, task, and checkpoint control records; `.pi/evidence/backend-neutral-cpn-P1-contract/checksums.sha256` and `.pi/evidence/class-owned-evidence-convention/checksums.sha256` are no longer allowed H0 changes. `validate_nonmutation()` still limits all other task output to `.pi/evidence/pi-harness-incubation/H0/` (`validate_h0.py:395-404`). Current Git inspection showed no tracked or staged change from baseline commit `d0b253158eac2c57748923f6484a794721e5c97f`, and all four existing historical checksum catalogs replayed successfully.

- **Correct:** Artifact/boundary and Workflow ownership recommendations remain aligned with the accepted grammar. `.pi/evidence/pi-harness-incubation/H0/open-finding-resolutions.md:5-15` retains only generic `class_owned` and `artifact_owned`, makes relation sides/directionality artifact metadata, keeps legacy P1 `boundary_owned` behind a local compatibility mapping, and treats a genuine public Workflow as class-owned while technical integration remains artifact-owned. This matches `.pi/skills/document-research-python/references/test-evidence-documentation.md:108-125,137-176`. P1 ownership, grammar validation, and the ten-case artifact replay all passed.

- **Correct:** The evidence grammar has one source capability rather than competing skill authorities. `.pi/evidence/pi-harness-incubation/H0/open-finding-resolutions.md:17-27`, `duplication-and-overlap-analysis.md:11-21`, and `source-of-truth-map.json` (`research_evidence_documentation_grammar`) all retain `document-research-python` as the accepted grammar source, with operator/CPN/local extensions referencing it. `.pi/skills/develop-operator-records/SKILL.md:10-12` explicitly delegates repository-wide grammar ownership to that shared reference. `proposed-H1-contract.md:59-72` excludes a new `write-research-evidence-tests` identity and a third generic `boundary_owned` kind.

- **Correct:** The leakage/profile split is complete at H0's screening boundary and is not overstated as semantic proof. `leakage-audit.json` covers all 38 readable `SPLIT_GENERIC_AND_LOCAL` candidates, with 527 reproducible occurrences classified into project-domain, task/evidence-identity, or path/discovery coupling; five candidates have no lexical match. `validate_h0.py:276-341` reconstructs those occurrences over every readable candidate file. `open-finding-resolutions.md:65-75` and `proposed-H1-contract.md:53-57` keep roots, IDs, markers, evidence namespaces, filename/migration policy, Git policy, compatibility, and domain semantics local/profile-owned and prohibit generic-to-local imports and implicit repository discovery.

- **Correct:** The strict evidence-ID debt is reported honestly. Warning mode returned 96 modules, 420 test functions, 403 unique owned identifiers, 22 unowned functions, and zero audit errors. Strict mode returned exit 1 for exactly those same 22 functions: 14 across the three `OperatorRecordDifferenceResult` facet modules and 8 in `test__OperatorRecordDifferencer.py`. `.pi/evidence/pi-harness-incubation/H0/validation-results.json:106-115` records warning-mode PASS and strict-mode exit 1 as known debt, not as strict conformance; `H0-report.md:123-129,140-144` retains the limitation without waiving it.

- **Correct:** H0's VVUQ classification is correct. The task limits H0 to control-plane/software-inventory evidence (`.pi/tasks/pi-harness-incubation-H0-inventory.md:21-34,52-54`). Structural schema, inventory, ownership, marker, checksum, and replay gates are software verification. No harness numerical algorithm, physical-reference comparison, or uncertainty propagation exists, so numerical verification, scientific validation, and UQ are not applicable. This agrees with the accepted definitions in `.pi/skills/document-research-python/references/test-evidence-documentation.md:9-27` and the retained result in `validation-results.json:164-168`. Independent AST inspection also confirmed exactly 92 software-verification modules and 4 numerical-verification modules, each with only its hierarchy-appropriate marker.

- **Blocker (high):** The required-review gate can accept an explicit FAIL review. `.pi/evidence/pi-harness-incubation/H0/validate_h0.py:382-392` considers a review passing whenever its text contains the substring `PASS`; it does not parse an exact verdict or reject `FAIL`. A normal failed review commonly mentions passing subchecks—each retained initial FAIL review does—so `--require-reviews` can false-pass. This makes the validator's “required passing review” claim unsound even though the present corrected evidence findings are otherwise satisfactory. Require an unambiguous structured verdict (for example, exact front-matter/JSON status or an anchored verdict line) and reject contradictory/multiple verdicts before final checksum creation.

- **Note:** The requested repository-root `plan.md` and `progress.md` were absent and could not be reviewed. The authoritative task, chains, retained H0 artifacts, accepted evidence grammar, and P1 replay records were available.

## Residual risks

1. `--require-reviews` currently has the false-pass behavior above; this blocks a reliable final H0 completion replay.
2. Strict evidence-ID conformance remains intentionally red for 22 protected operator tests and requires separate test-migration authorization.
3. The final H0 checksum catalog and `H0-HC01` checkpoint are intentionally not present yet; final checksum generation must follow corrected final-review stabilization, and H1 must remain blocked.
4. Focused gates and all existing checksum catalogs were replayed, but this reviewer did not rerun the full Python suite or Sphinx build.
5. H1 still requires human acceptance of relation metadata, generic/local profile fields, and migration constraints; structural validation cannot grant those decisions or scientific acceptance.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete high-severity validator finding at .pi/evidence/pi-harness-incubation/H0/validate_h0.py:382-392, plus file-cited verification of the corrected checksum boundary, evidence grammar, artifact/workflow recommendation, leakage/profile split, strict debt, and VVUQ classification."
    }
  ],
  "changedFiles": [
    ".pi-subagents/artifacts/outputs/74dd7a29/.pi/evidence/pi-harness-incubation/H0/review-evidence-vvuq.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py",
      "result": "passed",
      "summary": "341 components passed schema, accounting, source-map, dependency, leakage, state, and nonmutation checks in precheckpoint mode."
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/skills/audit_evidence_identifiers.py --self-test",
      "result": "passed",
      "summary": "96 modules, 420 test functions, 403 owned IDs, 22 warnings, and 0 audit errors."
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/skills/audit_evidence_identifiers.py --self-test --strict",
      "result": "failed",
      "summary": "Expected exit 1 for exactly 22 retained unowned operator tests; this was not treated as a pass."
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/backend-neutral-cpn-P1-contract/validate_test_ownership.py && PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/class-owned-evidence-convention/validate.py && PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/backend-neutral-cpn-P1-contract/contract_gates.py",
      "result": "passed",
      "summary": "P1 ownership and accepted grammar validation passed; artifact replay passed 10 cases across 5 modules."
    },
    {
      "command": "for f in .pi/evidence/*/checksums.sha256; do sha256sum -c \"$f\"; done",
      "result": "passed",
      "summary": "All four existing historical evidence catalogs verified; no H0 catalog exists yet by planned sequencing."
    },
    {
      "command": "independent Python AST marker inventory",
      "result": "passed",
      "summary": "96 modules and 420 functions; 92 modules had only software_verification and 4 had only numerical_verification."
    },
    {
      "command": "git diff --name-only d0b253158eac2c57748923f6484a794721e5c97f --; git diff --cached --name-only; git ls-files --others --exclude-standard",
      "result": "passed",
      "summary": "No tracked or staged H0-baseline changes; H0 artifacts and three hash-pinned unrelated paths are untracked."
    }
  ],
  "validationOutput": [
    "Overall corrected review verdict: FAIL because the final required-review validator can false-pass FAIL artifacts.",
    "Initial unauthorized historical-checksum allowlist blocker is resolved.",
    "Evidence grammar/source, artifact-boundary/workflow model, complete leakage/profile split, strict-debt reporting, and H0 VVUQ classification are otherwise correct."
  ],
  "residualRisks": [
    "The --require-reviews gate searches for an unanchored PASS substring and does not reject an explicit FAIL verdict.",
    "Strict evidence-ID mode remains blocked by 22 protected operator tests.",
    "Final H0 checksum, checkpoint, and closeout-mode validation remain outstanding by design.",
    "Full Python suite and Sphinx warnings-as-errors were not independently rerun in this focused review."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only project review; no reviewed source, tests, documentation, task, chain, checkpoint, or retained H0 artifact was modified. Only the required out-of-tree review artifact was written.",
  "reviewFindings": [
    "blocker: .pi/evidence/pi-harness-incubation/H0/validate_h0.py:382-392 - required reviews pass on any PASS substring, so an explicit FAIL review containing a passing-subcheck statement can satisfy --require-reviews.",
    "correct: .pi/evidence/pi-harness-incubation/H0/validate_h0.py:62-66 - closed P1 and evidence-convention checksum catalogs were removed from ALLOWED_CHANGES.",
    "correct: open-finding-resolutions.md:5-37 and proposed-H1-contract.md:53-72 - artifact/workflow ownership, unique grammar source, and generic/local evidence-profile split remain sound.",
    "correct: validation-results.json:106-115,164-168 - strict 22-test debt and H0 VVUQ applicability are reported without unsupported pass or scientific claims."
  ],
  "manualNotes": "plan.md and progress.md were requested but absent. H1-H5 and P2-P11 must remain blocked; generate the final H0 checksum only after correcting and stabilizing all final reviews."
}
```
