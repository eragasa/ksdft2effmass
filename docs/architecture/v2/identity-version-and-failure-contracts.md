# Identity, version, and failure contracts

## Identity classes

Architecture v2 keeps logical, revision, content, snapshot, operation, attempt, authority, obligation, and result identities distinct. These identity classes are not interchangeable. Filenames and deployment paths are not identities unless their owning contract explicitly defines them as such.

| Identity | Meaning |
|---|---|
| `WorkflowIdentity` | Reusable Workflow definition |
| `WorkflowRunIdentity` | One represented run |
| `TaskDefinitionIdentity` | Reusable Task contract |
| `TaskInstanceIdentity` | Run-scoped instance |
| `TaskStartGateSetIdentity` | One immutable `any_of` or `all_of` Workflow composition policy |
| `TaskActivationIdentity` | One `direct`, `any_of`, or `all_of` Task activation |
| `OperationIdentity` | Intended operation, distinct across retry/new execution |
| `AttemptIdentity` | One bounded attempt |
| `ResultObjectIdentity` | One immutable workflow-facing result |
| `ColoredPetriNetDefinitionIdentity` | Exact generic definition |
| `ColoredPetriNetMarkingIdentity` | Exact semantic marking |
| `SnapshotIdentity` | One closed authority, configuration, resource, or artifact-resolution snapshot |
| `ContentIdentity` | Exact bytes or canonical represented content under a named algorithm |
| `ExecutionGrantIdentity` | One exact-dispatch authority grant |
| `ObligationIdentity` | Durable dispatch or publication obligation |

Producer provenance is a closed variant, not a nullable collection of unrelated identities. A represented Task producer uses exact applicable Workflow, WorkflowRun, producing Task instance, TaskActivation, attempt, and produced ResultObject identities. A genuinely non-Workflow external producer may mark Workflow/run/task/activation identities unavailable but must carry authoritative external producer identity, producer attempt identity, and exact artifact and/or result identity. Retained, authored, and bounded legacy variants retain their actual source evidence.

## Version binding

Versioned records bind applicable schema, Workflow, Task, gate-policy, generic definition/expression/ordering, adapter, calculator input/output, executable configuration, normalization, analysis, and provenance-contract versions. A version identity cannot be silently replaced by “latest.” Unsupported versions return a represented failure.

## Closed results and failures

Each operation uses a closed result or failure vocabulary. A variant contains only fields valid for that outcome. In particular:

- confirmed `SimulationDispatchOutcome` is an envelope containing the one exact concrete returned ResultObject plus request, Task-instance, TaskActivation, attempt, executor, grant, and obligation correlation identities; it is not a second scientific result object;
- rejected dispatch contains a structured failure and no result;
- indeterminate dispatch contains no result and preserves its original activation/request/attempt/grant/obligation identities;
- generic firing success contains a successor `ColoredPetriNetMarking`, consumed/read/produced-token and inscription audit facts, and no WorkflowRun record;
- authority failure causes no effect; and
- persistence conflict reports expected and observed revisions without choosing a winner.

Failures carry failure identity, operation phase, stable code, applicable exact operation or attempt and implementation identities, expected condition, observed condition, sanitized diagnostic, retryability only when explicitly known, related artifact identities when applicable, and a claim boundary. They do not fabricate identities for phases that never began. Retry creates a new attempt and never erases its predecessor failure.

## Correlation invariants

- Each Task instance has zero or one `TaskStartGateSet`; its mode is exactly `any_of` or `all_of`, and it has zero or more member gates.
- Each TaskActivation identifies one Task instance, already-bound ResultObjects, Workflow/WorkflowRun, operation, attempt, and exactly one selection discriminant: `direct` with no gate-set/selected-gate identity; `any_of` with exact gate-set and one selected gate/binding; or `all_of` with exact gate-set and every member gate/binding in canonical order.
- Each represented Task-produced ResultObject identifies its applicable producer provenance.
- Result-dependency edges identify exact consumed ResultObjects independently of parent/child Workflow membership.
- One execution grant authorizes one exact dispatch.
- `SimulationExecutionRequest` binds the exact Task instance, TaskActivation, attempt, executor, grant/obligation scope, and already-bound ResultObject inputs; it does not embed a generic Simulation aggregate.
- Exactly one confirmed dispatch envelope correlates one returned concrete ResultObject to one request, activation, attempt, and executor.
- Retry or new execution uses new activation, operation, attempt, request, and grant identities.
- `ColoredPetriNetFiringInput` binds exact definition/transition, predecessor marking, selected binding, and an immutable generic external-output-value binding; missing, extra, or ambiguous output values reject firing.
- Every WorkflowRun stores exact initial/current marking content and a canonical ordered transition history sufficient for deterministic replay equality.
- Every repository successor identifies its exact predecessor and supplied validated unit.
- Every required publication has a committed obligation or an explicit no-publication disposition in the result-ingress unit.

## Artifact identity and equivalence

Exact native inputs, pseudopotentials, outputs, and retained artifacts keep content identities and producer provenance. Same labels, methods, cutoffs, asset families, or settings do not establish equivalence. Content identity, compatibility, numerical agreement, scientific validation, and human acceptance are distinct claims.

## Status

Exact lexical forms, digest algorithms, canonical encodings, and wire schemas remain deferred. This prospective documentation claims no implementation, verification, equivalence, protected execution, or human software acceptance.
