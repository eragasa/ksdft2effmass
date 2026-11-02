"""Periodic-2D arbitrary-rank support-truncation ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.support_truncation.base import (
    Periodic2DSupportTruncation,
    Periodic2DSupportTruncationAnalysis,
    Periodic2DSupportTruncationAnalysisRequest,
    Periodic2DSupportTruncationAnalyzer,
)


class Periodic2DRankNSupportTruncationCapability(
    Periodic2DSupportTruncation,
    ABC,
):
    """Identify periodic-2D finite-rank support truncation."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""


class Periodic2DRankNSupportTruncationAnalysisRequestRole(
    Periodic2DSupportTruncationAnalysisRequest,
    Periodic2DRankNSupportTruncationCapability,
    ABC,
):
    """Bind one periodic-2D arbitrary-rank support-truncation request."""

    __slots__ = ()


class Periodic2DRankNSupportTruncationAnalysisRole(
    Periodic2DSupportTruncationAnalysis,
    Periodic2DRankNSupportTruncationCapability,
    ABC,
):
    """Retain one periodic-2D arbitrary-rank support-truncation analysis."""

    __slots__ = ()


class Periodic2DRankNSupportTruncationAnalyzerRole[
    RequestT: Periodic2DRankNSupportTruncationAnalysisRequestRole,
    AnalysisT: Periodic2DRankNSupportTruncationAnalysisRole,
](
    Periodic2DSupportTruncationAnalyzer[RequestT, AnalysisT],
    Periodic2DRankNSupportTruncationCapability,
    ABC,
):
    """Execute one periodic-2D arbitrary-rank support-truncation request."""

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""
        return self.request.band_subspace_rank


__all__ = [
    "Periodic2DRankNSupportTruncationAnalysisRequestRole",
    "Periodic2DRankNSupportTruncationAnalysisRole",
    "Periodic2DRankNSupportTruncationAnalyzerRole",
    "Periodic2DRankNSupportTruncationCapability",
]
