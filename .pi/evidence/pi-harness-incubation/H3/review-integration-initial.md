# H3 independent integration/control-plane review

## Finding

**Major — project-specific task/control-plane data leaks into the generic layer, and the leakage gate cannot detect it.**

- The accepted boundary says project task IDs belong under `harness/local/`, and explicitly prohibits `generic resources → project task IDs` and `generic validators → implicit .pi discovery` (`docs/harness/ksdft2effmass.harness.01.md:43-45,74-84`). It further states that generic resources may not embed local task IDs (`docs/harness/ksdft2effmass.harness.02.md:165-168`).
- Nevertheless, the generic fixture `harness/pi/fixtures/canonical/canonical-json-vectors.json:4-6` embeds the local successor name `H2 Python`.
- The validator installed in the generic tree derives the repository root and directly discovers project-local resources and H3 `.pi` state (`harness/pi/validation/validate_h3_resources.py:24-27`). Its ownership/control check hard-codes H3, the project task record, project chain, evidence path, and active-task state (`harness/pi/validation/validate_h3_resources.py:574-589`). This is precisely the prohibited implicit `.pi`/local coupling rather than an explicit caller-supplied profile/path boundary.
- The reported leakage PASS is therefore not reliable: `leakage_gate()` scans only the generic manifest, schemas, skills, and docs (`harness/pi/validation/validate_h3_resources.py:537-559`), omitting both `harness/pi/fixtures/` and `harness/pi/validation/`, where the leakage occurs.

This violates H3's objective in `.pi/tasks/pi-harness-incubation-H3-resources.md` and the accepted H1 package boundary. It requires correction before H3 can be presented for acceptance.

## Control-plane and integration checks

- **Prerequisites/activation:** PASS. Resolved `H0-HC01`, `H1-HC02`, and `POLICY-CONSTITUTION-1-HC01` retain human-accepted PASS decisions. `activation.json` records zero unresolved checkpoints before activation and the separate H3-only authorization. Checkpoint dry-run passed all four dry-run gates, validated 16 records, and reported `unresolved_checkpoints=0`.
- **Starting identity:** PASS. `HEAD`, `dev`, and `origin/dev` all equal `49ffe047411468cba68379c5c69b1a44b19af7de`, matching `.pi/evidence/pi-harness-incubation/H3/activation.json` and `validation-results.json`.
- **Sole active task / H2 inactive:** PASS. `.pi/chains/pi-harness-incubation.chain.json` names only H3 as active; H2 is blocked behind `H3:human_accepted`. `.pi/tasks/pi-harness-incubation-H3-resources.md` and `h3-to-h2-handoff.json` consistently state that H2 remains inactive and separately authorized.
- **Ownership:** PASS. `python .pi/task-ownership/validate_task_ownership.py --task H3 --chain .pi/chains/pi-harness-incubation.chain.json` passed. The version-2 manifest has 12 exact writer scopes with no equal, ancestor, or descendant overlap; reviewer roles have no write scopes. Generic, local, fixture, validator, docs, and evidence ownership are separated in `.pi/evidence/pi-harness-incubation/H3/task-ownership.json`.
- **Artifacts and closure:** PASS apart from the leakage finding. Generic/local manifests, profile, skill and direct reference, public schemas, valid/invalid fixtures, resolution/diagnostic/evidence oracles, documentation, validator, and pre-review evidence/handoff artifacts exist. Manifest byte identities, declared coverage, dependency closure/cycles, profile binding, extension-only composition, schema identities, and fixtures passed the completion validator.
- **Dependency direction:** The manifest graph itself is correct: `harness/local/resource-manifest.json` extends and depends on generic identities, while `harness/pi/resource-manifest.json` contains no local identity dependency. Resolution fixtures cover reverse-edge rejection. The file-level generic leakage above still defeats the broader boundary.
- **Validator behavior:** The normal run returned `H3 VALIDATION PASS; gates_passed=46 defects=0`. A disposable-copy mutation of the generic skill bytes returned exit code 1 and reported the SHA-256 mismatch, confirming fail-closed exit behavior for content drift. Resolution oracles cover missing resources/dependencies, duplicates, cycles, overlays, incompatible versions, case mismatch, escape, symlink, non-file, and hash mismatch. However, the leakage gate's incomplete scan is a substantive fail-open gap.
- **Unrelated work:** PASS. All five paths in `unrelated-worktree-baseline.json` retain their recorded SHA-256 values. No staged files exist. Their pre-existing modified/untracked statuses remain outside H3 ownership.
- **Forbidden scope:** PASS. Git checks show no changes to `python/src`, dependency declarations, or lockfiles; no harness Python implementation exists under `python/`; no live `.agents/skills` retirement/cutover is present; no protected, scientific, external, publication, or release execution is claimed.
- **H3-to-H2 handoff:** Structurally complete as a pre-review candidate. `h3-to-h2-handoff.json` identifies the manifests, profile, validator, canonical vectors, DiagnosticPath obligations, revision/preservation state, and explicit acceptance/activation conditions. `acceptance-index.json` correctly leaves human acceptance false, review artifacts empty, and checksums unfinalized. H2 remains blocked. This review does not accept H3 or activate H2.

## Commands run

- `python harness/pi/validation/validate_h3_resources.py` — nominal PASS, 46 gates, 0 defects.
- `python .pi/checkpoints/validate_checkpoints.py --dry-run` — PASS, 0 unresolved checkpoints.
- `python .pi/task-ownership/validate_task_ownership.py --task H3 --chain .pi/chains/pi-harness-incubation.chain.json` — PASS.
- `git status`, staged/unstaged/untracked listings, revision comparisons, baseline SHA-256 checks, dependency/lock and Python-harness searches — results summarized above.
- Disposable-copy manifest-content mutation replay — validator exited 1 as expected; the repository was not mutated.

## Limitations

This was read-only with respect to repository state. No future H2 Python/Rust implementation was run, and no scientific, numerical, external, or protected execution was performed. The review establishes software/control-plane observations only, not scientific validity or human acceptance.

Review status: FAIL
