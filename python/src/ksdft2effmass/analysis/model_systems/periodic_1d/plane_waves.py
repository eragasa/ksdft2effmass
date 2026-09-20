"""Plane-wave fibers for one-dimensional periodic Fourier models."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    ScalarQuantity,
)
from ksdft2effmass.solid_state import PlaneWaveBasis1D

from .model import PeriodicFourierPotential1D


@dataclass(frozen=True, slots=True, eq=False)
class PlaneWaveFiberHamiltonian1DResult:
    """Retain one represented periodic fiber and all construction inputs."""

    reduced_momentum: float
    basis: PlaneWaveBasis1D
    potential: PeriodicFourierPotential1D
    recoil_energy: ScalarQuantity
    duality_absolute_tolerance: float
    represented_matrix: ComplexMatrixQuantity

    def __post_init__(self) -> None:
        """Validate the correlated represented-fiber result."""
        if type(self.reduced_momentum) is not float:
            raise TypeError("reduced_momentum must be a built-in float")
        if not np.isfinite(self.reduced_momentum):
            raise ValueError("reduced_momentum must be finite")
        if self.reduced_momentum < -0.5 or self.reduced_momentum > 0.5:
            raise ValueError("reduced_momentum must lie in [-0.5, 0.5]")
        if type(self.basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
        if type(self.potential) is not PeriodicFourierPotential1D:
            raise TypeError("potential must be PeriodicFourierPotential1D")
        if type(self.recoil_energy) is not ScalarQuantity:
            raise TypeError("recoil_energy must be ScalarQuantity")
        if self.recoil_energy.magnitude <= 0.0:
            raise ValueError("recoil_energy must be positive")
        if type(self.duality_absolute_tolerance) is not float:
            raise TypeError("duality_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.duality_absolute_tolerance)
            or self.duality_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "duality_absolute_tolerance must be finite and nonnegative"
            )
        if type(self.represented_matrix) is not ComplexMatrixQuantity:
            raise TypeError("represented_matrix must be ComplexMatrixQuantity")
        if self.represented_matrix.magnitude.shape != (
            self.basis.dimension,
            self.basis.dimension,
        ):
            raise ValueError("represented_matrix shape must match the basis")
        if self.represented_matrix.unit != self.recoil_energy.unit:
            raise ValueError("represented_matrix must use the recoil-energy unit")


class PlaneWaveFiberHamiltonian1DConstructor:
    """Construct finite plane-wave fibers for real periodic Fourier potentials."""

    __slots__ = ()

    def execute(
        self,
        reduced_momentum: float,
        basis: PlaneWaveBasis1D,
        potential: PeriodicFourierPotential1D,
        recoil_energy: ScalarQuantity,
        duality_absolute_tolerance: float,
    ) -> PlaneWaveFiberHamiltonian1DResult:
        """Construct ``H_nm(k)`` in ordered reciprocal-index convention."""
        if type(reduced_momentum) is not float:
            raise TypeError("reduced_momentum must be a built-in float")
        if not np.isfinite(reduced_momentum):
            raise ValueError("reduced_momentum must be finite")
        if reduced_momentum < -0.5 or reduced_momentum > 0.5:
            raise ValueError("reduced_momentum must lie in [-0.5, 0.5]")
        if type(basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
        if type(potential) is not PeriodicFourierPotential1D:
            raise TypeError("potential must be PeriodicFourierPotential1D")
        if type(recoil_energy) is not ScalarQuantity:
            raise TypeError("recoil_energy must be ScalarQuantity")
        if recoil_energy.magnitude <= 0.0:
            raise ValueError("recoil_energy must be positive")
        if type(duality_absolute_tolerance) is not float:
            raise TypeError("duality_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(duality_absolute_tolerance)
            or duality_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "duality_absolute_tolerance must be finite and nonnegative"
            )
        expected_reciprocal = potential.reciprocal_period_in(basis.reciprocal_vector)
        if not np.isclose(
            basis.reciprocal_vector.magnitude,
            expected_reciprocal,
            rtol=0.0,
            atol=duality_absolute_tolerance,
        ):
            raise ValueError("basis reciprocal vector is incompatible with the period")
        converter = MODEL_SYSTEM_UNIT_CONVERTER
        if not converter.compatible(
            potential.constant_coefficient.unit, recoil_energy.unit
        ):
            raise ValueError("potential and recoil-energy units must be compatible")
        constant = converter.convert_scalar(
            potential.constant_coefficient, recoil_energy.unit
        )
        cosine = converter.convert_vector(
            potential.cosine_coefficients, recoil_energy.unit
        )
        sine = converter.convert_vector(potential.sine_coefficients, recoil_energy.unit)
        indices = np.asarray(basis.reciprocal_indices, dtype=np.float64)
        matrix = np.diag(
            recoil_energy.magnitude * np.square(reduced_momentum + indices)
            + constant.magnitude
        ).astype(np.complex128)
        for harmonic, (cosine_value, sine_value) in enumerate(
            zip(cosine.magnitude, sine.magnitude, strict=True), start=1
        ):
            diagonal_size = basis.dimension - harmonic
            if diagonal_size <= 0:
                continue
            matrix += np.diag(
                np.full(
                    diagonal_size,
                    0.5 * (cosine_value + 1j * sine_value),
                    dtype=np.complex128,
                ),
                harmonic,
            )
            matrix += np.diag(
                np.full(
                    diagonal_size,
                    0.5 * (cosine_value - 1j * sine_value),
                    dtype=np.complex128,
                ),
                -harmonic,
            )
        return PlaneWaveFiberHamiltonian1DResult(
            reduced_momentum,
            basis,
            potential,
            recoil_energy,
            duality_absolute_tolerance,
            ComplexMatrixQuantity(matrix, recoil_energy.unit),
        )
