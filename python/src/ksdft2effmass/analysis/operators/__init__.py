"""Reusable analysis of finite represented operators."""

from .compression_residuals import (
    OrthogonalCompressionResidualAnalyzer,
    OrthogonalCompressionResidualResult,
)
from .decomposition_identifiability import (
    DecompositionIdentifiabilityAnalyzer,
    DecompositionIdentifiabilityResult,
)
from .eigenpair_diagnostics import (
    RealSymmetricEigenpairDiagnosticAnalyzer,
    RealSymmetricEigenpairDiagnosticResult,
)
from .model_fitting import RetainedModelClassFitResult, RetainedModelClassFitter

__all__ = [
    "OrthogonalCompressionResidualAnalyzer",
    "OrthogonalCompressionResidualResult",
    "RealSymmetricEigenpairDiagnosticAnalyzer",
    "RealSymmetricEigenpairDiagnosticResult",
    "DecompositionIdentifiabilityAnalyzer",
    "DecompositionIdentifiabilityResult",
    "RetainedModelClassFitResult",
    "RetainedModelClassFitter",
]
