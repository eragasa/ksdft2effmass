"""Unit contracts for the periodic-1D lattice kinetic-energy scale."""

from typing import cast

import pytest
from projectkoios.physkit.units import PhysicalUnit, UnitSystem

from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.periodic1d.model.blochhopping import (
    Periodic1DLatticeKineticEnergyScale,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestPeriodic1DLatticeKineticEnergyScale:
    r"""Establish the ``hbar^2 / (m_e a^2)`` convention and unit behavior."""

    @pytest.mark.numerical_verification
    def test__Periodic1DLatticeKineticEnergyScale__one_bohr_matches_hartree(
        self,
    ) -> None:
        """Match one Hartree at one bohr in the atomic unit system."""
        scale = Periodic1DLatticeKineticEnergyScale(
            lattice_geometry=Periodic1DLatticeGeometry(
                1.0,
                PhysicalUnit("bohr"),
            ),
            unit_system=UnitSystem.ATOMIC,
        )

        # The convention intentionally omits the kinetic-operator factor one half.
        assert scale.energy_scale.magnitude == pytest.approx(
            1.0,
            rel=0.0,
            abs=3.0e-15,
        )

    def test__Periodic1DLatticeKineticEnergyScale__retains_atomic_metadata(
        self,
    ) -> None:
        """Retain one coherent atomic action, mass, length, and energy inventory."""
        scale = Periodic1DLatticeKineticEnergyScale(
            Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
            UnitSystem.ATOMIC,
        )

        # These fields jointly identify the coherent dimensional scale convention.
        assert (
            scale.energy_scale.unit,
            scale.action_scale.unit,
            scale.mass_scale.unit,
            scale.length_scale.unit,
            "unit-system-atomic" in scale.identity,
        ) == (
            PhysicalUnit("hartree"),
            PhysicalUnit("atomic_unit_of_action"),
            PhysicalUnit("electron_mass"),
            PhysicalUnit("bohr"),
            True,
        )

    @pytest.mark.numerical_verification
    def test__Periodic1DLatticeKineticEnergyScale__follows_inverse_square_period(
        self,
    ) -> None:
        """Scale energy by the inverse square of the lattice period."""
        one = Periodic1DLatticeKineticEnergyScale(
            Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
            UnitSystem.ATOMIC,
        )
        two = Periodic1DLatticeKineticEnergyScale(
            Periodic1DLatticeGeometry(2.0, PhysicalUnit("bohr")),
            UnitSystem.ATOMIC,
        )

        assert two.energy_scale.magnitude == pytest.approx(
            one.energy_scale.magnitude / 4.0,
            rel=0.0,
            abs=3.0e-15,
        )

    @pytest.mark.numerical_verification
    def test__Periodic1DLatticeKineticEnergyScale__converts_to_electron_volt(
        self,
    ) -> None:
        """Express the one-bohr scale through the coherent metal unit system."""
        scale = Periodic1DLatticeKineticEnergyScale(
            Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
            UnitSystem.METAL,
        )

        # The tolerance reflects the maintained Pint constant precision only.
        assert scale.energy_scale.magnitude == pytest.approx(
            27.21138625,
            rel=0.0,
            abs=5.0e-8,
        )

    def test__Periodic1DLatticeKineticEnergyScale__retains_metal_energy_unit(
        self,
    ) -> None:
        """Return the exact energy unit selected by the metal unit system."""
        scale = Periodic1DLatticeKineticEnergyScale(
            Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
            UnitSystem.METAL,
        )

        assert scale.energy_scale.unit == PhysicalUnit("electron_volt")

    def test__Periodic1DLatticeKineticEnergyScale__reports_denominator_underflow(
        self,
    ) -> None:
        """Report mass-length underflow rather than dividing by binary64 zero."""
        scale = Periodic1DLatticeKineticEnergyScale(
            Periodic1DLatticeGeometry(1.0e-150, PhysicalUnit("meter")),
            UnitSystem.SI,
        )

        with pytest.raises(FloatingPointError, match="denominator"):
            _ = scale.energy_scale

    def test__Periodic1DLatticeKineticEnergyScale__rejects_nondimensional_system(
        self,
    ) -> None:
        """Reject a unitless control system at the physical model boundary."""
        geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))

        with pytest.raises(ValueError, match="must be physical"):
            Periodic1DLatticeKineticEnergyScale(
                geometry,
                UnitSystem.NONDIMENSIONAL,
            )

    def test__Periodic1DLatticeKineticEnergyScale__rejects_foreign_unit_system(
        self,
    ) -> None:
        """Reject strings rather than coercing them to unit-system members."""
        geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))

        with pytest.raises(TypeError, match="UnitSystem"):
            Periodic1DLatticeKineticEnergyScale(
                geometry,
                cast(UnitSystem, "atomic"),
            )
