"""PhysKit-backed direct and reciprocal geometry for periodic one dimension."""

from __future__ import annotations

import math
from abc import ABC
from dataclasses import dataclass
from typing import final

from projectkoios.physkit.periodic.lattice import (
    DirectLattice1D,
    ReciprocalLattice1D,
)
from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)


@dataclass(frozen=True, slots=True)
class Periodic1DLatticeGeometry:
    """Retain one immutable scalar snapshot of a one-dimensional lattice period.

    ``lattice_period`` uses one caller-declared consistent length convention. The
    PhysKit lattice objects are reconstructed from that immutable scalar so mutating a
    returned object cannot mutate this scientific value.
    """

    lattice_period: float

    def __post_init__(self) -> None:
        if type(self.lattice_period) is not float:
            raise TypeError("lattice_period must be a built-in float")
        if not math.isfinite(self.lattice_period) or self.lattice_period <= 0.0:
            raise ValueError("lattice_period must be finite and positive")

    @property
    def direct_lattice(self) -> DirectLattice1D:
        """Return a fresh PhysKit direct lattice with period ``a_0``."""
        return DirectLattice1D(self.lattice_period)

    @property
    def reciprocal_lattice(self) -> ReciprocalLattice1D:
        """Return the PhysKit reciprocal lattice with ``G = 2 pi / a_0``."""
        return ReciprocalLattice1D.from_direct_lattice(self.direct_lattice)

    def direct_translation(self, displacement: LatticeDisplacement) -> float:
        """Map one PhysKit 1D displacement index to ``R_n = n a_0``."""
        if type(displacement) is not LatticeDisplacement:
            raise TypeError("displacement must be an exact LatticeDisplacement")
        if displacement.dimension is not LatticeDimension.ONE:
            raise ValueError("displacement must have lattice dimension one")
        return self.direct_lattice.translation(displacement.components[0])

    def bloch_wavenumber(self, reduced_coordinate: float) -> float:
        """Map dimensionless ``q`` to ``k = G q`` in the reciprocal length unit."""
        if type(reduced_coordinate) is not float:
            raise TypeError("reduced_coordinate must be a built-in float")
        if not math.isfinite(reduced_coordinate):
            raise ValueError("reduced_coordinate must be finite")
        return self.reciprocal_lattice.b1 * reduced_coordinate

    def reduced_coordinate(self, bloch_wavenumber: float) -> float:
        """Map a finite Bloch wavenumber to dimensionless ``q = k / G``."""
        if type(bloch_wavenumber) is not float:
            raise TypeError("bloch_wavenumber must be a built-in float")
        if not math.isfinite(bloch_wavenumber):
            raise ValueError("bloch_wavenumber must be finite")
        return bloch_wavenumber / self.reciprocal_lattice.b1


class Periodic1DReducedCoordinateConvention(  # noqa: B024 - nominal convention marker
    ABC
):
    """Nominally identify the centered reduced-coordinate convention.

    Current controlled 1D studies calculate in ``q`` and therefore do not claim a
    physical value of ``a_0``. The normalized lattice has ``a_0 = 1`` in reduced direct
    units and ``G = 2 pi`` in the corresponding reciprocal units. A physical or other
    declared period is represented by constructing :class:`Periodic1DLatticeGeometry`
    with that period; it is never inferred from the normalized value.
    """

    __slots__ = ()

    @property
    @final
    def reduced_lattice_geometry(self) -> Periodic1DLatticeGeometry:
        """Return the explicit ``a_0 = 1`` reduced-unit geometry."""
        return Periodic1DLatticeGeometry(lattice_period=1.0)


__all__ = [
    "Periodic1DLatticeGeometry",
    "Periodic1DReducedCoordinateConvention",
]
