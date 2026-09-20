"""Immutable one-dimensional particle-in-a-box model contracts."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    FiniteDifferenceHamiltonian1D,
    SampledPotential1D,
    SchrodingerKineticEnergy1D,
    SecondOrderCentralDifferenceLaplacian1D,
)
from ksdft2effmass.operators.quantities import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    PhysicalUnit,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)

from ..intervals import DirichletInterval


@dataclass(frozen=True, slots=True)
class ParticleInBoxParameters:
    """Define positive unit-aware one-dimensional box parameters.

    Parameters
    ----------
    length
        Positive box length, or Unitless under explicit nondimensionalization.
    mass
        Positive particle mass, or Unitless under the same nondimensionalization.
    hbar
        Positive action quantity, or Unitless under the same nondimensionalization.
    """

    length: ScalarQuantity
    mass: ScalarQuantity
    hbar: ScalarQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.length, ScalarQuantity):
            raise TypeError("length must be ScalarQuantity")
        if not isinstance(self.mass, ScalarQuantity):
            raise TypeError("mass must be ScalarQuantity")
        if not isinstance(self.hbar, ScalarQuantity):
            raise TypeError("hbar must be ScalarQuantity")
        if self.length.magnitude <= 0.0:
            raise ValueError("length must be positive")
        if self.mass.magnitude <= 0.0:
            raise ValueError("mass must be positive")
        if self.hbar.magnitude <= 0.0:
            raise ValueError("hbar must be positive")
        modes = (
            isinstance(self.length.unit, Unitless),
            isinstance(self.mass.unit, Unitless),
            isinstance(self.hbar.unit, Unitless),
        )
        if any(modes) and not all(modes):
            raise ValueError("particle-in-box parameters must use one unit mode")
        if not self.is_nondimensional:
            if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
                self.length.unit, PhysicalUnit("meter")
            ):
                raise ValueError("length has incompatible dimensions")
            if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
                self.mass.unit, PhysicalUnit("kilogram")
            ):
                raise ValueError("mass has incompatible dimensions")
            if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
                self.hbar.unit, PhysicalUnit("joule * second")
            ):
                raise ValueError("hbar has incompatible dimensions")

    @property
    def is_nondimensional(self) -> bool:
        """Return whether all parameters use the first-class Unitless unit."""
        return isinstance(self.length.unit, Unitless)

    @property
    def canonical_length(self) -> ScalarQuantity:
        """Return length in Unitless or canonical meter units."""
        if self.is_nondimensional:
            return self.length
        return MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.length, PhysicalUnit("meter")
        )


@dataclass(frozen=True, slots=True)
class ParticleInBoxAnalytical:
    """Represent the continuum one-dimensional Dirichlet box spectrum."""

    parameters: ParticleInBoxParameters

    def __post_init__(self) -> None:
        if not isinstance(self.parameters, ParticleInBoxParameters):
            raise TypeError("parameters must be ParticleInBoxParameters")

    def energy_levels(self, count: int) -> VectorQuantity:
        """Return the first ``count`` continuum energies in ascending mode order."""
        if type(count) is not int:
            raise TypeError("count must be a built-in int")
        if count <= 0:
            raise ValueError("count must be positive")
        parameters = self.parameters
        indices = np.arange(1, count + 1, dtype=np.float64)
        if parameters.is_nondimensional:
            length = parameters.length.magnitude
            mass = parameters.mass.magnitude
            hbar = parameters.hbar.magnitude
            unit: PhysicalUnit | Unitless = Unitless()
        else:
            length = parameters.canonical_length.magnitude
            mass = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                parameters.mass, PhysicalUnit("kilogram")
            ).magnitude
            hbar = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                parameters.hbar, PhysicalUnit("joule * second")
            ).magnitude
            unit = PhysicalUnit("joule")
        energies = (
            hbar
            * hbar
            * np.pi
            * np.pi
            * indices
            * indices
            / (2.0 * mass * length * length)
        )
        return VectorQuantity(energies, unit)


@dataclass(frozen=True, slots=True)
class ParticleInBoxFiniteDifference:
    """Represent a particle in a reusable homogeneous Dirichlet interval.

    Parameters
    ----------
    analytical
        Continuum model supplying the physical parameters.
    interval
        Interval spanning exactly ``[0, length]`` with homogeneous Dirichlet data.
    """

    analytical: ParticleInBoxAnalytical
    interval: DirichletInterval

    def __post_init__(self) -> None:
        if not isinstance(self.analytical, ParticleInBoxAnalytical):
            raise TypeError("analytical must be ParticleInBoxAnalytical")
        if not isinstance(self.interval, DirichletInterval):
            raise TypeError("interval must be DirichletInterval")
        if not self.interval.boundary_condition.is_homogeneous:
            raise ValueError("particle-in-box matrix requires homogeneous boundaries")
        expected_length: PhysicalUnit | Unitless
        expected_field: PhysicalUnit | Unitless
        if self.analytical.parameters.is_nondimensional:
            expected_length = Unitless()
            expected_field = Unitless()
        else:
            expected_length = PhysicalUnit("meter")
            expected_field = PhysicalUnit("meter ** -0.5")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.interval.grid.coordinate_unit, expected_length
        ):
            raise ValueError("interval has incompatible coordinate dimensions")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.interval.boundary_condition.value.unit, expected_field
        ):
            raise ValueError("boundary value has incompatible wavefunction dimensions")
        lower = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.interval.grid.lower_bound, expected_length
        ).magnitude
        upper = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.interval.grid.upper_bound, expected_length
        ).magnitude
        length = self.analytical.parameters.canonical_length.magnitude
        if lower != 0.0 or not np.isclose(upper, length, rtol=0.0, atol=1.0e-12):
            raise ValueError("interval must span exactly from zero to box length")

    @property
    def interior_points(self) -> int:
        """Return the finite coordinate-space dimension."""
        return self.interval.interior_points

    @property
    def grid_spacing(self) -> ScalarQuantity:
        """Return realized spacing in canonical length units."""
        target = (
            Unitless()
            if self.analytical.parameters.is_nondimensional
            else PhysicalUnit("meter")
        )
        return MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.interval.grid.spacing, target
        )

    def hamiltonian(self) -> SparseMatrixQuantity:
        """Return the sparse zero-potential finite-difference Hamiltonian."""
        parameters = self.analytical.parameters
        laplacian = SecondOrderCentralDifferenceLaplacian1D(self.interval)
        kinetic = SchrodingerKineticEnergy1D(
            laplacian=laplacian,
            hbar=parameters.hbar,
            mass=parameters.mass,
        )
        potential_unit: PhysicalUnit | Unitless
        if parameters.is_nondimensional:
            potential_unit = Unitless()
        else:
            potential_unit = PhysicalUnit("joule")
        potential = SampledPotential1D(
            grid=self.interval.grid,
            values=VectorQuantity(
                np.zeros(self.interior_points, dtype=np.float64), potential_unit
            ),
        )
        return FiniteDifferenceHamiltonian1D(kinetic, potential).matrix()

    def discrete_energy_levels(self) -> VectorQuantity:
        """Return all centered-difference Dirichlet eigenvalues in mode order."""
        parameters = self.analytical.parameters
        points = self.interior_points
        indices = np.arange(1, points + 1, dtype=np.float64)
        spacing = self.grid_spacing.magnitude
        if parameters.is_nondimensional:
            mass = parameters.mass.magnitude
            hbar = parameters.hbar.magnitude
            unit: PhysicalUnit | Unitless = Unitless()
        else:
            mass = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                parameters.mass, PhysicalUnit("kilogram")
            ).magnitude
            hbar = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                parameters.hbar, PhysicalUnit("joule * second")
            ).magnitude
            unit = PhysicalUnit("joule")
        energies = (
            2.0
            * hbar
            * hbar
            / (mass * spacing * spacing)
            * np.sin(indices * np.pi / (2.0 * (points + 1))) ** 2
        )
        return VectorQuantity(energies, unit)
