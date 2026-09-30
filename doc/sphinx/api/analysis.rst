Scientific analysis
===================

Use the supported package-level imports shown below. The initial public analysis
package-root surface represents scalar quantities of interest (QoIs) and calculated
DFT reference targets. It performs no evaluation, comparison, fitting, calculator
execution, or scientific acceptance. Public domain analyses are documented separately;
see :doc:`model-systems`.

.. currentmodule:: ksdft2effmass.analysis

Observed numerical order
------------------------

These records and actions compute adjacent-level observed orders for one declared
positive error sequence. They do not by themselves establish convergence or scientific
acceptance.

.. autoclass:: ObservedConvergenceOrder
   :members:

.. autoclass:: ObservedConvergenceOrderResult
   :members:

.. autoclass:: ObservedConvergenceOrderEstimator
   :members:

Periodic band paths
-------------------

Periodic-band analyses retain explicit reciprocal coordinates and energy units.
``BandGapAnalyzer1D`` reports internal and external sampled direct gaps separately and
applies no isolation threshold. ``BandApproximationErrorAnalyzer1D`` compares ordered
Hermitian eigenvalues on one declared sample set; training and withheld meshes remain
separate calls and results.

.. currentmodule:: ksdft2effmass.analysis.periodic_bands

.. autoclass:: BandSpectrumSamples1D
   :members:

.. autoclass:: ContiguousBandSelection
   :members:

.. autoclass:: BandGapResult1D
   :members:

.. autoclass:: BandGapAnalyzer1D
   :members:

.. autoclass:: BandApproximationErrorResult1D
   :members:

.. autoclass:: BandApproximationErrorAnalyzer1D
   :members:

Hopping fitting and route comparison
------------------------------------

Weighted least-squares fitting consumes explicit positive sample weights and retains
design rank, condition number, identification status, and training residuals. Complete
uniform, weighted, and incomplete sample sets therefore remain distinct inputs and
results. Route comparison reports coefficient-space and sampled reciprocal-operator
Frobenius defects separately.

.. currentmodule:: ksdft2effmass.analysis.hopping_fits

.. autoclass:: BlockHoppingLeastSquaresFitResult1D
   :members:

.. autoclass:: BlockHoppingLeastSquaresFitter1D
   :members:

.. autoclass:: BlockHoppingModelComparisonResult1D
   :members:

.. autoclass:: BlockHoppingModelComparator1D
   :members:

Hopping Hermiticity
-------------------

Block-Hermiticity analysis checks ``T[-R] = T[R]^dagger`` while retaining pairing
coverage. A Born--von Karman representative modulus is explicit: without it, a
centered even-mesh Nyquist representative is not silently treated as self-opposite.

.. currentmodule:: ksdft2effmass.analysis.hopping_diagnostics

.. autoclass:: BlockHoppingHermiticityResult1D
   :members:

.. autoclass:: BlockHoppingHermiticityAnalyzer1D
   :members:

Complete-mesh Parseval analysis keeps the reciprocal training residual and omitted
block norm explicit and checks their discrete-Fourier scaling in squared energy units.

.. autoclass:: HoppingParsevalResult1D
   :members:

.. autoclass:: HoppingParsevalAnalyzer1D
   :members:

For scalar hopping blocks, band-shape analysis reports sampled bandwidth, analytical
zone-center curvature with respect to reduced reciprocal coordinate, and an independent
imaginary residual.

.. autoclass:: ScalarHoppingBandShapeResult1D
   :members:

.. autoclass:: ScalarHoppingBandShapeAnalyzer1D
   :members:

Isolated-band finite-supercell localization
-------------------------------------------

The localization analyzer evaluates the finite Born--von Karman inverse Bloch
transform of one rank-one plane-wave frame path. It retains the normalized sampled
density, quadrature norm, center and spread on an explicit centered coordinate branch,
and the SHA-256 identity of little-endian binary64 density values. These are finite-
supercell diagnostics, not branch-independent polarization observables.

.. currentmodule:: ksdft2effmass.analysis.wannier_localization

.. autoclass:: BornVonKarmanLocalizationResult1D
   :members:

.. autoclass:: BornVonKarmanLocalizationAnalyzer1D
   :members:

Finite-domain channels
----------------------

The finite-domain ResultObjects retain one identified scalar metric at a time. Measure,
fixed-measure shape, orientation, and boundary-phase channels remain separate. They do
not pool convergence status, construct operators, enumerate a campaign, or execute a
calculation.

.. currentmodule:: ksdft2effmass.analysis.finite_domains

.. autoclass:: FiniteDomainScalarMetric
   :members:

.. autoclass:: FiniteDomainMeasureStudyResult
   :members:

.. autoclass:: FiniteDomainShapeStudyResult
   :members:

.. autoclass:: FiniteDomainOrientationStudyResult
   :members:

.. autoclass:: BoundaryPhaseStudyResult
   :members:

Finite-domain locality diagnostics
----------------------------------

Minimum-image locality uses an explicitly named Chebyshev metric. Sparse residual
analysis reports global maximum and Frobenius values, core and exterior blocks,
combined bidirectional core--exterior coupling, and a nonoverlapping row-shell
Frobenius decomposition. It does not assign physical locality or convergence status.

.. currentmodule:: ksdft2effmass.analysis.finite_domain_locality

.. autoclass:: MinimumImageChebyshevPartition
   :members:

.. autoclass:: MinimumImageChebyshevPartitioner
   :members:

.. autoclass:: SparseLocalityResidualResult
   :members:

.. autoclass:: SparseLocalityResidualAnalyzer
   :members:

Finite-domain spectral diagnostics
----------------------------------

Host-edge diagnostics consume retained lowest complex-Hermitian eigenpairs only through
a correlated passing algebraic-residual result. They retain an explicit energy
threshold and distinguish a complete below-edge count from a
truncated selected window. Algebraic eigenpair residual analysis belongs to
:mod:`ksdft2effmass.operators`; neither surface solves an eigensystem.

.. currentmodule:: ksdft2effmass.analysis.finite_domain_spectra

.. autoclass:: HostEdgeReference
   :members:

.. autoclass:: BoundStateSelectionStatus
   :members:

.. autoclass:: HostEdgeBoundStateResult
   :members:

.. autoclass:: HostEdgeBoundStateAnalyzer
   :members:

Complete bound-subspace localization
------------------------------------

Projector construction requires complete below-edge spectral coverage. Localization
uses the normalized projector diagonal, so unitary mixing within a degenerate bound
subspace does not change site probabilities, core probability, IPR, or axis RMS radii
reported in lattice-coordinate index units.
A complete no-bound-state outcome retains unavailable metrics rather than numeric zeros.

.. currentmodule:: ksdft2effmass.analysis.bound_subspaces

.. autoclass:: BoundStateProjectorResult
   :members:

.. autoclass:: BoundStateProjectorConstructor
   :members:

.. autoclass:: BoundSubspaceLocalizationResult
   :members:

.. autoclass:: BoundSubspaceLocalizationAnalyzer
   :members:

.. currentmodule:: ksdft2effmass.analysis

QoI definition
--------------

.. autoclass:: QuantityOfInterestIdentity
.. autoclass:: QuantityOfInterestSubjectIdentity
.. autoclass:: QuantityOfInterestStateSpaceIdentity
.. autoclass:: QuantityOfInterestConventionIdentity
.. autoclass:: QuantityOfInterestEvaluatorIdentity
.. autoclass:: NormalizedObservationRequirementIdentity
.. autoclass:: QuantityOfInterestCompleteness
.. autoclass:: ScalarQuantityOfInterestDefinition

QoI evaluation results
----------------------

``ScalarQuantityOfInterestEvaluationResult`` is the closed union of the successful
value and failure records below.

.. autoclass:: ScalarQuantityOfInterestValue
   :members:
.. autoclass:: QuantityOfInterestEvaluationFailureCode
   :members:
.. autoclass:: ScalarQuantityOfInterestEvaluationFailure

Scalar result-value codec
-------------------------

``QuantityOfInterestResultValueSerializer`` implements the injected Workflow codec
port for the two exact scalar result classes, not DFT reference targets or arbitrary
``ResultObject`` implementations. It preserves complete definitions and correlations
in ``qoi-result-value:1`` without evaluation, conversion or native I/O. See
:doc:`../concepts/workflow-run-persistence` for the wire and failure boundary.

.. autoclass:: QuantityOfInterestResultValueSerializer
   :members:

DFT reference target
--------------------

.. autoclass:: QuantityOfInterestReferenceTargetIdentity
.. autoclass:: DftReferenceCalculationIdentity
.. autoclass:: DftReferenceCalculatorIdentity
.. autoclass:: DftReferenceMethodIdentity
.. autoclass:: QuantityOfInterestReferenceAssessmentIdentity
.. autoclass:: DftScalarQuantityOfInterestReferenceTarget
