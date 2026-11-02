"""Periodic-3D arbitrary-rank support-truncation analysis values."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.periodic3d.support_truncation.base import (
    Periodic3DSupportTruncationAnalysis,
)
from ksdft2effmass.real_space_support_truncation import (
    RealSpaceSupportTruncationModelToleranceSelection,
)

from .request import Periodic3DRankNSupportTruncationAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic3DRankNSupportTruncationAnalysis(
    RealSpaceSupportTruncationModelToleranceSelection,
    Periodic3DSupportTruncationAnalysis,
):
    """Retain one channel's minimum-support outcomes for two error functionals."""

    request: Periodic3DRankNSupportTruncationAnalysisRequest

    def __post_init__(self) -> None:
        RealSpaceSupportTruncationModelToleranceSelection.__post_init__(self)
        if type(self.request) is not Periodic3DRankNSupportTruncationAnalysisRequest:
            raise TypeError(
                "request must be the exact periodic-3D arbitrary-rank request"
            )


__all__ = ["Periodic3DRankNSupportTruncationAnalysis"]
