# WorkflowRun implementation plan

## Status and identity

**Status: human-accepted implementation, administratively closed.** This page retains
the maintained implementation plan for `migration.v2.workflows.workflow-run`; the
canonical Task record owns the exact lifecycle state and accepted result. The exact v2 owner is
`ksdft2effmass.workflows`; the normative aggregate contract remains
[WorkflowRun object model](../../../v2/ksdft2effmass/workflows/workflow-run.md).

The preserved human response `1A, 2A` selects private staging until Task-complete
closure and distinct append-only attempt-state record identities sharing one stable
attempt identity. This page does not itself grant implementation, persistence, protected execution,
automatic succession, release, or publication authority. Task lifecycle, operation
authority, acceptance, and selection remain owned by the applicable human instructions
and canonical Task and selection records.

## V1 source responsibilities

Architecture v1 contains no public scientific `WorkflowRun` aggregate. Existing shell
sequencing, calculation outputs, development Task state, provenance records, and
historical evidence are inputs to the ownership analysis only. They are not migrated,
backfilled, relabeled, or represented as historical WorkflowRun state.

The implementation consumes accepted v2 contracts from:

- `ksdft2effmass.workflows.model` for ResultObject, Task, Workflow, TaskInstance,
  TaskActivation, operation, attempt, and run identities;
- `ksdft2effmass.workflows.cpn_adapter` for effect-free Workflow-to-generic-selection
  correlation;
- `ksdft2effmass.workflows.artifacts` for existing artifact and producer-provenance
  contracts; and
- `ksdft2effmass.petrinet.colored` for immutable definitions, markings, enablement,
  selection, firing inputs, firing results, and pure firing.

There is no v1 WorkflowRun import, schema, fixture, serializer, or compatibility alias
to retain.

## Target concern and exclusions

This Task owns immutable in-memory WorkflowRun aggregate state, aggregate-owned record
families, intrinsic record invariants, exact cross-record identities, and the
effect-free `WorkflowRunReplayer` ActionObject. It owns the represented scientific run,
not the physical calculation, calculator process, generic Petri-net semantics,
scientific conclusion, or development lifecycle.

The Task-complete aggregate must cover:

- the stable run identity, immutable revision identity, exact Workflow definition and
  runtime-bundle references, and initial/current markings;
- run-scoped Task instances, ordinary and nested membership, activations, append-only
  attempt history, closed invocation outcomes, failures, and retries;
- ResultObject references, result production, explicit dependencies, exported-child
  admission, and references to the already-owned artifact/provenance contracts;
- origin-discriminated task and scientific-decision transition records in one canonical
  ordered history;
- nested Workflow invocation correlation without embedding child marking or history;
- scientific execution authority, reservation/claim, request, dispatch outcome,
  obligation, and disposition records required to represent control state without
  performing effects;
- scientific-decision request and resolution records required by the aggregate; and
- deterministic replay from one explicit immutable runtime bundle, with closed
  `equal`, `unequal`, `unsupported_version`, and `error` results.

The Task excludes Task invocation, scheduling, calculator or integration imports,
external effects, grant creation or authentication, response prompting or
interpretation, result-ingress actions, persistence transactions, validation at the
repository boundary, serialization, SQLite, read models, scientific analysis,
scientific validation, uncertainty quantification, and acceptance.

## Containment decomposition

The canonical Task remains one leaf Task. The stages below are implementation slices,
not child Tasks and not independent completion claims.

| Stage | WorkflowRun-owned output | Exit condition |
|---|---|---|
| 0. Contract closure | Exact record inventory, attempt-history representation, and public-rollout disposition | Every public field and variant needed by later stages has one owner; pending human-owned choices are resolved |
| 1. Task-origin core | Run/revision/runtime records, Task instances, activations, append-only attempts, outcomes, failures, task-origin transitions, and result-production/dependency correlations | Constructors and aggregate closure fail closed; non-success outcomes cannot claim firing or results |
| 2. Membership and nested runs | Workflow membership, distinct child-run correlation, terminal-child observation, and explicit export/admission references | Parent and child state remain separate; replay-equal terminal-child and explicit-export prerequisites are representable without cross-run atomicity |
| 3. Control-state and decision records | Authority/reservation/claim, request/dispatch/obligation/disposition, scientific-decision request/resolution, and the scientific-decision transition origin | Records represent exact state and prohibit effects, authority creation, raw-response authentication, and Task identities on no-Task decision ingress |
| 4. Complete replay and aggregate closure | One origin-complete `WorkflowRun`, explicit runtime bundle, `WorkflowRunReplayResult`, and `WorkflowRunReplayer` | Both transition origins replay canonically; every retained reference closes; all four replay outcomes satisfy their exact claim boundaries |
| 5. Public integration | Approved package exports, complete source docstrings, API and concept documentation, and maintained software-verification evidence | The selected public-rollout policy is satisfied and every Task completion criterion is verified |

No stage closes the Task by itself. Persistence, control Actions, and read-model Tasks
remain separate successors.

## Planning cascade

Planning covers only `migration.v2.workflows.workflow-run`. Its implementation may
proceed sequentially through Stages 0–5 after separate activation and prerequisite
resolution. One writer owns the source and synchronized public documentation in the
shared checkout unless a later operation introduces an explicit non-overlapping
ownership manifest. Maintained test evidence follows its declared ownership resource
and does not become an independent implementation authority.

The stage order prevents later control or persistence contracts from forcing reverse
dependencies into `WorkflowRun`. Planning may inspect successor requirements, but this
Task does not implement successor Actions or repositories.

## Implementation approach

### Object ownership

| Concern | Owner | WorkflowRun use |
|---|---|---|
| Intrinsic validity of one immutable run record | That WorkflowRun DataObject | Constructor checks exact types, closed variants, and local invariants only |
| Cross-record aggregate and replay closure | `WorkflowRunReplayer` for replay-relevant closure; future persistence validator for commit-bound structural closure | Replayer receives explicit run and runtime bundle and performs no ambient discovery |
| Generic marking, enablement, selection, and firing | `ksdft2effmass.petrinet.colored` | Retain and replay exact public generic values; do not duplicate generic semantics |
| Workflow activation mapping | `ColoredPetriNetWorkflowAdapter` | Correlate retained activation and firing-input identities; do not invoke the adapter during persistence |
| Artifact manifests and producer provenance | `ksdft2effmass.workflows.artifacts` | Store exact references and result/artifact relation identities; do not redefine producer variants |
| Dispatch, reconciliation, and result-ingress behavior | `migration.v2.workflows.control-ingress` | WorkflowRun defines only the immutable state consumed or produced by those later Actions |
| Transaction validation, wire, and repository | `migration.v2.workflows.persistence` | WorkflowRun supplies the complete in-memory aggregate; no serializer or store method is placed on DataObjects |
| Read-only projections | `migration.v2.workflows.read-models` | Consume exact run and artifact identities without creating authority |

### Attempt-history requirement

The human-selected attempt model uses one stable `AttemptIdentity` and distinct
append-only attempt-state record identities. Each later state record names the exact
predecessor state record; terminal closure and retry history retain every prior record.
No successor revision replaces a state record, and a new retry uses a new stable
`AttemptIdentity` while identifying the exact predecessor attempt. A single unique
attempt record whose status is replaced in a successor revision is prohibited.

### Stage 0 field inventory

Every identity named below is a frozen nominal identity with a nonempty exact built-in
string value unless an accepted upstream owner already supplies the type. Every
collection is a tuple with explicit canonical ordering and unique record identities.
Origin- or outcome-specific state uses closed variants rather than unrelated optional
fields. Exact wire encodings remain deferred to the persistence Task.

| Record family | Required in-memory fields and variants | Owner and closure rule |
|---|---|---|
| `WorkflowDefinitionReference` | `workflow_identity`, Workflow definition version, colored-Petri-net definition identity/version, canonically ordered Task-definition identities, and schema version | WorkflowRun owns the reference; it contains no executable closure or ambient lookup |
| `WorkflowRuntimeBundle` | Bundle identity, exact definition reference, immutable `ColoredPetriNetDefinition`, Task-definition identities, and adapter, evaluator, ordering, enabler, selector, and firer implementation identities | WorkflowRun owns replay input; replay never invokes a Task or discovers a latest version |
| `TaskWorkflowMembership` | Membership identity, run identity, Workflow identity, and member Task-instance identity | WorkflowRun owns ordinary within-run membership; membership grants no prerequisite or authority claim |
| `NestedWorkflowMembership` | Membership identity, parent run/revision and parent Task-instance identities, child Workflow definition and distinct child-run identities | WorkflowRun owns cross-run correlation; parent stores no child marking or transition history |
| `TaskAttempt` | `TaskAttemptRecordIdentity`, stable `AttemptIdentity`, run, Task-instance, activation, operation, exact status, predecessor attempt-state record identity, and optional retry-of attempt identity | Multiple state records may share one stable attempt identity; record identities are unique and append-only; the initial record has no state predecessor, and every later state names the immediately preceding record |
| `TaskInvocationOutcome` | Outcome identity, run, activation, operation, stable attempt and terminal attempt-state record identities, plus one closed variant: confirmed results/production-record identities; rejected failure-record identity; or indeterminate reconciliation identities | Exactly one effective terminal outcome per attempt; only confirmed carries results and may support firing |
| `TaskFailureRecord` | Failure-record identity, run, Task-instance, activation, operation, stable attempt and attempt-state record identities, applicable request/child-run identities, phase, structured failure, and explicit no-successful-firing claim | WorkflowRun owns correlation; the producing Task domain retains its failure-code meaning |
| `ResultObjectReference` | Reference identity, concrete immutable `ResultObject`, concrete-type identity, owning-domain identity, content identity, and exactly one closed producer-provenance variant | WorkflowRun owns result correlation, not the concrete result's intrinsic scientific invariants |
| Result producer provenance | Represented-Task producer with exact run/Task/activation/attempt/outcome/production identities; represented scientific-decision ingress producer with request/transition/recorder/source/authority identities and no Task fields; or explicit external, imported-retained, human-authored, or unknown-legacy provenance with actual evidence and limitations | WorkflowRun owns ResultObject provenance variants; existing artifact provenance types are referenced rather than copied and historical provenance is never invented |
| `ResultProductionRecord` | Production identity, run, producing Task-instance, activation, operation, stable attempt, terminal attempt-state, confirmed outcome, result-reference, result/artifact relation identities, and exact generic external-output binding | Every confirmed Task-produced or explicitly exported-child result used by a task-origin firing has one exact production/admission record |
| `ResultDependency` | Dependency identity, result-reference identity, producer run identity when represented, consumer run and Task-instance identities, optional consumer activation identity, and exact Task input name | Dependency is independent of membership; cross-run consumption and child export admission remain explicit |
| `NestedWorkflowInvocation` | Invocation identity, parent run/revision, parent Task-instance, activation, operation, stable attempt and attempt-state record, child Workflow definition, distinct child-run, input result-reference identities, child-creation idempotency identity, and one pending/confirmed/rejected/indeterminate terminal-observation variant | Confirmed alone names one replay-equal terminal child revision and explicit exported result references; uncertain creation is reconciled by exact child/idempotency identities without duplicate creation |
| Execution request and authority references | Request-correlation identity; exact run/Task/activation/operation/attempt/request/executor/obligation/grant identities; `ScientificExecutionAuthorityReference` with grant, revision, snapshot, and state identities; and the exact authorization-result identity | WorkflowRun records externally supplied authority state and correlations but never issues, authenticates, broadens, or consumes a grant by itself |
| `AuthorityReservationOutcome` | Reservation identity, run/revision, grant/snapshot/authorization-result, request, activation, operation, stable attempt and attempt-state record, obligation, expected revision, and exact reserved/claimed state with predecessor reservation identity | Reservation and claim are distinct append-only records; only one successful claim exists for one obligation |
| `DispatchOutcomeRecord` | Record identity, exact specialized envelope identity, request, Task/activation/operation/attempt/executor/obligation/grant correlations, and confirmed/rejected/indeterminate variant | Confirmed alone references the returned ResultObject; indeterminate invents no result and retains reconciliation identities |
| `SimulationDispatchObligation` | Obligation identity, run/revision, request, Task/activation/operation/attempt/executor/grant identities, immutable destination/resource-scope identities, and creation idempotency identity | The record represents durable pending work but performs no dispatch |
| `ObligationDisposition` | Disposition identity, obligation, request, dispatch-outcome, attempt-state and predecessor-disposition identities, plus confirmed/rejected/indeterminate/completed variant | Dispositions are append-only and cannot authorize redispatch |
| `ScientificDecisionRequest` | Request identity, question, canonically ordered options, declared scope, affected Workflow/run/Task/transition identities, required response-source and authority-context identities, and request definition/version | The request pauses only its represented branch and creates no Task or authority |
| `ScientificDecisionResolution` | ResultObject identity/content identity, exact request, verbatim response, one normalized option, direct response-source and authority-context identities, optional actually available boundary-receipt reference, predecessor/supersession resolution identities, and represented scientific-decision-ingress provenance | Initial resolution has no predecessor; correction names and supersedes the exact effective predecessor; no Task/activation/attempt fields are permitted |
| `TaskWorkflowTransitionRecord` | Transition-record and canonical-sequence identities/index, definition/runtime identities, predecessor marking and identity-closed firing input/result/audit/produced values/successor marking, plus exact activation, operation, stable attempt, terminal attempt-state, confirmed outcome, production, request, and applicable dispatch identities | Task origin prohibits scientific-decision fields and requires complete confirmed result closure |
| `ScientificDecisionWorkflowTransitionRecord` | The same generic transition and canonical-sequence fields plus exact decision request/resolution and decision-ingress provenance identities | Decision origin prohibits Task, activation, attempt, Task outcome, and Task result-production fields |
| `WorkflowRun` | Stable run identity, immutable revision identity and predecessor revision identity, definition/runtime references, schema and implementation identities, initial/current marking records, and canonically ordered tuples of every applicable record family above | One immutable snapshot-plus-history aggregate; every successor preserves all predecessor records and appends only identity-closed state |
| `WorkflowRunReplayResult` | Result identity, exact run/revision/runtime-bundle identities, equal/unequal/unsupported-version/error variant, reconstructed marking only for completed equal/unequal replay, ordered issues, and claim boundary | ResultObject owned by replay; it establishes deterministic represented reconstruction only |

Stage 0 uses the following aggregate rules:

1. record identity uniqueness and canonical sequence order are independent from stable
   operation, attempt, run, request, result, grant, and obligation identities;
2. a new WorkflowRun revision names its exact predecessor revision and contains a
   superset of predecessor history, except that the separately stored current marking
   advances to the last retained successor marking;
3. current/effective state is derived from the last valid append-only record, never by
   deleting or replacing an earlier record;
4. every successful transition closes over its origin-specific records and exact
   generic output binding in the same represented successor;
5. rejected and indeterminate variants carry no successful firing or fabricated
   ResultObject;
6. parent and child run histories, aggregate revisions, and persistence streams remain
   distinct; and
7. constructors own only intrinsic field/variant rules, while replay owns deterministic
   reconstruction and the later persistence validator owns complete commit-bound
   structural closure.

Under selected private rollout, none of these incomplete record families is added to
`ksdft2effmass.workflows.__all__`, the public API page, or the implemented concept page
before Stage 5. Provisional package-root exports and prose must be withdrawn or kept
unaccepted until the Task-complete public gate.

### Paths

All scientific Workflows use colored-Petri-net semantics. WorkflowRun is therefore one
concrete CPN-semantic aggregate contract rather than a generic protocol with pluggable
execution-model implementations. The implementation is organized under
`ksdft2effmass.workflows.runs` by object ownership: nominal identities, immutable run
records, aggregate closure, and effect-free replay. These modules are not lifecycle
stages or a directed-acyclic-graph execution model.

The authorized implementation plan is limited to these prospective maintained paths:

- `python/src/ksdft2effmass/workflows/runs/{__init__,identities,records,aggregate,replay}.py`;
- `python/src/ksdft2effmass/workflows/__init__.py` only for approved public exports;
- `python/tests/software_verification/ksdft2effmass/workflows/runs/**`;
- `docs/api/workflows.rst` for approved public API documentation; and
- `docs/concepts/scientific-workflow-model.rst` for implemented concepts.

The normative v2 architecture changes only if a later human decision changes the
accepted target. No schema, public wire, fixture family, dependency, or source-tree
move is introduced by this Task.

## Prerequisite results

Declared Task prerequisites are:

- `migration.v2.workflows.model`;
- `migration.v2.workflows.cpn-adapter`; and
- `migration.v2.workflows.artifacts-provenance`.

Their lifecycle labels do not by themselves establish implementation eligibility.
Before implementation activation, the operation must resolve each prerequisite to its
exact retained accepted result or closeout receipt and bind the applicable immutable
inputs. Missing or conflicting prerequisite evidence stops implementation without
changing this plan. No external prerequisite or protected scientific execution is
required.

## Conditional human decisions

### Public rollout

The exact in-memory field contract is a public-contract boundary because package-root
exports and Sphinx documentation make constructor and variant behavior externally
observable.

The preserved human response `1A, 2A` selects **Option A — private staging until
Task-complete closure**. Incomplete stages remain unexported implementation details.
Stage 5 exposes the cohesive public contract only after all aggregate families and
replay are verified. Existing or proposed package-root exports remain provisional and
cannot establish the accepted public contract before that gate.

The unselected alternative was incremental public contracts, under which each stage
would have required separate explicit human acceptance of its exact field/variant
contract and compatibility consequences.

The same response selects distinct append-only attempt-state record identities sharing
one stable attempt identity, with exact predecessor linkage. Stage 0 must define the
corresponding fields consistently; routine implementation convenience cannot replace
or collapse history.

No separate human decision is required for the Task/successor ownership split because
the accepted architecture already determines it.

## Verification

All tests in this Task are software verification. They establish represented software
behavior only and make no numerical-verification, scientific-validation, uncertainty-
quantification, authority, execution, or acceptance claim.

| Verification facet | Required evidence |
|---|---|
| Intrinsic records | Exact-type rejection, closed variant fields, booleans rejected as integers, immutable tuple shape, unique record identities, and local predecessor rules |
| Aggregate closure | Missing, duplicate, stale, cross-run, cross-Workflow, and mismatched activation/attempt/outcome/result references fail closed |
| Attempt history | Started, terminal, retry, and indeterminate histories preserve every prior record and reject self, stale, duplicate, or out-of-order predecessors |
| Result flow | Confirmed outcomes close over every produced or exported ResultObject and generic output binding; rejected and indeterminate outcomes produce no successful firing |
| Nested runs | Parent and child identities remain distinct; parent contains no child marking/history; only explicit exports from an exact replay-equal terminal child are admissible |
| Transition origins | Task origin requires Task correlations and prohibits decision fields; scientific-decision origin requires request/resolution and prohibits Task/attempt/result-production fields |
| Authority and obligations | Reservation/claim and obligation/disposition variants are exact and append-only; records perform no authorization or effect |
| Replay equality | Hand-inspectable public CPN examples independently establish empty, one-step, multi-step, retry/non-success, nested-reference, and both-origin histories |
| Replay failures | Unsupported runtime identities, noncanonical order, broken predecessor/successor links, stale selection identities, firing mismatch, ambiguous output binding, and unequal current marking return the correct closed variant |
| Public surface | The exact approved export inventory, source docstrings, API page, and concept page agree; prohibited provisional names are absent under Option A |

Tests use explicit class or artifact ownership, stable evidence identifiers, public
contracts as oracles, exact equality for exact records, and semantic parameter IDs.
The affected tests run first, followed by Ruff, targeted mypy, maintained Python
conformance, the broader pytest suite required by the activated implementation, Sphinx
with warnings as errors, Harness validation, synchronized projection checking, and
`git diff --check`. A passing check establishes only its declared software claim.

## Cutover, retirement, and rollback

WorkflowRun is an introduction, not a replacement import. No v1 alias, legacy adapter,
historical backfill, calculation rerun, or provenance reclassification is required.
The provisional pre-acceptance `workflows.workflow_run` module was replaced by the
concrete CPN-semantic `workflows.runs` package before closeout; package-root public
imports remain stable, and no obsolete-module compatibility facade is retained.
Existing external calculation artifacts remain in their actual locations with their
actual identities and limitations.

After acceptance, rollback must preserve the accepted package-root contract or use a
separately authorized compatibility change. The human-authorized administrative
closeout occurred only after all stages, required checks, public-contract decisions,
prerequisite results, and Task completion criteria agreed. Automatic successor
activation remains disabled.

## Residual limitations

- Selected private-rollout Option 1A and append-only attempt-history Option 2A are
  implemented in the accepted exact in-memory contract; the Stage 5 public gate is
  complete.
- Exact WorkflowRun wire fields, serializer behavior, transaction validation,
  repository composition, SQLite policy, and compaction remain with the persistence
  Task.
- Control Actions, dispatch effects, reconciliation, result ingress, scientific-
  decision recording, and terminal-state advancement remain with the control-ingress
  Task even though the aggregate records their state.
- Exact nested terminal/export wire forms, cancellation, compensation, and history
  retention policy remain deferred under the normative architecture.
- No historical calculation is evidence of WorkflowRun replay unless it is represented
  through a separately authorized, non-fabricated WorkflowRun construction.
