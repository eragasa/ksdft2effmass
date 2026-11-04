"""Periodic-1D arbitrary-retained-dimension Bloch-hopping contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.periodic1d.model.blochhopping import (
    Periodic1DBlochHoppingModel,
)


class Periodic1DRankNBlochHoppingModel(Periodic1DBlochHoppingModel, ABC):
    """Identify a declared finite retained-dimension Bloch-hopping model.

    Notes
    -----
    Rank-N and rank-two remain sibling scientific owners. Concrete rank-N families
    must enforce their own reviewed retained-dimension inventories; ``N`` denotes the
    retained state-space dimension rather than algebraic matrix rank.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return one admitted retained-space dimension.

        Returns
        -------
        int
            Positive built-in integer fixed by the concrete rank-N family.
        """


__all__ = ["Periodic1DRankNBlochHoppingModel"]
