# Identity, version, and failure contracts

## Identity classes

Architecture v2 keeps logical, revision, content, snapshot, operation, attempt, authority, obligation, and result identities distinct. These identity classes are not interchangeable. Filenames and deployment paths are not identities unless their owning contract explicitly defines them as such.

| Identity | Meaning |
|---|---|
| `WorkflowIdentity` | Reusable Workflow definition |
| `WorkflowRunIdentity` | One represented run |
| `WorkflowRuntimeBundleIdentity` | Exact immutable definitions, evaluators, adapter, schema, and implementation versions used for replay |
| `WorkflowRunReplayResultIdentity` | One closed replay outcome for an exact run revision and runtime bundle |
| `TaskDefinitionIdentity` | Reusable Task contract |
| `TaskInstanceIdentity` | Run-scoped instance |
| `TaskStartGateSetIdentity` | One immutable `any_of` or `all_of` Workflow composition policy |
| `TaskActivationIdentity` | One `direct`, `any_of`, or `all_of` Task activation |
| `OperationIdentity` | Intended operation, distinct across retry/new execution |
| `AttemptIdentity` | One bounded attempt |
| `TaskInvocationOutcomeIdentity` | One closed generic invocation outcome for an exact activation, operation, and attempt |
| `NestedWorkflowInvocationIdentity` | One parent invocation correlation to an exact distinct child WorkflowRun |
| `ResultObjectIdentity` | One immutable workflow-facing result |
| `ColoredPetriNetDefinitionIdentity` | Exact generic definition |
| `ColoredPetriNetMarkingIdentity` | Exact semantic marking |
| `ColoredPetriNetEnablementResultIdentity` | One complete enabled-set result for an exact definition and marking |
| `ColoredPetriNetSelectionResultIdentity` | One canonical or definition-permitted-directed selection from an exact enablement result |
| `SnapshotIdentity` | One closed authority, configuration, resource, or artifact-resolution snapshot |
| `ContentIdentity` | Exact bytes or canonical represented content under a named algorithm |
| `RevisionReadRequestIdentity` | One latest-or-explicit-revision read and optional exact reconciliation expectation set |
| `RevisionReadResultIdentity` | One closed generic found/absent/mismatch/incompatible/corrupt/indeterminate/error observation |
| `ExecutionGrantIdentity` | One externally issued exact-dispatch authority grant |
| `ScientificExecutionAuthoritySnapshotIdentity` | One verified trusted-source, issuer, validity, freshness, and revocation view |
| `SimulationExecutionAuthorizationResultIdentity` | One closed authorization outcome for exact operation phase, grant state, snapshot, and dispatch inputs |
| `ObligationIdentity` | Durable dispatch obligation |

Producer provenance is a closed variant, not a nullable collection of unrelated identities. A represented Task producer uses exact applicable Workflow, WorkflowRun, producing Task instance, TaskActivation, attempt, and produced ResultObject identities. A represented scientific-decision-ingress producer instead uses the exact Workflow, WorkflowRun, decision request, decision-origin transition, recorder implementation/version, direct response-source and authority-context, and produced `ScientificDecisionResolution` identities; Task-instance, TaskActivation, attempt, and Task result-production identities are prohibited. A genuinely non-Workflow external producer may mark Workflow/run/task/activation identities unavailable but must carry authoritative external producer identity, producer attempt identity, and exact artifact and/or result identity. Retained, authored, and bounded legacy variants retain their actual source evidence.

## Version binding

Versioned records bind applicable schema, Workflow, Task, gate-policy, generic definition/expression/ordering, adapter, calculator input/output, executable configuration, normalization, analysis, and provenance-contract versions. A version identity cannot be silently replaced by “latest.” Unsupported versions return a represented failure.

## Closed results and failures

Each operation uses a closed result or failure vocabulary. A variant contains only fields valid for that outcome. In particular:

- generic `TaskInvocationOutcome` is exactly `confirmed`, `rejected`, or `indeterminate` for one TaskActivation, operation, and attempt; confirmed alone contains returned concrete ResultObjects, rejected contains a structured failure, and indeterminate contains no results and preserves exact reconciliation identities;
- a confirmed nested-Workflow outcome additionally references one exact replay-equal terminal child WorkflowRun revision and explicit exported ResultObjects; its child owns a distinct marking and ordered history, while rejected or indeterminate nested outcomes export nothing;
- confirmed `SimulationDispatchOutcome` is an envelope containing the one exact concrete returned ResultObject plus request, Task-instance, TaskActivation, attempt, executor, grant, and obligation correlation identities; it is not a second scientific result object;
- rejected dispatch contains a structured failure and no result;
- indeterminate dispatch contains no result and preserves its original activation/request/attempt/grant/obligation identities;
- generic firing success contains a successor `ColoredPetriNetMarking`, exact enablement-result, selection-result, optional-directive, consumed/read/produced-token and inscription audit facts, and no WorkflowRun record;
- WorkflowRun replay is exactly `equal`, `unequal`, `unsupported_version`, or `error`; only `equal` permits service advancement or proposed-successor submission and no replay result grants authority;
- execution authorization is exactly `authorized`, `denied`, or `error`; only `authorized` binds a usable exact grant, verified snapshot, operation phase, and phase-compatible state (`unused` before reservation or exact reserved/unclaimed obligation before claim), while the other variants cause no reservation, claim, or effect; and
- persistence conflict reports expected and observed revisions without choosing a winner;
- shared revision read is exactly `found`, `absent`, `mismatch`, `incompatible`, `corrupt`, `indeterminate`, or `error`; only `found` contains a revision satisfying every supplied expectation, while `mismatch` carries only conflicting generic identities; and
- domain aggregate load is exactly `loaded`, `absent`, `mismatch`, `incompatible`, `corrupt`, `indeterminate`, or `error`; only `loaded` contains a reconstructed, domain-validated snapshot.

Failures carry failure identity, operation phase, stable code, applicable exact operation or attempt and implementation identities, expected condition, observed condition, sanitized diagnostic, retryability only when explicitly known, related artifact identities when applicable, and a claim boundary. They do not fabricate identities for phases that never began. Retry creates a new attempt and never erases its predecessor failure.

## Correlation invariants

- Each Task instance has zero or one `TaskStartGateSet`; its mode is exactly `any_of` or `all_of`, and it has zero or more member gates.
- Each TaskActivation identifies one Task instance, exact generic selection result, already-bound ResultObjects, Workflow/WorkflowRun, operation, attempt, and exactly one selection discriminant: `direct` with no gate-set/selected-gate identity; `any_of` with exact gate-set and one selected gate/binding; or `all_of` with exact gate-set and every member gate/binding in canonical order.
- Each TaskActivation/operation/attempt has at most one effective generic `TaskInvocationOutcome`; exact duplicate submission reconciles by the same complete identities and bytes, while retry creates new activation, operation, and attempt identities.
- Each nested Workflow invocation binds an exact parent run/revision, parent Task instance, activation, operation, attempt, intended child definition, distinct child WorkflowRun identity, input ResultObjects, and child-creation idempotency identity. Child creation uncertainty is reconciled through that exact identity and never by automatic duplicate creation.
- Each represented Task-produced ResultObject identifies its applicable producer provenance. A nested export retains child producer provenance and gains a separate parent admission dependency; parent membership does not rewrite its producer.
- Each represented `ScientificDecisionResolution` identifies its closed scientific-decision-ingress producer provenance and direct trusted-boundary source and authority-context identities without fabricating Task lineage.
- Result-dependency edges identify exact consumed ResultObjects independently of parent/child Workflow membership.
- One execution grant authorizes one exact dispatch. Its verified authority snapshot binds trusted source/issuer, content and authentication checks, predecessor/revocation closure, validity/freshness, and resolver version.
- `SimulationExecutionRequest` binds the exact Task instance, TaskActivation, attempt, executor, grant, closed authorization result, obligation scope, and already-bound ResultObject inputs; it does not embed a generic Simulation aggregate.
- The request transaction atomically records `reserved` for the exact grant/obligation. Immediately before the effect, one expected-revision compare-and-swap may append `claimed`; only that claimant proceeds, and claimed authority never becomes unused again.
- Exactly one confirmed dispatch envelope correlates one returned concrete ResultObject to one request, activation, attempt, and executor. Workflow control constructs the corresponding candidate generic invocation outcome, and `TaskResultIngester` validates their correlation and atomically admits that exact object with the generic outcome and result transition; the generic outcome references rather than replaces the specialized dispatch outcome.
- Retry or new execution uses new activation, operation, and attempt identities plus new request, obligation, grant, or child-run identities where applicable. Indeterminate reconciliation retains the original generic outcome and all applicable child-creation, authorization, reservation, claim, dispatch, and obligation identities and never reinvokes automatically.
- `ColoredPetriNetFiringInput` binds exact definition/transition, predecessor marking, enablement result, generic selection result, applicable definition-permitted directive or explicit absence, selected binding, and an immutable generic external-output-value binding; stale or mismatched selection identities and missing, extra, or ambiguous output values reject firing.
- Existing TaskActivation or scientific-decision request/resolution origin records retain why a generic selection was requested and reference that same selection result; no second Workflow selection-derivation result is required.
- One scientific-decision request has exactly one decision-state token at its ingress boundary. Initial recording replaces unresolved state with one effective resolution; correction atomically consumes the exact effective predecessor and produces its identified superseding resolution. Stale or competing correction fails, and historical downstream reads are not erased or reinterpreted.
- Every WorkflowRun stores exact initial/current marking content and a canonical ordered transition history sufficient for deterministic replay equality.
- `WorkflowRunReplayer` binds one exact WorkflowRun revision and explicit `WorkflowRuntimeBundle`; it performs no ambient latest-version discovery, and only an exact `equal` result permits workflow-service advancement or candidate submission.
- Every repository successor identifies its exact predecessor and candidate unit; the domain atomic repository invokes and binds its exact validator and serializer before commit.
- An exact idempotency replay uses the same complete bound commit and returns the original committed revision; reuse with any different identity or bytes is an idempotency-collision conflict.
- Reconciliation after an indeterminate commit reads the exact stream/revision/predecessor/schema/content/idempotency closure; incompatible, corrupt, indeterminate, or error observations never imply commit or absence.
- Confirmed result ingress identifies the exact native output manifest and extraction specification; it creates no implicit copy, transfer, or artifact-publication effect.

## Artifact identity and equivalence

Exact native inputs, pseudopotentials, outputs, and retained artifacts keep content identities and producer provenance. Same labels, methods, cutoffs, asset families, or settings do not establish equivalence. Content identity, compatibility, numerical agreement, scientific validation, and human acceptance are distinct claims.

## Status

Exact lexical forms, digest algorithms, canonical encodings, and wire schemas remain deferred.
