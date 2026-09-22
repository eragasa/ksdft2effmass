# Workflow control-ingress dispatch re-entry safety

Request identity: `migration.v2.workflows.control-ingress.dispatch-reentry-safety.request.1`

Parent workflow identity: `migration.v2.workflows.control-ingress.lifecycle`

Attempt identity: `migration.v2.workflows.control-ingress.dispatch-reentry-safety.attempt.1`

Status: **resolved — Option A selected**.

The preserved human response is `1A and 2A`; `1A` selects the persistence-owned dispatch-entry compare-and-swap and typed receipt described below. The decision authorizes the bounded control contract and deterministic candidate construction, not persistence implementation or protected execution.

## Problem

**Observed fact.** The selected architecture requires a persistence-owned committed-claim receipt before `SimulationDispatchEffect` invocation and prohibits automatic retry.

**Observed fact.** The immutable receipt proves that one claim revision was committed, but it is copyable. Repeating `SimulationDispatchAdapter.execute()` with the same valid request enters the effect again because neither the stateless adapter nor the stateless effect port owns durable consumption state.

**Human choice.** Select the authority boundary that prevents re-entry of the same committed dispatch after its first effect entry.

## Observed current behavior

**Observed fact.** `SimulationDispatchClaimPreparer` constructs an effect-free claimed candidate and the persistence owner is expected to commit it.

**Observed fact.** `WorkflowRunClaimCommitReceipt` names the exact committed claim revision, predecessor, claim record, authorization result, content identity, persistence operation, idempotency identity, and implementation.

**Observed fact.** `SimulationDispatchAdapter` validates the receipt and immediate claim authorization, then invokes the injected effect once per method call. It owns no mutable or durable state.

**Inference.** Claim-winner uniqueness and effect-entry uniqueness are distinct. A committed claim selects one claimant, but a replayed invocation by that same claimant requires an additional contract if effect entry itself must be at most once.

The immutable inputs inspected for this decision were:

- `harness/tasks/migration.v2.workflows.control-ingress.json`, SHA-256 `516eb84b55526d3823fd93480dccc6cdcd6275679b118789d1cc634d451f0eea`;
- `docs/architecture/migration/v1-to-v2/implementation/control-ingress-effect-bridge.md`, SHA-256 `9be50f73910fc64f0031d82e2124472396642ea31d0d99fa161acae5cc07635a`;
- `docs/architecture/migration/v1-to-v2/implementation/control-ingress-authorization-claim-evidence.md`, SHA-256 `77d3657d243e78b7ced9e6c5b923327f406a8a9c148d0e68754f7757f8d22deb`;
- `docs/architecture/v2/ksdft2effmass/workflows/control-plane.md`, SHA-256 `9b02f6becfc6bd7fb93442dd0dae76cec7f45df2b07f845e00f2acc7f96acc67`; and
- `python/src/ksdft2effmass/workflows/control/dispatch.py`, SHA-256 `b4ecb38279237b258c6bf6ad4322f0b0b1513e647d0756cfff231d336c639fb3`.

## Decision requirements

Every option must preserve exact request, claim, grant, obligation, executor, revision, and outcome correlation; perform no automatic retry; preserve the Workflow-owned effect port; and grant no protected execution authority. The control-ingress Task may define and consume a typed boundary but may not implement repository serialization, compare-and-swap storage, SQLite behavior, or recovery.

## Option A

**Conceptual model.** Add a persistence-owned dispatch-entry compare-and-swap after the committed claim and before the effect. A typed dispatch-entry receipt names the exact claim receipt, obligation, outcome identity, and committed entry revision.

**Authority and ownership.** Persistence owns durable one-use consumption. Control validates the supplied receipt; the adapter and effect remain stateless.

**Runtime.** Only the winner of `claimed -> dispatch_entered` may invoke the effect. Duplicate, stale, losing, or missing entry receipts fail before effect entry.

**Migration and complexity.** This adds one public receipt and one lifecycle state whose production is implemented later by Workflow persistence. Until that implementation exists, production dispatch remains unavailable.

**Reversibility and future compatibility.** The extra state can later support recovery without changing grant or effect semantics. Removing it would weaken the durable guarantee.

**Advantage.** Provides process-independent at-most-once effect entry while preserving stateless control and effect objects.

**Risk.** Expands the deferred persistence contract and introduces another commit before an external operation.

## Option B

**Conceptual model.** Make one `SimulationDispatchAdapter` instance a stateful one-shot consumer that remembers the exact claim receipt or outcome identity after first entry.

**Authority and ownership.** Workflow control owns process-local consumption; persistence still proves only the claim.

**Runtime.** A duplicate call on the same adapter instance fails before the effect. A new process or newly constructed adapter cannot detect prior entry.

**Migration and complexity.** This adds mutable process state and lifecycle rules to the adapter without changing persistence.

**Reversibility and future compatibility.** It is easy to replace later, but historical process crashes remain ambiguous and service reconstruction can repeat the effect.

**Advantage.** Smallest immediate implementation and blocks ordinary same-instance duplicate calls.

**Risk.** Does not provide durable at-most-once behavior and conflicts with the project's operational-immutability preference.

## Option C

**Conceptual model.** Require the application-supplied effect implementation to be idempotent for the exact outcome or dispatch identity. Repeated port calls return the same observation without repeating the underlying calculation.

**Authority and ownership.** Application integration or the external executor owns deduplication; Workflow control validates identity closure but may enter the port more than once.

**Runtime.** Duplicate adapter calls are permitted at the boundary, but the effect implementation must suppress duplicate external operations.

**Migration and complexity.** The port contract gains a mandatory idempotency guarantee and every integration must supply durable or executor-native deduplication.

**Reversibility and future compatibility.** Executor-native idempotency can remain useful with later persistence, but backends lacking it need an additional store.

**Advantage.** Avoids another Workflow repository state when the executor already supports exact idempotency keys.

**Risk.** Moves a Workflow safety property into heterogeneous integrations and does not prevent repeated effect-port entry.

## Three-option comparison

| Criterion | Option A: dispatch-entry receipt | Option B: one-shot adapter | Option C: idempotent effect |
|---|---|---|---|
| Durable across process restart | Yes | No | Backend-dependent |
| Stateless adapter and port | Yes | No | Adapter yes; implementation may store state |
| Prevents repeated port entry | Yes | Same instance only | No |
| Persistence-contract expansion | Moderate | None | Optional/backend-specific |
| Cross-backend consistency | Strong | Weak | Weak |

## Recommendation

Recommend **Option A: persistence-owned dispatch-entry receipt**. It is the only option that makes effect-entry consumption durable while preserving the selected stateless Workflow control and application effect boundaries. This recommendation defines no persistence implementation and authorizes no external calculation.

## Resolution

The human selected **Option A**. A persistence owner must commit the exact `claimed -> dispatch_entered` transition and issue a typed receipt before `SimulationDispatchEffect` invocation. Workflow control validates that supplied receipt and remains stateless; it does not implement repository serialization, compare-and-swap storage, SQLite behavior, recovery, or protected execution.
