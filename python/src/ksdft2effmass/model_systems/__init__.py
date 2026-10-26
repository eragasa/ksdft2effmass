"""Public definitions and finite representations for controlled model systems.

Model systems are idealized physical and mathematical systems used to expose
representation, discretization, and reduction behavior under explicit assumptions.
They are not described as toys, and their numerical verification does not establish
scientific validation for semiconductor applications.
"""

from ksdft2effmass.verification import BaseVerification

from .analysis import (
    BaseModelAnalysisVerifier,
    BaseModelSystemAnalyzer,
    ModelAnalysisVerificationResult,
)
from .boundary_conditions import DirichletBoundaryCondition
from .cartesian_grids import (
    UniformCartesianGrid1D,
    UniformCartesianGrid2D,
    UniformCartesianGrid3D,
)
from .intervals import DirichletInterval
from .mathieu1d import (
    Mathieu1dStudyDefinition,
    Mathieu1dStudyEvaluator,
    Mathieu1dStudyInputDeserializer,
    Mathieu1dStudyInputSerializer,
    Mathieu1dStudyResult,
    Mathieu1dStudyResultSerializer,
    Mathieu1dStudyVerificationResult,
    Mathieu1dStudyVerificationSerializer,
    Mathieu1dStudyVerifier,
)
from .periodic2d import (
    CenteredUniformReciprocalMesh2D,
    PlaneWaveBlochHamiltonian2DConstructor,
    PlaneWaveBlochHamiltonian2DModel,
    PlaneWaveBlochHamiltonian2DRequest,
    PlaneWaveBlochHamiltonian2DResult,
    PlaneWaveFourierCoefficient2D,
    PlaneWaveReciprocalSewing2DConstructor,
    PlaneWaveReciprocalSewing2DRequest,
    PlaneWaveReciprocalSewing2DResult,
    PositiveReciprocalDirection2D,
    ReciprocalMeshNeighbor2DConstructor,
    ReciprocalMeshNeighbor2DRequest,
    ReciprocalMeshNeighbor2DResult,
)
from .periodic_1d import (
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
    PeriodicFiniteDifferenceFiberHamiltonian1DResult,
    PeriodicFourierPotential1D,
    PeriodicUniformGrid1D,
    PlaneWaveFiberHamiltonian1DConstructor,
    PlaneWaveFiberHamiltonian1DResult,
)
from .qho1d import (
    Qho1dAnalytical,
    Qho1dComparator,
    Qho1dComparisonRequest,
    Qho1dComparisonResult,
    Qho1dFiniteDifference,
    Qho1dLadderOperators,
    Qho1dNondimensionalizer,
    Qho1dParameters,
)
from .result_sections import (
    AnalyticalSamplingResultSection,
    BaseModelAnalysisResultSection,
    EigensystemResultSection,
    HamiltonianResultSection,
    QuadratureResultSection,
    SpectralReductionResultSection,
)
from .verification import (
    BaseModelAnalysisVerification,
    QuadratureVerification,
    VisualizationProjectionVerification,
)
from .visualization import (
    BaseModelAnalysisFigure,
    BaseModelAnalysisFigureRenderer,
    BaseModelAnalysisPlot,
    BaseModelAnalysisSubplot,
    BaseModelAnalysisVisualization,
    BaseModelAnalysisVisualizationData,
    BaseModelAnalysisVisualizer,
    ModelAnalysisPngFigureRenderer,
    ModelAnalysisPngVisualization,
)

__all__ = [
    "AnalyticalSamplingResultSection",
    "BaseModelAnalysisResultSection",
    "BaseModelAnalysisVerification",
    "BaseModelAnalysisVerifier",
    "BaseModelAnalysisFigure",
    "BaseModelAnalysisFigureRenderer",
    "BaseModelAnalysisPlot",
    "BaseModelAnalysisSubplot",
    "BaseModelAnalysisVisualization",
    "BaseModelAnalysisVisualizationData",
    "BaseModelAnalysisVisualizer",
    "ModelAnalysisPngFigureRenderer",
    "ModelAnalysisPngVisualization",
    "ModelAnalysisVerificationResult",
    "BaseModelSystemAnalyzer",
    "BaseVerification",
    "CenteredUniformReciprocalMesh2D",
    "DirichletBoundaryCondition",
    "DirichletInterval",
    "EigensystemResultSection",
    "HamiltonianResultSection",
    "Qho1dAnalytical",
    "Qho1dComparator",
    "Qho1dComparisonRequest",
    "Qho1dComparisonResult",
    "Qho1dFiniteDifference",
    "Qho1dLadderOperators",
    "Qho1dNondimensionalizer",
    "Qho1dParameters",
    "QuadratureResultSection",
    "QuadratureVerification",
    "Mathieu1dStudyDefinition",
    "Mathieu1dStudyEvaluator",
    "Mathieu1dStudyInputDeserializer",
    "Mathieu1dStudyInputSerializer",
    "Mathieu1dStudyResult",
    "Mathieu1dStudyResultSerializer",
    "Mathieu1dStudyVerificationResult",
    "Mathieu1dStudyVerificationSerializer",
    "Mathieu1dStudyVerifier",
    "PeriodicFiniteDifferenceFiberHamiltonian1DConstructor",
    "PeriodicFiniteDifferenceFiberHamiltonian1DResult",
    "PeriodicFourierPotential1D",
    "PeriodicUniformGrid1D",
    "PlaneWaveBlochHamiltonian2DConstructor",
    "PlaneWaveBlochHamiltonian2DModel",
    "PlaneWaveBlochHamiltonian2DRequest",
    "PlaneWaveBlochHamiltonian2DResult",
    "PlaneWaveFiberHamiltonian1DConstructor",
    "PlaneWaveFiberHamiltonian1DResult",
    "PlaneWaveFourierCoefficient2D",
    "PlaneWaveReciprocalSewing2DConstructor",
    "PlaneWaveReciprocalSewing2DRequest",
    "PlaneWaveReciprocalSewing2DResult",
    "PositiveReciprocalDirection2D",
    "ReciprocalMeshNeighbor2DConstructor",
    "ReciprocalMeshNeighbor2DRequest",
    "ReciprocalMeshNeighbor2DResult",
    "SpectralReductionResultSection",
    "VisualizationProjectionVerification",
    "UniformCartesianGrid1D",
    "UniformCartesianGrid2D",
    "UniformCartesianGrid3D",
]
