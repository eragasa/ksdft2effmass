"""Nominal periodic-3D arbitrary-rank scientific-model base."""

from abc import ABC, abstractmethod

from ksdft2effmass.periodic.periodic3d.models import Periodic3DModel


class Periodic3DRankNModel(Periodic3DModel, ABC):
    """Identify periodic-3D models with a declared finite band-subspace rank."""

    __slots__ = ()

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the concrete family's admitted finite band-subspace rank.

        Returns
        -------
        int
            Positive built-in retained-space dimension supplied by a concrete family.

        """


__all__ = ["Periodic3DRankNModel"]
