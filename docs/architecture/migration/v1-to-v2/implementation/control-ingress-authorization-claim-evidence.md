# Workflow control-ingress authorization and committed-claim evidence

Request identity: `migration.v2.workflows.control-ingress.authorization-claim-evidence.request.1`

Parent workflow identity: `migration.v2.workflows.control-ingress.lifecycle`

Attempt identity: `migration.v2.workflows.control-ingress.authorization-claim-evidence.attempt.1`

Termination policy: stop before selecting or implementing an option; resume only after an explicit human decision.

## Problem

**Observed fact.** The resolved effect-bridge decision permits `SimulationDispatchEffect` invocation only after a persistence-owned compare-and-swap claim is committed.

**Observed fact.** The current provisional implementation embeds full authorization results in `WorkflowRun`, creating a `runs` to `control` dependency while control already depends on runs. It accepts a claimed reservation at dispatch without typed evidence that persistence committed it. Replay and dispatch also assign incompatible authorization-result identities to the claim.

**Human choice.** Select the ownership and evidence model for preparation- and claim-phase authorization and for proof of the committed claim at the effect boundary.

## Observed current behavior

**Observed fact.** `docs/architecture/migration/v1-to-v2/implementation/control-ingress-effect-bridge.md` selected an application-supplied Workflow effect port but explicitly deferred the aggregate location of closed authorization results.

**Observed fact.** `python/src/ksdft2effmass/workflows/runs/aggregate.py` provisionally retains complete `SimulationExecutionAuthorizationResult` values imported from `workflows.control.authority`.

**Observed fact.** `python/src/ksdft2effmass/workflows/control/dispatch.py` computes a distinct claim-phase authorization result after receiving a claimed reservation, then may invoke the effect without a persistence commit receipt.

**Observed fact.** `python/src/ksdft2effmass/workflows/runs/replay.py` provisionally requires a claim record to reuse the reservation's preparation authorization-result identity, so it cannot agree with the adapter's distinct claim-phase result.

**Inference.** Exact authority history and committed-claim evidence must be redesigned together because the effect boundary depends on both.

The immutable inputs inspected for this decision were:

- `harness/tasks/migration.v2.workflows.control-ingress.json`, SHA-256 `7bde4533f433faab613c37b3e907c54156221959ba86436a185fa7ff16f20a25`;
- `docs/architecture/migration/v1-to-v2/implementation/control-ingress-effect-bridge.md`, SHA-256 `9be50f73910fc64f0031d82e2124472396642ea31d0d99fa161acae5cc07635a`;
- `docs/architecture/v2/ksdft2effmass/workflows/control-plane.md`, SHA-256 `9b02f6becfc6bd7fb93442dd0dae76cec7f45df2b07f845e00f2acc7f96acc67`;
- `docs/architecture/v2/ksdft2effmass/workflows/service-model.md`, SHA-256 `d2619353d58b987c6d2e8a8b51335cbc728ca2f6d53e45a404d27e423ed1ffe5`;
- `docs/architecture/v2/ksdft2effmass/workflows/workflow-run.md`, SHA-256 `76c14d7cc0800b97783fcb30f1da2c870e14c6e51f4696155dee45392cdd49c9`;
- `python/src/ksdft2effmass/workflows/runs/aggregate.py`, SHA-256 `2c3792b53952c58e7056fa3d1ea979e910b7cfaa0df945abb68893e61191d23f`; and
- `python/src/ksdft2effmass/workflows/control/dispatch.py`, SHA-256 `f9cbea701e47d113646af42955fe11811cce61851d3f2672059f88bcfad39b03`.

## Decision requirements

**Observed fact.** Every option must retain distinct preparation- and claim-phase authorization evidence, exact grant and request correlation, append-only history, deterministic replay, and a fail-closed effect boundary.

**Observed fact.** Persistence owns commit atomicity and the eventual repository contract. Control ingress may consume typed commit evidence but may not implement Workflow serialization, repository compare-and-swap, SQLite behavior, or recovery.

**Observed fact.** Denied, stale, losing, mismatched, or uncommitted claims must perform no effect. A commit receipt proves only the represented persistence operation, not scientific validity or execution success.

**Human choice.** Select whether complete authorization evidence is run-owned, ledger-owned, or embedded in lifecycle records, and select the corresponding committed-claim attestation.

## Option A

**Conceptual model**
Move immutable authorization DataObjects beneath the run owner, retain complete preparation- and claim-phase results in `WorkflowRun`, and require a typed persistence commit receipt naming the exact claimed run revision before dispatch.

**Authority**
The external authority source still issues grants. Workflow-owned pure authorization results record checks only. The persistence receipt proves that the exact claim candidate was committed but grants no authority independently.

**Ownership/dependency**
Runs owns the lower-level immutable authorization contracts; control imports them. This removes the provisional `runs` to `control` dependency and keeps replay self-contained.

**Runtime/dispatch**
Preparation creates and retains its result. Claim preparation creates a distinct claim-phase result and claimed record. Persistence commits that candidate and returns a typed receipt. The adapter validates the receipt, committed revision, claim result, request, and effect scope before invocation.

**Migration**
Relocate provisional authorization classes without retaining the current module cycle; update exports, replay, tests, and documentation. The later persistence Task implements receipt production against the selected receipt contract.

**Reversibility**
The receipt can later gain additional persistence metadata without changing historical authorization meaning. Moving complete results out of runs later would require migration.

**Failures**
Missing or mismatched authorization results, stale revisions, unsuccessful commit receipts, and scope mismatches fail before the effect. Replay rejects incomplete phase history.

**Complexity**
Moderate aggregate and replay complexity with one new persistence-facing receipt type.

**Maintenance**
One aggregate closes its own authority evidence. Persistence and control share only the exact receipt contract.

**Context-window consequences**
A replay review needs the run-owned authorization records but not a second ledger. Dispatch review additionally needs the compact receipt contract.

**Future compatibility**
Supports multiple authority resolvers and persistence implementations while preserving one self-contained run history.

**Advantage**
Provides the strongest self-contained replay with minimal cross-aggregate coordination and a clear acyclic dependency direction.

**Risk**
Enlarges `WorkflowRun` and makes the selected receipt a public persistence/control boundary before the persistence implementation exists.

## Option B

**Conceptual model**
A distinct append-only authority ledger owns grants, snapshots, and complete phase results. `WorkflowRun` retains exact references only. Dispatch requires both ledger evidence and a typed persistence claim-commit receipt.

**Authority**
The ledger records authority evaluation without issuing authority. Workflow control consumes exact referenced evidence; persistence separately attests the committed claim.

**Ownership/dependency**
A lower-level authority-ledger package is independent of runs and control. Both depend on its references and records; control also consumes the persistence receipt.

**Runtime/dispatch**
Preparation and claim write or obtain ledger records, candidate runs retain their identities, persistence commits the claimed run, and dispatch resolves both ledger and receipt evidence before invoking the effect.

**Migration**
Remove provisional complete results from `WorkflowRun`, introduce ledger identities and access contracts, and migrate replay to require externally supplied exact ledger evidence.

**Reversibility**
The ledger can evolve independently, but folding it back into runs requires cross-stream migration and retained-reference reconciliation.

**Failures**
Missing ledger entries, inconsistent ledger/run state, stale commit receipts, and unavailable authority history fail closed. Cross-stream partial failure requires explicit recovery.

**Complexity**
High because replay and dispatch coordinate two append-only evidence streams plus persistence receipts.

**Maintenance**
Authority concerns are strongly separated, but every consumer must preserve cross-stream consistency and lifecycle ordering.

**Context-window consequences**
Reviews require run, ledger, resolver, and receipt contracts together, increasing the minimum evidence surface.

**Future compatibility**
Best supports reuse of one authority ledger across multiple aggregate types or services.

**Advantage**
Provides the clearest independent authority ownership and avoids enlarging every run revision with complete result values.

**Risk**
Introduces cross-stream consistency, availability, replay, and recovery complexity not otherwise required by the current project.

## Option C

**Conceptual model**
Remove standalone authorization-result storage and embed complete phase-specific authorization evidence directly in reserved and claimed lifecycle records. Dispatch requires a committed, replay-equal claimed-run attestation.

**Authority**
Each lifecycle record carries the exact evidence establishing that phase. The committed-run attestation proves persistence accepted the claimed successor but does not itself grant authority.

**Ownership/dependency**
Runs owns heavier reservation and claim records and replay closure. Control constructs and validates them. Persistence attests the exact committed claimed revision.

**Runtime/dispatch**
Preparation embeds unused-grant evaluation in the reservation. Claim embeds reserved-grant evaluation in the claimed successor. Persistence returns an attestation naming that successor, and dispatch validates the attested replay-equal run and claim before the effect.

**Migration**
Remove provisional standalone result collections, split or expand lifecycle records by phase, and migrate all correlation and replay evidence to embedded structures.

**Reversibility**
Extracting embedded evidence into reusable standalone records later is possible but requires history migration and new identities.

**Failures**
Partial or mismatched phase evidence makes the lifecycle record invalid. An unattested or non-replay-equal claimed run performs no effect.

**Complexity**
Moderate-to-high record complexity with fewer top-level collections but heavier lifecycle variants.

**Maintenance**
Evidence remains adjacent to its state transition, but authorization and reservation concerns become tightly coupled.

**Context-window consequences**
A control review needs fewer collections but must inspect large phase-specific records and their replay rules.

**Future compatibility**
Supports additional lifecycle phases by adding variants, at the cost of further record growth.

**Advantage**
Makes each reservation or claim locally evidence-complete and avoids a separate ledger or standalone result index.

**Risk**
Mixes authorization evaluation with reservation history and may duplicate common grant and snapshot evidence across phases.

## Three-option comparison

| Criterion | Option A: run-owned results and receipt | Option B: authority ledger and receipt | Option C: embedded phase evidence and run attestation |
|---|---|---|---|
| Self-contained WorkflowRun replay | Strong | Weak | Strong |
| Acyclic runs/control dependency | Strong | Strong | Strong |
| Authority separation | Moderate | Strongest | Weakest |
| Cross-stream coordination | Low | High | Low |
| Record size | Moderate | Lowest in run | Highest per lifecycle record |
| Persistence-facing proof | Compact commit receipt | Compact commit receipt | Claimed-run attestation |
| Migration complexity | Moderate | High | High |
| Reversibility | Moderate | Moderate | Lowest |

## Recommendation

Recommend **Option A: run-owned complete authorization evidence plus a typed persistence commit receipt**. It preserves self-contained deterministic replay, removes the provisional dependency cycle, distinguishes preparation and claim results, and provides the narrowest typed proof required before effect invocation without implementing persistence.

The human selected Option A with the verbatim response `1A and 2B selected`. Bounded implementation may now relocate the immutable authorization contracts beneath the run owner, retain complete distinct phase results, and introduce typed committed-claim evidence without implementing persistence.

## Deferred questions

**Deferred question.** Exact receipt serialization, repository operations, transaction validation, recovery, and SQLite behavior remain with `migration.v2.workflows.persistence`.

**Deferred question.** Input-artifact authority resolution depends on the selected native-output/artifact ownership and later artifact ingress contracts.

**Deferred question.** Cancellation, lease expiry, operator interruption, and automatic retry policy remain outside this decision.

## Human decision required

The human selected **Option A: run-owned complete authorization evidence plus a typed persistence commit receipt**. Options B and C remain excluded. The Task must stop again if implementation exposes another material human-owned or protected boundary.
