"""Public three-model analysis of the one-dimensional quantum harmonic oscillator.

``QHO1D`` is dimension-specific. No dimension-neutral ``QHO`` API is claimed.
The supported surface binds an exact analytical model, a bounded uniform-grid
Dirichlet model, and a retained ladder-operator model. An explicit injection places
the Dirichlet Hamiltonian and ladder Hamiltonian in the same ordered coordinates.
The comparison separates represented finite operators from the continuum differential
operator and makes no semiconductor-validation claim.
"""

from .analysis import Qho1dAnalysisRequest, Qho1dAnalyzer
from .analytical import Qho1dAnalytical
from .case_sections import (
    Qho1dHamiltonianComparisonResult,
    Qho1dResidualResult,
    Qho1dSampledStateAlignmentResult,
    Qho1dSpatialRepresentationResult,
)
from .comparison import Qho1dComparator
from .comparison_records import Qho1dComparisonRequest, Qho1dComparisonResult
from .configuration import Qho1dConfiguration
from .cross_grid import (
    Qho1dCrossGridAnalysisRequest,
    Qho1dCrossGridAnalysisResult,
    Qho1dCrossGridAnalyzer,
    Qho1dCrossGridComparisonResult,
    Qho1dCrossGridVerification,
    Qho1dCrossGridVerificationRequest,
    Qho1dCrossGridVerifier,
)
from .finite_difference import Qho1dFiniteDifference
from .ladder_operators import Qho1dLadderOperators
from .parameters import Qho1dNondimensionalizer, Qho1dParameters
from .result import (
    Qho1dCalculationResult,
    Qho1dCaseResult,
    Qho1dStateComparisonResult,
)
from .verification import Qho1dIndependentReferenceAnalyzer, Qho1dVerifier
from .verification_values import (
    Qho1dHamiltonianComparisonVerification,
    Qho1dResidualVerification,
    Qho1dSampledStateAlignmentVerification,
    Qho1dSpatialRepresentationVerification,
    Qho1dStateComparisonVerification,
    Qho1dSweepVerification,
    Qho1dVerification,
)
from .visualizations import (
    Qho1dVisualizationData,
    Qho1dVisualizationPlotEnum,
    Qho1dVisualizer,
)

__all__ = [
    "Qho1dAnalytical",
    "Qho1dAnalysisRequest",
    "Qho1dAnalyzer",
    "Qho1dCalculationResult",
    "Qho1dCaseResult",
    "Qho1dComparator",
    "Qho1dComparisonRequest",
    "Qho1dComparisonResult",
    "Qho1dConfiguration",
    "Qho1dCrossGridAnalysisRequest",
    "Qho1dCrossGridAnalysisResult",
    "Qho1dCrossGridAnalyzer",
    "Qho1dCrossGridComparisonResult",
    "Qho1dCrossGridVerification",
    "Qho1dCrossGridVerificationRequest",
    "Qho1dCrossGridVerifier",
    "Qho1dFiniteDifference",
    "Qho1dHamiltonianComparisonResult",
    "Qho1dHamiltonianComparisonVerification",
    "Qho1dIndependentReferenceAnalyzer",
    "Qho1dLadderOperators",
    "Qho1dNondimensionalizer",
    "Qho1dParameters",
    "Qho1dResidualResult",
    "Qho1dResidualVerification",
    "Qho1dSampledStateAlignmentResult",
    "Qho1dSampledStateAlignmentVerification",
    "Qho1dSpatialRepresentationResult",
    "Qho1dSpatialRepresentationVerification",
    "Qho1dStateComparisonResult",
    "Qho1dStateComparisonVerification",
    "Qho1dSweepVerification",
    "Qho1dVerification",
    "Qho1dVerifier",
    "Qho1dVisualizationData",
    "Qho1dVisualizationPlotEnum",
    "Qho1dVisualizer",
]
