"""Public three-model analysis of the one-dimensional quantum harmonic oscillator.

``QHO1D`` is dimension-specific. No dimension-neutral ``QHO`` API is claimed.
The supported surface binds an exact analytical model, a bounded uniform-grid
Dirichlet model, and a retained ladder-operator model. An explicit injection places
the Dirichlet Hamiltonian and ladder Hamiltonian in the same ordered coordinates.
The comparison separates represented finite operators from the continuum differential
operator and makes no semiconductor-validation claim.
"""

from .analysis import Qho1dAnalyzer
from .comparison import Qho1dComparator
from .configuration import Qho1dConfiguration
from .model import (
    Qho1dAnalytical,
    Qho1dComparisonRequest,
    Qho1dComparisonResult,
    Qho1dFiniteDifference,
    Qho1dLadderOperators,
    Qho1dNondimensionalizer,
    Qho1dParameters,
)
from .result import (
    Qho1dCalculationResult,
    Qho1dCaseResult,
    Qho1dStateComparisonResult,
)
from .study import (
    Qho1dResultVerifier,
    Qho1dStudyDefinition,
    Qho1dStudyEvaluator,
    Qho1dStudyInputDeserializer,
    Qho1dStudyResult,
    Qho1dStudyResultSerializer,
)
from .verification import Qho1dIndependentReferenceAnalyzer, Qho1dVerifier
from .verification_values import (
    Qho1dStateComparisonVerification,
    Qho1dSweepVerification,
    Qho1dVerification,
)
from .visualization import (
    Qho1dVisualizationData,
    Qho1dVisualizationPlotEnum,
    Qho1dVisualizer,
)

__all__ = [
    "Qho1dAnalytical",
    "Qho1dAnalyzer",
    "Qho1dCalculationResult",
    "Qho1dCaseResult",
    "Qho1dComparator",
    "Qho1dComparisonRequest",
    "Qho1dComparisonResult",
    "Qho1dConfiguration",
    "Qho1dFiniteDifference",
    "Qho1dIndependentReferenceAnalyzer",
    "Qho1dLadderOperators",
    "Qho1dNondimensionalizer",
    "Qho1dParameters",
    "Qho1dResultVerifier",
    "Qho1dStudyDefinition",
    "Qho1dStudyEvaluator",
    "Qho1dStudyInputDeserializer",
    "Qho1dStateComparisonResult",
    "Qho1dStateComparisonVerification",
    "Qho1dStudyResult",
    "Qho1dStudyResultSerializer",
    "Qho1dSweepVerification",
    "Qho1dVerification",
    "Qho1dVerifier",
    "Qho1dVisualizationData",
    "Qho1dVisualizationPlotEnum",
    "Qho1dVisualizer",
]
