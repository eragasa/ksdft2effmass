"""Nominal periodic-2D rank-one scientific-model base."""

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic.periodic2d.models import Periodic2DModel


class Periodic2DRank1Model(Periodic2DModel, ABC):
    """Identify periodic-2D models with retained band-subspace rank one."""

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> Literal[1]:
        """Return the exact retained band-subspace rank one."""
        return 1


__all__ = ["Periodic2DRank1Model"]
