"""Periodic-1D rank-two gauge-alignment ownership guardrail."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.periodic1d.rankN.gauge_alignment.base import (
    Periodic1DRankNGaugeAlignmentCapability,
)


class Periodic1DRank2GaugeAlignment(
    Periodic1DRankNGaugeAlignmentCapability,
    ABC,
):
    """Refine finite-rank periodic-1D gauge alignment to rank two."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the rank of the represented band subspace at each momentum."""


__all__ = ["Periodic1DRank2GaugeAlignment"]
