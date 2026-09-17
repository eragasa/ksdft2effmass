# Task catalog clean cutover

## Authority and status

The exact superseding human instruction and exclusions are retained in
`harness/intake/task-catalog-configuration.md`. This is parent-only implementation
of `harness.task-catalog-configuration`, not independent review, human acceptance,
scientific validation, release or Git closeout. The selected cutover is software
verified within the checks below; broader inherited diagnostics remain failures.

Earlier planning and value/wire reports describe their historical slices. Their
schema-1 compatibility choice is superseded, not silently retained. The original
classification map and reference inventory remain pre-cutover observations, not
current directory-discovery contracts.

## Implemented boundary

- Source and resolved Harness configuration require schema 2 and a named
  `TaskCatalogConfiguration`; the flat constructor field and schema-1 readers are
  removed. Historical literal fixtures now establish explicit refusal.
- Pi configuration, resolution results and snapshot framing retain their separate
  version-1 contracts. Task records remain schema 3. List-valued status details
  remain a separate inactive Task.
- One private catalog reader supplies immutable actual-path/Task observations.
  Consumers reject missing roots, symlinks, root aliases/overlap, duplicate IDs,
  filename/identity disagreement and an empty combined catalog. Empty individual
  categories are valid. These checks do not eliminate concurrent filesystem races.
- Ordinary ingestion never rewrites `H5`, fabricates Task aliases, or discovers an
  ambient flat root. SQL projection retains actual paths and all Task fields.
- Derived control database schema 4 removes `task_alias` and adds
  `documentation_path`, preserving optional current Task metadata.
- Current ownership validation accepts schema 2 and explicit JSON Task paths only.
  Archived version-1 declarations and their schema are historical evidence, not
  accepted runtime inputs.

## Record preservation

The 217-row classification was checked against exact source SHA-256 identities and
absent destinations before relocation. All 217 Task files were renamed byte-for-byte:
20 research, 48 simulation and 149 software. The combined relationship graph passed
before the single configuration replacement; the empty old directory was retired.
No ID, lifecycle, relationship, category decision or scientific setting changed.
This was a guarded single-writer operation, not a global filesystem transaction.

The six old `harness-simplification.agents.*` ownership declarations have no matching
canonical Task among the 217 records. The initial ownership conversion preflight
stopped before changing any declaration when this gap was detected. No replacement
Tasks or authority were invented. Their original bytes were initially retained under
`harness/archive/task-ownership/`. After confirming they had no current operational
use, the human instructed "then remove them". Those six files were subsequently
removed; their former paths and hashes remain in `task-catalog-cutover-records.json`.
Other archived files and historical reports were not removed. The current Quantum
ESPRESSO integration ownership
record instead received its exact new Task path. Signed/checksummed historical
evidence and archived-source identities were not rewritten.

Subsequent progress edits to the selected Task are distinct from byte-preserving
relocation. The status-details Task stays inactive and automatic successor activation
stays disabled. No staging, commit, push, dependency change or scientific execution
was performed.

## Software verification and corrections

- Pre-switch current-format configuration and catalog integration: **79 passed**.
- The first broad post-switch Harness/ownership run: **864 passed, seven failed**.
  Failures identified old fixture directory scans, stale live skill references,
  an incomplete static dependency-owner list, and insufficient CLI scratch inputs.
  These were corrected without weakening assertions. A subsequent 870-pass run
  exposed the changed skill's stale declared digest; its current source inventory
  was refreshed. Failed attempts remain retained, not represented as passes.
- Final full Python regression: **4,714 passed, three unchanged external-QEXSD
  skips, 90.57 seconds**. The skips require external 7.2/7.5 reference artifacts;
  they establish no external scientific validation.
- Separate ownership suite: **37 passed**. The migrated current ownership manifest
  also passes its maintained CLI preflight, without granting execution authority.
- Explicit Task-catalog conformance: **six modules / 33 evidence owners, PASS**.
  The existing configuration test module now has one cohesive collected owner.
- Ruff: **28 affected Python files, PASS**. Strict mypy: **19 configuration,
  consumer and focused-evidence files, PASS**. A broader 28-file diagnostic still
  reports three inherited errors in unchanged methods of
  `test__projection_synchronizer.py`: one `no-any-return` and two `attr-defined`
  findings. Their function ASTs match the operation baseline; that baseline matches
  HEAD. They are not newly introduced errors and are not relabeled PASS.
- Broader compiler conformance remains **FAIL: five inherited findings** in the
  unchanged `test__HarnessCompiler.py` and `test__HarnessRepositoryLoader.py`
  modules (two naming and three hidden-loop findings). No waiver is claimed.
- Sphinx dummy and HTML builds passed with warnings as errors. Generated build
  trees are removed; logs are retained.
- Final maintained projection sync/check, Harness validation and exact selected-Task
  inspection pass. `git diff --check` passes and the index remains empty.
- Cutover preservation passed before the subsequent authorized orphan removal:
  216 Task files remain byte-identical after the selected
  Task's explicit progress update; all 217 retain their original lifecycle and
  relationships. All 200 baseline retained evidence/archive/checkpoint files tested
  remain unchanged. At that check, the six moved ownership records retained exact bytes;
  no unrelated baseline files changed. Selection and inactive status-details state
  are unchanged.
- The configuration snapshot oracle changed because its configuration bytes changed,
  not because the framing algorithm changed. The retained literal frame is
  `python/tests/software_verification/ksdft2effmass/harness/resources/configuration-project-v2-snapshot-frame.bin`.
  Its three independently assembled canonical parts have lengths 1410, 247 and 229;
  OpenSSL independently gives SHA-256
  `da9a7d33e2ca8a4a588d30d1466517dd94b530393869dcd4bf81000a880c2c60`.
- The static local dependency check now includes the accepted generic configuration
  owner, because the catalog reader shares its path policy. The prohibition on
  traversal beyond Harness and on reverse generic-to-local imports is unchanged.

Operation logs and pre-change identities are retained at
`/var/folders/42/g1m9r43x2_v4bkyg4csrsn100000gn/T/task-catalog-clean-cutover.eg6ihl9h/`.
They include the original Task tarball, relocation preservation observations,
ownership migration identities and failed/corrected check logs. These are local
operation artifacts, not a reviewed release archive.

## Parent adversarial assessment and limits

**ReviewOutcome: NO_BLOCKING_FINDINGS** for this selected migration.
**OperatorRequest: NONE** for further implementation within this boundary. This is
parent self-assessment, not independent review or human acceptance.

The assessment challenged identity rewriting, cross-catalog duplicate shadowing,
path confinement and aliases, silent fallback, lost SQL metadata, orphan record
conversion, and accidental lifecycle/authority changes. Targeted counterexamples
and preservation checks cover those represented boundaries. Historical citations
in decision/evidence records deliberately keep their original paths and hashes;
the retained classification map provides the old-to-new location correspondence.
Current documentation and skill references use the new locations.

**FindingDisposition: SAFE_TO_DEFER** for the five inherited compiler-conformance
findings, the three inherited test-helper typing findings, and separately scoped
filesystem race hardening. Existing wider callable/typing migration debt is not
claimed resolved. These limits do not create a compatibility fallback or waive any
scientific, protected-execution or human-acceptance requirement.

The selected Task remains active with the software result recorded; no successor,
status-details implementation, independent reviewer, staging or Git operation is
activated by this report.
