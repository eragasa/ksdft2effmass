"""Unit-aware parameter records for the one-dimensional harmonic oscillator."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.units import (
    ModelSystemUnitConverter,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
)


@dataclass(frozen=True, slots=True)
class Qho1dParameters:
    r"""Define positive unit-aware harmonic-oscillator parameters.

    A parameter set is either fully physical or fully nondimensional. Physical values
    must have action, mass, and inverse-time dimensions. Nondimensional values must all
    use the first-class :class:`~ksdft2effmass.operators.Unitless` unit.

    Parameters
    ----------
    hbar
        Positive reduced Planck constant with action dimensions, or Unitless under an
        explicit nondimensionalization.
    mass
        Positive particle mass, or Unitless under that nondimensionalization.
    omega
        Positive angular frequency, or Unitless under that nondimensionalization.
    """

    hbar: ScalarQuantity
    mass: ScalarQuantity
    omega: ScalarQuantity

    def __post_init__(self) -> None:
        values = (("hbar", self.hbar), ("mass", self.mass), ("omega", self.omega))
        for name, value in values:
            if not isinstance(value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.magnitude <= 0.0:
                raise ValueError(f"{name} must be positive")
        unitless = tuple(isinstance(value.unit, Unitless) for _, value in values)
        if any(unitless) and not all(unitless):
            raise ValueError(
                "harmonic-oscillator parameters must not mix "
                "unitless and physical units"
            )
        if not all(unitless):
            converter = ModelSystemUnitConverter
            expectations = (
                (self.hbar.unit, PhysicalUnit("joule * second"), "hbar"),
                (self.mass.unit, PhysicalUnit("kilogram"), "mass"),
                (self.omega.unit, PhysicalUnit("1 / second"), "omega"),
            )
            for actual, expected, name in expectations:
                if not converter.compatible(actual, expected):
                    raise ValueError(f"{name} has incompatible physical dimensions")

    @property
    def is_nondimensional(self) -> bool:
        """Return whether all parameters use the first-class Unitless unit."""
        return isinstance(self.hbar.unit, Unitless)

    @property
    def oscillator_length(self) -> ScalarQuantity:
        r"""Return :math:`\sqrt{\hbar/(m\omega)}` with an explicit unit."""
        if self.is_nondimensional:
            value = np.sqrt(
                self.hbar.magnitude / (self.mass.magnitude * self.omega.magnitude)
            )
            return ScalarQuantity(float(value), Unitless())
        converter = ModelSystemUnitConverter
        hbar = converter.convert_scalar(
            self.hbar, PhysicalUnit("joule * second")
        ).magnitude
        mass = converter.convert_scalar(self.mass, PhysicalUnit("kilogram")).magnitude
        omega = converter.convert_scalar(
            self.omega, PhysicalUnit("1 / second")
        ).magnitude
        return ScalarQuantity(
            float(np.sqrt(hbar / (mass * omega))), PhysicalUnit("meter")
        )


class Qho1dNondimensionalizer:
    """Adapt explicit normalized scalar inputs to first-class Unitless quantities."""

    __slots__ = ()

    def execute(self, hbar: float, mass: float, omega: float) -> Qho1dParameters:
        """Return a fully Unitless parameter set without implying physical units."""
        return Qho1dParameters(
            hbar=ScalarQuantity(hbar, Unitless()),
            mass=ScalarQuantity(mass, Unitless()),
            omega=ScalarQuantity(omega, Unitless()),
        )
