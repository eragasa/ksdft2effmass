"""Public rank-generic diagnostics for finite matrix fields and Fourier tails."""

from .comparison import (
    MatrixErrorDecompositionAnalyzer,
    MatrixErrorDecompositionDiagnostics,
    MatrixFieldComparisonAnalyzer,
    MatrixFieldComparisonDiagnostics,
    MatrixFieldErrorAnalyzer,
    MatrixFieldErrorSummary,
    MatrixPerturbationBoundDiagnostics,
)
from .locality import (
    FourierMatrixBlockNorm1D,
    FourierMatrixBlockNormInventory1D,
    FourierMatrixBlockNormInventoryAnalyzer1D,
    SymmetricRangeTailAnalyzer1D,
    SymmetricRangeTailDiagnostics1D,
    SymmetricRangeTailMonotonicityAnalyzer1D,
    SymmetricRangeTailMonotonicityDiagnostics1D,
)
from .refinement import ScalarRefinementAnalyzer, ScalarRefinementDiagnostics
from .structure import (
    MatrixFieldHermiticityAnalyzer,
    MatrixFieldHermiticityDiagnostics,
    MatrixFieldIsometryAnalyzer,
    MatrixFieldIsometryDiagnostics,
    MatrixProjectorFieldAnalyzer,
    MatrixProjectorFieldDiagnostics,
)

__all__ = [
    "FourierMatrixBlockNorm1D",
    "FourierMatrixBlockNormInventory1D",
    "FourierMatrixBlockNormInventoryAnalyzer1D",
    "MatrixErrorDecompositionAnalyzer",
    "MatrixErrorDecompositionDiagnostics",
    "MatrixFieldComparisonAnalyzer",
    "MatrixFieldComparisonDiagnostics",
    "MatrixFieldErrorAnalyzer",
    "MatrixFieldErrorSummary",
    "MatrixFieldHermiticityAnalyzer",
    "MatrixFieldHermiticityDiagnostics",
    "MatrixFieldIsometryAnalyzer",
    "MatrixFieldIsometryDiagnostics",
    "MatrixPerturbationBoundDiagnostics",
    "MatrixProjectorFieldAnalyzer",
    "MatrixProjectorFieldDiagnostics",
    "ScalarRefinementAnalyzer",
    "ScalarRefinementDiagnostics",
    "SymmetricRangeTailAnalyzer1D",
    "SymmetricRangeTailDiagnostics1D",
    "SymmetricRangeTailMonotonicityAnalyzer1D",
    "SymmetricRangeTailMonotonicityDiagnostics1D",
]
