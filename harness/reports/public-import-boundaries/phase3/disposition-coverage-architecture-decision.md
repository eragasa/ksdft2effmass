# Disposition coverage reconciliation architecture decision

> **Human-selected architecture:** The operator selected Option A, `cohort_adjacent_overlay_dag`. This durable architecture selection does not accept or close the Task, classify a route, change a disposition, activate D1–D21 or another owner, or establish support, compatibility, public-API, scientific-validation, release, or publication status.

## Problem

**Observed fact:** The accepted Phase 3 plan assigns 985 predecessor routes on 35 F0 package surfaces to D1–D21. The accepted current-fact supplement contains the same 985 predecessor routes, 47 current package surfaces, and 471 separately keyed supplemental candidates (`harness/reports/python-public-import-boundaries-plan.md`; `harness/reports/public-import-boundaries/phase3/foundation.json`; `harness/reports/public-import-boundaries/phase3/current-fact-supplement.json`).

**Inference:** Starting D1 without a coverage architecture would leave twelve post-F0 surfaces and all 471 supplemental candidates outside an explicit decision owner, or would silently broaden an accepted D cohort. Either result would break the required distinction between immutable predecessor lineage and separately keyed current facts.

**Human choice:** This architecture boundary is resolved as Option A: later disposition coverage uses cohort-adjacent supplemental overlays while retaining every predecessor route in its accepted D1–D21 cohort.

## Observed current behavior

**Observed fact:** The current supplement records 47 unique `current_package_surfaces`, 985 unique `predecessor_routes`, and 471 unique `supplemental_candidates`; its summary reports the same cardinalities. Every supplemental candidate is a separately keyed `current-route:` record and retains neutral support and compatibility values (`harness/reports/public-import-boundaries/phase3/current-fact-supplement.json`).

**Observed fact:** The twelve surfaces added after F0 are the four `analysis.model_systems` surfaces, the five `campaigns.research_monograph` surfaces, `integration.wannier90`, `serialization`, and `solid_state`. Supplemental candidates also occur on the predecessor surfaces `analysis`, `campaigns`, and `operators`; being on an existing surface does not make them predecessor routes.

**Observed fact:** The accepted D1–D21 partition is a lineage and decision-ownership partition for the 985 predecessor routes. D21 owns ten accepted zero-route boundaries, including `campaigns`; current `campaigns` now has one supplemental route, but that current fact does not rewrite its accepted zero-boundary lineage (`harness/reports/python-public-import-boundaries-plan.md`).

**Observed fact:** The canonical companion packet is `harness/reports/public-import-boundaries/phase3/disposition-coverage-reconciliation.json`. It accounts once for every current surface, predecessor route, and supplemental candidate. Its decision state is explicitly `human_selected`, and its selected map state is `human_selected_architecture`.

**Observed fact:** The packet contains a frozen closed, non-self-referential request projection reconstructed from the selected Task's stable Task ID, decision question, authorized scope, authority inputs, completion criteria, expected output paths and schema identities, exclusions as the no-mutation boundary, and stop-before-implementation policy. Its canonical 4,829-byte encoding has SHA-256 `8d27b8285bdacde7721e40b6290c60000c16ea76f63b57dc929307420f287ec3`. Mutable `status` and `status_detail` are excluded, so lifecycle reporting cannot create a byte cycle or change this request identity.

**Observed fact:** The authoritative input identities used for this analysis are:

| Path | Bytes | SHA-256 |
|---|---:|---|
| `AGENTS.md` | 35349 | `72146e726e4251437a14e9ac0cf8c16db2750e8daa471f1a0fe03499697d3a9a` |
| `.pi/skills/develop-architecture-decision/SKILL.md` | 3228 | `bfc8e7a41f98a162fb80581b59b7c0e7cd66dcf5ade426cadb74d07055ad0928` |
| `.pi/skills/develop-architecture-decision/references/architecture-decision-conventions.md` | 4880 | `132b81f4f5c32b2d8de49bf1c0c3e08c184e578ded32b9330b3ee7b82255a66d` |
| `harness/reports/python-public-import-boundaries-plan.md` | 30016 | `65d8ed73355ec07f134643e9d1590c65464a7a0e5ec6955744812a1e809561a0` |
| `harness/reports/public-import-boundaries/phase3/foundation.json` | 3908387 | `3da51677747741fc0088d2f31f1359e6e8280bd1555ef514409ccfb5879f9e61` |
| `harness/reports/public-import-boundaries/phase3/current-fact-supplement.json` | 5742970 | `56fb7e16f87b5a7d70af5048a336e18da45f1101cd15f6db1949eac809a037a9` |
| `tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-foundation.json` | 18790 | `3eefffeb3b35196265f83ba2206cf76af10dd13dbdcd907b3da39bf0ca8f3ecf` |
| `tasks/software/python.architecture-refactor.public-import-boundaries.current-fact-supplement.json` | 13389 | `56a1490249c079ff79f777383b47b79e6dafe966195c7d7a0a6962f66296f164` |
| `tasks/software/python.architecture-refactor.public-import-boundaries.json` | 13585 | `771e66e72a905aa9260690213ddceeffcf037a28e33f8b8c9861a22fff2b9766` |

## Decision requirements

**Observed fact:** Accepted authority requires exact-once coverage of 47 current surfaces, preservation of all 985 predecessor routes in their accepted D1–D21 cohorts, and exact-once assignment or explicit deferral of 471 supplemental candidates. New facts must not be aliased to predecessor keys or silently folded into D1 (`tasks/software/python.architecture-refactor.public-import-boundaries.disposition-coverage-reconciliation.json`).

**Observed fact:** Any proposed map must name explicit owner keys, use an acyclic prerequisite graph, retain neutral support and compatibility states, remain reversible before implementation, and preserve accepted F0 and supplement history rather than rewriting either artifact. The typed packet parser rejects closed-schema, discriminant, ordering, relation, duplicate-key, and canonical-encoding defects and validates consistency between the embedded request and its embedded hash; the completion validator reconstructs the stable projection from the live selected Task and rejects live request drift.

**Observed fact:** D1–D21, M1, overlay owners, implementation children, V1, and automatic successor activation remain inactive. This decision-support task remains planning, its parent remains deferred between children, and task acceptance, closeout, successor recording, or implementation requires separate later human authority.

**Human choice:** The architecture choice is resolved as Option A; no route outcome, support state, compatibility disposition, successor boundary, or task acceptance is resolved by that selection. The three compared options differ materially in decision rights, dependency direction, persistent packet boundaries, runtime sequencing, retained history, migration, and failure recovery.

## Option A

**Conceptual model** — **Implementation consequence:** Retain D1–D21 as immutable predecessor-lineage owners and add six separately keyed, domain-cohesive supplemental overlays: analysis/model systems, research-monograph campaigns, Wannier90, operator supplements, serialization, and solid state. Persist one canonical exact-key selected architecture map; later accepted disposition packets remain distinct per predecessor cohort or overlay, preserving both F0 and supplement history.

**Authority** — **Human choice:** A later human decision would authorize each overlay independently. No D owner gains authority over a supplemental key merely because the key shares a package surface.

**Ownership/dependency** — **Implementation consequence:** Dependencies flow from accepted D cohorts into overlays that consume their decisions, never back into predecessor cohorts. A final aggregate consumer may depend on all accepted packets. The proposed graph in the companion JSON is acyclic and gives every assigned key one owner.

**Runtime/dispatch** — **Implementation consequence:** Dispatch remains bounded by owner packet: eligible D work and overlay work can proceed in dependency order, with unrelated roots parallelizable. State is immutable packet output; selection and activation remain external Harness control state.

**Migration** — **Implementation consequence:** Existing D task identities and all 985 route-to-cohort mappings remain unchanged. A later selected architecture would add overlay tasks or equivalent inactive packet owners without altering F0, the supplement, or predecessor keys.

**Reversibility** — **Implementation consequence:** Before disposition implementation, an overlay can be withdrawn or recomputed without touching a D packet. After acceptance, reversal is bounded to the overlay and its downstream aggregate consumers.

**Failures** — **Implementation consequence:** A missing authority item stops only its overlay and dependents; it remains unresolved rather than being converted into unsupported or retired. Cross-domain conflicts stop the dependent overlay or aggregate join without rewriting upstream history.

**Complexity** — **Inference:** Six overlays add more control records than a central owner but materially fewer than per-surface sharding. The graph and exact-key validation are straightforward.

**Maintenance** — **Inference:** Cohesive owners align review and future source mutation planning with domain boundaries while keeping predecessor and supplemental histories visibly separate.

**Context-window consequences** — **Inference:** Each overlay can load only its exact candidates, relevant current surfaces, cited D outputs, and authority evidence. The largest campaign overlay remains substantial but avoids repeatedly loading all 1,456 current routes.

**Future compatibility** — **Inference:** New post-supplement surfaces can receive new overlay owners without renumbering D1–D21 or changing accepted predecessor lineage. Overlay boundaries can later feed M1 without predetermining support or compatibility.

**Advantage** — **Inference:** This model balances bounded review, explicit lineage, partial recovery, and manageable control-plane size.

**Risk** — **Inference:** Cross-domain candidates can require conservative prerequisites or a later serial integration owner, and poorly chosen overlay cohesion could duplicate evidence unless exact keys remain single-owned.

## Option B

**Conceptual model** — **Implementation consequence:** Retain D1–D21 for predecessor lineage and create one central supplemental-coverage authority for all twelve new surfaces and all 471 supplemental candidates. One persistent supplemental disposition packet serializes authority, state, provenance, and history before downstream mutation planning.

**Authority** — **Human choice:** A single later decision boundary controls the entire supplemental universe. Partial acceptance is unavailable unless the central packet is redesigned.

**Ownership/dependency** — **Implementation consequence:** Every supplemental key points to one central owner; D packets and the central owner feed one aggregate stage. Domain owners provide evidence but do not own persistent supplemental decisions.

**Runtime/dispatch** — **Implementation consequence:** Supplemental dispatch is serial and centralized. The owner reads the complete supplement and all applicable authority; D work can run separately, but aggregate progress waits for the central packet.

**Migration** — **Implementation consequence:** D records remain unchanged, while one new task and one packet are inserted before M1. Migrating away later requires splitting a previously accepted central packet with explicit predecessor mappings.

**Reversibility** — **Implementation consequence:** A failed or rejected packet is easy to discard as one unit before implementation, but reverting one domain after acceptance invalidates the whole packet identity and every dependent aggregate.

**Failures** — **Implementation consequence:** Any unresolved candidate blocks central completion. Recovery reruns or reviews the full supplemental packet even when the defect is local.

**Complexity** — **Inference:** Control-plane structure is smallest, but semantic and review complexity is concentrated in one owner and one large artifact.

**Maintenance** — **Inference:** A single schema and validator are simple to locate, while domain evolution creates a central coordination bottleneck and broad ownership boundary.

**Context-window consequences** — **Inference:** The owner must reason over all 47 surfaces, all 471 supplemental candidates, relevant predecessor packets, and cross-domain authority in one context. Bounded mechanical projection is possible, but semantic review remains broad.

**Future compatibility** — **Inference:** Further supplements append naturally to the central ledger, but the owner grows monotonically and can become a permanent architecture bottleneck.

**Advantage** — **Inference:** Exact-once coverage and global consistency have one obvious authority and one atomic rollback point.

**Risk** — **Inference:** The large blast radius, all-or-nothing progress, and centralized domain decision rights conflict with cohesive ownership and bounded review.

## Option C

**Conceptual model** — **Implementation consequence:** Retain D1–D21 for predecessor lineage, create one immutable supplemental shard per affected current surface, and require a serial coverage-join packet before M1. Candidate state and history live in surface packets; the join stores identities and exact coverage, not route outcomes.

**Authority** — **Human choice:** Later human decisions can accept or defer each surface shard independently, while the join has mechanical coverage authority only and cannot adjudicate a shard.

**Ownership/dependency** — **Implementation consequence:** Candidate keys depend on their exact package-surface owner; all shard owners feed a non-adjudicating join. Cross-surface domains require explicit prerequisite edges or a separate integration shard, increasing graph breadth.

**Runtime/dispatch** — **Implementation consequence:** Many shards can dispatch in parallel after prerequisites, followed by a serial join. Persistence consists of numerous small decision packets plus one identity-only join; activation remains explicit per shard.

**Migration** — **Implementation consequence:** Existing D records remain intact. Selection would require recording owners for every affected surface and stable mapping rules for candidates that move between surfaces in later snapshots.

**Reversibility** — **Implementation consequence:** Individual surface packets are highly revertible. Changes to a surface invalidate its packet and the join but need not invalidate sibling packets.

**Failures** — **Implementation consequence:** Local failures remain local until join time; duplicate, omitted, or cross-surface keys fail the join. Domain-level inconsistencies may be discovered late because related surfaces can be reviewed separately.

**Complexity** — **Inference:** This option has the largest task graph, most activation records, and highest projection and review bookkeeping cost.

**Maintenance** — **Inference:** Small packets simplify narrow updates, but persistent surface-level administration and cross-surface consistency checks are ongoing costs.

**Context-window consequences** — **Inference:** Individual reviews use the smallest contexts. The join is mechanically bounded, but reviewers may need multiple packets to understand one domain concept spread across parent and child surfaces.

**Future compatibility** — **Inference:** New surfaces append cleanly as new shards, and unchanged shards remain reusable. Route movement or domain-level policy can make surface identities unstable ownership boundaries.

**Advantage** — **Inference:** Maximum isolation, parallelism, and local rollback are available without rewriting predecessor lineage.

**Risk** — **Inference:** Administrative fragmentation and late integration findings can outweigh the benefits for only 471 supplemental candidates.

## Three-option comparison

**Inference:** Option A allocates authority by cohesive domain overlay, Option B centralizes it, and Option C shards it by package surface. All preserve D1–D21 predecessor ownership and immutable fact history, but their persistent decision boundaries and recovery units differ materially.

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Decision rights | Six domain overlays | One central authority | Surface authorities plus mechanical join |
| Dependency direction | D cohorts to related overlays | Inputs to one central owner | D inputs to shards to join |
| State/persistence/history | Separate D and overlay packets | One supplemental packet | Per-surface packets and identity join |
| Sequencing/runtime | Bounded DAG, partial parallelism | Serial supplemental pass | Broad parallel fan-out, serial join |
| Migration/reversibility | Additive and domain-bounded | Simple addition, broad rollback | Many additions, narrow rollback |
| Failure recovery | Overlay-local | Whole-packet retry | Shard-local plus join retry |
| Complexity/maintenance | Moderate | Low structure, high concentration | High structure and bookkeeping |
| Context-window effect | Domain-bounded | Largest single context | Small shards, cross-packet synthesis |
| Future compatibility | Add overlays without D renumbering | Append to growing central owner | Append surface shards |

**Observed fact:** The companion JSON preserves all three conceptual options, the original A/B/C/D checkpoint, and Option A as the sole advisory recommendation. It now separately records the later human selection of Option A and its exact two-response authority trace.

## Recommendation

**Inference:** Recommend **Option A — cohort-adjacent supplemental overlay DAG**. It preserves accepted D1–D21 identities, keeps every supplemental key visibly separate, bounds semantic review by cohesive domain, permits local failure recovery, and avoids both Option B's central context bottleneck and Option C's surface-level control-plane fragmentation.

**Implementation consequence:** The human-selected Option A map supplies 27 explicit owner keys (D1–D21 plus six overlays), 47 unique surface assignments, 985 unique predecessor assignments with unchanged cohorts, 471 unique supplemental assignments, and an acyclic prerequisite graph. Selection authorizes durable recording of this architecture only; it does not decide support or compatibility, activate implementation, or accept and close this Task.

## Deferred questions

**Deferred question:** For each later owner, which exact routes are supported, unsupported, or unresolved, and which compatibility disposition applies? This task intentionally supplies no answer.

**Deferred question:** Which conservative overlay prerequisites can be narrowed after exact candidate authority citations are available? Narrowing must not infer runtime dependency meaning from lexical adjacency.

**Deferred question:** Whether accepted Option A should be represented as six new tasks, as typed subpackets under a later authorized reconciliation task, or through another contract-equivalent control representation remains an implementation-planning detail requiring separate post-selection authority.

**Deferred question:** PEP 561 installed-package typing, unknown third-party consumers, reflective access, downstream pickle behavior, release, publication, scientific validation, and uncertainty quantification remain outside this decision.

## Human decision required

**Observed fact:** The operator responded exactly `recommendation authorized`, selecting the sole recommendation, Option A; after being told the task awaited durable decision recording and closeout authorization, the operator responded exactly `continue`, authorizing durable recording of Option A only. The A/B/C/D boundary is resolved as A, `cohort_adjacent_overlay_dag`.

- `A — Cohort-adjacent supplemental overlay DAG` — **selected**
- `B — Single central supplemental coverage authority` — not selected
- `C — Surface-sharded supplemental packets with integration join` — not selected
- `D — Reconsider or defer` — not selected

**Human choice:** The final task acceptance and closeout remain separate and unresolved. A later explicit human response is required before closeout, commit, push, successor recording or activation, or dev integration.

**Implementation consequence:** This task remains planning and selected, the Phase 3 parent remains deferred, and D1–D21, M1, all overlays and implementation successors, and automatic successor activation remain inactive.
