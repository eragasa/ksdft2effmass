"""Periodic-1D arbitrary-rank support-truncation ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic1d.support_truncation.base import (
    Periodic1DSupportTruncation,
    Periodic1DSupportTruncationAnalysis,
    Periodic1DSupportTruncationAnalysisRequest,
    Periodic1DSupportTruncationAnalyzer,
)


class Periodic1DRankNSupportTruncationCapability(
    Periodic1DSupportTruncation,
    ABC,
):
    """Identify periodic-1D finite-rank support truncation."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""


class Periodic1DRankNSupportTruncationAnalysisRequestRole(
    Periodic1DSupportTruncationAnalysisRequest,
    Periodic1DRankNSupportTruncationCapability,
    ABC,
):
    """Bind one periodic-1D arbitrary-rank support-truncation request."""

    __slots__ = ()


class Periodic1DRankNSupportTruncationAnalysisRole(
    Periodic1DSupportTruncationAnalysis,
    Periodic1DRankNSupportTruncationCapability,
    ABC,
):
    """Retain one periodic-1D arbitrary-rank support-truncation analysis."""

    __slots__ = ()


class Periodic1DRankNSupportTruncationAnalyzerRole[
    RequestT: Periodic1DRankNSupportTruncationAnalysisRequestRole,
    AnalysisT: Periodic1DRankNSupportTruncationAnalysisRole,
](
    Periodic1DSupportTruncationAnalyzer[RequestT, AnalysisT],
    Periodic1DRankNSupportTruncationCapability,
    ABC,
):
    """Execute one periodic-1D arbitrary-rank support-truncation request."""

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""
        return self.request.band_subspace_rank


class Periodic1DRankNSupportTruncationValue(
    Periodic1DRankNSupportTruncationCapability,
    ABC,
):
    """Retain one standalone arbitrary-rank support-truncation value."""

    __slots__ = ()


__all__ = [
    "Periodic1DRankNSupportTruncationAnalysisRequestRole",
    "Periodic1DRankNSupportTruncationAnalysisRole",
    "Periodic1DRankNSupportTruncationAnalyzerRole",
    "Periodic1DRankNSupportTruncationCapability",
    "Periodic1DRankNSupportTruncationValue",
]
