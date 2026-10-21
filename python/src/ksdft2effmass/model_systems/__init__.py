"""Public definitions and finite representations for controlled model systems.

Model systems are idealized physical and mathematical systems used to expose
representation, discretization, and reduction behavior under explicit assumptions.
They are not described as toys, and their numerical verification does not establish
scientific validation for semiconductor applications.
"""

from ksdft2effmass.operators.quantities import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    MatrixQuantity,
    PhysicalUnit,
    PintUnitConverter,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)

from .boundary_conditions import DirichletBoundaryCondition
from .cartesian_grids import (
    UniformCartesianGrid1D,
    UniformCartesianGrid2D,
    UniformCartesianGrid3D,
)
from .intervals import DirichletInterval
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
from .piab1d import (
    Piab1dAnalytical,
    Piab1dFiniteDifference,
    Piab1dGridEvaluation,
    Piab1dGridEvaluator,
    Piab1dParameters,
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

__all__ = [
    "CenteredUniformReciprocalMesh2D",
    "DirichletBoundaryCondition",
    "DirichletInterval",
    "Qho1dAnalytical",
    "Qho1dComparator",
    "Qho1dComparisonRequest",
    "Qho1dComparisonResult",
    "Qho1dFiniteDifference",
    "Qho1dLadderOperators",
    "Qho1dNondimensionalizer",
    "Qho1dParameters",
    "MODEL_SYSTEM_UNIT_CONVERTER",
    "MatrixQuantity",
    "Piab1dAnalytical",
    "Piab1dFiniteDifference",
    "Piab1dGridEvaluation",
    "Piab1dGridEvaluator",
    "Piab1dParameters",
    "PeriodicFiniteDifferenceFiberHamiltonian1DConstructor",
    "PeriodicFiniteDifferenceFiberHamiltonian1DResult",
    "PeriodicFourierPotential1D",
    "PeriodicUniformGrid1D",
    "PhysicalUnit",
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
    "PintUnitConverter",
    "PositiveReciprocalDirection2D",
    "ReciprocalMeshNeighbor2DConstructor",
    "ReciprocalMeshNeighbor2DRequest",
    "ReciprocalMeshNeighbor2DResult",
    "ScalarQuantity",
    "SparseMatrixQuantity",
    "UniformCartesianGrid1D",
    "UniformCartesianGrid2D",
    "UniformCartesianGrid3D",
    "Unitless",
    "VectorQuantity",
]
