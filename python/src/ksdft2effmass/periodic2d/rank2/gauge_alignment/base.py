"""Periodic-2D rank-two gauge-alignment ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic2d.gauge_alignment.base import (
    Periodic2DGaugeAlignment,
    Periodic2DGaugeAlignmentAnalysis,
    Periodic2DGaugeAlignmentAnalysisRequest,
    Periodic2DGaugeAlignmentAnalyzer,
)


class _Periodic2DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""
        return 2


class Periodic2DRank2GaugeAlignment(Periodic2DGaugeAlignment, ABC):
    """Identify gauge alignment on a periodic-2D rank-two band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""


class Periodic2DRank2GaugeAlignmentAnalysisRequest(
    _Periodic2DRank2BandSubspace,
    Periodic2DGaugeAlignmentAnalysisRequest,
    Periodic2DRank2GaugeAlignment,
    ABC,
):
    """Bind one periodic-2D rank-two gauge-alignment request."""

    __slots__ = ()


class Periodic2DRank2GaugeAlignmentAnalysis(
    _Periodic2DRank2BandSubspace,
    Periodic2DGaugeAlignmentAnalysis,
    Periodic2DRank2GaugeAlignment,
    ABC,
):
    """Retain one periodic-2D rank-two gauge-alignment analysis."""

    __slots__ = ()


class Periodic2DRank2GaugeAlignmentAnalyzer[
    RequestT: Periodic2DRank2GaugeAlignmentAnalysisRequest,
    AnalysisT: Periodic2DRank2GaugeAlignmentAnalysis,
](
    _Periodic2DRank2BandSubspace,
    Periodic2DGaugeAlignmentAnalyzer[RequestT, AnalysisT],
    Periodic2DRank2GaugeAlignment,
    ABC,
):
    """Execute one periodic-2D rank-two gauge-alignment request."""

    __slots__ = ()


__all__ = [
    "Periodic2DRank2GaugeAlignment",
    "Periodic2DRank2GaugeAlignmentAnalysis",
    "Periodic2DRank2GaugeAlignmentAnalysisRequest",
    "Periodic2DRank2GaugeAlignmentAnalyzer",
]
