"""Periodic-3D rank-two hopping-locality ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic3d.hopping_locality.base import (
    Periodic3DHoppingLocality,
    Periodic3DHoppingLocalityAnalysis,
    Periodic3DHoppingLocalityAnalysisRequest,
    Periodic3DHoppingLocalityAnalyzer,
)


class _Periodic3DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""
        return 2


class Periodic3DRank2HoppingLocalityCapability(Periodic3DHoppingLocality, ABC):
    """Identify unchanged periodic-3D rank-two hopping coefficients."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the unchanged hopping-block rank."""


class Periodic3DRank2HoppingLocalityAnalysisRequestRole(
    _Periodic3DRank2BandSubspace,
    Periodic3DHoppingLocalityAnalysisRequest,
    Periodic3DRank2HoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-3D rank-two hopping-locality request."""

    __slots__ = ()


class Periodic3DRank2HoppingLocalityAnalysisRole(
    _Periodic3DRank2BandSubspace,
    Periodic3DHoppingLocalityAnalysis,
    Periodic3DRank2HoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-3D rank-two hopping-locality analysis."""

    __slots__ = ()


class Periodic3DRank2HoppingLocalityAnalyzerRole[
    RequestT: Periodic3DRank2HoppingLocalityAnalysisRequestRole,
    AnalysisT: Periodic3DRank2HoppingLocalityAnalysisRole,
](
    _Periodic3DRank2BandSubspace,
    Periodic3DHoppingLocalityAnalyzer[RequestT, AnalysisT],
    Periodic3DRank2HoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-3D rank-two hopping-locality request."""

    __slots__ = ()


__all__ = [
    "Periodic3DRank2HoppingLocalityAnalysisRequestRole",
    "Periodic3DRank2HoppingLocalityAnalysisRole",
    "Periodic3DRank2HoppingLocalityAnalyzerRole",
    "Periodic3DRank2HoppingLocalityCapability",
]
