"""Periodic-1D rank-two gauge-alignment ownership guardrail."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.periodic1d.gauge_alignment.base import Periodic1DGaugeAlignment


class Periodic1DRank2GaugeAlignment(Periodic1DGaugeAlignment, ABC):
    """Identify gauge alignment on a periodic-1D rank-two band subspace."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""


__all__ = ["Periodic1DRank2GaugeAlignment"]
