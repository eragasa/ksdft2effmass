r"""Two-dimensional centered finite-difference Bloch operator construction.

This module owns one explicit finite representation of a spinless scalar operator on a
square dimensionless periodic cell. The finite state space is
:math:`\mathbb C^{N^2}` with Euclidean-normalized site basis vectors in
``x_outer_y_inner`` order. Grid coordinates are the half-open points
:math:`x_i=y_i=iL/N`.

For reduced Bloch momentum :math:`\boldsymbol\kappa`, coordinate period :math:`L`,
kinetic scale :math:`E_K`, and potential samples :math:`V_{ij}`, the constructor
represents

.. math::

   -E_K(\partial_x^2+\partial_y^2)+V

with the centered second-order stencil. The last-to-first positive-direction seams use
:math:`\exp(+i\kappa_dL)` and the reverse seams use their conjugates. Public records
reject binary64 spacing, stencil, diagonal, or phase arguments that underflow to zero
or overflow to nonfinite values. The dense represented matrix has dimension
:math:`N^2` and storage scaling :math:`O(N^4)`; allocation failure propagates as
:class:`MemoryError`. No continuum convergence, eigensolve, scientific validation, or
acceptance decision is included.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import numpy.typing as npt

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
)

type ComplexMatrix = npt.NDArray[np.complex128]
type ReducedMomentum2D = tuple[float, float]


@dataclass(frozen=True, slots=True)
class UniformPeriodicCoordinateBasis2D:
    """Define one square half-open coordinate grid and ordered site basis.

    Parameters
    ----------
    coordinate_period
        Positive finite built-in float :math:`L` in the model's dimensionless
        coordinate convention.
    points_per_direction
        Odd built-in integer :math:`N` of at least five.
    basis_identifier
        Nonempty identity for the coordinate-basis convention.

    Notes
    -----
    Stored basis vectors are the Euclidean-orthonormal canonical vectors associated
    with grid samples. They are not silently interpreted as normalized continuum
    position eigenstates or as quadrature-weighted basis functions.
    """

    coordinate_period: float
    points_per_direction: int
    basis_identifier: str

    def __post_init__(self) -> None:
        """Validate the coordinate period, grid extent, and basis identity.

        Raises
        ------
        TypeError
            If a field has the wrong semantic type.
        ValueError
            If the period, grid extent, or basis identity violates its domain.
        OverflowError
            If ``coordinate_period / points_per_direction`` underflows binary64 and
            therefore cannot identify a positive represented spacing.
        """
        if type(self.coordinate_period) is not float:
            raise TypeError("coordinate_period must be a built-in float")
        if not np.isfinite(self.coordinate_period) or self.coordinate_period <= 0.0:
            raise ValueError("coordinate_period must be finite and positive")
        if type(self.points_per_direction) is not int:
            raise TypeError("points_per_direction must be a built-in integer")
        if self.points_per_direction < 5 or self.points_per_direction % 2 == 0:
            raise ValueError("points_per_direction must be odd and at least five")
        if self.coordinate_period / self.points_per_direction == 0.0:
            raise OverflowError("coordinate spacing underflows binary64")
        if type(self.basis_identifier) is not str:
            raise TypeError("basis_identifier must be a string")
        if not self.basis_identifier:
            raise ValueError("basis_identifier must be nonempty")

    @property
    def spacing(self) -> float:
        """Return the uniform dimensionless coordinate spacing ``L / N``."""
        return self.coordinate_period / self.points_per_direction

    @property
    def represented_dimension(self) -> int:
        """Return the finite Euclidean state-space dimension ``N**2``."""
        return self.points_per_direction**2

    @property
    def site_indices(self) -> tuple[tuple[int, int], ...]:
        """Return site pairs in ``x``-outer, ``y``-inner order."""
        return tuple(
            (x_index, y_index)
            for x_index in range(self.points_per_direction)
            for y_index in range(self.points_per_direction)
        )

    @property
    def ordering(self) -> Literal["x_outer_y_inner"]:
        """Return the fixed flattened-site ordering."""
        return "x_outer_y_inner"

    @property
    def normalization(self) -> Literal["euclidean_site_basis"]:
        """Return the fixed finite-basis normalization convention."""
        return "euclidean_site_basis"


@dataclass(frozen=True, slots=True, eq=False)
class FiniteDifferenceBlochHamiltonian2DModel:
    """Define one complete finite-difference representation input.

    Parameters
    ----------
    basis
        Square half-open coordinate grid and Euclidean site-basis definition.
    potential_samples
        Immutable real ``(N, N)`` potential samples in ``x``-outer, ``y``-inner
        order.
    kinetic_scale
        Positive finite energy multiplying the dimensionless negative Laplacian.
    source_identifier
        Nonempty identity for the source from which the samples were obtained.
    operator_identifier
        Nonempty identity for the represented operator.
    state_space_identifier
        Nonempty identity for the represented finite state space.
    energy_reference
        Nonempty identity for the represented operator's zero of energy.
    provenance_identifier
        Nonempty identity for the sampling and discretization provenance.

    Raises
    ------
    TypeError
        If a composed record or identifier has the wrong semantic type.
    ValueError
        If potential shape, energy unit, kinetic positivity, or identifier invariants
        fail.
    OverflowError
        If ``E_K / h**2`` underflows or overflows binary64, if the kinetic diagonal is
        not representable, or if adding finite potential samples would make the
        represented diagonal nonfinite.

    Notes
    -----
    ``Model`` denotes the complete finite representation definition, not a nominal
    scientific :class:`~ksdft2effmass.periodic.PeriodicModel` parent. Potential
    samples are data rather than an arbitrary callable so their values, order, unit,
    and source binding remain explicit.
    """

    basis: UniformPeriodicCoordinateBasis2D
    potential_samples: MatrixQuantity
    kinetic_scale: ScalarQuantity
    source_identifier: str
    operator_identifier: str
    state_space_identifier: str
    energy_reference: str
    provenance_identifier: str

    def __post_init__(self) -> None:
        """Validate basis, potential, energy, and semantic identities."""
        self._check_args_basis_and_potential()
        self._check_args_energy_scale()
        self._check_args_identifiers()

    def _check_args_basis_and_potential(self) -> None:
        """Require an exact basis and matching immutable potential samples."""
        if type(self.basis) is not UniformPeriodicCoordinateBasis2D:
            raise TypeError("basis must be UniformPeriodicCoordinateBasis2D")
        if type(self.potential_samples) is not MatrixQuantity:
            raise TypeError("potential_samples must be MatrixQuantity")
        points = self.basis.points_per_direction
        if self.potential_samples.magnitude.shape != (points, points):
            raise ValueError("potential_samples shape must match the coordinate grid")

    def _check_args_energy_scale(self) -> None:
        """Require one representable kinetic stencil and common energy unit."""
        if type(self.kinetic_scale) is not ScalarQuantity:
            raise TypeError("kinetic_scale must be ScalarQuantity")
        if self.kinetic_scale.magnitude <= 0.0:
            raise ValueError("kinetic_scale must be positive")
        if self.potential_samples.unit != self.kinetic_scale.unit:
            raise ValueError("potential_samples and kinetic_scale must use one unit")
        coefficient = self.kinetic_stencil_coefficient
        maximum = np.finfo(np.float64).max
        if coefficient > maximum / 4.0:
            raise OverflowError("finite-difference kinetic diagonal overflows binary64")
        kinetic_diagonal = 4.0 * coefficient
        with np.errstate(over="ignore", invalid="ignore"):
            represented_diagonal = kinetic_diagonal + self.potential_samples.magnitude
        if not np.all(np.isfinite(represented_diagonal)):
            raise OverflowError("finite-difference represented diagonal overflows")

    def _check_args_identifiers(self) -> None:
        """Require every represented-space and provenance identity explicitly."""
        for name, identifier in (
            ("source_identifier", self.source_identifier),
            ("operator_identifier", self.operator_identifier),
            ("state_space_identifier", self.state_space_identifier),
            ("energy_reference", self.energy_reference),
            ("provenance_identifier", self.provenance_identifier),
        ):
            if type(identifier) is not str:
                raise TypeError(f"{name} must be a string")
            if not identifier:
                raise ValueError(f"{name} must be nonempty")

    @property
    def kinetic_stencil_coefficient(self) -> float:
        """Return the finite positive binary64 coefficient ``E_K / h**2``.

        The expression preserves the established valid-input rounding route. An
        unrepresentable ``h**2`` intermediate or a zero/nonfinite quotient cannot
        define that route and raises :class:`OverflowError` during model construction.
        """
        spacing = self.basis.spacing
        try:
            spacing_squared = spacing**2
        except OverflowError as error:
            raise OverflowError(
                "squared coordinate spacing overflows binary64"
            ) from error
        if spacing_squared == 0.0 or not np.isfinite(spacing_squared):
            raise OverflowError("squared coordinate spacing is outside binary64 range")
        coefficient = self.kinetic_scale.magnitude / spacing_squared
        if coefficient == 0.0 or not np.isfinite(coefficient):
            raise OverflowError(
                "finite-difference kinetic coefficient is outside binary64 range"
            )
        return coefficient

    @property
    def represented_dimension(self) -> int:
        """Return the exact finite state-space dimension."""
        return self.basis.represented_dimension

    @property
    def spin_convention(self) -> Literal["spinless_scalar"]:
        """Return the fixed spin and internal-degree convention."""
        return "spinless_scalar"

    @property
    def stencil(self) -> Literal["centered_second_order"]:
        """Return the fixed finite-difference stencil identity."""
        return "centered_second_order"


@dataclass(frozen=True, slots=True)
class FiniteDifferenceBlochHamiltonian2DRequest:
    """Request one Bloch fiber of a finite-difference representation.

    ``reduced_momentum`` is a pair of finite built-in floats in the dimensionless
    reciprocal coordinates dual to the square coordinate period. It determines the
    seam phases and is not silently interpreted as a Cartesian physical wave vector.
    Construction rejects a finite pair whose product with the coordinate period would
    make either seam-phase argument nonfinite.
    """

    model: FiniteDifferenceBlochHamiltonian2DModel
    reduced_momentum: ReducedMomentum2D

    def __post_init__(self) -> None:
        """Validate the exact model, reduced momentum, and seam arguments.

        Raises
        ------
        TypeError
            If the model or momentum has the wrong semantic type.
        ValueError
            If either momentum component is nonfinite.
        OverflowError
            If a seam argument ``kappa_d * L`` is not representable as finite
            binary64 and therefore cannot define a phase.
        """
        if type(self.model) is not FiniteDifferenceBlochHamiltonian2DModel:
            raise TypeError("model must be FiniteDifferenceBlochHamiltonian2DModel")
        if type(self.reduced_momentum) is not tuple or len(self.reduced_momentum) != 2:
            raise TypeError("reduced_momentum must be a two-component tuple")
        if any(type(component) is not float for component in self.reduced_momentum):
            raise TypeError("reduced_momentum components must be built-in floats")
        if any(not np.isfinite(component) for component in self.reduced_momentum):
            raise ValueError("reduced_momentum components must be finite")
        period = self.model.basis.coordinate_period
        if any(
            not np.isfinite(component * period) for component in self.reduced_momentum
        ):
            raise OverflowError("Bloch seam phase argument overflows binary64")

    @property
    def boundary_phase_x(self) -> complex:
        """Return the last-to-first positive-x seam phase."""
        return complex(
            np.exp(1j * self.reduced_momentum[0] * self.model.basis.coordinate_period)
        )

    @property
    def boundary_phase_y(self) -> complex:
        """Return the last-to-first positive-y seam phase."""
        return complex(
            np.exp(1j * self.reduced_momentum[1] * self.model.basis.coordinate_period)
        )


@dataclass(frozen=True, slots=True, eq=False)
class FiniteDifferenceBlochHamiltonian2DResult:
    """Retain one represented finite-difference operator and complete request.

    The immutable matrix has the request model's exact dimension and energy unit and
    must be exactly Hermitian. This result is represented-space output, not a continuum
    operator, retained operator, convergence result, or campaign acceptance decision.
    """

    request: FiniteDifferenceBlochHamiltonian2DRequest
    represented_matrix: ComplexMatrixQuantity

    def __post_init__(self) -> None:
        """Validate request correlation, matrix shape, unit, and Hermiticity."""
        if type(self.request) is not FiniteDifferenceBlochHamiltonian2DRequest:
            raise TypeError("request must be FiniteDifferenceBlochHamiltonian2DRequest")
        if type(self.represented_matrix) is not ComplexMatrixQuantity:
            raise TypeError("represented_matrix must be ComplexMatrixQuantity")
        dimension = self.request.model.represented_dimension
        if self.represented_matrix.magnitude.shape != (dimension, dimension):
            raise ValueError("represented_matrix shape must match the coordinate basis")
        if self.represented_matrix.unit != self.request.model.kinetic_scale.unit:
            raise ValueError("represented_matrix must use the model energy unit")
        matrix = self.represented_matrix.magnitude
        if not np.array_equal(matrix, matrix.conj().T):
            raise ValueError("represented_matrix must be exactly Hermitian")


class FiniteDifferenceBlochHamiltonian2DConstructor:
    """Construct a centered finite-difference Bloch operator.

    The Action preserves the declared half-open grid, ``x_outer_y_inner`` order,
    Euclidean site normalization, and directed seam convention. It performs no
    eigensolve, convergence assessment, common-space transport, or acceptance test.
    """

    __slots__ = ()

    def execute(
        self, request: FiniteDifferenceBlochHamiltonian2DRequest
    ) -> FiniteDifferenceBlochHamiltonian2DResult:
        """Construct the represented matrix in the declared coordinate basis.

        Raises
        ------
        TypeError
            If ``request`` has the wrong semantic type.
        OverflowError
            If matrix assembly produces a nonfinite value despite the request's
            representability checks.
        MemoryError
            If the dense ``(N**2, N**2)`` allocation cannot be satisfied. Dense
            storage scales as ``O(N**4)`` and this Action imposes no arbitrary cap.
        """
        if type(request) is not FiniteDifferenceBlochHamiltonian2DRequest:
            raise TypeError("request must be FiniteDifferenceBlochHamiltonian2DRequest")
        model = request.model
        points = model.basis.points_per_direction
        period = model.basis.coordinate_period
        coefficient = model.kinetic_stencil_coefficient
        kinetic_x = self._one_dimensional(
            request.reduced_momentum[0], points, period, coefficient
        )
        kinetic_y = self._one_dimensional(
            request.reduced_momentum[1], points, period, coefficient
        )
        identity = np.eye(points, dtype=np.complex128)
        # Kronecker ordering matches the declared x-outer, y-inner site inventory.
        matrix = np.kron(kinetic_x, identity) + np.kron(identity, kinetic_y)
        matrix += np.diag(model.potential_samples.magnitude.ravel(order="C"))
        if not np.all(np.isfinite(matrix.real)) or not np.all(np.isfinite(matrix.imag)):
            raise OverflowError("finite-difference matrix contains nonfinite values")
        return FiniteDifferenceBlochHamiltonian2DResult(
            request=request,
            represented_matrix=ComplexMatrixQuantity(
                matrix,
                model.kinetic_scale.unit,
            ),
        )

    @staticmethod
    def _one_dimensional(
        momentum: float,
        points: int,
        period: float,
        stencil_coefficient: float,
    ) -> ComplexMatrix:
        """Return one centered negative-Laplacian block with Bloch seams."""
        matrix = np.diag(np.full(points, 2.0 * stencil_coefficient)).astype(
            np.complex128
        )
        off_diagonal = -stencil_coefficient
        matrix += np.diag(np.full(points - 1, off_diagonal), 1)
        matrix += np.diag(np.full(points - 1, off_diagonal), -1)
        # Row/column orientation is fixed: last-to-first in the positive coordinate
        # direction carries exp(+i*kappa*L); the reverse entry is its conjugate.
        matrix[0, -1] = off_diagonal * np.exp(-1j * momentum * period)
        matrix[-1, 0] = off_diagonal * np.exp(1j * momentum * period)
        return matrix
