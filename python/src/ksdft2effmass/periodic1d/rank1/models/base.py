"""Nominal periodic-1D rank-one scientific-model base."""

from abc import ABC
from typing import Literal, final

from ksdft2effmass.periodic.periodic1d.models import Periodic1DModel


class Periodic1DRank1Model(Periodic1DModel, ABC):
    """Identify periodic-1D models with retained band-subspace rank one."""

    __slots__ = ()

    @property
    @final
    def band_subspace_rank(self) -> Literal[1]:
        """Return the exact retained band-subspace rank one."""
        return 1


__all__ = ["Periodic1DRank1Model"]
