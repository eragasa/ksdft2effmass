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
