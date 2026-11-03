"""Periodic-1D arbitrary-retained-dimension Bloch-hopping model contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.periodic1d.model.blochhopping import (
    Periodic1DBlochHoppingModel,
)


class Periodic1DRankNBlochHoppingModel(Periodic1DBlochHoppingModel, ABC):
    """Identify a declared finite retained-dimension Bloch-hopping model.

    Rank-N and rank-two remain sibling scientific owners. Concrete rank-N families must
    enforce their own reviewed retained-dimension inventories.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return one admitted retained-space dimension."""


__all__ = ["Periodic1DRankNBlochHoppingModel"]
