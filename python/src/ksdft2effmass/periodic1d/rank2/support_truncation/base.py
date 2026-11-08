"""Periodic-1D rank-two support-truncation ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic1d.rankN.support_truncation.base import (
    Periodic1DRankNSupportTruncationAnalysisRequestRole,
    Periodic1DRankNSupportTruncationAnalysisRole,
    Periodic1DRankNSupportTruncationAnalyzerRole,
    Periodic1DRankNSupportTruncationCapability,
    Periodic1DRankNSupportTruncationValue,
)


class _Periodic1DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""
        return 2


class Periodic1DRank2SupportTruncationCapability(
    Periodic1DRankNSupportTruncationCapability,
    ABC,
):
    """Identify periodic-1D rank-two support truncation."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""


class Periodic1DRank2SupportTruncationAnalysisRequestRole(
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNSupportTruncationAnalysisRequestRole,
    Periodic1DRank2SupportTruncationCapability,
    ABC,
):
    """Bind one periodic-1D rank-two support-truncation request."""

    __slots__ = ()


class Periodic1DRank2SupportTruncationAnalysisRole(
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNSupportTruncationAnalysisRole,
    Periodic1DRank2SupportTruncationCapability,
    ABC,
):
    """Retain one periodic-1D rank-two support-truncation analysis."""

    __slots__ = ()


class Periodic1DRank2SupportTruncationAnalyzerRole[
    RequestT: Periodic1DRank2SupportTruncationAnalysisRequestRole,
    AnalysisT: Periodic1DRank2SupportTruncationAnalysisRole,
](
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNSupportTruncationAnalyzerRole[RequestT, AnalysisT],
    Periodic1DRank2SupportTruncationCapability,
    ABC,
):
    """Execute one periodic-1D rank-two support-truncation request."""

    __slots__ = ()


class Periodic1DRank2SupportTruncationAction(
    _Periodic1DRank2BandSubspace,
    Periodic1DRank2SupportTruncationCapability,
    ABC,
):
    """Execute one rank-two support-truncation supporting action."""

    __slots__ = ()


class Periodic1DRank2SupportTruncationValue(
    _Periodic1DRank2BandSubspace,
    Periodic1DRankNSupportTruncationValue,
    Periodic1DRank2SupportTruncationCapability,
    ABC,
):
    """Retain one standalone rank-two support-truncation value."""

    __slots__ = ()


__all__ = [
    "Periodic1DRank2SupportTruncationAction",
    "Periodic1DRank2SupportTruncationAnalysisRequestRole",
    "Periodic1DRank2SupportTruncationAnalysisRole",
    "Periodic1DRank2SupportTruncationAnalyzerRole",
    "Periodic1DRank2SupportTruncationCapability",
    "Periodic1DRank2SupportTruncationValue",
]
