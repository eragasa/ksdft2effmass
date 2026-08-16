# `ksdft2effmass.workflows` package

## Responsibility

`ksdft2effmass.workflows` owns calculator-independent `ResultObject`, `Task`, `Workflow`, immutable `TaskStartGateSet`, discriminated `TaskActivation`, closed `TaskInvocationOutcome`, correlated `NestedWorkflowInvocation`, Workflow-owned start-gate and invocation policy, `ColoredPetriNetWorkflowAdapter`, `WorkflowRun`, `ScientificDecisionRequest`, `ScientificDecisionResolution`, `ScientificDecisionRecorder`, exact execution authority/dispatch/reconciliation contracts, artifact lineage, normalization aggregation, and analysis readiness.

Concrete scientific domains own concrete ResultObjects and their intrinsic invariants. Calculator packages own concrete SimulationTasks, Simulation composites, inputs, executors, and outputs. Analysis packages own algorithms and numerical policy. Project-specific campaign definitions may be supplied as composition inputs; they are not the generic Workflow aggregate.

## Task and Workflow boundary

A Task consumes already-bound ResultObjects and explicit context and returns ResultObjects when its operation completes. It neither discovers prerequisites, schedules itself, nor constructs its durable invocation outcome. Workflow control owns the generic `TaskInvocationOutcome`, closed as confirmed with concrete results, rejected with failure and no results, or indeterminate with no results and exact reconciliation identities. Workflow implements Task and can be nested. Run-scoped Task instances are distinct from definitions. A Task instance has zero or one `TaskStartGateSet` in `any_of` or `all_of` mode with zero or more member gates. Empty/no gates provide no automatic activation; an enclosing caller uses `direct` activation without gate-set/selected-gate identity. `any_of` records one deterministic priority/identity-selected gate/binding; `all_of` records the canonical compatible tuple across every member. Start gates define Workflow composition policy and remain separate from the Task input contract.

`TaskActivation` identifies the Task instance, already-bound results, Workflow/WorkflowRun correlation, operation, attempt, and exactly one `direct`, `any_of`, or `all_of` selection. Each nested Workflow invocation creates a distinct child `WorkflowRun` with its own marking, transitions, failures, and replay. The parent records an exact `NestedWorkflowInvocation`; only a confirmed replay-equal terminal child revision may export explicit results for parent admission. Child and parent commits are separate and reconcile through exact identities rather than cross-run atomicity or automatic duplicate creation. ResultObject dependency is independent of parent/child Workflow membership.

## Generic colored-Petri-net dependency

Workflows imports `ksdft2effmass.petrinet.colored` and uses its full public `ColoredPetriNet*` names. For task-origin work, `ColoredPetriNetWorkflowAdapter` maps gates and values to generic inputs, applies gate-set selection, constructs TaskActivation, remains effect-free while workflow control/dispatch invokes Tasks through accepted authority, maps supplied returned ResultObjects into the immutable generic external-output-value binding of `ColoredPetriNetFiringInput`, and requests pure firing. For scientific-decision ingress, the same effect-free adapter only maps the supplied `ScientificDecisionResolution` and unresolved-or-effective predecessor token for the exact request-identified transition and binding; it creates no TaskActivation and does not prompt, authenticate, interpret, record, or authorize the decision. The generic package does not import workflows or create workflow records.

## Execution and result boundary

Workflow control obtains one exact `authorized` `SimulationExecutionAuthorizationResult` for the unused grant, verified authority snapshot, and immutable Task-instance/TaskActivation/request/attempt/executor/context/input/configuration identities before constructing the complete request, attempt, successor, grant-reservation, and dispatch-obligation unit. `WorkflowRunAtomicRepository` binds the exact workflow validator and serializer to each supplied unit, then delegates one complete opaque revision to its composed `AtomicRevisionStore`. The shared store atomically commits only that single-stream revision. The target-first executor boundary independently obtains an exact `authorized` result for the same reserved grant and inputs, then wins one expected-revision compare-and-swap claim from `reserved` to `claimed` before an external effect.

`SimulationExecutionRequest` binds the exact Task instance, TaskActivation, attempt, executor, already-bound ResultObject inputs, grant, and obligation scope; it does not embed a generic Simulation aggregate. Dispatch outcomes are envelopes closed as confirmed, rejected, or indeterminate. Indeterminate contains no invented result and is not automatically retried. Confirmed contains the concrete returned ResultObject and exact correlations, not a second scientific result object. After reconciliation, workflow control constructs the candidate generic invocation outcome from the exact specialized outcome. For confirmed work, `TaskResultIngester` validates the envelope/outcome correlation and admits the concrete object, exact native-output manifest references, generic outcome, and result transition in one atomic successor unit. The workflow does not copy or publish calculator-produced files; explicitly specified extraction reads them afterward.

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

Exact field and wire contracts, nested terminal/export forms, SQLite schema and operational policy, asynchronous interfaces, cancellation, external scheduler adapters, and project-specific catalog distribution remain deferred. Standard-library SQLite is selected as the initial shared-store realization, with a separate WorkflowRun store/database by default. Generic firing retains one identity-closed enablement, selection-result, optional-directive, and firing-input chain. Workflow-owned `WorkflowRunReplayer` consumes one exact run revision and explicit immutable `WorkflowRuntimeBundle`, returns closed `equal`/`unequal`/`unsupported_version`/`error`, and gates service use of loaded or proposed successor state without moving transition computation into persistence or introducing durable replay attestations.

Human decisions are explicit external inputs processed deterministically under the [domain-separated decision contract](../../human-decisions.md). An unresolved `ScientificDecisionRequest` pauses only its affected branch. Through an application-owned trusted boundary, `ScientificDecisionRecorder` receives the verbatim response with direct source and authority-context identities, constructs the resolution with closed no-Task ingress provenance, uses the adapter and pure firer for the exact request-identified transition, constructs the complete successor, and returns the resolution only after atomic commit. Correction consumes the exact effective predecessor token and produces one superseding token; it does not roll back earlier work. The generic colored-Petri-net package remains unaware of decisions and authority. Replay consumes the committed ordered records and never prompts or reauthenticates.

This prospective contract is documentation-only. Decision records grant no authority. It grants no protected execution and claims no implementation, software or numerical verification, scientific validation, equivalence, or human software acceptance.
