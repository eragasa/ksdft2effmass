# Workflow control-ingress native-output admission ownership

Request identity: `migration.v2.workflows.control-ingress.native-output-admission.request.1`

Parent workflow identity: `migration.v2.workflows.control-ingress.lifecycle`

Attempt identity: `migration.v2.workflows.control-ingress.native-output-admission.attempt.1`

Termination policy: stop before selecting or implementing an option; resume only after an explicit human decision.

## Problem

**Observed fact.** A confirmed simulation runtime outcome must retain exact native-output manifest and entry identities so result ingress can admit provenance without reading native calculation files.

**Observed fact.** The resolved effect-bridge decision explicitly deferred the aggregate location of native-output references. The current provisional implementation nevertheless adds them directly to every `ResultProductionRecord`.

**Human choice.** Select the durable ownership surface that correlates a confirmed dispatch result with its native-output manifest entries.

## Observed current behavior

**Observed fact.** `python/src/ksdft2effmass/workflows/control/dispatch.py` places one manifest identity and a nonempty tuple of manifest-entry identities on a confirmed runtime `SimulationDispatchOutcome`.

**Observed fact.** `python/src/ksdft2effmass/workflows/runs/records.py` provisionally broadens generic `ResultProductionRecord` with optional native manifest and entry fields.

**Observed fact.** `python/src/ksdft2effmass/workflows/artifacts.py` already owns manifests, manifest entries, artifact producer provenance, and result-artifact relation identities.

**Observed fact.** Workflow result ingress and artifact persistence are distinct from calculator execution. No option may read native output files, fabricate manifest membership, or claim scientific acceptance.

**Inference.** Production-record storage, a dispatch-specific admission record, and artifact-owned relation resolution are three materially distinct ownership architectures.

The immutable inputs inspected for this decision were:

- `harness/tasks/migration.v2.workflows.control-ingress.json`, SHA-256 `7bde4533f433faab613c37b3e907c54156221959ba86436a185fa7ff16f20a25`;
- `docs/architecture/migration/v1-to-v2/implementation/control-ingress-effect-bridge.md`, SHA-256 `9be50f73910fc64f0031d82e2124472396642ea31d0d99fa161acae5cc07635a`;
- `docs/architecture/v2/ksdft2effmass/workflows/control-plane.md`, SHA-256 `9b02f6becfc6bd7fb93442dd0dae76cec7f45df2b07f845e00f2acc7f96acc67`;
- `docs/architecture/v2/ksdft2effmass/workflows/workflow-run.md`, SHA-256 `76c14d7cc0800b97783fcb30f1da2c870e14c6e51f4696155dee45392cdd49c9`;
- `python/src/ksdft2effmass/workflows/runs/records.py`, SHA-256 `f7811fcf2cf49dfe5cd060d9eb8a36d0f50e66b85463658e57e722387be4c6e2`; and
- `python/src/ksdft2effmass/workflows/control/dispatch.py`, SHA-256 `f9cbea701e47d113646af42955fe11811cce61851d3f2672059f88bcfad39b03`.

## Decision requirements

**Observed fact.** Every option must preserve exact dispatch, result, production, manifest, and admitted-entry identities; immutable history; deterministic correlation; and artifact ownership of manifest membership.

**Observed fact.** The selected surface must distinguish runtime observation from durable ingress and must not make all result production simulation-specific without an explicit reason.

**Observed fact.** Wire formats, repository storage, native-file parsing, and artifact persistence remain outside this decision.

**Human choice.** Select whether native-output admission is represented directly on generic production, in a dedicated dispatch-specific admission record, or solely through artifact-owned relations.

## Option A

**Conceptual model**
Keep optional native manifest and manifest-entry identities directly on `ResultProductionRecord`; simulation production populates them and ordinary production omits them.

**Authority**
The production record reports exact supplied artifact identities but does not establish manifest integrity, file content, calculation validity, or scientific acceptance.

**Ownership/dependency**
Runs owns the fields while importing artifact identity types. Artifact objects continue to own manifest and entry contents.

**Runtime/dispatch**
Confirmed ingress constructs the result reference and production record together, copying exact native-output identities from the reconciled runtime outcome.

**Migration**
Retain the provisional fields, complete replay correlation, update all constructors and serialization later, and migrate existing production records with absent values.

**Reversibility**
Removing the fields later requires migration of every production record that used them.

**Failures**
Missing, empty, or mismatched native references reject simulation production ingress. Generic non-simulation production remains valid without them.

**Complexity**
Lowest immediate implementation complexity.

**Maintenance**
Every generic production consumer and future wire schema must understand simulation-specific optional fields.

**Context-window consequences**
Generic result-production reviews must include native-output admission rules even when no dispatch exists.

**Future compatibility**
Simple for one native manifest per production, less flexible for multiple output sets or later admission revisions.

**Advantage**
Requires the fewest records and provides direct lookup from production to native output.

**Risk**
Broadens a generic production contract with dispatch-specific artifact state and duplicates relation semantics.

## Option B

**Conceptual model**
Add a dedicated immutable native-output admission record correlating the dispatch outcome, result production, manifest, and exact admitted entries. Keep `ResultProductionRecord` generic.

**Authority**
The admission record states only that exact supplied entries were admitted for the represented dispatch production. Artifact owners retain content and manifest integrity authority.

**Ownership/dependency**
Workflow runs own the dispatch-specific correlation record; artifact identities remain owned by the artifact model. Generic production remains independent of dispatch-specific fields.

**Runtime/dispatch**
Confirmed ingress atomically adds the dispatch outcome, result reference, production record, and one native-output admission record. Replay requires exact one-to-one closure for simulation-confirmed production.

**Migration**
Remove provisional native fields from `ResultProductionRecord`, add the new record and aggregate collection, update replay and tests, and later define persistence for the new record.

**Reversibility**
The record can be retired or generalized independently without changing generic production identities.

**Failures**
Missing, duplicated, or mismatched admissions fail replay. A runtime outcome with no durable admission cannot become a complete confirmed ingress candidate.

**Complexity**
Moderate because it adds one public record, identity, aggregate collection, and replay rules.

**Maintenance**
Dispatch-specific native admission remains localized; generic result consumers remain simpler.

**Context-window consequences**
Dispatch ingress reviews need the admission record, while ordinary result-production reviews do not.

**Future compatibility**
Can support multiple manifests, admission revisions, or additional dispatch provenance without expanding generic production.

**Advantage**
Makes simulation-specific admission explicit and preserves clean ownership boundaries.

**Risk**
Adds another correlation record and increases aggregate/replay inventory.

## Option C

**Conceptual model**
Keep production limited to `ResultArtifactRelationIdentity` values. Resolve manifest and entry membership exclusively through artifact-owned manifests and relation records supplied to ingress.

**Authority**
Artifact-owned records alone establish represented manifest membership. Workflow records refer only to exact result-artifact relations and dispatch/result identities.

**Ownership/dependency**
Artifacts owns the complete native-output relation model. Runs and control consume relation identities without owning manifest-entry correlations.

**Runtime/dispatch**
Confirmed ingress verifies that supplied artifact relations resolve to the runtime outcome's exact manifest entries through an explicit artifact bundle, then stores only relation identities in production.

**Migration**
Remove provisional native fields, define or reuse exact artifact relation records and an explicit resolver bundle, and update replay to accept those immutable artifact inputs.

**Reversibility**
Workflow records remain stable if artifact relation internals evolve, but changing resolver contracts or reconstructing absent relation evidence is costly.

**Failures**
Unavailable or inconsistent artifact bundles fail ingress or replay. Cross-object resolution adds another source of unsupported-version and missing-evidence outcomes.

**Complexity**
High resolver and replay-input complexity despite the smallest WorkflowRun record footprint.

**Maintenance**
Artifact semantics remain centralized, but Workflow replay depends on externally supplied artifact closure.

**Context-window consequences**
Dispatch-result review must include artifact manifests, relation records, resolver bundles, and version contracts.

**Future compatibility**
Best if many subsystems need one general artifact relation graph independent of Workflow runs.

**Advantage**
Avoids duplicating artifact membership and keeps generic production limited to general relation identities.

**Risk**
Weakens self-contained Workflow replay and introduces cross-object availability and version-coordination costs.

## Three-option comparison

| Criterion | Option A: production fields | Option B: admission record | Option C: artifact-owned resolution |
|---|---|---|---|
| Generic production purity | Weak | Strong | Strongest |
| Self-contained run replay | Strong | Strong | Weak |
| Added records | None | One explicit record | External relation bundle |
| Dispatch-specific locality | Weak | Strongest | Moderate |
| Cross-object coordination | Low | Low | High |
| Immediate complexity | Lowest | Moderate | Highest |
| Future extensibility | Low | High | High |
| Migration burden | Low | Moderate | High |

## Recommendation

Recommend **Option B: a dedicated native-output admission record**. It preserves generic result production, makes dispatch-specific admission explicit, keeps replay self-contained, and avoids the external coordination required by artifact-only resolution.

The human selected Option B with the verbatim response `1A and 2B selected`. Bounded implementation may now add the dedicated dispatch-specific native-output admission record and remove the provisional simulation-specific fields from generic result production.

## Deferred questions

**Deferred question.** Exact wire format and persistence of the admission record remain with `migration.v2.workflows.persistence`.

**Deferred question.** Native file parsing, manifest creation, checksums, and calculator-specific provenance remain owned by calculators, integrations, and artifacts rather than Workflow control.

**Deferred question.** Multi-manifest and supersession behavior should be added only when a demonstrated consumer requires it.

## Human decision required

The human selected **Option B: a dedicated dispatch-specific native-output admission record**. Options A and C remain excluded. The Task must stop again if implementation exposes another material human-owned or protected boundary.
