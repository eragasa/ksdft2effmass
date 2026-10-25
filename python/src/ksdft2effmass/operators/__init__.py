"""Public API for finite represented operator records.

This package initializer defines the supported import surface
``ksdft2effmass.operators``. It re-exports finite operator-record DataObjects,
reusable represented ladder and finite-difference operators, Hermiticity analysis
objects, JSON serialization, exact compatibility auditing, represented-difference
construction, residual metric analysis, and the concrete comparison Workflow.

Finite-difference stencil and dimensional-scaling policy lives in
``operators.finite_differences``; retained ladder algebra lives in
``operators.ladder_operators``. Matrix subtraction lives in ``operators.difference``,
residual norm policy lives in ``operators.residuals``, and ``operators.comparison``
only composes those public ActionObjects. Importing these names is a
software-verification surface, not validation of DFT, Wannierization, impurity
physics, or an effective-mass model.
"""

from .comparison import OperatorRecordComparator
from .compatibility import (
    IncompatibleOperatorRecordsError,
    OperatorRecordCompatibilityAnalyzer,
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)
from .complex_eigenpairs import (
    ComplexHermitianEigenpairResidualAnalyzer,
    ComplexHermitianEigenpairResidualResult,
    ComplexHermitianEigenpairResult,
    HermitianEigenpairSelection,
)
from .complex_eigensolvers import (
    ComplexHermitianEigensolverRequest,
    ComplexHermitianEigensolverResult,
    ComplexHermitianSparseEigenpairSolver,
)
from .difference import (
    OperatorRecordDifferenceNumericalError,
    OperatorRecordDifferenceNumericalErrorCode,
    OperatorRecordDifferencer,
    OperatorRecordDifferenceResult,
)
from .finite_differences import (
    DirichletBoundaryConditionRepresentation,
    DirichletIntervalRepresentation,
    FiniteDifferenceHamiltonian1D,
    SampledPotential1D,
    SchrodingerKineticEnergy1D,
    SecondOrderCentralDifferenceLaplacian1D,
    UniformGrid1DRepresentation,
)
from .hermiticity import (
    HermiticityAnalyzer,
    HermiticityNumericalError,
    HermiticityNumericalErrorCode,
    HermiticityRequirementError,
    HermiticityResult,
    HermiticityUnitMismatchError,
)
from .ladder_operators import LadderOperator1D
from .records import Basis, EnergyReference, Geometry, OperatorRecord, StateSpace
from .residuals import (
    OperatorRecordComparisonNumericalError,
    OperatorRecordComparisonNumericalErrorCode,
    OperatorRecordComparisonResult,
    OperatorRecordResidualAnalyzer,
)
from .serialization import OperatorRecordJsonSerializer
from .sparse_hermiticity import (
    ComplexSparseHermiticityAnalyzer,
    ComplexSparseHermiticityResult,
)

__all__ = [
    "Basis",
    "ComplexHermitianEigenpairResidualAnalyzer",
    "ComplexHermitianEigenpairResidualResult",
    "ComplexHermitianEigenpairResult",
    "ComplexHermitianEigensolverRequest",
    "ComplexHermitianEigensolverResult",
    "ComplexHermitianSparseEigenpairSolver",
    "ComplexSparseHermiticityAnalyzer",
    "ComplexSparseHermiticityResult",
    "DirichletBoundaryConditionRepresentation",
    "DirichletIntervalRepresentation",
    "EnergyReference",
    "FiniteDifferenceHamiltonian1D",
    "Geometry",
    "HermiticityAnalyzer",
    "HermiticityNumericalError",
    "HermiticityNumericalErrorCode",
    "HermiticityRequirementError",
    "HermiticityResult",
    "HermiticityUnitMismatchError",
    "HermitianEigenpairSelection",
    "IncompatibleOperatorRecordsError",
    "LadderOperator1D",
    "OperatorRecord",
    "OperatorRecordComparator",
    "OperatorRecordComparisonNumericalError",
    "OperatorRecordComparisonNumericalErrorCode",
    "OperatorRecordComparisonResult",
    "OperatorRecordCompatibilityAnalyzer",
    "OperatorRecordCompatibilityIssue",
    "OperatorRecordCompatibilityMismatchCode",
    "OperatorRecordCompatibilityResult",
    "OperatorRecordDifferenceNumericalError",
    "OperatorRecordDifferenceNumericalErrorCode",
    "OperatorRecordDifferenceResult",
    "OperatorRecordDifferencer",
    "OperatorRecordJsonSerializer",
    "OperatorRecordResidualAnalyzer",
    "SampledPotential1D",
    "SchrodingerKineticEnergy1D",
    "SecondOrderCentralDifferenceLaplacian1D",
    "StateSpace",
    "UniformGrid1DRepresentation",
]
