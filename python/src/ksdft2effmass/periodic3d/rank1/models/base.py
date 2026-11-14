"""Nominal periodic-3D rank-one scientific-model base."""

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic.periodic3d.models import Periodic3DModel


class Periodic3DRank1Model(Periodic3DModel, ABC):
    """Identify periodic-3D models with retained band-subspace rank one."""

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> Literal[1]:
        """Return the exact retained band-subspace rank one."""
        return 1


__all__ = ["Periodic3DRank1Model"]
