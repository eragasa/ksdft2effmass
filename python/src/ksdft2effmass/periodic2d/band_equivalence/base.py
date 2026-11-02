"""Periodic-2D band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    PeriodicBandEquivalence,
    PeriodicBandEquivalenceAnalysis,
    PeriodicBandEquivalenceAnalyzer,
    PeriodicBandEquivalenceRequest,
)
from ksdft2effmass.periodic2d.base import Periodic2DCapability


class Periodic2DBandEquivalence(
    PeriodicBandEquivalence,
    Periodic2DCapability,
    ABC,
):
    """Identify band equivalence on a two-dimensional periodic lattice."""

    __slots__ = ()


class Periodic2DBandEquivalenceRequest(
    PeriodicBandEquivalenceRequest,
    Periodic2DBandEquivalence,
    ABC,
):
    """Require periodic-2D ownership for band-equivalence requests."""

    __slots__ = ()


class Periodic2DBandEquivalenceAnalysis[
    RequestT: Periodic2DBandEquivalenceRequest,
](
    PeriodicBandEquivalenceAnalysis[RequestT],
    Periodic2DBandEquivalence,
    ABC,
):
    """Require periodic-2D ownership for band-equivalence analyses."""

    __slots__ = ()


class Periodic2DBandEquivalenceAnalyzer[
    RequestT: Periodic2DBandEquivalenceRequest,
](
    Periodic2DBandEquivalence,
    PeriodicBandEquivalenceAnalyzer[RequestT],
    ABC,
):
    """Constrain periodic-2D specializations to typed request/analysis contracts."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic2DBandEquivalenceAnalysis[RequestT]:
        """Execute one periodic-2D analysis bound to the exact request type."""


__all__ = [
    "Periodic2DBandEquivalence",
    "Periodic2DBandEquivalenceAnalysis",
    "Periodic2DBandEquivalenceAnalyzer",
    "Periodic2DBandEquivalenceRequest",
]
