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

from .comparison import Qho1dComparator
from .model import (
    Qho1dAnalytical,
    Qho1dComparisonRequest,
    Qho1dComparisonResult,
    Qho1dFiniteDifference,
    Qho1dLadderOperators,
    Qho1dNondimensionalizer,
    Qho1dParameters,
)
from .study import (
    Qho1dResultVerifier,
    Qho1dStudyDefinition,
    Qho1dStudyEvaluator,
    Qho1dStudyInputDeserializer,
    Qho1dStudyResult,
    Qho1dStudyResultSerializer,
)

__all__ = [
    "Qho1dAnalytical",
    "Qho1dComparator",
    "Qho1dComparisonRequest",
    "Qho1dComparisonResult",
    "Qho1dFiniteDifference",
    "Qho1dLadderOperators",
    "Qho1dNondimensionalizer",
    "Qho1dParameters",
    "Qho1dResultVerifier",
    "Qho1dStudyDefinition",
    "Qho1dStudyEvaluator",
    "Qho1dStudyInputDeserializer",
    "Qho1dStudyResult",
    "Qho1dStudyResultSerializer",
    "MatrixQuantity",
    "PhysicalUnit",
    "PintUnitConverter",
    "ScalarQuantity",
    "SparseMatrixQuantity",
    "Unitless",
    "VectorQuantity",
]
