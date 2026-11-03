"""Periodic-1D retained-dimension-two Bloch-hopping model contract."""

from __future__ import annotations

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic1d.model.blochhopping import (
    Periodic1DBlochHoppingModel,
)


class Periodic1DRank2BlochHoppingModel(Periodic1DBlochHoppingModel, ABC):
    """Identify periodic-1D Bloch-hopping models with retained dimension two."""

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> Literal[2]:
        """Return the exact retained-space dimension two."""
        return 2


__all__ = ["Periodic1DRank2BlochHoppingModel"]
