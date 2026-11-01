"""Shared immutable diagnostics for rank-N Periodic1D capabilities."""

from .frame import Periodic1DRankNFrameErrorResult
from .matrix import (
    Periodic1DRankNMatrixComparisonResult,
    Periodic1DRankNMatrixErrorResult,
)

__all__ = [
    "Periodic1DRankNFrameErrorResult",
    "Periodic1DRankNMatrixComparisonResult",
    "Periodic1DRankNMatrixErrorResult",
]
