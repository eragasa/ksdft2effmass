"""Public three-model analysis of the one-dimensional quantum harmonic oscillator.

``QHO1D`` is dimension-specific. No dimension-neutral ``QHO`` API is claimed.
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

from .comparison import QHO1DComparator
from .model import (
    QHO1DAnalytical,
    QHO1DComparisonRequest,
    QHO1DComparisonResult,
    QHO1DFiniteDifference,
    QHO1DLadderOperators,
    QHO1DNondimensionalizer,
    QHO1DParameters,
)
from .study import (
    QHO1DResultVerifier,
    QHO1DStudyDefinition,
    QHO1DStudyEvaluator,
    QHO1DStudyInputDeserializer,
    QHO1DStudyResult,
    QHO1DStudyResultSerializer,
)

__all__ = [
    "QHO1DAnalytical",
    "QHO1DComparator",
    "QHO1DComparisonRequest",
    "QHO1DComparisonResult",
    "QHO1DFiniteDifference",
    "QHO1DLadderOperators",
    "QHO1DNondimensionalizer",
    "QHO1DParameters",
    "QHO1DResultVerifier",
    "QHO1DStudyDefinition",
    "QHO1DStudyEvaluator",
    "QHO1DStudyInputDeserializer",
    "QHO1DStudyResult",
    "QHO1DStudyResultSerializer",
    "MatrixQuantity",
    "PhysicalUnit",
    "PintUnitConverter",
    "ScalarQuantity",
    "SparseMatrixQuantity",
    "Unitless",
    "VectorQuantity",
]
