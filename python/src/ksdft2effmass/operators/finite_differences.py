"""Reusable unit-aware one-dimensional finite-difference operators."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

import numpy as np
from scipy import sparse  # type: ignore[import-untyped]

from .quantities import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ModelSystemUnit,
    PhysicalUnit,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)


@runtime_checkable
class UniformGrid1DRepresentation(Protocol):
    """Declare the uniform one-dimensional grid data required by operators."""

    @property
    def coordinate_unit(self) -> ModelSystemUnit:
        """Return the common coordinate unit."""
        ...

    @property
    def spacing(self) -> ScalarQuantity:
        """Return the positive uniform grid spacing."""
        ...

    @property
    def interior_point_count(self) -> int:
        """Return the number of points excluding the two boundary points."""
        ...


@runtime_checkable
class DirichletBoundaryConditionRepresentation(Protocol):
    """Declare the Dirichlet boundary metadata required by a Laplacian."""

    @property
    def condition_kind(self) -> str:
        """Return the exact boundary-condition kind identifier."""
        ...

    @property
    def is_homogeneous(self) -> bool:
        """Return whether the prescribed Dirichlet value is zero."""
        ...


@runtime_checkable
class DirichletIntervalRepresentation(Protocol):
    """Declare the interval representation required by Dirichlet operators."""

    @property
    def grid(self) -> UniformGrid1DRepresentation:
        """Return the represented uniform grid."""
        ...

    @property
    def boundary_condition(self) -> DirichletBoundaryConditionRepresentation:
        """Return the represented Dirichlet boundary data."""
        ...


@dataclass(frozen=True, slots=True)
class SecondOrderCentralDifferenceLaplacian1D:
    """Represent the centered second-order one-dimensional Laplacian matrix.

    Parameters
    ----------
    interval
        Uniform interval with homogeneous Dirichlet data. Nonhomogeneous conditions
        require an affine forcing contribution and are therefore not represented by
        this matrix alone.
    """

    interval: DirichletIntervalRepresentation

    def __post_init__(self) -> None:
        if not isinstance(self.interval, DirichletIntervalRepresentation):
            raise TypeError("interval must satisfy DirichletIntervalRepresentation")
        if self.interval.boundary_condition.condition_kind != "dirichlet":
            raise ValueError("Laplacian matrix requires Dirichlet boundary data")
        if not self.interval.boundary_condition.is_homogeneous:
            raise ValueError("Laplacian matrix requires homogeneous Dirichlet data")
        if self.interval.grid.interior_point_count <= 0:
            raise ValueError("Laplacian grid must contain at least one interior point")

    def matrix(self) -> SparseMatrixQuantity:
        """Return the sparse second-derivative matrix and inverse-area unit."""
        if isinstance(self.interval.grid.coordinate_unit, Unitless):
            spacing = self.interval.grid.spacing.magnitude
            unit: ModelSystemUnit = Unitless()
        else:
            spacing = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                self.interval.grid.spacing, PhysicalUnit("meter")
            ).magnitude
            unit = PhysicalUnit("1 / meter ** 2")
        points = self.interval.grid.interior_point_count
        inverse_square_spacing = 1.0 / (spacing * spacing)
        diagonal = np.full(points, -2.0 * inverse_square_spacing)
        adjacent = np.full(max(points - 1, 0), inverse_square_spacing)
        matrix = sparse.diags(
            (adjacent, diagonal, adjacent),
            offsets=(-1, 0, 1),
            shape=(points, points),
            format="csr",
            dtype=np.float64,
        )
        return SparseMatrixQuantity.from_csr(matrix, unit)


@dataclass(frozen=True, slots=True)
class SchrodingerKineticEnergy1D:
    r"""Represent ``-hbar**2/(2*m)`` times a finite Laplacian.

    Parameters
    ----------
    laplacian
        Represented centered finite-difference Laplacian.
    hbar
        Positive action quantity, or Unitless under explicit nondimensionalization.
    mass
        Positive mass quantity, or Unitless under the same nondimensionalization.
    """

    laplacian: SecondOrderCentralDifferenceLaplacian1D
    hbar: ScalarQuantity
    mass: ScalarQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.laplacian, SecondOrderCentralDifferenceLaplacian1D):
            raise TypeError("laplacian must be SecondOrderCentralDifferenceLaplacian1D")
        if not isinstance(self.hbar, ScalarQuantity):
            raise TypeError("hbar must be ScalarQuantity")
        if not isinstance(self.mass, ScalarQuantity):
            raise TypeError("mass must be ScalarQuantity")
        if self.hbar.magnitude <= 0.0:
            raise ValueError("hbar must be positive")
        if self.mass.magnitude <= 0.0:
            raise ValueError("mass must be positive")
        nondimensional = isinstance(self.hbar.unit, Unitless)
        if nondimensional != isinstance(self.mass.unit, Unitless):
            raise ValueError("hbar and mass must not mix unitless and physical units")
        if nondimensional != isinstance(
            self.laplacian.interval.grid.coordinate_unit, Unitless
        ):
            raise ValueError("kinetic parameters and grid must use the same unit mode")
        if not nondimensional:
            if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
                self.hbar.unit, PhysicalUnit("joule * second")
            ):
                raise ValueError("hbar has incompatible action dimensions")
            if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
                self.mass.unit, PhysicalUnit("kilogram")
            ):
                raise ValueError("mass has incompatible mass dimensions")

    @property
    def energy_unit(self) -> ModelSystemUnit:
        """Return the represented kinetic-energy unit."""
        if isinstance(self.hbar.unit, Unitless):
            return Unitless()
        return PhysicalUnit("joule")

    def matrix(self) -> SparseMatrixQuantity:
        """Return the represented sparse kinetic-energy matrix."""
        laplacian = self.laplacian.matrix()
        if isinstance(self.hbar.unit, Unitless):
            scale = -(self.hbar.magnitude * self.hbar.magnitude) / (
                2.0 * self.mass.magnitude
            )
        else:
            hbar = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                self.hbar, PhysicalUnit("joule * second")
            ).magnitude
            mass = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                self.mass, PhysicalUnit("kilogram")
            ).magnitude
            scale = -(hbar * hbar) / (2.0 * mass)
        return SparseMatrixQuantity.from_csr(
            scale * laplacian.to_csr(), self.energy_unit
        )


@dataclass(frozen=True, slots=True)
class SampledPotential1D:
    """Represent potential-energy values on ordered interior grid points.

    Parameters
    ----------
    grid
        Exact grid whose interior coordinates index the values.
    values
        Energy-valued vector ordered like the grid's interior coordinates.
    """

    grid: UniformGrid1DRepresentation
    values: VectorQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.grid, UniformGrid1DRepresentation):
            raise TypeError("grid must satisfy UniformGrid1DRepresentation")
        if not isinstance(self.values, VectorQuantity):
            raise TypeError("values must be VectorQuantity")
        if self.values.magnitude.shape != (self.grid.interior_point_count,):
            raise ValueError("values must match the grid interior-point count")
        if isinstance(self.grid.coordinate_unit, Unitless):
            if not isinstance(self.values.unit, Unitless):
                raise ValueError("a Unitless grid requires a Unitless potential")
        elif not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.values.unit, PhysicalUnit("joule")
        ):
            raise ValueError("physical potential values must have energy dimensions")

    def diagonal_operator(self) -> SparseMatrixQuantity:
        """Return the potential as an immutable sparse diagonal matrix."""
        matrix = sparse.diags(
            self.values.magnitude,
            offsets=0,
            shape=(self.values.magnitude.size, self.values.magnitude.size),
            format="csr",
            dtype=np.float64,
        )
        return SparseMatrixQuantity.from_csr(matrix, self.values.unit)


@dataclass(frozen=True, slots=True)
class FiniteDifferenceHamiltonian1D:
    """Compose compatible finite-difference kinetic and sampled potential energies.

    Parameters
    ----------
    kinetic_energy
        Represented kinetic-energy model and its exact grid correlation.
    potential
        Sampled diagonal potential on the same exact grid.
    """

    kinetic_energy: SchrodingerKineticEnergy1D
    potential: SampledPotential1D

    def __post_init__(self) -> None:
        if not isinstance(self.kinetic_energy, SchrodingerKineticEnergy1D):
            raise TypeError("kinetic_energy must be SchrodingerKineticEnergy1D")
        if not isinstance(self.potential, SampledPotential1D):
            raise TypeError("potential must be SampledPotential1D")
        if self.kinetic_energy.laplacian.interval.grid != self.potential.grid:
            raise ValueError("kinetic energy and potential must share the exact grid")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.potential.values.unit, self.kinetic_energy.energy_unit
        ):
            raise ValueError("kinetic and potential energy units are incompatible")

    def matrix(self) -> SparseMatrixQuantity:
        """Return the compatible sparse kinetic-plus-potential Hamiltonian."""
        kinetic = self.kinetic_energy.matrix()
        potential = MODEL_SYSTEM_UNIT_CONVERTER.convert_sparse_matrix(
            self.potential.diagonal_operator(), kinetic.unit
        )
        return SparseMatrixQuantity.from_csr(
            kinetic.to_csr() + potential.to_csr(), kinetic.unit
        )
