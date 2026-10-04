"""Dimensionless two-dimensional cosine-potential toy Hamiltonians."""

from dataclasses import dataclass
from typing import Literal

import numpy as np
import numpy.typing as npt
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    ReciprocalLattice2D,
)

from ksdft2effmass.analysis.model_systems.periodic2d import (
    PlaneWaveBlochHamiltonian2DConstructor,
    PlaneWaveBlochHamiltonian2DModel,
    PlaneWaveBlochHamiltonian2DRequest,
    PlaneWaveFourierCoefficient2D,
)
from ksdft2effmass.operators import ScalarQuantity, Unitless
from ksdft2effmass.periodic import Periodic2DModel, PeriodicModelRole

type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Periodic2DCosinePotentialToyModel(Periodic2DModel):
    """Represent a nominal spinless dimensionless periodic cosine toy model.

    The parent potential is
    ``lambda_x*cos(x) + lambda_y*cos(y) + lambda_xy*cos(x)*cos(y)`` on a
    square cell of period ``2*pi``. Energies use the reciprocal kinetic scale.

    Parameters
    ----------
    lambda_x
        Finite built-in-float coefficient of ``cos(x)``.
    lambda_y
        Finite built-in-float coefficient of ``cos(y)``.
    lambda_xy
        Finite built-in-float coefficient of ``cos(x)*cos(y)``.

    Notes
    -----
    ``model_id`` identifies this maintained model family; the immutable coupling
    values identify its configured instance. Nominal membership and the exact toy role
    do not establish material realism, scientific validation, or uncertainty
    quantification. Finite plane-wave and finite-difference matrices remain separate
    represented operators.
    """

    lambda_x: float
    lambda_y: float
    lambda_xy: float

    def __post_init__(self) -> None:
        """Validate the configured parent-model coefficients."""
        self._check_args_couplings()

    def _check_args_couplings(self) -> None:
        """Require exact finite binary64 coefficients for every Fourier channel."""
        # These are physical-model inputs, so booleans and coercible numeric strings
        # must not cross the public boundary as if they were real coefficients.
        for name, value in (
            ("lambda_x", self.lambda_x),
            ("lambda_y", self.lambda_y),
            ("lambda_xy", self.lambda_xy),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a float")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")

    @property
    def model_id(self) -> str:
        """Return the stable cosine-potential toy-family identity."""
        return "periodic2d.cosine-potential-toy"

    @property
    def model_role(self) -> PeriodicModelRole:
        """Return the exact toy-model evidentiary role."""
        return PeriodicModelRole.TOY

    @property
    def direct_lattice(self) -> DirectLattice2D:
        """Return the dimensionless square direct lattice ``A = 2*pi*I``."""
        # The cosine arguments are dimensionless, so each primitive coordinate repeats
        # after exactly 2*pi rather than after a material length supplied elsewhere.
        period = 2.0 * np.pi
        return DirectLattice2D(
            a1=np.array((period, 0.0), dtype=np.float64),
            a2=np.array((0.0, period), dtype=np.float64),
        )

    @property
    def reciprocal_lattice(self) -> ReciprocalLattice2D:
        """Return the two-pi-dual reciprocal lattice ``B = I``."""
        return ReciprocalLattice2D.from_direct_lattice(self.direct_lattice)


@dataclass(frozen=True, slots=True)
class Periodic2DPlaneWaveBasis:
    """Define one square finite reciprocal basis in deterministic pair order."""

    cutoff: int

    def __post_init__(self) -> None:
        """Require a nonnegative built-in integer cutoff."""
        if type(self.cutoff) is not int:
            raise TypeError("cutoff must be a built-in integer")
        if self.cutoff < 0:
            raise ValueError("cutoff must be nonnegative")

    @property
    def reciprocal_indices(self) -> tuple[tuple[int, int], ...]:
        """Return reciprocal pairs in ``p``-outer, ``q``-inner order."""
        return tuple(
            (p, q)
            for p in range(-self.cutoff, self.cutoff + 1)
            for q in range(-self.cutoff, self.cutoff + 1)
        )

    @property
    def represented_dimension(self) -> int:
        """Return the number of reciprocal basis vectors."""
        return (2 * self.cutoff + 1) ** 2

    @property
    def ordering(self) -> Literal["p_outer_q_inner"]:
        """Return the reciprocal-index ordering identifier."""
        return "p_outer_q_inner"


@dataclass(frozen=True, slots=True)
class Periodic2DUniformCellGrid:
    """Define one odd uniform grid on a dimensionless period-``2*pi`` cell."""

    points_per_direction: int

    def __post_init__(self) -> None:
        """Require an odd built-in integer grid size of at least five."""
        if type(self.points_per_direction) is not int:
            raise TypeError("points_per_direction must be a built-in integer")
        if self.points_per_direction < 5 or self.points_per_direction % 2 == 0:
            raise ValueError("points_per_direction must be odd and at least five")

    @property
    def period(self) -> float:
        """Return the dimensionless square-cell period."""
        return 2.0 * np.pi

    @property
    def spacing(self) -> float:
        """Return the uniform coordinate spacing."""
        return self.period / self.points_per_direction

    @property
    def represented_dimension(self) -> int:
        """Return the number of coordinate-basis sites."""
        return self.points_per_direction**2

    @property
    def site_indices(self) -> tuple[tuple[int, int], ...]:
        """Return grid indices in ``x``-outer, ``y``-inner order."""
        return tuple(
            (x_index, y_index)
            for x_index in range(self.points_per_direction)
            for y_index in range(self.points_per_direction)
        )

    @property
    def ordering(self) -> Literal["x_outer_y_inner"]:
        """Return the flattened coordinate ordering identifier."""
        return "x_outer_y_inner"


@dataclass(frozen=True, slots=True)
class Periodic2DPlaneWaveHamiltonianRequest:
    r"""Request a finite plane-wave representation of the toy Hamiltonian.

    Reduced momentum components are built-in floats giving the coefficients
    :math:`\boldsymbol\kappa` in the PhysKit reciprocal primitive basis ``B`` of the
    period-``2*pi`` cell. ``cutoff`` is a built-in integer. Each kinetic diagonal is
    :math:`\lVert B(\boldsymbol\kappa+\mathbf n)\rVert^2` in the reciprocal
    kinetic-energy scale, with the model's fixed zero of energy.
    ``duality_absolute_tolerance`` is the nonnegative maximum-component tolerance for
    :math:`A^{\mathsf T}B-2\pi I`; its default covers binary64 reconstruction of the
    fixed square lattice and is not a scientific acceptance threshold.
    """

    model: Periodic2DCosinePotentialToyModel
    reduced_momentum_x: float
    reduced_momentum_y: float
    cutoff: int
    duality_absolute_tolerance: float = 4.0e-15

    def __post_init__(self) -> None:
        """Validate the model, momentum coordinates, and symmetric cutoff."""
        if type(self.model) is not Periodic2DCosinePotentialToyModel:
            raise TypeError("model must be Periodic2DCosinePotentialToyModel")
        for name, value in (
            ("reduced_momentum_x", self.reduced_momentum_x),
            ("reduced_momentum_y", self.reduced_momentum_y),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")
        Periodic2DPlaneWaveBasis(self.cutoff)
        if type(self.duality_absolute_tolerance) is not float:
            raise TypeError("duality_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.duality_absolute_tolerance)
            or self.duality_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "duality_absolute_tolerance must be finite and nonnegative"
            )

    @property
    def basis(self) -> Periodic2DPlaneWaveBasis:
        """Return the immutable reciprocal-basis identity."""
        return Periodic2DPlaneWaveBasis(self.cutoff)

    @property
    def reciprocal_indices(self) -> tuple[tuple[int, int], ...]:
        """Return reciprocal pairs in the represented basis order."""
        return self.basis.reciprocal_indices

    @property
    def represented_dimension(self) -> int:
        """Return the finite plane-wave basis dimension."""
        return self.basis.represented_dimension

    @property
    def basis_ordering(self) -> Literal["p_outer_q_inner"]:
        """Return the declared reciprocal-index ordering identifier."""
        return self.basis.ordering


@dataclass(frozen=True, slots=True)
class Periodic2DFiniteDifferenceHamiltonianRequest:
    """Request a centered finite-difference representation on the square cell.

    Reduced momentum components are built-in floats in the dimensionless reciprocal
    coordinates of the period-``2*pi`` cell. ``points_per_direction`` is a built-in
    integer. The represented matrix uses the model's reciprocal kinetic-energy scale
    and fixed zero of energy.
    """

    model: Periodic2DCosinePotentialToyModel
    reduced_momentum_x: float
    reduced_momentum_y: float
    points_per_direction: int

    def __post_init__(self) -> None:
        """Validate the model, momentum coordinates, and odd grid size."""
        if type(self.model) is not Periodic2DCosinePotentialToyModel:
            raise TypeError("model must be Periodic2DCosinePotentialToyModel")
        for name, value in (
            ("reduced_momentum_x", self.reduced_momentum_x),
            ("reduced_momentum_y", self.reduced_momentum_y),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")
        Periodic2DUniformCellGrid(self.points_per_direction)

    @property
    def grid(self) -> Periodic2DUniformCellGrid:
        """Return the immutable coordinate-grid identity."""
        return Periodic2DUniformCellGrid(self.points_per_direction)

    @property
    def period(self) -> float:
        """Return the dimensionless square-cell period."""
        return self.grid.period

    @property
    def spacing(self) -> float:
        """Return the uniform real-space grid spacing."""
        return self.grid.spacing

    @property
    def represented_dimension(self) -> int:
        """Return the finite coordinate-basis dimension."""
        return self.grid.represented_dimension

    @property
    def site_ordering(self) -> Literal["x_outer_y_inner"]:
        """Return the declared flattened coordinate ordering identifier."""
        return self.grid.ordering

    @property
    def boundary_phase_x(self) -> complex:
        """Return the phase multiplying the last-to-first positive-x seam."""
        return complex(np.exp(1j * self.reduced_momentum_x * self.period))

    @property
    def boundary_phase_y(self) -> complex:
        """Return the phase multiplying the last-to-first positive-y seam."""
        return complex(np.exp(1j * self.reduced_momentum_y * self.period))


@dataclass(frozen=True, slots=True)
class Periodic2DHamiltonianResult:
    """Retain one operationally immutable finite represented Hamiltonian."""

    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        """Copy one finite square Hermitian matrix into immutable storage."""
        matrix = np.asarray(self.matrix, dtype=np.complex128)
        if (
            matrix.ndim != 2
            or matrix.shape[0] == 0
            or matrix.shape[0] != matrix.shape[1]
        ):
            raise ValueError("matrix must be nonempty and square")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("matrix must contain only finite values")
        if not np.array_equal(matrix, matrix.conj().T):
            raise ValueError("matrix must be exactly Hermitian")
        immutable = np.frombuffer(
            matrix.tobytes(order="C"), dtype=np.complex128
        ).reshape(matrix.shape)
        object.__setattr__(self, "matrix", immutable)


@dataclass(frozen=True, slots=True)
class Periodic2DPlaneWaveHamiltonianResult(Periodic2DHamiltonianResult):
    """Retain the cosine-model plane-wave adapter result.

    Parameters
    ----------
    matrix
        Immutable dimensionless Hermitian matrix in plane-wave basis order.
    request
        Exact cosine-model plane-wave request represented by the matrix.
    maximum_duality_residual
        Maximum absolute direct--reciprocal duality residual checked by the adapter.

    Notes
    -----
    The campaign-facing constructor delegates matrix construction to the reusable
    ``PlaneWaveBlochHamiltonian2DConstructor`` and retains the exact cosine request and
    duality residual. This adapter does not duplicate the general continuum
    construction and is not itself a scientific model or retained operator.
    """

    request: Periodic2DPlaneWaveHamiltonianRequest
    maximum_duality_residual: float

    def __post_init__(self) -> None:
        """Validate the matrix and its plane-wave request identity."""
        Periodic2DHamiltonianResult.__post_init__(self)
        if type(self.request) is not Periodic2DPlaneWaveHamiltonianRequest:
            raise TypeError("request must be Periodic2DPlaneWaveHamiltonianRequest")
        if self.matrix.shape != (
            self.request.represented_dimension,
            self.request.represented_dimension,
        ):
            raise ValueError("matrix shape must match the plane-wave basis")
        if type(self.maximum_duality_residual) is not float:
            raise TypeError("maximum_duality_residual must be a built-in float")
        if (
            not np.isfinite(self.maximum_duality_residual)
            or self.maximum_duality_residual < 0.0
        ):
            raise ValueError("maximum_duality_residual must be finite and nonnegative")
        if self.maximum_duality_residual > self.request.duality_absolute_tolerance:
            raise ValueError("maximum_duality_residual exceeds the request tolerance")


@dataclass(frozen=True, slots=True)
class Periodic2DFiniteDifferenceHamiltonianResult(Periodic2DHamiltonianResult):
    """Retain a coordinate matrix with its declared grid and fiber identity.

    Parameters
    ----------
    matrix
        Immutable dimensionless Hermitian matrix in coordinate-grid order.
    request
        Exact cosine-model grid and reduced-momentum request represented by the matrix.

    Notes
    -----
    The result retains the cosine-model request, including grid ordering and the
    reduced momentum determining the Bloch seam phases, but the bare matrix has only
    the campaign's implicit dimensionless energy convention. Migration to reusable
    periodic2d representation ownership remains
    pending an explicit general state-space, basis, energy-reference, and provenance
    contract; those metadata are not inferred here.
    """

    request: Periodic2DFiniteDifferenceHamiltonianRequest

    def __post_init__(self) -> None:
        """Validate the matrix and its finite-difference request identity."""
        Periodic2DHamiltonianResult.__post_init__(self)
        if type(self.request) is not Periodic2DFiniteDifferenceHamiltonianRequest:
            raise TypeError(
                "request must be Periodic2DFiniteDifferenceHamiltonianRequest"
            )
        if self.matrix.shape != (
            self.request.represented_dimension,
            self.request.represented_dimension,
        ):
            raise ValueError("matrix shape must match the coordinate grid")


class Periodic2DPlaneWaveHamiltonianConstructor:
    """Construct finite plane-wave matrices in ``p``-outer, ``q``-inner order."""

    __slots__ = ()

    def execute(
        self, request: Periodic2DPlaneWaveHamiltonianRequest
    ) -> Periodic2DPlaneWaveHamiltonianResult:
        """Construct kinetic and cosine Fourier blocks without implicit truncation."""
        if type(request) is not Periodic2DPlaneWaveHamiltonianRequest:
            raise TypeError("request must be Periodic2DPlaneWaveHamiltonianRequest")
        model = request.model
        coefficients = (
            PlaneWaveFourierCoefficient2D((-1, -1), complex(model.lambda_xy / 4.0)),
            PlaneWaveFourierCoefficient2D((-1, 0), complex(model.lambda_x / 2.0)),
            PlaneWaveFourierCoefficient2D((-1, 1), complex(model.lambda_xy / 4.0)),
            PlaneWaveFourierCoefficient2D((0, -1), complex(model.lambda_y / 2.0)),
            PlaneWaveFourierCoefficient2D((0, 1), complex(model.lambda_y / 2.0)),
            PlaneWaveFourierCoefficient2D((1, -1), complex(model.lambda_xy / 4.0)),
            PlaneWaveFourierCoefficient2D((1, 0), complex(model.lambda_x / 2.0)),
            PlaneWaveFourierCoefficient2D((1, 1), complex(model.lambda_xy / 4.0)),
        )
        operator_model = PlaneWaveBlochHamiltonian2DModel(
            direct_lattice=model.direct_lattice,
            reciprocal_lattice=model.reciprocal_lattice,
            reciprocal_cutoff=request.cutoff,
            fourier_coefficients=coefficients,
            kinetic_scale=ScalarQuantity(1.0, Unitless()),
            state_space_identifier="periodic2d.cosine.spinless_scalar",
            basis_identifier="periodic2d.cosine.p_outer_q_inner",
            energy_reference="periodic2d.cosine.model_zero",
        )
        represented = PlaneWaveBlochHamiltonian2DConstructor().execute(
            PlaneWaveBlochHamiltonian2DRequest(
                model=operator_model,
                reduced_momentum=(
                    request.reduced_momentum_x,
                    request.reduced_momentum_y,
                ),
                duality_absolute_tolerance=request.duality_absolute_tolerance,
            )
        )
        return Periodic2DPlaneWaveHamiltonianResult(
            matrix=represented.represented_matrix.magnitude,
            request=request,
            maximum_duality_residual=represented.maximum_duality_residual,
        )


class Periodic2DFiniteDifferenceHamiltonianConstructor:
    """Construct centered Bloch finite-difference matrices on the square cell."""

    __slots__ = ()

    def execute(
        self, request: Periodic2DFiniteDifferenceHamiltonianRequest
    ) -> Periodic2DFiniteDifferenceHamiltonianResult:
        """Construct the Kronecker kinetic operator and sampled cosine potential."""
        if type(request) is not Periodic2DFiniteDifferenceHamiltonianRequest:
            raise TypeError(
                "request must be Periodic2DFiniteDifferenceHamiltonianRequest"
            )
        points = request.points_per_direction
        period = request.period
        kinetic_x = self._one_dimensional(request.reduced_momentum_x, points, period)
        kinetic_y = self._one_dimensional(request.reduced_momentum_y, points, period)
        identity = np.eye(points, dtype=np.complex128)
        matrix = np.kron(kinetic_x, identity) + np.kron(identity, kinetic_y)
        coordinate = np.arange(points, dtype=np.float64) * period / points
        model = request.model
        potential = (
            model.lambda_x * np.cos(coordinate)[:, None]
            + model.lambda_y * np.cos(coordinate)[None, :]
            + model.lambda_xy
            * np.cos(coordinate)[:, None]
            * np.cos(coordinate)[None, :]
        )
        matrix += np.diag(potential.ravel())
        return Periodic2DFiniteDifferenceHamiltonianResult(
            matrix=matrix,
            request=request,
        )

    @staticmethod
    def _one_dimensional(momentum: float, points: int, period: float) -> ComplexMatrix:
        spacing = period / points
        matrix = np.diag(np.full(points, 2.0 / spacing**2)).astype(np.complex128)
        off_diagonal = -1.0 / spacing**2
        matrix += np.diag(np.full(points - 1, off_diagonal), 1)
        matrix += np.diag(np.full(points - 1, off_diagonal), -1)
        matrix[0, -1] = off_diagonal * np.exp(-1j * momentum * period)
        matrix[-1, 0] = off_diagonal * np.exp(1j * momentum * period)
        return matrix
