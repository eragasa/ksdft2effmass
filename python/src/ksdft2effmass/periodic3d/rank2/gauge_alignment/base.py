"""Periodic-3D rank-two gauge-alignment ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.gauge_alignment.base import (
    Periodic3DGaugeAlignment,
    Periodic3DGaugeAlignmentAnalysis,
    Periodic3DGaugeAlignmentAnalysisRequest,
    Periodic3DGaugeAlignmentAnalyzer,
)


class _Periodic3DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""
        return 2


class Periodic3DRank2GaugeAlignment(Periodic3DGaugeAlignment, ABC):
    """Identify gauge alignment on a periodic-3D rank-two band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""


class Periodic3DRank2GaugeAlignmentAnalysisRequest(
    _Periodic3DRank2BandSubspace,
    Periodic3DGaugeAlignmentAnalysisRequest,
    Periodic3DRank2GaugeAlignment,
    ABC,
):
    """Bind one periodic-3D rank-two gauge-alignment request."""

    __slots__ = ()


class Periodic3DRank2GaugeAlignmentAnalysis(
    _Periodic3DRank2BandSubspace,
    Periodic3DGaugeAlignmentAnalysis,
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
    Periodic3DGaugeAlignmentAnalyzer[RequestT, AnalysisT],
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
