"""Periodic-2D rank-two support-truncation ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.rankN.support_truncation.base import (
    Periodic2DRankNSupportTruncationAnalysisRequestRole,
    Periodic2DRankNSupportTruncationAnalysisRole,
    Periodic2DRankNSupportTruncationAnalyzerRole,
    Periodic2DRankNSupportTruncationCapability,
)


class _Periodic2DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""
        return 2


class Periodic2DRank2SupportTruncationCapability(
    Periodic2DRankNSupportTruncationCapability,
    ABC,
):
    """Identify periodic-2D rank-two support truncation."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""


class Periodic2DRank2SupportTruncationAnalysisRequestRole(
    _Periodic2DRank2BandSubspace,
    Periodic2DRankNSupportTruncationAnalysisRequestRole,
    Periodic2DRank2SupportTruncationCapability,
    ABC,
):
    """Bind one periodic-2D rank-two support-truncation request."""

    __slots__ = ()


class Periodic2DRank2SupportTruncationAnalysisRole(
    _Periodic2DRank2BandSubspace,
    Periodic2DRankNSupportTruncationAnalysisRole,
    Periodic2DRank2SupportTruncationCapability,
    ABC,
):
    """Retain one periodic-2D rank-two support-truncation analysis."""

    __slots__ = ()


class Periodic2DRank2SupportTruncationAnalyzerRole[
    RequestT: Periodic2DRank2SupportTruncationAnalysisRequestRole,
    AnalysisT: Periodic2DRank2SupportTruncationAnalysisRole,
](
    _Periodic2DRank2BandSubspace,
    Periodic2DRankNSupportTruncationAnalyzerRole[RequestT, AnalysisT],
    Periodic2DRank2SupportTruncationCapability,
    ABC,
):
    """Execute one periodic-2D rank-two support-truncation request."""

    __slots__ = ()


__all__ = [
    "Periodic2DRank2SupportTruncationAnalysisRequestRole",
    "Periodic2DRank2SupportTruncationAnalysisRole",
    "Periodic2DRank2SupportTruncationAnalyzerRole",
    "Periodic2DRank2SupportTruncationCapability",
]
