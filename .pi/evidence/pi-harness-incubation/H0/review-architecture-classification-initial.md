# H0 independent architecture and extraction review

## Review

**Result: FAIL**

The proposed generic/local architecture is directionally sound, but the retained evidence contains two material contradictions/gate defects that should be corrected before `H0-HC01` is presented as a technically passing inventory.

### Correct

- **Classification is generally conservative.** `component-inventory.json` assigns no component `EXTRACTABLE` or `RETIRE_AS_DUPLICATE`; it uses 27 `SPLIT_GENERIC_AND_LOCAL`, 110 `KEEP_PROJECT_LOCAL`, and 12 `DEFER`. The report explicitly avoids equating reuse potential with wholesale extraction (`.pi/evidence/pi-harness-incubation/H0/H0-report.md:24-34`).
- **The generic/local dependency boundary is appropriate.** Caller-supplied roots and profiles, generic-to-local/domain import prohibitions, path confinement, and rejection of implicit `.pi`, CWD, and Git-root discovery are consistent across `docs/harness/ksdft2effmass.harness.01.md:53-88`, `.03.md:19-72`, `proposed-H1-contract.md:53-57`, and `dependency-map.json#/prohibited_future_directions`.
- **H3-before-H2 is the safer sequence.** The recommendation is supported by resource/profile identities being inputs to H2 and by the shared-worktree sequential-writer rule. It is correctly presented as a pending protected recommendation rather than an already-authorized chain change (`open-finding-resolutions.md:41-51`).
- **Future ownership is properly harness-specific.** The evidence does not widen operator/CPN agents or assume ambient discovery. It calls for H2/H3-specific roles, version-2 manifests, exact paths, completion validators, and independent review (`open-finding-resolutions.md:53-63`; `H0-report.md:96-105`).
- **The minimum H1 model follows DataObject/ActionObject/ResultObject ownership.** Immutable/versioned records, stateless actions, explicit results, externalized I/O, and no abstract base-class or orchestration requirement align with `.pi/skills/design-data-action-objects/references/data-action-architecture.md:1-43`. The separate public-contract, wire, profile, resource, skill, adapter, and package versions are explicit (`proposed-H1-contract.md:39-51`), as are malformed-input versus internal-failure boundaries and Rust-portable fixed records (`proposed-H1-contract.md:3-37`).
- **Exclusions are well bounded.** H1 excludes dispatch/orchestration, subprocess/Git mutation, package publication, scientific CPN/domain APIs, automatic discovery, Graphify, scientific validation/UQ types, and numerical-verification APIs absent a numerical algorithm (`proposed-H1-contract.md:59-73`).

### Blocker

- **High — Graphify has contradictory classification and future ownership.** `component-inventory.json#/components/SKL-002` and `#/components/SKL-009` classify the Graphify entry/query resources as `SPLIT_GENERIC_AND_LOCAL` and propose destinations under `harness/pi`/`harness/local`. In contrast, `source-of-truth-map.json#/capabilities/graphify_optional_integration` assigns the capability to `existing project-domain source` and says not to copy it into harness resources; the minimum H1 contract also excludes Graphify (`proposed-H1-contract.md:59-73`). These cannot simultaneously be the accepted classification, destination, and unique future authority. Resolve conservatively—most likely by deferring the whole Graphify closure—or explicitly change the proposed source owner/scope before the human checkpoint.

- **High — the nonmutation gate does not inspect untracked paths, so it cannot support its recorded protected-path claim.** `validate_h0.py` obtains changed paths solely with `git diff --name-only BASE_COMMIT` in `git_paths()` and checks that list in `validate_nonmutation()`; Git does not include untracked files in that output. Current `git status --short` reports both the expected untracked H0 evidence directory and an untracked protected-documentation path, `docs/papers/ksdft2efffmas.P03.md`, while `validation-results.json#/nonmutation/docs_or_skills_changed` says `false` and the report claims protected-path nonmutation (`H0-report.md:140-148`). This does not establish that H0 created the documentation file, but it proves the gate cannot detect or account for such state. The validator must compare an explicitly captured initial untracked inventory or otherwise account for untracked protected paths before its nonmutation result is relied upon.

### Note

- **Medium — source-of-truth completeness is not validated.** `validate_source_map()` enforces unique capability names, allowed owners, known component IDs, and no component assigned twice, but never requires relevant inventory components to be assigned. At least `TST-001` (`python/pyproject.toml`, the current pytest/VVUQ configuration) is absent from `source-of-truth-map.json`, despite the map assigning adjacent documentation, evidence-grammar, and domain-test capabilities. The four prospective paths are also absent, though their omission is more defensible while unresolved. Thus uniqueness is checked only for rows that happen to be present, not for the required boundary as a whole.
- **Medium — dependency-map completeness is not validated against the inventory.** `validate_dependencies()` checks node identity, edge referential integrity, candidate accounting, and an exact prohibited-direction set, but it does not compare `dependency-map.json#/edges` with each component's `direct_dependencies`, consumers, or declared skill references. For example, the evidence identifies `SKL-012` (`resolve-human-checkpoint`) as a checkpoint-control consumer, but the edge list does not relate it to `CHK-S001`/`CHK-T001`. The current gate therefore proves consistency of listed edges, not completeness of the required dependency/consumer map.
- **Low — maintained prospective documents remain stale by design until a decision.** The architecture index still renders H2 before H3 (`docs/harness/ksdft2effmass.harness.00.md:42-57`), `.04` proposes a new `write-research-evidence-tests` skill (`docs/harness/ksdft2effmass.harness.04.md:19-63`), and `.05` treats `boundary` as a primary ownership/function surface (`docs/harness/ksdft2effmass.harness.05.md:16-59,88-125`). H0 correctly recommends H3-before-H2, reuse of `document-research-python`, and boundary-as-artifact-relation metadata. These pages are advisory, so this is not a present authorization conflict, but H1 must reconcile them after the human decision rather than allowing dual editable rules.
- **Input availability —** the requested repository-root `plan.md` and `progress.md` were absent (`ENOENT`). The original H0 task, chain, structured evidence, architecture pages, skill references, validators, and schemas were available and inspected.

## Residual risks

- Exact public names, serialized fields, compatibility behavior, issue-code namespace/order, and checkpoint durability/replay fields remain protected H1 decisions, as the evidence acknowledges.
- Strict evidence-ID validation still has 22 protected historical operator-test warnings; this is retained debt, not evidence of scientific or H0 architectural validity.
- H2/H3 chain order and task prose still permit sibling/concurrent interpretation until an accepted checkpoint durably revises the schedule.
- No scientific validation, UQ, numerical verification, external execution, or package extraction was performed; none is applicable to this H0 architecture review.

## Inspection summary

Inspected the H0 task/chain and all retained H0 JSON/Markdown evidence; `docs/harness` pages `.00`-`.08`; repository skill entries/references; DataObject/ActionObject architecture; checkpoint schema/validator; ownership v1/v2 and evidence-branch schemas; ownership validator surface/tests inventory; and current Git state. This was read-only with respect to the reviewed repository; only this required review artifact was written.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete high/medium/low findings cite H0 evidence paths, component IDs/JSON pointers, validator functions, and documentation line ranges; residual risks are listed separately."
    }
  ],
  "changedFiles": [
    ".pi-subagents/artifacts/outputs/d4578aed/.pi/evidence/pi-harness-incubation/H0/review-architecture-classification.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "git status --short --branch; find H0 evidence and docs/harness files",
      "result": "passed",
      "summary": "Confirmed dev branch, enumerated retained evidence/pages, and observed untracked H0 evidence plus docs/papers/ksdft2efffmas.P03.md."
    },
    {
      "command": "jq inventory/classification, source-map, dependency-map, capability-matrix, and validation-result inspections",
      "result": "passed",
      "summary": "Confirmed 149-component accounting and exposed the Graphify classification/source-owner contradiction and map-coverage limitations."
    },
    {
      "command": "H0 deterministic validator/test suite",
      "result": "not-run",
      "summary": "This reviewer inspected retained validation results and validator implementation but did not rerun the full suite."
    }
  ],
  "validationOutput": [
    "Review verdict: FAIL",
    "Two high-severity blockers: contradictory Graphify classification/source ownership; nonmutation validator omits untracked files.",
    "Two medium validator-completeness findings: source-map coverage and dependency-edge coverage are not enforced."
  ],
  "residualRisks": [
    "H1 protected API/version/failure details remain undecided.",
    "22 known strict evidence-ID warnings remain in protected historical operator tests.",
    "Prospective docs and authoritative schedule remain unreconciled pending checkpoint acceptance."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added only the required independent read-only review artifact; no reviewed repository implementation or evidence was edited.",
  "reviewFindings": [
    "blocker: component-inventory.json SKL-002/SKL-009 and source-of-truth-map.json graphify_optional_integration - contradictory Graphify classification, destination, and future authority",
    "blocker: .pi/evidence/pi-harness-incubation/H0/validate_h0.py git_paths()/validate_nonmutation() - untracked protected paths are invisible to the claimed nonmutation gate",
    "medium: validate_h0.py validate_source_map() - uniqueness is checked only for present rows; relevant inventory coverage is not enforced",
    "medium: validate_h0.py validate_dependencies() - listed edge consistency is checked, but completeness against declared dependencies/consumers is not"
  ],
  "manualNotes": "The requested plan.md and progress.md were absent. The architecture is otherwise conservative and well bounded, but the blockers should be resolved before H0-HC01 technical PASS."
}
```
