# Task catalog configuration: selected direction and recording scope

## Human instructions

The human proposed:

> i think tasks should be organized under tasks/research tasks/simulation tasks/software

After the assistant described migration of the existing canonical catalog rather
than creation of a second catalog, the human added:

> yes and make this configurable, i think we should start building a configuration object

Inspection identified the existing immutable `HarnessConfiguration` and its
`HarnessCatalogConfiguration` in `python/src/ksdft2effmass/harness/configuration.py`.
The assistant recommended configuring Task organization first through that
existing aggregate, with an immutable nested `TaskCatalogConfiguration`, rather
than starting a project-wide configuration framework. The proposed scope was to
update consumers and then migrate records while preserving Task identities,
dependencies and history; scientific parameters, execution settings and
credentials remain outside the object.

The human asked:

> where should we record this?

The assistant proposed recording the design in
`docs/architecture/v2/ksdft2effmass/harness/configuration.md`, tracking implementation
as one software Task under the current canonical `harness/tasks/`, and changing
`harness/configuration.json` only after the configuration model and consumers
support the new layout. The human answered:

> proceed

## Initial recording operation

This instruction selects the Task-organization-first direction and authorizes its
durable recording: the owning architecture section, this authority record, one
unactivated implementation Task, and necessary generated projection updates.

The Task identity is `harness.task-catalog-configuration`. Its current canonical
path is `harness/tasks/harness.task-catalog-configuration.json`; after the separately
activated migration it belongs under the configured software Task root, retaining
that same identity.

This recording does not activate implementation, change runtime configuration,
move Task records, grant scientific execution authority, or complete any new
configuration capability. Selection remains empty and automatic successor
activation remains disabled. No subagent delegation, dependency change, staging,
commit, push or protected action is included.

## Subsequent activation for planning

The assistant recommended activating `harness.task-catalog-configuration` for a
bounded implementation plan: exact configuration fields and compatibility,
affected consumers, a classification/migration map, and relevant verification.
The question was:

> Authorize activation and planning?

The human answered:

> yes and use adverserial skill

This explicitly selects and activates this Task **for planning only**. The parent
uses the `adversarial-thinking` skill directly to challenge assumptions, source-path
preservation, confinement, compatibility and classification. This is a parent
self-challenge, not independent review or authorization to launch subagents.

The permitted changes are the Task and selection, this authority record, bounded
planning/inventory records, links from the owning architecture page, and generated
projections through their maintained commands. No runtime configuration, Python
implementation/test source, Task relocation, scientific execution, dependency,
commit or push is authorized. Automatic successor activation remains disabled.
Implementation authorization and any genuinely unresolved public-contract or
classification decision remain separate from this planning activation.

## Approved configuration compatibility and classification choices

After the planning self-assessment, the assistant asked for approval of two
choices: a new Harness configuration format retaining existing flat-configuration
reading, and the proposed destinations for five mixed-purpose Tasks. The complete
field and compatibility proposal is retained in
`harness/reports/task-catalog-configuration-plan.md`.

The human answered:

> these choices are approved and authorized

Normalized decisions, distinct from the verbatim response:

1. Select Harness configuration schema 2 for the categorized layout while
   preserving schema-1 flat decoding and exact re-encoding. This does not change
   Task record, Pi, WorkflowRun or scientific-specification versions.
2. Confirm these five destinations, with no change to their Task meanings,
   lifecycle, prerequisites or execution authority:

   | Task ID | Category |
   |---|---|
   | `abinit.tutorials.basic2-h2-convergence` | simulation |
   | `abinit.tutorials.basic3-silicon` | simulation |
   | `abinit.tutorials.basic4-aluminum` | simulation |
   | `quantumespresso.simulations.review` | simulation |
   | `bulk-silicon.tight-binding.wannier.bridge` | software |

These choices are now authorized inputs to the bounded implementation, not
unresolved alternatives. The current operation records their resolution; it does
not itself implement the object, switch configuration, move Tasks or complete the
Task. The prior phase activation was planning only; this decision record does not
silently relabel it as implementation execution. Consumer support, verification
and the guarded cutover remain prerequisites to relocation. No independent review,
scientific acceptance, successor activation, delegation, Git closeout or protected
execution follows from the choices. No canonical checkpoint was created for these
planning questions, and this record does not fabricate a checkpoint lifecycle.

## Continuation into implementation

After both choices were recorded and the five destinations were clarified, the
human instructed:

> cotinue

In this context, continuation authorizes implementation of the selected Task under
the approved plan and decisions. It supersedes the earlier planning-only phase
restriction, not the Task's scientific, protected-action or Git exclusions. The
parent remains the sole writer; no delegation or independent review is inferred.
Implement the configuration value and wire contracts first, then the affected
catalog consumers. Keep the live configuration and canonical Task locations
unchanged until consumer support and preservation checks establish readiness for
the guarded cutover. Report completed slices separately from remaining work; do
not claim the Task complete after configuration-only verification.

## Superseding clean-cutover decision

After the value/wire slice, the assistant identified remaining flat-path assumptions,
old Markdown ownership bindings, an embedded one-off H5 identity rewrite, temporary
consumer guards, and the deliberately retained schema-1 configuration branch.
The human instructed:

> let's just migrate the historical compatiblity and update the records into the new format

This supersedes the earlier choice to preserve permanent flat-configuration support.
The selected target is a **clean categorized configuration cutover**: migrate the
applicable maintained records and live consumers to the current formats, then
retire obsolete compatibility paths rather than carry dual live layouts. Harness
configuration source/resolved schema 2 is the target; canonical Task records remain
schema 3, and current ownership records use their existing version-2 format. Pi,
resolution-result, snapshot-framing and scientific Workflow versions are not
implicitly changed. The separate list-valued status-details Task remains inactive.

The bounded operation includes consumer integration, live-reference and applicable
ownership-record migration, the classified Task relocation, and removal of the old
flat configuration branch and one-off Task identity rewriting once their inputs
have been reconciled. Do not switch the live configuration before the complete
consumer/cutover checks are ready. Original historical quotations, signed or
checksummed evidence and archived-source identities remain intact; a current
record/path migration must not fabricate past assignments, decisions or acceptance.
Material gaps in a record conversion must be reported, not filled by inference.
Existing IDs, lifecycle, relationships and scientific meaning remain unchanged.
No commit, push, delegation, successor activation or protected execution is granted.

## Subsequent removal of unused orphan ownership manifests

After the six orphan declarations were identified and a repository-reference check
found no current operational use, the human instructed:

> then remove them

This authorizes removal of exactly the six `harness-simplification.agents.*`
ownership manifests previously moved to `harness/archive/task-ownership/`:
`project-architecture`, `project-documentation`, `project-implementation`,
`project-integration-review`, `project-role-simplification`, and
`validator-migration-pilot`. It supersedes retention of those six copies only.
Keep the migration/removal audit, other historical records and the current Quantum
ESPRESSO integration ownership manifest. No Task activation, commit or push is
implied.

## Selected boundary

- Extend the existing Harness configuration composition, not a competing global
  configuration object or service locator.
- Configure exactly the research, simulation and software Task catalog locations;
  this project's intended locations are `tasks/research`, `tasks/simulation` and
  `tasks/software`.
- Classify records by their primary deliverable; dependencies may cross catalogs.
  Classification is not execution permission, scientific acceptance or lifecycle
  state. Research/simulation work records do not replace scientific `WorkflowRun`
  state.
- Preserve existing Task IDs, relationships, status and historical evidence.
  Migrate live path consumers coherently without retaining a second authoritative
  catalog or rewriting historical evidence to claim it originally used new paths.
- Keep exact public fields, wire compatibility and cutover behavior explicit in
  implementation planning before changing runtime consumers or canonical values.

This is a separate software concern, not a ninth Task silently added to the earlier
bounded eight-Task execution path. That operation's acceptance-pause waiver and
other Task-specific controls are not extended by this record. The existing research
protocols, scientific specifications and simulation settings retain their owners.
