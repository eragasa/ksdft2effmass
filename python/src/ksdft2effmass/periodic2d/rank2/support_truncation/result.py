"""Periodic-2D rank-two support-truncation analysis values."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.real_space_support_truncation import (
    RealSpaceSupportTruncationModelToleranceSelection,
)

from .base import Periodic2DRank2SupportTruncationAnalysisRole
from .request import Periodic2DRank2SupportTruncationAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic2DRank2SupportTruncationAnalysis(
    RealSpaceSupportTruncationModelToleranceSelection,
    Periodic2DRank2SupportTruncationAnalysisRole,
):
    """Retain one channel's minimum-support outcomes for two error functionals."""

    request: Periodic2DRank2SupportTruncationAnalysisRequest

    def __post_init__(self) -> None:
        RealSpaceSupportTruncationModelToleranceSelection.__post_init__(self)
        if type(self.request) is not Periodic2DRank2SupportTruncationAnalysisRequest:
            raise TypeError("request must be the exact periodic-2D rank-two request")


__all__ = ["Periodic2DRank2SupportTruncationAnalysis"]
