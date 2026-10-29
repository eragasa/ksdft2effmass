"""KSD-owned studies of the PhysKit one-dimensional particle-in-a-box model."""

from .analysis import (
    Piab1dAnalysis,
    Piab1dAnalysisRequest,
    Piab1dAnalyzer,
    Piab1dEigenpairSweepResult,
    Piab1dFiniteAlgebraicDiagnostics,
    Piab1dGridSweepAnalysis,
    Piab1dGridSweepAnalyzer,
    Piab1dGridSweepDefinition,
    Piab1dIndependentReference,
    Piab1dIndependentReferenceAnalyzer,
    Piab1dResidualNormSweepResult,
    Piab1dVerification,
    Piab1dVerifier,
)
from .configuration import Piab1dConfiguration
from .diagnostics import (
    DiagnosticMethodsEnum,
    DiscreteSpectrumMaximumAbsoluteErrorAnalyzer,
    Piab1dDiagnostics,
    ProjectorIdempotencyAnalyzer,
    ScaledEigenpairResidualAnalyzer,
    SpectralReconstructionErrorAnalyzer,
    WeightedGramErrorAnalyzer,
    WeightedProjectorErrorAnalyzer,
    diagnostic_method_names,
)
from .result import (
    Piab1dCalculationResult,
    Piab1dConvergenceResult,
    Piab1dSelectionResult,
)
from .visualizations import (
    Piab1dVisualizationData,
    Piab1dVisualizationPlotEnum,
    Piab1dVisualizer,
)

__all__ = [
    "DiagnosticMethodsEnum",
    "DiscreteSpectrumMaximumAbsoluteErrorAnalyzer",
    "Piab1dAnalysis",
    "Piab1dAnalysisRequest",
    "Piab1dCalculationResult",
    "Piab1dConfiguration",
    "Piab1dConvergenceResult",
    "Piab1dEigenpairSweepResult",
    "Piab1dFiniteAlgebraicDiagnostics",
    "Piab1dGridSweepAnalysis",
    "Piab1dGridSweepAnalyzer",
    "Piab1dGridSweepDefinition",
    "Piab1dIndependentReference",
    "Piab1dIndependentReferenceAnalyzer",
    "Piab1dAnalyzer",
    "Piab1dDiagnostics",
    "Piab1dResidualNormSweepResult",
    "Piab1dSelectionResult",
    "Piab1dVerification",
    "Piab1dVerifier",
    "Piab1dVisualizationData",
    "Piab1dVisualizationPlotEnum",
    "Piab1dVisualizer",
    "ProjectorIdempotencyAnalyzer",
    "ScaledEigenpairResidualAnalyzer",
    "SpectralReconstructionErrorAnalyzer",
    "WeightedGramErrorAnalyzer",
    "WeightedProjectorErrorAnalyzer",
    "diagnostic_method_names",
]
