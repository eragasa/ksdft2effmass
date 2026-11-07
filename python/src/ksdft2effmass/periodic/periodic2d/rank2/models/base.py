"""Nominal periodic-2D rank-two scientific-model base."""

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic.periodic2d.models import Periodic2DModel


class Periodic2DRank2Model(Periodic2DModel, ABC):
    """Identify periodic-2D models with retained band-subspace rank two."""

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> Literal[2]:
        """Return the exact retained band-subspace rank two.

        Returns
        -------
        Literal[2]
            Built-in integer two.

        """
        return 2


__all__ = ["Periodic2DRank2Model"]
