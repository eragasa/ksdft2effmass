---
document_id: ksdft2effmass.harness.010.040.010
task_id: harness-simplification.capability-rationalization
parent: ksdft2effmass.harness.010.040.000
status: proposed
sphinx: excluded
---

# Harness capability ownership rationalization

> **Rationalization status.** Slices 1 through 4 simplified
> `design-data-action-objects`, `develop-operator-records`,
> `develop-python-test-evidence`, and `recommend-next-task`; all later slices
> remain proposals. This page does not activate another skill, agent,
> ActionObject, tool, route, or task. The separately authorized
> `harness-simplification.resources.manifest-refresh` vertical slice added the
> deterministic `RefreshResourceManifest` ActionObject without changing the
> completed Slice 4 baseline or activating Slice 5 or `develop-harness-resources`.

Starting revision: `507221c8928f981e4b9697b097f22cdfbd1ba03d`
(`origin/dev` after fetch, with a clean worktree).

## Scope and current state

The inspected repository has nine repository-local skills, 34 retained project
agent records, 29 publicly exported maintained harness ActionObjects, and ten
maintained or retained harness command wrappers/validators relevant to this
audit. Project PI configuration exposes the 10 durable agents and disables the
24 phase-specific records. The harness-simplification chain has
`active_task: null`; no durable agent is currently assigned, automatic successor
activation is disabled, and the next delegation-validation task remains
inactive and unauthorized.

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
| `develop-operator-records` | Represented finite-operator semantics, metadata, compatibility, difference, residual, Hermiticity, and serialization | 309 lines | Project/domain-specific | Fixed inventories, migration/checkpoint history, command gates, test/docs grammar, and invocation ceremony were removed in Slice 2 | **Keep:** operator meaning retained; general architecture, tests, docs, and open decisions route to their owning skills |
| `develop-python-test-evidence` | Semantic design, writing, restructuring, and review of maintained Python evidence | 260 lines; byte footprint reduced by about half | Extractable core with a local profile | Invocation profiles, repository-conformance campaign state, universal migration ceremony, reporting envelopes, and validator implementation detail were removed in Slice 3 | **Keep:** evidence rigor retained; `ValidatePythonTestEvidence` and its CLI own structural enforcement |
| `document-python-research-software` | Public Python docstrings, API/concept pages, Sphinx integration, and serialization documentation | 21 lines | Extractable core with local build inputs | Correctly refers test semantics to the test-evidence skill | **Keep** |
| `inspect-task-state` | Invoke exact bounded task-state inspection for a known chain and task | 46 lines | Project-local command guidance | Contains no reusable judgment beyond input selection and interpretation; behavior is `InspectTaskState` plus its CLI | **Merge/retire:** retain command documentation outside skill routing |
| `recommend-next-task` | State-gated, read-only selection of one human-selectable next task | 117 lines | Project-specific planning policy | Broad repository discovery, fixed reporting schemas, orchestration ceremony, and duplicated control-plane procedure were removed in Slice 4 | **Keep:** use maintained task-state inspection; read-only and human-selection boundaries are unchanged |
| `graphify` | Explicitly requested local Graphify use under project safety policy | 167 mandatory lines | Project-specific external-tool policy | Exact external-tool safety policy is intentional; operation-specific references are loaded only when needed | **Keep** |
| `resolve-human-checkpoint` | Match an unambiguous human answer to one unresolved checkpoint and preserve human authority | 132 lines | Project-local policy; transition core may be extractable | Mixes ambiguity/authority judgment with deterministic record mutation, validation, commit/push, and resumption sequencing | **Update:** retain intent matching and authority judgment; move record transformation to a proposed ActionObject |

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
| `ksdft2effmass-harness-implementation` | Generic/project-local harness implementation writer boundary | Data/Action design; proposed resource skill when applicable |
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
| `ksdft2effmass-harness-cutover-integration-reviewer` | Cross-surface review uses durable harness integration reviewer; parity and routes use `CompareShadowPair`, `ReplayShadowSuite`, `SelectValidationRoute`, and `RollBackValidationRoute` | H4 commands, starting revision, fixed rollback and successor mechanics |
| `ksdft2effmass-harness-cutover-skill-resource-reviewer` | Resource-design judgment is the proposed `develop-harness-resources`; closure is `ValidateResourceManifest` and `ValidateSkillResources` | H4 skill-name correction and stale-path inventory |
| `ksdft2effmass-harness-generic-resource-writer` | Generic/local resource judgment is the proposed resource skill; writer authority remains durable harness implementation | H3 paths, accepted-H1 wording, path fences |
| `ksdft2effmass-harness-h2-verification-evidence-writer` | Evidence classification uses `develop-python-test-evidence`; artifact ownership is task state | H2 evidence paths, checksum/acceptance inventory, handoff phase |
| `ksdft2effmass-harness-h3-verification-evidence-writer` | Evidence classification uses `develop-python-test-evidence`; documentation facts use the durable documentation role when assigned | H3 activation, handoff, review aggregation, fixed paths |
| `ksdft2effmass-harness-local-doc-control-writer` | Documentation procedure uses `document-python-research-software`; role boundary uses durable harness documentation | H4 control synchronization, fixed paths, successor prohibitions |
| `ksdft2effmass-harness-local-python-writer` | Object ownership uses `design-data-action-objects`; implemented local behavior remains with maintained local Actions | H4 path assignment, cutover state, generic-contract stop wording |
| `ksdft2effmass-harness-local-resource-writer` | Local overlay/profile judgment is the proposed resource skill; manifest validity is `ValidateResourceManifest` | H3 paths, phase sequencing, fixed prohibitions |
| `ksdft2effmass-harness-local-test-parity-writer` | Test semantics use `develop-python-test-evidence`; parity uses `CompareShadowPair` and `ReplayShadowSuite`; role boundary uses durable harness tests | H4 evidence paths, completion script ownership, cutover acceptance state |
| `ksdft2effmass-harness-option-a-contract-resource-writer` | Relational validity is already `ValidateResourceManifest`; intrinsic object rules remain DataObject contracts | H2-HC01 option, one-time correction paths, historical accepted values |
| `ksdft2effmass-harness-python-architecture-rust-reviewer` | Object ownership uses `design-data-action-objects`; architecture independence uses durable harness architecture | H2 36-interface inventory, intended-port phase checklist |
| `ksdft2effmass-harness-python-documentation-writer` | Public Python documentation uses `document-python-research-software` and durable harness documentation | Single H2 page assignment and fixed H3 inputs |
| `ksdft2effmass-harness-python-evidence-vvuq-reviewer` | Evidence semantics use `develop-python-test-evidence`; independent review uses durable harness integration reviewer | H2 inventory closure and phase completion gate |
| `ksdft2effmass-harness-python-implementation-writer` | Implementation role uses durable harness implementation; object/source-doc procedure uses existing skills | H2 interface count, fixed manifest paths, phase fences |
| `ksdft2effmass-harness-python-integration-reviewer` | Cross-surface independence uses durable harness integration reviewer; checks use existing resource/ownership/checksum Actions | H2 packaging and command inventory |
| `ksdft2effmass-harness-python-test-writer` | Test procedure uses `develop-python-test-evidence`; writer authority uses durable harness tests | H2 ownership manifest, inventory state, completion gate |
| `ksdft2effmass-harness-resource-architecture-reviewer` | Resource judgment is the proposed resource skill; architecture independence uses durable harness architecture | H3/H1 identity and intended-Rust phase wording |
| `ksdft2effmass-harness-resource-documentation-writer` | Resource explanation uses maintained resource docs and durable harness documentation; public Python docs use the existing docs skill | H3 directories and handoff narration |
| `ksdft2effmass-harness-resource-evidence-vvuq-reviewer` | Evidence/oracle judgment uses `develop-python-test-evidence`; independent review uses durable harness integration reviewer | H3 fixture inventory and phase PASS/FAIL ceremony |
| `ksdft2effmass-harness-resource-integration-reviewer` | Manifest/leakage checks use existing Actions; independence uses durable harness integration reviewer | H3 control state and H2-inactive handoff checklist |
| `ksdft2effmass-harness-resource-test-writer` | Test/fixture evidence judgment uses `develop-python-test-evidence`; resource meaning uses the proposed resource skill | H3 fixture paths and accepted-H1 case inventory |
| `ksdft2effmass-harness-resource-validation-writer` | Deterministic behavior already belongs to maintained resource, resolution, skill, checksum, and local-composition Actions | H3 validator path, dependency-free completion-script assignment |
| `ksdft2effmass-harness-skill-resource-cutover-writer` | Resource judgment is the proposed resource skill; capability inventory is the maintained validator/tool | TEST-EVIDENCE-SKILL-1/H4 migration, fixed consumers, activation mechanics |

The extraction result is intentionally small: one cohesive resource-authoring
skill candidate, no cutover skill, no phase agent revival, and no copied prompt.

## Maintained ActionObject inventory

The public export surfaces were inspected directly. The generic package exports
14 Actions and the project-local package exports 15 Actions.

| Source | Existing ActionObjects | Primary deterministic ownership |
|---|---|---|
| `validation.py` | `SerializeJsonRecord`, `DeserializeJsonRecord` | Canonical closed wire serialization and strict kind-selected decoding |
| `profiles.py` | `LoadProjectProfile` | Profile byte decoding, identity, schema, and contract compatibility |
| `resources.py` | `ValidateResourceManifest`, `RefreshResourceManifest`, `ResolveResource`, `ValidateSkillResources` | Manifest closure/overlay/leakage, explicit-path identity refresh, confined resolution/hash, skill-resource closure |
| `ownership.py` | `ValidateOwnershipManifest` | Task/agent/scope/completion-command ownership relations |
| `checkpoints.py` | `ValidateCheckpointSet` | Checkpoint lifecycle and relation validation without resolution |
| `chains.py` | `EvaluateChainState` | Active, blocked, and structurally ready chain facts |
| `checksums.py` | `ValidateChecksumManifest` | Root-confined exact checksum verification |
| `evidence.py` | `AuditEvidenceIdentifiers` | Evidence namespace, marker, owner, and duplicate inspection |
| `test_evidence.py` | `ValidatePythonTestEvidence` | Explicit-path structural maintained-test validation |
| `task_state.py` | `InspectTaskState` | Exact declared task/ownership/completion/artifact/run/handoff inspection |
| `local/context.py` | `LoadLocalHarnessContext` | Explicit-root profile/manifest composition |
| `local/adapters.py` | `AdaptCheckpointRecords`, `AdaptTaskRecords`, `AdaptChainRecord`, `AdaptAgentRecords`, `AdaptOwnershipManifest`, `AdaptChecksumCatalog`, `AdaptSkillInventory`, `AdaptEvidenceOwnershipManifest`, `SelectEvidenceModules` | Strict compatibility adaptation of caller-selected repository records |
| `local/routing.py` | `SelectValidationRoute`, `RollBackValidationRoute` | Pure legacy/shadow/local selection and non-destructive rollback configuration |
| `local/shadow.py` | `CompareShadowPair`, `ReplayShadowSuite` | Normalized parity classification and aggregate assessment; no command launch |
| `local/validation.py` | `ValidateLocalRepository` | Composition of selected generic validators without severity downgrade |

### Maintained wrappers and validators

| Tool | Disposition |
|---|---|
| `python/.../local/inspect_task_state.py` | Keep as the thin `InspectTaskState` CLI |
| `python/.../local/refresh_resource_manifest.py` | Keep as the thin read-only `RefreshResourceManifest` proposal CLI |
| `harness/pi/validation/validate_python_test_evidence.py` | Keep as the thin `ValidatePythonTestEvidence` CLI |
| `harness/local/validation/validate_repository_test_evidence.py` | Keep as the project-local inventory/collection completion gate; it is not a new generic Action |
| `.pi/skills/validate_skill_capabilities.py` | Keep as the current fixed repository capability-inventory validator |
| `.pi/skills/validate_harness.py` | Keep as selected-route command composition; it does not replace pure route Actions |
| `harness/local/validation/replay_current_validators.py` | Keep as the current local-route wrapper while that route remains configured |
| `harness/pi/validation/validate_h3_resources.py` | Retain as a legacy broad resource completion validator; do not copy it into a skill |
| `harness/pi/validation/validate_architecture_decision_cases.py` | Keep as deterministic cases for the architecture-decision skill contract |
| `.pi/skills/audit_evidence_identifiers.py` | Retire in a bounded tool slice after callers use `AuditEvidenceIdentifiers` or a thin wrapper over it; do not retain duplicate AST policy |

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
| Exact declared task-state inspection | `ACTION_EXISTING` | `InspectTaskState` and CLI | Root agent and task workflows |
| Single next-task recommendation judgment | `SKILL_EXISTING` | `recommend-next-task` | Root agent only |
| Explicit local Graphify safety procedure | `SKILL_EXISTING` | `graphify` | Root agent after explicit request |
| Human checkpoint intent matching and ambiguity judgment | `SKILL_EXISTING` | `resolve-human-checkpoint` | Root agent |
| Deterministic checkpoint resolution transformation | `ACTION_CANDIDATE` | proposed `ResolveCheckpointDecision` | Checkpoint skill and future CLI |
| Canonical harness wire JSON | `ACTION_EXISTING` | `SerializeJsonRecord` / `DeserializeJsonRecord` | Profiles, resources, adapters |
| Project-profile loading and compatibility | `ACTION_EXISTING` | `LoadProjectProfile` | Local context |
| Generic/local resource design and evolution judgment | `SKILL_CANDIDATE` | proposed `develop-harness-resources` | Harness implementation/docs/tests/reviewer |
| Manifest closure, overlay, and generic-to-local leakage | `ACTION_EXISTING` | `ValidateResourceManifest` | Context and repository validation |
| Explicit-path resource identity refresh | `ACTION_EXISTING` | `RefreshResourceManifest` and read-only CLI | Resource authors and future `develop-harness-resources` |
| Root-confined resource selection and hashing | `ACTION_EXISTING` | `ResolveResource` | Resource consumers |
| Skill descriptor/resource closure | `ACTION_EXISTING` | `ValidateSkillResources` | Capability/resource routing |
| Ownership relation validation | `ACTION_EXISTING` | `ValidateOwnershipManifest` | Task preflight and local validation |
| Checkpoint lifecycle validation | `ACTION_EXISTING` | `ValidateCheckpointSet` | Chain evaluation and checkpoint skill |
| Chain active/blocked/ready evaluation | `ACTION_EXISTING` | `EvaluateChainState` | Local validation and planning |
| Checksum verification | `ACTION_EXISTING` | `ValidateChecksumManifest` | Local validation |
| Evidence-ID inspection | `ACTION_EXISTING` | `AuditEvidenceIdentifiers` | Test-evidence workflows |
| Structural Python test-evidence inspection | `ACTION_EXISTING` | `ValidatePythonTestEvidence` | Test-evidence skill and local gate |
| Explicit local profile/manifest composition | `ACTION_EXISTING` | `LoadLocalHarnessContext` | Local validation |
| Selected historical/live record normalization | `ACTION_EXISTING` | local `Adapt*` Actions and `SelectEvidenceModules` | Local validation only |
| Validation route selection and rollback facts | `ACTION_EXISTING` | `SelectValidationRoute` / `RollBackValidationRoute` | Route wrapper |
| Normalized parity comparison and aggregation | `ACTION_EXISTING` | `CompareShadowPair` / `ReplayShadowSuite` | Integration reviewer |
| Project-local validator composition | `ACTION_EXISTING` | `ValidateLocalRepository` | Maintained route consumers |
| Fixed repository skill-capability inventory validation | `ACTION_EXISTING` | `.pi/skills/validate_skill_capabilities.py` | Maintained local route |
| Maintained route execution/inspection | `ACTION_EXISTING` | `.pi/skills/validate_harness.py` and current replay wrapper | Root verification |
| Repository maintained-test conformance gate | `ACTION_EXISTING` | `validate_repository_test_evidence.py` | Authorized test-conformance tasks |
| Writer/reviewer authority, independence, and handoff | `DURABLE_AGENT` | 10 durable agent records | Task assignments |
| Paths, phases, assignments, checkpoints, gates, and successors | `TASK_STATE` | active chain/task/ownership/checkpoint records | Agents and skills as explicit inputs |
| Human-facing architecture and operation explanation | `DOCUMENTATION` | numbered harness pages and public harness docs | Humans and agents |
| Closed H2/H3/H4 command inventories and ceremony | `HISTORICAL_ONLY` | retained phase records/evidence | Historical reconstruction only |
| Phase-specific agent capability routing | `DUPLICATE_RETIRE` | durable agents plus accepted skill/Action destinations | Disabled historical agent files only |
| `inspect-task-state` procedural skill routing | `DUPLICATE_RETIRE` | `InspectTaskState` plus maintained CLI documentation | Current skill until bounded retirement |
| Legacy standalone evidence-ID AST policy | `DUPLICATE_RETIRE` | `AuditEvidenceIdentifiers` | Legacy CLI callers pending migration |
| General `assess-harness-cutover` procedure | `DUPLICATE_RETIRE` | route/parity Actions, architecture skill, and durable integration reviewer | A cutover task may compose them |

Counts from the 39 rows are:

| Classification | Count |
|---|---:|
| `SKILL_EXISTING` | 8 |
| `SKILL_UPDATE` | 0 |
| `SKILL_CANDIDATE` | 1 |
| `ACTION_EXISTING` | 21 |
| `ACTION_CANDIDATE` | 1 |
| `DURABLE_AGENT` | 1 |
| `TASK_STATE` | 1 |
| `DOCUMENTATION` | 1 |
| `HISTORICAL_ONLY` | 1 |
| `DUPLICATE_RETIRE` | 4 |
| `UNRESOLVED` | 0 |

## Candidate skill evaluation

### `develop-harness-resources` — accept as a proposal

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
- **Deterministic components outside the skill:** `ValidateResourceManifest`,
  `RefreshResourceManifest`, `ResolveResource`, `ValidateSkillResources`,
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
  cutover roles, current generic/local manifests and profiles, three maintained
  resource Actions, and retained skill-descriptor resources show repeated
  resource-boundary work across more than one closed task.

This candidate must not package H3 paths, H1 decisions, H4 cutover steps,
accepted hashes, or phase completion gates.

### `assess-harness-cutover` — reject

- **Potential trigger:** replacing one maintained harness implementation or route
  with another after both produce normalized observations.
- **Non-trigger conditions:** routine implementation/review, a deterministic
  correction, resource design, or a choice with no actual old/new runtime.
- **Possible procedure:** establish identical inputs, compare normalized results,
  classify differences, inspect route/rollback, review boundaries, and stop for
  any human choice.
- **Relationship to existing owners:** `CompareShadowPair` and
  `ReplayShadowSuite` own parity; route Actions own routing; `ValidateLocalRepository`
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
| Resource-manifest validation | `ValidateResourceManifest` | No duplicate tool |
| Explicit selected resource-identity refresh | `RefreshResourceManifest` | Maintained Action and read-only CLI added by the bounded refresh slice |
| Generic/local leakage detection | `ValidateResourceManifest` | No duplicate tool |
| Parity comparison | `CompareShadowPair`, `ReplayShadowSuite` | No duplicate tool |
| Route inspection/selection | `SelectValidationRoute`, `RollBackValidationRoute`; selected wrapper in `validate_harness.py` | No duplicate tool |
| Checksum verification | `ValidateChecksumManifest` | No duplicate tool |
| Evidence-ID inspection | `AuditEvidenceIdentifiers` | Retire duplicate legacy AST script after caller migration |
| Maintained validation-command inspection | `InspectTaskState` reports declared completion command | No duplicate tool |
| Capability-inventory inspection | `validate_skill_capabilities.py` validates the fixed repository inventory | Keep tool; do not create an Action until a second input contract needs a reusable public result |
| Checkpoint resolution record mutation | No Action; current skill prose specifies mutation | Propose `ResolveCheckpointDecision` |

`ResolveCheckpointDecision` should accept one immutable checkpoint record/identity,
expected unresolved status, normalized decision supplied by the human-matching
skill, preserved human response, authorized scope, resolved timestamp, and exact
record paths. It should return the transformed record and structured validation
without writing Git state, pushing, resuming work, selecting a successor, or
interpreting the human message. `ValidateCheckpointSet` remains the validator;
the new Action would own only the deterministic transition. Public-contract and
persistence review is required before implementation.

## Duplicate and historical retirement

The 24 phase agents remain disabled and retained. Their phase names, task IDs,
fixed paths, ownership assignments, checkpoint state, correction limits,
historical commands, acceptance mechanics, successor logic, and one-time
migration instructions are `HISTORICAL_ONLY` or `TASK_STATE`; none should enter a
skill. No active phase-specific role should be restored.

After accepted destination changes, retire only live routing or duplicate tools:

1. remove `inspect-task-state` from skill routing after maintained CLI docs cover
   its trigger, inputs, result interpretation, and stop boundary;
2. migrate callers from `.pi/skills/audit_evidence_identifiers.py` to the public
   evidence Action or a thin wrapper, then retire the duplicate AST policy; and
3. keep all historical agent files and old evidence unchanged.

## Recommended implementation sequence

Each slice is separately reviewable and affects one permitted owner class.
Nothing below is activated by this proposal. The completed manifest-refresh
vertical slice supplies deterministic maintenance for the future resource skill;
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
   Exact known task state now routes through maintained `InspectTaskState` usage;
   broad repository discovery, fixed reporting schemas, and duplicated
   orchestration and control-plane procedure were removed.
5. **Next proposed — update `resolve-human-checkpoint`.** Retain human-response
   matching and fail-closed authority judgment; specify the future Action
   boundary without embedding mutation mechanics.
6. **Implement one Action:** design, review, and implement
   `ResolveCheckpointDecision` with no Git/push/resumption side effects.
7. **Retire one existing skill:** move `inspect-task-state` invocation guidance to
   maintained command documentation, update its bounded consumers, and remove
   only that skill from live capability routing.
8. **Create one new skill:** implement the accepted
   `develop-harness-resources` proposal with one concise reference and existing
   Actions as deterministic owners.
9. **Retire one duplicate tool:** migrate the standalone evidence-ID script to
   `AuditEvidenceIdentifiers` and remove only that duplicate executable policy.
10. **Reconcile one bounded historical routing group:** verify the resource-phase
    agent group remains disabled after the new resource skill is accepted; update
    only current routing/inventory references, never historical files.

## Explicit deferred items

- `assess-harness-cutover` is rejected, not deferred for automatic creation.
- Machine-readable unification of skills, agents, Actions, wrappers, and lifecycle
  into a new capability inventory is deferred; the current fixed validator remains.
- Phase assumptions inside local compatibility adapters require a separate
  public-contract task before any removal or generalization.
- A Graphify execution wrapper is deferred because it would cross the external
  tool/dependency and command-runner boundary.
- SQLite/evidence redesign, review-dispatch idempotency, delegation validation,
  package extraction, historical-file deletion, and publication remain inactive.
- P3 and all scientific, numerical, external, protected, and release execution
  remain outside this proposal.

No harness-simplification chain entry is required for this bounded skill edit.
Recording Slice 4 completion here does not activate Slice 5. The next proposed
slice, `resolve-human-checkpoint`, remains inactive pending separate human
authorization.
