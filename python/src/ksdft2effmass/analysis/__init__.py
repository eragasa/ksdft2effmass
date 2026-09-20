"""Public calculator-independent scientific-analysis contracts.

The package root exports scalar quantities of interest and calculated DFT reference
targets. Public domain subpackages, including
:mod:`ksdft2effmass.analysis.model_systems`, own additional documented scientific
analyses without flattening their names into this
package root. Other comparison algorithms and parameter-study contracts remain under
active development and are not exported here.
"""

from .convergence import (
    ObservedConvergenceOrder,
    ObservedConvergenceOrderEstimator,
    ObservedConvergenceOrderResult,
)
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
from .result_values import QuantityOfInterestResultValueSerializer

__all__ = [
    "DftReferenceCalculationIdentity",
    "DftReferenceCalculatorIdentity",
    "DftReferenceMethodIdentity",
    "DftScalarQuantityOfInterestReferenceTarget",
    "NormalizedObservationRequirementIdentity",
    "ObservedConvergenceOrder",
    "ObservedConvergenceOrderEstimator",
    "ObservedConvergenceOrderResult",
    "QuantityOfInterestCompleteness",
    "QuantityOfInterestConventionIdentity",
    "QuantityOfInterestEvaluationFailureCode",
    "QuantityOfInterestEvaluatorIdentity",
    "QuantityOfInterestIdentity",
    "QuantityOfInterestReferenceAssessmentIdentity",
    "QuantityOfInterestReferenceTargetIdentity",
    "QuantityOfInterestResultValueSerializer",
    "QuantityOfInterestStateSpaceIdentity",
    "QuantityOfInterestSubjectIdentity",
    "ScalarQuantityOfInterestDefinition",
    "ScalarQuantityOfInterestEvaluationFailure",
    "ScalarQuantityOfInterestEvaluationResult",
    "ScalarQuantityOfInterestValue",
]
