"""Periodic-1D rank-N aggregate ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final

from ksdft2effmass.periodic1d.band_equivalence_hopping_locality.base import (
    Periodic1DBandEquivalenceHoppingLocality,
    Periodic1DBandEquivalenceHoppingLocalityAction,
    Periodic1DBandEquivalenceHoppingLocalityAnalysis,
    Periodic1DBandEquivalenceHoppingLocalityAnalyzer,
    Periodic1DBandEquivalenceHoppingLocalityRequest,
    Periodic1DBandEquivalenceHoppingLocalityValue,
)


class Periodic1DRankNBandEquivalenceHoppingLocalityCapability(
    Periodic1DBandEquivalenceHoppingLocality,
    ABC,
):
    """Coordinate one finite-rank case in the periodic-1D rank-N family."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the represented band-subspace rank."""


class Periodic1DRankNBandEquivalenceHoppingLocalityRequestRole(
    Periodic1DBandEquivalenceHoppingLocalityRequest,
    Periodic1DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-1D rank-N aggregate request."""

    __slots__ = ()


class Periodic1DRankNBandEquivalenceHoppingLocalityAnalysisRole[
    RequestT: Periodic1DRankNBandEquivalenceHoppingLocalityRequestRole,
](
    Periodic1DBandEquivalenceHoppingLocalityAnalysis[RequestT],
    Periodic1DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-1D rank-N aggregate analysis."""

    __slots__ = ()


class Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzerRole[
    RequestT: Periodic1DRankNBandEquivalenceHoppingLocalityRequestRole,
](
    Periodic1DBandEquivalenceHoppingLocalityAnalyzer[RequestT],
    Periodic1DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-1D rank-N aggregate request."""

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the bound request's band-subspace rank."""
        return self.request.band_subspace_rank

    @abstractmethod
    def execute(
        self,
    ) -> Periodic1DRankNBandEquivalenceHoppingLocalityAnalysisRole[RequestT]:
        """Execute the bound rank-N aggregate."""


class Periodic1DRankNBandEquivalenceHoppingLocalityValue(
    Periodic1DBandEquivalenceHoppingLocalityValue,
    Periodic1DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one standalone finite-rank aggregate value."""

    __slots__ = ()


class Periodic1DRankNBandEquivalenceHoppingLocalityAction(
    Periodic1DBandEquivalenceHoppingLocalityAction,
    Periodic1DRankNBandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Perform one supporting finite-rank aggregate action."""

    __slots__ = ()


__all__ = [
    "Periodic1DRankNBandEquivalenceHoppingLocalityAction",
    "Periodic1DRankNBandEquivalenceHoppingLocalityAnalysisRole",
    "Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzerRole",
    "Periodic1DRankNBandEquivalenceHoppingLocalityCapability",
    "Periodic1DRankNBandEquivalenceHoppingLocalityRequestRole",
    "Periodic1DRankNBandEquivalenceHoppingLocalityValue",
]
