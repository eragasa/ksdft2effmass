"""Lattice kinetic-energy scale for periodic-1D Bloch-hopping models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from projectkoios.physkit.constants import SI
from projectkoios.physkit.units import (
    ModelSystemUnitConverter,
    PhysicalUnit,
    ScalarQuantity,
)

from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry


@dataclass(frozen=True, slots=True)
class Periodic1DLatticeKineticEnergyScale:
    r"""Represent ``E_a = hbar^2 / (m_e a^2)`` in one physical energy unit.

    The convention deliberately excludes the kinetic-operator factor ``1/2``. In the
    associated reduced unit system, ``hbar = 1``, ``m_e = 1``, ``a = 1``, and therefore
    ``E_a = 1``. For ``a`` equal to one Bohr radius, ``E_a`` is one Hartree up to the
    admitted physical-constant precision.
    """

    SCALE_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic1d-lattice-kinetic-energy-scale.hbar2-over-me-a2.v1"
    )

    lattice_geometry: Periodic1DLatticeGeometry
    energy_unit: PhysicalUnit

    def __post_init__(self) -> None:
        """Validate explicit geometry and physical energy dimensionality."""
        if type(self.lattice_geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("lattice_geometry must be Periodic1DLatticeGeometry")
        if type(self.energy_unit) is not PhysicalUnit:
            raise TypeError("energy_unit must be PhysicalUnit")
        if not ModelSystemUnitConverter.compatible(
            self.energy_unit,
            PhysicalUnit("joule"),
        ):
            raise ValueError("energy_unit must have energy dimensionality")

    @property
    def action_scale(self) -> ScalarQuantity:
        """Return the reduced Planck constant in SI action units."""
        return ScalarQuantity(float(SI.hbar), PhysicalUnit("joule * second"))

    @property
    def mass_scale(self) -> ScalarQuantity:
        """Return the electron rest mass in SI mass units."""
        return ScalarQuantity(float(SI.me0), PhysicalUnit("kilogram"))

    @property
    def length_scale(self) -> ScalarQuantity:
        """Return the declared lattice period with its physical length unit."""
        return ScalarQuantity(
            self.lattice_geometry.lattice_period,
            self.lattice_geometry.lattice_unit,
        )

    @property
    def energy_scale(self) -> ScalarQuantity:
        """Return ``hbar^2 / (m_e a^2)`` in the requested physical energy unit."""
        length_meters = ModelSystemUnitConverter.convert_scalar(
            self.length_scale,
            PhysicalUnit("meter"),
        ).magnitude
        energy_joules = float(SI.hbar**2 / (SI.me0 * length_meters**2))
        return ModelSystemUnitConverter.convert_scalar(
            ScalarQuantity(energy_joules, PhysicalUnit("joule")),
            self.energy_unit,
        )

    @property
    def identity(self) -> str:
        """Return an identity binding formula, geometry, and output energy unit."""
        return (
            f"{self.SCALE_IDENTITY}:"
            f"period-{self.lattice_geometry.lattice_period.hex()}:"
            f"length-unit-{self.lattice_geometry.lattice_unit.expression}:"
            f"energy-unit-{self.energy_unit.expression}"
        )


__all__ = ["Periodic1DLatticeKineticEnergyScale"]
