Research-monograph campaigns
=============================

``ksdft2effmass.campaigns.research_monograph`` contains public composition and
retained-format contracts for the project's research-monograph calculations.  These
campaign objects bind exact study controls to reusable analysis contracts.  They do
not own generic scientific algorithms, grant protected execution authority, or decide
scientific acceptance.  Campaign implementation classes and methods are public and
use no underscore-prefixed implementation names; Python-required special methods are
the only exception.

Periodic-1D hopping reduction
-----------------------------

The versioned Appendix G Workflow composes complete uniform-mesh Fourier transform,
symmetric truncation, Parseval analysis, explicit-weight least-squares fitting, and
withheld-coordinate route comparison. The read-only composite Workflow binds retained
gaps, dense reciprocal Hamiltonians, complete smooth- and rough-gauge hopping blocks,
gauge and alignment defects, range studies, direct-route comparisons, Wilson spectra,
and intermediate-array identities to the exact campaign input.  These channels remain
separate: in particular, an unaligned gauge-dependent hopping defect is not a
basis-aligned operator error, and training errors are not withheld-mesh errors.
Wannier90 Workflows separately bind retained Wilson spectra and circular center
comparisons to exact inputs. Historical calculation scripts remain frozen and are
deprecated for new execution; these Workflows perform no filesystem discovery or
external Wannier90 operation.

.. currentmodule:: ksdft2effmass.campaigns.research_monograph

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

.. autoclass:: Periodic1DRetainedResultKind
   :members:

.. autoclass:: Periodic1DJsonArray
   :members:

.. autoclass:: Periodic1DJsonObject
   :members:

.. autoclass:: Periodic1DRetainedResultDocument
   :members:

.. autoclass:: Periodic1DRetainedResultJsonSerializer
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

.. autoclass:: Periodic1DHoppingReductionRequest
   :members:

.. autoclass:: Periodic1DHoppingReductionResult
   :members:

.. autoclass:: Periodic1DHoppingReductionWorkflow
   :members:

Harmonic-oscillator study
-------------------------

The Appendix E campaign deserializes its closed version-one input, evaluates the
ordered Cartesian product of interval half-width, grid spacing, and retained
dimension, and serializes the resulting comparisons with explicit source identities.
The retained historical result remains bound to its original runner identity.  Newly
authored records bind the current public model-system and campaign implementation
sources; this does not relabel historical evidence.

.. currentmodule:: ksdft2effmass.campaigns.research_monograph

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

.. currentmodule:: ksdft2effmass.campaigns.research_monograph

Particle-in-a-box residual study
--------------------------------

The Appendix D core residual campaign deserializes its retained version-one input,
composes the public one-dimensional box and represented-operator contracts, preserves
the historical numerical JSON payload, and verifies retained or newly authored
provenance without importing the implementation under verification. Public Workflows
also own the convergence, higher-eigenpair, norm, and identifiability campaigns while
calculation-directory runners and verifiers remain thin CLI adapters.

.. autoclass:: ParticleInBoxStudyDefinition
   :members:

.. autoclass:: ParticleInBoxResidualStudyResult
   :members:

.. autoclass:: ParticleInBoxStudyInputDeserializer
   :members:

.. autoclass:: ParticleInBoxResidualStudyEvaluator
   :members:

.. autoclass:: ParticleInBoxStudyResultSerializer
   :members:

.. autoclass:: ParticleInBoxResultVerifier
   :members:

.. autoclass:: ParticleInBoxConvergenceWorkflow
   :members:

.. autoclass:: ParticleInBoxConvergenceVerifier
   :members:

.. autoclass:: ParticleInBoxEigenpairSweepWorkflow
   :members:

.. autoclass:: ParticleInBoxEigenpairSweepVerifier
   :members:

.. autoclass:: ParticleInBoxNormSweepWorkflow
   :members:

.. autoclass:: ParticleInBoxNormSweepVerifier
   :members:

.. autoclass:: RetainedModelClassFitResult
   :members:

.. autoclass:: RetainedModelClassFitter
   :members:

.. autoclass:: ParticleInBoxIdentifiabilityWorkflow
   :members:

.. autoclass:: ParticleInBoxIdentifiabilityVerifier
   :members:
