"""Periodic-3D arbitrary-rank gauge-alignment ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, cast

from ksdft2effmass.gauge_alignment.base import (
    GaugeAlignmentGroupIdentity,
    PeriodicRankNGaugeAlignmentCapability,
)
from ksdft2effmass.periodic3d.gauge_alignment.base import (
    Periodic3DGaugeAlignment,
    Periodic3DGaugeAlignmentAnalysis,
    Periodic3DGaugeAlignmentAnalysisRequest,
    Periodic3DGaugeAlignmentAnalyzer,
)


class _GaugeGroupIdentityOwner(Protocol):
    @property
    def gauge_group_identity(self) -> GaugeAlignmentGroupIdentity:
        """Return the finite gauge-group identity."""


class _Periodic3DRankNBandSubspace:
    __slots__ = ()

    @property
    def band_subspace_rank(self) -> int:
        """Return the represented band-subspace rank for this alignment."""
        owner = cast(_GaugeGroupIdentityOwner, self)
        return owner.gauge_group_identity.represented_dimension


class Periodic3DRankNGaugeAlignmentCapability(
    Periodic3DGaugeAlignment,
    PeriodicRankNGaugeAlignmentCapability,
    ABC,
):
    """Identify gauge alignment on a periodic-3D finite-rank band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the represented band-subspace rank for this alignment."""


class Periodic3DRankNGaugeAlignmentAnalysisRequest(
    _Periodic3DRankNBandSubspace,
    Periodic3DGaugeAlignmentAnalysisRequest,
    Periodic3DRankNGaugeAlignmentCapability,
    ABC,
):
    """Bind one periodic-3D arbitrary-rank gauge-alignment request."""

    __slots__ = ()


class Periodic3DRankNGaugeAlignmentAnalysis(
    _Periodic3DRankNBandSubspace,
    Periodic3DGaugeAlignmentAnalysis,
    Periodic3DRankNGaugeAlignmentCapability,
    ABC,
):
    """Retain one periodic-3D arbitrary-rank gauge-alignment analysis."""

    __slots__ = ()


class Periodic3DRankNGaugeAlignmentAnalyzer[
    RequestT: Periodic3DRankNGaugeAlignmentAnalysisRequest,
    AnalysisT: Periodic3DRankNGaugeAlignmentAnalysis,
](
    _Periodic3DRankNBandSubspace,
    Periodic3DGaugeAlignmentAnalyzer[RequestT, AnalysisT],
    Periodic3DRankNGaugeAlignmentCapability,
    ABC,
):
    """Execute one periodic-3D arbitrary-rank gauge-alignment request."""

    __slots__ = ()


__all__ = [
    "Periodic3DRankNGaugeAlignmentCapability",
    "Periodic3DRankNGaugeAlignmentAnalysis",
    "Periodic3DRankNGaugeAlignmentAnalysisRequest",
    "Periodic3DRankNGaugeAlignmentAnalyzer",
]
