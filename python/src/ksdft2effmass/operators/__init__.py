"""Public API for finite represented operator records.

The module re-exports the maintained DataObjects, ResultObjects, ActionObjects,
public enum, and public exception for finite dense operator-matrix
representations.  It defines the stable import surface for state-space, basis,
geometry, energy-reference, operator-record, Hermiticity, JSON serialization,
compatibility, and compatible-record comparison objects.

No matrix operation is implemented in this package initializer.  Numerical
policies remain on action objects such as ``HermiticityAnalyzer`` and
``OperatorRecordComparator``.  Import success and API documentation are software
verification surfaces only; they do not scientifically validate any DFT or
reduced effective-mass calculation.
"""

from .comparison import (
    IncompatibleOperatorRecordsError,
    OperatorRecordComparator,
    OperatorRecordComparisonNumericalError,
    OperatorRecordComparisonResult,
    OperatorRecordCompatibilityAnalyzer,
    OperatorRecordCompatibilityIssue,
    OperatorRecordCompatibilityMismatchCode,
    OperatorRecordCompatibilityResult,
)
from .hermiticity import (
    HermiticityAnalyzer,
    HermiticityNumericalError,
    HermiticityRequirementError,
    HermiticityResult,
    HermiticityUnitMismatchError,
)
from .records import Basis, EnergyReference, Geometry, OperatorRecord, StateSpace
from .serialization import OperatorRecordJsonSerializer

__all__ = [
    "Basis",
    "EnergyReference",
    "Geometry",
    "HermiticityAnalyzer",
    "HermiticityNumericalError",
    "HermiticityRequirementError",
    "HermiticityResult",
    "HermiticityUnitMismatchError",
    "IncompatibleOperatorRecordsError",
    "OperatorRecord",
    "OperatorRecordComparator",
    "OperatorRecordComparisonNumericalError",
    "OperatorRecordComparisonResult",
    "OperatorRecordCompatibilityAnalyzer",
    "OperatorRecordCompatibilityIssue",
    "OperatorRecordCompatibilityMismatchCode",
    "OperatorRecordCompatibilityResult",
    "OperatorRecordJsonSerializer",
    "StateSpace",
]
