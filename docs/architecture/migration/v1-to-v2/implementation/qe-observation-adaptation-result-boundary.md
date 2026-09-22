# QE observation-adaptation result boundary

## Problem

**Human choice:** Select the public result and ownership boundary for deterministic
adaptation from one exact parsed QEXSD document plus admitted Workflow artifact
lineage into the retained neutral plane-wave Kohn--Sham observation contract.

The choice must preserve the existing schema-version-1 neutral aggregate, represent
exact manifest lineage, and avoid moving QE-native meaning into Workflow code.

## Observed current behavior

**Observed fact:**
`ksdft2effmass.integration.quantum_espresso.qexsd.ConstructQexsdKohnShamPlaneWaveRecord`
currently translates `QexsdDocument` into
`KohnShamPlaneWaveCalculationRecord`, including explicit bohr, inverse-bohr, Hartree,
coordinate, reciprocal-scale, unavailable-energy-reference, unavailable-spin-array,
FFT-grid, source-content, producer-version, and process-status fields
(`python/src/ksdft2effmass/integration/quantum_espresso/qexsd/construction.py`).

**Observed fact:** The retained aggregate has no Workflow `ResultObjectIdentity`,
`ArtifactManifestIdentity`, or `ArtifactManifestEntryIdentity`, and its accepted
schema-version-1 serializer remains unchanged pending separately authorized consumer
cutover (`python/src/ksdft2effmass/ksdft/pw/records.py` and
`harness/tasks/migration.v2.ksdft.plane-wave-disposition.json`).

**Observed fact:** Workflow artifacts already retain exact content identity, producer
provenance, run correlation, and explicit lineage in `ArtifactManifest` and
`ArtifactManifestEntry`
(`python/src/ksdft2effmass/workflows/artifacts.py`).

**Observed fact:** The Workflow model says concrete scientific domains own concrete
`ResultObject` implementations, while the artifact architecture describes a
Workflow-owned `NormalizedObservationSet`
(`python/src/ksdft2effmass/workflows/model.py` and
`docs/architecture/v2/ksdft2effmass/workflows/artifact-and-provenance-model.md`).

**Inference:** Current authority fixes the QE-native, neutral-observation, and
Workflow-artifact owners but does not fix whether the adaptation result itself is a
concrete integration result, a generic Workflow result, or a two-stage composition of
both.

## Decision requirements

**Observed fact:** The active Task requires explicit units, references, unavailable
metadata, and lineage while prohibiting fabricated Workflow history, protected
execution, dependency changes, and scientific acceptance
(`harness/tasks/migration.v2.integration.quantumespresso.adaptation.json`).

**Observed fact:** Dependency direction permits QE integration to import accepted
Workflow and neutral contracts; Workflow and neutral packages must not import QE
integration (`docs/architecture/migration/v1-to-v2/package-module-crosswalk.md`).

**Observed fact:** The accepted plane-wave disposition defers a new neutral wire and
requires the schema-version-1 aggregate to remain compatible
(`harness/tasks/migration.v2.ksdft.plane-wave-disposition.json`).

**Human choice:** Decide which owner publishes the new immutable adaptation result and
whether Workflow normalization is one step or a separate second step.

## Option A

**Conceptual model:** Add an integration-owned
`QuantumEspressoObservationAdaptationResult` concrete `ResultObject` containing the
unchanged neutral record, exact source manifest and entry identities, normalization
policy identity/version, and explicit limitations.

**Authority:** The active QE adaptation Task defines only the integration-owned
adapter and result; accepted Workflow manifest and neutral-record contracts remain
unchanged.

**Ownership/dependency:** Integration imports Workflow identities and neutral records;
neither Workflow nor neutral packages import integration.

**Runtime/dispatch:** After confirmed ingress and QEXSD parsing, one integration
ActionObject validates source-content and lineage correlation and returns one
immutable result. It performs no dispatch, persistence, or artifact publication.

**Migration:** Existing `ConstructQexsdKohnShamPlaneWaveRecord` remains available and
unchanged; the new adapter composes it and adds the missing lineage result boundary.

**Reversibility:** The companion result can later be adapted into a Workflow-owned
normalized set without altering the retained neutral record or its wire.

**Failures:** Wrong source content, absent or mismatched manifest membership,
incompatible producer/run lineage, unsupported unit declarations, or neutral-record
construction failure returns a closed integration adaptation failure.

**Complexity:** One result family and one adapter are added in the integration
package.

**Maintenance:** QE-specific correlation remains beside the QEXSD parser and existing
QE execution results.

**Context-window consequences:** Review remains bounded to QE integration, exact
Workflow artifact contracts, the retained neutral record, and focused tests.

**Future compatibility:** A later generic Workflow normalization layer can consume the
concrete result through the existing `ResultObject` protocol.

**Advantage:** Preserves dependency direction and the Workflow model's rule that
concrete scientific domains own concrete results while retaining exact lineage now.

**Risk:** Interprets the architecture phrase “Workflow-owned
`NormalizedObservationSet`” as a later composition rather than this Task's immediate
output.

## Option B

**Conceptual model:** Add a generic Workflow-owned `NormalizedObservationSet` that
directly contains one concrete neutral observation value plus normalization and source
manifest references; the QE adapter returns this generic result.

**Authority:** The active integration Task would also establish a new public Workflow
result contract, or would require a separately activated Workflow Task before
implementation can complete.

**Ownership/dependency:** Integration imports and constructs the Workflow result;
Workflow must represent domain values without importing QE integration or narrowing
the generic contract to Kohn--Sham data.

**Runtime/dispatch:** One adapter validates QEXSD and lineage and directly produces
the generic normalized set after confirmed ingress.

**Migration:** Existing neutral construction is reused, but Workflow gains a new
generic result and public exports immediately.

**Reversibility:** Removing or reshaping the generic result after consumers adopt it
would require a public-API migration.

**Failures:** Generic Workflow failure fields must represent domain-specific unit,
source, and normalization failures without acquiring QE policy.

**Complexity:** One generic result plus the integration adapter, with cross-package
contract design and tests.

**Maintenance:** Workflow owns a stable generic container while each integration owns
normalization policy.

**Context-window consequences:** Review must cover Workflow public API, all potential
result consumers, integration, neutral records, and dependency-direction evidence.

**Future compatibility:** Other calculators could reuse the generic container if its
value boundary is sufficiently typed without erased containers.

**Advantage:** Implements the architecture's named Workflow-owned
`NormalizedObservationSet` in one direct path.

**Risk:** The generic value boundary is not yet specified and may prematurely freeze a
cross-domain public API or move concrete result ownership into Workflow.

## Option C

**Conceptual model:** Split adaptation into an integration-owned extracted-observation
result followed by a separate Workflow-owned normalization assembler and
`NormalizedObservationSet` result.

**Authority:** The integration Task owns the first result; a separately activated
Workflow Task owns the second result and assembler before the complete path can close.

**Ownership/dependency:** Integration depends on neutral and Workflow identity
contracts, while Workflow consumes only an integration-independent normalized-input
protocol or neutral ResultObject.

**Runtime/dispatch:** Confirmed ingress leads to exact extraction and lineage closure;
a second pure Workflow ActionObject then assembles the normalized set. Neither step
performs execution or persistence.

**Migration:** Two explicit records permit staged consumer cutover and preserve the
legacy aggregate unchanged.

**Reversibility:** Either stage can evolve behind its own adapter, but their shared
correlation contract becomes an additional migration surface.

**Failures:** Extraction and normalization failures remain separate, requiring closed
cross-stage identity correlation and no partial normalized result.

**Complexity:** Two result families, two ActionObjects, and an additional protocol or
neutral wrapper are required.

**Maintenance:** Ownership is explicit but the project must maintain a larger public
surface and cross-task lifecycle.

**Context-window consequences:** Review spans integration, Workflow, neutral-result,
protocol, and composition surfaces in separate implementation phases.

**Future compatibility:** The split can support multiple native parsers and generic
normalization policies without forcing them into one ActionObject.

**Advantage:** Most strictly realizes the documented native parser → integration
adapter → Workflow normalized-set sequence with explicit stage separation.

**Risk:** It expands the current vertical slice and requires authority from multiple
Task owners before delivering one usable adaptation result.

## Three-option comparison

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Concrete result owner | QE integration | Workflow | Integration then Workflow |
| Existing contract mutation | None | New Workflow public contract | New integration and Workflow contracts |
| Exact lineage | In companion result | In generic normalized set | In both correlated stages |
| Dependency-direction risk | Low | Medium | Medium |
| Immediate scope | Bounded | Cross-package | Cross-task and staged |
| Legacy wire impact | None | None | None |
| Future generic reuse | Via later adapter | Immediate | Explicit second stage |

## Recommendation

**Inference:** Option A is the smallest complete boundary consistent with the accepted
narrow Kohn--Sham compatibility contract, current dependency direction, and the
Workflow model's statement that concrete scientific domains own concrete ResultObject
implementations. It records exact Workflow manifest lineage without changing the
Workflow artifact model or the retained schema-version-1 neutral wire.

**Recommendation:** Select Option A. Treat a generic Workflow-owned
`NormalizedObservationSet` as deferred cross-domain composition requiring its own
accepted contract and owner rather than freezing it implicitly during this QE-specific
Task.

## Deferred questions

**Deferred question:** Whether multiple calculator-specific adaptation results later
need one generic Workflow normalized-observation aggregate.

**Deferred question:** Whether a future neutral Kohn--Sham record should itself become
a workflow-facing ResultObject with an independent wire version.

**Deferred question:** Exact portable native-output reference representation beyond
the accepted ArtifactManifest fields.

## Human decision required

Select exactly one:

- `A` — integration-owned concrete adaptation ResultObject;
- `B` — directly returned Workflow-owned generic NormalizedObservationSet;
- `C` — two-stage integration extraction and Workflow normalization results; or
- `D` — reconsider or defer.

**Human decision:** The human response `C` selected Option C on 2026-09-15. QE
integration owns the exact extracted-observation result. A separately activated
Workflow Task must own the normalization assembler and Workflow-owned
`NormalizedObservationSet`. The decision does not activate that Workflow stage,
automatic succession, protected execution, or administrative closeout.
