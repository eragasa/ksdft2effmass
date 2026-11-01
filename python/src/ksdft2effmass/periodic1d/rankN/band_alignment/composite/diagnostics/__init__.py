"""Immutable scientific diagnostics for higher-rank alignment calculations."""

from .frame import Periodic1DRankNFrameErrorResult
from .matrix import (
    Periodic1DRankNMatrixComparisonResult,
    Periodic1DRankNMatrixErrorResult,
)
from .model import (
    Periodic1DRankNModelDiagnostics,
    Periodic1DRankNProcrustesDiagnostics,
)

__all__ = [
    "Periodic1DRankNFrameErrorResult",
    "Periodic1DRankNMatrixComparisonResult",
    "Periodic1DRankNMatrixErrorResult",
    "Periodic1DRankNModelDiagnostics",
    "Periodic1DRankNProcrustesDiagnostics",
]
