"""Finite plane-wave fibers for parent-qualified periodic-1D models."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
)
from ksdft2effmass.solid_state import PlaneWaveBasis1D

from .fibers import Periodic1DFiberHamiltonianRequest


@dataclass(frozen=True, slots=True, eq=False)
class PlaneWaveFiberHamiltonian1DResult:
    """Retain one parent-qualified finite plane-wave fiber.

    Parameters
    ----------
    request
        Exact request carrying stable parent-model, represented-operator, and
        finite-state-space identities and the reduced momentum.
    basis
        Ordered finite plane-wave basis.  Its reciprocal indices fix matrix row
        and column order exactly; the result never sorts or relabels them.
    duality_absolute_tolerance
        Nonnegative built-in float used only to check period--reciprocal-vector
        duality during construction.
    represented_matrix
        Immutable complex energy matrix in ``basis.reciprocal_indices`` order.

    Raises
    ------
    TypeError
        If a field has the wrong exact domain type or the tolerance is not an
        exact built-in float.
    ValueError
        If the tolerance is nonfinite or negative, matrix shape differs from the
        basis dimension, or matrix and parent recoil-energy units disagree.

    Notes
    -----
    This Result validates intrinsic immutable structure and retained correlation;
    it does not prove that a Constructor executed or authenticate provenance.
    The finite Galerkin matrix remains distinct from the untruncated parent
    operator.  Passing these checks establishes neither basis convergence,
    physical adequacy, scientific validation, nor uncertainty quantification.
    """

    request: Periodic1DFiberHamiltonianRequest
    basis: PlaneWaveBasis1D
    duality_absolute_tolerance: float
    represented_matrix: ComplexMatrixQuantity

    def __post_init__(self) -> None:
        """Validate exact components, tolerance, shape, and energy unit."""
        self._check_args_components_and_tolerance()
        self._check_args_matrix_correlation()

    def _check_args_components_and_tolerance(self) -> None:
        """Require exact request/basis types and a finite nonnegative tolerance."""
        if type(self.request) is not Periodic1DFiberHamiltonianRequest:
            raise TypeError("request must be Periodic1DFiberHamiltonianRequest")
        if type(self.basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
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

    def _check_args_matrix_correlation(self) -> None:
        """Require basis-sized storage in the parent's recoil-energy unit."""
        if self.represented_matrix.magnitude.shape != (
            self.basis.dimension,
            self.basis.dimension,
        ):
            raise ValueError("represented_matrix shape must match the basis")
        if self.represented_matrix.unit != self.request.parent_model.recoil_energy.unit:
            raise ValueError("represented_matrix must use the recoil-energy unit")


class PlaneWaveFiberHamiltonian1DConstructor:
    """Construct finite plane-wave fibers without changing scientific identity."""

    __slots__ = ()

    def execute(
        self,
        request: Periodic1DFiberHamiltonianRequest,
        basis: PlaneWaveBasis1D,
        duality_absolute_tolerance: float,
    ) -> PlaneWaveFiberHamiltonian1DResult:
        r"""Construct :math:`H_{nm}(k)` in reciprocal-basis order.

        Parameters
        ----------
        request
            Parent-qualified request.  The parent supplies the Fourier potential
            and positive recoil-energy scale; identities are not inferred from
            the basis or resulting matrix.
        basis
            Ordered finite plane-wave basis.  ``basis.reciprocal_indices`` is the
            exact output matrix ordering.
        duality_absolute_tolerance
            Finite nonnegative built-in float used with zero relative tolerance
            to compare the basis reciprocal vector with :math:`2\pi/a`.

        Returns
        -------
        PlaneWaveFiberHamiltonian1DResult
            Immutable parent-qualified represented fiber.

        Raises
        ------
        TypeError
            If an argument has the wrong exact domain type.
        ValueError
            If the tolerance is invalid, period and reciprocal vector disagree,
            or potential and recoil-energy units are incompatible.
        OverflowError
            If accepted finite input cannot be represented by the binary64 or
            complex128 arithmetic used to assemble the matrix.
        MemoryError
            If storage for the dense represented matrix cannot be allocated.

        Notes
        -----
        For basis dimension ``N`` and ``M`` potential harmonics, assembly uses
        ``O(N^2)`` storage and ``O(N^2 + N min(M, N))`` time.  No arbitrary size
        cap is imposed.  The operation constructs one discretization only; it
        does not establish discretization convergence or scientific validity.
        """
        self._check_args(request, basis, duality_absolute_tolerance)
        model = request.parent_model
        potential = model.potential
        recoil_energy = model.recoil_energy
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
        try:
            with np.errstate(over="raise", invalid="raise"):
                matrix = np.diag(
                    recoil_energy.magnitude
                    * np.square(request.reduced_momentum + indices)
                    + constant.magnitude
                ).astype(np.complex128)
                # Positive and negative Fourier harmonics populate conjugate
                # diagonals without changing the basis-owned reciprocal order.
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
        except FloatingPointError as exc:
            raise OverflowError(
                "plane-wave fiber is not representable in complex128"
            ) from exc
        if not np.all(np.isfinite(matrix)):
            raise OverflowError("plane-wave fiber is not representable in complex128")
        return PlaneWaveFiberHamiltonian1DResult(
            request=request,
            basis=basis,
            duality_absolute_tolerance=duality_absolute_tolerance,
            represented_matrix=ComplexMatrixQuantity(matrix, recoil_energy.unit),
        )

    @staticmethod
    def _check_args(
        request: Periodic1DFiberHamiltonianRequest,
        basis: PlaneWaveBasis1D,
        duality_absolute_tolerance: float,
    ) -> None:
        """Validate exact operation inputs before numerical assembly."""
        if type(request) is not Periodic1DFiberHamiltonianRequest:
            raise TypeError("request must be Periodic1DFiberHamiltonianRequest")
        if type(basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
        if type(duality_absolute_tolerance) is not float:
            raise TypeError("duality_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(duality_absolute_tolerance)
            or duality_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "duality_absolute_tolerance must be finite and nonnegative"
            )


__all__ = [
    "PlaneWaveFiberHamiltonian1DConstructor",
    "PlaneWaveFiberHamiltonian1DResult",
]
