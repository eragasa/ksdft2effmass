# `ksdft2effmass.workflows` package

## Responsibility

`ksdft2effmass.workflows` owns calculator-independent `ResultObject`, `Task`, `Workflow`, immutable `TaskStartGateSet`, discriminated `TaskActivation`, Workflow-owned start-gate policy, `ColoredPetriNetWorkflowAdapter`, `WorkflowRun`, `ScientificDecisionRequest`, `ScientificDecisionResolution`, `ScientificDecisionRecorder`, exact execution authority/dispatch/reconciliation contracts, artifact lineage, normalization aggregation, analysis readiness, and separately authorized disposition recording.

Concrete scientific domains own concrete ResultObjects and their intrinsic invariants. Calculator packages own concrete SimulationTasks, Simulation composites, inputs, executors, and outputs. Analysis packages own algorithms and numerical policy. Project-specific campaign definitions may be supplied as composition inputs; they are not the generic Workflow aggregate.

## Task and Workflow boundary

A Task consumes already-bound ResultObjects and explicit context and returns ResultObjects. It neither discovers prerequisites nor schedules itself. Workflow implements Task and can be nested. Run-scoped Task instances are distinct from definitions. A Task instance has zero or one `TaskStartGateSet` in `any_of` or `all_of` mode with zero or more member gates. Empty/no gates provide no automatic activation; an enclosing caller uses `direct` activation without gate-set/selected-gate identity. `any_of` records one deterministic priority/identity-selected gate/binding; `all_of` records the canonical compatible tuple across every member. Start gates define Workflow composition policy and remain separate from the Task input contract.

`TaskActivation` identifies the Task instance, already-bound results, Workflow/WorkflowRun correlation, operation, attempt, and exactly one `direct`, `any_of`, or `all_of` selection. ResultObject dependency is independent of parent/child Workflow membership.

## Generic colored-Petri-net dependency

Workflows imports `ksdft2effmass.petrinet.colored` and uses its full public `ColoredPetriNet*` names. For task-origin work, `ColoredPetriNetWorkflowAdapter` maps gates and values to generic inputs, applies gate-set selection, constructs TaskActivation, remains effect-free while workflow control/dispatch invokes Tasks through accepted authority, maps supplied returned ResultObjects into the immutable generic external-output-value binding of `ColoredPetriNetFiringInput`, and requests pure firing. For scientific-decision ingress, the same effect-free adapter only maps the supplied `ScientificDecisionResolution` for the exact request-identified transition and binding; it creates no TaskActivation and does not prompt, interpret, record, or authorize the decision. The generic package does not import workflows or create workflow records.

## Execution and result boundary

Workflow control checks one exact unused grant and immutable Task-instance/TaskActivation/request/attempt/executor/context/input/configuration identities before constructing the complete request, attempt, successor, grant-reservation, and dispatch-obligation unit. `WorkflowRunAtomicRepository` binds the exact workflow validator and serializer to each supplied unit, then delegates one complete opaque revision to its composed `AtomicRevisionStore`. The shared store atomically commits only that single-stream revision. The target-first executor boundary independently checks the same reserved grant and inputs immediately before an external effect.

`SimulationExecutionRequest` binds the exact Task instance, TaskActivation, attempt, executor, already-bound ResultObject inputs, grant, and obligation scope; it does not embed a generic Simulation aggregate. Dispatch outcomes are envelopes closed as confirmed, rejected, or indeterminate. Indeterminate contains no invented result and is not automatically retried. Confirmed contains the concrete returned ResultObject and exact correlations, not a second scientific result object. `TaskResultIngester` validates the envelope and admits that object into one atomic successor unit with the obligation disposition and all required publication obligations or explicit no-publication disposition. Publication consumes committed obligations only.

## Detailed pages

- [Human decisions](../../human-decisions.md)
- [Scientific service model](service-model.md)
- [Simulation Task model](simulation-task-model.md)
- [Task, Workflow, and colored-Petri-net adapter](task-and-colored-petri-net-adapter.md)
- [WorkflowRun object model](workflow-run.md)
- [Workflow control plane](control-plane.md)
- [Workflow persistence](persistence.md)
- [Shared revision persistence](../persistence/index.md)
- [Artifact and provenance model](artifact-and-provenance-model.md)
- [Scientific read models](read-models.md)
- [Generic colored Petri net](../petrinet/colored/index.md)
- [Separation from the development harness](../../separation-of-harness-and-workflow.md)

## Status and unresolved issues

Exact field and wire contracts, SQLite schema and operational policy, asynchronous interfaces, cancellation, external scheduler adapters, and project-specific catalog distribution remain deferred. Standard-library SQLite is selected as the initial shared-store realization, with a separate WorkflowRun store/database by default. Two reviewed design gaps also remain explicit: generic firing does not yet retain all enablement/selection/directive identities, and ownership of replay computation has not been separated coherently from repository persistence.

Human decisions are explicit external inputs processed deterministically under the [domain-separated decision contract](../../human-decisions.md). An unresolved `ScientificDecisionRequest` pauses only its affected branch. `ScientificDecisionRecorder` alone constructs the resolution, uses the adapter and pure firer for the exact request-identified no-Task ingress transition, constructs the complete scientific-decision-origin transition/successor, and returns the recorded resolution only after atomic commit. The generic colored-Petri-net package remains unaware of decisions and authority. Replay consumes the committed ordered record and never prompts again.

This prospective contract is documentation-only. Decision records grant no authority. It grants no protected execution and claims no implementation, software or numerical verification, scientific validation, equivalence, or human software acceptance.
