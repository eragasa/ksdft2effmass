"""Public API for finite represented operator records.

This package initializer defines the supported import surface
``ksdft2effmass.operators``. It re-exports finite operator-record DataObjects,
Hermiticity analysis objects, JSON serialization, exact compatibility auditing,
represented-difference construction, residual metric analysis, and the concrete
comparison Workflow.

No scientific or numerical policy is implemented here. Matrix subtraction lives
in ``operators.difference``, residual norm policy lives in ``operators.residuals``,
and ``operators.comparison`` only composes those public ActionObjects. Importing
these names is a software-verification surface, not validation of DFT,
Wannierization, impurity physics, or an effective-mass model.
"""

from .comparison import OperatorRecordComparator
from .compatibility import (
    IncompatibleOperatorRecordsError,
    OperatorRecordCompatibilityAnalyzer,
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)
from .difference import (
    OperatorRecordDifferenceNumericalError,
    OperatorRecordDifferenceNumericalErrorCode,
    OperatorRecordDifferencer,
    OperatorRecordDifferenceResult,
)
from .hermiticity import (
    HermiticityAnalyzer,
    HermiticityNumericalError,
    HermiticityNumericalErrorCode,
    HermiticityRequirementError,
    HermiticityResult,
    HermiticityUnitMismatchError,
)
from .records import Basis, EnergyReference, Geometry, OperatorRecord, StateSpace
from .residuals import (
    OperatorRecordComparisonNumericalError,
    OperatorRecordComparisonNumericalErrorCode,
    OperatorRecordComparisonResult,
    OperatorRecordResidualAnalyzer,
)
from .serialization import OperatorRecordJsonSerializer

__all__ = [
    "Basis",
    "EnergyReference",
    "Geometry",
    "HermiticityAnalyzer",
    "HermiticityNumericalError",
    "HermiticityNumericalErrorCode",
    "HermiticityRequirementError",
    "HermiticityResult",
    "HermiticityUnitMismatchError",
    "IncompatibleOperatorRecordsError",
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
    "StateSpace",
]
