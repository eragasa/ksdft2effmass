"""Periodic-2D arbitrary-rank support-truncation analysis values."""

from __future__ import annotations

from dataclasses import dataclass
from typing import final

from ksdft2effmass.real_space_support_truncation import (
    RealSpaceSupportTruncationModelToleranceSelection,
)

from .base import Periodic2DRankNSupportTruncationAnalysisRole
from .request import Periodic2DRankNSupportTruncationAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNSupportTruncationAnalysis(
    RealSpaceSupportTruncationModelToleranceSelection,
    Periodic2DRankNSupportTruncationAnalysisRole,
):
    """Retain one channel's minimum-support outcomes for two error functionals."""

    request: Periodic2DRankNSupportTruncationAnalysisRequest

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""
        return self.request.band_subspace_rank

    def __post_init__(self) -> None:
        RealSpaceSupportTruncationModelToleranceSelection.__post_init__(self)
        if type(self.request) is not Periodic2DRankNSupportTruncationAnalysisRequest:
            raise TypeError(
                "request must be the exact periodic-2D arbitrary-rank request"
            )


__all__ = ["Periodic2DRankNSupportTruncationAnalysis"]
