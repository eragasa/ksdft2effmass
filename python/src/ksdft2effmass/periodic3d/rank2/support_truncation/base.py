"""Periodic-3D rank-two support-truncation ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.rankN.support_truncation.base import (
    Periodic3DRankNSupportTruncationAnalysisRequestRole,
    Periodic3DRankNSupportTruncationAnalysisRole,
    Periodic3DRankNSupportTruncationAnalyzerRole,
    Periodic3DRankNSupportTruncationCapability,
)


class _Periodic3DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""
        return 2


class Periodic3DRank2SupportTruncationCapability(
    Periodic3DRankNSupportTruncationCapability,
    ABC,
):
    """Identify periodic-3D rank-two support truncation."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""


class Periodic3DRank2SupportTruncationAnalysisRequestRole(
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNSupportTruncationAnalysisRequestRole,
    Periodic3DRank2SupportTruncationCapability,
    ABC,
):
    """Bind one periodic-3D rank-two support-truncation request."""

    __slots__ = ()


class Periodic3DRank2SupportTruncationAnalysisRole(
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNSupportTruncationAnalysisRole,
    Periodic3DRank2SupportTruncationCapability,
    ABC,
):
    """Retain one periodic-3D rank-two support-truncation analysis."""

    __slots__ = ()


class Periodic3DRank2SupportTruncationAnalyzerRole[
    RequestT: Periodic3DRank2SupportTruncationAnalysisRequestRole,
    AnalysisT: Periodic3DRank2SupportTruncationAnalysisRole,
](
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNSupportTruncationAnalyzerRole[RequestT, AnalysisT],
    Periodic3DRank2SupportTruncationCapability,
    ABC,
):
    """Execute one periodic-3D rank-two support-truncation request."""

    __slots__ = ()


__all__ = [
    "Periodic3DRank2SupportTruncationAnalysisRequestRole",
    "Periodic3DRank2SupportTruncationAnalysisRole",
    "Periodic3DRank2SupportTruncationAnalyzerRole",
    "Periodic3DRank2SupportTruncationCapability",
]
