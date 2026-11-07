"""Nominal periodic-1D arbitrary-rank scientific-model base."""

from abc import ABC, abstractmethod

from ksdft2effmass.periodic.periodic1d.models import Periodic1DModel


class Periodic1DRankNModel(Periodic1DModel, ABC):
    """Identify periodic-1D models with a declared finite band-subspace rank."""

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


__all__ = ["Periodic1DRankNModel"]
