"""Periodic grids and twisted finite-difference fibers in one dimension."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.units import (
    ComplexSparseMatrixQuantity,
    ModelSystemUnitConverter,
    ScalarQuantity,
    VectorQuantity,
)
from scipy import sparse  # type: ignore[import-untyped]

from .model import PeriodicFourierPotential1D


@dataclass(frozen=True, slots=True)
class PeriodicUniformGrid1D:
    """Represent ordered points on one half-open periodic cell."""

    origin: ScalarQuantity
    period: ScalarQuantity
    point_count: int

    def __post_init__(self) -> None:
        """Validate compatible coordinates, positive period, and useful size."""
        if type(self.origin) is not ScalarQuantity:
            raise TypeError("origin must be ScalarQuantity")
        if type(self.period) is not ScalarQuantity:
            raise TypeError("period must be ScalarQuantity")
        if not ModelSystemUnitConverter.compatible(self.origin.unit, self.period.unit):
            raise ValueError("origin and period units must be compatible")
        object.__setattr__(
            self,
            "origin",
            ModelSystemUnitConverter.convert_scalar(self.origin, self.period.unit),
        )
        if self.period.magnitude <= 0.0:
            raise ValueError("period must be positive")
        if type(self.point_count) is not int:
            raise TypeError("point_count must be a built-in int")
        if self.point_count < 3:
            raise ValueError("point_count must be at least three")

    @property
    def spacing(self) -> ScalarQuantity:
        """Return the periodic-grid spacing."""
        return ScalarQuantity(
            self.period.magnitude / float(self.point_count), self.period.unit
        )

    @property
    def coordinates(self) -> VectorQuantity:
        """Return ordered half-open cell coordinates."""
        values = self.origin.magnitude + self.spacing.magnitude * np.arange(
            self.point_count, dtype=np.float64
        )
        return VectorQuantity(values, self.period.unit)


@dataclass(frozen=True, slots=True, eq=False)
class PeriodicFiniteDifferenceFiberHamiltonian1DResult:
    """Retain one twisted second-order periodic finite-difference fiber."""

    reduced_momentum: float
    grid: PeriodicUniformGrid1D
    potential: PeriodicFourierPotential1D
    recoil_energy: ScalarQuantity
    period_absolute_tolerance: float
    represented_matrix: ComplexSparseMatrixQuantity

    def __post_init__(self) -> None:
        """Validate the represented fiber correlations."""
        if type(self.reduced_momentum) is not float:
            raise TypeError("reduced_momentum must be a built-in float")
        if not np.isfinite(self.reduced_momentum):
            raise ValueError("reduced_momentum must be finite")
        if self.reduced_momentum < -0.5 or self.reduced_momentum > 0.5:
            raise ValueError("reduced_momentum must lie in [-0.5, 0.5]")
        if type(self.grid) is not PeriodicUniformGrid1D:
            raise TypeError("grid must be PeriodicUniformGrid1D")
        if type(self.potential) is not PeriodicFourierPotential1D:
            raise TypeError("potential must be PeriodicFourierPotential1D")
        if type(self.recoil_energy) is not ScalarQuantity:
            raise TypeError("recoil_energy must be ScalarQuantity")
        if self.recoil_energy.magnitude <= 0.0:
            raise ValueError("recoil_energy must be positive")
        if type(self.period_absolute_tolerance) is not float:
            raise TypeError("period_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.period_absolute_tolerance)
            or self.period_absolute_tolerance < 0.0
        ):
            raise ValueError("period_absolute_tolerance must be finite and nonnegative")
        if type(self.represented_matrix) is not ComplexSparseMatrixQuantity:
            raise TypeError("represented_matrix must be ComplexSparseMatrixQuantity")
        expected_shape = (self.grid.point_count, self.grid.point_count)
        if self.represented_matrix.shape != expected_shape:
            raise ValueError("represented_matrix shape must match the grid")
        if self.represented_matrix.unit != self.recoil_energy.unit:
            raise ValueError("represented_matrix must use the recoil-energy unit")


@dataclass(frozen=True, slots=True)
class PeriodicFiniteDifferenceFiberHamiltonian1DRequest:
    """Bind one complete twisted finite-difference fiber request."""

    reduced_momentum: float
    grid: PeriodicUniformGrid1D
    potential: PeriodicFourierPotential1D
    recoil_energy: ScalarQuantity
    period_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Admit one correlated represented-fiber request."""
        if type(self.reduced_momentum) is not float:
            raise TypeError("reduced_momentum must be a built-in float")
        if not np.isfinite(self.reduced_momentum):
            raise ValueError("reduced_momentum must be finite")
        if self.reduced_momentum < -0.5 or self.reduced_momentum > 0.5:
            raise ValueError("reduced_momentum must lie in [-0.5, 0.5]")
        if type(self.grid) is not PeriodicUniformGrid1D:
            raise TypeError("grid must be PeriodicUniformGrid1D")
        if type(self.potential) is not PeriodicFourierPotential1D:
            raise TypeError("potential must be PeriodicFourierPotential1D")
        if type(self.recoil_energy) is not ScalarQuantity:
            raise TypeError("recoil_energy must be ScalarQuantity")
        if self.recoil_energy.magnitude <= 0.0:
            raise ValueError("recoil_energy must be positive")
        if type(self.period_absolute_tolerance) is not float:
            raise TypeError("period_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.period_absolute_tolerance)
            or self.period_absolute_tolerance < 0.0
        ):
            raise ValueError("period_absolute_tolerance must be finite and nonnegative")
        potential_period = ModelSystemUnitConverter.convert_scalar(
            self.potential.period, self.grid.period.unit
        )
        if not np.isclose(
            potential_period.magnitude,
            self.grid.period.magnitude,
            rtol=0.0,
            atol=self.period_absolute_tolerance,
        ):
            raise ValueError("grid and potential periods do not agree")
        if not ModelSystemUnitConverter.compatible(
            self.potential.constant_coefficient.unit, self.recoil_energy.unit
        ):
            raise ValueError("potential and recoil-energy units must be compatible")


class PeriodicFiniteDifferenceFiberHamiltonian1DConstructor:
    """Construct one bound twisted finite-difference fiber request."""

    __slots__ = ("_request",)

    def __init__(
        self, request: PeriodicFiniteDifferenceFiberHamiltonian1DRequest
    ) -> None:
        if type(request) is not PeriodicFiniteDifferenceFiberHamiltonian1DRequest:
            raise TypeError(
                "request must be PeriodicFiniteDifferenceFiberHamiltonian1DRequest"
            )
        self._request = request

    @property
    def request(self) -> PeriodicFiniteDifferenceFiberHamiltonian1DRequest:
        """Return the complete immutable construction request."""
        return self._request

    def execute(self) -> PeriodicFiniteDifferenceFiberHamiltonian1DResult:
        """Construct the periodic central-difference Hamiltonian with Bloch seam."""
        request = self.request
        converter = ModelSystemUnitConverter
        sampled_potential = converter.convert_vector(
            request.potential.evaluate(request.grid.coordinates),
            request.recoil_energy.unit,
        )
        reciprocal_spacing = 2.0 * np.pi / float(request.grid.point_count)
        kinetic_link = request.recoil_energy.magnitude / (reciprocal_spacing**2)
        diagonal = 2.0 * kinetic_link + sampled_potential.magnitude
        dimension = request.grid.point_count
        matrix = sparse.diags(
            (
                np.full(dimension - 1, -kinetic_link, dtype=np.complex128),
                diagonal.astype(np.complex128),
                np.full(dimension - 1, -kinetic_link, dtype=np.complex128),
            ),
            offsets=(-1, 0, 1),
            shape=(dimension, dimension),
            format="lil",
            dtype=np.complex128,
        )
        seam = -kinetic_link * np.exp(-2j * np.pi * request.reduced_momentum)
        matrix[0, dimension - 1] = seam
        matrix[dimension - 1, 0] = np.conjugate(seam)
        represented = ComplexSparseMatrixQuantity.from_csr(
            matrix.tocsr(), request.recoil_energy.unit
        )
        return PeriodicFiniteDifferenceFiberHamiltonian1DResult(
            request.reduced_momentum,
            request.grid,
            request.potential,
            request.recoil_energy,
            request.period_absolute_tolerance,
            represented,
        )
