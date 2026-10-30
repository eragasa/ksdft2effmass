"""Immutable scientific diagnostics for higher-rank alignment calculations."""

from .frame import Periodic1DHigherRankFrameErrorResult
from .matrix import (
    Periodic1DHigherRankMatrixComparisonResult,
    Periodic1DHigherRankMatrixErrorResult,
)
from .model import (
    Periodic1DHigherRankModelDiagnostics,
    Periodic1DHigherRankProcrustesDiagnostics,
)

__all__ = [
    "Periodic1DHigherRankFrameErrorResult",
    "Periodic1DHigherRankMatrixComparisonResult",
    "Periodic1DHigherRankMatrixErrorResult",
    "Periodic1DHigherRankModelDiagnostics",
    "Periodic1DHigherRankProcrustesDiagnostics",
]
