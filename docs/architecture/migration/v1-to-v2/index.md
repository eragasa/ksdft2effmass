# Migration from Architecture v1 to Architecture v2

## Purpose and baseline

This subtree is the sole maintained cross-version comparison. It maps the
[implemented Architecture v1 snapshot](../../v1/index.md) at
`0dda56e2c11261280660139fe80dab0d395b4234` to the [prospective Architecture v2
target](../../v2/index.md).

The migration is organized first by package ownership, then by subject-specific
crosswalks and dependency-ordered cutover. Mapping describes responsibility
transfer; it is not a source-move plan, alias policy, compatibility promise, or
claim that a prospective package exists.

Current human instructions own ordinary direct work. Canonical Task records and
`harness/task-graph.json` own managed Task content and topology;
`harness/task-selection.json` owns current selection. Retired chains remain
non-operational history outside Pi discovery. No mapping
row activates work or authorizes a dependency change, protected execution,
publication, or release.

## Mapping vocabulary

| Disposition | Meaning |
|---|---|
| Retain | The v1 owner remains the prospective v2 package owner |
| Rename/move | Responsibility transfers after compatibility gates pass |
| Split | One v1 owner maps to multiple v2 owners |
| Replace | V2 introduces a different aggregate or execution boundary |
| Retire | A v1 compatibility or process surface has no permanent v2 counterpart |
| Introduce | V2 selects a responsibility with no implemented v1 package owner |
| Unresolved | V2 has not selected a complete destination; v1 remains authoritative |

## Package ownership map

| V1 as-built package or path | Prospective v2 owner | Disposition |
|---|---|---|
| `ksdft2effmass.harness.pi` and `.local` | `ksdft2effmass.harness`, with composition in `.application`, storage through `.persistence`, and outer adaptation in `.pi.agents` | Split and narrow |
| `ksdft2effmass.workflows.cpn` | `ksdft2effmass.petrinet.colored` | Rename/move |
| No v1 scientific Workflow aggregate | `ksdft2effmass.workflows` | Introduce |
| `ksdft2effmass.io.quantum_espresso.qexsd` | `ksdft2effmass.integration.quantumespresso` | Rename/move and narrow |
| Repository `calculations/` runners | `.calculators`, `.integration.quantumespresso`, `.workflows`, `.campaigns`, and `.application` | Split and replace |
| `ksdft2effmass.periodic` | `ksdft2effmass.periodic` | Retain |
| `ksdft2effmass.ksdft` | `ksdft2effmass.ksdft` | Retain and narrow |
| `ksdft2effmass.ksdft.pw` | `.ksdft`, `.calculators`, `.integration.quantumespresso`, and `.workflows` | Split; exact field destinations deferred |
| `ksdft2effmass.provenance` | `.workflows`, `.calculators`, `.integration.quantumespresso`, and the applicable domain identity owners | Split |
| `ksdft2effmass.operators` | `ksdft2effmass.operators` | Retain as the cohesive, narrowly bounded represented-operator kernel under accepted Option A; the current records contract is provisionally unchanged while exercises inform later API requirements and exact analysis disposition remains separately planned |
| No v1 domain-neutral revision store | `ksdft2effmass.persistence` | Introduce |
| No v1 campaign package | `ksdft2effmass.campaigns` | Introduce |
| Calculation-specific deterministic analysis | `ksdft2effmass.analysis` | Introduce and extract incrementally |
| Ad hoc repository composition | `ksdft2effmass.application` | Introduce |
| Pi descriptors, settings, and installed runtime | Repository role catalog and Pi runtime; governed actions through `.pi.agents` | Retain and split |

The complete module-family mapping, interaction diagrams, compatibility gates,
and unresolved operator boundary are maintained in the [package and module
crosswalk](package-module-crosswalk.md).

## Crosswalks by mapped responsibility

### Package and module ownership

- [Package and module crosswalk](package-module-crosswalk.md) — complete
  as-built module-family mapping for Harness, agents, CPN, Workflow, calculators,
  QE integration, observations, provenance, operators, analysis, persistence,
  campaigns, and application composition.

### Implementation planning

- [V2 migration implementation planning](implementation/index.md) — converts the
  crosswalk into module/submodule `HarnessTask` containment trees, recursive
  planning cascades, actual prerequisite-result dependencies, conditional human
  review, implemented-behavior documentation, and deterministic closeout.

### Development Harness

- [Development-harness projections](development-harness-projections.md) — maps
  v1 local control and database projections to the v2 compiler, synchronizer,
  comparator, repositories, and projections.
- [Coding-standards conformance](coding-standards-conformance.md) — maps the v1
  Python conformance family to the narrowed v2 conformance owner.

### Conversational agents and governed operations

- [Pi harness subagents](pi-harness-subagents.md) — maps descriptors, settings,
  role discovery, assignments, worktrees, handoffs, review, runtime evidence,
  and recovery.
- [Agent execution and deterministic actions](agents.md) — maps governed
  capabilities, the prospective Pi adapter, isolation, action composition,
  candidate promotion, and rollback.

### Scientific workflow and execution

The package/module crosswalk owns the current CPN, Workflow, calculator, QE,
observation, provenance, operator, analysis, campaign, and application mapping.
Normative prospective behavior remains on the corresponding v2 package pages.
Add a narrower scientific-execution crosswalk only when implementation requires
additional cutover detail that does not duplicate those owners.

## V2 packages without one-to-one v1 sources

| Prospective v2 package | Inputs from v1 | Introduction condition |
|---|---|---|
| `persistence` | Harness SQLite/projection experience only | Domain-neutral immutable revision and compare-and-swap contracts accepted |
| `workflows` | CPN semantics, execution observations, Task history, and provenance records | Scientific Task/Workflow/WorkflowRun and repository contracts accepted |
| `calculators` | Calculation inputs and direct runner records | SimulationTask/Simulation and executor protocols accepted |
| `integration.quantumespresso` | QEXSD I/O and QE runners | Concrete QE anti-corruption boundary accepted |
| `campaigns` | Tutorial and production definitions | Generic Workflow remains free of project-specific policy |
| `analysis` | Existing deterministic algorithms and later-authorized operator analysis | Units, tolerances, numerical policy, and evidence class explicit |
| `application` | Existing command and repository composition | Every injected component has an explicit owner |
| `pi.agents` | Role identities and accepted deterministic domain operations | Closed transport, composition, runtime identity, and isolation contracts accepted |

## Current progress after the v1 snapshot

The mapping baseline remains fixed. Later accepted changes do not rewrite the v1
snapshot:

- The foundational identity, version, immutable-result, and failure contract is
  stabilized under human-accepted Option B. Runtime types, results, failures,
  serializers, and repositories remain domain-owned; no shared contracts package,
  universal base hierarchy, schema, fixture, or dependency was introduced.
- Python conformance is publicly owned by
  `ksdft2effmass.harness.pi.conformance.python`; the former Python
  `harness.pi.evidence` facade is retired without changing repository evidence
  artifacts.
- The former public `HarnessControl*` compatibility names and duplicate command
  route are retired as recorded by the projection migration.
- Project-local role projection is settings-aware and remains a repository role
  projection rather than Pi runtime discovery.
- The former v1 `workflows.cpn` API is retired after full-name
  `petrinet.colored` contract verification and completion of the explicit Workflow
  adapter. No production source or example retained the old import, and no abbreviated
  aliases remain. Versioned v1 specifications, Architecture v1 documentation, and Git
  history remain audit records rather than live compatibility capability.
- The bounded v2 scientific Workflow model is implemented at
  `ksdft2effmass.workflows`: domain-owned `ResultObject`, structural `Task` and
  nested `Workflow` protocols, explicit named inputs and operation context,
  run-scoped Task instances, immutable start-gate composition, and discriminated
  direct/`any_of`/`all_of` activations. It performs no Task invocation, WorkflowRun
  aggregation, persistence, calculator effect, or scientific acceptance.
- The effect-free Workflow colored-Petri-net adapter is implemented under the
  human-selected explicit-mapping Option B. Immutable Workflow-owned mapping and
  result-token correlation records drive exact generic enablement and selection for
  direct, deterministic `any_of`, and compatible combined `all_of` activation. The
  adapter performs no Task invocation, generic firing, marking mutation, persistence,
  external effect, or scientific acceptance; domain-specific ResultObject value
  conversion and public wire formats remain deferred.
- The domain-neutral `persistence.store` foundation is implemented. A concrete
  SQLite realization and domain repository composition remain prospective.
- No complete scientific Workflow package, calculator, analysis, application,
  campaign, or Pi-agent-adapter package is claimed as implemented by this index.

Uncommitted working-tree changes are not added to this progress list merely
because they are present locally.

## Conditional minimal cutover

The accepted v2 target fixes ownership, dependency direction, and prohibitions; it
does not require implementation of every prospective surface. A capability remains
deferred until a selected consumer demonstrates need for it. In particular, complete
`HarnessState` compilation and validation, Harness persistence, projection redesign,
subagent redesign, planning automation, reporting, machine-derived closeout,
scientific Workflow execution, calculator execution, generalized analysis,
application composition, campaigns, and `pi.agents` are not minimal-cutover
requirements merely because prospective pages describe them.

The completed minimal Harness cutover is narrower: canonical `HarnessTask` records,
`HarnessTaskRegistry`, `DevelopmentTaskSelection`, and independently owned decisions
replace development-chain topology and selection. The former public `TaskReference`,
`ChainView`, `ChainEvaluationResult`, `ChainStateEvaluator`, and chain-dependent
ownership validator are retired; their live schemas and fixtures are removed while
archived chain files remain immutable non-operational history. This bounded cutover
does not require the deferred compiler, validation, persistence, projection,
subagent, reporting, planning-automation, or machine-derived-closeout stacks. Other
v1 routes remain until an actual selected v2 consumer supplies replacement behavior
and compatibility evidence.

## Dependency and cutover order

The ownership mapping imposes the following order. Each step requires separate
authority and does not activate its successor.

1. Preserve the v1 snapshot and identify exact current consumers.
2. Stabilize the shared semantic identity, version, failure, and immutable-result contracts while retaining domain-owned nominal runtime types.
3. Complete the minimal Harness cutover through canonical Task/selection and decision
   ownership plus retirement of live development-chain capability, without importing
   scientific state. Add compiler, validation, repository, projection, reporting, or
   orchestration capabilities only when a selected consumer demonstrates need.
4. Complete role identity, launch reconciliation, direct/managed assignment,
   runtime retention, and chain-discovery separation for subagents.
5. Implement shared `persistence.store` and `persistence.sqlite`, then compose
   domain-owned Harness repositories.
6. Implement `petrinet.colored` with accepted v1 CPN compatibility behavior.
7. Accept and implement scientific `workflows` contracts and repositories.
8. Extract calculator-facing contracts into `calculators` and concrete QE
   behavior into `integration.quantumespresso`.
9. Compose exact tutorial definitions through `campaigns` and `application` and
   demonstrate direct/Workflow-controlled software behavior without scientific
   claims.
10. Introduce deterministic `analysis` operations only with explicit numerical
    policy and applicable verification.
11. Resolve the `operators` ownership gap before any operator source move.
12. Implement `pi.agents` and a governed operator only after domain operations,
    authority, action composition, and isolation contracts exist.
13. Retire each v1 route only after replacement behavior and rollback pass the
    accepted compatibility gates.

Scientific execution requires separate exact protected-execution authority.
Historical calculation artifacts require no recalculation merely because their
software owners change.

## Target dependency direction

```text
persistence.sqlite → persistence.store
harness.persistence → persistence.store
workflows.persistence → persistence.store
workflows → petrinet.colored
campaigns → workflows
calculators → workflows, periodic, ksdft
integration.quantumespresso → calculators, workflows, periodic, ksdft
analysis → workflows, periodic, ksdft
application → persistence, harness, workflows, campaigns, calculators,
              integration.quantumespresso, analysis
pi.agents → application
```

Forbidden reverse edges include `petrinet.colored → workflows`,
`workflows → calculators/integration`, `calculators → integration`, neutral
scientific records importing calculator packages, scientific packages importing
Harness runtime state, and inward packages importing `pi.agents`.

## Exact-artifact and evidence boundary

Existing QE inputs, pseudopotentials, outputs, and convergence artifacts retain
actual identities, provenance, and limitations. Migration does not require
rendering, conversion, registration, rerun, assignment to WorkflowRun, fabricated
Task provenance, or evidence reclassification.

Shared labels, methods, cutoffs, pseudopotential families, or settings do not
establish equivalence. Passing software checks establishes only the declared
software contract. Numerical verification, scientific validation, uncertainty
quantification, protected-action authority, and human acceptance remain
separate.

## Deferred package decisions

Potential ProjectKoios extraction remains deferred. Neither ProjectKoios
repository is claimed as installed or integrated, and no extraction occurs
without dependency, licensing, compatibility, and acceptance authority. Exact
persistence wire and SQLite policy remain with their owning contracts.

The represented-operator destination is resolved under human-authorized Option A.
`ksdft2effmass.operators` remains the cohesive, narrowly bounded owner of represented
records, schema serialization, exact compatibility, fixed-representation
Hermiticity, guarded signed differencing, primitive residuals, and
fixed-representation comparison composition. Higher-level alignment selection,
model fitting, continuum reduction, structured learning, scientific findings, and
interpretation remain outside that kernel. The selected records-disposition Task
provisionally leaves the current source modules, supported package imports,
schema-version-1 wire, public fixtures, and exact compatibility audit unchanged,
without a facade or source move. This no-change baseline is not a final scientific API
freeze: controlled exercises may motivate a separately authorized, explicitly
versioned contract change. The analysis disposition remains with its separate
unselected Task; no successor is automatically activated.

## Status

Architecture v1 remains the implemented snapshot and architecture v2 remains
prospective except for explicitly reported migration foundations. This index and
its crosswalks authorize no implementation, source move, dependency change,
scientific execution, successor activation, publication, release, verification,
validation, or human acceptance.
