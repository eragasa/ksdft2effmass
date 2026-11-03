"""Periodic-1D Bloch-hopping model contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.model.blochhopping import BlochHoppingModel
from ksdft2effmass.periodic import Periodic1DModel
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry


class Periodic1DBlochHoppingModel(BlochHoppingModel, Periodic1DModel, ABC):
    """Bind ordinary hopping data to a periodic one-dimensional geometry.

    Notes
    -----
    This owner fixes the spatial dimension and requires an explicit physical lattice
    geometry. Rank-specific siblings retain responsibility for their basis-size and
    coefficient admissibility rules.
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
