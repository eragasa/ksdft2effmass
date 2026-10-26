"""Exact real-line solution for the one-dimensional harmonic oscillator."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.units import (
    MatrixQuantity,
    ModelSystemUnitConverter,
    PhysicalUnit,
    Unitless,
    VectorQuantity,
)

from .parameters import Qho1dParameters


@dataclass(frozen=True, slots=True)
class Qho1dAnalytical:
    """Represent the exact real-line harmonic-oscillator solution.

    Parameters
    ----------
    parameters
        Positive physical oscillator parameters shared by every representation.

    Attributes
    ----------
    parameters
        Exact physical parameter record.
    """

    parameters: Qho1dParameters

    def __post_init__(self) -> None:
        if not isinstance(self.parameters, Qho1dParameters):
            raise TypeError("parameters must be Qho1dParameters")

    def number_state_energies(self, retained_dimension: int) -> VectorQuantity:
        """Return exact unit-aware energies for states ``|0>`` through ``|K-1>``."""
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must be a built-in int")
        if retained_dimension <= 0:
            raise ValueError("retained_dimension must be positive")
        parameters = self.parameters
        if parameters.is_nondimensional:
            scale = parameters.hbar.magnitude * parameters.omega.magnitude
            unit: PhysicalUnit | Unitless = Unitless()
        else:
            converter = ModelSystemUnitConverter
            hbar = converter.convert_scalar(
                parameters.hbar, PhysicalUnit("joule * second")
            ).magnitude
            omega = converter.convert_scalar(
                parameters.omega, PhysicalUnit("1 / second")
            ).magnitude
            scale = hbar * omega
            unit = PhysicalUnit("joule")
        values = scale * (np.arange(retained_dimension, dtype=np.float64) + 0.5)
        return VectorQuantity(values, unit)

    def number_state_wavefunctions(
        self,
        dimensionless_coordinates: VectorQuantity,
        retained_dimension: int,
    ) -> MatrixQuantity:
        """Evaluate normalized Hermite states at Unitless coordinates ``x / ell``."""
        if not isinstance(dimensionless_coordinates, VectorQuantity):
            raise TypeError("dimensionless_coordinates must be VectorQuantity")
        if not isinstance(dimensionless_coordinates.unit, Unitless):
            raise ValueError("dimensionless_coordinates must use Unitless")
        coordinates = dimensionless_coordinates.magnitude
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must be a built-in int")
        if retained_dimension <= 0:
            raise ValueError("retained_dimension must be positive")
        states = np.empty((coordinates.size, retained_dimension), dtype=np.float64)
        oscillator_length = self.parameters.oscillator_length
        states[:, 0] = (
            np.pi ** (-0.25)
            * np.exp(-0.5 * np.square(coordinates))
            / np.sqrt(oscillator_length.magnitude)
        )
        if retained_dimension > 1:
            states[:, 1] = np.sqrt(2.0) * coordinates * states[:, 0]
        for degree in range(1, retained_dimension - 1):
            states[:, degree + 1] = (
                np.sqrt(2.0 / (degree + 1.0)) * coordinates * states[:, degree]
                - np.sqrt(degree / (degree + 1.0)) * states[:, degree - 1]
            )
        unit: PhysicalUnit | Unitless
        if self.parameters.is_nondimensional:
            unit = Unitless()
        else:
            unit = PhysicalUnit("meter ** -0.5")
        return MatrixQuantity(states, unit)
