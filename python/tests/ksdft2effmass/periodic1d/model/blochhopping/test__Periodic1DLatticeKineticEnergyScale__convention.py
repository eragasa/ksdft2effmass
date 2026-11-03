"""Unit contracts for the periodic-1D lattice kinetic-energy scale."""

import pytest
from projectkoios.physkit.units import PhysicalUnit, Unitless

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
        """Match one Hartree at one bohr within constant precision."""
        scale = Periodic1DLatticeKineticEnergyScale(
            lattice_geometry=Periodic1DLatticeGeometry(
                1.0,
                PhysicalUnit("bohr"),
            ),
            energy_unit=PhysicalUnit("hartree"),
        )

        # The convention intentionally omits the kinetic-operator factor one half.
        assert scale.energy_scale.magnitude == pytest.approx(
            1.0,
            rel=0.0,
            abs=2.0e-9,
        )

    def test__Periodic1DLatticeKineticEnergyScale__retains_scale_metadata(
        self,
    ) -> None:
        """Retain energy, action, mass, length, and convention identity metadata."""
        scale = Periodic1DLatticeKineticEnergyScale(
            Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
            PhysicalUnit("hartree"),
        )

        # These fields jointly identify the dimensional scale convention.
        assert (
            scale.energy_scale.unit,
            scale.action_scale.unit,
            scale.mass_scale.unit,
            scale.length_scale.unit,
            "hbar2-over-me-a2" in scale.identity,
        ) == (
            PhysicalUnit("hartree"),
            PhysicalUnit("joule * second"),
            PhysicalUnit("kilogram"),
            PhysicalUnit("bohr"),
            True,
        )

    @pytest.mark.numerical_verification
    def test__Periodic1DLatticeKineticEnergyScale__follows_inverse_square_period(
        self,
    ) -> None:
        """Scale energy by the inverse square of the lattice period."""
        unit = PhysicalUnit("hartree")
        one = Periodic1DLatticeKineticEnergyScale(
            Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
            unit,
        )
        two = Periodic1DLatticeKineticEnergyScale(
            Periodic1DLatticeGeometry(2.0, PhysicalUnit("bohr")),
            unit,
        )

        assert two.energy_scale.magnitude == pytest.approx(
            one.energy_scale.magnitude / 4.0,
            rel=1.0e-15,
            abs=0.0,
        )

    @pytest.mark.numerical_verification
    def test__Periodic1DLatticeKineticEnergyScale__converts_to_electron_volt(
        self,
    ) -> None:
        """Express the one-bohr scale explicitly in electron volts."""
        scale = Periodic1DLatticeKineticEnergyScale(
            Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr")),
            PhysicalUnit("electron_volt"),
        )

        assert scale.energy_scale.unit == PhysicalUnit("electron_volt")
        assert scale.energy_scale.magnitude == pytest.approx(
            27.21138625,
            rel=0.0,
            abs=5.0e-8,
        )

    def test__Periodic1DLatticeKineticEnergyScale__rejects_unitless_output(
        self,
    ) -> None:
        """Reject a dimensionless output unit at the physical scale boundary."""
        geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))

        with pytest.raises(TypeError, match="PhysicalUnit"):
            Periodic1DLatticeKineticEnergyScale(
                geometry,
                Unitless(),  # type: ignore[arg-type]
            )

    def test__Periodic1DLatticeKineticEnergyScale__rejects_nonenergy_output(
        self,
    ) -> None:
        """Reject physical output units without energy dimensionality."""
        geometry = Periodic1DLatticeGeometry(1.0, PhysicalUnit("bohr"))

        with pytest.raises(ValueError, match="energy dimensionality"):
            Periodic1DLatticeKineticEnergyScale(
                geometry,
                PhysicalUnit("meter"),
            )
