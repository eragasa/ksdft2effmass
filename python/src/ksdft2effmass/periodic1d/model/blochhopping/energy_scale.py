"""Lattice kinetic-energy scale for periodic-1D Bloch-hopping models."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import ClassVar

from projectkoios.physkit.units import (
    ModelSystemUnitConverter,
    PhysicalUnit,
    ScalarQuantity,
    UnitSystem,
)

from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry


@dataclass(frozen=True, slots=True)
class Periodic1DLatticeKineticEnergyScale:
    r"""Represent ``E_a = hbar^2 / (m_e a^2)`` in a coherent unit system.

    Parameters
    ----------
    lattice_geometry : Periodic1DLatticeGeometry
        Physical primitive period ``a`` and its explicit source length unit.
    unit_system : UnitSystem
        Physical coherent unit system supplying length, mass, action, and energy units.

    Raises
    ------
    TypeError
        If either argument lacks its exact nominal owner.
    ValueError
        If ``unit_system`` is nondimensional.

    Notes
    -----
    The convention deliberately excludes the kinetic-operator factor ``1/2``. KSD owns
    that model-parameterization choice. PhysKit owns the coherent unit-system
    quantities, Pint unit definitions, and conversion mechanics used by the calculation.
    """

    SCALE_IDENTITY: ClassVar[str] = (
        "ksdft2effmass.periodic1d-lattice-kinetic-energy-scale.hbar2-over-me-a2.v1"
    )

    lattice_geometry: Periodic1DLatticeGeometry
    unit_system: UnitSystem

    def __post_init__(self) -> None:
        """Validate explicit geometry and a physical coherent unit system."""
        if type(self.lattice_geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("lattice_geometry must be Periodic1DLatticeGeometry")
        if type(self.unit_system) is not UnitSystem:
            raise TypeError("unit_system must be UnitSystem")
        if self.unit_system is UnitSystem.NONDIMENSIONAL:
            raise ValueError("unit_system must be physical")

    @property
    def action_scale(self) -> ScalarQuantity:
        """Return the coherent reduced Planck constant.

        Returns
        -------
        ScalarQuantity
            Reduced Planck constant in ``unit_system.action_unit``.
        """
        return self.unit_system.hbar

    @property
    def mass_scale(self) -> ScalarQuantity:
        """Return the coherent bare-electron mass.

        Returns
        -------
        ScalarQuantity
            One Pint-supported electron mass converted to ``unit_system.mass_unit``.
        """
        mass_unit = self.unit_system.mass_unit
        if not isinstance(mass_unit, PhysicalUnit):
            raise TypeError("physical unit systems require a physical mass unit")
        return ModelSystemUnitConverter.convert_scalar(
            ScalarQuantity(1.0, PhysicalUnit("electron_mass")),
            mass_unit,
        )

    @property
    def length_scale(self) -> ScalarQuantity:
        """Return the primitive period in the coherent length unit.

        Returns
        -------
        ScalarQuantity
            Positive lattice period converted to ``unit_system.length_unit``.
        """
        length_unit = self.unit_system.length_unit
        if not isinstance(length_unit, PhysicalUnit):
            raise TypeError("physical unit systems require a physical length unit")
        return ModelSystemUnitConverter.convert_scalar(
            ScalarQuantity(
                self.lattice_geometry.lattice_period,
                self.lattice_geometry.lattice_unit,
            ),
            length_unit,
        )

    @property
    def energy_scale(self) -> ScalarQuantity:
        r"""Return ``hbar^2 / (m_e a^2)``.

        Returns
        -------
        ScalarQuantity
            Finite positive energy in ``unit_system.energy_unit``.

        Raises
        ------
        FloatingPointError
            If binary64 arithmetic underflows or overflows to a nonfinite result.
        """
        hbar = self.action_scale
        mass = self.mass_scale
        length = self.length_scale
        if not isinstance(hbar.unit, PhysicalUnit):
            raise TypeError("physical unit systems require a physical action unit")
        if not isinstance(mass.unit, PhysicalUnit):
            raise TypeError("physical unit systems require a physical mass unit")
        if not isinstance(length.unit, PhysicalUnit):
            raise TypeError("physical unit systems require a physical length unit")
        energy_unit = self.unit_system.energy_unit
        if not isinstance(energy_unit, PhysicalUnit):
            raise TypeError("physical unit systems require a physical energy unit")

        squared_length = length.magnitude * length.magnitude
        if squared_length == 0.0 or not math.isfinite(squared_length):
            raise FloatingPointError("lattice-period square must remain finite")
        denominator = mass.magnitude * squared_length
        if denominator == 0.0 or not math.isfinite(denominator):
            raise FloatingPointError("mass-length denominator must remain finite")
        magnitude = hbar.magnitude * hbar.magnitude / denominator
        if not math.isfinite(magnitude) or magnitude <= 0.0:
            raise FloatingPointError("lattice kinetic-energy scale must remain finite")

        # The compound unit is constructed from one coherent UnitSystem inventory;
        # conversion to its energy unit is explicit rather than numerically assumed.
        represented_unit = PhysicalUnit(
            f"({hbar.unit.expression}) ** 2 / "
            f"(({mass.unit.expression}) * ({length.unit.expression}) ** 2)"
        )
        return ModelSystemUnitConverter.convert_scalar(
            ScalarQuantity(magnitude, represented_unit),
            energy_unit,
        )

    @property
    def identity(self) -> str:
        """Return the complete scale identity.

        Returns
        -------
        str
            Stable identity binding formula, geometry, and coherent unit system.
        """
        return (
            f"{self.SCALE_IDENTITY}:"
            f"period-{self.lattice_geometry.lattice_period.hex()}:"
            f"length-unit-{self.lattice_geometry.lattice_unit.expression}:"
            f"unit-system-{self.unit_system.value}"
        )


__all__ = ["Periodic1DLatticeKineticEnergyScale"]
