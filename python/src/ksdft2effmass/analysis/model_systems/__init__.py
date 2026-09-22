"""Public scientific analyses for controlled quantum model systems.

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
from .harmonic_oscillator import (
    HarmonicOscillatorAnalytical,
    HarmonicOscillatorComparator,
    HarmonicOscillatorComparisonRequest,
    HarmonicOscillatorComparisonResult,
    HarmonicOscillatorFiniteDifference,
    HarmonicOscillatorLadderOperators,
    HarmonicOscillatorNondimensionalizer,
    HarmonicOscillatorParameters,
)
from .intervals import DirichletInterval
from .particle_in_box import (
    ParticleInBoxAnalytical,
    ParticleInBoxFiniteDifference,
    ParticleInBoxGridEvaluation,
    ParticleInBoxGridEvaluator,
    ParticleInBoxParameters,
)
from .periodic_1d import (
    PeriodicFiniteDifferenceFiberHamiltonian1DConstructor,
    PeriodicFiniteDifferenceFiberHamiltonian1DResult,
    PeriodicFourierPotential1D,
    PeriodicUniformGrid1D,
    PlaneWaveFiberHamiltonian1DConstructor,
    PlaneWaveFiberHamiltonian1DResult,
)

__all__ = [
    "DirichletBoundaryCondition",
    "DirichletInterval",
    "HarmonicOscillatorAnalytical",
    "HarmonicOscillatorComparator",
    "HarmonicOscillatorComparisonRequest",
    "HarmonicOscillatorComparisonResult",
    "HarmonicOscillatorFiniteDifference",
    "HarmonicOscillatorLadderOperators",
    "HarmonicOscillatorNondimensionalizer",
    "HarmonicOscillatorParameters",
    "MODEL_SYSTEM_UNIT_CONVERTER",
    "MatrixQuantity",
    "ParticleInBoxAnalytical",
    "ParticleInBoxFiniteDifference",
    "ParticleInBoxGridEvaluation",
    "ParticleInBoxGridEvaluator",
    "ParticleInBoxParameters",
    "PeriodicFiniteDifferenceFiberHamiltonian1DConstructor",
    "PeriodicFiniteDifferenceFiberHamiltonian1DResult",
    "PeriodicFourierPotential1D",
    "PeriodicUniformGrid1D",
    "PhysicalUnit",
    "PlaneWaveFiberHamiltonian1DConstructor",
    "PlaneWaveFiberHamiltonian1DResult",
    "PintUnitConverter",
    "ScalarQuantity",
    "SparseMatrixQuantity",
    "UniformCartesianGrid1D",
    "UniformCartesianGrid2D",
    "UniformCartesianGrid3D",
    "Unitless",
    "VectorQuantity",
]
