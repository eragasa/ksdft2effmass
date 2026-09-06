# Workflow control-ingress effect-bridge architecture

Request identity: `migration.v2.workflows.control-ingress.effect-bridge.request.1`

Parent workflow identity: `migration.v2.workflows.control-ingress.lifecycle`

Attempt identity: `migration.v2.workflows.control-ingress.effect-bridge.attempt.1`

Termination policy: Option A is human-selected; resume bounded control-ingress implementation and stop again at any new material human-owned or protected boundary.

## Problem

**Observed fact.** The activated `migration.v2.workflows.control-ingress` Task must preserve Workflow-owned dispatch orchestration while invoking a calculator-owned executor only after executor-bound authorization and a persistence-owned compare-and-swap claim.

**Human choice.** Select the typed effect bridge connecting Workflow control to the calculator-owned executor without reversing package dependencies or weakening the one-dispatch authority boundary.

## Observed current behavior

**Observed fact.** `SimulationDispatchAdapter` owns specialized dispatch orchestration under `docs/architecture/v2/ksdft2effmass/workflows/control-plane.md`, while calculator executor protocols belong to `ksdft2effmass.calculators` and concrete implementations belong to integration packages.

**Observed fact.** The permitted dependency direction is calculators to workflows. Workflows must not import calculator or integration implementations. Application composition may connect those owners.

**Observed fact.** The current public `Task.execute` contract accepts only bound `ResultObject` inputs and `TaskExecutionContext`. It carries no execution grant, request, claim, obligation, or executor-bound authorization state.

**Observed fact.** The retained calculator `DftCalculator` protocol is private and revisable. Its accepted Task explicitly excludes stable package exports until later public-contract work.

**Observed fact.** The shared `AtomicRevisionStore` is implemented, but `WorkflowRunRepository`, Workflow serialization, transaction validation, and concrete Workflow persistence remain owned by `migration.v2.workflows.persistence`.

**Observed fact.** The current `DispatchOutcomeRecord` requires a confirmed result reference before `TaskResultIngester`, while accepted architecture requires ingress to admit the concrete result and durable dispatch record together. `TaskInvocationOutcome` also lacks an exact dispatch-outcome reference for rejected and indeterminate simulation variants. These are aggregate-contract corrections required independently of the selected effect bridge.

**Inference.** Accepted ownership and semantic requirements determine the orchestration but do not determine a callable type that can cross the package boundary. Three materially distinct architectures remain defensible.

The immutable inputs inspected for this decision were:

- `harness/tasks/migration.v2.workflows.control-ingress.json`, activated-input SHA-256 `9325fdde2c0c77badac722e0a9c442784f4e5bcb4cac194a93c394cab847fe3c`;
- `harness/task-selection.json`, activated-input SHA-256 `ae1e7780b2ca6c8d95862d1f0690f4d111ade57cc41ffefeb1fea7b682f8b5f1`;
- `docs/architecture/v2/ksdft2effmass/workflows/control-plane.md`, SHA-256 `9b02f6becfc6bd7fb93442dd0dae76cec7f45df2b07f845e00f2acc7f96acc67`;
- `docs/architecture/v2/ksdft2effmass/workflows/service-model.md`, SHA-256 `d2619353d58b987c6d2e8a8b51335cbc728ca2f6d53e45a404d27e423ed1ffe5`;
- `docs/architecture/v2/ksdft2effmass/workflows/workflow-run.md`, SHA-256 `76c14d7cc0800b97783fcb30f1da2c870e14c6e51f4696155dee45392cdd49c9`;
- `python/src/ksdft2effmass/workflows/model.py`, SHA-256 `b0b401197dc7225d9ec08f0a6267b65379dd36ac0711645c183fbdf11a27d61c`; and
- `python/src/ksdft2effmass/workflows/runs/records.py`, SHA-256 `4f235846e21b7a17d8e3264075ae0379120b83b66b1d690736190724785f54b9`.

## Decision requirements

**Observed fact.** Every option must preserve Workflow-owned authorization, claim correlation, dispatch reconciliation, result ingress, and append-only history; calculator-owned execution; persistence-owned atomic compare-and-swap; application-owned composition; and the prohibited workflows-to-calculators dependency direction.

**Observed fact.** A denied, erroneous, stale, losing, or mismatched claimant performs no external effect. An indeterminate result contains no invented output and cannot authorize automatic redispatch.

**Observed fact.** Control ingress may construct exact candidate WorkflowRun successors but may not implement Workflow serialization, transaction validation, SQLite behavior, or scientific execution in this decision.

**Human choice.** Select which owner exposes the callable bridge and where the actual calculator invocation occurs after the claim is durably established.

All options require correction of the current pre-ingress result-reference ordering: introduce a distinct runtime `SimulationDispatchOutcome` envelope, create the durable confirmed dispatch record and `ResultObjectReference` together at ingress, and correlate every simulation `TaskInvocationOutcome` to its specialized dispatch record. The exact aggregate location for closed authorization results and native-output manifest references remains a separate deferred public-contract question; this decision does not select it.

## Option A

**Conceptual model**
Workflows defines one narrow generic typed `SimulationDispatchEffect[ResultT]` consumer port. Application composition adapts a calculator-owned executor to that port. The port accepts only the exact claimed dispatch context and returns one closed runtime dispatch observation; it stores no mutable state.

**Authority**
Workflow control owns the pre-effect authorization and verifies that the supplied claim state is exact. The port grants no authority and may be called only after the claim is represented as committed. Calculator authority remains external and separately checked at its boundary.

**Ownership/dependency**
Workflows owns the consumer-side effect-port contract and `SimulationDispatchAdapter`; calculators own executor contracts; application owns the adapter composition. Workflows imports neither calculators nor integration.

**Runtime/dispatch**
`SimulationDispatchAdapter` receives committed preparation and claim state, invokes the explicitly injected port once, and converts the returned observation into confirmed, rejected, or indeterminate `SimulationDispatchOutcome`. Reconciliation and ingress construct candidate successors; persistence later commits them.

**Migration**
The existing private calculator probe remains unchanged. A later calculator implementation supplies an application adapter conforming structurally to the Workflow port. No public calculator API is prematurely stabilized.

**Reversibility**
The narrow port can later be satisfied directly by a stable calculator executor or retired behind application composition without rewriting WorkflowRun history.

**Failures**
Port rejection and indeterminacy remain represented outcomes. Unexpected programming errors remain exceptions. A call without exact committed claim correlation is rejected before the port is invoked.

**Complexity**
Moderate. It adds one public generic port and exact dispatch request/outcome records but avoids sibling-task activation.

**Maintenance**
Workflow controls the minimum fields it must validate. Application adapters must remain synchronized with calculator-owned executors.

**Context-window consequences**
A control review needs the Workflow port, adapter, exact request/outcome records, and one application adapter contract, but not calculator implementation internals.

**Future compatibility**
New calculators can supply adapters without changing Workflow orchestration or creating a registry.

**Advantage**
It preserves the accepted orchestration and dependency direction while enabling a bounded, fully typed implementation now.

**Risk**
It introduces one generic indirection point and requires strict validation so the port cannot become an authority-bypassing executor abstraction.

## Option B

**Conceptual model**
Extend the public Task boundary with a discriminated simulation execution-context variant carrying the exact request, authorization, claim, obligation, executor identity, destination, resources, and result correlation. A simulation Task owns and calls its injected calculator executor.

**Authority**
Workflow control establishes and supplies the claimed context. The Task must reject any incomplete or mismatched simulation context and independently apply its calculator boundary checks.

**Ownership/dependency**
Workflows continues to own `Task` and the new context variant. Calculator Tasks depend on that Workflow contract and own their executors. No reverse import is introduced.

**Runtime/dispatch**
`SimulationDispatchAdapter` validates dispatch state and invokes the selected `SimulationTask` through the common Task protocol. The Task delegates to its calculator executor and returns the concrete result or structured observation.

**Migration**
The accepted `Task.execute` signature and every implementation, test double, nested Workflow, and caller must migrate to the discriminated context contract.

**Reversibility**
Reversal is expensive after generic Task implementations and callers depend on the enlarged execution context.

**Failures**
Wrong context variants fail before invocation. Simulation failures remain closed dispatch outcomes; ordinary Task failures remain generic invocation failures.

**Complexity**
High public-contract and migration complexity, with fewer explicit composition objects at runtime.

**Maintenance**
Every Task implementation shares responsibility for a context union whose simulation fields are irrelevant to ordinary and nested Tasks.

**Context-window consequences**
Reviews of the generic Task boundary must include simulation authority, claim, and dispatch semantics even for effect-free Tasks.

**Future compatibility**
Other effectful Task families may pressure the context union to grow with further domain-specific variants.

**Advantage**
It avoids a separate dispatch-effect port and keeps executor ownership inside concrete simulation Tasks.

**Risk**
It couples the generic Task contract to specialized effect-control state and destabilizes an accepted public API.

## Option C

**Conceptual model**
`SimulationDispatchAdapter` ends after authorization and claim validation by returning one immutable one-use claimed-dispatch ticket. Application composition consumes the ticket, invokes the calculator-owned executor directly, and supplies the resulting observation back for Workflow reconciliation.

**Authority**
Workflow control establishes the exact ticket only from committed claim state. The ticket records authority but grants none beyond its already-established one-use scope. Application remains responsible for invoking the selected executor once.

**Ownership/dependency**
Workflows owns the ticket and reconciliation contracts; calculators own executors; application owns the actual invocation sequence. No cross-package reverse import exists.

**Runtime/dispatch**
Control produces the ticket, application invokes the executor, and control reconciles the explicit returned observation. The Workflow adapter does not call the external-effect implementation itself.

**Migration**
Architecture and documentation must change the semantic owner of the final dispatch call from `SimulationDispatchAdapter` to application composition. Existing WorkflowRun records still require the common deterministic corrections.

**Reversibility**
The application step can later be wrapped by a Workflow-owned port, but deployed applications must migrate their orchestration.

**Failures**
A ticket may be consumed, rejected, or observed indeterminately by application code. Exact idempotency and single-consumption evidence must cross the application boundary without becoming application authority.

**Complexity**
Moderate implementation complexity but high distributed-control and integration complexity.

**Maintenance**
Every application composition must implement the same ordering and no-redispatch rules, increasing duplication risk.

**Context-window consequences**
Review requires Workflow control, application orchestration, and calculator executor surfaces together.

**Future compatibility**
Applications can integrate heterogeneous executors directly, but consistent dispatch semantics become harder to evolve.

**Advantage**
It keeps executor protocol ownership direct and avoids changing the generic Task contract.

**Risk**
It moves part of dispatch orchestration out of its accepted Workflow owner and can fragment one-dispatch enforcement across applications.

## Three-option comparison

| Criterion | Option A: Workflow effect port | Option B: Task context variant | Option C: application ticket |
|---|---|---|---|
| Preserve Workflow dispatch ownership | Strong | Strong | Weak |
| Preserve generic Task contract | Yes | No | Yes |
| Preserve dependency direction | Yes | Yes | Yes |
| Bounded implementation now | Yes | Yes, with broad migration | Yes, with architecture revision |
| Public-contract change | One narrow port | Core Task signature | Claimed-ticket orchestration |
| Application duplication risk | Low | Low | High |
| Reversibility | High | Low | Moderate |
| Expected technical debt | Lowest with strict port scope | High | Moderate to high |

## Recommendation

Recommend **Option A: application-supplied Workflow effect port**. It preserves Workflow-owned orchestration, calculator ownership, application composition, and dependency direction with the smallest public-contract change. The port must remain narrowly scoped to one exact already-claimed dispatch and must not issue authority, discover executors, persist state, retry, or reinterpret results.

The human selected Option A with the verbatim confirming response `confirmed`. Software-architecture terminology remains appropriate for this architecture-facing contract. Each application may wrap the effect port with its own application-specific public API rather than exposing dispatch-control terminology as its physicist-facing interface.

## Deferred questions

**Deferred question.** Exact WorkflowRun serialization, repository protocols, transaction validation, commit-result mapping, SQLite behavior, and recovery remain with `migration.v2.workflows.persistence`.

**Deferred question.** Stable public calculator executor types remain with later calculator public-contract work; this decision does not publish the retained private probe protocol.

**Deferred question.** Cancellation, operator interruption, nested-run compensation, and the distinct trigger for `ObligationDispositionKind.COMPLETED` remain outside this initial slice.

**Deferred question.** Exact wire formats for control requests, outcomes, authorization state, and native-output references remain deferred unless a demonstrated persistence or interoperability consumer requires them.

## Human decision required

The human confirmed the preceding unambiguous interpretation, resolving this decision as **Option A: application-supplied Workflow effect port**. Bounded implementation may resume under the recorded authorized scope. Options B and C remain excluded, and the Task must stop again if implementation exposes another material human-owned choice or protected boundary.
