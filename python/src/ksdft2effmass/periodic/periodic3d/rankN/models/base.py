"""Nominal periodic-3D arbitrary-rank scientific-model base."""

from abc import ABC, abstractmethod

from ksdft2effmass.periodic.periodic3d.models import Periodic3DModel
from ksdft2effmass.periodic.periodic3d.operators import Periodic3DBasisIdentity


class Periodic3DRankNModel(Periodic3DModel, ABC):
    """Identify periodic-3D models with an explicit finite retained basis.

    Notes
    -----
    Spatial dimension and retained rank are independent. This owner fixes spatial
    dimension three while concrete descendants provide both a positive retained rank
    and an exact ordered :class:`Periodic3DBasisIdentity` of that size.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def basis_identity(self) -> Periodic3DBasisIdentity:
        """Return the exact ordered basis of the retained band subspace.

        Returns
        -------
        Periodic3DBasisIdentity
            Compatibility-bearing coordinate sequence for the retained
            three-dimensional periodic operator space.

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


__all__ = ["Periodic3DRankNModel"]
