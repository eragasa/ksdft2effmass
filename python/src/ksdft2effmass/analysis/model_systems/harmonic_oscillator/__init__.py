"""Public three-model analysis of the quantum harmonic oscillator.

The supported surface binds an exact analytical model, a bounded uniform-grid
Dirichlet model, and a retained ladder-operator model. An explicit injection places
the Dirichlet Hamiltonian and ladder Hamiltonian in the same ordered coordinates.
The comparison separates represented finite operators from the continuum differential
operator and makes no semiconductor-validation claim.
"""

from ksdft2effmass.operators.quantities import (
    MatrixQuantity,
    PhysicalUnit,
    PintUnitConverter,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)

from .comparison import HarmonicOscillatorComparator
from .model import (
    HarmonicOscillatorAnalytical,
    HarmonicOscillatorComparisonRequest,
    HarmonicOscillatorComparisonResult,
    HarmonicOscillatorFiniteDifference,
    HarmonicOscillatorLadderOperators,
    HarmonicOscillatorNondimensionalizer,
    HarmonicOscillatorParameters,
)

__all__ = [
    "HarmonicOscillatorAnalytical",
    "HarmonicOscillatorComparator",
    "HarmonicOscillatorComparisonRequest",
    "HarmonicOscillatorComparisonResult",
    "HarmonicOscillatorFiniteDifference",
    "HarmonicOscillatorLadderOperators",
    "HarmonicOscillatorNondimensionalizer",
    "HarmonicOscillatorParameters",
    "MatrixQuantity",
    "PhysicalUnit",
    "PintUnitConverter",
    "ScalarQuantity",
    "SparseMatrixQuantity",
    "Unitless",
    "VectorQuantity",
]
