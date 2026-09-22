# Prerequisite-result resolution architecture

Request identity: `migration.v2.harness.prerequisite-resolution.architecture-decision.request.1`

Parent workflow identity: `migration.v2.harness.prerequisite-resolution.lifecycle`

Attempt identity: `migration.v2.harness.prerequisite-resolution.architecture-decision.attempt.1`

Termination policy: stop before implementation until the human selects one architecture.

## Problem

**Observed fact.** `migration.v2.harness.prerequisite-resolution` requires an accepted prerequisite-fact contract before implementation.

**Human choice.** Decide where typed prerequisite requirements live and who owns their evolution.

## Observed current behavior

**Observed fact.** `HarnessTask` stores Task and external prerequisite identities but deliberately leaves lifecycle status opaque. Task status, selection, planning prose, passing tests, reviewer agreement, and graph readiness cannot satisfy prerequisites.

**Observed fact.** The retired `ChainStateEvaluator` inferred Task satisfaction from configured status strings and external satisfaction from caller-supplied identifier sets. The accepted v2 Task-model contract rejects those rules as a new prerequisite-result model.

**Observed fact.** Results remain with their domain owners. Prerequisite resolution grants no operation authority and does not copy scientific or protected-authority state into Harness state.

**Inference.** Existing authority fixes those separation boundaries but does not determine requirement ownership or persistence.

The immutable inputs reviewed for this decision were:

- `harness/tasks/migration.v2.harness.prerequisite-resolution.json`, SHA-256 `7e058551610532466e029313247d8631c2f8638dcc109b9f9949f36c92591bab`;
- `harness/task-selection.json`, SHA-256 `efa9cd04905e4513c5530ddf901198855918233de31078d551dc34467101f4d2`;
- `harness/tasks/migration.v2.harness.task-model.json`, SHA-256 `0ac2ff019ca26d41a281b4e4f49294ea8f3c35d0c5d572bf5ed15eebde009d7c`;
- `harness/tasks/migration.v2.harness.decisions-authority.json`, SHA-256 `dd78314be7a014262224635a9419706e9c1b3312c58a125862b992ede657da7b`;
- `docs/architecture/migration/v1-to-v2/implementation/harness/task-model.md`, SHA-256 `c958ffa3f7f594656c58503bc19dda842056ca2dfb47ca738b79ec24d61630c7`; and
- the applicable accepted v2 Harness object-model and control-plane pages.

## Decision requirements

**Observed fact.** Every defensible architecture must preserve Task and external prerequisite distinctions, match exact retained owner-produced results, avoid lifecycle-status heuristics, preserve identity and lineage, and remain separate from selection, activation, and operation authority.

**Human choice.** Select the owner and persistence model for typed prerequisite requirements.

All options use per-edge outcomes `satisfied`, `missing`, `conflicting`, `superseded`, `revoked`, `unavailable`, and `indeterminate`. The aggregate is satisfied only when every declared edge is satisfied.

## Option A

**Conceptual model**
Consumer-scoped immutable sidecar contracts bind every declared prerequisite edge to the exact consumer Task content identity, required owner, result kind, claim, producer revision constraints, retention boundary, and lineage policy. Result payloads remain with their owners; the sidecar contains requirements only.

**Authority**
The consumer contract defines what satisfies its dependency. Result owners remain authoritative for result identity, availability, integrity, and effective lineage. Neither side grants operation authority.

**Ownership/dependency**
The Harness owns each sidecar contract and pure resolver. Domain owners retain referenced results. `HarnessTask` and `HarnessTaskRegistry` remain topology owners and do not depend on the resolver.

**Runtime/dispatch**
`DevelopmentPrerequisiteResolver` receives the exact Task, its identity-bound contract, and a complete explicitly supplied observation set. Every observation binds its owner and retention boundary, including absent, unavailable, and indeterminate observations. The accepted consumer lineage policy is exactly `effective_not_revoked`: only one effective matching result satisfies an edge. The resolver performs no repository discovery, persistence, activation, selection, authorization, repair, or successor choice.

**Migration**
Task wire version 3 remains unchanged. Named legacy adapters may produce identity-bound references from exact retained bytes under an explicit mapping contract; opaque status strings never become results.

**Reversibility**
The sidecar and resolver surfaces can be retired or composed into a future `HarnessState` without migrating every Task record.

**Failures**
An observation failure is `indeterminate`; an identified object that cannot be obtained is `unavailable`; a complete successful absence observation is `missing`; multiple effective candidates or contradictory lineage are `conflicting`; explicit lineage produces `revoked` or `superseded` as applicable.

**Complexity**
Moderate. It adds bounded contracts and matching behavior without changing canonical Task serialization.

**Maintenance**
Requirement changes affect the consumer sidecar. Exact Task-content binding and complete edge coverage prevent silent drift.

**Context-window consequences**
Review normally requires one Task, one sidecar, and the referenced owner-result contracts.

**Future compatibility**
New result kinds and owner domains normally require no Task schema change. Future Harness compilation may normalize the same contracts without changing their meaning.

**Advantage**
It most directly preserves consumer requirement ownership and producer result ownership while enabling a bounded implementation.

**Risk**
A missing or stale sidecar blocks resolution; deterministic validation must enforce exact Task binding and edge coverage.

## Option B

**Conceptual model**
Version `HarnessTask` so every prerequisite declaration embeds its typed result requirement and matching policy.

**Authority**
The Task record owns both topology and satisfaction semantics; result owners still own actual result truth.

**Ownership/dependency**
Consumers depend on an expanded Task schema, coupling topology to result-owner contracts.

**Runtime/dispatch**
The resolver reads requirements directly from the Task and matches explicit owner observations.

**Migration**
Every canonical Task, schema, serializer, fixture, projection, and consumer requires migration to a new wire version.

**Reversibility**
Reversal is expensive after migrated Task records become canonical.

**Failures**
The same closed outcomes apply, driven by embedded matching rules.

**Complexity**
High migration complexity with simpler lookup after migration.

**Maintenance**
Requirement evolution rewrites canonical Task records and may repeatedly evolve the Task wire.

**Context-window consequences**
Each Task is self-contained, but reviews must account for a larger coupled public wire contract.

**Future compatibility**
New result semantics may require further Task-wire versions.

**Advantage**
No separate requirement lookup exists at runtime.

**Risk**
Stable topology becomes durably coupled to evolving result semantics.

## Option C

**Conceptual model**
Add one centralized `DevelopmentPrerequisitePolicyCatalog` to normalized Harness state, mapping exact Task-edge identities to typed matching policies while referencing owner-retained results.

**Authority**
The catalog controls matching semantics; result owners control result truth. Neither controls operation authority.

**Ownership/dependency**
Harness composition owns a shared catalog, and every consumer depends on it. The Task graph remains nominally authoritative for topology, but the catalog duplicates edge-keyed information.

**Runtime/dispatch**
The resolver looks up edge policies in an explicitly supplied immutable catalog and matches explicit owner observations.

**Migration**
The Task wire remains unchanged, but complete `HarnessState`, compiler, persistence, validation, and projection integration become prerequisites.

**Reversibility**
Removing the catalog requires migrating all catalog consumers and normalized-state revisions.

**Failures**
The same closed outcomes apply; missing or contradictory catalog entries also block resolution.

**Complexity**
High aggregate and persistence complexity.

**Maintenance**
Centralized policy inspection is easier, but catalog entries can drift from canonical Task edges.

**Context-window consequences**
Changes require examining the shared catalog and all affected Tasks.

**Future compatibility**
It may support cross-project policy tooling after normalized Harness infrastructure is mature.

**Advantage**
One normalized policy inventory supports global inspection.

**Risk**
It is premature and can become a second topology registry.

## Three-option comparison

| Criterion | Option A: sidecars | Option B: Task wire | Option C: central catalog |
|---|---|---|---|
| Preserve Task v3 | Yes | No | Yes |
| Consumer/result-owner separation | Strong | Moderate | Strong |
| Bounded implementation now | Yes | No | No |
| Migration cost | Moderate | High | High |
| Drift risk | Sidecar versus bound Task | Schema coupling | Catalog versus Task graph |
| Deferred dependencies | Minimal | Task migration | Compiler and persistence |
| Reversibility | High | Low | Moderate to low |
| Expected technical debt | Lowest with exact binding | Highest | Moderate to high while infrastructure is deferred |

## Recommendation

Recommend **Option A: consumer-scoped immutable sidecar contracts**. It is the smallest architecture that preserves the stable Task wire, keeps consumer requirements separate from producer-owned results, and remains compatible with future normalized Harness composition.

## Deferred questions

**Deferred question.** Exact future `HarnessState` normalization belongs to the compiler and persistence Tasks.

**Deferred question.** A serialized sidecar wire beyond the initial canonical repository contract is warranted only by an actual consumer.

**Deferred question.** Scientific result kinds remain owned by their scientific domains and require separately accepted contracts when introduced.

**Observed compatibility limitation.** The pre-existing generated SQLite projection derives `task_state.is_active` from the opaque Task status spelling `active`; it does not consume canonical `harness/task-selection.json`. The accepted Task-model contract makes selection canonical and status opaque. Correcting that generated projection behavior belongs to its owning projection or validation Task, not this prerequisite resolver; this Task changes neither status semantics nor projection ingestion.

## Human decision required

The human selected the recommendation with the verbatim response `recommend authorized`, resolving this decision as Option A. Implementation remains bounded by the lifecycle authorization and must stop again if a new material human-owned choice or protected boundary appears.
