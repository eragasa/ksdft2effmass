# Workflow control-ingress indeterminate reconciliation lifecycle

Request identity: `migration.v2.workflows.control-ingress.indeterminate-reconciliation-lifecycle.request.1`

Parent workflow identity: `migration.v2.workflows.control-ingress.lifecycle`

Attempt identity: `migration.v2.workflows.control-ingress.indeterminate-reconciliation-lifecycle.attempt.1`

Status: **resolved — Option A selected**.

The preserved human response is `1A and 2A`; `2A` selects distinct append-only dispatch-observation records and one later final outcome. The decision authorizes the bounded control contract and deterministic candidate construction, not persistence implementation, recovery reads, redispatch, or protected execution.

## Problem

**Observed fact.** The accepted control contract preserves confirmed, rejected, and indeterminate dispatch observations without automatic redispatch and says later reconciliation retains the original identities.

**Observed fact.** The provisional result-ingress preparer currently turns indeterminacy into a terminal attempt, generic invocation outcome, durable dispatch outcome, and obligation disposition.

**Observed fact.** Existing WorkflowRun replay permits only one terminal attempt state and one dispatch outcome per obligation, so a later confirmed or rejected observation cannot supersede that indeterminate terminal group.

**Human choice.** Select how indeterminate evidence is retained while allowing or intentionally prohibiting later terminal reconciliation.

## Observed current behavior

**Observed fact.** A no-observation reconciliation constructs an indeterminate `SimulationDispatchOutcome` with the request's reserved outcome identity and exact reconciliation identities.

**Observed fact.** `SimulationDispatchResultIngressPreparer` can append that outcome as terminal state. The current replay contract then rejects a second terminal attempt or a second dispatch outcome for the same obligation.

**Observed fact.** `SimulationDispatchOutcomeIdentity` currently identifies the runtime outcome envelope, not a sequence of distinct observations. Reusing it for unequal indeterminate and later confirmed content would violate immutable identity meaning.

**Inference.** The design must distinguish provisional reconciliation evidence from the one final generic Task outcome, or explicitly define indeterminate as irreversible terminal failure.

The immutable inputs inspected for this decision were:

- `harness/tasks/migration.v2.workflows.control-ingress.json`, SHA-256 `516eb84b55526d3823fd93480dccc6cdcd6275679b118789d1cc634d451f0eea`;
- `docs/architecture/migration/v1-to-v2/implementation/control-ingress-effect-bridge.md`, SHA-256 `9be50f73910fc64f0031d82e2124472396642ea31d0d99fa161acae5cc07635a`;
- `docs/architecture/v2/ksdft2effmass/workflows/control-plane.md`, SHA-256 `9b02f6becfc6bd7fb93442dd0dae76cec7f45df2b07f845e00f2acc7f96acc67`;
- `python/src/ksdft2effmass/workflows/control/result_ingress.py`, SHA-256 `0302212b0bdd8ccca2e1d30590f494e5071bfae5b8557cbae947315dfec4cfb5`; and
- `python/src/ksdft2effmass/workflows/runs/replay.py`, SHA-256 `29761ac3f18262cf6959dc833bbaee9dc1650f5f05ffdf52e7f9995e1bc66dd8`.

## Decision requirements

Every option must retain exact original request, attempt, claim, obligation, executor, and reconciliation identities; forbid automatic redispatch; preserve append-only evidence; avoid inventing results; and keep CPN firing exclusive to one confirmed generic outcome. Persistence implementation and external observation acquisition remain separately owned.

## Option A

**Conceptual model.** Introduce distinct immutable dispatch-observation identities and append-only observation records beneath one stable dispatch correlation. Indeterminate observations do not terminalize the Task. A later confirmed or rejected observation may establish one final durable dispatch outcome and terminal generic group.

**Ownership.** WorkflowRun owns observation history and the one final outcome. Reconciliation constructs candidates; persistence commits them later.

**Runtime.** The started attempt and obligation remain pending while only indeterminate observations exist. Each observation has unique identity and immutable content. One correlated confirmed or rejected reconciliation terminalizes exactly once.

**Migration and complexity.** Add observation identity/record contracts, separate observation history from final `DispatchOutcomeRecord`, and update reconciliation, aggregate, replay, ingress, tests, and later serialization.

**Reversibility and future compatibility.** The observation stream naturally supports recovery reads and conflicting evidence. Folding it into terminal outcomes later would lose distinctions.

**Advantage.** Preserves immutable evidence and permits later terminal reconciliation without fabricating a new dispatch.

**Risk.** Adds the largest public and persistence-facing record surface.

## Option B

**Conceptual model.** Keep the current outcome records but make indeterminate state explicitly correctable. Append a later confirmed or rejected dispatch outcome, terminal attempt, generic outcome, and successor obligation disposition for the same stable dispatch.

**Ownership.** WorkflowRun owns an append-only correction chain over dispatch outcomes and dispositions.

**Runtime.** Indeterminate is recorded first; later evidence appends a correction rather than replacing it. Replay determines the effective terminal outcome from the exact predecessor chain.

**Migration and complexity.** Extend outcome identities or add correction identities so unequal content never reuses one immutable envelope identity; allow one indeterminate-to-terminal attempt path and disposition predecessor; update replay and ingress.

**Reversibility and future compatibility.** Correction chains retain history but increase effective-state logic and require careful read-model projection.

**Advantage.** Reuses most existing records and makes correction explicit.

**Risk.** Conflates observation history with effective outcomes and complicates the currently simple one-outcome-per-obligation invariant.

## Option C

**Conceptual model.** Define indeterminate as an irreversible terminal Workflow outcome. Later evidence cannot change that run; any follow-up is a separately authorized new operation with new identities and no claim that it is a retry of the original effect.

**Ownership.** Current terminal records and replay remain authoritative; no correction history is added.

**Runtime.** Indeterminate ingress closes the attempt and obligation once. The system preserves uncertainty permanently and never admits a later result for that dispatch.

**Migration and complexity.** Minimal implementation change; documentation must remove claims of later reconciliation to confirmed or rejected.

**Reversibility and future compatibility.** Adding correction later requires a public-contract migration of historical terminal indeterminate records.

**Advantage.** Smallest deterministic state machine and strongest prohibition on accidental redispatch.

**Risk.** Discards the ability to admit subsequently discovered completion and conflicts with the current retained-identity reconciliation intent.

## Three-option comparison

| Criterion | Option A: observation history | Option B: correction chain | Option C: terminal indeterminate |
|---|---|---|---|
| Later terminal reconciliation | Strong | Strong | None |
| Immutable identity clarity | Strongest | Moderate | Strong |
| Replay complexity | Moderate | Highest | Lowest |
| New public record surface | Highest | Moderate | Lowest |
| Alignment with current intent | Strongest | Strong | Weak |

## Recommendation

Recommend **Option A: distinct append-only observation history with one final outcome**. It cleanly separates uncertain evidence from terminal Task meaning, preserves immutable identities, and keeps successful CPN firing unique. This recommendation authorizes no persistence implementation, external recovery read, redispatch, or scientific acceptance.

## Resolution

The human selected **Option A**. Indeterminate evidence is retained as distinct immutable dispatch observations and does not terminalize the Task. One later correlated confirmed or rejected observation may establish the single final dispatch outcome and terminal generic record group. Workflow control performs no persistence, external recovery read, redispatch, or protected execution.
