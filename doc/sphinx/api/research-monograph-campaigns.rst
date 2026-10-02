Research-monograph campaigns
=============================

``ksdft2effmass.campaigns.research_monograph`` contains public composition and
retained-format contracts for the project's research-monograph calculations.  These
campaign objects bind exact study controls to reusable analysis contracts.  They do
not own generic scientific algorithms, grant protected execution authority, or decide
scientific acceptance.  Campaign implementation classes and methods are public and
use no underscore-prefixed implementation names; Python-required special methods are
the only exception.

Citation snapshot
-----------------

The unversioned citation snapshot covers one exact repository-owned manuscript
entrypoint and bibliography.  It emits immutable source files, include instances,
bibliography entries, rendered calls, key occurrences and groups, prospective
citation markers, and non-key source gaps.  A successful compilation means complete
coverage of the closed source grammar; unsupported citation-capable syntax fails
without returning a partial snapshot.  Locators retain exact content identities and
byte spans but no excerpts.  Relevant source bytes must equal the recorded Git HEAD.
The owner Result binds a root-independent request identity to the complete replayed
snapshot projection.  The nullable References observation binding remains unset until
an independent References owner verifies it.

.. currentmodule:: ksdft2effmass.campaigns.research_monograph

.. autoclass:: CitationContentAlgorithm
   :members:

.. autoclass:: CitationContentIdentity
   :members:

.. autoclass:: ManuscriptSourceLocator
   :members:

.. autoclass:: ManuscriptSourceFileSnapshot
   :members:

.. autoclass:: ManuscriptIncludeInstance
   :members:

.. autoclass:: ManuscriptBibliographyEntrySnapshot
   :members:

.. autoclass:: ManuscriptCitationCommandKind
   :members:

.. autoclass:: ManuscriptCitationOrigin
   :members:

.. autoclass:: ManuscriptCitationPriority
   :members:

.. autoclass:: ManuscriptCitationCall
   :members:

.. autoclass:: ManuscriptCitationOccurrence
   :members:

.. autoclass:: ManuscriptCitationGroup
   :members:

.. autoclass:: ManuscriptCitationTodo
   :members:

.. autoclass:: ManuscriptCitationSourceGapReason
   :members:

.. autoclass:: ManuscriptCitationSourceGap
   :members:

.. autoclass:: ManuscriptCitationSnapshot
   :members:

.. autoclass:: ResearchMonographCitationSnapshotRequest
   :members:

.. autoclass:: ResearchMonographCitationSnapshotResult
   :members:

.. autoclass:: CitationSnapshotErrorCode
   :members:

.. autoclass:: CitationSnapshotError
   :members:

.. autoclass:: ResearchMonographCitationSnapshotIntegrityValidator
   :members:

.. autoclass:: ResearchMonographCitationSnapshotCompiler
   :members:

Defect-2D retained-result plotting
----------------------------------

``AdoptedCriteriaPlot`` and ``AdverseControlBarPlot`` are the reusable Matplotlib
components for the retained scalar channels.  Each constructor accepts an existing
:class:`matplotlib.axes.Axes` or ``None``.  When no axes are supplied, ``execute``
creates axes in a new figure and returns them; when axes are supplied, the component
clears, populates, and returns that same object.  Adverse numerical bars are normalized
by their maximum solely for display.  A status-only adverse control receives a fixed
purple bar, so neither bar length nor color is a physical quantity.

``StageCParentSvgPlotter`` composes both components for new Stage C plotting
operations.  It consumes an explicitly supplied retained JSON result and writes a new
SVG containing only scalar criterion and adverse-control diagnostics.  It performs no
accepted-parent calculation, matrix-artifact read, scientific validation, or
uncertainty quantification.  Existing output paths are rejected.  Historical retained
SVG provenance remains bound to the frozen ``plot_stage_c_parent.py`` entry point; the
version-two CLI delegates new rendering to these public classes without reattributing
historical results.

.. currentmodule:: ksdft2effmass.campaigns.research_monograph

.. autoclass:: AdoptedCriterionPlotRecord
   :members:

.. autoclass:: AdoptedCriteriaPlot
   :members:

.. autoclass:: AdverseControlPlotRecord
   :members:

.. autoclass:: AdverseControlBarPlot
   :members:

.. autoclass:: StageCParentSvgPlotter
   :members:

Periodic2d isolated-band campaign
---------------------------------

``Periodic2DIsolatedBandCampaign`` preserves the retained periodic2d version-one
input and result bytes. Its current immutable model owns those exact wire documents.
Separate Actionizers calculate, correlate, and independently verify the controlled
scalar campaign. This surface does not yet claim complete periodic1d capability
parity. Canonical correlation reproduces the retained document but makes no
numerical claim. The verifier authenticates retained input and runner identities and
independently reconstructs parent convergence, separability, projector, topology,
hopping, effective-mass, coupling, and anisotropy channels without importing the
maintained calculation route or toy-model constructors.

Reusable represented mechanics live under
``ksdft2effmass.periodic2d.model.toy_models``.
``Periodic2DCosinePotentialToyModel`` owns the dimensionless separable-to-coupled
cosine potential. Separate constructors produce finite plane-wave and centered Bloch
finite-difference Hamiltonians. These toy owners contain no campaign provenance,
acceptance policy, or material interpretation. See
:doc:`../concepts/periodic2d-controlled-reduction` for the represented and evidence
boundaries.

.. currentmodule:: ksdft2effmass.periodic2d

``Periodic2DCampaign`` supplies the lightweight nominal and dimensional identity
shared by canonical periodic2d campaigns. It deliberately owns no model, numerical,
serialization, or acceptance policy; see
:doc:`ksdft2effmass/periodic2d/campaign/base`. The canonical one-band campaign
package is ``ksdft2effmass.periodic2d.campaign.nbands_1``. Because the project is
still alpha, the former ``ksdft2effmass.campaigns.periodic2d`` and publication-owned
routes were removed rather than retained as compatibility façades.

.. autoclass:: Periodic2DIsolatedBandEncodedDocuments
   :members:

.. autoclass:: Periodic2DIsolatedBandCampaign
   :members:

The version-one input now has a strict typed definition and deterministic JSON
serializer. See
:doc:`ksdft2effmass/periodic2d/campaign/nbands_1/serialization` for its complete
field, unit, failure, canonicalization, and evidence contracts.

.. toctree::
   :hidden:

   ksdft2effmass/periodic2d/campaign/base
   ksdft2effmass/periodic2d/campaign/nbands_1/serialization

.. autoclass:: Periodic2DIsolatedBandCampaignDefinition
   :members:
   :no-index:

.. autoclass:: Periodic2DIsolatedBandCampaignJsonSerializer
   :members:
   :no-index:

.. autoclass:: Periodic2DIsolatedBandProvenance
   :members:
   :no-index:

.. autoclass:: Periodic2DIsolatedBandResultDocument
   :members:
   :no-index:

``Periodic2DCompositeCampaign`` uses the same encapsulated retained-wire structure for
the isolated rank-three projected-gauge study. Correlation and numerical verification
remain distinct; the independent verifier reconstructs smooth and controlled rough
gauges without importing the maintained calculation route.

.. autoclass:: Periodic2DCompositeEncodedDocuments
   :members:

.. autoclass:: Periodic2DCompositeCampaign
   :members:

``Periodic2DTopologicalCampaign`` preserves three distinct topological model
families and their trivial controls. Its independent route reconstructs spectra,
projector Bargmann invariants, Chern diagnostics, and Wilson winding.

.. autoclass:: Periodic2DTopologicalEncodedDocuments
   :members:

.. autoclass:: Periodic2DTopologicalCampaign
   :members:

``Periodic2DTopologicalPhaseSweepCampaign`` retains separate parameter axes and
independently reconstructs every sampled gap and Chern diagnostic.

.. autoclass:: Periodic2DTopologicalPhaseSweepEncodedDocuments
   :members:

.. autoclass:: Periodic2DTopologicalPhaseSweepCampaign
   :members:

``Periodic2DWannier90BalancedCampaign`` independently reconstructs the compact
repository-portable evidence from one retained balanced Wannier90 comparison. It does
not execute Wannier90 or access the external native-run directory.

.. autoclass:: Periodic2DWannier90BalancedEncodedDocuments
   :members:

.. autoclass:: Periodic2DWannier90BalancedCampaign
   :members:

``Periodic2DWannier90StudyCampaign`` authenticates six compact case fixtures and
reuses the independent portable reconstruction for each declared sensitivity axis.

.. autoclass:: Periodic2DWannier90StudyEncodedDocuments
   :members:

.. autoclass:: Periodic2DWannier90StudyCampaign
   :members:

``Periodic2DOptimizerBasinCampaign`` verifies retained multi-start endpoints, basin
partitions, censored outcomes, and the frozen negative convergence disposition without
accessing native execution files.

.. autoclass:: Periodic2DOptimizerBasinEncodedDocuments
   :members:

.. autoclass:: Periodic2DOptimizerBasinCampaign
   :members:

``Periodic2DOptimizerReanalysisCampaign`` checks the retained native-spread
decomposition, terminal-trace classifications, symmetry-aware basin partitions, and
repository-retained estimator-grid refinements without opening external run paths.

.. autoclass:: Periodic2DOptimizerReanalysisCampaignModel
   :members:

.. autoclass:: Periodic2DOptimizerReanalysisCampaign
   :members:

``Periodic2DOptimizerStandaloneCampaign`` verifies all retained initial endpoints,
exact-checkpoint continuations, density-aware basin partitions, threshold-sensitivity
records, and the negative standalone-study disposition.

.. autoclass:: Periodic2DOptimizerStandaloneCampaignModel
   :members:

.. autoclass:: Periodic2DOptimizerStandaloneCampaign
   :members:

``Periodic2DOptimizerRegressionCampaign`` independently reconstructs the retained
right-censored log-normal likelihood, score, clustered covariance, adjusted time
ratios, intervals, and predicted finite-trajectory convergence curves.

.. autoclass:: Periodic2DOptimizerRegressionCampaignModel
   :members:

.. autoclass:: Periodic2DOptimizerRegressionCampaign
   :members:

Periodic2d common-space operator comparison
-------------------------------------------

The typed comparator samples the declared plane waves on the finite-difference grid,
transports the coordinate operator into plane-wave space, and records threshold-free
operator disagreement diagnostics. See
:doc:`ksdft2effmass/periodic2d/common_space` for equations, compatibility
preconditions, numerical evidence, and limitations.

.. toctree::
   :hidden:

   ksdft2effmass/periodic2d/common_space

.. currentmodule:: ksdft2effmass.periodic2d

.. autoclass:: Periodic2DCommonSpaceComparisonRequest
   :members:
   :no-index:

.. autoclass:: Periodic2DCommonSpaceComparisonResult
   :members:
   :no-index:

.. autoclass:: Periodic2DCommonSpaceOperatorComparator
   :members:
   :no-index:

.. currentmodule:: ksdft2effmass.periodic2d.model.toy_models

.. autoclass:: Periodic2DCosinePotentialToyModel
   :members:

.. autoclass:: Periodic2DPlaneWaveBasis
   :members:

.. autoclass:: Periodic2DPlaneWaveHamiltonianRequest
   :members:

.. autoclass:: Periodic2DPlaneWaveHamiltonianConstructor
   :members:

.. autoclass:: Periodic2DPlaneWaveHamiltonianResult
   :members:

.. autoclass:: Periodic2DUniformCellGrid
   :members:

.. autoclass:: Periodic2DFiniteDifferenceHamiltonianRequest
   :members:

.. autoclass:: Periodic2DFiniteDifferenceHamiltonianConstructor
   :members:

.. autoclass:: Periodic2DFiniteDifferenceHamiltonianResult
   :members:

.. autoclass:: Periodic2DHamiltonianResult
   :members:

Periodic2d finite-extent defects
--------------------------------

``Periodic2DDefect`` encapsulates a translation-invariant scalar parent and one
finite-support perturbation.  Representation keeps the bulk operator
:math:`H_0`, perturbation :math:`\Delta H`, compatibility evidence, and composed
defect operator :math:`H_{\mathrm{def}}=H_0+\Delta H` separate.  An onsite-only
perturbation represents a scalar perturbation potential; a perturbation containing
directed bond terms is the more general finite-extent operator change used by the
defect campaign and is not mislabeled as a potential.

The representer requires an explicit two-dimensional finite-periodic shape and boundary
twist.  It preserves basis, energy-reference, unit, geometry, and twist compatibility,
constructs sparse matrices without implicit densification, and performs no protected
calculation or scientific acceptance.  The separate perturbation extractor implements
:math:`\Delta H=H_{\mathrm{def}}-H_0` only for already compatible represented
operators; it performs no implicit alignment or energy-zero inference.  The locality
Actionizer partitions sites by minimum-image Chebyshev distance from an explicit defect
origin and reports core, exterior, core--exterior, and shell-resolved norms.  A
finite-extent disposition uses explicit energy-unit tolerances for the exterior and
core--exterior channels. See :doc:`../concepts/periodic2d-finite-extent-defects`
for the methodological boundary and partition definitions.

.. currentmodule:: ksdft2effmass.periodic2d

.. autoclass:: Periodic2DDefect
   :members:

.. autoclass:: Periodic2DDefectModel
   :members:

.. autoclass:: Periodic2DDefectRepresenter
   :members:

.. autoclass:: Periodic2DDefectRepresentationRequest
   :members:

.. autoclass:: Periodic2DDefectRepresentationResult
   :members:

.. autoclass:: Periodic2DDefectPerturbationExtractor
   :members:

.. autoclass:: Periodic2DDefectExtractionRequest
   :members:

.. autoclass:: Periodic2DDefectExtractionResult
   :members:

.. autoclass:: Periodic2DDefectLocalityAnalyzer
   :members:

.. autoclass:: Periodic2DDefectLocalityRequest
   :members:

.. autoclass:: Periodic2DDefectLocalityResult
   :members:

Periodic-1D hopping reduction
-----------------------------

The canonical public package is ``ksdft2effmass.campaigns.periodic_1d``. The former
``ksdft2effmass.campaigns.research_monograph.periodic_1d`` import façade is deprecated;
it re-exports the same public objects and emits :class:`DeprecationWarning`.

The versioned Appendix G Workflow composes complete uniform-mesh Fourier transform,
symmetric truncation, Parseval analysis, explicit-weight least-squares fitting, and
withheld-coordinate route comparison. The read-only composite Workflow binds retained
gaps, dense reciprocal Hamiltonians, complete smooth- and rough-gauge hopping blocks,
gauge and alignment defects, range studies, direct-route comparisons, Wilson spectra,
and intermediate-array identities to the exact campaign input.  These channels remain
separate: in particular, an unaligned gauge-dependent hopping defect is not a
basis-aligned operator error, and training errors are not withheld-mesh errors.
Wannier90 Workflows separately bind retained Wilson spectra and circular center
comparisons to exact inputs. Periodic-1D calculation scripts remain in-development
adapters and keep domain behavior in these Workflows, which perform no filesystem
discovery or external Wannier90 operation.

.. currentmodule:: ksdft2effmass.campaigns.periodic_1d

Periodic-1D defect toy models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Reusable controlled systems demonstrated by the defect campaigns are available from
``ksdft2effmass.campaigns.periodic_1d.model.toy_defects``.
``Periodic1DFiniteHoppingToyModel`` represents a finite Hermitian hopping family.
Separate Actionizers construct primitive Bloch fibers and explicitly twisted finite
supercells. ``Periodic1DBasisScramblingModel`` represents controlled site translation,
orbital permutation and rotation, site and orbital phases, and optional spin-half
rotation; its constructor returns both explicitly oriented unitary map directions.
``Periodic1DGaussianOnsiteDefectModel`` represents a dimensionless
minimum-image Gaussian onsite perturbation and its constructor returns the profile,
coordinates, and represented block-diagonal operator.

These classes own reusable toy-model state and numerical construction only. They own
no retained paths, campaign thresholds, phase labels, evidence acceptance, silicon
interpretation, or protected execution. A general finite-extent operator perturbation
with directed bond blocks is not represented as an onsite Gaussian potential.

.. currentmodule:: ksdft2effmass.campaigns.periodic_1d.model.toy_defects

.. autoclass:: Periodic1DBasisScramblingModel
   :members:

.. autoclass:: Periodic1DBasisScramblingRequest
   :members:

.. autoclass:: Periodic1DBasisScramblingResult
   :members:

.. autoclass:: Periodic1DBasisScramblingConstructor
   :members:

.. autoclass:: Periodic1DHoppingBlock
   :members:

.. autoclass:: Periodic1DFiniteHoppingToyModel
   :members:

.. autoclass:: Periodic1DPrimitiveFiberHamiltonianRequest
   :members:

.. autoclass:: Periodic1DPrimitiveFiberHamiltonianResult
   :members:

.. autoclass:: Periodic1DPrimitiveFiberHamiltonianConstructor
   :members:

.. autoclass:: Periodic1DSupercellHamiltonianRequest
   :members:

.. autoclass:: Periodic1DSupercellHamiltonianResult
   :members:

.. autoclass:: Periodic1DSupercellHamiltonianConstructor
   :members:

.. autoclass:: Periodic1DGaussianOnsiteDefectModel
   :members:

.. autoclass:: Periodic1DGaussianOnsiteDefectRequest
   :members:

.. autoclass:: Periodic1DGaussianOnsiteDefectResult
   :members:

.. autoclass:: Periodic1DGaussianOnsiteDefectConstructor
   :members:

Periodic-1D matched defect extraction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The maintained matched known-map capability is available from
``ksdft2effmass.campaigns.periodic_1d.defects.matched_extraction``.
Its immutable records preserve the retained version-one controls and represented-space
metadata.  ``MatchedDefectOperatorCompatibilityAnalyzer`` checks every declared
comparison convention before subtraction.  ``MatchedDefectExtractionWorkflow``
constructs the bounded synthetic folding, extraction, finite-size, model-class, and
observable controls.  ``MatchedDefectExtractionResultVerifier`` reconstructs the
retained result independently without importing the workflow.

The input deserializer rejects unsupported schemas, booleans in numeric fields,
numeric strings, nonfinite values, and malformed fixed-shape controls.  The parent
loader authenticates exact retained periodic-1D parent identities before decoding
hopping records.  A newly serialized result records the maintained implementation's
own provenance; it does not inherit the historical result's acceptance status.  See
:doc:`../concepts/periodic-1d-defect-extraction` for the comparison and evidence
boundary.

.. currentmodule:: ksdft2effmass.campaigns.periodic_1d.defects.matched_extraction

.. autoclass:: ParentSourceReference
   :members:

.. autoclass:: FoldingControl
   :members:

.. autoclass:: ExtractionControl
   :members:

.. autoclass:: AlignmentControl
   :members:

.. autoclass:: FiniteSizeControl
   :members:

.. autoclass:: SmoothnessControl
   :members:

.. autoclass:: MetricContrastControl
   :members:

.. autoclass:: DefectExerciseInput
   :members:

.. autoclass:: SupercellBasis
   :members:

.. autoclass:: RepresentedOperator
   :members:

.. autoclass:: CompatibilityResult
   :members:

.. autoclass:: ParentData
   :members:

.. autoclass:: MatchedDefectExtractionInputDeserializer
   :members:

.. autoclass:: MatchedDefectParentDataLoader
   :members:

.. autoclass:: MatchedDefectExtractionResultSerializer
   :members:

.. autoclass:: MatchedDefectOperatorCompatibilityAnalyzer
   :members:

.. autoclass:: MatchedDefectExtractionWorkflow
   :members:

.. autoclass:: MatchedDefectExtractionWorkflowResult
   :members:

.. autoclass:: MatchedDefectExtractionResultVerifier
   :members:

Periodic-1D blind alignment
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The maintained public route exports only ``BlindAlignmentCampaign`` and
``BlindAlignmentEncodedDocuments`` from
``ksdft2effmass.campaigns.periodic_1d.defects.blind_alignment``. The encoded-document
owner stores exact input and retained-result bytes only. The façade delegates retained
decoding, complete calculation, and identity-only correlation to cohesive Actionizers;
operations that authenticate repository-relative sources receive an explicit absolute
filesystem root in their request.

Internally, ``BlindAlignmentObservation`` contains only inference-visible represented operators,
anchor cross-covariance, retained-subspace overlap, exterior energy anchor, and the
explicit partial-alignment declaration. ``BlindAlignmentInferenceActionizer`` applies
only the supplied numerical policy and returns either a full or identified-sector
result or a structured stopping code. The separate rectangular method requires an
explicit lower-dimensional candidate and partial-alignment declaration.

``BlindAlignmentInputDeserializer`` adapts the exact closed version-one retained input.
It rejects additional or missing fields, unsupported versions, booleans in numeric
positions, numeric strings, and nonfinite values. It does not authenticate the files
named by source identities.

``BlindAlignmentBaselineLoader`` authenticates the matched input and result plus their
transitive periodic parents before adapting the pristine supercell, construction-only
hidden maps, and planted compact perturbations. Hidden values remain absent from
inference requests.

``BlindAlignmentObservationConstructor`` builds the declared synthetic candidate,
anchor covariance, retained-subspace overlap, and exterior energy anchor while
returning authored map, perturbation, and scalar shift in the separate
``BlindAlignmentHiddenTruth`` record. Only the observation is admissible as an
inference request.

``BlindAlignmentInferenceEvaluator`` receives successful inference and the separately
held truth only after inference. It reports phase-quotiented map error, scalar-shift
error, extraction error, onsite-model residuals, active-sector spectral diagnostics,
and canonical matrix identities as distinct channels.

The strict result decoder maps every retained version-one section into closed immutable
records. The canonical serializer reproduces the sorted, two-space-indented UTF-8
format, and the correlator reports semantic and byte identity without making a
numerical-verification claim. ``BlindAlignmentCaseExecutionActionizer`` passes only the
observation to inference and evaluates hidden truth only after success. The complete
``BlindAlignmentCampaignWorkflow`` composes exact, noise, gauge, stopping, conditioning,
angle, rank, spin, and energy-anchor cases into the typed result. The façade's
``verify_retained`` route delegates to an independent verifier that authenticates
sources and reconstructs all 34 retained case and diagnostic records without importing
the maintained Workflow, construction, inference, case-execution, or evaluation
implementations.

The inference core does not discover an authored map, infer geometry or units, or
perform post hoc campaign acceptance. Independent agreement is numerical verification
of this bounded synthetic campaign, not material validation or uncertainty
quantification.

.. currentmodule:: ksdft2effmass.campaigns.periodic_1d.defects.blind_alignment

.. autoclass:: BlindAlignmentEncodedDocuments
   :members:

.. autoclass:: BlindAlignmentCampaign
   :members:

Periodic-1D independent-route reconciliation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The maintained public route exports only ``RouteReconciliationCampaign`` and
``RouteReconciliationEncodedDocuments`` from
``ksdft2effmass.campaigns.periodic_1d.defects.route_reconciliation``. The document
owner stores exact version-one input and retained-result bytes only. Campaign
operations receive an explicit absolute filesystem root for authenticated source
loading. The façade delegates calculation, retained identity correlation, and
independent verification.

``RealSpaceExtractionActionizer`` assembles and subtracts the finite twisted
supercell directly in site coordinates. ``BlochFiberExtractionActionizer`` separately
evaluates primitive Bloch fibers and the discrete folding transform; neither route
invokes the other. The campaign preserves route-representation, alignment,
truncation, quadrature, spectral, eigenspace, and operator-commutativity channels
separately. Domain, quadrature, and alignment mismatches stop rather than being
silently coerced, while common-parent, common-domain, explicit-dual/metric, and
relative-unitary records represent only explicitly declared reconciliations.

The retained correlator reproduces canonical bytes under retained provenance but makes
no numerical claim. ``verify_retained`` uses a separate implementation that imports no
maintained Workflow or route Actionizer, authenticates the three retained source
identities, and reconstructs all 15 nominal, adversarial, and reconciliation records.
This is bounded synthetic software and numerical verification, not evidence for
silicon, continuum convergence, scientific validation, or uncertainty quantification.

.. currentmodule:: ksdft2effmass.campaigns.periodic_1d.defects.route_reconciliation

.. autoclass:: RouteReconciliationEncodedDocuments
   :members:

.. autoclass:: RouteReconciliationCampaign
   :members:

Periodic-1D finite-rank oracle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``FiniteRankOracleCampaign`` and ``FiniteRankOracleEncodedDocuments`` form the narrow
public route under ``periodic_1d.defects.finite_rank_oracle``. The document owner stores
exact input and retained-result bytes only. Campaign operations receive an explicit
absolute filesystem root and authenticate the periodic parent, matched-extraction
result, and route-reconciliation result before
comparing a rank-one Bloch-resolvent root with an independently assembled site-space
eigensolution. It retains 20 attractive controls plus zero-coupling, repulsive,
spin-degenerate, and unequal-rank boundaries.

Canonical correlation reproduces the retained document without making a numerical
claim. The separate verifier imports no maintained Workflow, independently rebuilds
all 24 records, and reports source, structural, and numerical channels. This evidence
concerns finite represented synthetic operators only; it does not establish an
infinite-system limit, continuum convergence, silicon behavior, scientific validation,
or uncertainty quantification.

.. currentmodule:: ksdft2effmass.campaigns.periodic_1d.defects.finite_rank_oracle

.. autoclass:: FiniteRankOracleEncodedDocuments
   :members:

.. autoclass:: FiniteRankOracleCampaign
   :members:

Periodic-1D separated continuum refinement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``ContinuumRefinementCampaign`` and ``ContinuumRefinementEncodedDocuments`` form the
narrow public route under ``periodic_1d.defects.continuum_refinement``. The document
owner stores exact version-one input and result bytes only. Correlation and verification
receive an explicit absolute filesystem root for three authenticated sources without
re-exporting lower-level numerical owners.

The maintained Workflow evaluates continuum mesh, continuum domain, lattice
supercell, lattice scale, and profile family as distinct axes. It does not relabel
profile broadening as lattice refinement or combine discretization, finite-domain,
periodic-image, lattice-scale, profile-model, operator, spectral, and state errors.
The verifier independently reconstructs 31 records and reports source, structural,
and numerical channels. Under the frozen tested controls the lattice-scale sequence
has a persistent bounded pass, while neither profile-width family establishes a
profile-defined continuum crossover over the tested domain. This is not an asymptotic
theorem, material validation, transferability evidence, or uncertainty quantification.

.. currentmodule:: ksdft2effmass.campaigns.periodic_1d.defects.continuum_refinement

.. autoclass:: ContinuumRefinementEncodedDocuments
   :members:

.. autoclass:: ContinuumRefinementCampaign
   :members:

.. currentmodule:: ksdft2effmass.campaigns.periodic_1d

Encoded documents and retained campaign operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``Periodic1DIsolatedBandEncodedDocuments``,
``Periodic1DCompositeEncodedDocuments``, and
``Periodic1DReductionChallengeEncodedDocuments`` own exact version-one input and
result bytes.  They are campaign-owned encoded documents, not physical models,
retained spaces, or operators.  The reduction-challenge name describes the current
campaign's tests of potential, discretization, band-isolation, gauge, hopping-range,
and fitting-route assumptions; it does not denote mechanical stress.

``Periodic1DIsolatedBandCampaign``, ``Periodic1DCompositeCampaign``, and the currently
named ``Periodic1DStressCampaign`` consume those documents.  Their correlators
deserialize, bind, and validate related input and result payloads without performing a
statistical correlation or making a numerical claim.  Their verifiers apply explicit
tolerance policy and return independent reconstruction diagnostics. The campaign
classes do not discover files, execute calculations, promote
unavailable channels into evidence, or establish material validation or uncertainty
quantification.

``Periodic1DWannier90Integration`` remains a separate integration boundary.
``Periodic1DWannier90EncodedDocuments`` owns exact composite input and result bytes
plus the result-document variant. Explicitly supplied native artifact groups remain
separate typed integration inputs. Wannier90 correlation does not require native
artifacts, while native verification requires complete artifact groups.

.. autoclass:: Periodic1DIsolatedBandCampaign
   :members:

.. autoclass:: Periodic1DIsolatedBandEncodedDocuments
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignCorrelator
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignCorrelationRequest
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignCorrelationResult
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignVerifier
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignVerificationRequest
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignVerificationResult
   :members:

.. autoclass:: Periodic1DCompositeCampaign
   :members:

.. autoclass:: Periodic1DCompositeEncodedDocuments
   :members:

.. autoclass:: Periodic1DCompositeCampaignCorrelator
   :members:

.. autoclass:: Periodic1DCompositeCampaignCorrelationRequest
   :members:

.. autoclass:: Periodic1DCompositeCampaignCorrelationResult
   :members:

.. autoclass:: Periodic1DCompositeCampaignVerifier
   :members:

.. autoclass:: Periodic1DCompositeCampaignVerificationRequest
   :members:

.. autoclass:: Periodic1DCompositeCampaignVerificationResult
   :members:

.. autoclass:: Periodic1DStressCampaign
   :members:

.. autoclass:: Periodic1DReductionChallengeEncodedDocuments
   :members:

.. autoclass:: Periodic1DStressCampaignCorrelator
   :members:

.. autoclass:: Periodic1DStressCampaignCorrelationRequest
   :members:

.. autoclass:: Periodic1DStressCampaignCorrelationResult
   :members:

.. autoclass:: Periodic1DStressCampaignVerifier
   :members:

.. autoclass:: Periodic1DStressCampaignVerificationRequest
   :members:

.. autoclass:: Periodic1DStressCampaignVerificationResult
   :members:

.. autoclass:: Periodic1DWannier90Integration
   :members:

.. autoclass:: Periodic1DWannier90EncodedDocuments
   :members:

.. autoclass:: Periodic1DWannier90IntegrationCorrelator
   :members:

.. autoclass:: Periodic1DWannier90IntegrationCorrelationRequest
   :members:

.. autoclass:: Periodic1DWannier90IntegrationCorrelationResult
   :members:

.. autoclass:: Periodic1DWannier90IntegrationVerifier
   :members:

.. autoclass:: Periodic1DWannier90IntegrationVerificationRequest
   :members:

.. autoclass:: Periodic1DWannier90IntegrationVerificationResult
   :members:

.. autoclass:: Periodic1DCampaignJsonDecoder
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignDefinition
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignJsonSerializer
   :members:

.. autoclass:: Periodic1DStressPotentialShape
   :members:

.. autoclass:: Periodic1DStressCampaignDefinition
   :members:

.. autoclass:: Periodic1DStressCampaignJsonSerializer
   :members:

.. autoclass:: Periodic1DRetainedBandGroup
   :members:

.. autoclass:: Periodic1DCompositeCampaignDefinition
   :members:

.. autoclass:: Periodic1DCompositeCampaignJsonSerializer
   :members:

.. autoclass:: Periodic1DCompositeExternalIsolationStatus
   :members:

.. autoclass:: Periodic1DCompositeBandIsolationResult
   :members:

.. autoclass:: Periodic1DCompositeGaugeComparisonResult
   :members:

.. autoclass:: Periodic1DCompositeHoppingRangeResult
   :members:

.. autoclass:: Periodic1DCompositeDirectRouteComparisonResult
   :members:

.. autoclass:: Periodic1DCompositeArtifactIdentities
   :members:

.. autoclass:: Periodic1DCompositeHoppingRepresentationResult
   :members:

.. autoclass:: Periodic1DCompositeWilsonGroupResult
   :members:

.. autoclass:: Periodic1DCompositeBandGroupResult
   :members:

.. autoclass:: Periodic1DCompositeCampaignResult
   :members:

.. autoclass:: Periodic1DCompositeResultJsonSerializer
   :members:

.. autoclass:: Periodic1DCompositeCampaignWorkflowRequest
   :members:

.. autoclass:: Periodic1DCompositeCampaignWorkflowResult
   :members:

.. autoclass:: Periodic1DCompositeCampaignWorkflow
   :members:

Independent composite-result verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The independent composite verifier consumes the correlated read-only Workflow result
and directly reconstructs the finite Fourier pair, exact represented-opposite
Hermiticity residual, smooth and rough omitted-block norms, training-mesh eigenvalue
errors, direct least-squares route, and the three identities whose arrays were
retained.  It imports no production transform, fitting, frame, alignment, or Wilson
algorithm.  Its result explicitly lists the gaps, frame/projector identities,
controlled-gauge and alignment diagnostics, Wilson data, rough reciprocal
reconstruction, and withheld errors that cannot be reconstructed from the retained
source values.  ``Periodic1DCompositeVerifiedWorkflow`` is the supported integrated
surface: it performs retained correlation first and then returns both the correlation
and verification ResultObjects.  A pass is therefore bounded numerical verification,
not scientific validation or UQ.

.. autoclass:: Periodic1DCompositeUnavailableVerificationChannel
   :members:

.. autoclass:: Periodic1DCompositeVerificationRequest
   :members:

.. autoclass:: Periodic1DCompositeGroupVerificationResult
   :members:

.. autoclass:: Periodic1DCompositeVerificationResult
   :members:

.. autoclass:: Periodic1DCompositeResultVerifier
   :members:

.. autoclass:: Periodic1DCompositeVerifiedWorkflowRequest
   :members:

.. autoclass:: Periodic1DCompositeVerifiedWorkflowResult
   :members:

.. autoclass:: Periodic1DCompositeVerifiedWorkflow
   :members:

Retained Wannier90 and Wilson verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The verified-native Workflow authenticates caller-supplied bytes before parsing or
numerical comparison.  For each active reciprocal edge, the independent verifier
forms the unitary polar factor :math:`Q_j` of the native overlap :math:`M_j` and
constructs the ordered loop :math:`W=Q_0Q_1\cdots Q_{N_k-1}`.  A second route first
applies the retained native gauge,
:math:`M'_j=U_j^\dagger M_j U_{j+1}`.  The two unordered principal-phase
spectra and the retained spectrum are compared by circular assignment.

This convention is related to the discrete geometric-phase framework of `King-Smith
and Vanderbilt (1993) <https://doi.org/10.1103/PhysRevB.47.1651>`_ and the Wannier
function review by `Marzari et al. (2012)
<https://doi.org/10.1103/RevModPhys.84.1419>`_.  The software result is deliberately
narrower than the physical conclusions discussed there: passing verifies represented
loop assembly, gauge-route agreement, unitarity, and overlap conditioning only.  It
does not by itself establish polarization, topology, material validity, or UQ.

.. autoclass:: Periodic1DWannier90WilsonGroupResult
   :members:

.. autoclass:: Periodic1DWannier90CampaignResult
   :members:

.. autoclass:: Periodic1DWannier90ResultJsonSerializer
   :members:

.. autoclass:: Periodic1DWannier90CampaignWorkflowRequest
   :members:

.. autoclass:: Periodic1DWannier90CampaignWorkflowResult
   :members:

.. autoclass:: Periodic1DWannier90CampaignWorkflow
   :members:

.. autoclass:: Periodic1DWannier90NativeArtifactGroup
   :members:

.. autoclass:: Periodic1DWannier90NativeArtifactGroupResult
   :members:

.. autoclass:: Periodic1DWannier90NativeArtifactWorkflowRequest
   :members:

.. autoclass:: Periodic1DWannier90NativeArtifactWorkflowResult
   :members:

.. autoclass:: Periodic1DWannier90NativeArtifactWorkflow
   :members:

.. autoclass:: Periodic1DWannier90WilsonVerificationRequest
   :members:

.. autoclass:: Periodic1DWannier90WilsonGroupVerificationResult
   :members:

.. autoclass:: Periodic1DWannier90WilsonVerificationResult
   :members:

.. autoclass:: Periodic1DWannier90WilsonVerifier
   :members:

.. autoclass:: Periodic1DWannier90VerifiedNativeWorkflowRequest
   :members:

.. autoclass:: Periodic1DWannier90VerifiedNativeWorkflowResult
   :members:

.. autoclass:: Periodic1DWannier90VerifiedNativeWorkflow
   :members:

.. autoclass:: Periodic1DEncodedResultKind
   :members:

.. autoclass:: Periodic1DJsonArray
   :members:

.. autoclass:: Periodic1DJsonObject
   :members:

.. autoclass:: Periodic1DEncodedResultDocument
   :members:

.. autoclass:: Periodic1DEncodedResultJsonSerializer
   :members:

.. autoclass:: Periodic1DPlaneWaveCutoffObservation
   :members:

.. autoclass:: Periodic1DFiniteDifferenceGridObservation
   :members:

.. autoclass:: Periodic1DLowModeOperatorObservation
   :members:

.. autoclass:: Periodic1DWeakPotentialGapObservation
   :members:

.. autoclass:: Periodic1DParentRepresentationVerificationResult
   :members:

.. autoclass:: Periodic1DHoppingRangeDiagnostic
   :members:

.. autoclass:: Periodic1DParentBandObservables
   :members:

.. autoclass:: Periodic1DRetainedLocalizationResult
   :members:

.. autoclass:: Periodic1DIsolatedBandReductionResult
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignResult
   :members:

.. autoclass:: Periodic1DIsolatedBandResultJsonSerializer
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignWorkflowRequest
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignWorkflowResult
   :members:

.. autoclass:: Periodic1DIsolatedBandCampaignWorkflow
   :members:

Isolated-band diagnostic calculation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``Periodic1DIsolatedBandCalculationWorkflow`` is the supported in-process calculation
surface for the reusable nonlocalization channels demonstrated by the Appendix G
isolated-band campaign.  It calculates plane-wave cutoff studies, finite-difference
spectra, common-low-mode operator defects, Mathieu and weak-cosine references,
symmetry residuals, lowest-band reciprocal samples, the complete scalar Fourier pair,
all requested finite-range training and withheld metrics, Parseval and direct-fit route
comparisons, and parent bandwidth, boundary-gap, and center-curvature observables.
The curvature differencing step is an explicit unitless request value.  The Workflow
performs no filesystem access, external execution, gauge transport, Wannier
localization, material validation, or uncertainty quantification.

The numerical meanings and reference boundaries are:

* the plane-wave fibers are finite Galerkin matrices in increasing reciprocal-index
  order, following the standard plane-wave electronic-structure representation
  reviewed by `Payne et al. (1992)
  <https://doi.org/10.1103/RevModPhys.64.1045>`_;
* the finite-difference fibers use the centered second-order stencil and conjugate
  Bloch-seam phases, consistent with real-space finite-difference electronic-structure
  methods such as `Chelikowsky, Troullier, and Saad (1994)
  <https://doi.org/10.1103/PhysRevLett.72.1240>`_ and the truncation-error treatment of
  `Strikwerda (2004) <https://doi.org/10.1137/1.9780898717938>`_;
* low-mode operator defects are formed only after discrete Fourier transport into a
  common represented subspace; they are not differences between unidentified matrix
  spaces;
* the Mathieu oracle uses :math:`q=2V_0/E_G` and :math:`E/E_G=A/4`, following
  McLachlan's *Theory and Application of Mathieu Functions*;
* the complete hopping pair, inverse reconstruction, and finite-transform Parseval
  residual use the stated uniform-mesh Fourier convention; see `Trefethen (2000)
  <https://doi.org/10.1137/1.9780898719598>`_ and the Wannier interpolation review of
  `Marzari et al. (2012) <https://doi.org/10.1103/RevModPhys.84.1419>`_;
* direct-route coefficients solve the unconstrained complex least-squares problem in
  the same Fourier class.  Least-squares rank and conditioning are separate numerical
  concerns, as treated by Golub and Van Loan, *Matrix Computations*, fourth edition;
  and
* bandwidth, zone-boundary gap, and center curvature remain separate observables.
  The curvature-to-effective-mass interpretation belongs to a declared band-edge
  model, not automatically to this dimensionless cosine benchmark; see `Luttinger and
  Kohn (1955) <https://doi.org/10.1103/PhysRev.97.869>`_.

The implementation uses array and special-function/eigensolver operations supplied by
`NumPy <https://doi.org/10.1038/s41586-020-2649-2>`_ and
`SciPy <https://doi.org/10.1038/s41592-019-0686-2>`_.  These citations identify the
software substrate; passing the Workflow remains software/numerical verification of
the represented model rather than scientific validation.

.. autoclass:: Periodic1DIsolatedBandCalculationRequest
   :members:

.. autoclass:: Periodic1DIsolatedBandCalculationResult
   :members:

.. autoclass:: Periodic1DIsolatedBandCalculationWorkflow
   :members:

Independent isolated-band verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The isolated verifier independently assembles the dense plane-wave and periodic
finite-difference parent matrices, Mathieu and weak-gap references, complete scalar
Fourier pair, finite-range and withheld-mesh errors, Parseval residuals, direct-fit
route, and parent observables.  Ordinary energy diagnostics and the
cancellation-sensitive finite-difference center curvature use separate explicit
``Unitless`` tolerances.  Source transported frames and localization-density samples
were not retained, so their channels remain explicitly unavailable.
``Periodic1DIsolatedVerifiedWorkflow`` is the supported integrated correlation and
verification surface.

.. autoclass:: Periodic1DIsolatedUnavailableVerificationChannel
   :members:

.. autoclass:: Periodic1DIsolatedVerificationRequest
   :members:

.. autoclass:: Periodic1DIsolatedVerificationResult
   :members:

.. autoclass:: Periodic1DIsolatedResultVerifier
   :members:

.. autoclass:: Periodic1DIsolatedVerifiedWorkflowRequest
   :members:

.. autoclass:: Periodic1DIsolatedVerifiedWorkflowResult
   :members:

.. autoclass:: Periodic1DIsolatedVerifiedWorkflow
   :members:

Independent reduction-challenge verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The reduction-challenge verifier reconstructs every typed retained channel from the
correlated version-one controls without importing the campaign runner or production
plane-wave, finite-difference, frame-transport, hopping-transform, or fitting
algorithms.  It independently assembles finite plane-wave Galerkin matrices and
periodic second-difference matrices, computes centered finite Fourier coefficients
and inverse sums, includes reciprocal sewing in neighbor overlaps and scalar parallel
transport, and solves complete, restricted-domain, and nonuniform-weight complex
least-squares routes directly.

The mathematical boundaries are the same as the documented reduction-challenge
protocol:
plane-wave fibers follow the standard finite reciprocal representation reviewed by
`Payne et al. (1992) <https://doi.org/10.1103/RevModPhys.64.1045>`_; periodic
second differences use conjugate seam phases and the centered stencil described in
the finite-difference discussion above; complete hoppings use the finite Fourier
convention of `Trefethen (2000) <https://doi.org/10.1137/1.9780898719598>`_;
and route fits are ordinary complex least-squares problems in the sense of Golub and
Van Loan, *Matrix Computations*, fourth edition.  Projector invariance, aligned
transported frames, and closure holonomy are separate gauge diagnostics consistent
with the Wannier framework reviewed by `Marzari et al. (2012)
<https://doi.org/10.1103/RevModPhys.84.1419>`_.

One inclusive ``Unitless`` tolerance is applied separately to the amplitude, shape,
mesh/band/isolation, gauge-covariance, and fitting-route maximum defects.
``Periodic1DStressVerifiedWorkflow`` is the supported integrated surface and preserves
retained correlation separately from numerical verification.  A pass is bounded
numerical verification of the represented illustrative campaign, not material
validation, topology or polarization evidence, UQ, or protected execution.

.. autoclass:: Periodic1DStressDiscretizationObservation
   :members:

.. autoclass:: Periodic1DPotentialAmplitudeStressResult
   :members:

.. autoclass:: Periodic1DMeshBandIsolationStressResult
   :members:

.. autoclass:: Periodic1DPotentialShapeStressCase
   :members:

.. autoclass:: Periodic1DPotentialShapeStressResult
   :members:

.. autoclass:: Periodic1DGaugeCovarianceStressResult
   :members:

.. autoclass:: Periodic1DRouteAssumptionStressResult
   :members:

.. autoclass:: Periodic1DStressCampaignResult
   :members:

.. autoclass:: Periodic1DStressResultJsonSerializer
   :members:

.. autoclass:: Periodic1DStressCampaignWorkflowRequest
   :members:

.. autoclass:: Periodic1DStressCampaignWorkflowResult
   :members:

.. autoclass:: Periodic1DStressCampaignWorkflow
   :members:

.. autoclass:: Periodic1DStressVerificationRequest
   :members:

.. autoclass:: Periodic1DStressVerificationResult
   :members:

.. autoclass:: Periodic1DStressResultVerifier
   :members:

.. autoclass:: Periodic1DStressVerifiedWorkflowRequest
   :members:

.. autoclass:: Periodic1DStressVerifiedWorkflowResult
   :members:

.. autoclass:: Periodic1DStressVerifiedWorkflow
   :members:

.. autoclass:: Periodic1DHoppingReductionRequest
   :members:

.. autoclass:: Periodic1DHoppingReductionResult
   :members:

.. autoclass:: Periodic1DHoppingReductionWorkflow
   :members:

QHO1D controlled campaign
-------------------------

The canonical public package is ``ksdft2effmass.campaigns.qho1d``. The former
``ksdft2effmass.campaigns.research_monograph.harmonic_oscillator`` import façade is
deprecated; it re-exports the same public objects and emits
:class:`DeprecationWarning`.

The Appendix E campaign deserializes its closed version-one input, evaluates the
ordered Cartesian product of interval half-width, grid spacing, and retained
dimension, and serializes the resulting comparisons with explicit source identities.
The mathematical models, common-coordinate map, campaign ownership, and retained
artifact boundary are described in
:doc:`../concepts/controlled-model-calculations`.
The retained historical result remains bound to its original runner identity.  Newly
authored records bind the current public model-system and campaign implementation
sources; this does not relabel historical evidence.

.. currentmodule:: ksdft2effmass.campaigns.qho1d

.. autoclass:: HarmonicOscillatorStudyDefinition
   :members:

.. autoclass:: HarmonicOscillatorStudyResult
   :members:

.. autoclass:: HarmonicOscillatorStudyInputDeserializer
   :members:

.. autoclass:: HarmonicOscillatorStudyEvaluator
   :members:

.. autoclass:: HarmonicOscillatorStudyResultSerializer
   :members:

.. autoclass:: HarmonicOscillatorResultVerifier
   :members:

Defect-2D finite-domain case inventory
--------------------------------------

The execution-free defect-2D case contracts retain separate area, fixed-area shape,
orientation, and boundary-phase memberships. Deterministic enumeration shares common
isotropic geometry evaluations and represents each orientation comparison as three
future operator evaluations. The version-one serializer retains the complete study
definition, exact nonpooled channel order, explicit non-execution status, case counts,
and a SHA-256 identity of all deterministically enumerated case content. Deserialization
reconstructs and authenticates that inventory. The planning Workflow composes only
definition validation, deterministic enumeration, and canonical serialization; its
ResultObject correlates the exact inventory and plan bytes. It does not construct
operators, consume accepted-parent results, or authorize the 2,430 proposed
evaluations.

.. currentmodule:: ksdft2effmass.campaigns.research_monograph.impurity_defect_2d

.. autoclass:: FiniteDomainChannel
   :members:

.. autoclass:: FiniteDomainEffectsStudyDefinition
   :members:

.. autoclass:: IsotropicFiniteDomainCase
   :members:

.. autoclass:: OrientationFiniteDomainCase
   :members:

.. autoclass:: FiniteDomainEffectsCaseInventory
   :members:

.. autoclass:: FiniteDomainEffectsCaseEnumerator
   :members:

.. autoclass:: FiniteDomainEffectsCaseInventoryJsonSerializer
   :members:

.. autoclass:: FiniteDomainEffectsCampaignPlanResult
   :members:

.. autoclass:: FiniteDomainEffectsCampaignPlanningWorkflow
   :members:

PIAB1D controlled campaigns
---------------------------

The public package is ``ksdft2effmass.campaigns.piab1d``. PIAB1D campaign objects are
not re-exported through ``ksdft2effmass.campaigns.research_monograph``.

.. currentmodule:: ksdft2effmass.campaigns.piab1d

The Appendix D core residual campaign deserializes its retained version-one input,
composes the public one-dimensional box and represented-operator contracts, preserves
the historical numerical JSON payload, and verifies retained or newly authored
provenance without importing the implementation under verification. The core verifier
returns a typed report that keeps source-identity authentication, independent numerical
reconstruction, and aggregate disposition separate. Historical runner admission is
reported distinctly from equality with currently available repository bytes, and
verification counts are derived from retained result collections. The reconstruction
uses the represented dimensionless box length in both discrete and continuum scales;
a maintained synthetic ``L=2`` case verifies that the unit-length retained fixture is
not an implicit implementation assumption. The convergence verifier likewise reports
source authentication separately from six aggregate numerical channels. Its
refinement and reconstructed mode-observation counts come from decoded collections,
not fixed campaign constants. The full-spectrum and fixed-mode eigenpair verifier
separately authenticates sources, reconstructs 14 numerical channels, and derives its
grid, eigenpair, and fixed-mode-series counts from decoded collections. Its reported
energy relation is checked directly; the retained relative-error roundoff envelope is
compatibility policy, not an eigensolver error theorem. Public Workflows also own the
convergence, eigenpair-sweep, norm, and identifiability campaigns while
calculation-directory runners and verifiers remain thin CLI adapters. Detailed source,
core-result, convergence, and eigenpair-sweep verifier contracts are organized under
:doc:`ksdft2effmass/campaigns/piab1d/verification/index`.

.. autoclass:: Piab1dStudyDefinition
   :members:

.. autoclass:: Piab1dResidualStudyResult
   :members:

.. autoclass:: Piab1dStudyInputDeserializer
   :members:

.. autoclass:: Piab1dResidualStudyEvaluator
   :members:

.. autoclass:: Piab1dStudyResultSerializer
   :members:

.. autoclass:: Piab1dConvergenceWorkflow
   :members:

.. autoclass:: Piab1dEigenpairSweepWorkflow
   :members:

.. autoclass:: Piab1dNormSweepWorkflow
   :members:

.. autoclass:: Piab1dNormSweepResultsVerifier
   :members:

.. autoclass:: RetainedModelClassFitResult
   :members:

.. autoclass:: RetainedModelClassFitter
   :members:

.. autoclass:: Piab1dIdentifiabilityWorkflow
   :members:

.. autoclass:: Piab1dIdentifiabilityResultsVerifier
   :members:
