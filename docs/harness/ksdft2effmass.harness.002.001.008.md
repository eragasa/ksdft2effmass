---
document_id: ksdft2effmass.harness.002.001.008
task_id: harness-simplification.capability-rationalization
parent: ksdft2effmass.harness.002.001.000
status: proposed
sphinx: excluded
---

# Harness capability ownership rationalization

> **Rationalization status.** Slices 1 through 5 simplified
> `design-data-action-objects`, `develop-operator-records`,
> `develop-python-test-evidence`, `recommend-next-task`, and
> `resolve-human-checkpoint`; Slice 6 implemented `CheckpointDecisionResolver`;
> Slice 7 is deferred; Slice 8 created `develop-harness-resources`; Slice 9
> corrected evidence auditing and retired its duplicate AST script; and Slice 10
> reconciled the historical resource-phase routing group. Later slices remain
> proposals. This page does not activate another skill, agent,
> ActionObject, tool, route, or task. The separately authorized
> `harness-simplification.resources.manifest-refresh` vertical slice added the
> deterministic `ResourceManifestRefresher` ActionObject without changing the
> completed Slice 4 baseline or activating Slice 5 or `develop-harness-resources`.

Starting revision: `507221c8928f981e4b9697b097f22cdfbd1ba03d`
(`origin/dev` after fetch, with a clean worktree).

## Scope and current state

The inspected repository has ten repository-local skills, 34 retained project
agent records, 30 publicly exported maintained harness ActionObjects, and ten
maintained or retained harness command wrappers/validators relevant to this
audit. Project PI configuration exposes the 10 durable agents and disables the
24 phase-specific records. The [harness-simplification chain](../../.pi/chains/harness-simplification.chain.json)
owns live task status, prerequisites, and successor state. This page does not
restate a mutable active-task or next-task snapshot. Availability of a durable
agent does not assign it, and later work still requires explicit task
authorization.

The ownership rule used below is strict: each substantive capability has one
primary classification and owner. A secondary consumer may invoke or apply that
owner, but does not redefine the capability.

## Current skill inventory

Line counts include the entry `SKILL.md` and the reference that it requires on
entry; optional Graphify operation references remain on demand.

| Skill | Trigger and reusable capability | Context | Portability | Overlap or misplaced content | Disposition |
|---|---|---:|---|---|---|
| `design-data-action-objects` | New scientific object models, public object-boundary changes, and substantial ownership refactors | 195 lines | Extractable core with project policy inputs | Historical OperatorRecord policy and invocation/reporting ceremony were removed in Slice 1 | **Keep:** Slice 1 completed; identity and durable ownership guidance retained |
| `develop-architecture-decision` | A genuine material architecture choice with exactly three defensible conceptual alternatives | 126 lines | Extractable decision method with local authority inputs | No material overlap: durable architecture agents supply independence; the skill supplies decision method | **Keep** |
| `develop-harness-resources` | Design and evolution of generic or project-local textual resources | 241 lines across entry and reference | Canonical extractable skill with project profile inputs | Stable resource-agent judgment was extracted without H3/H4 paths, counts, hashes, phase gates, or agent procedure | **Keep:** generic/local ownership, identity, closure, fixtures, descriptor, manifest, deterministic routing, and claim boundaries retained |
| `develop-operator-records` | Represented finite-operator semantics, metadata, compatibility, difference, residual, Hermiticity, and serialization | 309 lines | Project/domain-specific | Fixed inventories, migration/checkpoint history, command gates, test/docs grammar, and invocation ceremony were removed in Slice 2 | **Keep:** operator meaning retained; general architecture, tests, docs, and open decisions route to their owning skills |
| `develop-python-test-evidence` | Semantic design, writing, restructuring, and review of maintained Python evidence | 260 lines; byte footprint reduced by about half | Extractable core with a local profile | Invocation profiles, repository-conformance campaign state, universal migration ceremony, reporting envelopes, and validator implementation detail were removed in Slice 3 | **Keep:** evidence rigor retained; `PythonConformanceValidator` and its CLI own structural enforcement |
| `document-python-research-software` | Public Python docstrings, API/concept pages, Sphinx integration, and serialization documentation | 21 lines | Extractable core with local build inputs | Correctly refers test semantics to the test-evidence skill | **Keep** |
| `inspect-task-state` | Invoke exact bounded task-state inspection for a known chain and task | 46 lines | Project-local command guidance | Contains no reusable judgment beyond input selection and interpretation; behavior is `TaskStateInspector` plus its CLI | **Merge/retire:** retain command documentation outside skill routing |
| `recommend-next-task` | State-gated, read-only selection of one human-selectable next task | 117 lines | Project-specific planning policy | Broad repository discovery, fixed reporting schemas, orchestration ceremony, and duplicated control-plane procedure were removed in Slice 4 | **Keep:** use maintained task-state inspection; read-only and human-selection boundaries are unchanged |
| `graphify` | Explicitly requested local Graphify use under project safety policy | 167 mandatory lines | Project-specific external-tool policy | Exact external-tool safety policy is intentional; operation-specific references are loaded only when needed | **Keep** |
| `resolve-human-checkpoint` | Interpret one current human answer to a durable unresolved checkpoint | 99 lines | Project-local interpretation policy | Git, resumption, CPN, replay, incremental-acceptance, validation-command, and mutation ceremony were removed in Slice 5 | **Keep:** intent matching, ambiguity detection, verbatim response preservation, normalized decision, and authorized-scope boundaries retained; transformation routes to `CheckpointDecisionResolver` |

Capability classification and implementation disposition are different axes. A
`SKILL_EXISTING` capability row means the reusable interpretation capability has
an existing owner; an inventory disposition of **Update** or **Keep** records
whether that owner's current implementation still requires rationalization.
Completing Slice 5 changes the disposition to **Keep** without relabeling the
capability.

Across the skills, authorization requirements may remain invocation
preconditions, but writer/reviewer authority, independence, mutation paths, and
handoff ownership belong to durable agents and task state. The repeated CPN
request/result/retry field inventories in the design, operator, architecture,
next-task, and checkpoint skills should not become five separately evolving
protocol owners. Preserve only subject-specific inputs, outputs, failures, and
stop rules; let the accepted shared invocation contract own common envelopes.
Slice 2 removed the operator skill's closed task IDs, fixed path/test inventories,
completed checkpoint state, successor logic, and repeated invocation envelopes.
Graphify's fixed executable/version policy is current project safety
configuration rather than closed-task history.

No rename or merge between the retained judgment skills is recommended.
`inspect-task-state` is the only current skill recommended for eventual retirement,
and only after its CLI invocation and result interpretation remain discoverable
through maintained documentation and routing.

## Durable agent inventory

All 10 are selectable durable capabilities but are currently unassigned. Their
primary ownership is role authority, mutation/read-only boundaries,
independence, and handoff responsibility—not domain procedure or task paths.

| Durable agent | Stable primary responsibility | Procedure consumers |
|---|---|---|
| `ksdft2effmass-implementation` | Project production writer boundary and implementation handoff | Data/Action design and task-selected domain skills |
| `ksdft2effmass-tests` | Independent project test-evidence writer boundary | `develop-python-test-evidence` |
| `ksdft2effmass-documentation` | Project maintained-documentation writer boundary | `document-python-research-software` |
| `ksdft2effmass-integration-reviewer` | Independent project cross-surface review boundary | Subject skills selected by task |
| `ksdft2effmass-architecture` | Optional independent project architecture analysis | `develop-architecture-decision` |
| `ksdft2effmass-harness-implementation` | Generic/project-local harness implementation writer boundary | Data/Action design; `develop-harness-resources` when applicable |
| `ksdft2effmass-harness-tests` | Independent harness software-verification writer boundary | `develop-python-test-evidence` |
| `ksdft2effmass-harness-documentation` | Harness documentation writer boundary and numbered-page convention | Documentation skill when public Python is affected |
| `ksdft2effmass-harness-integration-reviewer` | Independent harness cross-surface review boundary | Subject skills and deterministic results selected by task |
| `ksdft2effmass-harness-architecture` | Optional independent generic/local harness architecture analysis | `develop-architecture-decision` |

Agent prompts should continue to contain stable role and independence boundaries.
Current paths, commands, checkpoints, phase names, ownership assignments,
correction limits, acceptance state, and successor state belong to `TASK_STATE`.

## Inactive and historical agent extraction

All 24 rows below are disabled by `.pi/settings.json` and classified
`historical-reference-only` by the maintained agent inventory. The files remain
historical artifacts. “Discard” means do not extract that content into a live
skill; it does not mean delete or rewrite the file.

| Inactive agent | Reusable extraction and authoritative destination | Discard from live capability routing |
|---|---|---|
| `ksdft2effmass-harness-cutover-architecture-reviewer` | Generic/local boundary judgment uses `design-data-action-objects`; independence uses durable harness architecture/review roles; routing facts use existing route Actions | H4 identity, rollback checklist, PASS/FAIL ceremony |
| `ksdft2effmass-harness-cutover-integration-reviewer` | Cross-surface review uses durable harness integration reviewer; parity and routes use `ShadowPairComparator`, `ShadowSuiteReplayer`, `ValidationRouteSelector`, and `LegacyRouteConfigurationPreparer` | H4 commands, starting revision, fixed rollback and successor mechanics |
| `ksdft2effmass-harness-cutover-skill-resource-reviewer` | Resource-design judgment uses `develop-harness-resources`; closure is `ResourceManifestValidator` and `SkillResourceValidator` | H4 skill-name correction and stale-path inventory |
| `ksdft2effmass-harness-generic-resource-writer` | Generic/local resource judgment is `develop-harness-resources`; writer authority remains durable harness implementation | H3 paths, accepted-H1 wording, path fences |
| `ksdft2effmass-harness-h2-verification-evidence-writer` | Evidence classification uses `develop-python-test-evidence`; artifact ownership is task state | H2 evidence paths, checksum/acceptance inventory, handoff phase |
| `ksdft2effmass-harness-h3-verification-evidence-writer` | Evidence classification uses `develop-python-test-evidence`; documentation facts use the durable documentation role when assigned | H3 activation, handoff, review aggregation, fixed paths |
| `ksdft2effmass-harness-local-doc-control-writer` | Documentation procedure uses `document-python-research-software`; role boundary uses durable harness documentation | H4 control synchronization, fixed paths, successor prohibitions |
| `ksdft2effmass-harness-local-python-writer` | Object ownership uses `design-data-action-objects`; implemented local behavior remains with maintained local Actions | H4 path assignment, cutover state, generic-contract stop wording |
| `ksdft2effmass-harness-local-resource-writer` | Local overlay/profile judgment is `develop-harness-resources`; manifest validity is `ResourceManifestValidator` | H3 paths, phase sequencing, fixed prohibitions |
| `ksdft2effmass-harness-local-test-parity-writer` | Test semantics use `develop-python-test-evidence`; parity uses `ShadowPairComparator` and `ShadowSuiteReplayer`; role boundary uses durable harness tests | H4 evidence paths, completion script ownership, cutover acceptance state |
| `ksdft2effmass-harness-option-a-contract-resource-writer` | Relational validity is already `ResourceManifestValidator`; intrinsic object rules remain DataObject contracts | H2-HC01 option, one-time correction paths, historical accepted values |
| `ksdft2effmass-harness-python-architecture-rust-reviewer` | Object ownership uses `design-data-action-objects`; architecture independence uses durable harness architecture | H2 36-interface inventory, intended-port phase checklist |
| `ksdft2effmass-harness-python-documentation-writer` | Public Python documentation uses `document-python-research-software` and durable harness documentation | Single H2 page assignment and fixed H3 inputs |
| `ksdft2effmass-harness-python-evidence-vvuq-reviewer` | Evidence semantics use `develop-python-test-evidence`; independent review uses durable harness integration reviewer | H2 inventory closure and phase completion gate |
| `ksdft2effmass-harness-python-implementation-writer` | Implementation role uses durable harness implementation; object/source-doc procedure uses existing skills | H2 interface count, fixed manifest paths, phase fences |
| `ksdft2effmass-harness-python-integration-reviewer` | Cross-surface independence uses durable harness integration reviewer; checks use existing resource/ownership/checksum Actions | H2 packaging and command inventory |
| `ksdft2effmass-harness-python-test-writer` | Test procedure uses `develop-python-test-evidence`; writer authority uses durable harness tests | H2 ownership manifest, inventory state, completion gate |
| `ksdft2effmass-harness-resource-architecture-reviewer` | Resource judgment is `develop-harness-resources`; architecture advice uses durable harness architecture | H3/H1 identity and intended-Rust phase wording |
| `ksdft2effmass-harness-resource-documentation-writer` | Resource documentation uses durable harness documentation with `develop-harness-resources` for resource judgment | H3 directories and handoff narration |
| `ksdft2effmass-harness-resource-evidence-vvuq-reviewer` | Evidence semantics use `develop-python-test-evidence`; independent review uses durable harness integration reviewer | H3 fixture inventory and phase PASS/FAIL ceremony |
| `ksdft2effmass-harness-resource-integration-reviewer` | Resource/checksum/local-composition Actions own mechanics; durable harness integration review owns independence | H3 control state and H2-inactive handoff checklist |
| `ksdft2effmass-harness-resource-test-writer` | Test semantics use `develop-python-test-evidence`; resource judgment uses `develop-harness-resources`; durable harness tests own implementation | H3 fixture paths and accepted-H1 case inventory |
| `ksdft2effmass-harness-resource-validation-writer` | `ResourceManifestValidator`, `ResourceResolver`, `ResourceManifestRefresher`, `SkillResourceValidator`, `ChecksumManifestValidator`, and maintained local Actions own deterministic behavior | H3 validator path, dependency-free completion-script assignment |
| `ksdft2effmass-harness-skill-resource-cutover-writer` | Resource judgment is `develop-harness-resources`; capability inventory is the maintained validator/tool | TEST-EVIDENCE-SKILL-1/H4 migration, fixed consumers, activation mechanics |

The extraction result is intentionally small: one cohesive maintained
resource-authoring skill, no cutover skill, no phase agent revival, and no copied
prompt.

### Slice 10 resource-phase routing reconciliation

The six resource-phase agent records remain disabled, byte-unchanged, and
`historical-reference-only`, with no live assignment or capability consumer.
Reusable generic/local resource judgment belongs to `develop-harness-resources`.
Durable harness agents own assigned implementation, tests, documentation,
architecture advice, and independent integration review. Deterministic mechanics
remain with `ResourceManifestValidator`, `ResourceResolver`,
`ResourceManifestRefresher`, `SkillResourceValidator`, `ChecksumManifestValidator`,
and maintained project-local composition Actions. No phase agent was revived and
no historical record was deleted. This completes the resource-agent
rationalization sequence.

## Maintained ActionObject inventory

The public export surfaces were inspected directly. The generic root package exports
15 Actions, the generic `evidence` subpackage exports 2 Actions, and the project-local
package exports 15 Actions.

| Source | Existing ActionObjects | Primary deterministic ownership |
|---|---|---|
| `validation.py` | `JsonRecordSerializer`, `JsonRecordDeserializer` | Canonical closed wire serialization and strict kind-selected decoding |
| `profiles.py` | `ProjectProfileLoader` | Profile byte decoding, identity, schema, and contract compatibility |
| `resources.py` | `ResourceManifestValidator`, `ResourceManifestRefresher`, `ResourceResolver`, `SkillResourceValidator` | Manifest closure/overlay/leakage, explicit-path identity refresh, confined resolution/hash, skill-resource closure |
| `ownership.py` | `OwnershipManifestValidator` | Task/agent/scope/completion-command ownership relations |
| `checkpoints.py` | `CheckpointDecisionResolver`, `CheckpointSetValidator` | Pure explicit decision transformation and checkpoint lifecycle/relation validation |
| `chains.py` | `ChainStateEvaluator` | Active, blocked, and structurally ready chain facts |
| `checksums.py` | `ChecksumManifestValidator` | Root-confined exact checksum verification |
| `evidence/identifiers.py` | `IdentifierAuditor` | Evidence namespace, marker, owner, and duplicate inspection |
| `evidence/python_conformance.py` | `PythonConformanceValidator` | Explicit-path structural maintained-test validation |
| `task_state.py` | `TaskStateInspector` | Exact declared task/ownership/completion/artifact/run/handoff inspection |
| `local/context.py` | `LocalHarnessContextLoader` | Explicit-root profile/manifest composition |
| `local/adapters.py` | `CheckpointRecordAdapter`, `TaskRecordAdapter`, `ChainRecordAdapter`, `AgentRecordAdapter`, `OwnershipManifestAdapter`, `ChecksumCatalogAdapter`, `SkillInventoryAdapter`, `EvidenceOwnershipManifestAdapter`, `EvidenceModuleSelector` | Strict compatibility adaptation of caller-selected repository records |
| `local/routing.py` | `ValidationRouteSelector`, `LegacyRouteConfigurationPreparer` | Pure legacy/shadow/local selection and non-destructive rollback configuration |
| `local/shadow.py` | `ShadowPairComparator`, `ShadowSuiteReplayer` | Normalized parity classification and aggregate assessment; no command launch |
| `local/validation.py` | `LocalRepositoryValidator` | Composition of selected generic validators without severity downgrade |

### Maintained wrappers and validators

| Tool | Disposition |
|---|---|
| `python/.../local/inspect_task_state.py` | Keep as the thin `TaskStateInspector` CLI |
| `python/.../local/refresh_resource_manifest.py` | Keep as the thin read-only `ResourceManifestRefresher` proposal CLI |
| `python/.../local/identifier_audit.py` | Keep as the thin explicit-root and explicit-inventory `IdentifierAuditor` CLI |
| `harness/pi/validation/validate_python_conformance.py` | Keep as the thin `PythonConformanceValidator` CLI |
| `harness/local/validation/validate_evidence_repository_conformance.py` | Keep as the project-local inventory/collection completion gate; it is not a new generic Action |
| `.pi/skills/validate_skill_capabilities.py` | Keep as the current fixed repository capability-inventory validator |
| `.pi/skills/validate_harness.py` | Retired from current operation with the phase-era route; historical evidence references remain unchanged |
| `harness/local/validation/replay_current_validators.py` | Retired from current operation rather than renamed into another replay system |
| `harness/pi/validation/validate_h3_resources.py` | Retired after its current gates received explicit Action, focused-test, historical-only, or obsolete dispositions |
| `harness/pi/validation/validate_architecture_decision_cases.py` | Keep as deterministic cases for the architecture-decision skill contract |
| `.pi/skills/identifier_audit.py` | Retired in Slice 9 after controlled and maintained-inventory replacement gates passed; historical command records remain unchanged |

## Capability-to-owner matrix

This is the primary decomposition. Each row has exactly one primary owner;
secondary consumers do not share ownership.

| Capability | Classification | Primary owner | Secondary consumers |
|---|---|---|---|
| DataObject/ResultObject/ActionObject boundary judgment | `SKILL_EXISTING` | `design-data-action-objects` | Implementation and architecture agents |
| Three-option material architecture decision support | `SKILL_EXISTING` | `develop-architecture-decision` | Durable architecture agents |
| Represented finite-operator scientific/software judgment | `SKILL_EXISTING` | `develop-operator-records` | Project implementation/tests/docs/reviewer |
| Evidence class, owner, oracle, acceptance, and semantic review | `SKILL_EXISTING` | `develop-python-test-evidence` | Test writers and integration reviewers |
| Public Python and Sphinx documentation procedure | `SKILL_EXISTING` | `document-python-research-software` | Documentation and implementation agents |
| Exact declared task-state inspection | `ACTION_EXISTING` | `TaskStateInspector` and CLI | Root agent and task workflows |
| Single next-task recommendation judgment | `SKILL_EXISTING` | `recommend-next-task` | Root agent only |
| Explicit local Graphify safety procedure | `SKILL_EXISTING` | `graphify` | Root agent after explicit request |
| Human checkpoint intent matching and ambiguity judgment | `SKILL_EXISTING` | `resolve-human-checkpoint` | Root agent |
| Deterministic checkpoint resolution transformation | `ACTION_EXISTING` | `CheckpointDecisionResolver` | Interpreted decision consumers and authorized local workflows |
| Canonical harness wire JSON | `ACTION_EXISTING` | `JsonRecordSerializer` / `JsonRecordDeserializer` | Profiles, resources, adapters |
| Project-profile loading and compatibility | `ACTION_EXISTING` | `ProjectProfileLoader` | Local context |
| Generic/local resource design and evolution judgment | `SKILL_EXISTING` | `develop-harness-resources` | Harness implementation/docs/tests/reviewer |
| Manifest closure, overlay, and generic-to-local leakage | `ACTION_EXISTING` | `ResourceManifestValidator` | Context and repository validation |
| Explicit-path resource identity refresh | `ACTION_EXISTING` | `ResourceManifestRefresher` and read-only CLI | Resource authors using `develop-harness-resources` |
| Root-confined resource selection and hashing | `ACTION_EXISTING` | `ResourceResolver` | Resource consumers |
| Skill descriptor/resource closure | `ACTION_EXISTING` | `SkillResourceValidator` | Capability/resource routing |
| Ownership relation validation | `ACTION_EXISTING` | `OwnershipManifestValidator` | Task preflight and local validation |
| Checkpoint lifecycle validation | `ACTION_EXISTING` | `CheckpointSetValidator` | Chain evaluation and checkpoint skill |
| Chain active/blocked/ready evaluation | `ACTION_EXISTING` | `ChainStateEvaluator` | Local validation and planning |
| Checksum verification | `ACTION_EXISTING` | `ChecksumManifestValidator` | Local validation |
| Evidence-ID and executable-marker inspection | `ACTION_EXISTING` | `IdentifierAuditor` and thin local CLI | Test-evidence workflows |
| Structural Python test-evidence inspection | `ACTION_EXISTING` | `PythonConformanceValidator` | Test-evidence skill and local gate |
| Explicit local profile/manifest composition | `ACTION_EXISTING` | `LocalHarnessContextLoader` | Local validation |
| Selected historical/live record normalization | `ACTION_EXISTING` | local `Adapt*` Actions and `EvidenceModuleSelector` | Local validation only |
| Validation route selection and rollback facts | `ACTION_EXISTING` | `ValidationRouteSelector` / `LegacyRouteConfigurationPreparer` | Retained compatibility inputs; no current operational route |
| Normalized parity comparison and aggregation | `ACTION_EXISTING` | `ShadowPairComparator` / `ShadowSuiteReplayer` | Retained compatibility and historical comparison |
| Project-local validator composition | `ACTION_EXISTING` | `LocalRepositoryValidator` | Explicit current validation clients |
| Fixed repository skill-capability inventory validation | `ACTION_EXISTING` | `.pi/skills/validate_skill_capabilities.py` | Root verification |
| Current harness resource validation | `ACTION_EXISTING` | `LocalHarnessContextLoader`, `ResourceResolver`, and `validate_local_harness_resources.py` | Root verification |
| Repository maintained-test conformance gate | `ACTION_EXISTING` | `validate_evidence_repository_conformance.py` | Authorized test-conformance tasks |
| Writer/reviewer authority, independence, and handoff | `DURABLE_AGENT` | 10 durable agent records | Task assignments |
| Paths, phases, assignments, checkpoints, gates, and successors | `TASK_STATE` | active chain/task/ownership/checkpoint records | Agents and skills as explicit inputs |
| Human-facing architecture and operation explanation | `DOCUMENTATION` | numbered harness pages and public harness docs | Humans and agents |
| Closed H2/H3/H4 command inventories and ceremony | `HISTORICAL_ONLY` | retained phase records/evidence | Historical reconstruction only |
| Phase-specific agent capability routing | `DUPLICATE_RETIRE` | durable agents plus accepted skill/Action destinations | Disabled historical agent files only |
| `inspect-task-state` procedural skill routing | `DUPLICATE_RETIRE` | `TaskStateInspector` plus maintained CLI documentation | Current skill until bounded retirement |
| General `assess-harness-cutover` procedure | `DUPLICATE_RETIRE` | route/parity Actions, architecture skill, and durable integration reviewer | A cutover task may compose them |

Counts from the 38 current rows are:

| Classification | Count |
|---|---:|
| `SKILL_EXISTING` | 9 |
| `SKILL_UPDATE` | 0 |
| `SKILL_CANDIDATE` | 0 |
| `ACTION_EXISTING` | 22 |
| `ACTION_CANDIDATE` | 0 |
| `DURABLE_AGENT` | 1 |
| `TASK_STATE` | 1 |
| `DOCUMENTATION` | 1 |
| `HISTORICAL_ONLY` | 1 |
| `DUPLICATE_RETIRE` | 3 |
| `UNRESOLVED` | 0 |

These are capability-classification counts, not counts of pending skill
implementation dispositions; `SKILL_UPDATE: 0` therefore remains compatible with
the completed per-skill updates above.

## Candidate skill evaluation

### `develop-harness-resources` — completed in Slice 8

- **Trigger conditions:** a task must design or change a generic/local resource
  identity, manifest/profile relationship, skill descriptor closure, resource
  schema/version boundary, or associated fixture/documentation meaning.
- **Non-trigger conditions:** running an existing validator; editing one value
  already fixed by an accepted contract; routine docs; test grammar; route
  selection; parity assessment; task ownership; or a phase cutover.
- **Reusable procedure:** classify generic versus local ownership; define stable
  logical, format/behavior, path, and byte identities; declare dependency and
  extension-only overlay direction; synchronize manifest/schema/descriptor and
  semantic fixtures/docs; invoke existing deterministic Actions; separate
  structural PASS from authorization or scientific meaning.
- **Relationship to existing skills:** use `design-data-action-objects` only for
  Python object boundaries, `document-python-research-software` for public
  Python docs, and `develop-python-test-evidence` for maintained pytest evidence.
  It owns textual-resource design judgment, which none of those skills owns.
- **Deterministic components outside the skill:** `ResourceManifestValidator`,
  `ResourceManifestRefresher`, `ResourceResolver`, `SkillResourceValidator`,
  canonical wire serialization, checksum validation, and local repository
  composition.
- **Expected references/scripts:** a concise, de-historicized resource-contract
  reference derived from `harness/pi/docs/resources.md`; public schemas and
  manifests remain authority. Existing Actions, not a copied H3 validator, are
  the executable references.
- **Anticipated context size:** target at most about 150 lines for entry plus one
  core reference; load schemas/manifests only when the request names them.
- **Realistic future uses:** add/version a generic wire-record resource; add a
  project-local policy extension/profile without reverse leakage; evolve a skill
  descriptor and its complete resource closure; add a new canonical fixture
  family tied to a versioned resource contract.
- **Recurrence evidence:** six H3 resource-specific agents, three H4 resource or
  cutover roles, current generic/local manifests and profiles, four maintained
  resource Actions, and retained skill-descriptor resources show repeated
  resource-boundary work across more than one closed task.

The skill must not package H3 paths, H1 decisions, H4 cutover steps,
accepted hashes, or phase completion gates.

### `assess-harness-cutover` — reject

- **Potential trigger:** replacing one maintained harness implementation or route
  with another after both produce normalized observations.
- **Non-trigger conditions:** routine implementation/review, a deterministic
  correction, resource design, or a choice with no actual old/new runtime.
- **Possible procedure:** establish identical inputs, compare normalized results,
  classify differences, inspect route/rollback, review boundaries, and stop for
  any human choice.
- **Relationship to existing owners:** `ShadowPairComparator` and
  `ShadowSuiteReplayer` own parity; route Actions own routing; `LocalRepositoryValidator`
  owns composed checks; `develop-architecture-decision` owns genuine alternatives;
  the durable integration reviewer owns independent cross-surface assessment.
- **Deterministic components outside a skill:** all parity, route, checksum,
  manifest, and local validation behavior.
- **Expected references/scripts:** it would necessarily repeat H4 plans and the
  current route wrapper rather than introduce a stable independent reference.
- **Anticipated context size:** likely more than 150 lines because it would
  duplicate route, parity, architecture, review, and rollback boundaries.
- **Realistic future uses:** validator-backend replacement, a future state-store
  cutover, and extraction from local to packaged resources.
- **Recurrence evidence:** one completed H4 cutover and proposed future migrations
  show possible recurrence, but not a missing cohesive judgment owner.

The candidate is rejected because it is orchestration of existing Actions,
skills, durable review authority, and task-specific acceptance state. A future
cutover task should compose those owners instead.

## Deterministic action assessment

| Repeated operation | Existing owner or proposal | Decision |
|---|---|---|
| Resource-manifest validation | `ResourceManifestValidator` | No duplicate tool |
| Explicit selected resource-identity refresh | `ResourceManifestRefresher` | Maintained Action and read-only CLI added by the bounded refresh slice |
| Generic/local leakage detection | `ResourceManifestValidator` | No duplicate tool |
| Parity comparison | `ShadowPairComparator`, `ShadowSuiteReplayer` | No duplicate tool |
| Route inspection/selection | `ValidationRouteSelector`, `LegacyRouteConfigurationPreparer`; selected wrapper in `validate_harness.py` | No duplicate tool |
| Checksum verification | `ChecksumManifestValidator` | No duplicate tool |
| Evidence-ID inspection | `IdentifierAuditor` plus thin explicit-inventory CLI | Duplicate legacy AST script retired after conformance gates passed |
| Maintained validation-command inspection | `TaskStateInspector` reports declared completion command | No duplicate tool |
| Capability-inventory inspection | `validate_skill_capabilities.py` validates the fixed repository inventory | Keep tool; do not create an Action until a second input contract needs a reusable public result |
| Checkpoint resolution record transformation | `CheckpointDecisionResolver` | Pure explicit immutable transformation implemented in Slice 6 |

`CheckpointDecisionResolver` owns deterministic generic checkpoint-record
transformation after intent interpretation. `CheckpointSetValidator` remains the
checkpoint-set validation owner. Request and result are runtime DataObjects, not
wire records. Because project-local checkpoint JSON has additional fields, no
local rewrite CLI was added; lossless project-local patching, persistence, Git,
task resumption, successor activation, and other external effects remain with a
separately authorized root/local workflow.

## Duplicate and historical retirement

The 24 phase agents remain disabled and retained. Their phase names, task IDs,
fixed paths, ownership assignments, checkpoint state, correction limits,
historical commands, acceptance mechanics, successor logic, and one-time
migration instructions are `HISTORICAL_ONLY` or `TASK_STATE`; none should enter a
skill. No active phase-specific role should be restored.

After accepted destination changes, retire only live routing or duplicate tools:

1. remove `inspect-task-state` from skill routing after maintained CLI docs cover
   its trigger, inputs, result interpretation, and stop boundary;
2. **Completed in Slice 9:** current callers use the public evidence Action through
   its thin local wrapper, and the duplicate AST policy was retired; and
3. keep all historical agent files and old evidence unchanged.

## Recommended implementation sequence

Each slice is separately reviewable and affects one permitted owner class.
Nothing below is activated by this proposal. The completed manifest-refresh
vertical slice supplies deterministic maintenance used by the maintained resource skill;
it does not create or activate that skill and does not alter this sequence.

1. **Completed — update `design-data-action-objects`.** Historical
   OperatorRecord correction policy and invocation/reporting ceremony were
   removed; reusable ownership, serialization, Workflow, free-function,
   portability, and scientific-claim boundaries remain. The skill identity and
   both durable consumers are unchanged, and no Python runtime changed.
2. **Completed — update `develop-operator-records`.** Fixed package/test
   inventories, migration and checkpoint history, command gates, invocation
   envelopes, and duplicated test/documentation procedure were removed.
   Represented meaning, operator-specific ownership, compatibility, Hermiticity,
   numerical robustness, gauge/coordinate, serialization, and evidence
   boundaries remain. Production behavior and public APIs are unchanged.
3. **Completed — update `develop-python-test-evidence`.** Evidence taxonomy,
   class/artifact ownership, semantic naming and parameterization, research-grade
   test documentation, oracle quality, cohesion/layering, and validation/UQ
   boundaries remain. Invocation and migration ceremony, fixed conformance
   counts, and duplicated validator logic were removed. Canonical and live skill
   resources remain byte-identical; test behavior and evidence IDs are unchanged.
4. **Completed — update `recommend-next-task`.** Retained state-gated,
   read-only selection of exactly one proposed task and the human-selection stop.
   Exact known task state now routes through maintained `TaskStateInspector` usage;
   broad repository discovery, fixed reporting schemas, and duplicated
   orchestration and control-plane procedure were removed.
5. **Completed — update `resolve-human-checkpoint`.** Retained human-intent
   matching, ambiguity detection, the restricted affirmative rule, verbatim
   response preservation, normalized decisions, authorized-scope limits, and the
   human-authority boundary. Git, commit/push, resumption, CPN, retry/replay,
   invocation-envelope, incremental-acceptance, validation-command, and mutation
   ceremony were removed. Deterministic transformation is assigned to
   `CheckpointDecisionResolver`, implemented separately in Slice 6.
6. **Completed — implement one Action:** `CheckpointDecisionResolver` now owns
   pure explicit immutable generic checkpoint transformation, exact option-ID
   membership, deterministic conflicts, and idempotent repetition. Runtime
   request/result records remain outside `HarnessWireRecord`; no local rewrite
   CLI, filesystem, clock, Git, resumption, or successor behavior was added.
7. **Deferred — retire one existing skill:** `inspect-task-state` remains in
   live routing with its maintained command guidance unchanged.
8. **Completed — create one new skill:** `develop-harness-resources` now owns
   generic/local resource judgment, identity and versioning, dependency closure,
   schema/fixture and descriptor agreement, manifest synchronization, and claim
   boundaries. Existing Actions remain deterministic owners; canonical and live
   skill/reference bytes are identical.
9. **Completed — retire one duplicate tool:** corrected normalized field parsing in
   `IdentifierAuditor`, added its thin explicit-inventory CLI, migrated live
   callers, confirmed all 201 maintained modules pass, and removed the standalone
   duplicate AST policy.
10. **Completed — reconcile one bounded historical routing group:** the six
    resource-phase agents remain disabled and unchanged; reusable judgment routes
    to maintained skills and durable agents, deterministic mechanics route to
    maintained Actions, and no historical agent was revived or deleted.

## Explicit deferred items

- `assess-harness-cutover` is rejected, not deferred for automatic creation.
- Machine-readable unification of skills, agents, Actions, wrappers, and lifecycle
  into a new capability inventory is deferred; the current fixed validator remains.
- Phase assumptions inside local compatibility adapters require a separate
  public-contract task before any removal or generalization.
- A Graphify execution wrapper is deferred because it would cross the external
  tool/dependency and command-runner boundary.
- SQLite/evidence redesign, review-dispatch idempotency, package extraction,
  historical-file deletion, and publication remain inactive.
- The separately authorized
  `harness.simplification.agents.delegation-validation` Task is active; its
  nonmutating runtime probes do not reopen this completed architecture work.
- P3 and all scientific, numerical, external, protected, and release execution
  remain outside this proposal.

The harness-simplification chain records Slice 10 completion and owns current
active-task state; this page does not activate another slice. Slice 7 retirement
of `inspect-task-state` remains deferred, and telemetry or other successors
still require separate human authorization.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [Maintained execution interface](ksdft2effmass.harness.002.001.007.md)
- **Next:** [Incremental migration plan](ksdft2effmass.harness.002.001.009.md)
