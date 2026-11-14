"""Periodic-2D arbitrary-rank gauge-alignment ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, cast

from ksdft2effmass.gauge_alignment.base import (
    GaugeAlignmentGroupIdentity,
    PeriodicRankNGaugeAlignmentCapability,
)
from ksdft2effmass.periodic2d.gauge_alignment.base import (
    Periodic2DGaugeAlignment,
    Periodic2DGaugeAlignmentAnalysis,
    Periodic2DGaugeAlignmentAnalysisRequest,
    Periodic2DGaugeAlignmentAnalyzer,
)


class _GaugeGroupIdentityOwner(Protocol):
    @property
    def gauge_group_identity(self) -> GaugeAlignmentGroupIdentity:
        """Return the finite gauge-group identity."""


class _Periodic2DRankNBandSubspace:
    __slots__ = ()

    @property
    def band_subspace_rank(self) -> int:
        """Return the represented band-subspace rank for this alignment."""
        owner = cast(_GaugeGroupIdentityOwner, self)
        return owner.gauge_group_identity.represented_dimension


class Periodic2DRankNGaugeAlignmentCapability(
    Periodic2DGaugeAlignment,
    PeriodicRankNGaugeAlignmentCapability,
    ABC,
):
    """Identify gauge alignment on a periodic-2D finite-rank band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the represented band-subspace rank for this alignment."""


class Periodic2DRankNGaugeAlignmentAnalysisRequest(
    _Periodic2DRankNBandSubspace,
    Periodic2DGaugeAlignmentAnalysisRequest,
    Periodic2DRankNGaugeAlignmentCapability,
    ABC,
):
    """Bind one periodic-2D arbitrary-rank gauge-alignment request."""

    __slots__ = ()


class Periodic2DRankNGaugeAlignmentAnalysis(
    _Periodic2DRankNBandSubspace,
    Periodic2DGaugeAlignmentAnalysis,
    Periodic2DRankNGaugeAlignmentCapability,
    ABC,
):
    """Retain one periodic-2D arbitrary-rank gauge-alignment analysis."""

    __slots__ = ()


class Periodic2DRankNGaugeAlignmentAnalyzer[
    RequestT: Periodic2DRankNGaugeAlignmentAnalysisRequest,
    AnalysisT: Periodic2DRankNGaugeAlignmentAnalysis,
](
    _Periodic2DRankNBandSubspace,
    Periodic2DGaugeAlignmentAnalyzer[RequestT, AnalysisT],
    Periodic2DRankNGaugeAlignmentCapability,
    ABC,
):
    """Execute one periodic-2D arbitrary-rank gauge-alignment request."""

    __slots__ = ()


__all__ = [
    "Periodic2DRankNGaugeAlignmentCapability",
    "Periodic2DRankNGaugeAlignmentAnalysis",
    "Periodic2DRankNGaugeAlignmentAnalysisRequest",
    "Periodic2DRankNGaugeAlignmentAnalyzer",
]
