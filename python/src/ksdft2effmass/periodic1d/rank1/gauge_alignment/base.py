"""Periodic-1D rank-one gauge-alignment ownership guardrail."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.periodic1d.gauge_alignment.base import Periodic1DGaugeAlignment


class Periodic1DRank1GaugeAlignment(Periodic1DGaugeAlignment, ABC):
    """Identify the operator-trivial U(1) alignment boundary in periodic 1D."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the scalar band-subspace rank."""


__all__ = ["Periodic1DRank1GaugeAlignment"]
