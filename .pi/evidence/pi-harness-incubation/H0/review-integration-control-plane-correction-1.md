# Corrected H0 integration/control-plane review

## Verdict: PASS

PASS applies to the corrected pre-checksum integration/control-plane evidence. It is not H0 completion, human acceptance, or authorization to create implementation. The four final review records must be retained and the final checksum catalog generated and verified before `H0-HC01` is created.

## Review

### Correct

- **The initial untracked-file blocker is corrected.** `.pi/evidence/pi-harness-incubation/H0/validate_h0.py:405-432` now inventories nonignored untracked paths, rejects any path outside the H0 evidence/checkpoint allowance unless it is recorded as concurrent unrelated work, and verifies every recorded concurrent file by SHA-256. All three current unrelated paths are explicitly preserved, pinned, and excluded from the future H0 checkpoint commit in `.pi/evidence/pi-harness-incubation/H0/concurrent-unrelated-worktree.json:5-26`. Their current hashes exactly match the record. There are no other untracked paths outside H0.
- **Current Git scope is clean and bounded.** `HEAD` and the H0 baseline are both `d0b253158eac2c57748923f6484a794721e5c97f` on `dev`. Tracked, unstaged, and staged diffs are empty. The only untracked repository paths are the 18 H0 evidence files and the three pinned unrelated documentation files. The latter are not staged. The corrected allowlist at `validate_h0.py:62-66` contains only the H0 harness chain, H0 task, and future H0 checkpoint; the two closed historical checksum catalogs flagged by the initial evidence/VVUQ review are no longer allowed.
- **The corrected structural inventory passes.** The H0 validator reports 341 component records: 38 `SPLIT_GENERIC_AND_LOCAL`, 289 `KEEP_PROJECT_LOCAL`, and 14 `DEFER`. It now enforces complete 341-component capability/source-map accounting, reconciles declared direct dependencies with dependency-map edges, reproduces all 527 screened leakage occurrences across 38 readable candidates, and rejects prohibited prospective roots. This addresses the initial inventory and architecture findings. Graphify is consistently deferred from minimum H1 and assigned to existing project-domain source in `source-of-truth-map.json` rather than copied into future harness resources.
- **The exact control-plane state is correct.** `.pi/chains/pi-harness-incubation.chain.json:5-7,37-73,104-108` keeps H0 as the sole active read-only task, H1--H5 blocked, no pending checkpoint, no production/publication authority, and no concurrent execution authority. `.pi/chains/backend-neutral-kohn-sham-qe.chain.json:4-6,62-70` has no active task and keeps P2 blocked. P3--P11 are also blocked.
- **The exact P2 gate agrees across authoritative records.** The harness chain requires exactly `P1:human_accepted`, `H5:human_accepted`, and `explicit_activation:P2`, with no automatic activation on H5 (`.pi/chains/pi-harness-incubation.chain.json:81-87`). The backend-neutral chain has the same ordered prerequisite list (`.pi/chains/backend-neutral-kohn-sham-qe.chain.json:62-70`), and `.pi/tasks/backend-neutral-cpn-P2-tools-provenance.md:3-13` states that accepted H5 must not launch P2.
- **Checkpoint state and sequencing are correct for this phase.** Checkpoint validation passed 13 records including fixtures, with zero unresolved checkpoints and zero duplicate resolved decisions. `H0-HC01` does not yet exist and was not created prematurely. The closeout validator separately supports review-required and checkpoint-required phases at `validate_h0.py:371-391`.
- **No implementation or capability overclaim was found.** All four prospective roots are absent. `H0-report.md:5` explicitly denies human acceptance, `open-finding-resolutions.md:1-3` keeps the six protected outcomes as recommendations, and `proposed-H1-contract.md` limits H1 to proposed immutable records/stateless actions while excluding orchestration, execution, publication, scientific interfaces, and implicit repository discovery. No H1/P2 implementation, source movement, test/schema/fixture mutation, external scientific execution, or package work is present.
- **Dependencies, locks, and documentation remain unchanged.** Current SHA-256 values are `5d6318812c7db69b7b1d5d742bbd9be903419a2c5bd702ed90a240a73d661f6c` for `python/pyproject.toml` and `186504b6dc24b054c15ef01ed3219c6829f83585a0d7c6a551d79ede37cb7368` for `python/uv.lock`, matching `validate_h0.py:438-449`. `docs/conf.py:15-26` retains the bounded numbered harness glob, and `docs/index.rst:46-62` lists the index and eight hidden children. Sphinx warnings-as-errors passed to a removed temporary directory.
- **Existing integrity records remain valid.** All five existing P0/P0A/P1/EVIDENCE-DOC-1/harness-initialization checksum catalogs verify. The final H0 catalog is intentionally deferred until corrected final reviews stabilize, as required by the review-first/checksum-last sequence.

### Blocker

- None for this corrected integration review.

### Note

- **Final assembly remains mandatory.** At inspection time the retained H0 directory contains only the four `*-initial.md` FAIL reviews and no `checksums.sha256`; the corrected final reviews are being produced as separate review artifacts. The forward references in `H0-report.md:131-138` become true only after all four final PASS records are copied into the retained H0 directory. Generate and verify the final checksum catalog only after those records stabilize. Then run `validate_h0.py --require-reviews`; after creating the genuine pending checkpoint and updating its task/chain state, run `validate_h0.py --require-reviews --require-checkpoint`. If the checksum catalog includes task, chain, or checkpoint state that changes at the checkpoint boundary, regenerate it after that mutation rather than retaining a stale digest.
- **Medium residual gate weakness:** `validate_h0.py:382-391` treats any occurrence of the text `PASS` in a final review file as a passing review. A top-level `FAIL` review that mentions a passing command could satisfy that mechanical check. Parent verification must inspect each explicit overall verdict rather than relying on this substring test. This does not invalidate the present independent PASS, but it remains a fail-open risk in final closeout evidence.
- The pinned Office lock file may change while its owning application is open. That will correctly make H0 validation fail closed; it must not be refreshed, staged, or silently adopted as H0 work.
- The known 22 protected operator evidence-ID gaps remain strict-mode debt. Warning-mode success must not be represented as strict conformance.
- `plan.md` and `progress.md` requested by the review task do not exist at repository root. Authoritative task, chain, checkpoint, and retained evidence records were available and sufficient.
- Structural inventory and control-plane PASS do not establish semantic correctness of every future classification, extraction readiness, package readiness, scientific validation, uncertainty quantification, or human acceptance.

## Commands run

- `PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py` — PASS; 341 components, corrected accounting/state/nonmutation gates.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/checkpoints/validate_checkpoints.py --include-fixtures --dry-run` — PASS; 13 records, zero unresolved, zero duplicate resolved decisions.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/skills/validate_skill_capabilities.py` — PASS; 6 skills, 13 review blocks, 12 deterministic blocks, zero errors.
- `cd python && PYTHONDONTWRITEBYTECODE=1 uv run sphinx-build -W -q ../docs <temporary>/html` — PASS; temporary output removed.
- `cd python && uv run ruff check ../.pi/evidence/pi-harness-incubation/H0/validate_h0.py` — PASS.
- `sha256sum -c` for the five existing evidence/initialization catalogs — PASS.
- Dependency/lock and concurrent-unrelated SHA-256 checks — PASS; all recorded hashes match.
- Prospective-path absence, JSON parsing, Git status/diff/staging, and `git diff --check` inspections — PASS; four roots absent, nine H0 JSON files valid, no tracked/staged diff, no unexpected untracked path.

## Residual risks

- Final corrected review files and the final H0 checksum catalog were not yet retained, so their eventual bytes and catalog coverage could not be attested by this review.
- The review-required validator uses a fail-open substring test for `PASS`; explicit verdict inspection remains necessary.
- Concurrent unrelated untracked files remain outside H0 ownership and must stay excluded from staging.
- Strict evidence-ID mode retains 22 known protected gaps.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings cite validate_h0.py, both chains, the P2 task, H0 report, concurrent-unrelated record, docs configuration, hashes, commands, and residual risks."
    }
  ],
  "changedFiles": [
    ".pi-subagents/artifacts/outputs/74dd7a29/.pi/evidence/pi-harness-incubation/H0/review-integration-control-plane.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py",
      "result": "passed",
      "summary": "341-component inventory, state, leakage, dependency, source-map, prospective-path, hash, and nonmutation validation passed."
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/checkpoints/validate_checkpoints.py --include-fixtures --dry-run",
      "result": "passed",
      "summary": "13 checkpoint records validated; zero unresolved and zero duplicate resolved decisions."
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/skills/validate_skill_capabilities.py",
      "result": "passed",
      "summary": "Six skills validated with zero errors."
    },
    {
      "command": "cd python && PYTHONDONTWRITEBYTECODE=1 uv run sphinx-build -W -q ../docs <temporary>/html",
      "result": "passed",
      "summary": "Warnings-as-errors Sphinx build passed; temporary output was removed."
    },
    {
      "command": "sha256sum -c <five existing evidence and initialization catalogs>",
      "result": "passed",
      "summary": "All existing catalogs verified; the final H0 catalog is intentionally generated after final reviews stabilize."
    },
    {
      "command": "git status/diff/staging, hash, JSON, prospective-path, Ruff, and whitespace inspections",
      "result": "passed",
      "summary": "No tracked or staged diff; three unrelated untracked paths exactly pinned; no unexpected untracked paths; four prospective roots absent."
    }
  ],
  "validationOutput": [
    "H0 validator: 341 components; 38 split, 289 local, 14 deferred.",
    "Control state: H0 active read-only; H1-H5 and P2-P11 blocked; no pending checkpoint.",
    "Exact P2 gate: accepted P1, accepted H5, and separate explicit P2 activation; H5 cannot auto-launch P2.",
    "Dependency and lock hashes match the recorded baseline; Sphinx -W and existing checksum catalogs pass.",
    "Corrected final reviews and final H0 checksum remain intentionally pending final assembly."
  ],
  "residualRisks": [
    "Final corrected review bytes and the final H0 checksum catalog are not yet retained or attestable.",
    "validate_h0.py review checking uses a PASS substring rather than an explicit overall verdict.",
    "Three unrelated untracked documentation paths must remain hash-pinned and excluded from staging.",
    "Strict evidence-ID mode retains 22 protected historical gaps."
  ],
  "noStagedFiles": true,
  "diffSummary": "No tracked or staged repository diff. Current untracked state consists of authorized H0 evidence plus three explicitly preserved and hash-pinned unrelated documentation files.",
  "reviewFindings": [
    "no blockers: corrected integration/control-plane evidence passes at the pre-checksum review phase",
    "medium: .pi/evidence/pi-harness-incubation/H0/validate_h0.py:382-391 - review-required mode accepts any PASS token instead of verifying the explicit overall verdict",
    "note: .pi/evidence/pi-harness-incubation/H0/H0-report.md:131-138 - final review references are forward-looking until corrected review artifacts are retained and checksummed"
  ],
  "manualNotes": "Verdict PASS for the corrected independent integration review only. Do not create H0-HC01 until all four explicit final PASS reviews are retained, the final checksum catalog is generated and verified, and review-required validation passes."
}
```
