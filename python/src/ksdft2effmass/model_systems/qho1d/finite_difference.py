"""Finite Dirichlet-grid representation of the harmonic oscillator."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.units import (
    ModelSystemUnitConverter,
    PhysicalUnit,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.operators import (
    FiniteDifferenceHamiltonian1D,
    SampledPotential1D,
    SchrodingerKineticEnergy1D,
    SecondOrderCentralDifferenceLaplacian1D,
)

from ..intervals import DirichletInterval
from .analytical import Qho1dAnalytical


@dataclass(frozen=True, slots=True)
class Qho1dFiniteDifference:
    """Represent a harmonic oscillator on a reusable Dirichlet interval.

    Parameters
    ----------
    analytical
        Exact oscillator model supplying physical parameters and wavefunction units.
    interval
        Symmetric interval with homogeneous Dirichlet boundary data.
    """

    analytical: Qho1dAnalytical
    interval: DirichletInterval

    def __post_init__(self) -> None:
        if not isinstance(self.analytical, Qho1dAnalytical):
            raise TypeError("analytical must be Qho1dAnalytical")
        if not isinstance(self.interval, DirichletInterval):
            raise TypeError("interval must be DirichletInterval")
        if not self.interval.boundary_condition.is_homogeneous:
            raise ValueError(
                "finite-matrix realization requires homogeneous Dirichlet data"
            )
        expected_length = self.canonical_length_unit
        if not ModelSystemUnitConverter.compatible(
            self.interval.grid.coordinate_unit, expected_length
        ):
            raise ValueError("grid has incompatible coordinate dimensions")
        expected_field: PhysicalUnit | Unitless
        if self.analytical.parameters.is_nondimensional:
            expected_field = Unitless()
        else:
            expected_field = PhysicalUnit("meter ** -0.5")
        if not ModelSystemUnitConverter.compatible(
            self.interval.boundary_condition.value.unit, expected_field
        ):
            raise ValueError("boundary value has incompatible wavefunction dimensions")
        lower = ModelSystemUnitConverter.convert_scalar(
            self.interval.grid.lower_bound, expected_length
        ).magnitude
        upper = ModelSystemUnitConverter.convert_scalar(
            self.interval.grid.upper_bound, expected_length
        ).magnitude
        if not np.isclose(lower, -upper, rtol=0.0, atol=1.0e-12):
            raise ValueError(
                "harmonic-oscillator interval must be symmetric about zero"
            )

    @property
    def canonical_length_unit(self) -> PhysicalUnit | Unitless:
        """Return Unitless for normalized models and meters for physical models."""
        if self.analytical.parameters.is_nondimensional:
            return Unitless()
        return PhysicalUnit("meter")

    @property
    def box_half_width(self) -> ScalarQuantity:
        """Return the symmetric interval half-width in the canonical length unit."""
        upper = ModelSystemUnitConverter.convert_scalar(
            self.interval.grid.upper_bound, self.canonical_length_unit
        )
        return ScalarQuantity(upper.magnitude, self.canonical_length_unit)

    @property
    def requested_grid_spacing(self) -> ScalarQuantity:
        """Return the requested grid spacing in the canonical length unit."""
        return ModelSystemUnitConverter.convert_scalar(
            self.interval.grid.requested_spacing, self.canonical_length_unit
        )

    @property
    def interior_points(self) -> int:
        """Return the number of ordered interior grid coordinates."""
        return self.interval.interior_points

    @property
    def grid_spacing(self) -> ScalarQuantity:
        """Return the realized uniform spacing in the canonical length unit."""
        return ModelSystemUnitConverter.convert_scalar(
            self.interval.grid.spacing, self.canonical_length_unit
        )

    def grid_coordinates(self) -> VectorQuantity:
        """Return interior grid coordinates in the canonical length unit."""
        return ModelSystemUnitConverter.convert_vector(
            self.interval.grid.interior_coordinates(), self.canonical_length_unit
        )

    def hamiltonian(self) -> SparseMatrixQuantity:
        """Return the sparse kinetic-plus-harmonic-potential Hamiltonian."""
        parameters = self.analytical.parameters
        laplacian = SecondOrderCentralDifferenceLaplacian1D(self.interval)
        kinetic = SchrodingerKineticEnergy1D(
            laplacian=laplacian,
            hbar=parameters.hbar,
            mass=parameters.mass,
        )
        coordinates = self.grid_coordinates().magnitude
        if parameters.is_nondimensional:
            mass = parameters.mass.magnitude
            omega = parameters.omega.magnitude
            energy_unit: PhysicalUnit | Unitless = Unitless()
        else:
            mass = ModelSystemUnitConverter.convert_scalar(
                parameters.mass, PhysicalUnit("kilogram")
            ).magnitude
            omega = ModelSystemUnitConverter.convert_scalar(
                parameters.omega, PhysicalUnit("1 / second")
            ).magnitude
            energy_unit = PhysicalUnit("joule")
        potential = SampledPotential1D(
            grid=self.interval.grid,
            values=VectorQuantity(
                0.5 * mass * omega**2 * np.square(coordinates), energy_unit
            ),
        )
        return FiniteDifferenceHamiltonian1D(kinetic, potential).matrix()
