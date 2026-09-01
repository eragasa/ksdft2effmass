# Harness Task, registry, and selection migration plan

## Status and identity

**Implementation result: human-accepted and closed.** The canonical Task is
`migration.v2.harness.task-model`, contained by `migration.v2.harness`. The accepted
`migration.v2.identity-contracts` result is its sole declared Task prerequisite. The
accepted implementation provides the authorized source, test, public-documentation,
and one-way compatibility slice without changing dependencies or wire versions.
Protected execution and successor activation remain unauthorized; automatic
successor activation remains disabled.

The v2 owner is `ksdft2effmass.harness`. Public Task, registry, serializer, and
selection contracts now reside there; temporary `harness.pi.local` imports resolve to
the same objects during consumer migration.

## V1 source responsibilities

The pre-cutover project-local foundation was split across these maintained surfaces.
The table is the compatibility baseline, not the candidate's current ownership map:

| Surface | Current responsibility | Compatibility significance |
|---|---|---|
| `python/src/ksdft2effmass/harness/pi/local/task_model.py` | `HarnessTask`, version-3 serializer/deserializer, `HarnessTaskRegistry`, and the local-result `HarnessTaskGraphValidator` | Public through `ksdft2effmass.harness.pi.local`; canonical Task JSON depends on its exact wire behavior |
| `python/src/ksdft2effmass/harness/pi/local/task_selection.py` | Immutable version-1 `DevelopmentTaskSelection` and its serializer/deserializer | Owns the exact `harness/task-selection.json` representation |
| `harness/local/schemas/task-record-v3.schema.json` | Closed Task-record wire shape | Agrees with runtime deserialization but does not define lifecycle meaning |
| `harness/local/schemas/task-selection-v1.schema.json` | Closed selection wire shape | Enforces structural shape and disabled automatic succession, not authority or receipt validity |
| `harness/tasks/*.json` | Canonical Task content, lifecycle text, containment, prerequisites, and supersession | Sole current development topology source; `harness/task-graph.json`, SQL, and SQLite are derived projections |
| `harness/task-selection.json` | Current selected Task and activation-receipt references | Selection only; grants no authority |
| `docs/api/harness-task.rst` | Maintained public Task and selection documentation | Currently documents the transitional `harness.pi.local` import surface |

The canonical repository currently contains multiple opaque lifecycle spellings,
including planning, blocked, inactive, deferred, superseded, completed, and several
human-accepted variants. Version-3 `HarnessTask.status` intentionally validates only
the project-local identifier grammar. Retired chain records under
`harness/archive/task-control-v1/chains/` additionally contain historical chain
status, task sequence, active-Task, explicit-activation, history, and protected-action
fields. They are non-operational history and are not inputs to current Task selection
or topology.

The former `python/src/ksdft2effmass/harness/pi/chains.py` public and wire
compatibility surface (`TaskReference`, `ChainView`, and `ChainStateEvaluator`) is
retired. Canonical Tasks and selection now own live topology and requested work state;
archived chain JSON remains non-operational history. Projection and subagent redesign
were not prerequisites for this conditionally accepted minimal cutover.

## Target concern and exclusions

This Task stabilizes the domain-owned immutable Task, registry, graph-query, and
selection contracts needed by v2 Harness consumers. It owns:

- intrinsic version-3 `HarnessTask` and version-1 `DevelopmentTaskSelection`
  behavior;
- strict serializers and deserializers for those already accepted wires;
- an immutable registry derived only from explicitly supplied canonical Tasks;
- exact direct-child, prerequisite, and recursive-descendant queries derived from
  Task fields; and
- lifecycle-applicability semantics sufficient to separate planning,
  implementation, and closeout without normalizing historical status text.

It does not own repository discovery, loading, normalized-state validation,
prerequisite-result resolution, authority reconstruction, operation authorization,
persistence, projection, automatic successor selection, Pi child orchestration, or
scientific Workflow state. `DevelopmentTaskSelectionValidator` remains owned by
`migration.v2.harness.validation`, and actual prerequisite matching remains owned by
`migration.v2.harness.prerequisite-resolution`.

## Containment decomposition

`migration.v2.harness.task-model` is one leaf Task and creates no child Tasks. Its
implementation is one bounded vertical slice:

1. establish the v2 public owner and one-way compatibility imports;
2. add the recursive descendant query;
3. synchronize focused software-verification and public documentation; and
4. retain exact wire and historical compatibility while leaving validation and
   chain retirement to their existing Tasks.

## Planning cascade

Planning may inspect the complete canonical Task set and retired chain fixtures to
establish compatibility. It activates no descendant or sibling. Later source
implementation is eligible only after separate explicit authorization binds the
accepted planning result, exact permitted paths, and accepted identity-contract
prerequisite result.

The produced Task-model result may satisfy declared implementation prerequisites for
consumer Tasks only after this Task is implemented, verified, and closed. Merely
selecting this planning Task, rendering this page, or passing a structural check does
not satisfy a prerequisite or authorize a consumer.

## Lifecycle applicability

Existing authority determines the following semantics; no new human choice is
required:

- `parent_task_id` expresses containment only. Parent planning, selection, status, or
  closure neither activates a child nor satisfies one of its prerequisites.
- Declared Task and external prerequisites do not block planning or implementation
  planning. Those phases may inspect and plan around absent future results.
- Source implementation requires actual retained results for every declared
  prerequisite plus separate operation authority. A producer's parent status,
  planning prose, selection, graph eligibility, or passing check is not a result.
- Closeout rechecks the exact implementation prerequisites and this Task's own
  completion claims. A parent closeout waits for child results only when its exact
  aggregate claim names those results.
- Selection records current requested work only. It does not interpret lifecycle
  status, prove eligibility, resolve a prerequisite, or grant authority.
- Automatic successor activation remains literal `false`; no graph query computes or
  writes a successor.

Version 3 retains `status` as opaque lifecycle text. This Task does not introduce a
closed status enum, rewrite the currently represented status spellings, infer one
status from another, or bump the Task wire version. The future prerequisite resolver
must consume explicit accepted status/result policy rather than embedding historical
string heuristics in `HarnessTask`, `HarnessTaskRegistry`, or
`DevelopmentTaskSelection`.

## Recursive descendant contract

Add `HarnessTaskRegistry.descendant_task_ids(root_task_id)` with this exact contract:

- input is one valid registered Task identity;
- output contains every distinct registered Task reachable from that root by one or
  more canonical `parent_task_id` edges;
- the root is always excluded, including when malformed input contains a parent
  cycle;
- output order is deterministic depth-first pre-order: visit each direct child in
  registry order, then that child's descendants by the same rule; this keeps parents
  before descendants without defining execution order;
- unknown or lexically invalid identities use the same `ValueError`/`TypeError`
  behavior as existing registry lookup;
- traversal is iterative so a valid deep tree does not depend on Python recursion
  depth;
- a reachable parent cycle raises `ValueError` rather than returning a truncated or
  apparently valid scope; complete missing-parent and cycle findings remain owned by
  `HarnessTaskGraphValidator`; and
- execution performs no repository discovery, mutation, selection, activation,
  prerequisite evaluation, or authority inference.

This is a registry query, not an ActionObject: it derives a trivial immutable view
solely from retained registry state and applies no external policy.

## Implementation approach

### V2 public owner

The authorized implementation:

1. Introduces `python/src/ksdft2effmass/harness/task.py` containing
   `ArchivedTaskSource`, `HarnessTask`, `HarnessTaskSerializer`,
   `HarnessTaskDeserializer`, and `HarnessTaskRegistry`.
2. Introduces `python/src/ksdft2effmass/harness/task_selection.py` containing
   `DevelopmentTaskSelection`, `DevelopmentTaskSelectionSerializer`, and
   `DevelopmentTaskSelectionDeserializer`.
3. Exports those names from `python/src/ksdft2effmass/harness/__init__.py` and makes
   that package the supported v2 import surface.
4. Converts `harness.pi.local.task_model` and `harness.pi.local.task_selection` into
   one-way compatibility modules that import and re-export the v2-owned objects.
   New v2 code must not import the transitional modules. Existing imports retain
   object identity during the compatibility period.
5. Keeps the local-result `HarnessTaskGraphValidator` on the transitional boundary
   until `migration.v2.harness.validation` supplies the normative v2
   `ValidationResult` contract and validator composition. Do not make the v2 Task
   model depend inward on `harness.pi.local.models`.

No dependency, schema version, canonical JSON field, fixture representation, or
Task-record rewrite is required.

### Selection-validation boundary

The Task and selection DataObjects retain intrinsic checks only. The future
`DevelopmentTaskSelectionValidator` consumes a normalized registry and selection and
reports, through the normative v2 `ValidationResult`, at least:

- selected Task identity exists;
- exact activation-reference applicability required by an explicitly supplied policy;
  and
- any lifecycle eligibility asserted by that policy is established from explicit
  retained inputs rather than guessed from opaque status text.

An inactive selection with receipt references remains structurally representable in
version 1. Receipt existence, authenticity, applicability, and authority remain with
the authority-context owner; this validator must not invent those facts.

It does not authenticate receipts, authorize work, resolve prerequisites, select a
successor, or mutate selection. This validator is specified here for interface
agreement but implemented by `migration.v2.harness.validation`.

### Evidence and documentation paths

Later implementation owns focused changes to:

- `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__HarnessTaskRegistry.py`;
- applicable existing class-owned serializer, deserializer, Task, registry, and
  selection test modules in the same directory;
- `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__task_registry_selection_contract.py`;
- `docs/api/harness-task.rst`;
- `docs/architecture/v2/ksdft2effmass/harness/object-model.md`;
- `docs/architecture/v2/ksdft2effmass/harness/development-harness.md`; and
- this migration page when actual cutover state changes.

Existing evidence identities remain stable. Tests change their supported import to
`ksdft2effmass.harness`, verify transitional imports resolve to the identical public
objects, and add class-owned descendant-query partitions. The artifact-owned
selection test must validate and round-trip the actual canonical live selection
whether active or inactive; it must not require the repository to equal the inactive
fixture. Separate fixtures continue to cover canonical inactive bytes.

## Prerequisite results

Planning inputs are present:

- the closed human-accepted `migration.v2.identity-contracts` result;
- current version-3 Task and version-1 selection source, schema, fixtures, tests, and
  API documentation;
- the canonical Task graph and represented opaque lifecycle vocabulary;
- retired chain records and current live readers; and
- accepted v2 Harness ownership and validation boundaries.

The human separately authorized source implementation after accepting the planning
result, and later accepted the completed implementation result. No downstream Task was
a prerequisite for this bounded DataObject/registry cutover.
`migration.v2.harness.validation`,
`migration.v2.harness.prerequisite-resolution`, and
`migration.v2.harness.chain-replacement` remain separately activated downstream
owners.

## Conditional human decisions

No material decision remains for this planning slice. Existing authority selects:

- canonical Task fields rather than independent chain topology;
- Option B domain-owned runtime types;
- v2 ownership under `ksdft2effmass.harness`;
- one-way transitional compatibility rather than a second implementation;
- opaque historical lifecycle text rather than an invented closed vocabulary; and
- implementation-only prerequisite gating with separately owned result resolution.

A future closed lifecycle vocabulary or compatibility-breaking removal becomes a
separate decision only when its owning Task presents concrete alternatives and a
consumer impact that existing authority does not resolve.

## Verification

The accepted implementation ran, in increasing scope:

1. focused software-verification tests for Task, registry, descendant traversal,
   selection, serializers, and cross-surface schema/fixture/public-import agreement;
2. maintained Python conformance for every changed test module with its explicit
   ownership input;
3. Ruff and mypy over changed source and tests;
4. the configured Python software-verification suite;
5. Sphinx with warnings as errors;
6. `validate_harness.py` and projection drift checking; and
7. `git diff --check` plus dependency-file immutability confirmation.

These checks establish only documented software and migration compatibility. They do
not establish authority, protected execution, numerical verification, scientific
validation, uncertainty quantification, or human acceptance.

## Cutover, retirement, and rollback

Cutover is one-directional:

1. introduce and verify the v2-owned public objects;
2. make transitional local imports resolve to those exact objects;
3. migrate maintained consumers to the v2 import surface under their owning Tasks;
4. retain version-3 Task and version-1 selection wires unchanged;
5. let `migration.v2.harness.validation` replace the local-result graph validation
   boundary;
6. let `migration.v2.harness.chain-replacement` dispose every retained `chains.py`,
   wire, ownership, fixture, test, and public-export consumer; and
7. remove compatibility modules only when no retained consumer remains and the
   accepted compatibility gates pass.

Before consumer migration, rollback removes the candidate v2 modules and restores the
last accepted local implementation. After migration begins, rollback restores the
last accepted consumer/import revision without rewriting canonical Task or selection
bytes, archived chain history, lifecycle text, or activation receipts.

## Residual limitations

- Exact normative `ValidationResult` fields and `HarnessState` composition remain with
  their own Tasks.
- Actual prerequisite-result identities and matching are deferred to
  `migration.v2.harness.prerequisite-resolution`.
- The closed lifecycle vocabulary remains deferred; existing status text is preserved
  without reinterpretation.
- The chain-replacement cutover removed `chains.py` and its public/wire consumers;
  archived chain bytes remain retained outside live discovery and decoding.
- Multiple independent repository selection scopes remain deferred; version 1
  represents one project-local scope.
- The current activation-receipt identifier is retained only as a selection reference;
  no independent repository receipt record was identified, so later authority
  resolution must fail closed unless its owning input supplies and verifies that
  reference.
- No source, test, schema, fixture, dependency, consumer migration, or successor
  activation is authorized by this planning result.
