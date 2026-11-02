"""Periodic-3D arbitrary-rank support-truncation ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.support_truncation.base import (
    Periodic3DSupportTruncation,
    Periodic3DSupportTruncationAnalysis,
    Periodic3DSupportTruncationAnalysisRequest,
    Periodic3DSupportTruncationAnalyzer,
)


class Periodic3DRankNSupportTruncationCapability(
    Periodic3DSupportTruncation,
    ABC,
):
    """Identify periodic-3D finite-rank support truncation."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""


class Periodic3DRankNSupportTruncationAnalysisRequestRole(
    Periodic3DSupportTruncationAnalysisRequest,
    Periodic3DRankNSupportTruncationCapability,
    ABC,
):
    """Bind one periodic-3D arbitrary-rank support-truncation request."""

    __slots__ = ()


class Periodic3DRankNSupportTruncationAnalysisRole(
    Periodic3DSupportTruncationAnalysis,
    Periodic3DRankNSupportTruncationCapability,
    ABC,
):
    """Retain one periodic-3D arbitrary-rank support-truncation analysis."""

    __slots__ = ()


class Periodic3DRankNSupportTruncationAnalyzerRole[
    RequestT: Periodic3DRankNSupportTruncationAnalysisRequestRole,
    AnalysisT: Periodic3DRankNSupportTruncationAnalysisRole,
](
    Periodic3DSupportTruncationAnalyzer[RequestT, AnalysisT],
    Periodic3DRankNSupportTruncationCapability,
    ABC,
):
    """Execute one periodic-3D arbitrary-rank support-truncation request."""

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated operator blocks."""
        return self.request.band_subspace_rank


__all__ = [
    "Periodic3DRankNSupportTruncationAnalysisRequestRole",
    "Periodic3DRankNSupportTruncationAnalysisRole",
    "Periodic3DRankNSupportTruncationAnalyzerRole",
    "Periodic3DRankNSupportTruncationCapability",
]
