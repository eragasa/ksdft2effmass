Scientific analysis
===================

Use the supported package-level imports shown below. The initial public analysis
surface represents scalar quantities of interest (QoIs) and calculated DFT reference
targets. It performs no evaluation, comparison, fitting, calculator execution, or
scientific acceptance.

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
