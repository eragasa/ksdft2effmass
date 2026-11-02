"""Periodic-1D band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    PeriodicBandEquivalence,
    PeriodicBandEquivalenceAnalysis,
    PeriodicBandEquivalenceAnalyzer,
    PeriodicBandEquivalenceRequest,
)
from ksdft2effmass.periodic1d.base import Periodic1DCapability


class Periodic1DBandEquivalence(
    PeriodicBandEquivalence,
    Periodic1DCapability,
    ABC,
):
    """Identify band equivalence on a one-dimensional periodic lattice."""

    __slots__ = ()


class Periodic1DBandEquivalenceRequest(
    PeriodicBandEquivalenceRequest,
    Periodic1DBandEquivalence,
    ABC,
):
    """Require periodic-1D ownership for band-equivalence requests."""

    __slots__ = ()


class Periodic1DBandEquivalenceAnalysis[
    RequestT: Periodic1DBandEquivalenceRequest,
](
    PeriodicBandEquivalenceAnalysis[RequestT],
    Periodic1DBandEquivalence,
    ABC,
):
    """Require periodic-1D ownership for band-equivalence analyses."""

    __slots__ = ()


class Periodic1DBandEquivalenceAnalyzer[
    RequestT: Periodic1DBandEquivalenceRequest,
](
    Periodic1DBandEquivalence,
    PeriodicBandEquivalenceAnalyzer[RequestT],
    ABC,
):
    """Constrain periodic-1D specializations to typed request/analysis contracts."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic1DBandEquivalenceAnalysis[RequestT]:
        """Execute one periodic-1D analysis bound to the exact request type."""


__all__ = [
    "Periodic1DBandEquivalence",
    "Periodic1DBandEquivalenceAnalysis",
    "Periodic1DBandEquivalenceAnalyzer",
    "Periodic1DBandEquivalenceRequest",
]
