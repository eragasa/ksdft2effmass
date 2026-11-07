"""Nominal periodic-3D rank-two scientific-model base."""

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic.periodic3d.models import Periodic3DModel


class Periodic3DRank2Model(Periodic3DModel, ABC):
    """Identify periodic-3D models with retained band-subspace rank two."""

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


__all__ = ["Periodic3DRank2Model"]
