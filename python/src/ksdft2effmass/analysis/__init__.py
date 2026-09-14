"""Public calculator-independent scientific-analysis contracts.

The initial supported surface defines scalar quantities of interest and calculated DFT
reference targets.  Comparison algorithms and parameter-study contracts remain under
active internal development and are not exported here.
"""

from .qoi import (
    DftReferenceCalculationIdentity,
    DftReferenceCalculatorIdentity,
    DftReferenceMethodIdentity,
    DftScalarQuantityOfInterestReferenceTarget,
    NormalizedObservationRequirementIdentity,
    QuantityOfInterestCompleteness,
    QuantityOfInterestConventionIdentity,
    QuantityOfInterestEvaluationFailureCode,
    QuantityOfInterestEvaluatorIdentity,
    QuantityOfInterestIdentity,
    QuantityOfInterestReferenceAssessmentIdentity,
    QuantityOfInterestReferenceTargetIdentity,
    QuantityOfInterestStateSpaceIdentity,
    QuantityOfInterestSubjectIdentity,
    ScalarQuantityOfInterestDefinition,
    ScalarQuantityOfInterestEvaluationFailure,
    ScalarQuantityOfInterestEvaluationResult,
    ScalarQuantityOfInterestValue,
)

__all__ = [
    "DftReferenceCalculationIdentity",
    "DftReferenceCalculatorIdentity",
    "DftReferenceMethodIdentity",
    "DftScalarQuantityOfInterestReferenceTarget",
    "NormalizedObservationRequirementIdentity",
    "QuantityOfInterestCompleteness",
    "QuantityOfInterestConventionIdentity",
    "QuantityOfInterestEvaluationFailureCode",
    "QuantityOfInterestEvaluatorIdentity",
    "QuantityOfInterestIdentity",
    "QuantityOfInterestReferenceAssessmentIdentity",
    "QuantityOfInterestReferenceTargetIdentity",
    "QuantityOfInterestStateSpaceIdentity",
    "QuantityOfInterestSubjectIdentity",
    "ScalarQuantityOfInterestDefinition",
    "ScalarQuantityOfInterestEvaluationFailure",
    "ScalarQuantityOfInterestEvaluationResult",
    "ScalarQuantityOfInterestValue",
]
