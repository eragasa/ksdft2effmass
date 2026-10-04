# Current-to-target periodic class crosswalk

## Status and inventory identity

- **Status:** Active migration inventory
- **Inspected base:** `94f5330b6fa3ebefa0f78183aa5d9df1af9d1f70`
- **Target architecture:** [`index.md`](index.md)
- **Retirement rule:** [Archive and retirement](#archive-and-retirement)

This record classifies current periodic types by represented meaning rather than by
historical package or class name. It is a source-migration map. It does not change a
scientific definition, authorize a calculation, establish validation, or make a
proposed target API public.

The inventory covers boundary-defining types under:

- `ksdft2effmass.periodic`;
- `ksdft2effmass.analysis.model_systems.periodic_1d`;
- `ksdft2effmass.analysis.model_systems.periodic2d`;
- `ksdft2effmass.campaigns.periodic_1d`;
- `ksdft2effmass.periodic2d`;
- applicable records in `ksdft2effmass.analysis.periodic_bands`,
  `ksdft2effmass.operators`, and `ksdft2effmass.solid_state`.

A type is boundary-defining here when it names a model, retention selection or space,
operator or representation, encoded campaign document, campaign definition, campaign
execution envelope, or aggregate result that currently combines those meanings.
Mechanical serializers, decoders, verifiers, correlators, numerical analyzers, issue
enums, and fine-grained metric records are supporting owners. They are listed by
family where their migration follows the boundary record they consume, but they are not
misclassified as scientific objects.

## Target categories and dispositions

Every entry has one primary target category:

| Category | Meaning |
|---|---|
| Scientific model | A modeled periodic system with nominal dimensional identity. |
| Retention definition | A declared selection or construction that identifies what is retained from a parent. |
| Retained subspace | The selected state space, with parentage, rank, and projector or frame identity. |
| Retained operator | The exact operator restricted to an identified retained subspace. |
| Represented operator | A finite coordinate representation of an operator with state-space, basis, geometry, unit, and energy-reference metadata. |
| Effective model | An approximate model instance in a declared restricted class, connected to a parent or retained operator by a reduction result. |
| Encoded campaign document | Preserved input, result, or auxiliary bytes and their identities. |
| Campaign definition/request/result | Immutable controls or outcomes owned by an executable campaign. |

Supporting owner means that the type remains a component, Action, serializer, or
numerical container and does not enter one of the scientific categories by name alone.

Dispositions are **Keep**, **Move**, **Rename**, **Split**, **Replace**, **Remove**, or
**Pending scientific decision**. `Split` means one current type combines meanings that
must become separate target objects. A proposed name below is a migration target, not a
compatibility alias.

## Implemented nominal foundation

| ID | Current type | Current owner | Target category | Disposition and target |
|---|---|---|---|---|
| `PERIODIC-XWALK-001` | `PeriodicModelRole` | `periodic.model` | Scientific model | **Keep.** Orthogonal role metadata; it does not classify retention. |
| `PERIODIC-XWALK-002` | `PeriodicModel` | `periodic.model` | Scientific model | **Keep.** Nominal root only; never a retained-operator or campaign base. |
| `PERIODIC-XWALK-003` | `Periodic1DModel` | `periodic.model` | Scientific model | **Keep.** Canonical 1D nominal branch. |
| `PERIODIC-XWALK-004` | `Periodic2DModel` | `periodic.model` | Scientific model | **Keep.** Canonical 2D nominal branch. |
| `PERIODIC-XWALK-005` | `Periodic3DModel` | `periodic.model` | Scientific model | **Keep.** Canonical 3D nominal branch. |
| `PERIODIC-XWALK-006` | `Periodic1DDefectModel` | `periodic.model` | Scientific model | **Keep.** Nominal 1D defect branch with parent identity. |
| `PERIODIC-XWALK-007` | `Periodic2DDefectModel` | `periodic.model` | Scientific model | **Keep.** Nominal 2D defect branch with parent identity. |
| `PERIODIC-XWALK-008` | `Periodic3DDefectModel` | `periodic.model` | Scientific model | **Keep.** Nominal 3D defect branch with parent identity. |
| `PERIODIC-XWALK-009` | `PeriodicToyModelCatalog` | `periodic.catalog` | Scientific model | **Keep as supporting catalog owner.** Populate only with migrated nominal toy models. |

## Scientific-model and effective-model candidates

| ID | Current type | Observed meaning | Target category | Disposition and target | Preservation or blocker |
|---|---|---|---|---|---|
| `PERIODIC-XWALK-010` | `Periodic2DCosinePotentialToyModel` | Dimensionless 2D cosine parent potential parameters | Scientific model | **Move/adopt** under canonical `periodic2d` model ownership and inherit `Periodic2DModel`. | Preserve the cosine equation, coefficient signs, dimensionless convention, and model identity. |
| `PERIODIC-XWALK-011` | `Periodic1DFiniteHoppingToyModel` | Finite block-hopping toy parent used by 1D defect studies | Scientific model | **Move/adopt** under canonical `periodic1d` model ownership and inherit `Periodic1DModel`. | Add stable model identity without changing block order, units, or Hermiticity contract. |
| `PERIODIC-XWALK-012` | `Periodic2DDefectModel` in `periodic2d.defects.base` | Concrete scalar bulk-plus-localized-perturbation model | Scientific model | **Rename** to a descriptive concrete scalar-hopping defect name and inherit the nominal `periodic.Periodic2DDefectModel`. | Resolve the current name collision; preserve bulk and perturbation composition. |
| `PERIODIC-XWALK-013` | `Periodic1DGaussianOnsiteDefectModel` | Localized Gaussian perturbation parameters, without a pristine parent | Scientific model | **Split.** Keep a descriptively named perturbation definition; construct a separate `Periodic1DDefectModel` only when a parent identity and compatibility data are supplied. | The current record alone is not a complete defect model. |
| `PERIODIC-XWALK-014` | `BlockHoppingModel1D` | Ordered matrix hopping coefficients used for both complete transforms and finite approximations | Represented operator / effective model | **Split semantically.** Keep the coefficient container as supporting representation data; exact transform results identify a represented retained operator, while truncated or fitted results construct an effective model. | Construction route cannot be inferred from coefficients alone. |
| `PERIODIC-XWALK-015` | `ScalarHoppingModel` | Dimensioned reusable scalar hopping inventory | Effective model | **Keep as supporting reusable model data.** A ksdft scientific effective model composes it with parentage, geometry, and reduction provenance. | Do not make a reusable PhysKit-style component depend on ksdft campaign classes. |
| `PERIODIC-XWALK-016` | `PlaneWaveBlochHamiltonian2DModel` | Complete input to one finite plane-wave operator construction | Represented operator | **Rename or retain as a representation definition**, not a `PeriodicModel`; the constructor result supplies the represented operator. | It fixes cutoff, basis, and representation metadata and therefore is not the parent physical model alone. |
| `PERIODIC-XWALK-017` | `PeriodicFourierPotential1D` | Fourier potential component | Scientific model | **Keep as supporting model input.** Compose it into a concrete 1D parent model rather than granting nominal membership by itself. | A potential alone does not identify kinetic law, state space, or complete model. |
| `PERIODIC-XWALK-018` | `Periodic1DBasisScramblingModel` | Parameters of an artificial basis/gauge transformation | Campaign definition/request/result | **Rename** to `Periodic1DBasisScramblingDefinition` and keep with the alignment construction Action. | It is an operation specification, not a scientific model. |

## Retention definitions, spaces, and operators

| ID | Current type | Observed meaning | Target category | Disposition and target | Preservation or blocker |
|---|---|---|---|---|---|
| `PERIODIC-XWALK-019` | `ContiguousBandSelection` | Inclusive parent-band index interval | Retention definition | **Keep and compose** into a parent-qualified periodic retention definition. | Band indices alone do not identify a parent operator, reciprocal domain, or gauge. |
| `PERIODIC-XWALK-020` | `Periodic1DRetainedBandGroup` | Group identity plus contiguous band selection | Retention definition | **Move/replace** with a campaign-independent retention definition carrying explicit parent identity and construction kind. | Preserve group and ordered band identities. |
| `PERIODIC-XWALK-021` | `OrthogonalSpectralSubspace` | Numerical eigenspace basis and eigenvalues | Retained subspace | **Keep as supporting numerical data.** A scientific retained-subspace record wraps or composes it with parent, rank, domain, and construction identity. | It currently has no parent or state-space identity. |
| `PERIODIC-XWALK-022` | `ReciprocalBandFramePath1D` | Ordered frames over a reciprocal mesh | Retained subspace | **Keep as supporting represented frame data.** A retained-subspace owner identifies the parent and interprets the frame path. | A frame path is gauge-dependent representation data, not the abstract retained space by itself. |
| `PERIODIC-XWALK-023` | `Periodic1DIsolatedBandReductionResult` | Aggregate campaign result containing reciprocal samples, hopping data, localization, and diagnostics | Retained operator / effective model / campaign result | **Complete: split.** The historical campaign result remains the diagnostic owner. Authenticated replay artifacts supply the missing frame/projector identity and separate coefficient routes. `Periodic1DIsolatedBandScientificAdoption` constructs the untruncated Fourier parent; a distinct cutoff-11, dimension-23 finite plane-wave parent representation; finite-parent selected-band retention; the retained space and represented frame; an exact invariant restriction of that finite operator; an identified zone-center representation; a complete hopping representation; and distinct truncation- and fit-derived effective-model results. | Historical input/result/producer bytes remain unchanged and SHA-256 correlated. Replay reproduced `result.json` exactly; the sidecar retains the rank-one frame and complete/truncated/fitted coefficients. Separate discretization evidence identifies the cutoff-15 finite reference, five comparison momenta, three compared bands, and retained cutoff-11 observation without claiming an untruncated-parent bound. The adoption request accepts an explicit energy-valued allowance or calculates distinct scale- and dimension-adjusted binary64 allowances when it is `None`; reciprocal-coordinate comparison owns a separate calculated allowance. Passing establishes reproducibility, not validation or UQ. |
| `PERIODIC-XWALK-024` | `Periodic1DCompositeHoppingRepresentationResult` | Smooth reciprocal matrices plus complete smooth and rough hopping representations | Retained operator / represented operator | **Complete: split.** `Periodic1DCompositeScientificAdoption` constructs one gauge-independent exact retained operator per finite-parent band group. `Periodic1DRetainedOperatorReciprocalRepresentation` binds the smooth reciprocal matrices, while separate `Periodic1DRetainedOperatorHoppingRepresentation` records bind the smooth and rough complete hopping families with explicit ordered-basis, energy-reference, map, and gauge metadata. The latter is an authenticated family binding, not the transform-owning `Periodic1DCompleteHoppingRepresentationResult`. | Historical matrices, blocks, ordering, units, and array SHA-256 identities are preserved and authenticated. The unavailable rough reciprocal matrices and frame bytes are not reconstructed; the retained smooth frame/projector identities remain explicit. |
| `PERIODIC-XWALK-025` | `Periodic1DCompositeBandGroupResult` | Aggregate group result combining selection, isolation, gauge, hopping, routes, and identities | Campaign definition/request/result | **Complete: split.** `Periodic1DCompositeBandGroupResult` remains the unchanged owner of isolation, Wilson, gauge, range, route, representation-diagnostic, and artifact-identity evidence. `Periodic1DCompositeOperatorGroupAdoption` references that exact source result while separately binding the finite-parent selected-band definition, retained space, exact retained operator, and represented forms. | Retained-space identity requires the authenticated smooth-projector identity; matching rank or Wilson data alone is rejected. Diagnostics and route outcomes are neither copied into nor reclassified as scientific retained objects. |
| `PERIODIC-XWALK-026` | `ReciprocalOperatorSamples1D` | Square matrices at ordered reciprocal coordinates | Represented operator | **Complete: kept as supporting representation data.** The reusable record retains coordinates, reciprocal period, homogeneous matrix units, rank, and ordering without claiming an operator role. `BandProjectedOperatorPathConstructor1D` establishes parent-input and projected-output roles for its operation. `Periodic1DRetainedOperatorReciprocalRepresentation` separately composes the samples with retained-operator, mesh, ordered-basis, gauge, energy-reference, map, provenance, and content identities when that scientific interpretation is claimed. | Parent, projected, retained, and reconstructed roles are not inferred from the shared sample type or matrix shape. Existing isolated campaign samples remain campaign evidence unless an owning aggregate supplies the missing scientific metadata. |
| `PERIODIC-XWALK-027` | `OperatorCompressionResult` | Numerical coordinates and embedding from orthogonal compression | Retained operator | **Complete: kept as supporting numerical result.** The immutable result correlates one finite real parent matrix and orthonormal numerical subspace with the retained-coordinate matrix $Q^T H Q$ and ambient embedding $Q(Q^T H Q)Q^T=PHP$, including exact dimensions and units. `OperatorCompression` remains the matrix-product Action. No demonstrated periodic-1D route currently composes this generic result into a scientific retained operator; row 023 uses separately identified invariant selected-band retention and is not retrofitted. | The numerical result carries no parent-model/operator, retained-space, basis, gauge, energy-zero, invariance-result, or provenance identity. Invariant restriction, non-invariant Ritz compression, and energy-dependent downfolding remain distinct. Scientific meaning must be attached explicitly rather than inferred from dimensions or route names. |

The phase-4 retention owners now supply the manuscript-level retained-subspace and
exact retained-operator contracts used by completed rows 023--027. Supporting
numerical records remain separate when no campaign-specific scientific binding is
demonstrated. These owners use composition and do not inherit from `PeriodicModel`.

## Represented operators

| ID | Current type | Observed meaning | Target category | Disposition and target |
|---|---|---|---|---|
| `PERIODIC-XWALK-028` | `OperatorRecord` with `StateSpace`, `Basis`, `Geometry`, and `EnergyReference` | Generic dense finite operator representation and interpreting metadata | Represented operator | **Complete: kept.** The general record owns immutable canonical dense matrix values plus explicit state-space, ordered orthonormal basis, geometry, energy-zero/unit, operator-kind, identity, and provenance metadata. It remains non-Hermitian-capable; Hermiticity, compatibility, alignment, subtraction, and residual policy stay in separate Actions. |
| `PERIODIC-XWALK-029` | `ScalarFiniteLatticeOperator` | Sparse scalar finite-periodic hopping operator with twist, basis, and provenance | Represented operator | **Complete: kept.** The specialized record owns canonical complex CSR data, finite-periodic shape/order, correlated twist fiber and gauge, scalar basis identity, matrix unit, energy reference, and provenance. Periodic2d defect aggregates compose it without making PhysKit depend on ksdft scientific owners. It is not replaced by dense `OperatorRecord`. |
| `PERIODIC-XWALK-030` | `RepresentedOperator` with `SupercellBasis` in matched extraction | Campaign-local dense operator and basis | Represented operator | **Pending: exact replacement blocked.** The record remains operationally immutable and campaign-local. `SupercellBasis` lacks explicit cell vectors, exact per-state ordered labels, and structured provenance required for a lossless `OperatorRecord` mapping. These values cannot be reconstructed from dimensions or descriptive ordering strings; no compatibility alias or guessed adapter is introduced. |
| `PERIODIC-XWALK-031` | `PlaneWaveFiberHamiltonian1DResult` | Plane-wave represented 1D fiber operator | Represented operator | **Pending: keep before ownership migration.** The reusable result correlates momentum, finite plane-wave basis, Fourier potential, recoil-energy scale, duality tolerance, and matrix. Canonical `periodic1d` ownership remains blocked on a parent-qualified request carrying stable parent-model, operator, and state-space identities. The potential or matrix dimension is not treated as that identity. |
| `PERIODIC-XWALK-032` | `PeriodicFiniteDifferenceFiberHamiltonian1DResult` | Finite-difference represented 1D fiber operator | Represented operator | **Pending: keep before ownership migration.** The reusable result preserves the ordered half-open grid, reduced momentum, Fourier potential, recoil scale, period tolerance, sparse matrix, and conjugate Bloch seam. Canonical `periodic1d` ownership remains blocked on the same parent-qualified identity contract; moving it must not change grid order or seam orientation. |
| `PERIODIC-XWALK-033` | `PlaneWaveBlochHamiltonian2DResult` | General 2D continuum plane-wave represented operator | Represented operator | **Complete: kept.** The reusable result retains the complete request, model-owned state-space/basis/energy-reference identities, PhysKit direct/reciprocal geometry, reduced momentum, finite cutoff/order, energy-valued matrix, and checked duality residual. It remains represented-space output and does not inherit from `PeriodicModel` or own campaign acceptance. |
| `PERIODIC-XWALK-034` | `Periodic2DPlaneWaveHamiltonianResult` | Cosine-model plane-wave campaign adapter result | Represented operator | **Complete: adapted.** `Periodic2DPlaneWaveHamiltonianConstructor` maps the cosine model and exact request into the general `PlaneWaveBlochHamiltonian2DConstructor`, then retains the campaign request, immutable matrix, and duality residual in the adapter result. The campaign no longer owns a second plane-wave assembly algorithm. |
| `PERIODIC-XWALK-035` | `Periodic2DFiniteDifferenceHamiltonianResult` | Cosine-model finite-difference represented operator | Represented operator | **Pending: keep before reusable migration.** The result retains the exact toy-model request, grid size/order, reduced momentum determining the seam phases, matrix dimension, and Hermiticity, but the bare matrix still relies on an implicit dimensionless energy convention and lacks a general state-space, basis, energy-reference, and provenance contract. Those metadata must be designed explicitly before moving ownership. |
| `PERIODIC-XWALK-036` | `Periodic2DCommonSpaceComparisonResult` | Transport map and threshold-free represented-operator disagreement | Campaign definition/request/result | **Complete: kept as comparison result.** The exact request enforces common model and momentum plus grid resolution; the result intrinsically correlates the directional plane-wave-to-grid isometry, transported finite-difference operator, signed difference, and recomputed threshold-free norms. It is neither another represented operator nor an acceptance result. |

Rows 028, 029, 033, 034, and 036 are complete. Rows 030--032 and 035 remain
explicitly pending because their missing metadata or ownership contracts cannot be
recovered without choosing new conventions. This is a bounded blocker disposition,
not an authorization to infer metadata, add compatibility aliases, or duplicate
represented-operator algorithms.

## Encoded campaign documents

Every row in this section preserves exact bytes, byte order, content digests,
experiment identifiers, and provenance paths. Renames provide no compatibility aliases.

| ID | Current type | Current encoded fields | Disposition and target |
|---|---|---|---|
| `PERIODIC-XWALK-037` | `Periodic1DIsolatedBandCampaignModel` | `input_payload`, `result_payload` | **Rename/move** to `Periodic1DIsolatedBandEncodedDocuments`. |
| `PERIODIC-XWALK-038` | `Periodic1DCompositeCampaignModel` | `input_payload`, `result_payload` | **Rename/move** to `Periodic1DCompositeEncodedDocuments`. |
| `PERIODIC-XWALK-039` | `Periodic1DStressCampaignModel` | `input_payload`, `result_payload` | **Rename/move** to `Periodic1DReductionChallengeEncodedDocuments`; “challenge” refers to tests of the nominal reduction assumptions, not mechanical stress. |
| `PERIODIC-XWALK-040` | `Periodic1DWannier90IntegrationModel` | composite input, result, result kind, native artifact groups | **Rename/split** to `Periodic1DWannier90EncodedDocuments` plus the existing artifact-group records. |
| `PERIODIC-XWALK-041` | `BlindAlignmentCampaignModel` | input and result documents plus repository root | **Rename/move** to `BlindAlignmentEncodedDocuments`; move repository location into an execution request. |
| `PERIODIC-XWALK-042` | `ContinuumRefinementCampaignModel` | input and result documents plus repository root | **Rename/move** to `ContinuumRefinementEncodedDocuments`; move repository location into an execution request. |
| `PERIODIC-XWALK-043` | `FiniteRankOracleCampaignModel` | input and result documents plus repository root | **Rename/move** to `FiniteRankOracleEncodedDocuments`; move repository location into an execution request. |
| `PERIODIC-XWALK-044` | `RouteReconciliationCampaignModel` | input and result documents plus repository root | **Rename/move** to `RouteReconciliationEncodedDocuments`; move repository location into an execution request. |
| `PERIODIC-XWALK-045` | `Periodic1DRetainedResultDocument` | parsed result tree, kind, source bytes, and source digest | **Rename** to `Periodic1DEncodedResultDocument`; rename its associated kind and serializer to `Periodic1DEncodedResultKind` and `Periodic1DEncodedResultJsonSerializer`. Scientific result names using `Retained` for selected-space content remain unchanged. |
| `PERIODIC-XWALK-046` | `Periodic2DIsolatedBandCampaignModel` | `input_payload`, `result_payload` | **Rename/move** to `Periodic2DIsolatedBandEncodedDocuments`. |
| `PERIODIC-XWALK-047` | `Periodic2DCompositeCampaignModel` | `input_payload`, `result_payload` | **Rename/move** to `Periodic2DCompositeEncodedDocuments`. |
| `PERIODIC-XWALK-048` | `Periodic2DTopologicalCampaignModel` | `input_payload`, `result_payload` | **Rename/move** to `Periodic2DTopologicalEncodedDocuments`. |
| `PERIODIC-XWALK-049` | `Periodic2DTopologicalPhaseSweepCampaignModel` | `input_payload`, `result_payload` | **Rename/move** to `Periodic2DTopologicalPhaseSweepEncodedDocuments`. |
| `PERIODIC-XWALK-050` | `Periodic2DWannier90BalancedCampaignModel` | `result_payload` | **Rename/move** to `Periodic2DWannier90BalancedEncodedDocuments`. |
| `PERIODIC-XWALK-051` | `Periodic2DWannier90StudyCampaignModel` | `input_payload`, `result_payload` | **Rename/move** to `Periodic2DWannier90StudyEncodedDocuments`. |
| `PERIODIC-XWALK-052` | `Periodic2DOptimizerBasinCampaignModel` | `input_payload`, `result_payload` | **Rename/move** to `Periodic2DOptimizerBasinEncodedDocuments`. |
| `PERIODIC-XWALK-053` | `Periodic2DOptimizerReanalysisCampaignModel` | source result and reanalysis result payloads | **Rename/move** to `Periodic2DOptimizerReanalysisEncodedDocuments`. |
| `PERIODIC-XWALK-054` | `Periodic2DOptimizerRegressionCampaignModel` | standalone result, analyzer, and regression payloads | **Rename/move** to `Periodic2DOptimizerRegressionEncodedDocuments`. |
| `PERIODIC-XWALK-055` | `Periodic2DOptimizerStandaloneCampaignModel` | proposal, initial-gauge, and result payloads | **Rename/move** to `Periodic2DOptimizerStandaloneEncodedDocuments`. |
| `PERIODIC-XWALK-056` | `Periodic2DIsolatedBandResultDocument` | exact result payload | **Keep** as an encoded campaign result document; it is already not named as a model. |
| `PERIODIC-XWALK-057` | `ContinuumRefinementCampaignResultDocument`, `FiniteRankOracleCampaignResultDocument`, `RouteReconciliationCampaignResultDocument` | exact result payload | **Keep/move** with their campaign document owners; they are encoded documents, not scientific models. |

## Campaign definitions, executions, and results

The entries below classify cohesive families. Every exact member named in a row has the
same category and disposition; the family identifier is the migration unit. Supporting
serializers, calculators, correlators, verifiers, and Workflows remain with the family
unless a separate reusable Action contract is demonstrated.

| ID | Exact current members | Target category | Disposition |
|---|---|---|---|
| `PERIODIC-XWALK-058` | `Periodic1DIsolatedBandCampaignDefinition`, `Periodic1DIsolatedBandCampaign`, `Periodic1DIsolatedBandCampaignResult` | Campaign definition/request/result | **Move** together to canonical `periodic1d.campaign` ownership; replace model fields with encoded-document and scientific-object fields as applicable. |
| `PERIODIC-XWALK-059` | `Periodic1DCompositeCampaignDefinition`, `Periodic1DCompositeCampaign`, `Periodic1DCompositeCampaignResult` | Campaign definition/request/result | **Move** together; reference explicit retention definitions and retained scientific objects after their introduction. |
| `PERIODIC-XWALK-060` | `Periodic1DStressCampaignDefinition`, `Periodic1DStressCampaign`, `Periodic1DStressCampaignResult` | Campaign definition/request/result | **Rename/move** together as the periodic-1D reduction-challenge campaign family without converting expected trends into verification criteria; preserve existing wire identifiers and filenames. |
| `PERIODIC-XWALK-061` | `Periodic1DWannier90CampaignResult` and its Workflow request/result envelopes | Campaign definition/request/result | **Move** under the canonical 1D campaign integration boundary; native artifacts remain integration-owned. |
| `PERIODIC-XWALK-062` | `BlindAlignmentCampaignInput`, `BlindAlignmentCampaign`, `BlindAlignmentCampaignResult`, and calculation/workflow/verification request/results | Campaign definition/request/result | **Keep then move** as one campaign family; alignment Actions remain distinct from encoded documents and campaign policy. |
| `PERIODIC-XWALK-063` | `ContinuumRefinementCampaignInput`, `ContinuumRefinementCampaign`, result document, correlation, and verification request/results | Campaign definition/request/result | **Keep then move** as one campaign family; continuum/lattice embedding remains explicit. |
| `PERIODIC-XWALK-064` | `FiniteRankOracleCampaignInput`, `FiniteRankOracleCampaign`, result document, correlation, and verification request/results | Campaign definition/request/result | **Keep then move** as one campaign family; finite-rank oracle mathematics does not define general retention by itself. |
| `PERIODIC-XWALK-065` | `DefectExerciseInput`, `MatchedDefectExtractionWorkflowResult`, and matched-extraction compatibility/verification result envelopes | Campaign definition/request/result | **Keep then move**; replace the local represented-operator record through row 030 before widening use. |
| `PERIODIC-XWALK-066` | `RouteReconciliationCampaignInput`, `RouteReconciliationCampaign`, result document, correlation, extraction, and verification request/results | Campaign definition/request/result | **Keep then move** with explicit route identities and compatibility prerequisites. |
| `PERIODIC-XWALK-067` | `Periodic2DIsolatedBandCampaignDefinition`, `Periodic2DIsolatedBandCampaign`, calculation/correlation/verification request/results | Campaign definition/request/result | **Keep** under canonical `periodic2d.campaign.nbands_1`; replace encoded-model terminology and decompose scientific results. |
| `PERIODIC-XWALK-068` | `Periodic2DCompositeCampaign` and calculation/correlation/verification request/results | Campaign definition/request/result | **Keep then decompose** under canonical `periodic2d.campaign`; introduce typed scientific results before adapter retirement. |
| `PERIODIC-XWALK-069` | `Periodic2DTopologicalCampaign` and calculation/correlation/verification request/results | Campaign definition/request/result | **Keep then decompose**; topology results remain campaign observations, not expected-result oracles. |
| `PERIODIC-XWALK-070` | `Periodic2DTopologicalPhaseSweepCampaign` and calculation/correlation/verification request/results | Campaign definition/request/result | **Keep then decompose** with explicit unavailable outcomes. |
| `PERIODIC-XWALK-071` | `Periodic2DWannier90BalancedCampaign`, `Periodic2DWannier90StudyCampaign`, and their verification request/results | Campaign definition/request/result | **Keep then move** behind integration-owned native adapters. |
| `PERIODIC-XWALK-072` | `Periodic2DOptimizerBasinCampaign`, `Periodic2DOptimizerStandaloneCampaign`, `Periodic2DOptimizerReanalysisCampaign`, `Periodic2DOptimizerRegressionCampaign`, and verification request/results | Campaign definition/request/result | **Keep then decompose**; optimizer policy remains campaign-owned. |
| `PERIODIC-XWALK-073` | `Periodic2DCampaign` | Campaign definition/request/result | **Remove** after its ten concrete subclasses no longer need a dimension-only campaign base. Do not replace it with 1D/3D campaign bases. |

The request/result envelopes for correlation, verification, verified Workflows, and
native-artifact preparation remain campaign types even when they contain represented
scientific observations. Their contained objects retain their own categories; container
membership does not change scientific identity.

## Supporting owners deliberately outside the eight categories

The following owners are inspected and retained as supporting mechanics rather than
being forced into a scientific category:

| Supporting family | Current owners | Required boundary |
|---|---|---|
| Representation definitions | `PeriodicUniformGrid1D`, `Periodic2DPlaneWaveBasis`, `Periodic2DUniformCellGrid`, `CenteredUniformReciprocalMesh2D` | Grids, bases, and meshes are neither models nor retained spaces. |
| Construction requests and Actions | plane-wave, finite-difference, reciprocal-neighbor, sewing, primitive-fiber, supercell, onsite-defect, and basis-scrambling requests/constructors | Actions construct or transform typed objects; request names do not establish model identity. |
| Alignment and frame mechanics | `PolarBandFrameTransporter1D`, `BandFrameAligner1D`, projector-path and basis-scrambling constructors | Diagnostics, transport maps, and aligned frames remain separate results. |
| Operator comparison | `OperatorRecordCompatibilityAnalyzer`, `OperatorRecordDifferencer`, `OperatorRecordResidualAnalyzer`, `Periodic2DCommonSpaceOperatorComparator` | Compatibility precedes transport, subtraction, and residual analysis. |
| Finite hopping mechanics | `ReciprocalOperatorFourierTransformer1D`, truncators, fitters, Parseval analyzers, and `TwistedSupercellOperatorConstructor` | Complete transform, truncation, fitting, and finite-periodic construction remain distinct. |
| Wire mechanics | campaign JSON serializers/decoders and `OperatorRecordJsonSerializer` | Serializers adapt typed records; they do not own scientific policy. |
| Evidence mechanics | campaign correlators and verifiers | Authentication, reconstruction, and scientific interpretation remain distinct. |

## Completeness accounting

The inventory used Python AST inspection of every module in the listed roots. The
following exclusions are intentional:

- private classes and type aliases;
- enums that only label issue codes, numerical status, or serialization variants;
- fine-grained scalar diagnostic records already contained in a classified campaign
  result;
- serializers, decoders, Actions, Workflows, correlators, and verifiers covered by the
  supporting-family table;
- geometry, lattice, unit, and quantity records that do not claim model, retention,
  operator, or campaign ownership; and
- compatibility re-export modules containing no independent class definition.

A migration that encounters an omitted class whose meaning crosses one of the eight
category boundaries must add it here before changing that class. Source changes cite
the applicable `PERIODIC-XWALK-*` identifier.

## Dependency-ordered migration

The authoritative phase index is [`migration.md`](migration.md), and the detailed
encoded-document gate is in [`migration-3.md`](migration-3.md). In crosswalk terms:

1. Complete rows 037--057 through the four bounded encoded-document slices without
   changing bytes or provenance.
2. Introduce the missing parent-qualified retention definition, retained-subspace, and
   retained-operator owners needed by rows 019--027.
3. Complete represented-operator mapping in rows 028--036.
4. Adopt the 1D scientific and effective model candidates in rows 011 and 013--018,
   then complete 1D campaign rows 058--066.
5. Register only migrated nominal toy models in `PeriodicToyModelCatalog` and add one
   campaign that consumes an exact immutable catalog snapshot.
6. Adopt 2D model rows 010 and 012 while completing campaign rows 067--072 and the
   periodic2d parity gate.
7. Remove the provisional base through row 073 after all concrete consumers are
   independent of it.

Defect progression remains blocked until its parent model, retained space, represented
operator, alignment, and comparison prerequisites are implemented and verified.

## Completion criteria

This crosswalk becomes **Completed** only when:

1. every row has a terminal implemented disposition and no unresolved split;
2. target owners, typing, exports, tests, and documentation agree;
3. former encoded-document model names and import routes are absent, with no
   compatibility aliases;
4. preserved bytes, digests, experiment identities, and provenance paths have been
   verified unchanged;
5. relevant software and numerical verification gates pass; and
6. a final AST inventory confirms every boundary-defining source type is represented.

## Archive and retirement

Git is the archive; no duplicate completed crosswalk remains in the active tree.
Retirement uses two commits:

1. a completion commit marks this document **Completed**, records the completion
   commit's parent as the final source audit point, and contains every terminal
   disposition; and
2. a following retirement commit removes this page from active navigation and adds an
   entry to `archives.md` containing the immutable repository locator
   `<completion-commit>:docs/architecture/v2/ksdft2effmass/periodic/current-to-target-class-crosswalk.md`
   plus links to the final authoritative architecture pages.

The crosswalk is not retired merely because the first rename lands, tests pass on a
feature branch, or retained evidence remains readable. Retirement occurs only after
integration into the canonical development branch and the completion audit above.
