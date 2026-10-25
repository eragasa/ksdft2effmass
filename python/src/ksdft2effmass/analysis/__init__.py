"""Public calculator-independent scientific-analysis contracts.

The package root exports scalar quantities of interest and calculated DFT reference
targets. Model definitions and finite representations are owned separately by
:mod:`ksdft2effmass.model_systems`; analysis consumes them rather than owning them.
Other comparison algorithms and parameter-study contracts remain under active
development and are not exported here.
"""

from .convergence import (
    ObservedConvergenceOrder,
    ObservedConvergenceOrderEstimator,
    ObservedConvergenceOrderResult,
    RelativeErrorConvergenceAnalyzer,
    RelativeErrorConvergenceResult,
)
from .diagnostics import (
    BaseDiagnosticAnalyzer,
    DiagnosticObservation,
    MatrixNormDiagnosticOptions,
)
from .probability_selection import TailProbabilitySelection, TailProbabilitySelector
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
from .verification import (
    DiagnosticVerification,
    EigensystemVerification,
    KineticPotentialDecompositionVerification,
    RelativeErrorConvergenceVerification,
    TailProbabilitySelectionVerification,
)

__all__ = [
    "BaseDiagnosticAnalyzer",
    "DiagnosticObservation",
    "DiagnosticVerification",
    "DftReferenceCalculationIdentity",
    "DftReferenceCalculatorIdentity",
    "DftReferenceMethodIdentity",
    "DftScalarQuantityOfInterestReferenceTarget",
    "EigensystemVerification",
    "KineticPotentialDecompositionVerification",
    "MatrixNormDiagnosticOptions",
    "NormalizedObservationRequirementIdentity",
    "ObservedConvergenceOrder",
    "ObservedConvergenceOrderEstimator",
    "ObservedConvergenceOrderResult",
    "RelativeErrorConvergenceAnalyzer",
    "RelativeErrorConvergenceResult",
    "RelativeErrorConvergenceVerification",
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
    "TailProbabilitySelection",
    "TailProbabilitySelector",
    "TailProbabilitySelectionVerification",
]
