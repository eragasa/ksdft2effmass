"""Periodic-1D rank-one hopping-locality ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic1d.hopping_locality.base import (
    Periodic1DHoppingLocality,
    Periodic1DHoppingLocalityAnalysis,
    Periodic1DHoppingLocalityAnalysisRequest,
    Periodic1DHoppingLocalityAnalyzer,
)


class _Periodic1DRank1BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the unchanged scalar hopping rank."""
        return 1


class Periodic1DRank1HoppingLocalityCapability(Periodic1DHoppingLocality, ABC):
    """Identify unchanged periodic-1D rank-one hopping coefficients."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the unchanged scalar hopping rank."""


class Periodic1DRank1HoppingLocalityAnalysisRequestRole(
    _Periodic1DRank1BandSubspace,
    Periodic1DHoppingLocalityAnalysisRequest,
    Periodic1DRank1HoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-1D rank-one hopping-locality request."""

    __slots__ = ()


class Periodic1DRank1HoppingLocalityAnalysisRole(
    _Periodic1DRank1BandSubspace,
    Periodic1DHoppingLocalityAnalysis,
    Periodic1DRank1HoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-1D rank-one hopping-locality analysis."""

    __slots__ = ()


class Periodic1DRank1HoppingLocalityAnalyzerRole[
    RequestT: Periodic1DRank1HoppingLocalityAnalysisRequestRole,
    AnalysisT: Periodic1DRank1HoppingLocalityAnalysisRole,
](
    _Periodic1DRank1BandSubspace,
    Periodic1DHoppingLocalityAnalyzer[RequestT, AnalysisT],
    Periodic1DRank1HoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-1D rank-one hopping-locality request."""

    __slots__ = ()


class Periodic1DRank1HoppingLocalityValue(
    _Periodic1DRank1BandSubspace,
    Periodic1DRank1HoppingLocalityCapability,
    ABC,
):
    """Retain one standalone rank-one hopping-locality value."""

    __slots__ = ()


__all__ = [
    "Periodic1DRank1HoppingLocalityAnalysisRequestRole",
    "Periodic1DRank1HoppingLocalityAnalysisRole",
    "Periodic1DRank1HoppingLocalityAnalyzerRole",
    "Periodic1DRank1HoppingLocalityCapability",
    "Periodic1DRank1HoppingLocalityValue",
]
