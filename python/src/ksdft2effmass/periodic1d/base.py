"""Shared dimensional contract for periodic one-dimensional capabilities."""

from __future__ import annotations

from abc import ABC
from typing import final

from projectkoios.physkit.periodic.lattice.finite_domain import LatticeDimension


class Periodic1DCapability(ABC):  # noqa: B024 - dimensional capability owner
    """Identify a capability whose periodic lattice domain has dimension one.

    This base fixes only the lattice dimension. It does not choose a direct-lattice
    period, physical unit, reciprocal-coordinate convention, mesh, basis, gauge,
    translation inventory, support policy, numerical algorithm, or wire format.
    Concrete domain bases retain ownership of those stronger contracts.
    """

    __slots__ = ()

    @property
    @final
    def lattice_dimension(self) -> LatticeDimension:
        """Return the exact one-dimensional PhysKit lattice identity."""
        return LatticeDimension.ONE


__all__ = ["Periodic1DCapability"]
