# H0 inventory-completeness review

**Result: FAIL**

H0 is not yet adequate to enter `H0-HC01`. This verdict concerns inventory/control-plane evidence only; it is not human acceptance and says nothing about future implementation correctness.

## Review

- **Correct:** The authoritative state is coherent: `.pi/chains/pi-harness-incubation.chain.json` keeps H0 as the sole active read-only task and H1--H5 blocked, while `.pi/chains/backend-neutral-kohn-sham-qe.chain.json` keeps P2--P11 blocked. The four prospective implementation/resource roots remain absent.
- **Correct:** The inventory schema requires every documented component field, makes classification and authority scalar enums, and rejects unknown component fields (`.pi/evidence/pi-harness-incubation/H0/component-inventory.schema.json:20-68`). The retained instance has 149 unique lexically ordered IDs; all per-record string-array fields checked by the validator are ordered. Classification totals are 27 `SPLIT_GENERIC_AND_LOCAL`, 110 `KEEP_PROJECT_LOCAL`, and 12 `DEFER`; authority totals are 82 authoritative, 42 historical, 20 advisory, 1 derived, and 4 unresolved.
- **Correct:** The capability matrix accounts for all 149 inventory IDs exactly once and reports 12 capability rows. The dependency map has all 149 nodes, 73 uniquely keyed edges, and consumer entries for all 27 split/extraction candidates. No candidate is classified wholesale `EXTRACTABLE`, which is consistent with the retained project/path coupling evidence.
- **Correct:** The retained H1 proposal stays bounded to demonstrated records and stateless validation actions and explicitly excludes orchestration, external/Git mutation, scientific interfaces, package publication, and implicit repository discovery (`.pi/evidence/pi-harness-incubation/H0/proposed-H1-contract.md:1-73`). Finding resolutions remain recommendations requiring human judgment rather than implemented decisions.
- **Blocker:** The required H0 checksum catalog is absent. The original task requires “deterministic inventory validator and checksums” (`.pi/tasks/pi-harness-incubation-H0-inventory.md`, Required outputs), but the retained H0 directory has no `checksums.sha256`. The validation record explicitly says only pre-existing catalogs were checked “before H0 checksum creation” (`.pi/evidence/pi-harness-incubation/H0/validation-results.json:141-145`), while the report nevertheless calls the inventory complete (`H0-report.md:3-5`). The evidence set therefore lacks a retained identity/integrity boundary and is not checkpoint-ready.
- **Blocker:** The leakage audit is incomplete by construction. It reports 122 occurrences across 19 files (`leakage-audit.json:4-52`), but there are 27 split/extraction candidates. `expected_leakage()` silently excludes directories and every file whose suffix is not `.md`, `.py`, or `.json` (`validate_h0.py:263-276`). This omits the split candidate `POL-002` (`docs/development/agent-control-plane.rst`), four split checksum catalogs, and the three split fixture families (`CHK-F001`, `OWN-006`, `OWN-007`). A read-only reproduction over those omitted candidate resources found 412 additional matching line/term records, including project paths in `docs/development/agent-control-plane.rst:14-16,20-26,37-45,75-76`, fixture-local `.pi/` paths, and extensive project/task/path identities in the checksum catalogs. Thus the validator proves only agreement with its narrowed scan, not complete candidate leakage screening.
- **High:** Exact component accounting is not defensible at the retained mixed granularity. Individual artifacts and their containing directory families are simultaneously counted—for example EVD-001 through EVD-007 are files under EVD-008’s whole `.pi/evidence/backend-neutral-cpn-P0-preflight/` family—while other directory families collapse many files into one component (OWN-006 covers 3 fixture files, OWN-007 covers 11, TST-002 covers 33 non-cache files, and TST-010 covers 25). The schema has no record-family membership or exclusion field (`component-inventory.schema.json:20-68`), and the validator checks only ID/count/path existence (`validate_h0.py:125-156`). Consequently, “149 components” is a count of heterogeneous rows with overlapping path coverage, not an exact, non-overlapping accounting of instantiated components.
- **High:** The source-of-truth map does not account for the complete inventory. It assigns only 108 of 149 IDs. The 41 unassigned IDs are all 36 task records, `TST-001`, and the four prospective roots. This is especially inconsistent with the `task_chain_and_live_authorization_state` row, whose boundary says tasks own scope but whose `current_components` contains only CHN-001--CHN-004 (`source-of-truth-map.json:34-40`). `validate_source_map()` checks unknown IDs and duplicate assignment but never requires coverage (`validate_h0.py:192-219`). The report’s source-of-truth claim at `H0-report.md:83-94` is therefore not supported by exact owner cardinality.
- **High:** The inventory’s declared direct dependencies are not reconciled with the dependency map. Twenty-one inventory rows declare direct dependencies: all 11 checkpoint instances depend on CHK-S001 (example `component-inventory.json:273-307`), all nine harness architecture pages depend on POL-001, and POL-002 depends on POL-001. None of those declared relations appears as a corresponding dependency-map edge. Conversely, the map contains many material relations absent from the inventory `direct_dependencies` fields. `validate_dependencies()` verifies only node membership, edge-key uniqueness, candidate consumers, and five prohibited directions (`validate_h0.py:222-260`); it never compares the two dependency representations. The 73-edge “dependency consistency” claim in `H0-report.md:140-142` is therefore overstated.
- **Medium:** The command/environment manifest is not a complete reproducibility manifest. Its `commands_planned` array contains descriptive labels rather than exact argv (`command-environment-manifest.json:4-12`), omits several commands later asserted in `validation-results.json:80-158` (strict evidence audit, P1 ownership/documentation/artifact replay, and Ruff), and does not bind inputs or outputs by digest. Exact command strings in the separate validation-results file partly mitigate this, but the retained command manifest itself is incomplete.
- **Note:** `validate_h0.py` passed in its default mode, but that result does not exercise `--require-checkpoint` or `--require-reviews`, and the defects above are outside its present assertions. A passing validator is therefore not sufficient for checkpoint readiness.
- **Note:** The requested repository-root `plan.md` and `progress.md` do not exist, so they could not provide additional scope or completion evidence. No repository files were edited.

## Commands

- `git status --short --branch`; `find .pi/evidence/pi-harness-incubation/H0 -type f -print | sort`; control-record discovery — completed read-only.
- `PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py` — **PASS**: 149 components; default checkpoint/review requirements false.
- `jq`/Python read-only accounting of inventory, capability matrix, source map, dependency map, classification/authority/kind cardinalities, ordering, family coverage, and candidate consumers — completed; found 108/149 source-map assignment and mixed/overlapping family granularity.
- Read-only leakage reproduction across every split/extraction candidate resource, including `.rst`, checksum catalogs, and directory descendants — completed; found 412 line/term records omitted by the retained 122-record audit.
- `git status --short` after inspection — no staged files and no review-caused repository changes; pre-existing untracked H0 evidence and `docs/papers/ksdft2efffmas.P03.md` remain.

## Residual risks

- This review did not independently rerun every historical command claimed in `validation-results.json`; it directly ran the requested H0 validator and audited the retained inventory evidence.
- Checksums and the final review/checkpoint set do not yet exist, so evidence identity and final `--require-reviews --require-checkpoint` closeout cannot be assessed.
- The 412 omitted leakage matches are lexical screening signals, not 412 semantic defects; each still needs a recorded semantic disposition under the audit’s own stated method.
- No scientific validation, uncertainty quantification, or implementation validation is implied or applicable to this H0 inventory preflight.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete blocker/high/medium findings cite the H0 task and retained evidence paths/lines; residual risks and commands are recorded."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "PYTHONDONTWRITEBYTECODE=1 python .pi/evidence/pi-harness-incubation/H0/validate_h0.py",
      "result": "passed",
      "summary": "Default-mode validator reported 149 components and passed with checkpoint_required=false and reviews_required=false."
    },
    {
      "command": "Read-only jq/Python inventory, source-owner, dependency, family-granularity, and leakage accounting",
      "result": "passed",
      "summary": "Reproduced retained counts and identified 41 source-map omissions, unreconciled direct dependencies, overlapping family granularity, and 412 leakage records outside the validator's narrowed scan."
    },
    {
      "command": "git status --short --branch and retained-file/control-record discovery",
      "result": "passed",
      "summary": "Confirmed dev state, no staged files, authoritative blocked chains, absent prospective roots, and absent H0 checksum catalog."
    }
  ],
  "validationOutput": [
    "h0_inventory_validation=passed; components=149; checkpoint_required=False; reviews_required=False",
    "Independent review result=FAIL: retained evidence is not adequate for H0-HC01 until completeness defects are corrected."
  ],
  "residualRisks": [
    "Historical gates in validation-results.json were inspected but not all independently rerun.",
    "Final checksums, review set, checkpoint record, and closeout-mode validation are not yet available.",
    "Omitted leakage matches require semantic review; lexical presence alone does not determine classification."
  ],
  "noStagedFiles": true,
  "diffSummary": "Read-only review; no repository diff was created.",
  "reviewFindings": [
    "blocker: .pi/tasks/pi-harness-incubation-H0-inventory.md Required outputs / H0 evidence directory - required H0 checksums are absent",
    "blocker: .pi/evidence/pi-harness-incubation/H0/validate_h0.py:263-276 - leakage validation excludes .rst, checksum files, and candidate directory descendants",
    "high: .pi/evidence/pi-harness-incubation/H0/component-inventory.json - mixed overlapping file/family granularity prevents exact 149-component accounting",
    "high: .pi/evidence/pi-harness-incubation/H0/source-of-truth-map.json:34-40 - 41 inventory IDs have no source-owner assignment",
    "high: .pi/evidence/pi-harness-incubation/H0/validate_h0.py:222-260 - dependency map is not reconciled with inventory direct_dependencies",
    "medium: .pi/evidence/pi-harness-incubation/H0/command-environment-manifest.json:4-12 - planned command labels are not a complete exact command manifest"
  ],
  "manualNotes": "PASS here would mean checkpoint adequacy only, not human acceptance or implementation correctness; the review result is FAIL."
}
```
