"""Periodic-3D band-equivalence ownership guardrails."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.analysis.model_adequacy.band_equivalence.base import (
    PeriodicBandEquivalence,
    PeriodicBandEquivalenceAnalysis,
    PeriodicBandEquivalenceAnalyzer,
    PeriodicBandEquivalenceRequest,
)
from ksdft2effmass.periodic3d.base import Periodic3DCapability


class Periodic3DBandEquivalence(
    PeriodicBandEquivalence,
    Periodic3DCapability,
    ABC,
):
    """Identify band equivalence on a three-dimensional periodic lattice."""

    __slots__ = ()


class Periodic3DBandEquivalenceRequest(
    PeriodicBandEquivalenceRequest,
    Periodic3DBandEquivalence,
    ABC,
):
    """Require periodic-3D ownership for band-equivalence requests."""

    __slots__ = ()


class Periodic3DBandEquivalenceAnalysis[
    RequestT: Periodic3DBandEquivalenceRequest,
](
    PeriodicBandEquivalenceAnalysis[RequestT],
    Periodic3DBandEquivalence,
    ABC,
):
    """Require periodic-3D ownership for band-equivalence analyses."""

    __slots__ = ()


class Periodic3DBandEquivalenceAnalyzer[
    RequestT: Periodic3DBandEquivalenceRequest,
](
    Periodic3DBandEquivalence,
    PeriodicBandEquivalenceAnalyzer[RequestT],
    ABC,
):
    """Constrain periodic-3D specializations to typed request/analysis contracts."""

    __slots__ = ()

    @abstractmethod
    def execute(self) -> Periodic3DBandEquivalenceAnalysis[RequestT]:
        """Execute one periodic-3D analysis bound to the exact request type."""


__all__ = [
    "Periodic3DBandEquivalence",
    "Periodic3DBandEquivalenceAnalysis",
    "Periodic3DBandEquivalenceAnalyzer",
    "Periodic3DBandEquivalenceRequest",
]
