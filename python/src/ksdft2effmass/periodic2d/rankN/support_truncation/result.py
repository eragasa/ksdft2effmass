"""Periodic-2D arbitrary-rank support-truncation analysis values."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.periodic2d.support_truncation.base import (
    Periodic2DSupportTruncationAnalysis,
)
from ksdft2effmass.real_space_support_truncation import (
    RealSpaceSupportTruncationModelToleranceSelection,
)

from .request import Periodic2DRankNSupportTruncationAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRankNSupportTruncationAnalysis(
    RealSpaceSupportTruncationModelToleranceSelection,
    Periodic2DSupportTruncationAnalysis,
):
    """Retain one channel's minimum-support outcomes for two error functionals."""

    request: Periodic2DRankNSupportTruncationAnalysisRequest

    def __post_init__(self) -> None:
        RealSpaceSupportTruncationModelToleranceSelection.__post_init__(self)
        if type(self.request) is not Periodic2DRankNSupportTruncationAnalysisRequest:
            raise TypeError(
                "request must be the exact periodic-2D arbitrary-rank request"
            )


__all__ = ["Periodic2DRankNSupportTruncationAnalysis"]
