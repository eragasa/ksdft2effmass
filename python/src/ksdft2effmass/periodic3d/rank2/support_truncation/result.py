"""Periodic-3D rank-two support-truncation analysis values."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.periodic3d.support_truncation.base import (
    Periodic3DSupportTruncationAnalysis,
)
from ksdft2effmass.real_space_support_truncation import (
    RealSpaceSupportTruncationModelToleranceSelection,
)

from .request import Periodic3DRank2SupportTruncationAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRank2SupportTruncationAnalysis(
    RealSpaceSupportTruncationModelToleranceSelection,
    Periodic3DSupportTruncationAnalysis,
):
    """Retain one channel's minimum-support outcomes for two error functionals."""

    request: Periodic3DRank2SupportTruncationAnalysisRequest

    def __post_init__(self) -> None:
        RealSpaceSupportTruncationModelToleranceSelection.__post_init__(self)
        if type(self.request) is not Periodic3DRank2SupportTruncationAnalysisRequest:
            raise TypeError("request must be the exact periodic-3D rank-two request")


__all__ = ["Periodic3DRank2SupportTruncationAnalysis"]
