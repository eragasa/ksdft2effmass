# Workflow normalized-observation input boundary

## Problem

**Human choice:** Select the calculator-independent public boundary by which Workflow
normalization consumes an integration-owned extracted-observation ResultObject and
produces a Workflow-owned `NormalizedObservationSet` without importing a concrete
calculator integration.

The choice must preserve the accepted two-stage Option C architecture, exact source
and policy correlation, operational immutability, strict typing, and a result that can
be consumed by analysis without fabricating provenance or changing the retained
schema-version-1 neutral plane-wave record.

## Observed current behavior

**Observed fact:** `QuantumEspressoExtractedObservationResult` is a frozen
integration-owned ResultObject containing a neutral
`KohnShamPlaneWaveCalculationRecord`, Workflow-owned artifact and producer identities,
integration-owned parsed-document and parser identities, an integration-owned
normalization policy, and canonical limitations
(`python/src/ksdft2effmass/integration/quantum_espresso/observation.py`).

**Observed fact:** The resolved observation-adaptation checkpoint selected two stages:
QE integration owns exact extraction and a separately activated Workflow Task owns
normalization assembly and `NormalizedObservationSet`
(`.pi/checkpoints/migration.v2.integration.quantumespresso.adaptation.result-boundary.json`).

**Observed fact:** Dependency direction prohibits `workflows` from importing
`integration.quantum_espresso`; integration may import Workflow and neutral Kohn--Sham
contracts
(`docs/architecture/migration/v1-to-v2/package-module-crosswalk.md`).

**Observed fact:** Analysis may import Workflow and Kohn--Sham contracts but never a
calculator package, and the documented analysis path consumes
`NormalizedObservationSet`
(`docs/architecture/v2/ksdft2effmass/analysis/index.md`).

**Observed fact:** The public Workflow `ResultObject` protocol exposes only
`ResultObjectIdentity`; it does not expose a scientific payload or extraction lineage
(`python/src/ksdft2effmass/workflows/model.py`).

**Inference:** The selected two-stage owner boundary does not determine whether the
Workflow result retains the concrete source through a typed protocol, copies a closed
neutral snapshot, or stores only references requiring later source resolution.

## Decision requirements

**Observed fact:** The active Task requires one calculator-independent typed boundary,
exact source, parser, policy, result, limitation, failure, and lineage correlation,
strict typing without `Any` or `object`, and no QE integration import from Workflow
(`harness/tasks/migration.v2.workflows.normalized-observations.json`).

**Observed fact:** Maintained results must be operationally immutable, and reusable
cross-object transformation belongs to an ActionObject
(`AGENTS.md` and `.pi/skills/design-data-action-objects/SKILL.md`).

**Observed fact:** No new neutral wire format, persistence mechanism, dependency, or
protected execution is authorized by the active Task.

**Human choice:** Decide whether the Workflow-owned set carries the exact concrete
source object through a structural protocol, owns a copied calculator-independent
snapshot, or owns reference-only membership resolved elsewhere.

## Option A

**Conceptual model:** Define a Workflow-owned read-only
`NormalizedObservationSource` protocol extending `ResultObject` and exposing the
neutral Kohn--Sham record plus exact artifact, parser, policy, and limitation
properties. `NormalizedObservationSet` retains a tuple of those source objects, and a
pure assembler validates their complete correlations.

**Authority:** The active Workflow Task adds only Workflow protocol, request, result,
failure, and assembler contracts; the accepted integration result and neutral record
remain unchanged.

**Ownership/dependency:** Workflow imports the calculator-independent neutral
Kohn--Sham record and Workflow identity owners but not QE integration. The concrete QE
result conforms structurally without a reverse integration import.

**Runtime/dispatch:** The caller passes already-existing extracted ResultObjects. The
assembler validates the protocol and correlations, performs no lookup or persistence,
and returns a set retaining the exact source objects.

**Migration:** Existing integration results become directly admissible without copying
or adapters. Other integrations must implement the same Kohn--Sham source protocol.

**Reversibility:** The protocol can gain a versioned successor, but consumers that rely
on concrete nested source types may require adaptation.

**Failures:** Wrong source shape, empty membership, duplicate result identity, or
inconsistent lineage returns a closed correlated assembly failure; no partial set is
returned.

**Complexity:** One protocol, request, result, failure family, and assembler are added
to Workflow.

**Maintenance:** Exact source identity objects remain owned by their concrete domains;
Workflow maintains only the structural consumption contract and set invariants.

**Context-window consequences:** Review spans the new Workflow module, the accepted QE
result, the neutral record, public exports, focused tests, and synchronized docs.

**Future compatibility:** Additional Kohn--Sham integrations can conform directly;
non-Kohn--Sham observation families require another explicit protocol or a versioned
union.

**Advantage:** Preserves every exact source object without modifying the accepted
integration result or inventing replacement identities.

**Risk:** A structural immutability promise cannot itself prove that every future
third-party protocol implementation is frozen, and the public set exposes concrete
source implementations through the protocol.

## Option B

**Conceptual model:** Define a Workflow-owned immutable
`NormalizedObservationEntry` that copies the neutral Kohn--Sham record and Workflow
artifact identities while converting integration-owned parsed-document, parser, and
policy identities into explicit owner-qualified external identity references.
`NormalizedObservationSet` stores only these Workflow-owned entries.

**Authority:** The active Workflow Task owns the copied result shape and identity
reference representation; no integration or neutral source contract is changed.

**Ownership/dependency:** Workflow imports the neutral Kohn--Sham record and its own
artifact identities. It does not import QE, but it introduces a generic owner-qualified
reference type for external identity domains.

**Runtime/dispatch:** The assembler reads a structural source protocol, validates every
field, snapshots the represented values into new frozen entries, and discards the
concrete source object from the returned set.

**Migration:** Existing QE results require no source change, but the new external
identity-reference mapping becomes a public compatibility boundary for every future
integration.

**Reversibility:** Snapshot fields can evolve by adding a new result version; changing
owner/value reference semantics after adoption requires migration.

**Failures:** Unrepresentable external identities, duplicate sources, mismatched
artifact correlation, or unsupported observation families return closed failures
without partial entries.

**Complexity:** Adds a source protocol, external identity-reference DataObject, copied
entry, set, request, failure family, and assembler.

**Maintenance:** Workflow owns stable snapshots and must keep their copied fields
synchronized with source protocols while concrete integrations retain native meaning.

**Context-window consequences:** Review includes the source protocol, new reference
semantics, copying invariants, compatibility tests, public documentation, and future
migration consequences.

**Future compatibility:** Other integrations can map into the snapshot without leaking
concrete types, provided their identity domains fit the owner-qualified reference
contract.

**Advantage:** The returned set is operationally immutable and independent of the
lifetime or mutability of supplied source objects.

**Risk:** Copying creates a second representation of exact source correlation and may
mistakenly equate lexical owner/value references with the original nominal identity
objects.

## Option C

**Conceptual model:** Define `NormalizedObservationSet` as an immutable reference-only
aggregate containing existing Workflow `ResultObjectReference`, artifact-manifest,
entry, content, and producer references. The concrete extracted result and neutral
observation are resolved separately by the analysis composition.

**Authority:** The active Task adds a Workflow set and assembler over existing generic
reference contracts; a later application or persistence Task must own resolution of
concrete source values.

**Ownership/dependency:** Workflow remains independent of both integration and neutral
Kohn--Sham packages. Application or analysis imports the concrete domains and supplies
resolved values separately.

**Runtime/dispatch:** The assembler validates reference closure only. Analysis must
receive the set plus an explicit resolver or already-resolved source-result mapping;
there is no hidden lookup.

**Migration:** Existing extracted results must first have exact Workflow result
references. Consumers must change from direct set consumption to set-plus-resolution
composition.

**Reversibility:** Reference membership is stable, but adding embedded normalized
values later creates a materially new result version.

**Failures:** Missing, duplicate, or inconsistent references return closed failures;
unavailable concrete values remain a separate resolution failure outside the set.

**Complexity:** The immediate set is small, but complete use requires a separately
owned resolver and explicit analysis composition changes.

**Maintenance:** Workflow maintains generic reference closure while persistence or
application owners maintain value resolution and consistency with retained history.

**Context-window consequences:** Immediate review is narrow, but delivering a usable
analysis input spans Workflow, persistence or application composition, and analysis.

**Future compatibility:** Any ResultObject family can be referenced without changing
Workflow, provided a downstream resolver and analyzer understand it.

**Advantage:** Preserves the strongest generic Workflow dependency direction and avoids
copying scientific payloads or integration-owned identity values.

**Risk:** A reference-only aggregate is not independently usable as the documented
normalized observation input and expands the current Task into unresolved resolution
and composition work.

## Three-option comparison

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Workflow stores | Exact typed source objects | Workflow-owned copied entries | References only |
| QE import from Workflow | None | None | None |
| Neutral Kohn--Sham import | Yes | Yes | None |
| Exact nominal source identities | Retained directly | Re-expressed as references | Retained indirectly through references |
| Standalone analysis input | Yes | Yes | No |
| New representation duplication | Low | High | Low |
| Additional owner required | No | No | Resolver/application owner |
| Immediate scope | Bounded | Larger public contract | Incomplete vertical slice |

## Recommendation

**Inference:** Option A is the smallest complete vertical slice consistent with the
accepted two-stage architecture. It retains the exact immutable integration result,
uses a calculator-independent Kohn--Sham protocol, avoids a duplicate identity
representation, and produces a directly analyzable Workflow ResultObject without
adding persistence or resolution work.

**Recommendation:** Select Option A. Require the assembler to validate exact fields and
closed correlations at runtime, document protocol immutability as a public contract,
and return a closed failure for unsupported or inconsistent sources.

## Deferred questions

**Deferred question:** Whether a later multi-physics Workflow requires a versioned
union of normalized observation-source protocols.

**Deferred question:** Whether future persistence needs a wire form for normalized sets
or only source ResultObject references.

**Deferred question:** Whether analyzer composition should narrow one protocol member
to a concrete neutral observation family through a dedicated ActionObject.

## Human decision required

Select exactly one:

- `A` — retain exact extracted ResultObjects through a typed Kohn--Sham source protocol;
- `B` — copy sources into Workflow-owned normalized entries with owner-qualified identity references;
- `C` — create a reference-only normalized set and defer concrete value resolution; or
- `D` — reconsider or defer.

**Human decision:** The human response `A` selected Option A on 2026-09-15.
Workflow retains exact extracted ResultObjects through a calculator-independent typed
Kohn--Sham source protocol.

**Acceptance and closeout:** The subsequent human response `acceptance and closeout
authorized` on 2026-09-15 accepts the bounded implementation and authorizes managed
administrative closeout. The accepted assembler retains exact sources, requires a
new output identity distinct from every source identity, validates source and lineage
correlation, and returns closed request-retaining failures without a calculator or
integration import. This acceptance establishes software verification only and does
not authorize dependency changes, protected or scientific execution, numerical
verification, scientific validation, uncertainty quantification, scientific
acceptance, publication, release, or automatic succession.
