"""Periodic-1D rank-one support-truncation ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic1d.support_truncation.base import (
    Periodic1DSupportTruncation,
    Periodic1DSupportTruncationAnalysis,
    Periodic1DSupportTruncationAnalysisRequest,
    Periodic1DSupportTruncationAnalyzer,
)


class _Periodic1DRank1BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated scalar representation."""
        return 1


class Periodic1DRank1SupportTruncationCapability(
    Periodic1DSupportTruncation,
    ABC,
):
    """Identify periodic-1D rank-one support truncation."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the support-truncated scalar representation."""


class Periodic1DRank1SupportTruncationAnalysisRequestRole(
    _Periodic1DRank1BandSubspace,
    Periodic1DSupportTruncationAnalysisRequest,
    Periodic1DRank1SupportTruncationCapability,
    ABC,
):
    """Bind one periodic-1D rank-one support-truncation request."""

    __slots__ = ()


class Periodic1DRank1SupportTruncationAnalysisRole(
    _Periodic1DRank1BandSubspace,
    Periodic1DSupportTruncationAnalysis,
    Periodic1DRank1SupportTruncationCapability,
    ABC,
):
    """Retain one periodic-1D rank-one support-truncation analysis."""

    __slots__ = ()


class Periodic1DRank1SupportTruncationAnalyzerRole[
    RequestT: Periodic1DRank1SupportTruncationAnalysisRequestRole,
    AnalysisT: Periodic1DRank1SupportTruncationAnalysisRole,
](
    _Periodic1DRank1BandSubspace,
    Periodic1DSupportTruncationAnalyzer[RequestT, AnalysisT],
    Periodic1DRank1SupportTruncationCapability,
    ABC,
):
    """Execute one periodic-1D rank-one support-truncation request."""

    __slots__ = ()


class Periodic1DRank1SupportTruncationValue(
    _Periodic1DRank1BandSubspace,
    Periodic1DRank1SupportTruncationCapability,
    ABC,
):
    """Retain one standalone rank-one support-truncation value."""

    __slots__ = ()


__all__ = [
    "Periodic1DRank1SupportTruncationAnalysisRequestRole",
    "Periodic1DRank1SupportTruncationAnalysisRole",
    "Periodic1DRank1SupportTruncationAnalyzerRole",
    "Periodic1DRank1SupportTruncationCapability",
    "Periodic1DRank1SupportTruncationValue",
]
