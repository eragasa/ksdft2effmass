# H0 integration/control-plane review

## Verdict: FAIL

The structured H0 inventory and current control-plane state pass their available deterministic gates, but H0 is not ready for checkpoint creation. The nonmutation gate omits untracked files, an untracked documentation file is present despite the recorded clean H0 starting worktree, and the required H0 review/checksum set is not yet retained.

## Review

### Correct

- **Structured evidence is actually inspected.** `.pi/evidence/pi-harness-incubation/H0/validate_h0.py` validates the component inventory against its Draft 2020-12 schema, accounts for every component in the capability matrix, checks future-owner uniqueness, checks dependency nodes/candidates/prohibited directions, reproduces the leakage occurrence list, and asserts control-plane state. It passed with 149 components: 27 `SPLIT_GENERIC_AND_LOCAL`, 110 `KEEP_PROJECT_LOCAL`, and 12 `DEFER`.
- **Current state is correct for the precheckpoint phase.** `.pi/chains/pi-harness-incubation.chain.json` keeps H0 as the sole active task with no pending checkpoint; H1--H5 are blocked. `.pi/chains/backend-neutral-kohn-sham-qe.chain.json` has no active task and keeps P2--P11 blocked. This is the required precheckpoint state; `H0-HC01` has not been created prematurely.
- **The exact P2 gate agrees everywhere inspected.** The harness chain, backend-neutral chain, and `.pi/tasks/backend-neutral-cpn-P2-tools-provenance.md` require exactly `P1:human_accepted`, `H5:human_accepted`, and `explicit_activation:P2`; accepted H5 cannot auto-launch P2.
- **P1 authority is durable and resolved.** `.pi/checkpoints/P1-HC01-cpn-numeric-wire-contract.json`, `P1-HC02-u64-expression-routing.json`, and `P1-HC03-final-acceptance.json` are resolved, and the P1 task records human-accepted `PASS`. Checkpoint validation found 13 records including fixtures, zero unresolved checkpoints, and zero duplicate decisions.
- **Prospective boundaries remain prospective.** None of `python/src/ksdft2effmass/harness/pi/`, `python/src/ksdft2effmass/harness/pi/local/`, `harness/pi/`, or `harness/local/` exists. `.pi/evidence/pi-harness-incubation/H0/H0-report.md` and `proposed-H1-contract.md` consistently describe recommendations rather than implemented capability. No capability overclaim was found in those H0 records.
- **Retained status findings were not silently edited.** `.pi/evidence/pi-harness-incubation/H0/duplication-and-overlap-analysis.md` retains stale live-status prose as a finding, while `open-finding-resolutions.md` carries all six protected recommendations to human decision. The H2/H3 sequencing recommendation is not applied to the blocked chain.
- **Dependencies and locks match the recorded baseline.** SHA-256 values are `5d6318812c7db69b7b1d5d742bbd9be903419a2c5bd702ed90a240a73d661f6c` for `python/pyproject.toml` and `186504b6dc24b054c15ef01ed3219c6829f83585a0d7c6a551d79ede37cb7368` for `python/uv.lock`.
- **Documentation integration remains bounded.** `docs/conf.py` includes only the exact harness glob, and `docs/index.rst` lists the index plus all eight hidden children. Sphinx warnings-as-errors passed to a temporary directory, which was removed.
- **Known evidence debt is represented honestly.** Warning-mode evidence audit passed with 22 known unowned protected operator tests; strict mode exited 1 as expected. `.pi/evidence/pi-harness-incubation/H0/validation-results.json` does not misreport strict mode as passing.

### Blockers

1. **Blocker — H0 nonmutation validation does not inspect untracked files.**
   `.pi/evidence/pi-harness-incubation/H0/validate_h0.py` (`git_paths`, approximately lines 91--96; `validate_nonmutation`, approximately lines 385--407) uses `git diff --name-only <base>`, which omits untracked files. Current `git status --short` reports `?? docs/papers/ksdft2efffmas.P03.md`, while `.pi/evidence/pi-harness-incubation/H0/command-environment-manifest.json` records an empty starting worktree near line 53. The validator nevertheless passes and `.pi/evidence/pi-harness-incubation/H0/validation-results.json` reports `docs_or_skills_changed: false`. Therefore the claimed protected-path nonmutation is not attested. Before checkpoint creation, provenance of this file must be established and the H0 validator must fail closed on nonignored untracked files outside the authorized H0 evidence/control paths (without deleting or rewriting unrelated user work).

2. **Blocker — required H0 reviews and checksum catalog are not retained yet, while the report says they are.**
   `.pi/tasks/pi-harness-incubation-H0-inventory.md` under “Required outputs” requires four independent reviews plus checksums. At inspection time, all of `review-inventory-completeness.md`, `review-architecture-classification.md`, `review-evidence-vvuq.md`, `review-integration-control-plane.md`, and `checksums.sha256` were absent from `.pi/evidence/pi-harness-incubation/H0/`. However `.pi/evidence/pi-harness-incubation/H0/H0-report.md` under “Review results” says the four review records are retained, and its scope language says the required evidence/checksums were created. Existing historical and initialization checksum catalogs pass, but they do not authenticate the H0 artifact set. Assemble the reviews, resolve any findings, generate a final H0 checksum catalog after the reviewed set is stable, and rerun validation with review/checkpoint requirements at the appropriate boundary. H0 must remain active and H1 blocked until then.

### Notes

- `plan.md` and `progress.md`, which the task asked the reviewer to read, do not exist at the repository root. The authoritative task/chain/checkpoint/evidence records were sufficient to perform this review, but the missing requested context should be noted by the parent.
- The tracked Git diff and staged diff are empty. The worktree contains the untracked H0 evidence directory and the unrelated-looking untracked documentation path above.
- The present H0 state correctly remains active precheckpoint with no `H0-HC01`. The checkpoint should be created only after the blockers are resolved and final reviews/checksums pass; its creation must then change H0 to blocked at the checkpoint without activating H1.

## Commands

- `PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py` — PASS; 149 components and all structural/state checks reported passing, subject to the untracked-file blind spot above.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/checkpoints/validate_checkpoints.py --include-fixtures --dry-run` — PASS; 13 records, 0 unresolved, 0 duplicate decisions.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/skills/validate_skill_capabilities.py` — PASS.
- `cd python && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q ../.pi/task-ownership/tests/test_validate_task_ownership.py` — PASS; 36 tests.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/skills/audit_evidence_identifiers.py --self-test` — PASS with 22 known warnings.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/skills/audit_evidence_identifiers.py --self-test --strict` — expected FAIL (exit 1) for the same 22 retained protected-test gaps.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/backend-neutral-cpn-P1-contract/validate_test_ownership.py` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/class-owned-evidence-convention/validate.py` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/backend-neutral-cpn-P1-contract/contract_gates.py` — PASS; 10 cases.
- `cd python && PYTHONDONTWRITEBYTECODE=1 uv run sphinx-build -W -q ../docs <temporary>/html` — PASS; temporary output removed.
- `sha256sum -c` for all existing task catalogs plus initialization — PASS; no H0 catalog exists.
- `cd python && uv run ruff check ../.pi/evidence/pi-harness-incubation/H0/validate_h0.py` — PASS.
- `git diff --check` — PASS.
- `git status --short --branch`, prospective-path checks, and dependency hashes — inspection completed; tracked/staged diff empty, four prospective paths absent, untracked documentation file present.

## Residual risks

- The 22 strict evidence-ID gaps remain protected historical/operator debt; warning-mode success must not be promoted to strict conformance.
- Structured inventory validation establishes accounting consistency, not semantic correctness of every classification or future H1 contract decision.
- Stale status prose remains intentionally retained until an authorized later documentation correction.
- Passing Sphinx and control-plane validators establishes software/documentation consistency only, not scientific validation, UQ, extraction readiness, package readiness, or human acceptance.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete blocker and residual-risk findings cite H0 validator, report, task, command manifest, chains, and current Git status."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py",
      "result": "passed",
      "summary": "149-component structural inventory/state validation passed, but omits untracked files."
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/checkpoints/validate_checkpoints.py --include-fixtures --dry-run",
      "result": "passed",
      "summary": "13 records validated; zero unresolved or duplicate decisions."
    },
    {
      "command": "cd python && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q ../.pi/task-ownership/tests/test_validate_task_ownership.py",
      "result": "passed",
      "summary": "36 tests passed."
    },
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/skills/audit_evidence_identifiers.py --self-test --strict",
      "result": "failed",
      "summary": "Expected exit 1 from 22 retained protected operator-test ownership gaps."
    },
    {
      "command": "cd python && PYTHONDONTWRITEBYTECODE=1 uv run sphinx-build -W -q ../docs <temporary>/html",
      "result": "passed",
      "summary": "Warnings-as-errors documentation build passed; temporary output removed."
    },
    {
      "command": "sha256sum -c <existing evidence catalogs>",
      "result": "passed",
      "summary": "All existing task and initialization catalogs passed; H0 has no checksum catalog."
    },
    {
      "command": "git diff --check && git status --short --branch",
      "result": "passed",
      "summary": "Whitespace check passed; status exposed untracked H0 evidence and docs/papers/ksdft2efffmas.P03.md."
    }
  ],
  "validationOutput": [
    "H0 validator: 149 components; 27 split, 110 local, 12 deferred.",
    "Control state: H0 active precheckpoint; H1-H5 and P2-P11 blocked; no pending checkpoint.",
    "Exact P2 gate: accepted P1, accepted H5, and separate explicit activation.",
    "Sphinx -W passed to temporary output.",
    "Required H0 review/checksum files were absent at inspection."
  ],
  "residualRisks": [
    "22 protected operator tests remain strict evidence-ID debt.",
    "Inventory structural validity does not establish semantic correctness or human acceptance.",
    "Untracked docs/papers/ksdft2efffmas.P03.md is not covered by the H0 nonmutation gate."
  ],
  "noStagedFiles": true,
  "diffSummary": "No tracked or staged diff; untracked H0 evidence directory and untracked docs/papers/ksdft2efffmas.P03.md are present.",
  "reviewFindings": [
    "blocker: .pi/evidence/pi-harness-incubation/H0/validate_h0.py - nonmutation validation omits untracked files and therefore misses an untracked docs path.",
    "blocker: .pi/evidence/pi-harness-incubation/H0/ - required review files and H0 checksums.sha256 are absent while H0-report.md says reviews are retained."
  ],
  "manualNotes": "Verdict FAIL. Keep H0 active and H1-H5/P2-P11 blocked; do not create H0-HC01 until blockers are resolved and the complete reviewed artifact set is checksummed."
}
```
