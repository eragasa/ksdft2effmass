"""Periodic-1D Bloch-hopping model contract."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.model.blochhopping import BlochHoppingModel
from ksdft2effmass.periodic import Periodic1DModel
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry


class Periodic1DBlochHoppingModel(BlochHoppingModel, Periodic1DModel, ABC):
    """Bind ordinary hopping data to one explicit periodic-1D lattice geometry."""

    __slots__ = ()

    @property
    @abstractmethod
    def lattice_geometry(self) -> Periodic1DLatticeGeometry:
        """Return the explicit physical one-dimensional lattice geometry."""


__all__ = ["Periodic1DBlochHoppingModel"]
