# Scientific Workflow architecture

## Status

**Expanded nominal-ABC documentation gate complete; source implementation pending separate authorization.**

The [architecture gate](../workflows/architecture-gate.md) records the completed
documentation and planning gate for one coordinated implementation run. It does not
authorize that run. Source implementation, periodic-1D
replay, protected execution, pushing, release, and publication remain outside this
stage.

The class-owned contracts linked below supersede conflicting details in older proposal
text. The [implementation page](implementation.md) continues to describe current
software until the coordinated migration occurs.

## Responsibility

The architecture separates:

1. immutable Task and Workflow definitions;
2. declarative execution plans;
3. process-local runtime bindings;
4. route-specific behavior and protected effects; and
5. represented WorkflowRun state and durable outcomes.

Workflow definitions compose operations but execute none. Scientific Tasks own cohesive
operations. Simulation effects remain behind authority-bearing dispatch. Nested Tasks
target distinct child runs. Durable Workflow control owns production, admission, and
outcome correlation.

## Generic definition model

Every Task uses one frozen [`TaskDefinition`](../workflows/TaskDefinition/index.md),
containing stable identity and one closed
[`TaskExecutionKind`](../workflows/TaskExecutionKind/index.md). Every Workflow uses one
frozen [`WorkflowDefinition`](../workflows/WorkflowDefinition/index.md), containing
identity and immutable composition.

Concrete operations do not create per-Task or per-Workflow definition subclasses or
schemas. The ABC hierarchy supplies final generic definition construction.

## Nominal inheritance

[`AbstractTask`](../workflows/AbstractTask/index.md) is the generic engine-node ABC. It
owns stable identity, final definition construction, and subclass-time route
enforcement. It does not impose one universal execution method.

The closed hierarchy is:

```text
AbstractTask
├── AbstractScientificTask
│   ├── AbstractInProcessScientificTask
│   └── AbstractSimulationTask
└── NestedWorkflowTask
```

[`AbstractScientificTask`](../workflows/AbstractScientificTask/index.md) is a grouping
ABC without a route. The three route roots fix their execution kinds. Multiple route
roots, route overrides, definition overrides, and concrete route-less Tasks are
rejected before instantiation. Plan and binding compilation repeat exact checks as
cross-object defense in depth.

[`AbstractWorkflow`](../workflows/AbstractWorkflow/index.md) is an independent
nominal definition owner. It is not an `AbstractTask` and has no execution method.

## Route ownership

### In-process

[`AbstractInProcessScientificTask`](../workflows/AbstractInProcessScientificTask/index.md)
owns the ordinary public `execute(inputs, context)` operation and returns exact
[`TaskExecutionResults`](../workflows/TaskExecutionResults/index.md).
`TaskExecutionContext` supplies correlation, not authority.

### Simulation

[`AbstractSimulationTask`](../workflows/AbstractSimulationTask/index.md) owns immutable
simulation operation definition and input correlation but no direct effect method.
[`AbstractSimulationDispatchEffect`](../workflows/AbstractSimulationDispatchEffect/index.md)
is the nominal external-effect ABC consuming the existing authority-bearing dispatch
request. Reservation, claim, dispatch entry, reconciliation, and result ingress remain
with the established control plane.

There is no generic `AbstractDispatchEffect`: no second effect family demonstrates a
shared typed contract.

### Nested Workflow

[`NestedWorkflowTask`](../workflows/NestedWorkflowTask/index.md) owns one immutable
child definition and no scientific execute method. Declarative plans retain that child
through [`NestedWorkflowTarget`](../workflows/NestedWorkflowTarget/index.md). Nested
control creates a distinct child WorkflowRun and never reuses parent Task context for
child members.

## Execution-results boundary

`TaskExecutionResults` is one concrete frozen, non-subclassed Workflow-control
DataObject containing an ordered, nonempty tuple of uniquely identified ResultObjects.
It establishes local result-shape validity only. It does not establish authority,
production provenance, artifact lineage, ingress, persistence, scientific validity, or
a confirmed durable outcome.

All concrete operations reuse this class; scientific variation remains in contained
domain ResultObjects. Durable confirmation separately requires production records and
exact run, activation, operation, attempt, and specialized-route correlation.

## Declarative plan

[`WorkflowExecutionPlan`](../workflows/WorkflowExecutionPlan/index.md) contains only:

- one immutable `WorkflowDefinition`;
- ordered `TaskDefinition` snapshots matching composition exactly; and
- exact nested child targets.

It contains no live owner or adapter.
[`WorkflowExecutionPlanConstructor`](../workflows/WorkflowExecutionPlanConstructor/index.md)
owns complete declarative compilation.

## Runtime bindings

[`WorkflowTaskBinding`](../workflows/WorkflowTaskBinding/index.md) is a process-local
frozen association of one Task-instance identity, one explicit nominal Task, and the
simulation effect only when required by the route.

[`WorkflowExecutionBindings`](../workflows/WorkflowExecutionBindings/index.md) binds
one exact plan to the complete ordered runtime set.
[`WorkflowExecutionBindingsConstructor`](../workflows/WorkflowExecutionBindingsConstructor/index.md)
validates exact definition, route, effect, nested-target, membership, and order
agreement. Runtime references never become declarative plan content or durable
scientific state.

No constructor performs discovery, registry lookup, execution, authority decisions,
persistence, or scientific interpretation.

## Engine boundary

[`WorkflowEngine`](../workflows/WorkflowEngine/index.md) remains a stateless ActionObject
for exact ordinary in-process invocation. It consumes validated
`WorkflowExecutionBindings` plus one exact activation, derives context, invokes the
bound in-process Task, and requires `TaskExecutionResults`.

Simulation and nested kinds fail closed at this method and retain their established,
distinct control paths. The coordinated migration does not hide unlike durable
lifecycles behind one universal engine return union.

## Schema economy

Inheritance is used only for shared behavior and route enforcement. Composition is used
for data. The architecture introduces one generic Task definition, one generic Workflow
definition, one execution-results class, one declarative plan, and one runtime bindings
aggregate. Concrete operations do not add operation-specific versions of these types.

A durable wire schema is introduced only when a value actually crosses an accepted
persistence or interchange boundary. Runtime bindings and `TaskExecutionResults` are
not independently serialized by default.

## Coordinated migration

The [current-to-target class crosswalk](../workflows/migration/current-to-target-class-crosswalk.md) defines
one implementation run covering shared records, ABCs, plan/binding separation, engine
migration, nominal simulation effect migration, Quantum ESPRESSO updates, exports,
tests, and documentation. No compatibility aliases are retained.

The consolidated [Workflow defects](../workflows/defects/index.md) remain open until
that implementation and its required software evidence pass.

## Evidence boundary

Architecture agreement and software verification do not establish that a calculation
ran, that a numerical method converged, or that a scientific result was validated or
accepted.

## Detailed pages

- [Architecture gate](../workflows/architecture-gate.md)
- [Schematic](schematic.md)
- [Implementation status](implementation.md)
- [Workflow architecture migration](../workflows/migration/index.md)
- [Workflow defects](../workflows/defects/index.md)
- [`ksdft2effmass.workflows` package architecture](../workflows/index.md)
- [WorkflowRun object model](../workflows/workflow-run.md)
- [Control plane](../workflows/control-plane.md)
