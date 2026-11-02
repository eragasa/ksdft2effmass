"""Periodic-1D rank-two aggregate ownership guardrails."""

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


class _Periodic1DRank2BandSubspace:
    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> int:
        """Return the fixed represented band-subspace rank."""
        return 2


class Periodic1DRank2BandEquivalenceHoppingLocalityCapability(
    Periodic1DBandEquivalenceHoppingLocality,
    ABC,
):
    """Coordinate one periodic-1D rank-two aggregate study."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the represented band-subspace rank."""


class Periodic1DRank2BandEquivalenceHoppingLocalityRequestRole(
    _Periodic1DRank2BandSubspace,
    Periodic1DBandEquivalenceHoppingLocalityRequest,
    Periodic1DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Bind one periodic-1D rank-two aggregate request."""

    __slots__ = ()


class Periodic1DRank2BandEquivalenceHoppingLocalityAnalysisRole[
    RequestT: Periodic1DRank2BandEquivalenceHoppingLocalityRequestRole,
](
    _Periodic1DRank2BandSubspace,
    Periodic1DBandEquivalenceHoppingLocalityAnalysis[RequestT],
    Periodic1DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Retain one periodic-1D rank-two aggregate analysis."""

    __slots__ = ()


class Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzerRole[
    RequestT: Periodic1DRank2BandEquivalenceHoppingLocalityRequestRole,
](
    _Periodic1DRank2BandSubspace,
    Periodic1DBandEquivalenceHoppingLocalityAnalyzer[RequestT],
    Periodic1DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):
    """Execute one periodic-1D rank-two aggregate request."""

    __slots__ = ()

    @abstractmethod
    def execute(
        self,
    ) -> Periodic1DRank2BandEquivalenceHoppingLocalityAnalysisRole[RequestT]:
        """Execute the bound rank-two aggregate."""


class Periodic1DRank2BandEquivalenceHoppingLocalityValue(
    _Periodic1DRank2BandSubspace,
    Periodic1DBandEquivalenceHoppingLocalityValue,
    Periodic1DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):  # noqa: B024
    """Retain one standalone rank-two aggregate value."""

    __slots__ = ()


class Periodic1DRank2BandEquivalenceHoppingLocalityAction(
    _Periodic1DRank2BandSubspace,
    Periodic1DBandEquivalenceHoppingLocalityAction,
    Periodic1DRank2BandEquivalenceHoppingLocalityCapability,
    ABC,
):  # noqa: B024
    """Perform one supporting rank-two aggregate action."""

    __slots__ = ()


__all__ = [
    "Periodic1DRank2BandEquivalenceHoppingLocalityAction",
    "Periodic1DRank2BandEquivalenceHoppingLocalityAnalysisRole",
    "Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzerRole",
    "Periodic1DRank2BandEquivalenceHoppingLocalityCapability",
    "Periodic1DRank2BandEquivalenceHoppingLocalityRequestRole",
    "Periodic1DRank2BandEquivalenceHoppingLocalityValue",
]
