"""Periodic-1D Bloch-hopping model contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.models.blochhopping import BlochHoppingModel
from ksdft2effmass.periodic.periodic1d.models.base import Periodic1DModel
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry


class Periodic1DBlochHoppingModel(BlochHoppingModel, Periodic1DModel, ABC):
    """Bind ordinary hopping data to a periodic one-dimensional geometry.

    Notes
    -----
    This owner fixes the spatial dimension and requires an explicit physical lattice
    geometry. Finite-rank descendants retain responsibility for structured basis,
    retained-rank, and coefficient-admissibility rules; fixed-rank descendants may
    refine those finite-rank contracts further.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def lattice_geometry(self) -> Periodic1DLatticeGeometry:
        """Return the physical one-dimensional lattice geometry.

        Returns
        -------
        Periodic1DLatticeGeometry
            Immutable primitive-period convention associated with the hopping model.
        """


__all__ = ["Periodic1DBlochHoppingModel"]
