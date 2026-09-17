# Configurable Task catalogs — bounded implementation plan

## Status, authority and evidence boundary

`harness.task-catalog-configuration` is active **for implementation**, following
planning activation, approval of the compatibility/classification choices and the
human continuation instruction “cotinue”, retained in
`harness/intake/task-catalog-configuration.md`. The parent applied adversarial
thinking directly: devil's advocate, assumption busting, source verification,
path-attack analysis and defensive design. This is **not independent review**.

This plan defines the bounded implementation under the public compatibility and
classification choices now approved in the intake by the human response
“these choices are approved and authorized”. It does not itself execute
implementation, move records, change runtime configuration, create scientific
evidence, grant execution authority or authorize commit/push. The selected design owner remains
`docs/architecture/v2/ksdft2effmass/harness/configuration.md`.

## 1. Inputs and bounded inventory

- Existing `HarnessConfiguration`, source/resolved serializers, resolver and
  `HarnessCatalogConfiguration` in `python/src/ksdft2effmass/harness/configuration.py`.
- Current `harness/configuration.json`: schema 1, flat `catalogs.task_root`.
- Accepted prerequisite `migration.v2.harness.configuration`.
- The initial 216 canonical Tasks were inspected through their objectives,
  declared Task kinds and completion requirements; mixed-purpose records received
  additional scope/status inspection. The later separately recorded software Task
  `harness.task-status-details` brings the refreshed map to 217 records.
- `task-catalog-classification.json`: one explicit proposed destination per Task,
  source identity, rationale and decision disposition. Totals are
  **20 research, 48 simulation, 149 software**; the five previously mixed-purpose
  destinations are human-confirmed. This is a planning inventory, not a runtime
  routing registry or executed migration command.
- `task-catalog-path-references.json`: bounded textual-reference inventory with
  file identities and line numbers. It separates runtime, tests, instructions,
  live records and retained history; string occurrence is not proof of live use.
  It excludes its own outputs and generated control storage. Dynamically composed
  paths and tools outside this repository are not proven covered by this scan.

Inventory hashes are observations, not migration authorization. Refresh changed
records and reconcile added/deleted Tasks before cutover. In particular, the
active Task and maintained planning/implementation documents legitimately change.
The observed consumer inventory below describes the pre-implementation baseline;
current slice status is in `task-catalog-configuration-implementation.md`.

## 2. Proposed public object contract

`TaskCatalogConfiguration` is a frozen, slotted DataObject with three required
fields, each an exact built-in `str` representing a normalized repository-relative
POSIX directory:

| Field | Proposed project value |
|---|---|
| `research_root` | `tasks/research` |
| `simulation_root` | `tasks/simulation` |
| `software_root` | `tasks/software` |

No defaults silently select project paths. Reject non-string values with TypeError;
reject empty, absolute, drive-prefixed, traversal, non-normalized, reserved-device,
control/surrogate-containing paths with ValueError under the existing portable
path contract. Reject equal or ancestor/descendant category roots by path
components, including conservative case-fold aliases; do not silently normalize
meaningful inputs. A sibling such as `tasks/research-extra` is not a descendant.
Filesystem existence, actual aliasing and symlink confinement remain I/O-owner
checks, not DataObject behavior.

Compose this object through `HarnessCatalogConfiguration`, not directly beside it
in another global configuration. Proposed compatible Python shape:

- retain the existing first four constructor arguments;
- allow `task_root: ResourcePath | None`;
- append `task_catalog: TaskCatalogConfiguration | None = None`;
- require exactly one of flat root and categorized configuration;
- preserve existing flat construction and equality/default semantics;
- retain the existing agent/checkpoint/skill roots and reject cross-catalog exact
  root collisions; add the three-root checks only to categorized mode.

The source/resolved aggregate owns agreement between its format version and the
selected catalog representation. The object contains no registry, repository,
callbacks, environment lookup, classifier, scientific settings or authority flags.

### Selected wire compatibility — implemented value/wire slice

**Human-selected: introduce explicit Harness configuration schema 2 for the
categorized layout while preserving schema-1 flat decoding and exact re-encoding.**
This concerns Harness configuration only: Task record schema 3, Pi settings schema,
WorkflowRun schema and scientific specifications remain unchanged.

Proposed schema-2 `catalogs` members, in canonical order:

```json
{
  "task_catalog": {
    "research_root": "tasks/research",
    "simulation_root": "tasks/simulation",
    "software_root": "tasks/software"
  },
  "agent_roots": [".pi/agents"],
  "checkpoint_roots": [".pi/checkpoints"],
  "skill_roots": [".agents/skills", ".pi/skills"]
}
```

This is an illustrative schema-2 fragment, now supported by the value and wire
APIs but **not yet by catalog consumers or the live repository configuration**.
Schema 1 continues to require its exact existing `task_root` member set. Schema 2
requires all three new roots and excludes `task_root`. Reject mixed layouts,
missing/extra members, duplicate JSON keys, wrong versions and incomplete values;
never infer a version from a directory or retry another catalog after failure.
Keep the current canonical encoding grammar and exact schema-1 byte oracles.
Source bindings/content identities remain exact; retain the snapshot-framing
algorithm's own version unless that algorithm changes. Do not globally relax the
shared version validator for unrelated resolution-result or Pi records.

The previously considered schema-2-only clean cutover would have rejected old
flat configurations and withdrawn their existing public read contract. The human
selected preservation instead; the clean-break alternative is not the implementation
target. Acceptance of that choice is not evidence that either format change has
already been implemented.

## 3. Consumer inventory and ownership

Paths below are under `python/src/ksdft2effmass/harness/` unless stated otherwise.

| Surface | Observed issue / planned change |
|---|---|
| `configuration.py` | Exact schema-1 member checking rejects an added section today. Extend concrete records and owned wire branches under the chosen compatibility contract. Remove affected module-level/erased boundary debt rather than adding more. |
| `__init__.py`; `docs/api/harness-control.rst` | Add the public configuration export and document its complete intrinsic and wire contract. |
| `pi/local/control/inputs.py` | Current discovery checks one root and `glob('*.json')`. Resolve the configured flat root or all three categorized roots explicitly. |
| `pi/local/validation.py` | `_task_check` also scans one root, and an empty scan can pass. Share catalog selection semantics with projection generation; require a nonempty total catalog, not a nonempty research category. |
| `pi/local/control/generation.py` | Pass the complete resolved catalog and identified sources to ingestion/projector, not one derived root or ambient default. Retain explicit isolated-test inputs only where still justified. |
| `pi/local/dbcontrol/ingestion.py` | Current code indexes by Task ID and synthesizes `<task_root>/<id>.json`. Detect duplicates before dictionary assignment and retain each actual root-relative source path. |
| `pi/local/dbcontrol/projections.py` | `render_all` currently reconstructs all paths below one root. Use and validate retained `task_definition.source_path`, not a guessed destination from ID prefixes. |
| `pi/local/control/verification.py` | Unexpected-owned-path checking must cover every configured category and reject unsafe reconstructed paths before any publisher operation. |
| `pi/local/task_ownership_validation.py` | Existing legacy compatibility requires a `harness/tasks/` prefix. Replace that assumption with exact configured catalog membership and matching Task identity; do not accept arbitrary JSON paths by suffix. |
| `.pi/task-ownership/{ownership-v2,evidence-branch-matrix}.schema.json` | Existing `task_record` patterns hard-code `harness/tasks/`. Permit safe relative JSON paths structurally; runtime validation must establish configured membership. Keep valid legacy bindings separately identifiable. |
| Task inspector/CLI | Keep exact caller-supplied Task paths; do not add ambient category discovery to `TaskStateInspector`. Update examples/live calls, not its bounded inspection responsibility. |
| Current instructions and docs | Review `.pi/task-ownership/README.md`, `.pi/skills/inspect-task-state/SKILL.md`, capability inventory and current control docs. If a mirrored/manifest-addressed resource changes, use its maintained refresh/validation owners. |

The control SQL schema already contains a unique `task_definition.source_path`.
A new category column or database schema version is **not justified merely to
remember source paths**. Categories come from exact configured parent directories;
Task IDs and graph relationships remain globally scoped.

Use one cohesive project-local catalog-read ActionObject where selection must be
shared by validation and generation. It returns a closed immutable sequence of
source-path/decoded-Task pairs, preserving exact identity/path association. Reuse
existing Task deserialization and graph validation; do not invent a second graph,
generic filesystem utility or new public Task model. Wire mechanics stay with
serializer owners, and intrinsic checks stay with their DataObjects. Existing
`object`, `Any`, dynamic field lookup and module-level helpers are migration debt,
not patterns for new or affected behavior.

## 4. Classification and history

The JSON classification inventory, not a filename-prefix rule, is the proposed
migration map. Classification changes location only, never scientific meaning,
Task status, prerequisites, scope, protected authority or evidence class.

Notable counterexamples to prefix classification:

- `quantumespresso.simulations.integration` belongs to software: its deliverable is
  an integration implementation, not a simulation result.
- `harness.telemetry.effectiveness-evaluation` and `.controlled-benchmarks` are
  proposed research: their declared deliverables are evidence interpretation and
  a controlled comparison protocol, not instrumentation.
- Declared calculation/extraction Tasks are proposed simulation; explicit physical
  validation, numerical comparison and analysis Tasks are proposed research.
- Historical uppercase IDs and superseded Tasks remain present with unchanged IDs
  and statuses. No prefix renaming, deletion or automatic activation follows.

The human confirmed the following five previously mixed-purpose rows:

| Task | Confirmed destination | Ambiguity considered before selection |
|---|---|---|
| `abinit.tutorials.basic2-h2-convergence` | simulation | Record allows software examples or separately authorized reproduction. |
| `abinit.tutorials.basic3-silicon` | simulation | Same mixed example/reproduction objective. |
| `abinit.tutorials.basic4-aluminum` | simulation | Same mixed example/reproduction objective. |
| `bulk-silicon.tight-binding.wannier.bridge` | software | Superseded, never-launched typed bridge contract; simulation protocol is another defensible classification. |
| `quantumespresso.simulations.review` | simulation | Campaign disposition/artifact review also informs reusable software behavior. |

Do not split or redefine these Tasks as a side effect of moving them. These five
classification questions are resolved. Any newly discovered unresolved row still
blocks complete cutover; refresh and reconcile the inventory before relocation.

Live references must be distinguished from historical quoted paths, immutable
source bindings, archive checksums and signed decision evidence. Do **not** apply
a repository-wide string replacement. An old signed/checksummed binding cannot be
rewritten and presented as original evidence. Where a live consumer needs to follow
an old path, use an explicitly reviewed old-path/new-path/Task-identity disposition;
never grant authority merely because a new record has a familiar filename.

## 5. Guarded cutover, not an atomic-filesystem claim

1. Freeze the exact working inputs, including uncommitted Task bytes; do not assume
   HEAD contains them. Reconcile this inventory against the then-current catalog.
2. Complete configuration, reader, ingestion, projection, validation and resource
   changes with isolated fixture coverage before changing canonical locations.
3. Finalize every classification and live/historical reference disposition. Reject
   existing target conflicts, ID/case aliases and unsafe paths before writes.
4. Quiesce catalog-writing/sync operations. Prepare destination records without
   overwriting an existing differing file; retain recoverable before-bytes and
   an explicit operation log. Unselected prepared copies are not a second
   authoritative catalog.
5. Verify ID/relationship/status/authority meaning and expected source bytes;
   enumerate any authorized live-path-only payload edits separately. Switch the
   one canonical configuration only when the complete target set is ready.
6. Retire the old live catalog only after successful target verification, then run
   maintained projection sync/check and validation. Keep historical artifacts and
   their original identity claims unchanged.
7. If interrupted, stop and report the observed partial state. No automatic source
   fallback, deletion, activation or continuation is allowed. Reconcile against
   the operation log; rollback restores exact before-state only within separately
   authorized mutation scope. Multiple file moves are not globally atomic.

No code implementing these steps runs in this planning phase. No publication,
Git history rewrite or calculation-data movement is included.

## 6. Verification plan

Use class-owned maintained tests with explicit semantic cases and independent
literal wire oracles; authored fixtures belong under the relevant test `resources/`.

- Configuration: exact fields/types, frozen state, portable paths, equality and
  ancestor overlap, case aliases, near-prefix siblings, missing/extra JSON fields,
  both/neither layout, unsupported versions and preserved schema-1 bytes if chosen.
- Catalog discovery: alternate unrelated root names, empty research category,
  nonempty total requirement, missing roots, malformed records, wrong filename/ID,
  duplicate IDs across roots, deterministic ordering, symlinked roots/files and
  escaped or aliased paths. Do not claim this proves race-free filesystem access.
- Graph/ownership: cross-category parent/prerequisite edges, repeated filenames
  with duplicate IDs, retained uppercase IDs, wrong-category source membership and
  old binding validation without weakening authority or exact Task identity.
- Projection: preserve source path through real ingestion and reconstruction;
  reject a stored traversal/unconfigured target, stale path metadata, missing or
  extra owned files and an attempted write outside configured roots. A successful
  parser round trip alone is not migration evidence.
- Cutover: controlled small fixtures with one record per category, mixed live and
  historical references, conflicts before writes and injected interruption at
  meaningful stages. Verify unchanged before-state or explicitly reported partial
  state; do not claim all-or-nothing multi-file durability without an actual design.
- Repository gates after authorized implementation: affected Ruff and strict mypy,
  explicit test-evidence conformance, focused then full pytest, Sphinx warnings as
  errors, maintained projection sync/check, Harness validation and exact Task
  inspection. Existing unrelated conformance debt stays explicit.

No new tests, test fixtures, source behavior or scientific execution were authored
or run as implementation evidence during this planning operation.

## 7. Adversarial self-assessment

**ReviewOutcome: NO_BLOCKING_FINDINGS**

**OperatorRequest: NONE**

The initial self-assessment was REVIEW_INCONCLUSIVE / DECISION_REQUIRED because
compatibility and five classifications were unresolved. The human has now selected
them; no bounded planning blocker remains. This is not an implementation review.
The subsequent continuation instruction authorizes implementation. This planning
assessment does not establish completion; the implementation report records the
bounded value/wire slice and pending consumer/cutover work.

| Finding | Disposition | Evidence, consequence and smallest next action |
|---|---|---|
| A1: “Changing three directory strings is sufficient.” | NO_ACTION_REQUIRED | `control/inputs.py`, `local/validation.py`, ingestion and projector all assume one root. Directory-only relocation would omit records or flatten paths. Implement the complete consumer slice before cutover; addressed in the plan, not fixed in code. |
| A2: “Existing SQL already preserves actual Task locations.” | NO_ACTION_REQUIRED | The column exists, but ingestion synthesizes its value and rendering ignores it. Preserve/validate observed source paths through both directions; no speculative new database schema is needed. |
| A3: “Three configured roots cannot create ambiguity.” | NO_ACTION_REQUIRED | Equal/nested/case-alias roots, duplicate IDs and symlinks can alias data or escape boundaries. Add explicit intrinsic and filesystem checks plus negative tests. Never let dictionary insertion order choose the winner. |
| A4: “All matching old paths can be replaced.” | NO_ACTION_REQUIRED | The reference inventory includes checkpoints, evidence, fixtures and prefix-constrained ownership schemas. Review roles and exact bindings; preserve historical/signature meaning and update live consumers deliberately. |
| A5: Configuration compatibility policy | NO_ACTION_REQUIRED | The human selected schema 2 plus preserved schema-1 flat reading and exact re-encoding. The public choice is resolved; implementation must satisfy it, not silently choose a clean break. |
| A6: Five mixed-deliverable classifications | NO_ACTION_REQUIRED | The human confirmed all five proposed destinations in section 4. Preserve Task meanings and authority during any later relocation. |
| A7: Configuration grants research or execution authority | NO_ACTION_REQUIRED | Rejected by the selected design and explicit scope. Keep configuration separate from lifecycle, scientific acceptance and protected execution. |
| A8: Filesystem race hardening | SAFE_TO_DEFER | Existing selectors check paths then use them; a separate `harness-task-state-symlink-toctou-hardening` concern exists. Preserve and test confinement, do not weaken it or claim TOCTOU elimination; revisit if new catalog access enlarges that risk or race-free guarantees become required. |

No invented penetration results, risk-reduction percentages, scientific findings or
independent-review claims accompany this self-assessment. A1–A4 are counterexamples
to a naive migration, already addressed by this plan's required work and tests;
they are not defects in current flat-catalog behavior or remaining planning fixes.
Their implementation requirements are not waived. The decision boundary is now
resolved; implementation authority comes from the human continuation, not this
report's technical outcome.

## 8. Historical planning-record checks actually performed

The exact 216-source inventory was checked for one row per canonical Task, matching
filename/ID, unique case-folded proposed targets, declared destination roots and
current source SHA-256 identities. The five confirmation rows were initially
proposals and are now marked human-confirmed under the intake decision.
The textual-reference snapshot covers 116 files; it is not a claim of exhaustive
semantic consumer discovery.

Maintained Harness projection sync/check, `validate-harness`, exact Task inspection,
Sphinx HTML with warnings as errors and `git diff --check` passed. These establish
planning/control-record consistency only, not implemented configuration behavior.
Logs are at
`/var/folders/42/g1m9r43x2_v4bkyg4csrsn100000gn/T/task-catalog-planning.5wz5_9ml/`.
At that planning boundary the staging index was empty, and no runtime code, tests,
configuration values, Task placement, dependencies, scientific inputs or results
had changed. Later implementation evidence is recorded separately; these historical
checks are not presented as checks of the current implementation.
