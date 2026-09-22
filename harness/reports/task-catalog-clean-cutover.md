# Task catalog clean cutover

## Authority and status

The exact superseding human instruction and exclusions are retained in
`harness/intake/task-catalog-configuration.md`. The implementation and assessment
of `harness.task-catalog-configuration` were parent-only, not independent review.
The human subsequently accepted the software result and authorized administrative
closeout, as recorded below and in the intake. This establishes neither scientific
validation nor release. The selected cutover is software verified within the
checks below; broader inherited diagnostics remain failures.

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
was performed during the cutover operation. Subsequent Git operations and this
Task's separately authorized acceptance are distinguished below; they do not
rewrite the byte-preserving relocation observations.

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

At the implementation-report boundary, the selected Task remained active with the
software result recorded. This parent assessment did not grant human acceptance,
Git authority, independent review or successor activation.

## Human acceptance and administrative closeout

The implementation was subsequently committed and pushed as
`5d551e0ad5f238b92389d3448e7a367f18dae9d1`; `origin/dev` identity and a clean working
tree were verified. The fresh pre-commit regression had **4,714 passes, three
unchanged skips**, and **37 ownership-suite passes**. Harness/projection checks and
warning-as-error Sphinx dummy/HTML builds passed. Those operation logs are retained
locally at `/tmp/ksdft-commit-all.rzQPvN/`; generated Sphinx trees were removed.

The human then answered **yes** to the explicit recommendation to accept and
administratively close this Task, including commit/push without successor
activation. The intake preserves the question, verbatim answer and bounded
interpretation. The Task is now `closed_human_accepted_pass`; selection is cleared.
The status-details proposal remains inactive and automatic successor activation is
still disabled. The inherited diagnostics and scientific limitations above are
unchanged, not waived or relabeled PASS. The cutover audit retains its original
historical hashes rather than rewriting them to describe the later closed Task.

Closeout verification passed maintained projection synchronization/checking,
Harness validation and exact Task-state inspection (closed human-accepted status,
no selected Task, no findings). The affected Harness and ownership
software-verification suites passed **871 tests in 76.62 seconds**. Logs are
retained locally at `/tmp/ksdft-catalog-closeout.CmbIgN/`. The full regression and
Sphinx builds cited above were not repeated for this administrative-only change.
It changes no source, tests, scientific settings or other Task records.
Staged-diff/scope checks are required before the administrative Git boundary:
one non-amended commit pushed to the configured `origin/dev`, with exact
remote-identity verification. The containing commit supplies its identity rather
than a self-referential field in this report.
