"""Periodic-1D arbitrary-rank gauge-alignment ownership guardrail."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.periodic1d.gauge_alignment.base import Periodic1DGaugeAlignment


class Periodic1DRankNGaugeAlignmentCapability(Periodic1DGaugeAlignment, ABC):
    """Identify gauge alignment on a periodic-1D finite-rank band subspace.

    The ``Capability`` suffix distinguishes this owner from the existing
    ``Periodic1DRankNGaugeAlignment`` route vocabulary. A later vocabulary cleanup may
    free the shorter capability name without changing this scientific contract.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the represented band-subspace rank for this alignment."""


__all__ = ["Periodic1DRankNGaugeAlignmentCapability"]
