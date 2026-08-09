# Task JSON authority and allocation architecture

Request identity: `task-json-authority-architecture-1`
Task: `harness.simplification.docs-json.schema-projection`
Parent workflow: `harness.simplification.docs-json`
Attempt: `attempt-1`
Immutable revision: `bd3879e077bfac95b4b293167fbfed2e65c8d150`
Git tree: `9baba81b0866eea3e7f795a668f50b1f50bc9212`

## Problem

**Observed fact.** The active Task requires authoritative JSON control records
and deterministic full-page documentation projection, but it does not select
where complete Task records are allocated
(`.pi/tasks/harness.simplification.docs-json.schema-projection.md`).

**Observed fact.** Allocation changes a public persistence and serialization
boundary and is therefore human-owned under `AGENTS.md`.

**Inference.** Three materially distinct defensible allocations remain:
chain-embedded records, one central catalog, and one JSON file per Task. They
differ in authority locality, persistence granularity, failure isolation, Git
history, migration, and bounded-context behavior.

**Human choice.** Select the allocation model before defining fields, schemas,
fixtures, serializers, or generated pages.

## Observed current behavior

**Observed fact.** The chain owns `active_task`, automatic-successor policy,
ordered Task references, prerequisites, and lifecycle status
(`.pi/chains/harness-simplification.chain.json`).

**Observed fact.** Hierarchy, prerequisites, and sequence are distinct
relationships. Documentation cannot activate work, and only current explicit
human authority can activate a bootstrap Markdown Task
(`.pi/tasks/harness.simplification.docs-json.md`).

**Observed fact.** `TaskReference` is a narrow immutable generic view rather
than a complete persisted Task. `ChainView` and `ChainStateEvaluator` do not
dispatch or mutate work (`python/src/ksdft2effmass/harness/pi/chains.py`).

**Observed fact.** `TaskRecordAdapter` currently combines caller-supplied
Markdown, chain, and activation bytes using project-local compatibility policy
(`python/src/ksdft2effmass/harness/pi/local/adapters.py`).

**Observed fact.** `TaskStateInspector` resolves one exact Task through an exact
chain reference and reads only declared paths
(`python/src/ksdft2effmass/harness/pi/task_state.py`).

**Observed fact.** Existing generic Task-reference and chain schemas do not
constitute a complete project Task persistence contract
(`harness/pi/schemas/records/task-reference.schema.json` and
`harness/pi/schemas/records/chain-view.schema.json`).

**Observed fact.** The documentation-correction handoff selects the Task family
as pilot but leaves authoritative fields and allocation undecided
(`.pi/tasks/harness.simplification.docs-json.documentation-correction.md`).

**Inference.** Accepted generic views constrain validation and projection but do
not determine project-local allocation.

## Decision requirements

**Observed fact.** Explicit human activation and disabled automatic successor
activation must remain; readiness, ordering, hierarchy, or documentation cannot
activate work.

**Observed fact.** JSON owns selected control fields; generated pages are
complete deterministic projections and never authority inputs.

**Observed fact.** Task vocabulary, schemas, fixtures, paths, and profiles remain
project-local. Generic validators/renderers receive explicit bytes and cannot
depend on `.pi/` or project identities.

**Observed fact.** Migration is a pre-release hard cutover without aliases or a
dual-read compatibility layer.

**Observed fact.** SQLite, event logs, CPN semantics, dispatch, scientific
authority, protected execution, publication, and release remain excluded.

**Human choice.** Decide whether complete Tasks are allocated to chains, one
central catalog, or individual Task files.

**Deferred question.** Exact fields, lifecycle vocabulary, hierarchy encoding,
fixtures, projection profile, and generated-page path follow the allocation
decision.

## Option A

**Conceptual model**
Each chain JSON embeds the complete authoritative Task records that it owns,
while keeping Task data, hierarchy, prerequisites, sequence, and activation as
separate fields.

**Authority**
The chain aggregate owns both Task-local data and chain relations; generated
pages remain derived, and activation remains an explicit human-authorized fact.

**Ownership/dependency**
Project-local schemas own the aggregate. Generic validation and rendering use
only explicitly supplied bytes and schemas.

**Runtime/dispatch**
One aggregate read supplies a chain and its Tasks. Validation must distinguish
relations despite colocation and cannot dispatch work.

**Migration**
Merge each selected Markdown Task and chain entry into its owning chain, validate
the aggregate and projection, then remove migrated Markdown authority.

**Reversibility**
Git can revert a chain aggregate, but moving a Task between chains changes its
authoritative file allocation.

**Failures**
A malformed aggregate blocks every Task in that chain; within-chain updates are
atomic in one file.

**Complexity**
The read path is simplest, but the combined schema and relational validator are
broad.

**Maintenance**
Small isolated chains are easy; large chains create contention and unrelated
diffs.

**Context-window consequences**
Exact Task review may require loading a large chain aggregate.

**Future compatibility**
Chain-local use is direct, but reusable Tasks and multiple chain views are
awkward.

**Advantage**
Strong within-chain atomicity and minimal file resolution.

**Risk**
The chain becomes an oversized authority and conflict surface.

## Option B

**Conceptual model**
One project-local JSON catalog owns every complete Task. Chains contain only
references plus chain-owned sequence and activation relations.

**Authority**
The catalog owns Task-local fields, hierarchy, and prerequisites; chains own
membership, sequence, and activation.

**Ownership/dependency**
Project-local catalog and reference schemas own vocabulary. Generic mechanics
consume explicit inputs without repository discovery.

**Runtime/dispatch**
Project-local code joins one catalog with a selected chain and validates
referential integrity before constructing narrow generic views.

**Migration**
Collect selected Tasks into one catalog, replace chain data with references,
validate projection and joins, then remove migrated Markdown authority.

**Reversibility**
Git can revert catalog and chain files; later partitioning requires another
allocation migration.

**Failures**
A malformed or conflicted catalog blocks every Task consumer; catalog/chain skew
must fail closed.

**Complexity**
Global uniqueness is straightforward, but global validation and cross-file
agreement are required.

**Maintenance**
Central lookup is simple, while unrelated Task edits contend on one file.

**Context-window consequences**
The full catalog has the largest routine context unless safely preselected.

**Future compatibility**
Global identities and multiple chain views are supported, but growth pressures
the monolithic file.

**Advantage**
One unambiguous global Task authority.

**Risk**
A monolithic failure, merge-conflict, and context boundary.

## Option C

**Conceptual model**
Each Task has one authoritative project-local JSON file. Chains reference those
files and own only membership, order, active-task relation, and explicit human
activation facts.

**Authority**
Task files solely own Task-local fields; chains solely own chain relations.
Validators reject duplicate identities, missing references, and cross-record
contradictions.

**Ownership/dependency**
Project-local schemas own Task vocabulary and path policy. Generic actions
receive exact Task, chain, schema, and projection bytes explicitly.

**Runtime/dispatch**
Project-local code resolves the exact selected chain and referenced Task files,
validates them, and constructs narrow generic views without activation or
dispatch.

**Migration**
Convert each selected Markdown Task to one JSON file, update chain references,
validate the family and generated page, then remove migrated Markdown authority.

**Reversibility**
Git can revert one Task, chain references, or the complete cutover commit while
preserving stable Task identity.

**Failures**
A malformed Task primarily blocks itself and its consumers. Missing or partial
cross-file updates fail closed; Git commits provide coherence.

**Complexity**
There are more files and joins, but intrinsic Task validation and cross-record
validation remain separable.

**Maintenance**
Task-local ownership, diffs, review, and generated inputs stay bounded.

**Context-window consequences**
The selected chain and exact referenced Task files provide the smallest normal
context, matching `TaskStateInspector`.

**Future compatibility**
Multiple chain views, generated non-authoritative catalogs, and later adapters
remain possible without changing Task ownership.

**Advantage**
Best authority locality, reviewability, failure isolation, and bounded context.

**Risk**
Cross-file integrity requires disciplined fail-closed project-local validation.

## Three-option comparison

| Criterion | A: chain aggregate | B: central catalog | C: file per Task |
|---|---|---|---|
| Task authority | Owning chain | Global catalog | Individual Task file |
| Failure isolation | Chain-wide | Repository-wide | Primarily Task-local |
| Git contention | High for large chains | Highest | Lowest for unrelated Tasks |
| Bounded inspection | Weak | Weak without extraction | Strong |
| Cross-chain use | Awkward | Direct | Direct |
| Atomicity | One chain file | Coherent catalog/chain commit | Coherent Task/chain commit |
| Migration | Few aggregates | One large aggregation | Direct file-for-record cutover |
| Generic/local boundary | Preserved | Preserved | Preserved |

**Inference.** A optimizes chain-local atomicity, B optimizes global lookup, and C
optimizes authority locality, bounded context, and failure isolation.

## Recommendation

**Recommendation.** Select **Option C — one authoritative JSON file per Task
referenced by chains**.

**Inference.** It matches the existing exact record-reference and
`TaskStateInspector` boundaries while replacing rather than centralizing
transitional Markdown authority.

**Implementation consequence.** If selected, define Task-owned fields separately
from chain-owned sequence and activation before authoring schemas or fixtures.
This recommendation does not select those fields or authorize implementation.

## Deferred questions

**Deferred question.** What is the smallest complete Task field set?

**Deferred question.** Does hierarchy use one parent reference, child references,
or both with one canonical owner?

**Deferred question.** What cross-record invariant relates chain `active_task` to
Task lifecycle without conflating them?

**Deferred question.** How is explicit human activation linked to durable human
decision evidence?

**Deferred question.** What projection profile and generated-page path are used?

**Deferred question.** How is human-authored intake retained after control fields
move to JSON?

## Human decision required

**Human choice.** Select exactly one architecture:

- **A — Chain-owned aggregate:** complete Tasks are embedded in one owning chain.
- **B — Central catalog:** one authoritative Task catalog is referenced by chains.
- **C — File per Task:** one authoritative JSON file per Task is referenced by chains.
- **D — Reconsider or defer:** retain the bootstrap boundary and stop schema work.

**Implementation consequence.** Selection authorizes only the allocation basis
inside the active Task. It does not select fields, accept a schema, implement
code, activate a successor, or grant scientific or protected authority.
