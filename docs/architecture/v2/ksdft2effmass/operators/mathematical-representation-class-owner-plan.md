<!--
Copyright (c) 2026 Eugene Joseph M. Ragasa.
SPDX-License-Identifier: Apache-2.0
Author: Eugene Joseph M. Ragasa
Initial document completed: 2026-10-20
-->

# Mathematical representation class owner plan

## Status and authority boundary

**Status:** The operator selected plural sibling packages
`ksdft2effmass.operators.representations` and
`ksdft2effmass.operators.transformations`, plus first-class
`ksdft2effmass.operators.<concrete_operator>` packages for cohesive mathematical operator
families. The bounded Phase 1 implementation remains an uncommitted review candidate.
Later phases remain proposed and require separate review. This document is not a schema
migration, retained calculation, formal proof, or scientific result.

This plan responds to the verification-side recommendation
`projectkoios-formal/docs/BandGauge/ksdft2effmass/mathematical-representation-class-architecture-plan.md`.
That recommendation was read as an untracked working-tree file at formal-repository HEAD
`26603110e9d64cd51c9101eff68060307f258a18`; its inspected byte digest was
`sha256:4c0141b199078124f75877e215fe05d801e130f2064f0580d8e5a6a52bcf77a8`.
The file is therefore a review input identified by bytes, not an immutable formal-repo
commit or an accepted owner authority.

The general computational-peer boundary is cross-referenced from
`projectkoios-formal/docs/ecosystem-architecture.md#executable-verification-boundary-for-computational-peers`.
The inspected formal-side working snapshot was at the same repository HEAD and had digest
`sha256:68bae28bcc06e2c54ef7c3ed3e324a19188e478930423541b48260525a87e49f`.
That ecosystem file was modified relative to HEAD, so Phase 7 must bind a later committed
immutable revision before using it as a certificate contract.  Its stated boundary is
nevertheless the planning rule here: KSD, PhysKit, Numerics, and Optimization remain
computational peers owning their runtime abstractions; formal executable verification is
a separate certificate/checker lane, not a production superclass relationship.

The source audit uses immutable `ksdft2effmass` objects:

- Papers A and B: `99a46cb59d0c6f27ada7d709f194996ef9619d9f`;
- Paper C and the schema-free higher-rank calculation:
  `8bafdeeb6b0c75bcd7a2984d0c283a8e64fb0fd8`.

Dirty and ignored artifacts in the audited checkouts were excluded from the source
inventory. Phase 1 was moved to a dedicated worktree based on the immutable Paper C
revision; it does not interpret or depend on the unrelated protocol or development
artifacts found in the original checkout.

## Selected owner direction

The selected direction separates intrinsic representation carriers from directed
transformations. `operators.representations` owns finite carriers, represented spaces,
intrinsic node identities, and fields. `operators.transformations` owns transformation
kinds, directed edge identities, and generic transformation contracts, with the strict
one-way dependency `transformations -> representations`. Concrete operator-family
packages own their operator-specific laws, parameters, invariants, construction, and
non-reusable transformations. Nothing is flattened into `ksdft2effmass.operators`.

Generic numerical analyzers remain under `analysis.matrix_field`; model-adequacy
interpretation remains outward under `analysis.model_adequacy`. Paper C would be the first
adapter. Papers A and B would follow only after Paper C demonstrates the boundary without
changing a retained schema.

Approval would authorize only the first implementation checkpoint defined below.  It
would not approve later phases, Paper C's scientific protocol amendment, schema changes,
retained execution, scientific claims, a Lean bridge, a dependency change, commit, push,
merge, release, or publication.

## Objectives

The proposed layer must:

1. make finite domain, state space, basis, rank, coordinate convention, energy reference,
   and representation role explicit;
2. represent compression, gauge action, alignment, Fourier conversion, support
   truncation, and reconstruction as distinct typed transformations;
3. prohibit entrywise comparison before common-space and common-basis identification;
4. keep arrays, mathematical-property evidence, diagnostics, and decisions distinct;
5. extend `operators` with separate generic representation and transformation owners plus
   cohesive concrete operator-family packages, while keeping `analysis.matrix_field`
   numerical diagnostics outward and unduplicated;
6. provide rank- and dimension-generic machinery while leaving paper laws and thresholds
   with their campaign or analysis owner;
7. represent qualified, deficient, nonunique, integrity-rejected, unresolved,
   not-applicable, and cap-exhausted outcomes explicitly;
8. preserve existing public imports and serialized bytes until a separately approved
   migration; and
9. carry sufficient immutable identity for later certificate export without treating a
   Python class or numerical tolerance as a formal proof.

## Non-negotiable ownership constraints

The proposal does not replace these existing owners:

- `ksdft2effmass.operators` continues to own `StateSpace`, `Basis`, `Geometry`,
  `EnergyReference`, `OperatorRecord`, exact represented compatibility, guarded
  differencing, and primitive represented residuals.
- `ksdft2effmass.analysis.matrix_field` continues to own semantic-neutral NumPy matrix-
  field calculations and diagnostics.
- PhysKit and Project Koios Numerics continue to own reusable lattice, finite-periodic,
  mesh, hopping, unit, and array primitives.  In particular, the new layer composes
  `CenteredUniformMesh`; it does not introduce another mesh-size-plus-coordinate API.
- Project Koios Optimization continues to own reusable Procrustes and generic
  optimization mechanics.  KSD owns its admissible alignment family, thresholds,
  evidence, and disposition policy.
- `ksdft2effmass.analysis.model_adequacy` owns KSD-specific normalization, loss-channel,
  admissibility, and finite-decision meaning.
- Campaigns own fixed case inventories, scientific thresholds, lifecycle, schema,
  provenance, and retained-result policy.
- Human scientific acceptance and formal theorem applicability remain outside runtime
  analysis objects.

No new runtime dependency is proposed.  Lean and `projectkoios-formal` remain outside the
owner runtime graph.  This follows the ecosystem-wide executable-verification boundary,
not a KSD-specific exception.  Computational-to-formal conformance is structural at the
certificate boundary; no computational peer inherits production classes from the formal
sidecar.

## Deliberate owner-side refinements of the recommendation

This plan adopts the verification recommendation as a planning input rather than as
accepted architecture.  Its deliberate refinements are explicit:

1. `FiniteMomentumMeshDomain` composes a `CenteredUniformMesh`; construction versus
   shifted evaluation is recorded as role/identity, not as two mesh subclasses.
2. Existing `operators` metadata is reused rather than replaced by another space/basis
   hierarchy.
3. The Paper C scientific target is the separately selected `SO(r)` amendment.  The
   recommendation's global and pointwise `U(r)` strategies remain only as legacy parity
   adapters and are not silently renamed.
4. Nonunique and integrity-rejected alignment outcomes are added so admission can be
   fail-closed.
5. Support-property evidence is split into negation, orbit, metric-shell, and source-range
   records rather than collapsed into one generic closure flag.
6. Projector and frame construction remain in the exact target inventory but are deferred
   pending a separate design of analytic, eigensolver, projection, and Wannier90 routes.
7. Existing paper objects are wrapped first. Inheriting from a new ABC is not required
   where doing so would disturb a frozen public or schema leaf.
8. Intrinsic representations and directed transformations use plural sibling packages.
   A concrete-operator package denotes a cohesive mathematical family, not a runtime
   object, graph node, paper stage, or campaign case.

## Proposed package and dependency layout

```text
python/src/ksdft2effmass/
  operators/
    representations/                # intrinsic carriers and finite representations
      __init__.py                    # documentation only; no flattened exports
      domains.py
      spaces.py
      identities.py
      fields.py
      nodes.py                       # prospective generic node composition
    transformations/                # typed directed edges and reusable operations
      __init__.py                    # documentation only; no flattened exports
      identities.py
      base.py
      <reusable_operation>.py        # prospective, only if cross-family reusable
    hamiltonian/                     # example cohesive concrete operator family
      laws.py
      invariants.py
      construction.py
      transformations.py             # Hamiltonian-specific operations when needed
  periodic/                          # existing periodic-model identities
  analysis/
    matrix_field/                    # semantic-neutral array diagnostics
    model_adequacy/                  # outward KSD loss and decision semantics
  campaigns/                         # case, threshold, provenance, retained policy
```

`hamiltonian/` is illustrative until separately reviewed. A concrete package is never
created per runtime instance, graph node, paper stage, or campaign case.

The dependency direction is:

```text
operators.records / Numerics / PhysKit / Optimization
                        |
                        v
            operators.representations
                        |
                        v
            operators.transformations
                        |
                        v
         operators.<concrete_operator>
                        |
          +-------------+----------------+
          |                              |
          v                              v
analysis.matrix_field          analysis.model_adequacy
                                         |
                                         v
                               campaigns / serializers
```

Forbidden reverse dependencies are:

- `operators.representations` importing `operators.transformations` or any concrete
  operator package;
- `operators.transformations` importing a concrete operator package;
- generic packages importing analysis, campaigns, publications, Workflow, serializers,
  schemas, retained calculations, or formal code;
- campaigns or paper cases being moved into an operator-family package; and
- a DataObject performing filesystem discovery or external execution.

The generic representation package composes existing `OperatorRecord` metadata where
applicable. It does not create competing `StateSpace`, `Basis`, `Geometry`, or
`EnergyReference` classes.

## Exact proposed abstract interfaces

The following is the complete proposed abstract-interface inventory.  No universal
`MathematicalObject` or generic `BaseCalculator` is proposed.

| Owner module | Abstract interface | Stable responsibility |
|---|---|---|
| `representations/domains.py` | `FiniteDomainABC` | immutable domain identity and cardinality |
| `representations/fields.py` | `MatrixFieldABC` | domain-correlated immutable matrix values and dimensions |
| `representations/fields.py` | `SquareMatrixFieldABC` | square-field shape refinement only |
| `representations/fields.py` | `OperatorFieldABC` | intended operator-field role; no inferred Hermiticity |
| `representations/fields.py` | `ProjectorFieldABC` | intended projector-field role; no inferred projector identity |
| `representations/fields.py` | `GaugeFieldABC` | intended coordinate-map role; no inferred unitarity |
| `representations/fields.py` | `RectangularMatrixFieldABC` | rectangular-field shape refinement only |
| `representations/fields.py` | `FrameFieldABC` | intended frame role; no inferred isometry |
| `representations/fields.py` | `FourierBlockFieldABC` | translation-indexed block field |
| `representations/nodes.py` | `OperatorRepresentationABC` | intrinsic node identity plus represented field and evidence references |
| `representations/nodes.py` | `BlochOperatorRepresentationABC` | momentum-domain operator representation |
| `representations/nodes.py` | `CellHoppingRepresentationABC` | translation-domain coefficient representation |
| `transformations/base.py` | `RepresentationTransformationRequestABC` | nominal operation-specific request and enum kind |
| `transformations/base.py` | `RepresentationTransformationResultABC` | nominal operation-specific result and enum kind |
| `transformations/base.py` | `RepresentationTransformationABC[RequestT, ResultT]` | typed request-to-result Action with enum agreement |
| `operators/<concrete_operator>/laws.py` | operator-family law ABC, if needed | family-specific law evaluated on a declared domain |
| outward analysis owner | `ParameterPathABC` | declared parameter path and coordinate semantics |
| outward analysis owner | `ParameterizedRepresentationFamilyABC` | graph evaluated at one declared parameter value |
| reviewed reusable transformation module | `AlignmentStrategyABC` | one declared admissible alignment family |
| reviewed support owner | `SupportABC` | one primary finite-support semantic class |
| `analysis.model_adequacy` | `ErrorMeasureABC` | explicit representation-comparison specification |
| `analysis.model_adequacy` | finite decision ABCs | threshold, first-pass, and Pareto policy |

`MetricGeometry` remains a narrow structural `Protocol` under its existing owner.  It is
not converted into an abstract base solely for uniformity.

## Exact proposed concrete leaf inventory

All concrete value and result classes below are proposed as frozen, slotted, final
DataObjects unless explicitly identified as an ActionObject.  Array leaves defensively
own immutable validated NumPy arrays and do not subclass `numpy.ndarray`.

### Domains, spaces, and identities

| Owner module | Concrete leaf | Meaning |
|---|---|---|
| `representations/domains.py` | `MomentumSampleRole` | enum with `general`, `construction`, and `evaluation` members |
| `representations/domains.py` | `FiniteMomentumMeshDomain` | composed centered mesh, coordinate convention, sample role, and identity |
| `representations/domains.py` | `FiniteTranslationDomain` | ordered unique finite translation inventory |
| `representations/spaces.py` | `RepresentationSpaceIdentity` | state-space, basis, geometry, energy-reference, scalar-field, and coordinate identities |
| `representations/identities.py` | `BlochSpaceRole` | Bloch-space enum with `ambient` and `retained` members |
| `representations/identities.py` | `CellHoppingRepresentationRole` | complete-inventory or support-truncated enum |
| `representations/identities.py` | `RepresentationIdentity` | intrinsic domain, space, role, and source-artifact identity |
| `representations/identities.py` | `RepresentationIdentityFactory` | carrier-specific node-identity construction |
| `transformations/identities.py` | `RepresentationTransformationKind` | directed edge-kind enum |
| `transformations/identities.py` | `TransformationIdentity` | kind, method, orientation, and full source/target identities |
| `transformations/identities.py` | `TransformationIdentityFactory` | identity-only edge construction |

Construction and evaluation are sample roles, not subclasses of mesh.  A shifted
evaluation mesh is another `FiniteMomentumMeshDomain` whose composed
`CenteredUniformMesh` has the selected offset.  This avoids parallel mesh-size and
coordinate inputs and avoids encoding campaign role into mesh inheritance.

### NumPy-backed fields

| Owner module | Concrete leaf | Implements |
|---|---|---|
| `representations/fields.py` | `NumpyOperatorField` | `OperatorFieldABC` |
| `representations/fields.py` | `NumpyProjectorField` | `ProjectorFieldABC` |
| `representations/fields.py` | `NumpyGaugeField` | `GaugeFieldABC` |
| `representations/fields.py` | `NumpyFrameField` | `FrameFieldABC` |
| `representations/fields.py` | `NumpyFourierBlockField` | `FourierBlockFieldABC` |

These types assert role, domain correlation, dtype, immutability, and shape only.
Hermiticity, idempotency, unitarity, isometry, periodicity, and sewing remain evidence.

### Analytic laws and parameterized families

| Owner | Concrete leaf | Meaning |
|---|---|---|
| reviewed concrete operator-family package | `AxisSymmetricFourStateParentLawAdapter` | adapter around Paper A/B's analytic parent law |
| reviewed concrete operator-family package | `SeparableSineRotationGaugeLawAdapter` | adapter around Paper A/B's gauge law |
| reviewed concrete operator-family package | `HigherRankConstantProjectorParentLaw` | Paper C parent formula, without campaign policy |
| reviewed concrete operator-family package | `RealGivensCircuitGaugeLaw` | Paper C real Givens formula, without alignment policy |
| outward parameter-path owner | `BainPathAdapter` | Paper B continuous unit-volume Bain path adapter |
| outward parameter-path owner | `DeclaredFiniteParameterPath` | immutable ordered parameter inventory |
| outward family-analysis owner | `PaperBStrainRepresentationFamilyAdapter` | evaluates ordinary nodes and edges at one parameter |

A law returns field values for a supplied domain; it does not own the mesh, evidence,
transformation graph, or campaign.  A parameterized family returns ordinary
representation nodes and edges.  Strain envelopes, extrema, and transition brackets are
analysis results over the path, not new representation subclasses.

### Representation nodes

| Owner module | Concrete leaf | Representation role |
|---|---|---|
| `representations/nodes.py` | `BlochOperatorRepresentation` | momentum-domain node using an ambient or retained role |
| `representations/nodes.py` | `CellHoppingRepresentation` | translation-domain coefficient node using a complete or truncated inventory role |

Gauge-conjugated, aligned, Fourier-converted, support-truncated, and reconstructed status
is derivation history carried by typed transformation edges. It is not encoded through
exclusive stage subclasses. In particular, a reconstructed target remains a Bloch node
with its applicable space role, while its incoming edge uses
`RepresentationTransformationKind.fourier_reconstruction`. Frame compression
`F^\dagger H F` is distinct from projector construction `P=F F^\dagger` and from
restriction to an invariant subspace.

### Evidence leaves

| Owner | Concrete leaf |
|---|---|
| outward property-evidence owner | `HermiticityEvidence` |
| outward property-evidence owner | `IsometryEvidence` |
| outward property-evidence owner | `UnitarityEvidence` |
| outward property-evidence owner | `ProjectorEvidence` |
| outward property-evidence owner | `ConstantRankEvidence` |
| outward property-evidence owner | `PeriodicityEvidence` |
| outward property-evidence owner | `SewingEvidence` |
| outward property-evidence owner | `CoverageEvidence` |
| outward support-evidence owner | `NegationClosureEvidence` |
| outward support-evidence owner | `CompleteOrbitEvidence` |
| outward support-evidence owner | `MetricShellCompletenessEvidence` |
| outward support-evidence owner | `SourceRangeBinding` |
| outward transformation-evidence owner | `TransformationIdentityEvidence` |

Every evidence leaf includes subject identity, stage identity, finite domain, method,
exact certificate or tolerance convention, disposition, and retained bound or failure
location as applicable.  `EvidenceMode` is a `StrEnum` with exactly:

- `analytic-identity-declared`;
- `checked-exact-certificate`;
- `checked-outward-interval-certificate`;
- `numerical-diagnostic`;
- `unresolved`; and
- `not-applicable`.

`EvidenceDisposition` is separate from `EvidenceMode`; mode states what kind of evidence
was evaluated, while disposition states whether its declared requirement passed, failed,
was unresolved, or was inapplicable.  No class name promotes numerical evidence to proof.

### Transformation ActionObjects and results

| Prospective owner | ActionObject | Request | Result |
|---|---|---|---|
| concrete Hamiltonian family | `SpectralProjectorConstruction` | `SpectralProjectorConstructionRequest` | `SpectralProjectorConstructionResult` |
| concrete Hamiltonian family | `FrameConstruction` | `FrameConstructionRequest` | `FrameConstructionResult` |
| reusable transformation module | `FrameCompression` | `FrameCompressionRequest` | `FrameCompressionResult` |
| reusable transformation module | `GaugeConjugation` | `GaugeConjugationRequest` | `GaugeConjugationResult` |
| reviewed reusable or concrete owner | `AlignmentTransformation` | `AlignmentTransformationRequest` | `AlignmentTransformationResult` |
| reusable transformation module | `FiniteFourierConversion` | `FiniteFourierConversionRequest` | `FiniteFourierConversionResult` |
| reusable transformation module | `SupportTruncation` | `SupportTruncationRequest` | `SupportTruncationResult` |
| reusable transformation module | `FourierReconstruction` | `FourierReconstructionRequest` | `FourierReconstructionResult` |

Each ActionObject accepts one nominal request and returns one nominal result. Request,
Action, result, and emitted `TransformationIdentity` use the same explicit
`RepresentationTransformationKind` member. The enum is a computational discriminator, not a wire token or universal factory key.
Each concrete Action implements the selected abstract public `transform(request, /) ->
result` contract and must reject mismatched nominal request or result kinds. Shared
protected validators support that fail-closed behavior. Kind agreement does not establish
correctness or evidence.

A result contains source/target identities, the target representation, method identity,
orientation or sign convention, supplied witness/support, and applicable evidence. A
one-field wrapper is prohibited; the result exists because the transformation edge and
its evidence are additional semantic outputs.

`SpectralProjectorConstruction` and `FrameConstruction` are in the exact target inventory
but their implementation is deliberately deferred beyond the numbered phases below.  The
current papers use materially different analytic, eigensolver, projection, and Wannier90
routes; their request and result payloads require a separate bounded design review before
source creation.

### Alignment strategies and results

| Prospective owner | Concrete strategy | Role |
|---|---|---|
| reviewed reusable transformation module | `IdentityAlignment` | no corrective alignment |
| reviewed reusable or concrete owner | `GlobalRealRotationAlignment` | Paper A's declared real-rotation family |
| reviewed reusable or concrete owner | `GlobalSpecialOrthogonalProcrustesAlignment` | Paper C global `SO(r)` Kabsch family |
| reviewed reusable or concrete owner | `PointwiseSpecialOrthogonalProcrustesAlignment` | Paper C pointwise `SO(r)` Kabsch family |
| reviewed reusable transformation module | `ParallelTransportAlignment` | ordered reciprocal-path transport |
| concrete operator-family package | `SuppliedAnalyticInverseGaugeAlignment` | supplied construction control |
| Paper C compatibility adapter | `LegacyGlobalUnitaryProcrustesAlignment` | committed development parity only |
| Paper C compatibility adapter | `LegacyPointwiseUnitaryProcrustesAlignment` | committed development parity only |

`AlignmentSelectionRequest` is the common nominal request.  The target union
`AlignmentSelectionResult` contains exactly:

- `QualifiedAlignmentSelection`;
- `RankDeficientAlignmentSelection`;
- `NonuniqueAlignmentSelection`;
- `IntegrityRejectedAlignmentSelection`;
- `NumericallyUnresolvedAlignmentSelection`; and
- `NotApplicableAlignmentSelection`.

Only `QualifiedAlignmentSelection` contains an applicable transformation.  Every other
variant omits transformation and downstream-alignment payloads.  Special-orthogonal
strategies require orthogonality, realness, determinant `+1`, objective identity,
stationarity, rank, and uniqueness evidence before qualification.  The determinant-
corrected branch requires an explicit smallest-singular-value degeneracy policy.

The two legacy unitary strategies are temporary parity tools and are not proposed Paper C
scientific channels.  Their removal requires completion of the Paper C protocol
amendment and parity audit.

### Supports and support costs

| Prospective owner | Concrete leaf | Primary semantic class |
|---|---|---|
| reviewed support owner | `ArbitraryFiniteSupport` | declared finite translation set |
| reviewed support owner | `NegationClosedSupport` | support whose primary contract is inversion closure |
| reviewed support owner | `CompleteMetricShellSupport` | complete equal-radius metric shells |
| concrete operator-family package | `SourceHoppingRangeSupport` | support bound to an exact source range |
| reviewed support owner | `SupportLadder` | ordered finite inventory of one support type |
| outward model-adequacy owner | `SupportCost` | block count, physical radius, and shell index |

A support has one primary concrete class.  Additional negation, orbit, shell, or source-
range properties are composed as evidence rather than represented by multiple
inheritance.  Paper C periodic-1D symmetric ranges use `NegationClosedSupport`; Paper B
metric-shell families use `CompleteMetricShellSupport`.

### Error and finite-decision leaves

| Owner | Concrete leaf | Role |
|---|---|---|
| `analysis.model_adequacy` | `FrobeniusErrorMeasure` | raw or declared normalized matrix Frobenius error |
| `analysis.model_adequacy` | `OperatorNormErrorMeasure` | operator norm error and perturbation input |
| `analysis.model_adequacy` | `OrderedSpectrumErrorMeasure` | ordered multiset eigenvalue comparison |
| `analysis.model_adequacy` | `WeightedFrobeniusLossMeasure` | explicitly weighted and normalized loss |
| `analysis.model_adequacy` | `RepresentationErrorResult` | identities plus one matrix-field diagnostic result |
| `analysis.model_adequacy` | `OrderedSpectrumErrorResult` | identities plus one spectrum diagnostic result |
| compatibility adapter | `LegacyErrorChannelsAdapter` | read-only legacy Paper A/B channel meanings |
| compatibility adapter | `LegacyFirstPassingDecisionAdapter` | read-only legacy decision projection |
| `analysis.model_adequacy` | `FiniteObjectivePoint` | attained objective vector and witness identity |
| `analysis.model_adequacy` | `ThresholdDecisionResult` | threshold result with interval-aware disposition |
| `analysis.model_adequacy` | `EarlierCutoffAuditEntry` | one earlier cutoff evaluation |
| `analysis.model_adequacy` | `FirstPassAudit` | candidate plus all required earlier results |
| `analysis.model_adequacy` | `JointThresholdDecisionResult` | all channels for one identical witness |
| `analysis.model_adequacy` | `ParetoAssessment` | attained points and checked dominance mask |
| `analysis.model_adequacy` | `MinimumFeasibleCostResult` | least feasible cost or cap-exhausted outcome |

Rank-normalized Frobenius error remains a descriptive channel.  It is not used as a
general eigenvalue perturbation bound.  General perturbation certificates use operator
norm or rank-unnormalized Frobenius norm unless a separate structural proof applies.

### Aggregate result

A future `CaseRepresentationBundle` containing both nodes and edges must live on the
transformation or outward composition side; it must not force representations to import
transformations. No module is selected in Phase 1. The bundle is not a campaign result,
ledger, Workflow result, serializer payload, or scientific acceptance record. Its
constructor must require graph closure under identical endpoint identities.

No immutable tuple snapshot is named a ledger. Append-only execution journals, if later
required, are infrastructure and remain outside immutable result objects.

## Paper A--C migration crosswalk

Paper labels below mean Ragasa2026A, Ragasa2026B, and Ragasa2026C.  Migration changes
software representation only unless a row explicitly identifies a separately approved
scientific correction.

### Paper A

| Current object | Proposed target | Compatibility rule |
|---|---|---|
| `AxisSymmetricFourStateParent` | paper-owned analytic law producing `AmbientBlochRepresentation` | preserve formulas and results; do not make the law a representation subclass |
| `SeparableSineRotation` | paper-owned gauge law producing `NumpyGaugeField` | preserve phase/orientation conventions |
| `FrameTransportDiagnostic` | adapter to `ParallelTransportAlignment` result and evidence | retain legacy public record and schema bytes |
| `restricted_alignment` | `GlobalRealRotationAlignment` strategy | preserve the frozen admissible angle family |
| `PointDiagnostic` | campaign aggregate referencing common representations, errors, and decisions | no direct schema replacement in initial phases |
| `ErrorChannels` | explicit `LegacyErrorChannelsAdapter` | preserve old field meaning; never reinterpret normalized Frobenius as operator norm |
| `FirstPassingDecision` | legacy adapter; new work uses `FirstPassAudit` | old schema remains unchanged; corrected semantics require a new schema |
| `Periodic1DMultibandAlignmentCalculationDefinition` | unchanged campaign input with an internal graph adapter | preserve validation and public import |
| `Periodic1DMultibandAlignmentCalculator` | thin composition over adapted representation Actions | preserve numerical route during migration |
| `Periodic1DMultibandAlignmentDiagnostics`, `Periodic1DMultibandAlignmentRangeResult`, and `Periodic1DMultibandAlignmentCalculationResult` | legacy outer results with internal common-value adapters | preserve schema `ksdft2effmass.periodic1d.multiband-alignment-calculation-result.v1` |
| `Periodic1DMultibandAlignmentResultJsonSerializer` and `Periodic1DMultibandAlignmentResultVerifier` | unchanged schema boundary and independent verifier | preserve canonical bytes and verifier independence |
| `Periodic1DConstrainedAdmissibleSetCalculationDefinition` | unchanged M3 campaign input | preserve validation and public import |
| `Periodic1DConstrainedAdmissibleSetCalculator` | model-adequacy composition consuming adapted M2/common representations | preserve legacy result until a new schema is approved |
| `Periodic1DConstrainedAdmissibleSetCalculationResult` | legacy outer result | preserve schema `ksdft2effmass.periodic1d.constrained-admissible-set-result.v1` |
| `Periodic1DConstrainedAdmissibleSetResultJsonSerializer` and `Periodic1DConstrainedAdmissibleSetResultVerifier` | unchanged schema boundary and independent verifier | preserve canonical bytes and verifier independence |

### Paper B

| Current object | Proposed target | Compatibility rule |
|---|---|---|
| `BandEquivalenceLocalityCase` | thin composition of geometry, parent-law, gauge, normalization, and sample-role specifications | do not turn a campaign configuration into a representation |
| `MetricGeometry` | retain existing narrow `Protocol` | no nominal superclass required |
| `SignedPermutationShellInventoryDefinition` | paper-owned support-ladder configuration | PhysKit remains lattice owner |
| `SignedPermutationShell` | adapter to `CompleteMetricShellSupport` | preserve complete equal-radius ties and deterministic ordering |
| `SignedPermutationShellInventory` | adapter to `SupportLadder` | retain shell inventory identity |
| `SignedPermutationShellInventoryBuilder` | paper-owned Action returning common support leaves | do not introduce a generic builder until another owner needs the same construction |
| `BainPath` and `BainPathPoint` | `BainPathAdapter` and path-evaluation value | preserve continuous unit-volume path semantics |
| `ShellScaleDecisionPoint` | `FiniteObjectivePoint` adapter | preserve sampled-point identity; no continuum-surface claim |
| `ShellScaleCaseDecisionLandscape` | finite objective inventory plus `ParetoAssessment` | plotting triangulation remains non-authoritative |
| strain definition/response/scan records | parameter-path analyses over ordinary representation graphs | no strain object becomes an operator representation |
| `ErrorChannels` and `FirstPassingDecision` consumers | legacy adapters followed by new-version results | semantic correction cannot use an old schema identity |

Existing Paper B schema documents under
`campaigns/model_adequacy/band_equivalence_locality/schema_documents/` remain unchanged
through the representation migration.  A corrected first-pass or error meaning requires
new schema identities and an explicit old-to-new crosswalk.

### Paper C

| Current object | Proposed target | Compatibility rule |
|---|---|---|
| `HigherRankD1SampledFields` | `CaseRepresentationBundle` containing separate nodes and edges | legacy object remains the numerical characterization source until replacement |
| `HigherRankD1ModelConstructor` | paper-owned analytic parent/gauge pipeline returning common nodes | mesh input becomes `FiniteMomentumMeshDomain` composed from `CenteredUniformMesh` |
| raw A0--A3 strings | descriptive alignment strategy identities | A0--A3 retained only inside legacy parity adapters; no frozen Paper C schema requires aliases |
| A1/A2 selection variants | common `AlignmentSelectionResult` variants | add nonunique and integrity-rejected outcomes; only qualified contains a transform |
| `analysis.matrix_field.diagnostics` results | retained numerical kernels wrapped by semantic identities | preferred shared arithmetic; do not duplicate calculations |
| `HigherRankD1FourierDiagnostics` | `FiniteFourierConversionResult` plus evidence | preserve numerical values during graph migration |
| `HigherRankD1SupportDiagnostics` | support, truncation, reconstruction, error, and evidence composition | do not replace this with a support “calculator” or immutable “ledger” |
| `HigherRankD1ParetoPoint` | `FiniteObjectivePoint` | preserve separate alignment-family feasible sets |
| `HigherRankD1ScalarLedgerEntry` | eliminate generic string-key transport in favor of typed evidence/result fields | no new universal scalar record is proposed |
| `HigherRankD1ScalarLedger` | rename/replace as immutable diagnostic collection during Paper C result redesign | no append-only semantics are inferred from a tuple |
| monolithic case calculator | thin campaign composition over common Actions | no internal object is named Workflow or Task |

A session-level operator direction selected an in-place pre-execution amendment from
unitary alignment to special-orthogonal alignment for Paper C.  That direction is not yet
a source-level protocol amendment.  Architecture migration must not silently relabel the
legacy unitary calculation.  It must first record the scientific amendment, including
determinant-corrected Kabsch orientation, determinant and realness checks, uniqueness,
degeneracy, and fail-closed integrity policy.  Legacy unitary adapters are used only to
separate representation-graph parity from the changed scientific alignment family.

## Schema and serialization compatibility

### General rules

1. No schema changes occur in phases 1--4.
2. Existing serializers continue to serialize existing concrete records, not ABCs.
3. Abstract-interface names and Python `__module__` values never become wire
   discriminators.
4. Exact discriminator and version checks remain at serialization boundaries.
5. Internal substitutability uses the abstract contract; serializer acceptance remains
   an explicit tagged-union policy.
6. Existing schema bytes, canonical JSON bytes, digests, and verifier reconstruction
   routes are preserved.
7. A semantic correction receives a new schema identity; it is never hidden behind an
   old field name or version.
8. Historical evidence and manifests are never rewritten.

### Family-specific disposition

| Family | Current wire boundary | Proposed treatment |
|---|---|---|
| Paper A M2 | `...multiband-alignment-calculation-result.v1` | byte-preserving adapter only |
| Paper A M3 | `...constrained-admissible-set-result.v1` | byte-preserving adapter only |
| Paper A smooth continuum | three `smooth-continuum.*.v1` schemas | unchanged; common graph remains internal |
| Paper B maintained campaign schemas | files under `campaigns/model_adequacy/.../schema_documents/` | unchanged until separately reviewed version proposal |
| Paper C schema-free development result | no frozen schema | complete typed semantics and independent verifier before first schema; no compatibility alias required |
| shared representation graph | no wire format in initial phases | in-memory only |
| future formal certificate export | absent | separate optional versioned schema after computational schemas stabilize |

A new Paper A/B schema proposal must include explicit adapters for legacy
`ErrorChannels` and `FirstPassingDecision`, correct first-pass audit coverage, and a
field-by-field semantic comparison.  Passing numerical parity alone is insufficient if
meaning changed.

## Implementation phases and bounded file sets

### Phase 0 — plan and source-selection decisions

Deliverables are this plan, operator decisions, the Paper C statement-selection note,
and the proposed Paper C companion implementation/evidence contract.  No production
Python or schema changes occur.

Proposed companion path, subject to separate approval:

`experiments/periodic-reduction/higher-rank-composite-band-alignment-and-locality/implementation-and-evidence-contract.md`

### Phase 1 — representations and nominal transformation contracts

Bounded source files:

- `operators/representations/__init__.py`;
- `operators/representations/domains.py`;
- `operators/representations/spaces.py`;
- `operators/representations/identities.py`;
- `operators/representations/fields.py`;
- `operators/transformations/__init__.py`;
- `operators/transformations/identities.py`; and
- `operators/transformations/base.py`.

The strict dependency is `transformations -> representations`. No singular compatibility
package or root re-export is added.

Bounded tests:

- domain and mesh correlation;
- space/basis/rank mismatch;
- immutable array ownership;
- exact type and Boolean/string rejection; and
- import/dependency-boundary tests.

No campaign, result, serializer, schema, manuscript, protocol, or external dependency
changes are included.

### Phase 2 — representation nodes and reviewed transformation operations

After Phase 1 review, add `operators/representations/nodes.py` and only the generic
transformation modules proven reusable across operator families. Select the first
concrete operator-family package in a separate bounded review before moving any law or
operator-specific construction. Do not mass-move committed flat modules.

Demonstrate graph closure on one Paper C rank-3/depth-1 case using the committed
calculator's unitary output as a characterization source. The named legacy alignment
strategy is added in Phase 3. This validates representation plumbing only; it does not
validate or select the amended `SO(r)` science.

### Phase 3 — evidence, alignment, support, and error semantics

Place reusable transformation mechanics under reviewed transformation modules and
operator-specific mechanics with the selected concrete operator family. Keep evidence,
loss interpretation, and finite decisions in their outward scientific owners rather than
pulling them into generic packages. `analysis.model_adequacy` adapters consume both
representation identities and existing `analysis.matrix_field` results without
duplicating arithmetic. Add direct-formula numerical tests for transformation orientation
and the special-orthogonal Kabsch branches.

### Phase 4 — Paper C scientific and case migration

Prerequisites:

1. approved Paper C in-place protocol amendment to `SO(r)` alignment;
2. approved implementation/evidence companion contract;
3. explicit Kabsch uniqueness and degeneracy rule;
4. fail-closed alignment and mandatory-gate inventory; and
5. characterization of legacy unitary outputs separately from new `SO(r)` outputs.

Then migrate one complete Paper C case, require an independent direct-formula
reconstruction, and only afterward migrate the 16-case development composition.  Do not
freeze a schema or execute retained evidence in this phase.

### Phase 5 — finite decisions and Paper A/B adapters

Add finite decisions and parameter families under their outward analysis owners; add
Paper A/B laws only to a separately approved cohesive concrete operator-family package;
and introduce remaining adapters without changing old public imports or wire bytes.  Verify legacy numerical agreement where semantics are unchanged.  Where
first-pass or error semantics change, produce a schema proposal rather than mutating old
records.

### Phase 6 — schema-version proposals

After typed results and independent verifiers are complete, propose new tagged schemas
for corrected Paper A/B semantics and the first Paper C retained contract.  Review
codecs, unknown-field rejection, unavailable-payload omission, canonical bytes,
corruption tests, and old/new compatibility before implementation.

### Phase 7 — optional certificate export boundary

Only after computational schema freeze, propose an optional owner-side export adapter
that binds exact source identity, mesh, support, weights, alignment witness, objectives,
intervals, and theorem-premise identities into canonical certificate bytes.  The formal
side may provide the versioned machine-readable contract, exact or outward-interval Lean
data, parser, fail-closed checker, soundness theorem, conformance fixtures, and invocation
documentation.  KSD retains ownership of the adapter from native records.  A development
or publication-verification job may pin an immutable formal revision and invoke the
checker offline.

No formal-side Python ABC is part of this phase.  If a shared runtime ABC ever becomes
necessary across computational peers, it requires a separately governed neutral package
and an explicit ecosystem ownership and dependency decision.  This is evidence
interchange, not a production import, runtime Lean dependency, automatic proof claim, or
scientific-acceptance result.

## Validation and regression strategy

Every implemented phase must run the cheapest affected checks first, followed by the
broader checks appropriate to its boundary.  Required validation is:

1. constructor tests for domain, space, basis, rank, role, unit, energy-reference, and
   representation identity mismatches;
2. rejection of comparison before a common-basis or alignment map exists;
3. frame-compression and gauge-conjugation orientation against direct formulas;
4. qualified, rank-deficient, nonunique, integrity-rejected, unresolved, and
   not-applicable alignment fixtures;
5. `SO(r)` orthogonality, realness, determinant, Kabsch objective, rank, and degeneracy
   fixtures;
6. primary support-class exclusivity and separate closure evidence;
7. separate block-count, physical-radius, and shell-index costs;
8. complete Fourier conversion, support truncation, reconstruction, Parseval, and error-
   decomposition checks;
9. the normalized-Frobenius perturbation counterexample
   `A = diag(1, 0), B = 0`;
10. nonmonotone pass sequences requiring every earlier cutoff to be retained;
11. rejection of a joint decision formed from channel passes with different witnesses;
12. interval-overlapping threshold comparisons returning unresolved;
13. finite Pareto masks containing only attained objective vectors;
14. legacy-to-new numerical parity where semantics are unchanged;
15. explicit non-parity tests where Paper C changes from `U(r)` to `SO(r)`;
16. rejection of semantic changes under an old schema identity;
17. parameter-path endpoint, ordering, coordinate, and ordinary-representation return
    contracts;
18. independent-verifier reconstruction without importing producer aggregate Actions;
19. static import-boundary checks preventing inward or campaign dependencies;
20. strict mypy over source and affected tests;
21. Ruff check and format verification;
22. focused software- and numerical-verification tests;
23. full Python test suite after each paper migration;
24. package build and installed-wheel import smoke tests for any public import change; and
25. Sphinx build with warnings as errors when public API documentation changes.

Passing these checks establishes only the stated software or bounded numerical behavior.
It does not establish formal proof, scientific validation, uncertainty quantification,
material relevance, or publication acceptance.

## Unresolved choices for operator approval

### Choice 1 — package taxonomy (resolved)

The operator selected plural sibling `operators.representations` and
`operators.transformations` packages with the one-way dependency
`transformations -> representations`. Cohesive concrete operator families use
`operators.<concrete_operator>` and may consume both generic siblings. The generic
siblings never import a concrete family. Generic diagnostics remain under
`analysis.matrix_field`; KSD-specific losses and decisions remain under
`analysis.model_adequacy`.

### Choice 2 — first migration target

- **Paper C first, recommended:** no frozen Paper C schema and newer generic diagnostics;
- Papers A/B first: stronger retained compatibility pressure and legacy semantic debt.

### Choice 3 — initial public status

- **Selected:** direct imports from defining modules such as
  `ksdft2effmass.operators.representations.domains` and
  `ksdft2effmass.operators.transformations.base`; keep both sibling initializers and
  `ksdft2effmass.operators` free of flattened re-exports;
- rejected for Phase 1: immediate package-root or operators-root export.

### Choice 4 — identity persistence

- **Explicit stable identity fields, recommended:** campaign supplies stable identifiers;
- content-derived identity digest.

Content digests remain useful provenance but should not replace semantic identity because
numerically equivalent arrays can have distinct parentage and conventions.

### Choice 5 — Paper C alignment compatibility

- **Recommended:** legacy `U(r)` strategies only for characterization, amended `SO(r)`
  strategies for new scientific results;
- retain both as active Paper C scientific families.

The second option would broaden the protocol rather than implement the selected in-place
amendment.

### Choice 6 — schema timing

- **Recommended:** no shared representation schema and no Paper C schema until typed
  semantics plus independent reconstruction are complete;
- freeze an early graph schema and migrate it later.

### Choice 7 — evidence record factorization

- **Recommended:** distinct final evidence records sharing narrow validation functions;
- one generic evidence record with a property-kind discriminator.

Distinct records preserve property-specific payloads without `Any`, optional-field
matrices, or reflective tables.

### Choice 8 — ecosystem executable-verification boundary

The ecosystem rule applies uniformly to KSD, PhysKit, Numerics, and Optimization:

- **Option A, recommended and consistent with the current ecosystem rule:**
  `projectkoios-formal` supplies a versioned machine-readable certificate contract,
  parser/checker, soundness result, and frozen conformance fixtures.  KSD owns an optional
  export adapter that emits canonical certificate bytes and binds contract version and
  immutable revision identities.  Conformance and checker invocation occur in an offline
  verification lane without subclassing a formal-side Python class.
- **Option B, future ecosystem decision only:** if multiple computational peers establish
  a genuine runtime need for one ABC, place it in a separately governed neutral package
  after explicit ownership, dependency, release, and compatibility review.  It must not
  be introduced merely as a facade for the formal repository and does not establish Lean
  theorem applicability.
- **Option C, excluded under the current ecosystem rule:** KSD or another computational
  peer inherits production runtime classes from `projectkoios-formal`.

Option A preserves the horizontal-sidecar relationship, avoids cross-repository circular
or transitive runtime coupling, and keeps executable verification fail-closed at an
explicit certificate boundary.  Option B is not part of this plan and would require a
new ecosystem architecture decision.  Option C would turn the formal sidecar into a
runtime compatibility layer while still proving nothing about an arbitrary Python
instance.

## Explicit exclusions

This plan excludes:

- production Quantum ESPRESSO or Wannier90 execution;
- remote, cluster, cloud, GPU, scheduler, or network computation;
- D2/D3 campaign implementation or execution;
- moving-projector, complex-gauge, topological, SOC, or material extensions;
- a `tau_E`/`tau_O` minimum-cost decision layer for current Paper C v1;
- changing the Paper C scientific protocol without its separate amendment review;
- changing any existing schema, serializer, wire bytes, digest, or retained manifest;
- rewriting historical evidence or Git history;
- adding, replacing, repinning, or relicensing a dependency;
- runtime or build-time Lean dependency;
- production runtime inheritance by KSD, PhysKit, Numerics, or Optimization from a
  `projectkoios-formal` Python base class;
- a shared computational-peer runtime ABC unless a separately governed neutral package
  and explicit ecosystem ownership/dependency decision are approved;
- representing numerical tolerance evidence as a formal proof;
- generic optimizer, mutable registry, service locator, reflective type table, or
  universal mathematical-object superclass;
- Workflow or Task classes for in-process matrix, alignment, Fourier, support,
  refinement, or decision actions;
- commit, push, merge, release, publication, tag, DOI, or evidence promotion.

## First proposed implementation checkpoint

If the operator approves the recommended choices, the first implementation checkpoint is
**Phase 1 only**:

- create the eight bounded source modules listed in Phase 1;
- add their focused constructor, immutability, mismatch, and dependency tests;
- add no root re-export;
- touch no Paper A/B/C production class;
- touch no schema, serializer, verifier, experiment protocol, manuscript, or retained
  result; and
- report the exact diff and verification results before requesting approval for Phase 2.

## Recorded checkpoint and next approval

The owner selection and Phase 1 authorization are recorded below. Remaining target items
must be reviewed before Phase 2:

1. use the selected plural sibling representation/transformation owners and strict
   `transformations -> representations` dependency without flattened exports or a
   compatibility facade;
2. reuse existing `operators` metadata and external mesh/lattice owners rather than
   duplicate them;
3. adopt the implemented nominal Phase 1 ABCs and treat every later concrete leaf and
   concrete-operator package as subject to phase-specific review;
4. migrate Paper C first while preserving legacy unitary behavior only as a parity
   adapter;
5. keep the initial package internal to its direct import path;
6. make no schema change through Phase 4;
7. use distinct property-specific evidence records;
8. apply the ecosystem executable-verification rule: machine-readable certificate plus
   owner-side export adapter and offline checker lane, no formal-side production ABC, and
   no shared peer ABC absent a separately governed neutral-package decision;
9. reserve the proposed Paper C companion path for a separately approved planning
   document; and
10. record the bounded Phase 1 implementation candidate produced after a clean-base
    re-audit; do not begin Phase 2 until its API and ownership are reviewed.

The recorded authorization does not authorize a commit or push. If any remaining target
item is rejected, revise this plan before its production implementation. Later proposed
classes remain unsupported until their phase-specific checkpoint is approved.
