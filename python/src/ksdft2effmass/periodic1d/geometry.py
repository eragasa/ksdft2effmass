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
from projectkoios.physkit.units import (
    ModelSystemUnitConverter,
    PhysicalUnit,
    ScalarQuantity,
)


@dataclass(frozen=True, slots=True)
class Periodic1DLatticeGeometry:
    """Retain one immutable scalar snapshot of a one-dimensional lattice period.

    ``lattice_period`` is expressed in the explicit physical length unit selected by
    the caller. PhysKit lattice objects are reconstructed from the immutable scalar so
    mutating a returned object cannot mutate this scientific value. Choices such as
    ``a_0 = 1 bohr`` remain unit-aware; this value does not own mass or action scales.
    """

    lattice_period: float
    lattice_unit: PhysicalUnit

    def __post_init__(self) -> None:
        if type(self.lattice_period) is not float:
            raise TypeError("lattice_period must be a built-in float")
        if not math.isfinite(self.lattice_period) or self.lattice_period <= 0.0:
            raise ValueError("lattice_period must be finite and positive")
        if type(self.lattice_unit) is not PhysicalUnit:
            raise TypeError("lattice_unit must be PhysicalUnit")
        if not ModelSystemUnitConverter.compatible(
            self.lattice_unit,
            PhysicalUnit("meter"),
        ):
            raise ValueError("lattice_unit must have length dimensionality")

    @classmethod
    def from_direct_lattice(
        cls,
        direct_lattice: DirectLattice1D,
        lattice_unit: PhysicalUnit,
    ) -> Periodic1DLatticeGeometry:
        """Snapshot one explicit PhysKit direct lattice without retaining mutation."""
        if type(direct_lattice) is not DirectLattice1D:
            raise TypeError("direct_lattice must be the exact PhysKit DirectLattice1D")
        return cls(
            lattice_period=float(direct_lattice.lattice_constant),
            lattice_unit=lattice_unit,
        )

    @property
    def direct_lattice(self) -> DirectLattice1D:
        """Return a fresh PhysKit direct lattice with period ``a_0``."""
        return DirectLattice1D(self.lattice_period)

    @property
    def reciprocal_lattice(self) -> ReciprocalLattice1D:
        """Return the PhysKit reciprocal lattice with ``G = 2 pi / a_0``."""
        return ReciprocalLattice1D.from_direct_lattice(self.direct_lattice)

    @property
    def reciprocal_lattice_unit(self) -> PhysicalUnit:
        """Return the physical inverse-length unit dual to ``lattice_unit``."""
        return PhysicalUnit(f"1 / ({self.lattice_unit.expression})")

    def direct_translation(self, displacement: LatticeDisplacement) -> ScalarQuantity:
        """Return ``R_n = n a_0`` with the declared physical length unit."""
        if type(displacement) is not LatticeDisplacement:
            raise TypeError("displacement must be an exact LatticeDisplacement")
        if displacement.dimension is not LatticeDimension.ONE:
            raise ValueError("displacement must have lattice dimension one")
        return ScalarQuantity(
            self.direct_lattice.translation(displacement.components[0]),
            self.lattice_unit,
        )

    def bloch_wavenumber(self, reduced_coordinate: float) -> ScalarQuantity:
        """Return ``k = G q`` with the physical reciprocal-length unit."""
        if type(reduced_coordinate) is not float:
            raise TypeError("reduced_coordinate must be a built-in float")
        if not math.isfinite(reduced_coordinate):
            raise ValueError("reduced_coordinate must be finite")
        return ScalarQuantity(
            self.reciprocal_lattice.b1 * reduced_coordinate,
            self.reciprocal_lattice_unit,
        )

    def reduced_coordinate(self, bloch_wavenumber: ScalarQuantity) -> float:
        """Convert a physical reciprocal-length quantity to reduced ``q = k/G``."""
        if type(bloch_wavenumber) is not ScalarQuantity:
            raise TypeError("bloch_wavenumber must be ScalarQuantity")
        if type(bloch_wavenumber.unit) is not PhysicalUnit:
            raise TypeError("bloch_wavenumber must use PhysicalUnit")
        if not ModelSystemUnitConverter.compatible(
            bloch_wavenumber.unit,
            self.reciprocal_lattice_unit,
        ):
            raise ValueError("bloch_wavenumber must have inverse-length dimensions")
        converted = ModelSystemUnitConverter.convert_scalar(
            bloch_wavenumber,
            self.reciprocal_lattice_unit,
        )
        if not math.isfinite(converted.magnitude):
            raise ValueError("bloch_wavenumber must be finite")
        return converted.magnitude / self.reciprocal_lattice.b1


class Periodic1DReducedCoordinateConvention(  # noqa: B024 - nominal convention marker
    ABC
):
    """Nominally identify the centered reduced-coordinate convention.

    The reduced coordinate ``q`` does not determine a direct-lattice period or its
    caller-declared unit convention. Historical controlled studies select ``a_0 = 1``
    through :attr:`reduced_lattice_geometry`; this is the explicit atomic-length choice
    ``a_0 = 1 bohr``, not a requirement imposed on all periodic-1D studies. Values of
    ``hbar`` and particle mass remain owned by the parent model. New rank-first study
    specifications bind a separate :class:`Periodic1DLatticeGeometry`, which may be
    created from any admitted PhysKit :class:`DirectLattice1D`.
    """

    __slots__ = ()

    @property
    @final
    def reduced_lattice_geometry(self) -> Periodic1DLatticeGeometry:
        """Return the explicit atomic-length choice ``a_0 = 1 bohr``."""
        return Periodic1DLatticeGeometry(
            lattice_period=1.0,
            lattice_unit=PhysicalUnit("bohr"),
        )


__all__ = [
    "Periodic1DLatticeGeometry",
    "Periodic1DReducedCoordinateConvention",
]
