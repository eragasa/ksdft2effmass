"""Periodic-3D rank-two gauge-alignment ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.rankN.gauge_alignment.base import (
    Periodic3DRankNGaugeAlignmentAnalysis,
    Periodic3DRankNGaugeAlignmentAnalysisRequest,
    Periodic3DRankNGaugeAlignmentAnalyzer,
    Periodic3DRankNGaugeAlignmentCapability,
)


class _Periodic3DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""
        return 2


class Periodic3DRank2GaugeAlignment(
    Periodic3DRankNGaugeAlignmentCapability,
    ABC,
):
    """Refine finite-rank periodic-3D gauge alignment to rank two."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""


class Periodic3DRank2GaugeAlignmentAnalysisRequest(
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNGaugeAlignmentAnalysisRequest,
    Periodic3DRank2GaugeAlignment,
    ABC,
):
    """Bind one periodic-3D rank-two gauge-alignment request."""

    __slots__ = ()


class Periodic3DRank2GaugeAlignmentAnalysis(
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNGaugeAlignmentAnalysis,
    Periodic3DRank2GaugeAlignment,
    ABC,
):
    """Retain one periodic-3D rank-two gauge-alignment analysis."""

    __slots__ = ()


class Periodic3DRank2GaugeAlignmentAnalyzer[
    RequestT: Periodic3DRank2GaugeAlignmentAnalysisRequest,
    AnalysisT: Periodic3DRank2GaugeAlignmentAnalysis,
](
    _Periodic3DRank2BandSubspace,
    Periodic3DRankNGaugeAlignmentAnalyzer[RequestT, AnalysisT],
    Periodic3DRank2GaugeAlignment,
    ABC,
):
    """Execute one periodic-3D rank-two gauge-alignment request."""

    __slots__ = ()


__all__ = [
    "Periodic3DRank2GaugeAlignment",
    "Periodic3DRank2GaugeAlignmentAnalysis",
    "Periodic3DRank2GaugeAlignmentAnalysisRequest",
    "Periodic3DRank2GaugeAlignmentAnalyzer",
]
