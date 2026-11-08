"""Nominal periodic-2D arbitrary-rank scientific-model base."""

from abc import ABC, abstractmethod

from ksdft2effmass.periodic.periodic2d.models import Periodic2DModel
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity


class Periodic2DRankNModel(Periodic2DModel, ABC):
    """Identify periodic-2D models with an explicit finite retained basis.

    Notes
    -----
    Spatial dimension and retained rank are independent. This owner fixes spatial
    dimension two while concrete descendants provide both a positive retained rank
    and an exact ordered :class:`Periodic2DBasisIdentity` of that size.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def basis_identity(self) -> Periodic2DBasisIdentity:
        """Return the exact ordered basis of the retained band subspace.

        Returns
        -------
        Periodic2DBasisIdentity
            Compatibility-bearing coordinate sequence for the retained two-dimensional
            periodic operator space.

        Notes
        -----
        Concrete families must establish this identity explicitly. Provider labels,
        model names, retained rank, geometry, and hopping support do not determine it.
        """

    @property
    @abstractmethod
    def band_subspace_rank(self) -> int:
        """Return the concrete family's admitted finite band-subspace rank.

        Returns
        -------
        int
            Positive built-in retained-space dimension supplied by a concrete family.

        """


__all__ = ["Periodic2DRankNModel"]
