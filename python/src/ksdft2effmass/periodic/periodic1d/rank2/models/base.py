"""Nominal periodic-1D rank-two scientific-model base."""

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic.periodic1d.models import Periodic1DModel


class Periodic1DRank2Model(Periodic1DModel, ABC):
    """Identify periodic-1D models with retained band-subspace rank two."""

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


__all__ = ["Periodic1DRank2Model"]
