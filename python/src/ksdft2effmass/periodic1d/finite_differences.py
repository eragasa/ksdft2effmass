"""Half-open grids and twisted finite-difference fibers in one dimension."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexSparseMatrixQuantity,
    ScalarQuantity,
    VectorQuantity,
)

from .fibers import Periodic1DFiberHamiltonianRequest


@dataclass(frozen=True, slots=True)
class PeriodicUniformGrid1D:
    """Represent ordered coordinates on one half-open periodic cell.

    Parameters
    ----------
    origin
        First grid coordinate.
    period
        Positive cell period and canonical coordinate unit.
    point_count
        Exact built-in integer number of points, at least three.  Booleans and
        NumPy integer substitutes are rejected.

    Raises
    ------
    TypeError
        If a quantity has the wrong exact type or ``point_count`` is not an exact
        built-in integer.
    ValueError
        If coordinate units are incompatible, the period is not positive, or
        fewer than three points are requested.

    Notes
    -----
    Coordinates are ordered as ``origin + j * period / point_count`` for
    ``j = 0, ..., point_count - 1``.  The endpoint is excluded exactly by
    construction; no sorting or seam duplication occurs.
    """

    origin: ScalarQuantity
    period: ScalarQuantity
    point_count: int

    def __post_init__(self) -> None:
        """Validate quantities and canonicalize the origin to the period unit."""
        if type(self.origin) is not ScalarQuantity:
            raise TypeError("origin must be ScalarQuantity")
        if type(self.period) is not ScalarQuantity:
            raise TypeError("period must be ScalarQuantity")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.origin.unit, self.period.unit
        ):
            raise ValueError("origin and period units must be compatible")
        object.__setattr__(
            self,
            "origin",
            MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(self.origin, self.period.unit),
        )
        if self.period.magnitude <= 0.0:
            raise ValueError("period must be positive")
        if type(self.point_count) is not int:
            raise TypeError("point_count must be a built-in int")
        if self.point_count < 3:
            raise ValueError("point_count must be at least three")

    @property
    def spacing(self) -> ScalarQuantity:
        """Return the positive periodic-grid spacing in the period unit."""
        return ScalarQuantity(
            self.period.magnitude / float(self.point_count), self.period.unit
        )

    @property
    def coordinates(self) -> VectorQuantity:
        """Return immutable ordered half-open cell coordinates.

        Returns
        -------
        VectorQuantity
            Coordinates in the period unit and original index order.

        Raises
        ------
        OverflowError
            If coordinates are not representable in binary64.
        MemoryError
            If the length-``point_count`` coordinate vector cannot be allocated.
        """
        try:
            with np.errstate(over="raise", invalid="raise"):
                values = self.origin.magnitude + self.spacing.magnitude * np.arange(
                    self.point_count, dtype=np.float64
                )
        except FloatingPointError as exc:
            raise OverflowError(
                "grid coordinates are not representable in binary64"
            ) from exc
        if not np.all(np.isfinite(values)):
            raise OverflowError("grid coordinates are not representable in binary64")
        return VectorQuantity(values, self.period.unit)


@dataclass(frozen=True, slots=True, eq=False)
class PeriodicFiniteDifferenceFiberHamiltonian1DResult:
    """Retain one parent-qualified twisted finite-difference fiber.

    Parameters
    ----------
    request
        Exact request carrying parent-model, represented-operator, and finite
        state-space identities and reduced momentum.
    grid
        Ordered half-open coordinate grid fixing matrix row and column order.
    period_absolute_tolerance
        Nonnegative built-in float used during construction to check grid and
        parent-potential periods.
    represented_matrix
        Immutable sparse complex energy matrix in grid-point order.  Its corner
        entries retain the directed conjugate Bloch seam.

    Raises
    ------
    TypeError
        If a field has the wrong exact domain type or the tolerance is not an
        exact built-in float.
    ValueError
        If the tolerance is invalid, matrix shape differs from the grid, or
        matrix and parent recoil-energy units disagree.

    Notes
    -----
    This Result checks retained intrinsic structure, not Constructor execution or
    provenance authenticity.  It is a finite discretization of the parent model,
    not the parent operator itself.  Construction does not establish mesh
    convergence, physical adequacy, scientific validation, or uncertainty
    quantification.
    """

    request: Periodic1DFiberHamiltonianRequest
    grid: PeriodicUniformGrid1D
    period_absolute_tolerance: float
    represented_matrix: ComplexSparseMatrixQuantity

    def __post_init__(self) -> None:
        """Validate exact components, tolerance, shape, and energy unit."""
        self._check_args_components_and_tolerance()
        self._check_args_matrix_correlation()

    def _check_args_components_and_tolerance(self) -> None:
        """Require exact request/grid types and a finite nonnegative tolerance."""
        if type(self.request) is not Periodic1DFiberHamiltonianRequest:
            raise TypeError("request must be Periodic1DFiberHamiltonianRequest")
        if type(self.grid) is not PeriodicUniformGrid1D:
            raise TypeError("grid must be PeriodicUniformGrid1D")
        if type(self.period_absolute_tolerance) is not float:
            raise TypeError("period_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.period_absolute_tolerance)
            or self.period_absolute_tolerance < 0.0
        ):
            raise ValueError("period_absolute_tolerance must be finite and nonnegative")
        if type(self.represented_matrix) is not ComplexSparseMatrixQuantity:
            raise TypeError("represented_matrix must be ComplexSparseMatrixQuantity")

    def _check_args_matrix_correlation(self) -> None:
        """Require grid-sized storage in the parent's recoil-energy unit."""
        expected_shape = (self.grid.point_count, self.grid.point_count)
        if self.represented_matrix.shape != expected_shape:
            raise ValueError("represented_matrix shape must match the grid")
        if self.represented_matrix.unit != self.request.parent_model.recoil_energy.unit:
            raise ValueError("represented_matrix must use the recoil-energy unit")


class PeriodicFiniteDifferenceFiberHamiltonian1DConstructor:
    """Construct sparse second-order fibers while preserving seam orientation."""

    __slots__ = ()

    def execute(
        self,
        request: Periodic1DFiberHamiltonianRequest,
        grid: PeriodicUniformGrid1D,
        period_absolute_tolerance: float,
    ) -> PeriodicFiniteDifferenceFiberHamiltonian1DResult:
        r"""Construct the central-difference Hamiltonian with its Bloch seam.

        Parameters
        ----------
        request
            Parent-qualified request.  The parent supplies the potential and
            recoil-energy scale; identities are never inferred from dimensions.
        grid
            Ordered half-open periodic grid.
        period_absolute_tolerance
            Finite nonnegative built-in float used with zero relative tolerance
            for grid--potential period compatibility.

        Returns
        -------
        PeriodicFiniteDifferenceFiberHamiltonian1DResult
            Immutable sparse represented fiber.

        Raises
        ------
        TypeError
            If an argument has the wrong exact domain type.
        ValueError
            If the tolerance is invalid, periods disagree, or parent potential
            and recoil-energy units are incompatible.
        OverflowError
            If accepted finite input cannot be represented by binary64 or
            complex128 arithmetic.
        MemoryError
            If grid sampling or sparse matrix storage cannot be allocated.

        Notes
        -----
        For ``N`` grid points and ``M`` Fourier harmonics, construction uses
        ``O(N)`` sparse storage and ``O(N M)`` potential-evaluation time.  No
        arbitrary size cap is imposed.  The directed corner convention is

        ``H[0, N-1] = -t exp(-2π i k)`` and
        ``H[N-1, 0] = conjugate(H[0, N-1])``.

        The operation constructs one discretization only and does not establish
        mesh convergence or scientific validity.
        """
        self._check_args(request, grid, period_absolute_tolerance)
        model = request.parent_model
        potential = model.potential
        recoil_energy = model.recoil_energy
        potential_period = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            potential.period, grid.period.unit
        )
        if not np.isclose(
            potential_period.magnitude,
            grid.period.magnitude,
            rtol=0.0,
            atol=period_absolute_tolerance,
        ):
            raise ValueError("grid and potential periods do not agree")
        converter = MODEL_SYSTEM_UNIT_CONVERTER
        if not converter.compatible(
            potential.constant_coefficient.unit, recoil_energy.unit
        ):
            raise ValueError("potential and recoil-energy units must be compatible")
        try:
            with np.errstate(over="raise", invalid="raise"):
                sampled_potential = converter.convert_vector(
                    potential.evaluate(grid.coordinates), recoil_energy.unit
                )
                reciprocal_spacing = 2.0 * np.pi / float(grid.point_count)
                kinetic_link = recoil_energy.magnitude / (reciprocal_spacing**2)
                diagonal = 2.0 * kinetic_link + sampled_potential.magnitude
                dimension = grid.point_count
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
                # The upper-right edge transports from the final point back to
                # the first with exp(-2πik); the reverse edge is its conjugate.
                seam = -kinetic_link * np.exp(-2j * np.pi * request.reduced_momentum)
                matrix[0, dimension - 1] = seam
                matrix[dimension - 1, 0] = np.conjugate(seam)
        except FloatingPointError as exc:
            raise OverflowError(
                "finite-difference fiber is not representable in complex128"
            ) from exc
        represented = ComplexSparseMatrixQuantity.from_csr(
            matrix.tocsr(), recoil_energy.unit
        )
        return PeriodicFiniteDifferenceFiberHamiltonian1DResult(
            request=request,
            grid=grid,
            period_absolute_tolerance=period_absolute_tolerance,
            represented_matrix=represented,
        )

    @staticmethod
    def _check_args(
        request: Periodic1DFiberHamiltonianRequest,
        grid: PeriodicUniformGrid1D,
        period_absolute_tolerance: float,
    ) -> None:
        """Validate exact operation inputs before sampling and assembly."""
        if type(request) is not Periodic1DFiberHamiltonianRequest:
            raise TypeError("request must be Periodic1DFiberHamiltonianRequest")
        if type(grid) is not PeriodicUniformGrid1D:
            raise TypeError("grid must be PeriodicUniformGrid1D")
        if type(period_absolute_tolerance) is not float:
            raise TypeError("period_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(period_absolute_tolerance)
            or period_absolute_tolerance < 0.0
        ):
            raise ValueError("period_absolute_tolerance must be finite and nonnegative")


__all__ = [
    "PeriodicFiniteDifferenceFiberHamiltonian1DConstructor",
    "PeriodicFiniteDifferenceFiberHamiltonian1DResult",
    "PeriodicUniformGrid1D",
]
